" In Windows sometimes the HOME directory is defined as a remote drive
" Lets make it local (also get rid of the dots)

let $HOME = $USERPROFILE
let $VIMFILES = '~/vimfiles'
set runtimepath=$VIMFILES,$VIMRUNTIME
set viminfo+=n$USERPROFILE/vimfiles/viminfo
source $VIMFILES/vimrc
