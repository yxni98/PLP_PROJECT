import os
import re
import json
import spacy
import numpy as np
from pytorch_pretrained_bert import BertModel, BertTokenizer

bert_tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')

def save_term_data(data, word2index, path, tokenizer):
    dirname = os.path.dirname(path)
    if not os.path.exists(dirname):
        os.makedirs(dirname)
    sentence = []
    aspect = []
    label = []
    context = []
    bert_token = []
    bert_segment = []
    td_left = []
    td_right = []
    f = lambda x: word2index[x] if x in word2index else word2index[UNK]
    g = lambda x: list(map(f, tokenizer(x)))
    d = {
        'positive': 0,
        'negative': 1,
        'neutral': 2,
        'conflict': 3
    }
    for piece in data:
        text, term, polarity, start, end = piece.split('__split__')
        start, end = int(start), int(end)
        assert text[start: end] == term
        sentence.append(g(text))
        aspect.append(g(term))
        label.append(d[polarity])
        left_part = g(text[:start])
        right_part = g(text[end:])
        context.append(left_part + [ASPECT_INDEX] + right_part)
        bert_sentence = bert_tokenizer.tokenize(text)
        bert_aspect = bert_tokenizer.tokenize(term)
        bert_token.append(bert_tokenizer.convert_tokens_to_ids(['[CLS]'] + bert_sentence + ['[SEP]'] + bert_aspect + ['[SEP]']))
        bert_segment.append([0] * (len(bert_sentence) + 2) + [1] * (len(bert_aspect) + 1))
        td_left.append(g(text[:end]))
        td_right.append(g(text[start:])[::-1])
        assert len(bert_token[-1]) == len(bert_segment[-1])
    max_length = lambda x: max([len(y) for y in x])
    sentence_max_len = max_length(sentence)
    aspect_max_len = max_length(aspect)
    context_max_len = max_length(context)
    bert_max_len = max_length(bert_token)
    td_left_max_len = max_length(td_left)
    td_right_max_len = max_length(td_right)
    num = len(data)
    for i in range(num):
        sentence[i].extend([0] * (sentence_max_len - len(sentence[i])))
        aspect[i].extend([0] * (aspect_max_len - len(aspect[i])))
        context[i].extend([0] * (context_max_len - len(context[i])))
        bert_token[i].extend([0] * (bert_max_len - len(bert_token[i])))
        bert_segment[i].extend([0] * (bert_max_len - len(bert_segment[i])))
        td_left[i].extend([0] * (td_left_max_len - len(td_left[i])))
        td_right[i].extend([0] * (td_right_max_len - len(td_right[i])))
    sentence = np.asarray(sentence, dtype=np.int32)
    aspect = np.asarray(aspect, dtype=np.int32)
    label = np.asarray(label, dtype=np.int32)
    context = np.asarray(context, dtype=np.int32)
    bert_token = np.asarray(bert_token, dtype=np.int32)
    bert_segment = np.asarray(bert_segment, dtype=np.int32)
    td_left = np.asarray(td_left, dtype=np.int32)
    td_right = np.asarray(td_right, dtype=np.int32)
    np.savez(path, sentence=sentence, aspect=aspect, label=label, context=context, bert_token=bert_token, bert_segment=bert_segment,
             td_left=td_left, td_right=td_right)

def load_glove(path, vocab_size, word2index):
    if not os.path.isfile(path):
        raise IOError('Not a file', path)
    glove = np.random.uniform(-0.01, 0.01, [vocab_size, 300])
    with open(path, 'r', encoding='utf-8') as f:
        for line in f:
            content = line.split(' ')
            if content[0] in word2index:
                glove[word2index[content[0]]] = np.array(list(map(float, content[1:])))
    glove[PAD_INDEX, :] = 0
    return glove

def load_sentiment_matrix(glove_path, sentiment_path):
    sentiment_matrix = np.zeros((3, 300), dtype=np.float32)
    sd = json.load(open(sentiment_path, 'r', encoding='utf-8'))
    sd['positive'] = set(sd['positive'])
    sd['negative'] = set(sd['negative'])
    sd['neutral'] = set(sd['neutral'])
    with open(glove_path, 'r', encoding='utf-8') as f:
        for line in f:
            content = line.split(' ')
            word = content[0]
            vec = np.array(list(map(float, content[1:])))
            if word in sd['positive']:
                sentiment_matrix[0] += vec
            elif word in sd['negative']:
                sentiment_matrix[1] += vec
            elif word in sd['neutral']:
                sentiment_matrix[2] += vec
    sentiment_matrix -= sentiment_matrix.mean()
    sentiment_matrix = sentiment_matrix / sentiment_matrix.std() * np.sqrt(2.0 / (300.0 + 3.0))
    return sentiment_matrix