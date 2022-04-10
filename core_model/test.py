import os
import torch

from model_utils.backbone import backbone_model
from torch.utils.data import DataLoader
from data_utils.create_dataset import create_dataset
from test_utils.eval import eval



def make_term_test_data(args):
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

def test(args):
    os.environ["CUDA_VISIBLE_DEVICES"] = args.gpu_device
    model = backbone_model()
    model = model.cuda()
    model_path = os.path.join(args.data_path, 'checkpoints/'+'lr_'+str(args.learning_rate)+'_layerno_'+str(args.num_layers)+'_recurrent_capsnet.pth')
    model.load_state_dict(torch.load(model_path))
    test_loader = make_term_test_data(args)
    test_accuracy = eval(model, test_loader)
    print('test:\taccuracy: %.4f' % (test_accuracy))