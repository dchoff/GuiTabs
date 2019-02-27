import subprocess
from sys import argv
import os

def generate_pdf(file_name):
	if os.path.isfile('./ly_files/{0}.ly'.format(file_name)):
		subprocess.run("lilypond --pdf ./ly_files/{0}.ly".format(file_name))
		os.startfile("{0}.pdf".format(file_name))
	else:
		print('Please make sure that you inputted a valid .ly file name, and moved it into the ./ly_files/ directory.')
		raise FileNotFoundError('Program was unable to find file {0}.ly in the ./ly_files/ directory.'.format(file_name))


f_name = argv[1]
generate_pdf(f_name)
