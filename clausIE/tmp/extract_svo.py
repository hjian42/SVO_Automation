# -*- coding: utf-8 -*-
import os
import re
def extract(PATH_OUT):
	start = os.getcwd()
	os.chdir(os.path.abspath('..'))
	tmp = os.getcwd()
	PATH_sentences_out = os.path.join(PATH_OUT, 'sentences-test-out.txt')
	PATH_SVO = os.path.join(PATH_OUT, 'raw_svo.txt')
	os.chdir(start)
	with open(PATH_sentences_out) as f:
		file = f.read()
		matchobj = re.findall(r'SV.* \((.*)\)', file)

		file = '\n'.join(matchobj)
		
		# demonstrate two ways of doing the substitution

		# remove @dd patterns
		r = re.compile('@\d*')
		file = r.sub('',file)

		# remove irrelevant labels: only reserve S,V,O
		file = re.sub(r'A[\?\!\-]: \w*,?', '', file) # remove A-, A?, A!
		file = re.sub(r'.COMP: \w*,?', '', file) # remove .COMP
		file = re.sub(r'IO: \w*,?', '', file)

		with open(PATH_SVO,'w') as out:
			out.write(file)

