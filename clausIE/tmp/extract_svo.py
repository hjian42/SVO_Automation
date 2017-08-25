# -*- coding: utf-8 -*-
import os
import re
def extract(PATH_OUT):
	start = os.getcwd() 
	os.chdir(os.path.abspath('..'))
	tmp = os.getcwd()
	PATH_sentences_out = '/'.join([PATH_OUT, 'sentences-test-out.txt'])
	PATH_SVO = '/'.join([PATH_OUT, 'svo.txt'])
	os.chdir(start)
	with open(PATH_sentences_out) as f:
		file = f.read()
		matchobj = re.findall(r'SVO \((.*)\)', file)
		# for each in matchobj:
		# 	print each
		file = '\n'.join(matchobj)
		# print file
		r = re.compile('@\d*')
		matchobj = r.sub('',file)
		# print(matchobj)
		file = matchobj
		matchobj = re.sub(r'A\?: \w*,?', '', file)
		# matchobj = unicode(matchobj, 'utf-8')
		matchobj = matchobj.replace('â', "'")
		# print matchobj
		# print type(matchobj)
		with open(PATH_SVO,'w') as out:
			out.write(matchobj)

