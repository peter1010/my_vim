import vim
import os
import sys

TYPES_DIR = "tag_types"

def find_tag_plugin(plugin_dir, dirname, ext):
	"""Give a list of plugins, find which (if any) can do the tag function from the working directory dirname, given the file
		extension ext of the file in the current vim buffer"""
	for script in os.listdir(plugin_dir):
		if script.endswith(".py"):
			name = script[:-3]
			mod = importlib.import_module("{}.{}".format(TYPES_DIR, name))
			if hasattr(mod, "get_plugin"):
				plugin = mod.get_plugin()
				if plugin.can_build(dirname, ext):
					return plugin

	# Go up to the next level in the build tree and try again..
	dirname, removedPath = os.path.split(dirname)
	if dirname and removedPath:
		return find_build_plugin(plugin_dir, dirname, ext)
	else:
		return None

def main():
	print("|", sys.argv[0], "|")
#	plugin_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), TYPES_DIR))
	filepath = vim.current.buffer.name
	dirname, filename = os.path.split(filepath)
	filename, ext = os.path.splitext(filename)
	plugin = find_tag_plugin(plugin_dir, dirname, ext)
	if plugin:
		plugin.run()

main()
