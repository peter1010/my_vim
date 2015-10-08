" If already done, exit early
if exists('g:did_my_python_bits')
    finish
endif

let g:did_my_python_bits = 1

if !has('python')
    finish
endif

" keys


