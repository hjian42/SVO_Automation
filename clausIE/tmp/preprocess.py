import glob
import os
import re
from nltk.tokenize import sent_tokenize
import string
import sys

# Title_length_limit = int(sys.argv[1])

def isTitle(sentence):
	if sentence[-1] not in string.punctuation:
		if len(sentence) < 15:
			# print sentence
			return True
	if sentence.isupper():
		# print sentence
		return True
	if sentence.istitle():
		# print sentence
		return True

def clean_murphy(PATH_IN, PATH_PROCESSED):

	return

# clean data for the first time
def clean(PATH_IN, PATH_PROCESSED):
	path = PATH_IN
	count = 0
	titles = []
	for filename in glob.glob(os.path.join(path, '*.txt')):
		with open(filename,'r') as each:
			sentences = []
			sentences = each.read().split('\r')
			lst = []
			for sentence in sentences:
				for s in sentence.split('\n'):
					lst.append(s)
			sentences = lst
			sentences = [each.strip() for each in sentences if each.strip()] 
			# filename = filename.split('\\')[-1]
			filename = filename.split('/')[-1]
			file_path = PATH_PROCESSED + '/data%d__%s' % (count, filename)
			with open(file_path, 'w') as out:
				for sentence in sentences:
					if isTitle(sentence):
						if sentence and sentence[-1]!='.':
							out.write(sentence + '.')
						else:
							out.write(sentence)
					else:
						for one in sent_tokenize(sentence):
							out.write(one)
							out.write(' ')
				# titles.append((title,filename))
		count += 1


# with open('/Users/apple/Desktop/Roberto-Research/TitleExtractor/titles.txt','w') as output:
# 	count = 0
# 	for i,title in enumerate(titles):
# 		if title:
# 			count += 1
# 		output.write('\n')
# 		output.write('Essay%d:     %s: ' % (i,title[1]))
# 		output.write('\n')
# 		for t in title[0]:
# 			if t and t[-1]!='.':
# 				output.write(t + '.')
# 			else:
# 				output.write(t)
# 			output.write('\n')

# 	print "There are %s files out of 1150 files that have generated titles." % count
# 	print "The percentage IS %f" % (float(count)/1150)





