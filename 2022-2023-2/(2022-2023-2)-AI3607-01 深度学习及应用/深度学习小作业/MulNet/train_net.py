import jittor as jt
from jittor import nn
from data_loader import get_dataset
from mul_net import MulNet
import argparse
import time
from animation import rolling_ball
import math

jt.flags.use_cuda = 1


def config():
    parser = argparse.ArgumentParser(description='Train MulNet')
    parser.add_argument('--train_path', type=str, default='./train_data.csv', help='file name for training data')
    parser.add_argument('--test_path', type=str, default='./test_data.csv', help='file name for testing data')
    parser.add_argument('--validate_only', action='store_true')
    parser.add_argument('--seed', type=int, default=151, help='Random seed')
    parser.add_argument('--lr', type=float, default=1e-5, help='Learning rate')
    parser.add_argument('--epochs', type=int, default=5000, help='Num of epochs')
    args = parser.parse_args()
    return args


def test(args, test_loader):
    model = MulNet()
    model.load('multiplier.pkl')
    test_acc = 0
    for x, y in test_loader:
        y_pred = model(x)
        test_acc += jt.sum((abs(y_pred / (y + 1e-7) - 1) < 0.01))
    print('test accuracy: {:.4f}'.format(test_acc / len(test_loader)))
    with open('log.txt', 'a') as logfile:
        logfile.writelines(time.strftime("%Y-%m-%d %H:%M:%S"))
        logfile.writelines(['\n\t', str(args.__dict__)])
        logfile.writelines(['\n\t', 'test acc:', str(test_acc / len(test_loader)), '\n\n'])


def train(args):
    train_loader, test_loader = get_dataset(train_path=args.train_path, test_path=args.test_path, seed=args.seed)
    model = MulNet()
    criterion = lambda d1, d2: jt.sum(jt.abs(d1 - d2))
    if args.validate_only:
        test(args, test_loader)
        return

    start_time = time.time()
    time_str = lambda t: time.strftime("%H:%M:%S", time.gmtime(t))
    num_epochs = args.epochs
    for epoch in range(num_epochs):
        for i, (x, y) in enumerate(train_loader):

            y_pred = model(x)
            loss = jt.sqrt(criterion(y_pred, y))
            optimizer = nn.Adam(model.parameters(), lr=args.lr * (math.log2(2 + 1e-7) - math.log2(1 + 1e-7 + min(num_epochs, 3 * epoch) / num_epochs)) * (1 if num_epochs > 2 * epoch else 1e-7))
            optimizer.zero_grad()
            optimizer.backward(loss)
            optimizer.step()

            if (i + 1) % 2 == 0:
                time_diff = time.time() - start_time
                rolling_ball(7, 0, f"[{time_str(time_diff)}<{time_str(time_diff * (num_epochs - epoch - 1) / (epoch + 1))}]Epoch [{epoch + 1}/{num_epochs}], Loss: {loss.item():.4f}")

    print('\n training completed.')
    model.save('multiplier.pkl')
    test(args, test_loader)


if __name__ == '__main__':
    train(config())
