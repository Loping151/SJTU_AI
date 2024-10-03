import jittor as jt
from jittor import nn
from data_loader import get_dataset
from jcnn import JCNN
import argparse
import time
from animation import rolling_ball
import numpy as np
import json
import os

flags = jt.Flags()
flags.use_cuda = 1
flags.use_tensorcore = 1
flags.para_opt_level = 5
flags.use_parallel_op_compiler = 32

jt.flags = flags

if not os.path.exists('logs'):
    os.mkdir('logs')


def config():
    parser = argparse.ArgumentParser(description='Train JCNN')
    parser.add_argument('--exp_name', type=str, default='default', help='exp name for training')
    parser.add_argument('--train_path', type=str, default='data/', help='file name for training data')
    parser.add_argument('--test_path', type=str, default='data/', help='file name for testing data')
    parser.add_argument('--validate_only', action='store_true')
    parser.add_argument('--seed', type=int, default=151, help='Random seed')
    parser.add_argument('--lr', type=float, default=1e-5, help='Learning rate')
    parser.add_argument('--epochs', type=int, default=100, help='Num of epochs')
    parser.add_argument('--batch_size', type=int, default=32, help='Size of batches')
    parser.add_argument('--data_seg', type=bool, default=False, help='Whether to segment the training data')
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
    return args


def test(args, test_loader):
    model = JCNN()
    model.load('logs/' + args.exp_name + '/jcnn.pkl')
    test_acc = 0
    for x, y in test_loader:
        y_pred = model(x)
        for i in range(len(y)):
            test_acc += 1 if jt.max(y_pred[i]).item() == y_pred[i][y[i]].item() else 0
    print('test accuracy: {:.4f}'.format(test_acc / len(test_loader) / test_loader.batch_size))
    with open('logs/' + args.exp_name + '/log.txt', 'a') as logfile:
        logfile.writelines(time.strftime("%Y-%m-%d %H:%M:%S"))
        logfile.writelines(['\n\t', str(args.__dict__)])
        logfile.writelines(['\n\t', 'test acc:', str(test_acc / len(test_loader) / test_loader.batch_size), '\n\n'])


def train(args):
    train_loader, test_loader = get_dataset(train_path=args.train_path, test_path=args.test_path, download=False, batch_size=args.batch_size, data_seg=args.data_seg)
    model = JCNN()
    criterion = nn.MSELoss()
    optimizer = nn.Adam(model.parameters(), lr=args.lr)
    lr_scheduler = jt.lr_scheduler.StepLR(optimizer, step_size=10, gamma=0.1)
    if args.validate_only:
        test(args, test_loader)
        return

    start_time = time.time()
    time_str = lambda t: time.strftime("%H:%M:%S", time.gmtime(t))
    num_epochs = args.epochs
    for epoch in range(num_epochs):
        for i, (x, y) in enumerate(train_loader):
            y = nn.one_hot(y, num_classes=10)
            y_pred = model(x)
            loss = criterion(y_pred, y)
            optimizer.__setattr__('lr', optimizer.lr)
            optimizer.zero_grad()
            optimizer.backward(loss)
            optimizer.step()

            if (i + 1) % 30 == 0:
                time_diff = time.time() - start_time
                rolling_ball(7, 0, f"[{time_str(time_diff)}<{time_str(time_diff * (num_epochs - epoch - 1) / (epoch + 1))}]Epoch [{epoch + 1}/{num_epochs}], Loss: {loss.item():.4f}")

        lr_scheduler.step()

    print('\n training completed.')
    model.save('logs/' + args.exp_name + '/jcnn.pkl')
    test(args, test_loader)


if __name__ == '__main__':
    train(config())

# example: python train_net.py --config config/exp.json
