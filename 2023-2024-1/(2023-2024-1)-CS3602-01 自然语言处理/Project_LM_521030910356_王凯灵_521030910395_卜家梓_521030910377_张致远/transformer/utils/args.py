#coding=utf-8
import argparse
import sys


def init_args(params=sys.argv[1:]):
    arg_parser = argparse.ArgumentParser()
    arg_parser = add_argument_base(arg_parser)
    opt = arg_parser.parse_args(params)
    return opt


def add_argument_base(arg_parser):
    #### General configuration ####
    arg_parser.add_argument('--dataroot', default='../data', help='root of data')
    arg_parser.add_argument('--word2vec_path', default='../word2vec-768.txt', help='path of word2vector file path')
    arg_parser.add_argument('--seed', default=998, type=int, help='Random seed')
    arg_parser.add_argument('--device', type=int, default=1, help='Use which device: -1 -> cpu ; the index of gpu o.w.')
    arg_parser.add_argument('--testing', action='store_true', help='training or evaluation mode')
    #### Training Hyperparams ####
    arg_parser.add_argument('--batch_size', default=64, type=int, help='Batch size')
    arg_parser.add_argument('--lr', type=float, default=2e-5, help='learning rate')
    arg_parser.add_argument('--max_epoch', type=int, default=100, help='terminate after maximum epochs')
    #### Common Encoder Hyperparams ####
    arg_parser.add_argument('--encoder_cell', default='LSTM', choices=['LSTM', 'GRU', 'RNN'], help='root of data')
    arg_parser.add_argument('--dropout', type=float, default=0.001, help='feature dropout rate')
    arg_parser.add_argument('--embed_size', default=768, type=int, help='Size of word embeddings')
    arg_parser.add_argument('--hidden_size', default=32, type=int, help='hidden size')
    arg_parser.add_argument('--num_layer', default=3, type=int, help='number of layer')
    arg_parser.add_argument('--num_head', default=3, type=int, help='number of head')
    return arg_parser