# Build Code
import sys
import os
import importlib

import output_window

def load_plugins(plugin_dir):
	plugins = []
	for script in os.listdir(plugin_dir):
		if script.endswith(".py"):
			name = script[:-3]
			mod = importlib.import_module("build_types." + name)
			if hasattr(mod, "get_plugin"):
				plugins.append(mod.get_plugin())
	return plugins
        
def find_build_plugin(plugins, dirname, ext):
	for plugin in plugins:
		if plugin.can_build(dirname, ext):
			return plugin
	dirname, filename = os.path.split(dirname)
	if dirname and filename:
		return find_build_plugin(plugins, dirname, ext)
	else:
		print("No Build file found", dirname, filename)
		return None

def main():
	plugin_dir = os.path.abspath(os.path.join(os.path.dirname(sys.argv[0]), "build_types"))
	filepath = sys.argv[1]
	if len(sys.argv) > 2:
		action = sys.argv[2]
	else:
		action = None
	plugins = load_plugins(plugin_dir)
	dirname, filename = os.path.split(filepath)
	filename, ext = os.path.splitext(filename)
	plugin = find_build_plugin(plugins, dirname, ext)
	if plugin:
		output = output_window.OutputWindow()
		output.open()
		error_list = plugin.run(action, output)
		for err in error_list:
		    print(err)

if __name__ == "__main__":
	main()
