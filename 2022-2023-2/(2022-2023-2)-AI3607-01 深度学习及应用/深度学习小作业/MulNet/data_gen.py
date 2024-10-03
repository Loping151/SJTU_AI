import numpy as np
import pandas as pd

# seeding is a good habit
np.random.seed(114514)


def generator(maxlen=100):
    data = np.random.randint(-1 * maxlen, maxlen, size=(5000, 2))/maxlen
    label = np.multiply(data[:, 0], data[:, 1])
    data = np.column_stack((data, label))
    df = pd.DataFrame(data, columns=["a", "b", "label"])

    train_df = df[:4000]
    test_df = df[4000:]

    train_df.to_csv("train_data.csv", index=False)
    test_df.to_csv("test_data.csv", index=False)


if __name__ == '__main__':
    generator()
