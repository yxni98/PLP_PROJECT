import random

def data_transfer(read_path, output_path):

	start_doc = '<?xml version="1.0" encoding="utf-8"?>\n<sentences>\n'
	end_doc = '</sentences>\n'

	count = 0
	text = ''
	term = ''
	polarity = ''
	polarity_dict = {'0':'neutral', '1':'positive', '-1':'negative'}
	text2terms = {}
	for line in open(read_path+'Laptops_Train.xml.seg', 'r', encoding = 'utf-8'):
		if count%3 == 0:
			text = line.replace('\n', '')
			text = line.replace('"', '')
		elif count%3 == 1:
			term = line.replace('\n', '')
			term = line.replace('"', '')
			from_index = text.index('$T$')
			to_index = from_index+len(term)
			from_index = str(from_index)
			to_index = str(to_index)
		elif count%3 == 2:
			polarity = polarity_dict[line.replace('\n', '')]
			original_text = text.replace('$T$', term)
			if original_text not in text2terms.keys():
				text2terms[original_text] = [(from_index, polarity, term, to_index)]
			else:
				text2terms[original_text].append((from_index, polarity, term, to_index))
		count += 1
	for line in open(read_path+'Laptops_Test_Gold.xml.seg', 'r', encoding = 'utf-8'):
		if count%3 == 0:
			text = line.replace('\n', '')
			text = line.replace('"', '')
		elif count%3 == 1:
			term = line.replace('\n', '')
			term = line.replace('"', '')
			from_index = text.index('$T$')
			to_index = from_index+len(term)
			from_index = str(from_index)
			to_index = str(to_index)
		elif count%3 == 2:
			polarity = polarity_dict[line.replace('\n', '')]
			original_text = text.replace('$T$', term)
			if original_text not in text2terms.keys():
				text2terms[original_text] = [(from_index, polarity, term, to_index)]
			else:
				text2terms[original_text].append((from_index, polarity, term, to_index))
		count += 1

	all_input_sentences = []
	for text in text2terms.keys():
		aspect_terms = ''
		for term_unit in text2terms[text]:
			aspect_term = '\t\t\t<aspectTerm from="%s" polarity="%s" term="%s" to="%s"/>\n' % (term_unit[0], term_unit[1], term_unit[2], term_unit[3])
			aspect_terms += aspect_term
		input_sentence = '\t<sentence>\n\t\t<text>%s</text>\n\t\t<aspectTerms>\n%s\t\t</aspectTerms>\n\t</sentence>\n' % (text, aspect_terms)
		all_input_sentences.append(input_sentence)

	random.shuffle(all_input_sentences)
	length = len(all_input_sentences)
	# train : val : test = 8 : 1 : 1
	train_sentences = all_input_sentences[:int(0.8*length)]
	valid_sentences = all_input_sentences[int(0.8*length):int(0.9*length)]
	test_sentences = all_input_sentences[int(0.9*length):]

	xml = ''
	xml += start_doc
	for sentence in train_sentences:
		xml += sentence
	xml += end_doc
	f = open(output_path+'train.xml', 'w+', encoding = 'utf-8')
	f.write(xml)
	f.close()

	xml = ''
	xml += start_doc
	for sentence in valid_sentences:
		xml += sentence
	xml += end_doc
	f = open(output_path+'val.xml', 'w+', encoding = 'utf-8')
	f.write(xml)
	f.close()

	xml = ''
	xml += start_doc
	for sentence in test_sentences:
		xml += sentence
	xml += end_doc
	f = open(output_path+'test.xml', 'w+', encoding = 'utf-8')
	f.write(xml)
	f.close()