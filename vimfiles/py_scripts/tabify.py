import vim
import os


def calculate_size(indent, tabstop):
	idx = 0
	for ws in indent:
		if ws > 0:		# Number of spaces
			idx += ws;
		elif ws < 0:	# Number of tabs
			for j in range(-ws):
				idx = (int(idx / tabstop) + 1) * tabstop
	return idx


def stillInCommentBlock(line):
	while True:
		i = line.find("*/")
		if i >= 0:
			line = line[i+2:]
			i = line.find("/*")
			if i >= 0:
				line = line[i+2:]
			else:
				return False
		else:
			return True


def nowInCommentBlock(line):
	while True:
		i = line.find("/*")
		if i >= 0:
			line = line[i+2:]
			i = line.find("*/")
			if i >= 0:
				line = line[i+2:]
			else:
				return True
		else:
			return False


def stillInTripleQuoteBlock(line):
	while True:
		i = line.find('"""')
		if i >= 0:
			line = line[i+3:]
			i = line.find('"""')
			if i >= 0:
				line = line[i+3:]
			else:
				return False
		else:
			return True


def nowInTripleQuoteBlock(line):
	while True:
		i = line.find('"""')
		if i >= 0:
			j = line.rfind("'", i)
			line = line[i+3:]
			if j >= 0:
				continue
			i = line.find('"""')
			if i >= 0:
				line = line[i+3:]
			else:
				return True
		else:
			return False


class Whitespace:

	def __init__(self):
		self.cnt = 0


	def tabify(self, currLineNum, indent):
		if (len(indent) > 0) and ((indent[0] > 0) or (len(indent) > 1)):
			length = calculate_size(indent, self.tabstop)
			num_of_tabs = int(length / self.tabstop)
			num_of_spaces = length - num_of_tabs * self.tabstop
			whitespace = '\t' * num_of_tabs + ' ' * num_of_spaces
			num_of_chs_to_replace = sum([abs(x) for x in indent])
			old_line = vim.current.buffer[currLineNum]
			if old_line.startswith(whitespace) and num_of_chs_to_replace == len(whitespace):
				return
			vim.current.buffer[currLineNum] = whitespace + old_line[num_of_chs_to_replace:]
			self.cnt -= 1


	def spacify(self, currLineNum, indent):
		if (len(indent) > 0) and ((indent[0] < 0) or (len(indent) > 1)):
			length = calculate_size(indent, self.tabstop)
			whitespace = ' ' * length
			num_of_chs_to_replace = sum([abs(x) for x in indent])
			old_line = vim.current.buffer[currLineNum]
			if old_line.startswith(whitespace) and num_of_chs_to_replace == len(whitespace):
				return
			vim.current.buffer[currLineNum] = whitespace + old_line[num_of_chs_to_replace:]
			self.cnt += 1


	def find_idents(self, actionFn):
		inCommentBlock = False
		inTripleQuoteBlock = False
		inLineContdBlock = False
		buf = vim.current.buffer
		for lineNum in range(len(buf)):
			line = buf[lineNum]

			# Is there a line continuation marker, meaning next line is
			# continuation of this line?
			hasLineContdMarker = line.endswith('\\')

			if inLineContdBlock:
				inLineContdBlock = hasLineContdMarker
				continue
			inLineContdBlock = hasLineContdMarker

			line = line.rstrip()
			if len(line) == 0:
				continue
			if inCommentBlock:
				inCommentBlock = stillInCommentBlock(line)
				continue
			if inTripleQuoteBlock:
				inTripleQuoteBlock = stillInTripleQuoteBlock(line)
				continue
			indent = []
			cnt = 0
			prevCh = None
			for ch in line:
				if ch == '\t':
					if prevCh == ' ':
						indent.append(cnt)
						cnt = 1
					else:
						cnt += 1
				elif ch == ' ':
					if prevCh == '\t':
						indent.append(-cnt)
						cnt = 1
					else:
						cnt += 1
				else:
					if prevCh == ' ':
						indent.append(cnt)
					elif prevCh == '\t':
						indent.append(-cnt)
					elif len(indent) == 0:
						indent.append(0)
					break

				prevCh = ch
			inCommentBlock = nowInCommentBlock(line)
			inTripleQuoteBlock = nowInTripleQuoteBlock(line)
#			print(lineNum, indent, inTripleQuoteBlock)
			actionFn(lineNum, tuple(indent))

	def load_settings(self):
		buf = vim.current.buffer
		dirpath, filename = os.path.split(buf.name)
		modelines = os.path.join(dirpath, ".modelines")
		try:
			with open("modelines", "r") as inFp:
				for line in inFp:
					if line.startswith(filename + '\t'):
						modeline = line[len(filename)+1:]
						break
		except IOError:
			modeline = None


def main():
	settings = Whitespace()
	options = vim.current.buffer.options
	settings.tabstop = options['tabstop']

	if sys.argv[1] == 't':
		func = settings.tabify
	elif sys.argv[1] == 's':
		func = settings.spacify
	else:
		settings.load_settings()
		func = None
	if func:
		settings.find_idents(func)

	if settings.cnt > 0:
		print("% i lines spacified" % settings.cnt)
	elif settings.cnt < 0:
		print("% i lines tabified" % -settings.cnt)
	else:
		print("No lines modified")


main()
