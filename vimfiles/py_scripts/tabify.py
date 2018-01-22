import vim

likely_indent = None
likely_dont_use_tabs_for_indent = None
likely_tabs_equals_indent = None
likely_dont_expand_tabs = None

def get_ident():
	options = vim.current.buffer.options
	return options['shiftwidth'], options['expandtab'], options['tabstop']


def set_ident(indent, dont_use_tabs, indent_equals_tabs, dont_expand_tabs):
#	print dir(vim.options)
	options = vim.current.buffer.options
	options['shiftwidth'] = indent
	if dont_use_tabs:
		options['softtabstop'] = indent
		if dont_expand_tabs:
			options['expandtab'] = False
		else:
			options['expandtab'] = True
	else:
		options['expandtab'] = False
	if indent_equals_tabs:
		options['tabstop'] = indent
	else:
		options['tabstop'] = 8

def calculate_size(indent, tabstop):
	idx = 0
	for ws in indent:
		if ws > 0:
			idx += ws;
		elif ws < 0:
			for j in range(-ws):
				idx = (int(idx / tabstop) + 1) * tabstop
	return idx;

prev_indent = []
def analysis_idents(curLineNum, indent, settings):
	global prev_indent
	if len(indent) > 0:
		if len(indent) > 1:
			# Mixed tabs and whitespace
			settings.likely_dont_use_tabs_for_indent = True
			settings.likely_dont_expand_tabs = True
		elif indent[0] > 0:
			# Spaces
			settings.likely_dont_use_tabs_for_indent = True
			if indent[0] > 1:
				if (settings.likely_indent is None) or (indent[0] < settings.likely_indent):
					settings.likely_indent = indent[0]
                    
		elif indent[0] < 0:
			# Tabs
			if (prev_indent == []) and (indent[0] == -1):
				settings.likely_tabs_equals_indent = True
	prev_indent = indent	
      	

def tabify(currLineNum, indent, settings):
	length = calculate_size(indent, settings.tabstop)
	num_of_tabs = int(length / settings.tabstop)
	num_of_spaces = length - num_of_tabs * settings.tabstop
	whitespace = '\t' * num_of_tabs + ' ' * num_of_spaces
	num_of_chs_to_replace = sum([abs(x) for x in indent])
	old_line = vim.current.buffer[currLineNum] 
	if num_of_chs_to_replace == len(whitespace):
		if old_line.startswith(whitespace):
			return
	vim.current.buffer[currLineNum] = whitespace + old_line[num_of_chs_to_replace:]

def spacify(currLineNum, indent, settings):
	length = calculate_size(indent, settings.tabstop)
	whitespace = ' ' * length
	num_of_chs_to_replace = sum([abs(x) for x in indent])
	old_line = vim.current.buffer[currLineNum] 
	if num_of_chs_to_replace == len(whitespace):
		if old_line.startswith(whitespace):
			return
	vim.current.buffer[currLineNum] = whitespace + old_line[num_of_chs_to_replace:]



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
			line = line[i+3:]
			i = line.find('"""')
			if i >= 0:
				line = line[i+3:]
			else:
				return True
		else:
			return False

def find_idents(actionFn, settings):
	tabIdents, spaceIdents = 0, 0
	inCommentBlock = False
	inTripleQuoteBlock = False
	lineNum = 0
	while True:
		curLineNum = lineNum
		line = vim.current.buffer[lineNum]
		lineNum += 1
		while line.endswith('\\'):
			line = line[:-1] + vim.current.buffer[lineNum]
			lineNum += 1
        
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
				prevCh = ch
			elif ch == ' ':
				if prevCh == '\t':
					indent.append(-cnt)
					cnt = 1
				else:
					cnt += 1
				prevCh = ch
			else:
				if prevCh == ' ':
					indent.append(cnt)
				elif prevCh == '\t':
					indent.append(-cnt)
				break
		inCommentBlock = nowInCommentBlock(line)
		inTripleQuoteBlock = nowInTripleQuoteBlock(line)
		print(curLineNum, indent, inCommentBlock, inTripleQuoteBlock, line)
		actionFn(curLineNum, indent, settings)


class Settings:
	pass

def main():
	settings = Settings()
	settings.tabstop = 4

	if sys.argv[0] == 't':
		func = tabify
	elif sys.argv[0] == 's':
		func = spacify
	else:
		func = analysis_idents
	try:
		find_idents(func, settings)
	except IndexError:
		pass
	print(likely_indent, likely_dont_use_tabs_for_indent, likely_tabs_equals_indent, likely_dont_expand_tabs)
	set_ident(likely_indent, likely_dont_use_tabs_for_indent, likely_tabs_equals_indent, likely_dont_expand_tabs)
#    row, col = vim.current.window.cursor
#    row -= 1
#    cline = vim.current.buffer[row]
#
#    func = select_snippet(cline)
#    if func:
#        func(row)

main()
