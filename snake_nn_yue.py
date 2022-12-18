import torch
from torch import nn
from torch.utils.data import DataLoader
from torchvision import datasets
from torchvision.transforms import ToTensor
from torch.utils.data import Dataset
import numpy as np
import matplotlib.pyplot as plt
import torchvision.transforms as transforms

class CustomDataset(Dataset):
    def __init__(self, training_data, transform=None, target_transform=None):
        self.training_data = training_data 
        self.transform = transform
        self.target_transform = target_transform

    def __len__(self):
        return len(self.training_data)

    def __getitem__(self, idx):
        image = self.training_data[idx][0]
        action = self.training_data[idx][1]
        label = torch.zeros((4))
        if action=='UP':
            label[0] = 1

        elif action=='DOWN':
            label[1] = 1
        elif action=='LEFT':
            label[2] = 1
        elif action=='RIGHT':
            label[3] = 1
        
        if self.transform:
            image = self.transform(image)
        if self.target_transform:
            label = self.target_transform(label)
        return image, label



class Snake_NN(nn.Module):
    def __init__(self):
        super().__init__()
        self.flatten = nn.Flatten(0,2)
        self.layer1 = nn.Sequential(
            nn.Conv2d(4, 16, kernel_size=3, stride=1, padding=1),
            nn.BatchNorm2d(16),
            nn.ReLU(),
            nn.MaxPool2d(kernel_size = 3, stride = 1))
        self.layer2 = nn.Sequential(
            nn.Conv2d(16, 96, kernel_size=3, stride=1, padding=1),
            nn.BatchNorm2d(96),
            nn.ReLU(),
            nn.MaxPool2d(kernel_size = 3, stride = 1))
        self.layer3 = nn.Sequential(
            nn.Conv2d(96, 256, kernel_size=3, stride=1, padding=1),
            nn.BatchNorm2d(256),
            nn.ReLU())
        self.layer4 = nn.Sequential(
            nn.Conv2d(256, 384, kernel_size=3, stride=1, padding=1),
            nn.BatchNorm2d(384),
            nn.ReLU(),
            nn.MaxPool2d(kernel_size = 3, stride = 1))
        self.layer5 = nn.Sequential(
            nn.Conv2d(384, 256, kernel_size=3, stride=1, padding=1),
            nn.BatchNorm2d(256),
            nn.ReLU(),
            nn.MaxPool2d(kernel_size = 3, stride = 1))

        self.fc = nn.Sequential(
            nn.Dropout(0.5),
            nn.Linear(1024, 256),
            nn.ReLU())
        self.fc1 = nn.Sequential(
            nn.Dropout(0.5),
            nn.Linear(256, 4),
            nn.ReLU())
        # self.fc2= nn.Sequential(
        #     nn.Linear(32, 4))



        self.data = np.load('training_data.npy',allow_pickle=True)
        self.training_data = self.data[0:int(len(self.data)*0.8)]
        self.testing_data = self.data[int(len(self.data)*0.8):]
        self.loss_fn = nn.CrossEntropyLoss()
        self.loss_fn = self.loss_fn.cuda()
        self.optimizer = torch.optim.SGD(self.parameters(), lr=1e-3, momentum=0.9, weight_decay = 0.0002)
        self.loss_list = []


    def save(self):
        torch.save(self.state_dict(), 'model.pt')

    def load(self):
        self.load_state_dict(torch.load('model.pt'))

    def forward(self, x):
        # x = self.flatten(x)
        # logits = self.linear_relu_stack(x)
        out = self.layer1(x)
        out = self.layer2(out)
        out = self.layer3(out)
        out = self.layer4(out)
        out = self.layer5(out)

        out = out.reshape(out.size(0), -1)
        out = self.fc(out)
        out = self.fc1(out)
        # out = self.fc2(out)


        return out

    def train_model(self):
        self.train()
        epochs = 100
        # print(len(self.training_data))
        training_set = CustomDataset(training_data = self.training_data )
        train_dataloader = torch.utils.data.DataLoader(training_set, batch_size=128, shuffle=True)
        test_set = CustomDataset(training_data = self.testing_data )
        test_dataloader = torch.utils.data.DataLoader(test_set, batch_size=128, shuffle=True)
        best_accuracy = 0

        self = self.cuda()
        # exit()
        for i in range(epochs):
            self.train()
            
            for idx, data in enumerate(train_dataloader):
                
                # input = torch.from_numpy(data[0])
                # input = input.to(torch.float32)
                input, label = data

                input = input.to(torch.float32)
                input = input.cuda()
                label = label.cuda()
                # print(type(input))
                # exit()
                # Compute prediction error
                pred = self(input)
                loss = self.loss_fn(pred, label)

                # Backpropagation
                self.optimizer.zero_grad()
                loss.backward()
                self.optimizer.step()

                loss= loss.item()
                self.loss_list.append(loss)
                # print(f"loss: {loss:>7f}")
                if idx % 10 == 0:
                    print('Epoch:', i )
                    print('loss: ',loss)
            self.eval()
            test_loss, correct = 0, 0
            total = 0
            with torch.no_grad():
                for idx, data in enumerate(test_dataloader):
                    input, label = data
                    input = input.to(torch.float32)
                    input = input.cuda()
                    label = label.cuda()

                    # Compute prediction error
                    pred = self(input)
                    test_loss += self.loss_fn(pred, label).item()
                    _, predicted = torch.max(pred, 1)
                    total += label.size(0)
                    _, truth = torch.max(label, 1)
                    correct += ( predicted == truth).type(torch.float).sum().item()

            test_loss /= total
            correct /= total
            if(correct > best_accuracy):
                best_accuracy = correct
                # torch.save(self.state_dict(), 'checkpoint_{}.pt'.format(i+1))

                if(best_accuracy > 0.8):
                    torch.save(self.state_dict(), 'checkpoints/checkpoint_{}.pt'.format(i+1))

            print('Epoch:', i, " fininshed")
            print(f"Test Error: \n Accuracy: {(100*correct):>0.1f}%, Avg loss: {test_loss:>8f} \n")
            

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
    snake_nn.train_model()
       # snake_nn.plot_loss()

    snake_nn.save()
    # snake_nn.load()
    # snake_nn.test()
