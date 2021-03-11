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
		elif token.startswith("no"):
			name, value = token[2:], False
		else:
			name, value = token, True
		if name in ALLOW_SETTINGS:
			options[name] = value


def load_settings():
	buf = vim.current.buffer
	dirpath, filename = os.path.split(buf.name)
	modelines = os.path.join(dirpath, ".modelines")
	try:
		with open(modelines, "r") as inFp:
			for line in inFp:
				if line.startswith(filename + '\t'):
					modeline = line[len(filename)+1:]
					break
	except IOError:
		modeline = None

def save_settings(modeline):
	buf = vim.current.buffer
	dirpath, filename = os.path.split(buf.name)
	modelines = os.path.join(dirpath, ".modelines")
	found = False
	lines = []
	try:
		with open(modelines, "r") as inFp:
			for line in inFp:
				if line.startswith(filename + '\t'):
					if not found:
						found = True
						lines.append(filename + '\t' + modeline + '\n')
				else:
					lines.append(line)
	except IOError:
		pass
	if not found:
		lines.append(filename + '\t' + modeline + '\n')

	with open(modelines, "w") as outFp:
		outFp.writelines(lines)


def main():

	if sys.argv[1] == 'r':
		modeline = load_settings()
		if modeline:
			set_settings(modeline)
	elif sys.argv[1] == 'w':
		modeline = get_modeline()
		save_settings(modeline)

main()
