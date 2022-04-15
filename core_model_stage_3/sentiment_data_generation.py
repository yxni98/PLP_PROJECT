import os
import numpy as np
import pickle
import yaml
import spacy
import re
from xml.etree.ElementTree import parse
from core_model.data_utils.vocabulary import Vocabulary
from core_model.data_utils.sentence2embedding import save_term_data, load_glove, load_sentiment_matrix
from pytorch_pretrained_bert import BertModel, BertTokenizer

bert_tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')

url = re.compile('(<url>.*</url>)')
spacy_en = spacy.load('en_core_web_sm')


def tokenizer(text):
    def legal_verify(x):
        return len(x) >= 1 and not x.isspace()
    tokens = [tok.text for tok in spacy_en.tokenizer(url.sub('@URL@', text))]
    return list(filter(legal_verify, tokens))

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

def construct_data(sentences, terms):

    start_doc = '<?xml version="1.0" encoding="utf-8"?>\n<sentences>\n'
    end_doc = '</sentences>\n'

    text = ''
    term = ''
    polarity = ''
    polarity_dict = {'0':'neutral', '1':'positive', '-1':'negative'}
    text2terms = {}
    for i in range(len(sentences)):
        polarity = polarity_dict['0']
        original_text = sentences[i]
        for term in terms[i]:
            from_index = original_text.index(term)
            to_index = from_index+len(term)
            from_index = str(from_index)
            to_index = str(to_index)
            if original_text not in text2terms.keys():
                text2terms[original_text] = [(from_index, polarity, term, to_index)]
            else:
                text2terms[original_text].append((from_index, polarity, term, to_index))

    all_input_sentences = []
    for text in text2terms.keys():
        aspect_terms = ''
        for term_unit in text2terms[text]:
            aspect_term = '\t\t\t<aspectTerm from="%s" polarity="%s" term="%s" to="%s"/>\n' % (term_unit[0], term_unit[1], term_unit[2], term_unit[3])
            aspect_terms += aspect_term
        input_sentence = '\t<sentence>\n\t\t<text>%s</text>\n\t\t<aspectTerms>\n%s\t\t</aspectTerms>\n\t</sentence>\n' % (text, aspect_terms)
        input_sentence = input_sentence.replace('&', ' ')
        all_input_sentences.append(input_sentence)

    xml = ''
    xml += start_doc
    for sentence in all_input_sentences:
        xml += sentence
    xml += end_doc
    f = open('./data/raw/search_test.xml', 'w+', encoding = 'utf-8')
    f.write(xml)
    f.close()

def sentiment_data_generation(args, sentences, terms):
    construct_data(sentences, terms)

    raw_test_path = './data/raw/search_test.xml'

    test_data = generate_sentence(raw_test_path, lowercase=True)

    word2index, index2word = generate_vocab(test_data, max_size=args.max_vocab_size, min_freq=args.min_vocab_freq)
    if not os.path.exists('./data/processed/'):
        os.makedirs('./data/processed/')

    save_term_data(test_data, word2index, './data/processed/search_test.npz', tokenizer, bert_tokenizer)

    glove = load_glove(args.glove_file, len(index2word), word2index)
    sentiment_matrix = load_sentiment_matrix(args.glove_file, args.add_predefined_sentiment)
    np.save('./data/processed/glove.npy', glove)
    np.save('./data/processed/sentiment_matrix.npy', sentiment_matrix)
    with open('./data/processed/word2index.pickle', 'wb') as handle:
        pickle.dump(word2index, handle)
    with open('./data/processed/index2word.pickle', 'wb') as handle:
        pickle.dump(index2word, handle)
    analyze = analyze_term
    log = {
        'vocab_size': len(index2word),
        'oov_size': len(word2index) - len(index2word),
        'train_data': analyze(test_data),
        'val_data': analyze(test_data),
        'test_data': analyze(test_data),
        'num_categories': 3
    }
    if not os.path.exists('./data/log/'):
        os.makedirs('./data/log/')
    with open('./data/log/log.yml', 'w') as handle:
        yaml.safe_dump(log, handle, encoding='utf-8', allow_unicode=True, default_flow_style=False)
