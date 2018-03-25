import data_formatting
import extract_svo
import subprocess
import filtering
import sys, os
import preprocess

#subprocess.call(['python', 'install.py'])
# python process.py none /Users/hang/Desktop/automatic-svo-extraction-master/clausIE/data/input /Users/hang/Desktop/automatic-svo-extraction-master/clausIE/data

# set up the initial parameters 
do_coref = sys.argv[1]
PATH_IN = sys.argv[2]
PATH_OUT = sys.argv[3]
coref_out = os.path.join(PATH_OUT, 'processed_input')

# create processed_input folder
path_processed = coref_out
if not os.path.exists(coref_out):
    os.makedirs(coref_out)

if __name__ == '__main__':

	NUM_SENT = 0
	startingDir = os.getcwd()

	# choose mode: "coref" for coreference-resolution; "none" for plain text
	if do_coref == "coref":
		os.chdir(os.path.abspath('../../Miscellaneous'))
		subprocess.call(['java', '-jar', 'Coref.jar', '-inputDir', PATH_IN, '-outputDir', coref_out])
		os.chdir(startingDir)
	elif do_coref == "none":
		preprocess.clean(PATH_IN, path_processed)

	NUM_SENT = data_formatting.run(PATH_OUT, path_processed)
	os.chdir(os.path.abspath('..'))
	path_clausie_input = os.path.join(PATH_OUT, 'clausie_input.txt')
	path_clausie_out = os.path.join(PATH_OUT, 'sentences-test-out.txt')
	subprocess.call(['java', '-jar', 'clausie.jar', '-vlf', path_clausie_input, '-o', path_clausie_out])
	os.chdir(startingDir)
	extract_svo.extract(PATH_OUT)
	filtering.svo_filter(NUM_SENT, PATH_OUT, use_actors=False)
	


