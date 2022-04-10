from config import args
from data_utils.data_transfer import data_transfer
from data_utils.data_generation import data_generation

def dataset():
	# data_transfer(args.read_path, args.output_path)
	data_generation(args)
