# Build Code
import sys
import os
import subprocess

def execute_ghs(dirname):
	args = [os.path.join("C:\\", "ghs", "mips524", "gbuild.exe"), "-top", os.path.join(dirname, "default.gpj")]
	print args
	subprocess.call(args)

def find_build_file(dirname, ext):
	files = os.listdir(dirname)
	if "makefile" in files or "Makefile" in files:
		execute_make(dirname)
	elif "default.gpj" in files and ext in (".c", ".h", ".cpp", ".hpp"):
		execute_ghs(dirname)
	else:
		dirname, filename = os.path.split(dirname)
		if dirname and filename:
			return find_build_file(dirname, ext)
		else:
			print("No Build file found", dirname, filename)

def main():
    path = sys.argv[1]
    dirname, filename = os.path.split(path)
    filename, ext = os.path.splitext(filename)
    find_build_file(dirname, ext)

if __name__ == "__main__":
    main()
