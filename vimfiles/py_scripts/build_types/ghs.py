# Build Code
import os
import subprocess

class GHS:

	def __init__(self):
		pass

	def can_build(self, dirname, ext):
		if ext in (".c", ".h", ".cpp", ".hpp"):
			build_file = os.path.join(dirname, "default.gpj")
			if os.path.exists(build_file):
				self.build_file = build_file
				return True
		return False

	def run(self, action, output):
		args = [os.path.join("C:\\", "ghs", "mips524", "gbuild.exe"), "-top", self.build_file]
		print(args)
		subprocess.call(args)

def get_plugin():
	return GHS()
