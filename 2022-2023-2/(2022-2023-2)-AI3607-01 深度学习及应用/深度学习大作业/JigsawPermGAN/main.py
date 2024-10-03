from typing import Any
import jittor as jt
from data_loader import get_dataset
import argparse
from train_net import train_solver, inference
import numpy as np
import json
import time
import os

flags = jt.Flags()
flags.log_silent = 1
flags.use_cuda = 1
flags.use_tensorcore = 1
flags.para_opt_level = 5
flags.use_parallel_op_compiler = 32

jt.flags = flags

if not os.path.exists('logs'):
    os.mkdir('logs')
if not os.path.exists('pics'):
    os.mkdir('pics')
if not os.path.exists('data'):
    os.makedirs('data')
    print('No data in the default path. Downloading for you.')
    get_dataset('data/', download=True)
    print('Done.')

time_str = lambda t: time.strftime("%H:%M:%S", time.gmtime(t))


def config():
    parser = argparse.ArgumentParser(description='Train JPG')
    parser.add_argument('--exp_name', type=str, default='default', help='exp name for training')
    parser.add_argument('--data_root', type=str, default='./data', help='root for testing data')
    parser.add_argument('--prob', type=float, default=1, help='prob to acquire each shuffle of an image')
    parser.add_argument('--lr_step_size', type=int, default=15000, help='lr step size')
    parser.add_argument('--validate_only', action='store_true')
    parser.add_argument('--seed', type=int, default=151, help='Random seed')
    parser.add_argument('--cuts', type=int, default=2, help='Jigsaw cuts for training')
    parser.add_argument('--num_epochs', type=int, default=2, help='Epochs for training')
    parser.add_argument('--current_size', type=int, default=16, help='Resize of jigsaw pieces')
    parser.add_argument('--use_encoder', type=bool, default=True, help='Whether to use encoder')
    parser.add_argument('--pretrained', type=bool, default=False, help='Whether to pretrain encoder')
    parser.add_argument('--use_edge_loss', type=bool, default=False, help='Use edge loss or not')
    parser.add_argument('--use_discriminator_loss', type=bool, default=False, help='Use discrimiter loss or not')
    parser.add_argument('--edge_loss_weight', type=float, default=1e-3, help='Edge loss weight')
    parser.add_argument('--discriminator_loss_weight', type=float, default=1e-5, help='Discriminator loss weight')
    parser.add_argument('--additional', type=Any, default={}, help='Read code for detail')
    parser.add_argument('--config', type=str, default=None, help='Configuration file')
    args = parser.parse_args()
    if args.config is not None:
        with open(args.config, 'r') as f:
            config_dict = json.load(f)
            for k, v in config_dict.items():
                setattr(args, k, v)

    jt.misc.set_global_seed(args.seed)
    np.random.seed(args.seed)
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


def JPG(args):
    if args.validate_only:
        with open('logs/' + args.exp_name + '/log.txt', 'a') as logfile:
            logfile.writelines(['\t', 'inference acc:', inference(args), '\n'])
        return
    models, acc = train_solver(cuts=args.cuts,
                               num_epochs=args.num_epochs,
                               current_size=args.current_size,
                               data_root=args.data_root,
                               prob=args.prob,
                               lr_step_size=args.lr_step_size,
                               solver=None,
                               use_encoder=args.use_encoder,
                               pretrained=args.pretrained,
                               use_edge_loss=args.use_edge_loss,
                               edge_loss_weight=args.edge_loss_weight,
                               use_discriminator_loss=args.use_discriminator_loss,
                               discriminator_loss_weight=args.discriminator_loss_weight,
                               test=True,
                               **args.additional)

    models[0].save('logs/' + args.exp_name + '/encoder.pkl')
    if args.use_encoder:
        models[1].save('logs/' + args.exp_name + '/discriminator.pkl')
    if args.use_discriminator_loss:
        models[2].save('logs/' + args.exp_name + '/solver.pkl')
    with open('logs/' + args.exp_name + '/log.txt', 'a') as logfile:
        logfile.writelines(['\t', 'encoder acc:', acc[0], '\n'])
        logfile.writelines(['\t', 'discriminator acc:', acc[1], '\n'])
        logfile.writelines(['\t', 'test acc:', acc[2], '\n'])


if __name__ == '__main__':
    args = config()
    JPG(args)
    # try:
    #     JPG(args)
    # except Exception as e:
    #     log_out(args, e)

# example: python main.py --config config/default.json
