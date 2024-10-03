import math
import torch
import torch.nn as nn
from utils.example import Example
import json
import numpy as np


class PositionalEncoding(torch.nn.Module):
    def __init__(self, d_model, max_len=5000):
        super(PositionalEncoding, self).__init__()
        pe = torch.zeros(max_len, d_model)
        position = torch.arange(0, max_len, dtype=torch.float).unsqueeze(1)
        div_term = torch.exp(torch.arange(0, d_model, 2).float() * (-np.log(10000.0) / d_model))
        pe[:, 0::2] = torch.sin(position * div_term)
        pe[:, 1::2] = torch.cos(position * div_term)
        pe = pe.unsqueeze(0).transpose(0, 1)
        self.register_buffer('pe', pe)

    def forward(self, x):
        x = x + self.pe[:x.size(0), :]
        return x



class OurTransformer(nn.Module):
    
    def __init__(self, config):
        super(OurTransformer, self).__init__()
        self.config = config
        self.transformer = nn.Transformer(
            nhead= self.config.num_head,
            d_model= self.config.embed_size,
            num_encoder_layers = self.config.num_layer,
            num_decoder_layers = self.config.num_layer,
            dim_feedforward = self.config.hidden_size,
            dropout = self.config.dropout,
            batch_first=True,
        )
        self.positional_encoding = PositionalEncoding(self.config.embed_size)
        self.tag_embedding_layer = nn.Embedding(self.config.num_tags, self.config.embed_size, padding_idx=self.config.tag_pad_idx)
        self.word_embedding_layer = nn.Embedding(self.config.vocab_size, self.config.embed_size, padding_idx=self.config.tag_pad_idx)
        self.dropout_layer = nn.Dropout(p=self.config.dropout)        
        self.output_layer = nn.Linear(self.config.embed_size, self.config.num_tags)
        self.poi_names = Example.poi_names
        self.poi_names_pinyin = Example.poi_names_pinyin
        self.loss_fct = nn.CrossEntropyLoss(ignore_index=self.config.tag_pad_idx) 
    
    
    def forward(self, batch, step=0):
        tag_ids, tag_mask, input_ids, lengths = batch.tag_ids, batch.tag_mask, batch.input_ids, batch.lengths
        length = tag_ids.size(1)
        word_embedding, tag_embedding = self.word_embedding_layer(input_ids), self.tag_embedding_layer(tag_ids[:, :-1])
        tag_mask_bool = (tag_mask == 0)
        logits = None

        # NOTE:add and 0 to disable teacher forcing
        if self.training: # and 0: # and ((step + 1) % 10 != 0 and step < 75):
            # when training, we use tag_ids as tgt to perform teacher forcing
            tgt_sequence_mask = self.transformer.generate_square_subsequent_mask(length-1).to(tag_embedding.device)
            # emb = self.transformer(src=self.positional_encoding(word_embedding), tgt=self.positional_encoding(tag_embedding), tgt_mask=tgt_sequence_mask)
            emb = self.transformer(src=self.positional_encoding(word_embedding), tgt=self.positional_encoding(tag_embedding), tgt_mask=tgt_sequence_mask, src_key_padding_mask=tag_mask_bool, tgt_key_padding_mask=tag_mask_bool[:, :-1])
            out = self.dropout_layer(emb)
            logits = self.output_layer(out)
        else:
            # when testing, we use generated tags as tgt
            tmp_ids = torch.ones((tag_ids.size(0), 1), dtype=torch.long).to(tag_ids.device) * 2 # note that we use 2 as the token id of <s>
            for i in range(length - 2):
                tgt_sequence_mask = self.transformer.generate_square_subsequent_mask(i+1).to(tag_embedding.device)
                emb = self.tag_embedding_layer(tmp_ids)
                # pred = self.transformer(src=self.positional_encoding(word_embedding), tgt=self.positional_encoding(emb), tgt_mask=tgt_sequence_mask)
                pred = self.transformer(src=self.positional_encoding(word_embedding), tgt=self.positional_encoding(emb), tgt_mask=tgt_sequence_mask, src_key_padding_mask=tag_mask_bool, tgt_key_padding_mask=tag_mask_bool[:, :i+1])
                out = self.dropout_layer(pred[:, [-1], :])
                tmp_logits = self.output_layer(out)
                logits = tmp_logits if logits is None else torch.cat([logits, tmp_logits], dim=1)
                tmp_ids = torch.concat([tmp_ids, torch.argmax(tmp_logits, dim=-1)], dim=1)
            emb = self.tag_embedding_layer(tmp_ids)
            tgt_sequence_mask = self.transformer.generate_square_subsequent_mask(length-1).to(tag_embedding.device)
            # pred = self.transformer(src=self.positional_encoding(word_embedding), tgt=self.positional_encoding(emb), tgt_mask=tgt_sequence_mask)
            pred = self.transformer(src=self.positional_encoding(word_embedding), tgt=self.positional_encoding(emb), tgt_mask=tgt_sequence_mask, src_key_padding_mask=tag_mask_bool, tgt_key_padding_mask=tag_mask_bool[:, :-1])
            out = self.dropout_layer(pred[:, [-1], :])
            logits = torch.cat([logits, self.output_layer(out)], dim=1)

        logits += (1 - tag_mask[:, 1:]).unsqueeze(-1).repeat(1, 1, self.config.num_tags) * -1e32
        
        # if self.training:
        #     for i in range(1):
        #         print(torch.argmax(logits[i], dim=-1).tolist(), tag_ids[i][1:].tolist())
        loss = None
        if tag_ids is not None:
            loss = self.loss_fct(logits.reshape(-1, logits.shape[-1]), tag_ids[:, 1:].reshape(-1))
        prob = torch.softmax(logits, dim=-1)
        return prob, loss
    
    
    # 继承baseline的decode
    def decode(self, label_vocab, batch):
        batch_size = len(batch)
        labels = batch.labels
        output = self.forward(batch)
        prob = output[0] 
        predictions = []
        for i in range(batch_size):
            # prob[i][2, 3] = torch.ones_like(prob[i][2, 3]) * -1e32
            pred = torch.argmax(prob[i], dim=-1).cpu().tolist() # we know that the last token is <s>, so we ignore it
            # print(pred, batch.tag_ids[i][1:])
            pred_tuple = []
            idx_buff, tag_buff, pred_tags = [], [], []
            pred = pred[:len(batch.utt[i])] # no begin and end token
            # NOTE: Formalize
            # for i in range(1, len(pred)):
            #     # if pred[i] < 3 and pred[i-1] % 2 == 0:
            #     #     pred[i-1] = 1
            #     if pred[i] > 3:
            #         if pred[i] % 2 == 1 and pred[i-1] != pred[i]:
            #             pred[i-1] = pred[i] - 1
            for idx, tid in enumerate(pred):
                tag = label_vocab.convert_idx_to_tag(tid)
                pred_tags.append(tag)
                if (tag == 'O' or tag.startswith('B')) and len(tag_buff) > 0:
                    slot = '-'.join(tag_buff[0].split('-')[1:])
                    value = ''.join([batch.utt[i][j] for j in idx_buff])
                    idx_buff, tag_buff = [], []
                    pred_tuple.append(f'{slot}-{value}')
                    if tag.startswith('B'):
                        idx_buff.append(idx)
                        tag_buff.append(tag)
                elif tag.startswith('I') or tag.startswith('B'):
                    idx_buff.append(idx)
                    tag_buff.append(tag)
            if len(tag_buff) > 0:
                slot = '-'.join(tag_buff[0].split('-')[1:])
                value = ''.join([batch.utt[i][j] for j in idx_buff])
                pred_tuple.append(f'{slot}-{value}')
            # print(pred_tags, labels[i])
            predictions.append(pred_tuple)
        
        if len(output) == 1:
            return predictions
        else:
            loss = output[1]
            return predictions, labels, loss.cpu().item()


    

