import json, re

from utils.vocab import Vocab, LabelVocab
from utils.word2vec import Word2vecUtils
from utils.evaluator import Evaluator
from pypinyin import pinyin

class Example():

    @classmethod
    def configuration(cls, root, train_path=None, word2vec_path=None):
        cls.evaluator = Evaluator()
        cls.word_vocab = Vocab(padding=True, unk=True, filepath=train_path)
        cls.word2vec = Word2vecUtils(word2vec_path)
        cls.label_vocab = LabelVocab(root)
        
        pinyin_list = []
        
        poi_file = open('../data/lexicon/poi_name.txt', 'r')
        lines = poi_file.readlines()
        for i in range(len(lines)):
            lines[i] = lines[i].strip()
            pinyin_list.append(''.join([item[0] for item in pinyin(lines[i])]))
        
            
        cls.poi_names = lines
        cls.poi_names_pinyin = pinyin_list

    @classmethod
    def load_dataset(cls, data_path):   
                             
        def has_chinese(text):
            pattern = re.compile(r'[\u4e00-\u9fa5]')
            return bool(pattern.search(text))
        
        dataset = json.load(open(data_path, 'r'))
        examples = []
        # NOTE: exp for history info
        # for di, data in enumerate(dataset):
        #     asr_1best = ''
        #     hist_semantic = []
        #     for ui, utt in enumerate(data):
        #         if 'train' in data_path:
        #             if utt['utt_id'] > 1:
        #                 asr_1best += ','
        #             utt['out_lenth'] = len(utt['asr_1best'])
        #             asr_1best += utt['asr_1best']
        #             utt['asr_1best'] = asr_1best
        #             utt['semantic'] += hist_semantic
        #             hist_semantic = utt['semantic']
        is_train = 'train' in data_path
        for di, data in enumerate(dataset):
            for ui, utt in enumerate(data):
                ex = cls(utt, f'{di}-{ui}', is_train)
                # if has_chinese(utt['manual_transcript']) and (ex.valid or not ('train' in data_path)):
                # if ex.valid or not ('train' in data_path):
                examples.append(ex)
        return examples

    def __init__(self, ex: dict, did, is_train):
        super(Example, self).__init__()
        self.ex = ex
        self.did = did
        self.valid = True
        """code review example
        ex['utt_id'] : current round of dialogue
        ex['manual_transcript'] : input content, by human?
        ex['asr_1best'] : input content from ASR
        ex['semantic'] : semantic label
        For example, 
            {'utt_id': 1,
            'manual_transcript': '去滨州职业技术学校',
            'asr_1best': '去冰粥职业技术学校',
            'semantic': [['inform', '操作', '导航'], ['inform', '终点名称', '滨州职业技术学校']]}
        """
        if is_train:
            self.utt = ex['manual_transcript'].replace('(unknown)', '') # .replace('(noise)', '').replace('(robot)', '').replace('(dialect)', '').replace('(side)', '')
        else:
            self.utt = ex['asr_1best']
        self.slot = {}
        for label in ex['semantic']:
            act_slot = f'{label[0]}-{label[1]}'
            if len(label) == 3:
                self.slot[act_slot] = label[2]
        self.tags = ['O'] * len(self.utt)
        for slot in self.slot:
            value = self.slot[slot]
            bidx = self.utt.find(value)
            if bidx != -1:
                self.tags[bidx: bidx + len(value)] = [f'I-{slot}'] * len(value)
                self.tags[bidx] = f'B-{slot}'
            else:
                self.valid = False
        self.slotvalue = [f'{slot}-{value}' for slot, value in self.slot.items()]
        self.input_idx = [Example.word_vocab[c] for c in self.utt]
        l = Example.label_vocab # what was this guy thinking when he do this?
        self.tag_id = [l.convert_tag_to_idx(tag) for tag in self.tags] # tag is like 'B-inform-操作' 'I-inform-操作' 'O'
