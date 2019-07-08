
import torch
import torchvision
import torchvision.transforms as transforms
import torch.nn as nn
import torch.nn.functional as F
import cv2, time, os
import numpy as np
import matplotlib.pyplot as plt

'''
transform = transforms.Compose(
    [transforms.ToTensor(),
     transforms.Normalize((0.5, 0.5, 0.5), (0.5, 0.5, 0.5))])

trainset = torchvision.datasets.CIFAR10(root='./data', train=True,
                                        download=False, transform=transform)
trainloader = torch.utils.data.DataLoader(trainset, batch_size=4, shuffle=True, num_workers=2)

testset = torchvision.datasets.CIFAR10(root='./data', train=False,
                                       download=False, transform=transform)
testloader = torch.utils.data.DataLoader(testset, batch_size=4, shuffle=False, num_workers=2)

classes = ('plane', 'car', 'bird', 'cat',
           'deer', 'dog', 'frog', 'horse', 'ship', 'truck')

def save_foto(x, name):
    if x.requires_grad:
        foto = x.detach().numpy()
    else:
        foto = x.numpy()
    for i in range(3):
        foto[i] += 1
        max = np.amax(foto[i])
        min = np.amin(foto[i])
        result = np.around((foto[i] - min) * 255 / (max-min))
        #result = cv2.resize(result, (256, 256), interpolation=cv2.INTER_AREA)
    cv2.imwrite(os.getcwd() + '/foto/' + name, result)
    print('foto save')


class Net(nn.Module):
    def __init__(self):
        super(Net, self).__init__()
        self.conv1 = nn.Conv2d(3, 6, 5)
        self.pool = nn.MaxPool2d(2, 2)
        self.conv2 = nn.Conv2d(6, 16, 5)
        self.fc1 = nn.Linear(16 * 5 * 5, 120)
        self.fc2 = nn.Linear(120, 84)
        self.fc3 = nn.Linear(84, 10)

    def forward(self, x):
        print(x.shape)
        save_foto(x[0], '1.png')
        x = self.pool(F.relu(self.conv1(x)))
        save_foto(x[0], '2.png')
        x = self.pool(F.relu(self.conv2(x)))
        save_foto(x[0], '3.png')
        time.sleep(5)
        x = x.view(-1, 16 * 5 * 5)
        x = F.relu(self.fc1(x))
        x = F.relu(self.fc2(x))
        x = self.fc3(x)
        return x


net = Net()
import torch.optim as optim

criterion = nn.CrossEntropyLoss()
optimizer = optim.SGD(net.parameters(), lr=0.001, momentum=0.9)


for epoch in range(2):  # loop over the dataset multiple times

    running_loss = 0.0
    for i, data in enumerate(trainloader, 0):
        # get the inputs; data is a list of [inputs, labels]
        inputs, labels = data

        # zero the parameter gradients
        optimizer.zero_grad()
        # forward + backward + optimize
        outputs = net(inputs)
        #print(outputs, labels)
        loss = criterion(outputs, labels)
        #print(loss)
        loss.backward()
        optimizer.step()

        # print statistics
        running_loss += loss.item()
        if i % 2000 == 1999:    # print every 2000 mini-batches
            print('[%d, %5d] loss: %.3f' %
                  (epoch + 1, i + 1, running_loss / 2000))
            running_loss = 0.0

print('Finished Training')
'''


def save_photo(path, output):
    if round(output.shape[1] ** 0.5) < (output.shape[1] ** 0.5):
        side = round(output.shape[1] ** 0.5) + 1
    else:
        side = round(output.shape[1] ** 0.5)
    all_result = np.zeros((1, output.shape[2] * side, output.shape[3] * side))
    for i in range(output.shape[1]):
        temp = output[:, i, :, :].detach().numpy()
        max = np.amax(temp)
        min = np.amin(temp)
        result = np.around((temp - min) * 255 / (max - min))
        ind_x = i % side
        ind_y = i // side
        start = (output.shape[2] * ind_y, output.shape[3] * ind_x)
        all_result[:, start[0]: start[0] + output.shape[2], start[1]: start[1] + output.shape[3]] = result
    cv2.imwrite(path + '/{}.png'.format(i + 1), all_result[0, :, :])


im = cv2.imread(os.getcwd() + '/foto/1.png')
input = np.zeros((1, im.shape[2], im.shape[0], im.shape[1]))
input[:, 0, :, :] += im[:, :, 0]
input[:, 1, :, :] += im[:, :, 1]
input[:, 2, :, :] += im[:, :, 2]

input = torch.from_numpy(input).float()
print(input.shape)

m = nn.Conv2d(3, 6, kernel_size=15)
output = m(input)
#output = F.relu(output)
n = nn.MaxPool2d(2, 2)
output = n(output)
#b = nn.BatchNorm2d(6)
#output = b(output)
print(output.shape)
path = os.getcwd() + '/foto/test'
#save_photo(path, output)

m = nn.Conv2d(6, 16, kernel_size=10)
output = m(output)
output = n(output)
print(output.shape)
path = os.getcwd() + '/foto/test/2'
#save_photo(path, output)


m = nn.Conv2d(16, 64, kernel_size=5)
output = m(output)
output = n(output)
print(output.shape)
path = os.getcwd() + '/foto/test/3'
#save_photo(path, output)
