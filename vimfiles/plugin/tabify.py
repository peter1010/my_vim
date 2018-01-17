import vim

def func_header_snippet(row):
    cmt = "//!"
    cb = vim.current.buffer
    start = row
    while start >= 0:
        line = cb[start-1].strip()
        if not line.startswith(cmt):
            break
        start -= 1



    print("HDR")

def select_snippet(line):
    line = line.strip()
    if line.startswith("//!"):
        return func_header_snippet

def stillInCommentBlock(line):
    while True:
        i = line.find("*/")
        if i > 0:
            line = line[i+2]
            i = line.find("/*")
            if i > 0:
                line = line[i+2]
            else:
                return False
        else:
            return True

def nowInCommentBlock(line):
    while True:
        i = line.find("/*")
        if i > 0:
            line = line[i+2]
            i = line.find("*/")
            if i > 0:
                line = line[i+2]
            else:
                return True
        else:
            return False

def stillInTripleQuoteBlock(line):
    while True:
        i = line.find('"""')
        if i > 0:
            line = line[i+3]
            i = line.find('"""')
            if i > 0:
                line = line[i+3]
            else:
                return False
        else:
            return True


def nowInTripleQuoteBlock(line):
    while True:
        i = line.find('"""')
        if i > 0:
            line = line[i+3]
            i = line.find('"""')
            if i > 0:
                line = line[i+3]
            else:
                return True
        else:
            return False


def analysis_idents():
    tabIdents, spaceIdents = 0, 0
    inCommentBlock = False
    inTripleQuoteBlock = False
    line = ""
    for partline in vim.current.buffer:
        line += partline
        if line.endswith('\\'):
            continue
        line = line.rstrip()
        if len(line) == 0:
            continue
        if inCommentBlock:
            inCommentBlock = stillInCommentBlock(line)
            line = ""
            continue
        if inTripleQuoteBlock:
            inTripleQuoteBlock = stillInTripleQuoteBlock(line)
            line = ""
            continue
        ident = []
        cnt = 0
        prevCh = None
        for ch in line:
            if ch == '\t':
                if prevCh == ' ':
                    ident.append(cnt)
                    cnt = 1
                else:
                    cnt += 1
                prevCh = ch
            elif ch == ' ':
                if prevCh == '\t':
                    ident.append(-cnt)
                    cnt = 1
                else:
                    cnt += 1
                prevCh = ch
            else:
                if prevCh == ' ':
                    ident.append(cnt)
                elif ident == '\t':
                    ident.append(-cnt)
                break
        print(ident)
        inCommentBlock = nowInCommentBlock(line)
        inTripleQuoteBlock = nowInTripleQuoteBlock(line)
        line = ""

def main():
    analysis_idents()
#    row, col = vim.current.window.cursor
#    row -= 1
#    cline = vim.current.buffer[row]
#
#    func = select_snippet(cline)
#    if func:
#        func(row)

main()
