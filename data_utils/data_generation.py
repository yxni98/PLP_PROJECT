import os
import numpy as np
import pickle
import yaml
from data_process.utils import *

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
    return data

def data_generation(args):
    raw_train_path = os.path.join(args.data_path, 'raw/train.xml')
    raw_val_path = os.path.join(args.data_path, 'raw/val.xml')
    raw_test_path = os.path.join(args.data_path, 'raw/test.xml')

    train_data = generate_sentence(raw_train_path, lowercase=True)
    val_data = generate_sentence(raw_val_path, lowercase=True)
    test_data = generate_sentence(raw_test_path, lowercase=True)

    word2index, index2word = build_vocab(train_data, max_size=args.max_vocab_size, min_freq=args.min_vocab_freq)
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