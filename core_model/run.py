from dataset import dataset
from train import train
from test import test
from datetime import datetime


if __name__ == '__main__':
	print(str(datetime.now()))
	print('##################### DATA PROCESS ###################################')
	dataset()

	print(str(datetime.now()))
	print('##################### TRAINING ###################################')
	train()

	print(str(datetime.now()))
	print('##################### TESTING ###################################')
	test()
