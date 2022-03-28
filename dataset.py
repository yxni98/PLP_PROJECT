from config import args

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