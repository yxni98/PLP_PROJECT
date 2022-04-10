from dataset import dataset
from train import train
from test import test
from datetime import datetime
from config import args

if __name__ == '__main__':
	print(str(datetime.now()))
	print('##################### DATA PROCESS ###################################')
	dataset()

	for lr in [0.0001, 0.001, 0.01, 0.1]:
		for layerno in [1, 2, 3, 4, 5]:
			print('##################### CONFIGURATION ##############################')
			args.learning_rate = lr
			args.num_layers = layerno
			print(lr, layerno)
			print(str(datetime.now()))
			print('##################### TRAINING ###################################')
			train(args)

			print(str(datetime.now()))
			print('##################### TESTING ####################################')
			test(args)
