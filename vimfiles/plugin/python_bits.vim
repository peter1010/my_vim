" If already done, exit early
" g: means global namespace

if exists('g:did_my_python_bits')
    finish
endif

let g:did_my_python_bits = 1

if !has('python')
    finish
endif

" Expand source script file to full path
" The s: put the variable in the script's namespace
let s:path = fnamemodify(resolve(expand('<sfile>:p')), ":h:h") . '/py_scripts'

" echom "path is " . s:path

"& in from of a option means treat the option as a variable
"This means the option is set to the evaluation of the expression
let &makeprg = 'python "' . s:path . '/build.py" %:p'

function! Snippet() 
    execute 'pyfile ' . s:path . '/snippet.py'
endfunc

function! Tabify()
    execute 'python import sys'
    execute 'python sys.argv = ["t"]'
    execute 'pyfile ' . s:path . '/tabify.py'
endfunc

function! Spacify()
    execute 'python import sys'
    execute 'python sys.argv = ["s"]'
    execute 'pyfile ' . s:path . '/tabify.py'
endfunc
    
function! Gtag()
    execute 'pyfile ' . s:path . '/gtags.py'
endfunc

command! SNIPPET call Snippet()
command! TABIFY call Tabify()
command! SPACIFY call Spacify()
command! GTAG call Gtag()

" keys
