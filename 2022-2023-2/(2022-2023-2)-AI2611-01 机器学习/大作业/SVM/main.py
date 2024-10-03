# All the comments are written by myself, I hope you know. None of the code is generated, help was offered though.

import argparse
import os
import json
from typing import Any
import torch
from cuda_acc import cuda, cpu, has_cuda, np, cp
from train import train, inference
import time

if not os.path.exists('logs'):
    os.mkdir('logs')

if not os.path.exists('data'):
    os.makedirs('data')

device = cuda if has_cuda() else cpu  # Do not support override through config


def time_str(t):
    return time.strftime("%H:%M:%S", time.gmtime(t))


def set_seeds(seed):
    torch.manual_seed(seed)
    if torch.cuda.is_available():
        torch.cuda.manual_seed(seed)
        torch.cuda.manual_seed_all(seed)
    np.random.seed(seed)
    cp.random.seed(seed)


def config():
    parser = argparse.ArgumentParser(description='Train SVM')
    parser.add_argument('--exp_name', type=str, default='default', help='exp name')
    parser.add_argument('--data_path', type=str, default='./data', help='file path for data')
    parser.add_argument('--data_type', type=str, default='mnist', help='mnist or cifar10')
    parser.add_argument('--validate_only', action='store_true')
    parser.add_argument('--seed', type=int, default=151, help='random seed')
    parser.add_argument('--add_features', type=bool, default=True, help='To add features on datasets')
    parser.add_argument('--lm', type=float, default=1e-2,
                        help='learning lambda, inversely proportional to learning rate')
    parser.add_argument('--epochs', type=int, default=200, help='num of epochs')
    parser.add_argument('--cache_size', type=int, default=1024, help='batch size in SGD')
    parser.add_argument('--multi_kernel', type=bool, default=False, help='whether to use multi-kernel or not')
    parser.add_argument('--C', type=float, default=1.0, help='penalty parameter')
    parser.add_argument('--kernel', type=str, default='linear', help='kernel if single kernel')
    parser.add_argument('--kernel_args', type=Any, default=(), help='kernel args')
    parser.add_argument('--silence', type=bool, default=True, help='silent print')
    parser.add_argument('--PCA', type=bool, default=True, help='use PCA or not')
    parser.add_argument('--dim', type=int, default=512, help='PCA dimension')
    parser.add_argument('--mode', type=str, default='one_to_rest',
                        help='one_to_one or one_to_rest')
    parser.add_argument('--config', type=str, default=None, help='configuration file')
    args = parser.parse_args()
    if args.config is not None:
        with open(args.config, 'r') as f:
            config_dict = json.load(f)
            for k, v in config_dict.items():
                setattr(args, k, v)
    set_seeds(args.seed)
    if not os.path.exists('logs/' + args.exp_name):
        os.mkdir('logs/' + args.exp_name)
    with open('logs/' + args.exp_name + '/log.txt', 'a') as logfile:
        logfile.writelines([time.strftime("%Y-%m-%d %H:%M:%S"), '\n'])
        logfile.writelines(['\t', str(args.__dict__), '\n'])
    return args


def log_out(args, e):
    with open('logs/' + args.exp_name + '/log.txt', 'a') as logfile:
        logfile.writelines(['\t', str(e) + '\n'])
    print('Error logged')


if __name__ == '__main__':
    args = config()
    try:
        if args.validate_only:
            inference(args, device)
        else:
            train(args, device)
    except Exception as e:
        log_out(args, e)

# python main.py --config config/default.json
