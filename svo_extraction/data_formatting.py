# coding: utf-8

from nltk.tokenize import sent_tokenize
import glob
import os
import string

PATH = '/Users/apple/Desktop/clausie/10out'
NUM_SENT = 0

def isSentence(sentence):
    if len(sentence.split()) < 5:
        return False
#     if sentence.split()[0].isnumeric():
#         return False
    if sentence[-1] not in string.punctuation:
        return False
    if sentence.isupper():
        return False
    if sentence.istitle():
        return False
    count = 0
    for token in sentence.split():
        if len(token) >=2 and token.isupper():
            count += 1
        if token.strip('.').isnumeric():
            count += 1
        elif token in ['p.', 'Vol.', 'pp.', 'Published']:
            count +=3
        if count >=3:
            return False
    return True


def isTitle(sentence):
	if sentence[-1] not in string.punctuation:
		if len(sentence) < Title_length_limit:
			# print sentence
			return True
	if sentence.isupper():
		# print sentence
		return True
	if sentence.istitle():
		# print sentence
		return True

def run():
	with open('cleaned_corenlp_lynching.txt', 'w') as out:
		for file in glob.glob(os.path.join(PATH, '*.txt')):
			with open(file, 'r') as f:
				lines = sent_tokenize(f.read().decode('utf-8'))
				for line in lines:
					# print(line)
					line = line.replace(u"â $ ™", "'")
					line = line.replace(u'â $', '').replace(u'œ', '').replace("''", '').replace("``", '')
					line = line.replace(u"¦", '').replace(u"™", '').strip()
					# print(line)
					# print('\n')
					if isSentence(line):
						out.write(line.encode('utf-8'))
						out.write(' ')

	with open('cleaned_corenlp_lynching.txt', 'r') as f:
		sentences = f.read()
		sentences = sent_tokenize(sentences.decode('utf-8'))
		NUM_SENT = len(sentences)
		print('There are %d number of sentences from the dataset to be fed into ClausIE.' % (NUM_SENT))
		with open('clausie_input.txt','w') as out:
			for i,sentence in enumerate(sentences):
				out.write('%d\t%s\n'% (i, sentence.encode('utf-8'))) 
	return NUM_SENT
