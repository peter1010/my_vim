# Build Code
import sys
import os

def execute_ghs(dirname):
    pass

def find_build_file(dirname, ext):
    files = os.listdir(dirname)
    if "makefile" in files or "Makefile" in files:
        execute_make(dirname)
    elif "defaults.gpj" in files and ext in (".c", ".h", ".cpp", ".hpp"):
        execute_ghs(direname)
    else:
        print("No Build file found")

def main():
    path = sys.argv[1]
    dirname, filename = os.path.split(path)
    ext = os.path.splitext(filename)
    find_build_file(dirname, ext)

if __name__ == "__main__":
    main()
