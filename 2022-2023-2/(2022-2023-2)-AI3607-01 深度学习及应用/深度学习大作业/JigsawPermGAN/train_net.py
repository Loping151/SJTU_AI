import jittor as jt
from jittor import nn
from calc_utils import max_to_one, edge_loss, remap, zero_or_one, rank
from data_loader import get_dataset
from cifar import CIFAR10
from JPG import Encoder, Discriminator, JigsawSolver, Empty
from animation import rolling_ball
import numpy as np


def train_discriminator(cuts: int = 2,
                        num_epochs: int = 2,
                        current_size: int = 16,
                        data_root='data/',
                        discriminator=None,
                        test: bool = False,
                        **kwargs):
    print('Training discriminator')
    lr = kwargs.get('lr', 0.01)
    batch_size = kwargs.get('batch_size', 50)
    train_loader, test_loader = get_dataset(cuts, batch_size=batch_size, resize_piece=(current_size, current_size), with_original=False, data_root=data_root)
    if discriminator is None:
        discriminator = Discriminator(shape=(current_size * 2, current_size * 2))
    criterion = nn.MSELoss()
    optimizer_discriminator = nn.SGD(discriminator.parameters(), lr=lr)
    lr_scheduler_discriminator = jt.lr_scheduler.StepLR(optimizer_discriminator, step_size=6000, gamma=0.631)
    true_label = jt.ones(1, train_loader.batch_size)
    false_label = -1 * jt.ones(1, train_loader.batch_size)
    for epoch in range(num_epochs):
        for original, shuffled, _, _ in train_loader:
            pred_true = discriminator(original)
            pred_false = discriminator(shuffled)
            loss = criterion(pred_true, true_label) + criterion(pred_false, false_label)
            rolling_ball(7, 0, f"Epoch [{epoch + 1}/{num_epochs}], Loss: {loss.item():.4f}, Lr: {optimizer_discriminator.lr}")
            optimizer_discriminator.__setattr__('lr', max(optimizer_discriminator.lr, 1e-7))
            optimizer_discriminator.zero_grad()
            optimizer_discriminator.backward(loss)
            optimizer_discriminator.step()
            lr_scheduler_discriminator.step()
    print('\nDone trainin.')
    acc = 'None'
    if test:
        acc = test_discriminator(discriminator, test_loader)
    return discriminator, acc


def test_discriminator(discriminator, test_loader):
    print('Testing discriminator')
    acc = 0
    for original, shuffled, _, _ in test_loader:
        pred_true = zero_or_one(discriminator(original))
        acc += jt.sum(pred_true)
        pred_false = zero_or_one(discriminator(shuffled))
        acc += jt.sum(1 - pred_false)
        print(pred_true, pred_false)
    print('Done testing.')
    return str(acc / len(test_loader))


def train_encoder(num_epochs: int = 100,
                  current_size: int = 16,
                  data_root='data/',
                  encoder=None,
                  test: bool = False,
                  **kwargs
                  ):
    print('Training encoder')
    lr = kwargs.get('lr', 0.01)
    cifar10 = CIFAR10(root=data_root, train=True, download=False, resize=(current_size * 2, current_size * 2))
    if encoder is None:
        encoder = Encoder(shape=(current_size * 2, current_size * 2))
    criterion = nn.MSELoss()
    optimizer_encoder = nn.SGD(encoder.parameters(), lr=lr)
    lr_scheduler_encoder = jt.lr_scheduler.StepLR(optimizer_encoder, step_size=20, gamma=0.1)
    for epoch in range(num_epochs):
        for train_data, train_label in cifar10:
            x = train_data.transpose(0, 3, 1, 2) / 255
            x = jt.float32(x)
            pred_label = encoder(x, False)
            y = nn.one_hot(train_label, num_classes=10)
            loss = criterion(pred_label, y)
            rolling_ball(7, 0, f"Epoch [{epoch + 1}/{num_epochs}], Loss: {loss.item():.4f}, Lr: {optimizer_encoder.lr}")
            optimizer_encoder.__setattr__('lr', optimizer_encoder.lr)
            optimizer_encoder.zero_grad()
            optimizer_encoder.backward(loss)
            optimizer_encoder.step()
        lr_scheduler_encoder.step()
    print('\nDone training.')
    acc = 'None'
    if test:
        acc = test_encoder(encoder, current_size, data_root)
    return encoder, acc


def test_encoder(encoder, current_size, data_root):
    print('Testing encoder')
    cifar10test = CIFAR10(root=data_root, train=False, download=False, resize=(current_size * 2, current_size * 2))
    acc = 0
    for train_data, train_label in cifar10test:
        x = train_data.transpose(0, 3, 1, 2) / 255
        x = jt.float32(x)
        pred_label = encoder(x, False)
        y = nn.one_hot(train_label, num_classes=10)
        for v in range(len(y)):
            acc += np.sum(np.abs(max_to_one(pred_label[v]) - y[v])) / 2
    print('Done testing.')
    return str(1 - acc / 10000)


# TODO: better define a trainer class
def train_solver(cuts: int = 2,
                 num_epochs: int = 3,
                 current_size: int = 16,
                 data_root='data/',
                 prob: float = 1,
                 lr_step_size: int = 15000,
                 solver=None,
                 use_encoder: bool = True,
                 pretrained: bool = False,
                 use_edge_loss: bool = True,
                 edge_loss_weight: float = 1e-3,
                 use_discriminator_loss: bool = True,
                 discriminator_loss_weight: float = 1e-5,
                 test: bool = True,
                 **kwargs):
    lr = kwargs.get('lr', 0.1)
    batch_size = kwargs.get('batch_size', 10)
    args_encoder = kwargs.get('args_encoder', {})
    args_discriminator = kwargs.get('args_discriminator', {})
    train_loader, test_loader = get_dataset(cuts, data_root=data_root, batch_size=batch_size, resize_piece=(current_size, current_size), prob=prob)
    if pretrained:
        encoder, e_acc = train_encoder(*args_encoder, current_size=current_size, data_root=data_root)
    elif use_encoder:
        encoder, e_acc = Encoder(shape=(current_size * 2, current_size * 2)), 'None'
    else:
        encoder, e_acc = Empty(), 'None'
    if use_discriminator_loss:
        discriminator, d_acc = train_discriminator(*args_discriminator, cuts=cuts, current_size=current_size, data_root=data_root)
    else:
        discriminator, d_acc = Empty(), 'None'
    if solver is None:
        solver = JigsawSolver(shape=(current_size, current_size), use_encoder=use_encoder)
    criterion = nn.L1Loss()
    print('Training solver')
    optimizer_solver = nn.SGD(solver.parameters(), lr=lr)
    lr_scheduler_solver = jt.lr_scheduler.StepLR(optimizer_solver, step_size=lr_step_size, gamma=0.316)
    for epoch in range(num_epochs):
        for original, shuffled, train_data, train_seq in train_loader:
            if use_encoder:
                pred_seq = solver(encoder(train_data.view(train_data.shape[0], -1, current_size, current_size)))
            else:
                pred_seq = solver(train_data.view(train_data.shape[0], -1, current_size, current_size))
            loss = criterion(pred_seq, train_seq)
            if use_edge_loss:
                loss += edge_loss(remap(train_data, pred_seq, with_gradient=True), cuts=2) * edge_loss_weight
            if use_discriminator_loss:
                loss += jt.mean(remap(train_data, pred_seq, with_gradient=True) * discriminator(remap(train_data, pred_seq, with_gradient=False)).reshape(-1, 1, 1, 1)) * discriminator_loss_weight
            rolling_ball(7, 0, f"Epoch [{epoch + 1}/{num_epochs}], Loss: {loss.item():.4f}, Lr: {optimizer_solver.lr}")
            optimizer_solver.__setattr__('lr', max(optimizer_solver.lr, 1e-5))
            optimizer_solver.zero_grad()
            optimizer_solver.backward(loss)
            optimizer_solver.step()
            lr_scheduler_solver.step()
    print('\nDone training.')
    acc = 'None'
    if test:
        acc = test_solver(solver, encoder, test_loader, current_size=current_size, use_encoder=use_encoder)
    return [encoder, discriminator, solver], [e_acc, d_acc, acc]


def test_solver(solver, encoder, test_loader, current_size: int = 16, use_encoder: bool = True):
    print('Testing solver')
    total_acc = 0
    for original, shuffled, test_data, test_seq in test_loader:
        if use_encoder:
            pred_seq = solver(encoder(test_data.view(test_data.shape[0], -1, current_size, current_size)))
        else:
            pred_seq = solver(test_data.view(test_data.shape[0], -1, current_size, current_size))
        r = rank(pred_seq)
        test_acc = 0
        for i in range(len(r)):
            test_acc += np.sum(r[i] == np.array(test_seq[i]))
        total_acc += test_acc
    print('Done testing.')
    return 'test accuracy: {:.4f}'.format(total_acc / len(test_loader) / 4)


def inference(args):
    print('Inferencing')
    _, test_loader = get_dataset(args.cuts, data_root=args.data_root, batch_size=128, resize_piece=(args.current_size, args.current_size), prob=args.prob)
    if args.use_encoder:
        encoder = Encoder(shape=(args.current_size * 2, args.current_size * 2))
        encoder.load('logs/' + args.exp_name + '/encoder.pkl')
    else:
        encoder = Empty()
    solver = JigsawSolver(shape=(args.current_size, args.current_size))
    solver.load('logs/' + args.exp_name + '/solver.pkl')
    print('Done inference.')
    return test_solver(solver, encoder, test_loader, args.current_size, args.use_encoder)
