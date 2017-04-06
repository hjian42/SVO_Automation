import data_formatting
import extract_svo
import subprocess
import filtering
import os
 
if __name__ == '__main__':
	NUM_SENT = data_formatting.run()
	startingDir = os.getcwd()
	os.chdir(os.path.abspath('..'))
	subprocess.call(['java', '-jar', 'clausie.jar', '-vlf', 'tmp/clausie_input.txt', '-o', 'tmp/sentences-test-out.txt'])
	os.chdir(startingDir)
	extract_svo.extract()
	filtering.svo_filter(NUM_SENT)
	