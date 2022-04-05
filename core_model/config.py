class params(object):
	"""docstring for params"""
	def __init__(self):
		super(params, self).__init__()
		self.read_path = './laptop_raw_data/'
		self.output_path = './data/raw/'
		self.data_path = './data'
		self.max_vocab_size = None
		self.min_vocab_freq = 0
		self.glove_file = './data/glove.840B.300d.txt'
		self.add_predefined_sentiment = './data/sentiment_dict.json'
		self.num_epoches = 12
		self.learning_rate = 0.0003
		self.weight_decay = 0
		self.embed_size = 300
		self.num_layers = 3
		self.capsule_size = 300
		self.bidirectional = True
		self.dropout = 0.1
		self.batch_size = 64
		self.gpu_device = '1'
		self.optimizer = 'adam'

args = params()
