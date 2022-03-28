import os
import numpy as np
import pickle
import yaml
import spacy
import re
from xml.etree.ElementTree import parse
from data_utils.vocabulary import Vocabulary
from data_utils.sentence2embedding import save_category_data, load_glove, load_sentiment_matrix

def generate_sentence(path, lowercase=False):
    tree = parse(path)
    sentences = tree.getroot()
    data = []
    split_char = '__split__'
    for sentence in sentences:
        text = sentence.find('text')
        if text is None:
            continue
        text = text.text
        if lowercase:
            text = text.lower()
        aspectTerms = sentence.find('aspectTerms')
        if aspectTerms is None:
            continue
        for aspectTerm in aspectTerms:
            term = aspectTerm.get('term')
            if lowercase:
                term = term.lower()
            polarity = aspectTerm.get('polarity')
            start = aspectTerm.get('from')
            end = aspectTerm.get('to')
            piece = text + split_char + term + split_char + polarity + split_char + start + split_char + end
            data.append(piece)
    remove_set = set(['conflict'])
    filtered_data = []
    for text in data:
        if not text.split('__split__')[2] in remove_set:
            filtered_data.append(text)
    return filtered_data

def tokenizer(text):
    url = re.compile('(<url>.*</url>)')
    spacy_en = spacy.load('en_core_web_sm')
    def legal_verify(x):
        return len(x) >= 1 and not x.isspace()
    tokens = [tok.text for tok in spacy_en.tokenizer(url.sub('@URL@', text))]
    return list(filter(legal_verify, tokens))

def generate_vocab(data, max_size, min_freq):

    if max_size == 'None':
        max_size = None
    vocab = Vocabulary()
    for piece in data:
        text = piece.split('__split__')[0]
        text = tokenizer(text)
        vocab.add_list(text)
    return vocab.get_vocab(max_size=max_size, min_freq=min_freq)

def analyze_term(data):
    num = len(data)
    sentence_lens = []
    aspect_lens = []
    log = {'total': num}
    for piece in data:
        text, term, polarity, _, _ = piece.split('__split__')
        sentence_lens.append(len(tokenizer(text)))
        aspect_lens.append(len(tokenizer(term)))
        if not polarity in log:
            log[polarity] = 0
        log[polarity] += 1
    log['sentence_max_len'] = max(sentence_lens)
    log['sentence_avg_len'] = sum(sentence_lens) / len(sentence_lens)
    log['aspect_max_len'] = max(aspect_lens)
    log['aspect_avg_len'] = sum(aspect_lens) / len(aspect_lens)
    return log

def data_generation(args):
    raw_train_path = os.path.join(args.data_path, 'raw/train.xml')
    raw_val_path = os.path.join(args.data_path, 'raw/val.xml')
    raw_test_path = os.path.join(args.data_path, 'raw/test.xml')

    train_data = generate_sentence(raw_train_path, lowercase=True)
    val_data = generate_sentence(raw_val_path, lowercase=True)
    test_data = generate_sentence(raw_test_path, lowercase=True)

    word2index, index2word = generate_vocab(train_data+val_data+test_data, max_size=args.max_vocab_size, min_freq=args.min_vocab_freq)
    if not os.path.exists(os.path.join(args.data_path, 'processed')):
        os.makedirs(os.path.join(args.data_path, 'processed'))

    save_term_data(train_data, word2index, os.path.join(args.data_path, 'processed/train.npz'))
    save_term_data(val_data, word2index, os.path.join(args.data_path, 'processed/val.npz'))
    save_term_data(test_data, word2index, os.path.join(args.data_path, 'processed/test.npz'))

    glove = load_glove(args.glove_file, len(index2word), word2index)
    sentiment_matrix = load_sentiment_matrix(args.glove_file, args.add_predefined_sentiment)
    np.save(os.path.join(args.data_path, 'processed/glove.npy'), glove)
    np.save(os.path.join(args.data_path, 'processed/sentiment_matrix.npy'), sentiment_matrix)
    with open(os.path.join(args.data_path, 'processed/word2index.pickle'), 'wb') as handle:
        pickle.dump(word2index, handle)
    with open(os.path.join(args.data_path, 'processed/index2word.pickle'), 'wb') as handle:
        pickle.dump(index2word, handle)
    analyze = analyze_term
    log = {
        'vocab_size': len(index2word),
        'oov_size': len(word2index) - len(index2word),
        'train_data': analyze(train_data),
        'val_data': analyze(val_data),
        'test_data': analyze(test_data),
        'num_categories': 3
    }
    if not os.path.exists(os.path.join(args.data_path, 'log')):
        os.makedirs(os.path.join(args.data_path, 'log'))
    with open(os.path.join(args.data_path, 'log/log.yml'), 'w') as handle:
        yaml.safe_dump(log, handle, encoding='utf-8', allow_unicode=True, default_flow_style=False)