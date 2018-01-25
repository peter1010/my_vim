import vim
import re
import subprocess
import os

class Tags:

	def __init__(self):
		self.word_break = re.compile("[^a-zA-Z0-9]*[a-zA-Z0-9_]+[^a-zA-Z0-9_]")
		self.last_word = re.compile("([a-zA-Z_][a-zA-Z0-9_]*)$")

	def get_global(self):
		return ['global', '-x', '-r']


	def get_pattern(self):
		row, col = vim.current.window.cursor
		cline = vim.current.buffer[row-1]
		result = self.word_break.match(cline[col:])
		if result:
			result = self.last_word.search(cline[:col+result.end(0)-1])
			if result:
				return result.group(1)
		return None

	def run(self):
		pattern = self.get_pattern()
		args = self.get_global() + [pattern]
		answer = subprocess.check_output(args)
		print answer


def find_tag_plugin(dirname):
	a = "C:\\msys64\\usr\bin\\bash -l -c global"
	return Tags()


def get_plugin():
	return GTAGS()
