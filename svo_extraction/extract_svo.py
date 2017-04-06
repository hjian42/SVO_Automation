import re
def extract():
	with open('sentences-test-out.txt') as f:
		file = f.read()
		matchobj = re.findall(r'SVO \((.*)\)', file)
		# for each in matchobj:
		# 	print each
		file = '\n'.join(matchobj)
		# print file
		r = re.compile('@\d*')
		matchobj = r.sub('',file)
		# print matchobj
		# print type(matchobj)
		file = matchobj
		matchobj = re.sub(r'A\?: \w*,?', '', file)
		print matchobj
		with open('svo.txt','w') as out:
			out.write(matchobj)

