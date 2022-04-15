# PLP_PROJECT

## environment requiement
To run this project, you need to install the following libraries
* pytorch
* pytorch-pretrained-bert
* spacy
* numpy
* scipy
* scikit-learn
* pyyaml
* adabound
* xlrd==1.2.0

## data requiement
To enable init representation of words, you need to download the glove file from http://nlp.stanford.edu/data/wordvecs/glove.840B.300d.zip, and put the txt file under the 'data' directory.

## sentiment analysis model workflow
This project is developed based on capsule network, execute the command 'python run.py' and you will see the results of 'data processing', 'training' and 'testing'.

## configuration
To see results from different settings, just modify the 'config.py'.

## detailed workflow
1. Run the 'dataset.py', the laptop review files under the 'laptop_raw_data' directory would be combined and generate 'train/val/test' files under the path 'data/raw/', which are all in 'xml' format, recording the correct aspect terms and the corresponding sentiment labels from each given sentence. Note that train : val : test = 8 : 1 : 1 (see line 64 in 'data_utils/data_transfer.py'). Then it generates 'log' and 'processed' folders under the 'data' path, which would be used in training and testing stages. 
2. Run the 'train.py', which construct model and train the model with 'data/processed/train.xml' and 'data/processed/val.xml'.
3. Run the 'test.py', which load the checkpoint learned before and output the test results on 'data/processed/test.xml'.

## the website url (Welcome to use!)
The website link is the http://plp2022acas.natapp1.cc/index/, we recommend you to run it on your phone.
