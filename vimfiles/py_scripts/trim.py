import vim

def main():
    cnt = 0
    buf = vim.current.buffer
    for lineNum in range(len(buf)):
	line = buf[lineNum]
	newline = line.rstrip()
	if len(line) != len(newline):
            cnt += 1
	    buf[lineNum] = newline
    if cnt > 0:
        print("%i lines trimmed" % cnt)
    else:
        print("No lines trimmed")

main()
