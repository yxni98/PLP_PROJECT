import yaml
import os
import time
import pickle
from config import args
import torch
from torch import optim
from torch import nn
import adabound
from train.eval import eval
from model_utils.backbone import backbone_model

os.environ["CUDA_VISIBLE_DEVICES"] = args.gpu_device

class capsule_nn_loss(nn.Module):
    def __init__(self, smooth=0.1, lamda=0.6):
        super(capsule_nn_loss, self).__init__()
        self.smooth = smooth
        self.lamda = lamda

    def forward(self, input, target):
        one_hot = torch.zeros_like(input).to(input.device)
        one_hot = one_hot.scatter(1, target.unsqueeze(-1), 1)
        a = torch.max(torch.zeros_like(input).to(input.device), 1 - self.smooth - input)
        b = torch.max(torch.zeros_like(input).to(input.device), input - self.smooth)
        loss = one_hot * a * a + self.lamda * (1 - one_hot) * b * b
        loss = loss.sum(dim=1, keepdim=False)
        return loss.mean()

def optimizer_selection(args, model):
    lr = args.learning_rate
    weight_decay = args.weight_decay
    opt = {
        'sgd': optim.SGD,
        'adadelta': optim.Adadelta,
        'adam': optim.Adam,
        'adamax': optim.Adamax,
        'adagrad': optim.Adagrad,
        'asgd': optim.ASGD,
        'rmsprop': optim.RMSprop,
        'adabound': adabound.AdaBound
    }
    optimizer = opt[args.optimizer](model.parameters(), lr=lr, weight_decay=weight_decay)
    return optimizer

def make_term_data():
    data_path = args.data_path
    train_path = os.path.join(data_path, 'processed/train.npz')
    val_path = os.path.join(data_path, 'processed/val.npz')
    train_data = ABSADataset(train_path, ['context', 'aspect'])
    val_data = ABSADataset(val_path, ['context', 'aspect'])
    train_loader = DataLoader(
        dataset=train_data,
        batch_size=args.batch_size,
        shuffle=True,
        pin_memory=True
    )
    val_loader = DataLoader(
        dataset=val_data,
        batch_size=args.batch_size,
        shuffle=False,
        pin_memory=True
    )
    return train_loader, val_loader

def train(args):
    model = backbone_model()
    train_loader, val_loader = make_term_data()

    model = model.cuda()
    model_path = os.path.join(args.data_path, 'checkpoints/recurrent_capsnet.pth')
    if not os.path.exists(os.path.dirname(model_path)):
        os.makedirs(os.path.dirname(model_path))
    with open(os.path.join(args.data_path, 'processed/index2word.pickle'), 'rb') as handle:
        index2word = pickle.load(handle)
    criterion = capsule_nn_loss()
    optimizer = optimizer_selection(args, model)
    max_val_accuracy = 0
    min_val_loss = 100
    global_step = 0
    for epoch in range(args.num_epoches):
        total_loss = 0
        total_samples = 0
        correct_samples = 0
        start = time.time()
        for i, data in enumerate(train_loader):
            global_step += 1
            model.train()
            input0, input1, label = data
            input0, input1, label = input0.cuda(), input1.cuda(), label.cuda()
            optimizer.zero_grad()
            logit = model(input0, input1)
            loss = criterion(logit, label)
            batch_size = input0.size(0)
            total_loss += batch_size * loss.item()
            total_samples += batch_size
            pred = logit.argmax(dim=1)
            correct_samples += (label == pred).long().sum().item()
            loss.backward()
            torch.nn.utils.clip_grad_norm_(model.parameters(), 5.0)
            optimizer.step()
            if i % 10 == 0 and i > 0:
                train_loss = total_loss / total_samples
                train_accuracy = correct_samples / total_samples
                total_loss = 0
                total_samples = 0
                correct_samples = 0
                val_accuracy, val_loss = eval(model, val_loader, criterion)
                print('[epoch %2d] [step %3d] train_loss: %.4f train_acc: %.4f val_loss: %.4f val_acc: %.4f'
                      % (epoch, i, train_loss, train_accuracy, val_loss, val_accuracy))
                if val_accuracy > max_val_accuracy:
                    max_val_accuracy = val_accuracy
                    # torch.save(aspect_term_model.state_dict(), model_path)
                if val_loss < min_val_loss:
                    min_val_loss = val_loss
                    if epoch > 0:
                        torch.save(model.state_dict(), model_path)
        end = time.time()
        print('time: %.4fs' % (end - start))
    print('max_val_accuracy:', max_val_accuracy)

train(args)