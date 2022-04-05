import torch
from torch import nn
import torch.nn.functional as F
from torch.nn import init
from model_utils.attention import Attention
import numpy as np

PAD_INDEX = 0

def squash(x, dim=-1):
    squared = torch.sum(x * x, dim=dim, keepdim=True)
    scale = torch.sqrt(squared) / (1.0 + squared)
    return scale * x

def sentence_clip(sentence):
    mask = (sentence != PAD_INDEX)
    sentence_lens = mask.long().sum(dim=1, keepdim=False)
    max_len = sentence_lens.max().item()
    return sentence[:, :max_len]

class BilinearAttention(Attention):

    def __init__(self, query_size, key_size, dropout=0):
        super(BilinearAttention, self).__init__(dropout)
        self.weights = nn.Parameter(torch.FloatTensor(query_size, key_size))
        init.xavier_uniform_(self.weights)

    def _score(self, query, key):
        """
        query: FloatTensor (batch_size, num_queries, query_size)
        key: FloatTensor (batch_size, time_step, key_size)
        """
        score = query.matmul(self.weights).matmul(key.transpose(1, 2))
        return score

class CapsuleNetwork(nn.Module):

    def __init__(self, embedding, hidden_size, capsule_size, dropout, num_categories):
        super(CapsuleNetwork, self).__init__()
        self.embedding = embedding
        embed_size = embedding.embedding_dim
        self.capsule_size = capsule_size
        self.aspect_transform = nn.Sequential(
            nn.Linear(embed_size, capsule_size),
            nn.Dropout(dropout)
        )
        self.sentence_transform = nn.Sequential(
            nn.Linear(hidden_size, capsule_size),
            nn.Dropout(dropout)
        )
        self.norm_attention = BilinearAttention(capsule_size, capsule_size)
        self.guide_capsule = nn.Parameter(
            torch.Tensor(num_categories, capsule_size)
        )
        self.guide_weight = nn.Parameter(
            torch.Tensor(capsule_size, capsule_size)
        )
        self.scale = nn.Parameter(torch.tensor(4.0))
        self.capsule_projection = nn.Linear(capsule_size, capsule_size * num_categories)
        self.dropout = dropout
        self.num_categories = num_categories
        self._reset_parameters()

    def _reset_parameters(self):
        init.xavier_uniform_(self.guide_capsule)
        init.xavier_uniform_(self.guide_weight)

    def load_sentiment(self, path):
        sentiment = np.load(path)
        e1 = np.mean(sentiment)
        d1 = np.std(sentiment)
        e2 = 0
        d2 = np.sqrt(2.0 / (sentiment.shape[0] + sentiment.shape[1]))
        sentiment = (sentiment - e1) / d1 * d2 + e2
        self.guide_capsule.data.copy_(torch.tensor(sentiment))

    def forward(self, sentence, aspect):
        # get lengths and masks
        sentence = sentence_clip(sentence)
        aspect = sentence_clip(aspect)
        sentence_mask = (sentence != PAD_INDEX)
        aspect_mask = (aspect != PAD_INDEX)
        # sentence_lens = sentence_mask.long().sum(dim=1, keepdim=True)
        aspect_lens = aspect_mask.long().sum(dim=1, keepdim=True)
        # embedding
        sentence = self.embedding(sentence)
        sentence = F.dropout(sentence, p=self.dropout, training=self.training)
        aspect = self.embedding(aspect)
        aspect = F.dropout(aspect, p=self.dropout, training=self.training)
        # aspect average pooling
        aspect = aspect.masked_fill(aspect_mask.unsqueeze(-1) == 0, 0)
        aspect = aspect.sum(dim=1, keepdim=False) / aspect_lens.float()
        # sentence encode layer
        sentence = self._sentence_encode(sentence, aspect)
        # primary capsule layer
        sentence = self.sentence_transform(sentence)
        primary_capsule = squash(sentence, dim=-1)
        # aspect capsule layer
        aspect = self.aspect_transform(aspect)
        aspect_capsule = squash(aspect, dim=-1)
        # aspect aware normalization
        norm_weight = self.norm_attention.get_attention_weights(aspect_capsule, primary_capsule, sentence_mask)
        # capsule guided routing
        category_capsule = self._capsule_guided_routing(primary_capsule, norm_weight)
        category_capsule_norm = torch.sqrt(torch.sum(category_capsule * category_capsule, dim=-1, keepdim=False))
        return category_capsule_norm

    def _sentence_encode(self, sentence, aspect, mask=None):
        raise NotImplementedError('_sentence_encode method is not implemented.')

    def _capsule_guided_routing(self, primary_capsule, norm_weight):
        guide_capsule = squash(self.guide_capsule)
        guide_matrix = primary_capsule.matmul(self.guide_weight).matmul(guide_capsule.transpose(0, 1))
        guide_matrix = F.softmax(guide_matrix, dim=-1)
        guide_matrix = guide_matrix * norm_weight.unsqueeze(-1) * self.scale  # (batch_size, time_step, num_categories)
        category_capsule = guide_matrix.transpose(1, 2).matmul(primary_capsule)
        category_capsule = F.dropout(category_capsule, p=self.dropout, training=self.training)
        category_capsule = squash(category_capsule)
        return category_capsule
