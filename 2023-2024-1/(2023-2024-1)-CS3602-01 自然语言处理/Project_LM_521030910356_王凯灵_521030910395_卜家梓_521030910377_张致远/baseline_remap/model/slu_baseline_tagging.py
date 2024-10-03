#coding=utf8
import torch
import torch.nn as nn
import torch.nn.utils.rnn as rnn_utils
import numpy as np
from utils.example import Example
import Levenshtein
from pypinyin import pinyin
import json

class SLUTagging(nn.Module):

    def __init__(self, config):
        super(SLUTagging, self).__init__()
        self.config = config
        self.cell = config.encoder_cell
        self.word_embed = nn.Embedding(config.vocab_size, config.embed_size, padding_idx=0)
        self.rnn = getattr(nn, self.cell)(config.embed_size, config.hidden_size // 2, num_layers=config.num_layer, bidirectional=True, batch_first=True)
        self.dropout_layer = nn.Dropout(p=config.dropout)
        self.output_layer = TaggingFNNDecoder(config.hidden_size, config.num_tags, config.tag_pad_idx)
        self.poi_names = Example.poi_names
        self.poi_names_pinyin = Example.poi_names_pinyin
        
        

    def forward(self, batch):
        tag_ids = batch.tag_ids
        tag_mask = batch.tag_mask
        input_ids = batch.input_ids
        lengths = batch.lengths

        embed = self.word_embed(input_ids)
        packed_inputs = rnn_utils.pack_padded_sequence(embed, lengths, batch_first=True, enforce_sorted=True)
        packed_rnn_out, h_t_c_t = self.rnn(packed_inputs)  # bsize x seqlen x dim
        rnn_out, unpacked_len = rnn_utils.pad_packed_sequence(packed_rnn_out, batch_first=True)
        hiddens = self.dropout_layer(rnn_out)
        tag_output = self.output_layer(hiddens, tag_mask, tag_ids)

        return tag_output

    def decode(self, label_vocab, batch,choice):
        batch_size = len(batch)
        labels = batch.labels
        output = self.forward(batch)
        prob = output[0]
        predictions = []
        for i in range(batch_size):
            pred = torch.argmax(prob[i], dim=-1).cpu().tolist()
            pred_tuple = []
            idx_buff, tag_buff, pred_tags = [], [], []
            pred = pred[:len(batch.utt[i])]
            slot_value_dict = {}
            for idx, tid in enumerate(pred):
                tag = label_vocab.convert_idx_to_tag(tid)
                pred_tags.append(tag)
                if (tag == 'O' or tag.startswith('B')) and len(tag_buff) > 0:
                    slot = '-'.join(tag_buff[0].split('-')[1:])
                    value = ''.join([batch.utt[i][j] for j in idx_buff])
                    idx_buff, tag_buff = [], []
                    if not slot in slot_value_dict.keys():
                        slot_value_dict[slot] = ''
                    slot_value_dict[slot] += value
                    #pred_tuple.append(f'{slot}-{value}')
                    if tag.startswith('B'):
                        idx_buff.append(idx)
                        tag_buff.append(tag)
                elif tag.startswith('I') or tag.startswith('B'):
                    idx_buff.append(idx)
                    tag_buff.append(tag)
            if len(tag_buff) > 0:
                slot = '-'.join(tag_buff[0].split('-')[1:])
                value = ''.join([batch.utt[i][j] for j in idx_buff])
                
                if not slot in slot_value_dict.keys():
                    slot_value_dict[slot] = ''
                slot_value_dict[slot] += value
                #pred_tuple.append(f'{slot}-{value}')
            for slot in slot_value_dict.keys():
                split = slot.split('-')
                slot1 = split[1]
                value = slot_value_dict[slot]
                if slot1 in ["poi名称", "poi修饰","poi目标","起点名称", "起点修饰","起点目标","终点名称","终点修饰","终点目标","途经点名称"] and not value in self.poi_names:
                    
                    value_pinyin = ''.join([item[0] for item in pinyin(value)])
                    distance_list =  []
                    distance_list_pinyin =  []
                    for poi in self.poi_names:
                        distance_list.append(Levenshtein.distance(poi, value))
                    for poi_pinyin in self.poi_names_pinyin:
                        distance_list_pinyin.append(Levenshtein.distance(poi_pinyin, value_pinyin))
                    
                    distance_final = np.array(distance_list)*3 + np.array(distance_list_pinyin)
                    
                    min_index = np.argmin(distance_final)
                    new_value = self.poi_names[min_index]
                    #if choice =='dev':
                    #    print(batch.utt[i],batch.labels[i],value+'->'+new_value)      
                else:
                    new_value = value 
                
                pred_tuple.append(f'{slot}-{new_value}')
            predictions.append(pred_tuple)
            
        if len(output) == 1:
            return predictions
        else:
            loss = output[1]
            return predictions, labels, loss.cpu().item()


class TaggingFNNDecoder(nn.Module):

    def __init__(self, input_size, num_tags, tag_pad_idx):
        super(TaggingFNNDecoder, self).__init__()
        self.num_tags = num_tags
        self.output_layer = nn.Linear(input_size, num_tags)
        self.loss_fct = nn.CrossEntropyLoss(ignore_index=tag_pad_idx) 

    def forward(self, hiddens, mask, labels=None):
        logits = self.output_layer(hiddens)
        logits += (1 - mask).unsqueeze(-1).repeat(1, 1, self.num_tags) * -1e32
        prob = torch.softmax(logits, dim=-1)
        if labels is not None:
            loss = self.loss_fct(logits.view(-1, logits.shape[-1]), labels.view(-1))
            return prob, loss
        return (prob, )