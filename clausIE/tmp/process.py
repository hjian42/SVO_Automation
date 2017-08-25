import data_formatting
import extract_svo
import subprocess
import filtering
import os
import sys
import completeArticles
reload(sys)
sys.setdefaultencoding("utf-8")

#subprocess.call(['python', 'install.py'])

do_coref = sys.argv[1]
PATH_IN = sys.argv[2]
PATH_OUT = sys.argv[3]
coref_out = PATH_OUT + '/processed_input'
path_processed = coref_out
if not os.path.exists(coref_out):
    os.makedirs(coref_out)

if __name__ == '__main__':
	NUM_SENT = 0
	startingDir = os.getcwd()
	if do_coref == "coref":
		os.chdir(os.path.abspath('../../Miscellaneous'))
		subprocess.call(['java', '-jar', 'Coref.jar', '-inputDir', PATH_IN, '-outputDir', coref_out])
		os.chdir(startingDir)
	else:
		# path_processed = PATH_IN
		completeArticles.clean(PATH_IN, path_processed)
		# write everything in to the processed_output
	NUM_SENT = data_formatting.run(PATH_OUT, path_processed)
	os.chdir(os.path.abspath('..'))
	path_clausie_input = '/'.join([PATH_OUT, 'clausie_input.txt'])
	path_clausie_out = '/'.join([PATH_OUT, 'sentences-test-out.txt'])
	subprocess.call(['java', '-jar', 'clausie.jar', '-vlf', path_clausie_input, '-o', path_clausie_out])
	os.chdir(startingDir)
	extract_svo.extract(PATH_OUT)
	filtering.svo_filter(NUM_SENT, PATH_OUT)
	
# python process.py coref /Users/apple/Desktop/clausie/data1 /Users/apple/Desktop/clausie/data_out