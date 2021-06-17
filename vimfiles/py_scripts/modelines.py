import vim
import os

ALLOW_SETTINGS = (
	'shiftwidth',
	'softtabstop',
	'expandtab',
	'tabstop',
	'autoindent'
)

def get_modeline():
	tokens = []
	options = vim.current.buffer.options
	for name in ALLOW_SETTINGS:
		value = options[name]
		if value is True:
			tokens.append(name)
		elif value is False:
			tokens.append("no" + name)
		else:
			tokens.append(name + "=" + str(value))
	return ":".join(tokens)


def set_modeline(modeline):
	options = vim.current.buffer.options
	tokens = modeline.split(":")
	for token in tokens:
		idx = token.find("=")
		if idx >= 0:
			name, value = token[:idx], token[idx+1:]
			value = int(value)
		elif token.startswith("no"):
			name, value = token[2:], False
		else:
			name, value = token, True
		if name in ALLOW_SETTINGS:
			options[name] = value

def find_modelines():
	buf = vim.current.buffer
	dirpath, filename = os.path.split(os.path.abspath(buf.name))
	if os.name.lower() == "nt":
		filename = "_modelines"
	else:
		filename = ".modelines"
	default_path = os.path.join(dirpath, filename)
	prev_dirpath = dirpath
	for i in range(10):
		modelines = os.path.join(dirpath, filename)
		if os.path.exists(modelines):
			return modelines
		dirpath = os.path.split(dirpath)[0]
		if dirpath == prev_dirpath:
			break
		prev_dirpath = dirpath

	return default_path

def load_settings():
	modelines = find_modelines()
	print(modelines)
	buf = vim.current.buffer
	filetype = os.path.splitext(buf.name)[1].lower()
	try:
		with open(modelines, "r") as inFp:
			for line in inFp:
				if line.startswith(filetype + '\t'):
					modeline = line[len(filetype)+1:]
					break
	except IOError:
		modeline = None
	return modeline

def save_settings(modeline):
	modelines = find_modelines()
	buf = vim.current.buffer
	filetype = os.path.splitext(buf.name)[1].lower()
	found = False
	lines = []
	try:
		with open(modelines, "r") as inFp:
			for line in inFp:
				if line.startswith(filetype + '\t'):
					if not found:
						found = True
						lines.append(filetype + '\t' + modeline + '\n')
				else:
					lines.append(line)
	except IOError:
		pass
	if not found:
		lines.append(filetype + '\t' + modeline + '\n')

	with open(modelines, "w") as outFp:
		outFp.writelines(lines)


def main():

	if sys.argv[1] == 'r':
		modeline = load_settings()
		if modeline:
			set_modeline(modeline)
	elif sys.argv[1] == 'w':
		modeline = get_modeline()
		save_settings(modeline)

main()
