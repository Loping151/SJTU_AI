import pandas as pd
import jittor as jt
from jittor.dataset import Dataset, DataLoader


class MulDataset(Dataset):
    def __init__(self, csv_file):
        super().__init__()
        self.data = pd.read_csv(csv_file)

    def __len__(self):
        return len(self.data)

    def __getitem__(self, idx):
        sample = self.data.iloc[idx]
        a, b, label = sample["a"], sample["b"], sample["label"]
        return jt.array([a, b]), jt.array(label)


def get_dataset(train_path, test_path, seed=1919810):
    jt.misc.set_global_seed(seed)

    train_dataset = MulDataset(train_path)
    test_dataset = MulDataset(test_path)

    train_loader = DataLoader(train_dataset, batch_size=32, shuffle=True)
    test_loader = DataLoader(test_dataset, batch_size=32, shuffle=False)
    return train_loader, test_loader
