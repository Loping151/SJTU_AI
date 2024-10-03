#coding=utf8
import torch
import torch.nn as nn
from transformers import BertTokenizer, BertModel, BertConfig
import json
from utils.example_bert import Example


class RoBERTa(nn.Module):

    def __init__(self, config):
        super(RoBERTa, self).__init__()
        self.config = config
        self.cell = config.encoder_cell
        
        self.roberta_config = BertConfig.from_pretrained('../pretrain_models/roberta/config.json')
        self.tokenizer = BertTokenizer.from_pretrained('../pretrain_models/roberta/vocab.txt')
        self.bertmodel = BertModel.from_pretrained('../pretrain_models/roberta/pytorch_model.bin', config=self.roberta_config)
        
        self.output_layer =nn.Sequential(
        nn.Linear(self.roberta_config.hidden_size, 1024),
        nn.ReLU(),
        nn.Dropout(0.2),
        nn.Linear(1024, 256),
        nn.ReLU(),
        nn.Dropout(0.2),
        nn.Linear(256, self.config.num_tags )
        )
        
            
        self.loss_fct = nn.CrossEntropyLoss(ignore_index=self.config.tag_pad_idx) 

    def forward(self, batch):
        utt = batch.utt
        tokens = self.tokenizer(utt, return_tensors="pt",padding=True) 
        for key in tokens.keys():
            tokens[key] = tokens[key].to(self.bertmodel.device)
            
        bert_output = self.bertmodel(**tokens)
        hidden = bert_output.last_hidden_state
        batch_size, token_size, hidden_dim = hidden.shape
        hidden.reshape(batch_size*token_size, hidden_dim)
        output = self.output_layer(hidden)
        logits = output.reshape(batch_size, token_size, self.config.num_tags)[:,1:-1,:] 
        if logits.shape[1]!=batch.tag_mask.shape[1]:
            print(tokens, batch.tag_ids, batch.utt)       
        logits += (1 - batch.tag_mask).unsqueeze(-1).repeat(1, 1, self.config.num_tags) * -1e32
        probs = torch.softmax(logits, dim=-1)
        
        if batch.tag_ids is None:
            return [probs]
        else:
            loss = self.loss_fct(logits.reshape(-1, logits.shape[-1]),  batch.tag_ids.reshape(-1))
            return probs, loss
    def decode(self, label_vocab, batch):
        batch_size = len(batch)
        labels = batch.labels
        output = self.forward(batch)
        prob = output[0]
        
        predictions = []
        for i in range(batch_size):

            pred = torch.argmax(prob[i], dim=-1).cpu().tolist()
            pred_tuple = []
            idx_buff, tag_buff, pred_tags = [], [], []
            if isinstance(pred, list):
                pred = pred[:len(batch.utt[i])]
            else:
                pred = [pred]
            
            for idx, tid in enumerate(pred):
                tag = label_vocab.convert_idx_to_tag(tid)
                pred_tags.append(tag)
                if (tag == 'O' or tag.startswith('B')) and len(tag_buff) > 0:
                    slot = '-'.join(tag_buff[0].split('-')[1:])
                    value = ''.join([self.tokenizer.convert_ids_to_tokens(batch.input_ids[i][j].item()).replace("##", "") for j in idx_buff])
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
                value = ''.join([self.tokenizer.convert_ids_to_tokens(batch.input_ids[i][j].item()).replace("##", "") for j in idx_buff])
                pred_tuple.append(f'{slot}-{value}')
            predictions.append(pred_tuple)
            
       
        if len(output) == 1:
            return predictions
        else:
            loss = output[1] 
            return predictions, labels, loss.cpu().item()


