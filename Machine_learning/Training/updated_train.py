import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import DataLoader, Dataset
import pandas as pd
import numpy as np
import argparse
import os

parser = argparse.ArgumentParser()
parser.add_argument('--learning_rate', type=float, default=0.001, help="Learning rate for the optimizer")
parser.add_argument('--batch_size', type=int, default=32, help="Batch size for training")
parser.add_argument('--epochs', type=int, default=10, help="Number of training epochs")
parser.add_argument('--data_dir', type=str, default='/opt/ml/input/data/train', help="Training data directory")
parser.add_argument('--model_dir', type=str, default='/opt/ml/model', help="Model output directory")
args = parser.parse_args()

class LSTMClassifier(nn.Module):
    def __init__(self, input_dim, hidden_dim, output_dim):
        super(LSTMClassifier, self).__init__()
        self.lstm = nn.LSTM(input_dim, hidden_dim, batch_first=True)
        self.fc = nn.Linear(hidden_dim, output_dim)

    def forward(self, x):
        _, (h, _) = self.lstm(x)
        return self.fc(h[-1])

class SentimentDataset(Dataset):
    def __init__(self, csv_file):
        self.data = pd.read_csv(csv_file)

    def __len__(self):
        return len(self.data)

    def __getitem__(self, idx):
        row = self.data.iloc[idx]
        inputs = np.random.rand(50, 300).astype(np.float32)  
        label = int(row['sentiment']) 
        return torch.tensor(inputs), torch.tensor(label)

train_dataset = SentimentDataset(os.path.join(args.data_dir, "train.csv"))
train_loader = DataLoader(train_dataset, batch_size=args.batch_size, shuffle=True)

input_dim = 300
hidden_dim = 128
output_dim = 3  
model = LSTMClassifier(input_dim, hidden_dim, output_dim)

criterion = nn.CrossEntropyLoss()
optimizer = optim.Adam(model.parameters(), lr=args.learning_rate)

for epoch in range(args.epochs):
    model.train()
    total_loss = 0
    for inputs, labels in train_loader:
        optimizer.zero_grad()
        outputs = model(inputs)
        loss = criterion(outputs, labels)
        loss.backward()
        optimizer.step()
        total_loss += loss.item()
    print(f"Epoch {epoch+1}/{args.epochs}, Loss: {total_loss:.4f}")

os.makedirs(args.model_dir, exist_ok=True)
torch.save(model.state_dict(), os.path.join(args.model_dir, "model.pth"))
print(f"Model saved to {args.model_dir}")
