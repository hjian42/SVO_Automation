import data_formatting
import extract_svo
import subprocess

if __name__ == '__main__':
	data_formatting.run()
	subprocess.call(['java', '-jar', 'clausie.jar', '-vlf', 'tmp/clausie_input.txt', '-o', 'tmp/sentences-test-out.txt'])
	extract_svo.extract()