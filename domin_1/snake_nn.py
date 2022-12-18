import torch
from torch import nn
from torch.utils.data import DataLoader
from torchvision import datasets
from torchvision.transforms import ToTensor
import numpy as np
import matplotlib.pyplot as plt

class Snake_NN(nn.Module):
    def __init__(self):
        super().__init__()
        self.flatten = nn.Flatten(0,2)
        self.linear_relu_stack = nn.Sequential(
            nn.Linear(4*100, 1000),
            #nn.ReLU(),
            nn.Linear(1000, 512),
            #nn.ReLU(),
            nn.Linear(512, 4)
        )
        self.data = np.load('training_data.npy',allow_pickle=True)
        self.training_data = self.data[0:int(len(self.data)*0.8)]
        self.testing_data = self.data[int(len(self.data)*0.8):]

        self.loss_fn = nn.CrossEntropyLoss()
        self.optimizer = torch.optim.SGD(self.parameters(), lr=1e-3)
        self.loss_list = []

    def save(self):
        torch.save(self.state_dict(), 'model.pt')

    def load(self):
        self.load_state_dict(torch.load('model.pt'))

    def forward(self, x):
        x = self.flatten(x)
        logits = self.linear_relu_stack(x)
        return logits

    def train_model(self):
        self.train()
        for data in self.training_data:
            input = torch.from_numpy(data[0])
            input = input.to(torch.float32)
            action = data[1]
            label = torch.zeros((4))
            if action=='UP':
                label[0] = 1
            elif action=='DOWN':
                label[1] = 1
            elif action=='LEFT':
                label[2] = 1
            elif action=='RIGHT':
                label[3] = 1

            # Compute prediction error
            pred = self(input)
            loss = self.loss_fn(pred, label)

            # Backpropagation
            self.optimizer.zero_grad()
            loss.backward()
            self.optimizer.step()

            loss= loss.item()
            self.loss_list.append(loss)
            print(f"loss: {loss:>7f}")

    def test(self):
        self.eval()
        test_loss, correct = 0, 0
        with torch.no_grad():
            for data in self.testing_data:
                input = torch.from_numpy(data[0])
                input = input.to(torch.float32)
                action = data[1]
                label = torch.zeros((4))
                if action=='UP':
                    label[0] = 1
                elif action=='DOWN':
                    label[1] = 1
                elif action=='LEFT':
                    label[2] = 1
                elif action=='RIGHT':
                    label[3] = 1

                pred = self(input)
                test_loss += self.loss_fn(pred, label).item()
                correct += (pred.argmax(0) == label.argmax(0)).type(torch.float).sum().item()
        test_loss /= len(self.testing_data)
        correct /= len(self.testing_data)
        print(f"Test Error: \n Accuracy: {(100*correct):>0.1f}%, Avg loss: {test_loss:>8f} \n")

    def plot_loss(self):
        plt.plot(self.loss_list)
        plt.ylabel('some numbers')
        plt.show()

if __name__ == '__main__':
    snake_nn = Snake_NN()
    #for i in range(5):
    #    snake_nn.train_model()
    #    snake_nn.plot_loss()

    #snake_nn.save()
    snake_nn.load()
    snake_nn.test()
