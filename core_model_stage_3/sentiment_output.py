import os
import torch
from torch import nn
import yaml
import numpy as np
from core_model.model_utils.backbone import backbone_model
from torch.utils.data import DataLoader
from core_model.data_utils.create_dataset import create_dataset
from core_model.data_utils.sentiment_data_generation import sentiment_data_generation
from core_model.config import args

os.chdir('../core_model/')

def make_term_test_data(args):
    data_path = args.data_path
    test_path = os.path.join(data_path, 'processed/search_test.npz')
    test_data = create_dataset(test_path, ['context', 'aspect'])
    test_loader = DataLoader(
        dataset=test_data,
        batch_size=5,
        shuffle=False,
        pin_memory=True
    )
    return test_loader

def self_eval(model, data_loader):
    total_samples = 0
    correct_samples = 0
    total_loss = 0
    model.eval()
    return_sentiment_pred = []
    sentiment_dict = {0:'positive', 1:'negative', 2:'neutral'}
    with torch.no_grad():
        for data in data_loader:
            input0, input1, label = data
            logit = model(input0, input1)
            pred = logit.argmax(dim=1)
            return_sentiment_pred += list(pred)
        for i in range(len(return_sentiment_pred)):
            return_sentiment_pred[i] = int(return_sentiment_pred[i])
        return return_sentiment_pred

def return_sentiment_output(platform, sentences, terms):
    sentiment_data_generation(args, sentences, terms)
    # os.environ["CUDA_VISIBLE_DEVICES"] = args.gpu_device
    # model = model.cuda()

    current_glove = np.load('./data/processed/glove.npy')
    chosen_word_index = [] 

    if platform == 'amazon':
        amazon_glove = np.load('./data/processed/amazon_glove.npy')
        for sent_emb in current_glove:
            chosen_word_index.append(np.argmin(np.sqrt(np.sum(np.square(amazon_glove - sent_emb), 1))))
        model_path = './data/checkpoints/lr_0.01_layerno_2_amazon_recurrent_capsnet.pth'
    else:
        reddit_glove = np.load('./data/processed/reddit_glove.npy')
        for sent_emb in current_glove:
            chosen_word_index.append(np.argmin(np.sqrt(np.sum(np.square(reddit_glove - sent_emb), 1))))
        model_path = './data/checkpoints/lr_0.01_layerno_2_reddit_recurrent_capsnet.pth'
    model = backbone_model()
    saved_params = torch.load(model_path, map_location='cpu')
    for key in saved_params.keys():
        if key == 'embedding.weight':
            saved_params[key] = saved_params[key][chosen_word_index]
    model.load_state_dict(saved_params)
    test_loader = make_term_test_data(args)
    return_sentiment_pred = self_eval(model, test_loader)
    return return_sentiment_pred
