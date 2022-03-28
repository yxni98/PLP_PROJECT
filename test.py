import os
import torch
from train.test import test
from config import args
from model_utils.backbone import backbone_model
from torch.utils.data import DataLoader
from data_utils.create_dataset import create_dataset
from train.eval import eval

os.environ["CUDA_VISIBLE_DEVICES"] = args.gpu_device

def make_term_test_data():
    data_path = args.data_path
    test_path = os.path.join(data_path, 'processed/test.npz')
    test_data = create_dataset(test_path, ['context', 'aspect'])
    test_loader = DataLoader(
        dataset=test_data,
        batch_size=args.batch_size,
        shuffle=False,
        pin_memory=True
    )
    return test_loader

def test():
    model = backbone_model()
    model = model.cuda()
    model_path = os.path.join(args.data_path, 'checkpoints/recurrent_capsnet.pth')
    model.load_state_dict(torch.load(model_path))
    test_loader = make_term_test_data()
    test_accuracy = eval(model, test_loader)
    print('test:\taccuracy: %.4f' % (test_accuracy))