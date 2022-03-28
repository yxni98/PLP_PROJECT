from config import args
from data_utils.data_transfer import data_transfer
from data_utils.data_generation import data_generation

read_path = './laptop_raw_data/'
output_path = './data/raw/'

data_path = './data'
max_vocab_size = None
min_vocab_freq = 0

glove_file = './data/glove.840B.300d.txt'
add_predefined_sentiment = './data/sentiment_dict.json'

data_transfer(read_path, output_path)
data_generation(args)
print('data ready!')