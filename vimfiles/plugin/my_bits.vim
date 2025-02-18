" If already done, exit early
" g: means global namespace

if exists('g:did_my_bits')
    finish
endif

let g:did_my_bits = 1

function! Trim()
    " find whitespace at end of line and replace with nothing (/e means don't
    " erro if nothing found
    execute '%s/\s\+$//e'
endfunc

command! TABIFY call my_bits#tabify#Tabify()
command! SPACIFY call my_bits#tabify#Spacify()
command! TRIM call Trim()

function! DetectIndentation(language)
    call my_bits#tabify#DetectIndent(a:language)
endfunc


if !has('pythonx')
    finish
endif

" Expand source script file to full path
" The s: put the variable in the script's namespace
let s:path = fnamemodify(resolve(expand('<sfile>:p')), ":h:h") . '/pythonx'

" echom "path is " . s:path

"& in from of a option means treat the option as a variable
"This means the option is set to the evaluation of the expression
let &makeprg = 'python "' . s:path . '/build.py" %:p'

" -> "filename", line y:x E:comment
set efm=\"%f\"\\,\ line\ %l:%c\ %t:%m


function! Gtag()
    execute 'pythonx import sys'
    execute 'pythonx sys.argv = [r"' . s:path . '/gtags.py", "b"]'
    execute 'pyxfile ' . s:path . '/gtags.py'
endfunc

command! GTAG call Gtag()

function! LspGet(type)
    execute 'pythonx import sys'
    execute 'pythonx sys.argv = [r"' . s:path . '/lsp/client.py", r"' . a:type . '"]'
    execute 'pyxfile ' . s:path . '/lsp/client.py'
endfunc


command! LSPxDCL call LspGet("find_declaration")
command! LSPxDEF call LspGet("find_definition")
command! LSPxIMP call LspGet("find_implementation")
command! LSPxREF call LspGet("find_references")
command! LSPxHOV call LspGet("hover")
