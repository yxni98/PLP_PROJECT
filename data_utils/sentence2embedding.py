import os
import re
import json
import spacy
import numpy as np
from pytorch_pretrained_bert import BertModel, BertTokenizer

bert_tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')

def save_category_data(data, word2index, path):
    url = re.compile('(<url>.*</url>)')
    spacy_en = spacy.load('en_core_web_sm')

    def legal_verify(x):
        return len(x) >= 1 and not x.isspace()

    def tokenizer(text):
        tokens = [tok.text for tok in spacy_en.tokenizer(url.sub('@URL@', text))]
        return list(filter(legal_verify, tokens))

    dirname = os.path.dirname(path)
    if not os.path.exists(dirname):
        os.makedirs(dirname)
    sentence = []
    aspect = []
    label = []
    bert_token = []
    bert_segment = []
    f = lambda x: word2index[x] if x in word2index else word2index[UNK]
    g = lambda x: list(map(f, tokenizer(x)))
    d = {
        'positive': 0,
        'negative': 1,
        'neutral': 2,
        'conflict': 3
    }
    cd = {
        'service': 0,
        'price': 1,
        'look': 2,
        'battery': 3,
        'performance': 4,
        'miscellaneous': 5
    }
    for piece in data:
        text, category, polarity = piece.split('__split__')
        sentence.append(g(text))
        aspect.append(cd[category])
        label.append(d[polarity])
        bert_sentence = bert_tokenizer.tokenize(text)
        bert_aspect = bert_tokenizer.tokenize(category)
        bert_token.append(bert_tokenizer.convert_tokens_to_ids(['[CLS]'] + bert_sentence + ['[SEP]'] + bert_aspect + ['[SEP]']))
        bert_segment.append([0] * (len(bert_sentence) + 2) + [1] * (len(bert_aspect) + 1))
        assert len(bert_token[-1]) == len(bert_segment[-1])
    max_length = lambda x: max([len(y) for y in x])
    sentence_max_len = max_length(sentence)
    bert_max_len = max_length(bert_token)
    num = len(data)
    for i in range(num):
        sentence[i].extend([0] * (sentence_max_len - len(sentence[i])))
        bert_token[i].extend([0] * (bert_max_len - len(bert_token[i])))
        bert_segment[i].extend([0] * (bert_max_len - len(bert_segment[i])))
    sentence = np.asarray(sentence, dtype=np.int32)
    aspect = np.asarray(aspect, dtype=np.int32)
    label = np.asarray(label, dtype=np.int32)
    bert_token = np.asarray(bert_token, dtype=np.int32)
    bert_segment = np.asarray(bert_segment, dtype=np.int32)
    np.savez(path, sentence=sentence, aspect=aspect, label=label, bert_token=bert_token, bert_segment=bert_segment)

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