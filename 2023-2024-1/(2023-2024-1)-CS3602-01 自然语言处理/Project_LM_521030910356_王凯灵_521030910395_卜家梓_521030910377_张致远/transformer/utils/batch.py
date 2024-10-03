#-*- coding:utf-8 -*-
import torch


def from_example_list(args, ex_list, device='cpu', train=True):
    ex_list = sorted(ex_list, key=lambda x: len(x.input_idx), reverse=True)
    batch = Batch(ex_list, device)
    pad_idx = args.pad_idx
    tag_pad_idx = args.tag_pad_idx

    batch.utt = [ex.utt for ex in ex_list]
    input_lens = [len(ex.input_idx) for ex in ex_list]
    max_len = max(input_lens)
    input_ids = [[0] + ex.input_idx + [1] + [pad_idx] * (max_len - len(ex.input_idx)) for ex in ex_list] # 我定义词令牌为0
    batch.input_ids = torch.tensor(input_ids, dtype=torch.long, device=device)
    batch.lengths = [leni + 2 for leni in input_lens]
    batch.did = [ex.did for ex in ex_list]

    if train:
        batch.labels = [ex.slotvalue for ex in ex_list] # 32 sets of slot-value pairs, ie ['inform-操作-导航', 'inform-终点名称-绍兴文理学院']
        tag_lens = [len(ex.tag_id) for ex in ex_list] # 字数，比如 '导航到凯里大十字' 就是8
        max_tag_lens = max(tag_lens) # 需要用于padding, +1是为了给令牌预留位置，我定义令牌为2。应该和上面的max_len一样？为什么要重复
        tag_ids = [[2] + ex.tag_id + [3] + [tag_pad_idx] * (max_tag_lens - len(ex.tag_id)) for ex in ex_list] # padding过的tag_id
        tag_mask = [[1] + [1] * len(ex.tag_id) + [1] + [0] * (max_tag_lens - len(ex.tag_id)) for ex in ex_list] # 有效tag_mask
        batch.tag_ids = torch.tensor(tag_ids, dtype=torch.long, device=device)
        batch.tag_mask = torch.tensor(tag_mask, dtype=torch.float, device=device)
    else:
        # I did not made modifications to this part yet, because we do not use it
        batch.labels = None
        batch.tag_ids = None
        tag_mask = [[1] * len(ex.input_idx) + [0] * (max_len - len(ex.input_idx)) for ex in ex_list]
        batch.tag_mask = torch.tensor(tag_mask, dtype=torch.float, device=device)

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