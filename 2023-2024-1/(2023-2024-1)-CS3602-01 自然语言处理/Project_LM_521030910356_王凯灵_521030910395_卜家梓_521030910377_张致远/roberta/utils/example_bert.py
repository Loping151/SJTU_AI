import json
import re
from utils.vocab import Vocab, LabelVocab
from utils.word2vec import Word2vecUtils
from utils.evaluator import Evaluator
from transformers import BertTokenizer, BertModel, BertConfig

class Example():

    @classmethod
    def configuration(cls, root, train_path=None, word2vec_path=None):
        cls.evaluator = Evaluator()
        cls.word_vocab = Vocab(padding=True, unk=True, filepath=train_path)
        cls.word2vec = Word2vecUtils(word2vec_path)
        cls.label_vocab = LabelVocab(root)
        

    @classmethod
    def load_dataset(cls, data_path):
        tokenizer = BertTokenizer.from_pretrained('../pretrain_models/bert_wwm/vocab.txt')
        dataset = json.load(open(data_path, 'r'))
        examples = []
        is_train = ('train' in data_path)
        for di, data in enumerate(dataset):
            for ui, utt in enumerate(data):
                #if has_chinese(utt['asr_1best']):      #################################
                ex = cls(utt, f'{di}-{ui}',tokenizer, is_train)
                examples.append(ex)

                
        return examples
    
    

    def __init__(self, ex: dict, did, tokenizer, is_train=False):
        super(Example, self).__init__()
        
        def remove_non_chinese(text):
            pattern = re.compile(r'[^\u4e00-\u9fa5]')
            return pattern.sub('', text)
        
        def find_sub_list(list1,list2):
            idxs = len(list2)-len(list1)+1
            for idx in range(idxs):
                if list1 == list2[idx:len(list1)+idx]:
                    return idx
            return -1
        self.ex = ex
        self.did = did
        if is_train:
            self.utt = ex['manual_transcript']
        else:    
            self.utt = ex['asr_1best']
        self.slot = {}
        self.input_idx = tokenizer(self.utt)['input_ids'][1:-1]
        for label in ex['semantic']:
            act_slot = f'{label[0]}-{label[1]}'
            if len(label) == 3:
                self.slot[act_slot] = label[2]
                
        
        self.tags = ['O'] * len(self.input_idx)
        for slot in self.slot:
            value = tokenizer(self.slot[slot])['input_ids'][1:-1]
            bidx = find_sub_list(value,self.input_idx)
            if bidx != -1:
                self.tags[bidx: bidx + len(value)] = [f'I-{slot}'] * len(value)
                self.tags[bidx] = f'B-{slot}'
        self.slotvalue = [f'{slot}-{value}' for slot, value in self.slot.items()]

        l = Example.label_vocab
        self.tag_id = [l.convert_tag_to_idx(tag) for tag in self.tags]
        self.tag_id = self.tag_id
        
        
        ##