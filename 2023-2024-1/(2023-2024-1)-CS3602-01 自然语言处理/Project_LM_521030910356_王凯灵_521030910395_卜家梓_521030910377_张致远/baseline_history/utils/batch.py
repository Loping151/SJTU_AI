#-*- coding:utf-8 -*-
import torch


def from_example_list(args, ex_list, device='cpu', train=True):
    pad_idx = args.pad_idx
    tag_pad_idx = args.tag_pad_idx
    batch = Batch(ex_list, device)
    batch.max_seq_lenth = 0
    batch.max_word_lenth = 0
    batch.utt = []
    
    utt_list = []
    input_lens_list = []
    lenth_list = []
    for exs in ex_list:
        batch.max_seq_lenth = max(batch.max_seq_lenth,len(exs))
        for ex in exs:
            batch.max_word_lenth = max(batch.max_word_lenth,len(ex.input_idx))
        
    batch.input_ids = torch.zeros((len(ex_list), batch.max_seq_lenth ,batch.max_word_lenth),dtype=torch.long, device=device)
    batch.tag_mask = torch.zeros((len(ex_list), batch.max_seq_lenth, batch.max_word_lenth),dtype=torch.long, device=device)  
    batch.word_lengths = torch.ones((len(ex_list), batch.max_seq_lenth),dtype=torch.int64, device='cpu')  
    batch.seq_lengths = []    
    if train:
        batch.tag_ids = torch.zeros((len(ex_list), batch.max_seq_lenth, batch.max_word_lenth),dtype=torch.long, device=device)  
        batch.labels = []
    else:
        batch.tag_ids = None
        batch.labels = None
        
        
    for i in range(len(ex_list)):
        exs = ex_list[i]
        #exs = sorted(exs, key=lambda x: len(x.input_idx), reverse=True)
        utt_list_tmp = [ex.utt for ex in exs] # + [None for _ in range(max_word_lenth - len(exs))]
        input_ids = [ex.input_idx + [pad_idx] * ( batch.max_word_lenth - len(ex.input_idx)) for ex in exs]
        tag_mask = [[1] * len(ex.tag_id) + [0] * ( batch.max_word_lenth - len(ex.input_idx)) for ex in exs]
        word_lengths = [len(ex.input_idx) for ex in exs]
        batch.input_ids[i,0:len(exs),:] = torch.tensor(input_ids,dtype=torch.long, device=device)
        batch.tag_mask[i,0:len(exs),:] = torch.tensor(tag_mask,dtype=torch.long, device=device)
        batch.word_lengths[i,0:len(exs)] = torch.tensor(word_lengths,dtype=torch.int64, device='cpu')
        batch.seq_lengths.append(len(exs))
        batch.utt.append([ex.utt for ex in exs])
        
        if train:
            tag_ids = [ex.tag_id + [tag_pad_idx] * ( batch.max_word_lenth - len(ex.tag_id)) for ex in exs]
            batch.tag_ids[i,0:len(exs),:] = torch.tensor(tag_ids,dtype=torch.long, device=device)
            batch.labels.append([ex.slotvalue for ex in exs])

    return batch


class Batch():

    def __init__(self, examples, device):
        super(Batch, self).__init__()

        self.examples = examples
        self.device = device

    def __len__(self):
        return len(self.examples)

    def __getitem__(self, idx):
        return self.examples[idx]