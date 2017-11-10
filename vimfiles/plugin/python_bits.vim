" If already done, exit early
if exists('g:did_my_python_bits')
    finish
endif

let g:did_my_python_bits = 1

if !has('python')
    finish
endif

" 1/ expand source script file to full path
" 2/
let s:path = fnamemodify(resolve(expand('<sfile>:p')), ":h")

" echom "path is" . s:path

function! Snippet()
    execute 'pyfile' . s:path . '/snippet.py'
endfunc

command! SNIPPET call Snippet()
" keys
