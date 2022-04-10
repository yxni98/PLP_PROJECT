import random
import xlrd

def construct_data(read_path, output_path, platform):
	readbook = xlrd.open_workbook(read_path)
	sheet = readbook.sheet_by_index(0)

	start_doc = '<?xml version="1.0" encoding="utf-8"?>\n<sentences>\n'
	end_doc = '</sentences>\n'

	count = 0
	text = ''
	term = ''
	polarity = ''
	polarity_dict = {'0':'neutral', '1':'positive', '-1':'negative'}
	text2terms = {}
	if platform == 'amazon':
		for i in range(348):
			polarity = polarity_dict[str(int(float(str(sheet.cell(i,2).value))))]
			original_text = str(sheet.cell(i,3).value)
			term = str(sheet.cell(i,5).value)
			from_index = original_text.index(term)
			to_index = from_index+len(term)
			from_index = str(from_index)
			to_index = str(to_index)
			if original_text not in text2terms.keys():
				text2terms[original_text] = [(from_index, polarity, term, to_index)]
			else:
				text2terms[original_text].append((from_index, polarity, term, to_index))
	elif platform == 'reddit':
		for i in range(179):
			polarity = polarity_dict[str(int(sheet.cell(i,3).value))]
			original_text = str(sheet.cell(i,0).value) + ' ' + str(sheet.cell(i,1).value)
			original_text = original_text.replace('\n', '').replace('<3', '').replace('<4', '')
			term = str(sheet.cell(i,2).value)
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


# construct_data('manually_labeled_amazon.xlsx', 'amazon_raw/', 'amazon')

construct_data('manually_labeled_reddit.xlsx', 'reddit_raw/', 'reddit')