from data_loader import load_data
from SVM import SVC151
from cuda_acc import cpu, cp, np
from img_process import PCA, histo_gram, mathcal_fetures, rgb_vector, hog_features


def train(args, device):
    lib = np if device is cpu else cp
    X_train, y_train, X_test, y_test = load_data(args.data_type)
    if args.add_features:
        if args.data_type == 'cifar10':
            X_train = lib.concatenate((X_train, rgb_vector(X_train), hog_features(X_train, fast_laod=True)), axis=1)
            X_test = lib.concatenate((X_test, rgb_vector(X_test), hog_features(X_test)), axis=1)
            print('Added features: rgb, hog.')
        X_train = lib.concatenate((X_train, histo_gram(X_train, 5), mathcal_fetures(X_train)), axis=1)
        X_test = lib.concatenate((X_test, histo_gram(X_test, 5), mathcal_fetures(X_test)), axis=1)
        print('Added features: hist, mathcal.')
    if args.PCA:
        pca = PCA(args.dim)
        X_train = pca.fit_reduce(X_train, device)
        X_test = pca.reduce(X_test)
        print(f'Done PCA. To {args.dim} dim.')
    print('Data ready.')
    print('Warm up')
    warm_up = SVC151(device, multi_kernel=args.multi_kernel, C=args.C, num_classes=10, mode=args.mode)
    warm_up.fit(X_train, y_train,
                cache_size=args.cache_size,
                epochs=1)
    print('Done.\nTraining')
    model = SVC151(device, multi_kernel=args.multi_kernel, C=args.C, num_classes=10, mode=args.mode)
    _, t = model.fit(X_train, y_train,
                     cache_size=args.cache_size,
                     epochs=args.epochs,
                     step_lambda=args.lm,
                     kernel=args.kernel,
                     kernel_args=args.kernel_args,
                     silence=args.silence
                     )
    print('Done.')
    print('Testing')
    test_acc = model.test(X_test, y_test)
    with open('logs/' + args.exp_name + '/log.txt', 'a') as logfile:
        logfile.writelines(['acc: ', str(test_acc), '\n'])
        logfile.writelines(['time cost: ', str(t), '\n'])
    print('Done. Results logged.')
    model.save('logs/' + args.exp_name + '/SVM.pkl')
    print('Model saved.')


def inference(args, device):
    print('Warning: should have potentional bug during inference.')
    print('Inferencing')
    _, _, X_test, y_test = load_data(args.data_type)
    model = SVC151(device, multi_kernel=args.multi_kernel, C=args.C, num_classes=10, mode=args.mode)
    model.fit(X_test, y_test,
              epochs=10,
              kernel=args.kernel,
              kernel_args=args.kernel_args,
              )
    model.load('logs/' + args.exp_name + '/SVM.pkl')  # w, b, theta will be ovwerwritten
    test_acc = model.test(X_test, y_test)
    with open('logs/' + args.exp_name + '/log.txt', 'a') as logfile:
        logfile.writelines(['inference acc: ', str(test_acc), '\n'])
    print('Done. Results logged.')
