#!/usr/bin/env bash
function usage() {
    echo "NAME:"
    echo "    print the absolte path of target File(s) or Folder(s)."
    echo "SYNOPSIS:"
    echo "    abspath <target> ..."
    echo "AUTHOR:"
    echo "    YP CHEN, 2020-08-05"
    exit 1
}

if [[ '--help' =~ $1 ]]; then
    if [[ $# -ne 0 ]]; then
        usage
    fi
fi

# If no argument, the current working directory will be print.
if [[ $# -eq 0 ]]; then
    pwd
else
    # Multiple arguments
    for fd in $@
    do
        if [[ -f $fd ]]; then
            # If relative path of a file was supplied.
            echo $fd | grep '/' > /dev/null
            if [[  $? -eq 0 ]]; then
                cd $(dirname $fd) && echo $PWD/$(basename $fd) && cd - > /dev/null
            else
                echo $PWD/$fd
            fi
        elif [[ -d $fd ]]; then
            # If realative path of a folder was supplied.
            echo $fd | grep '/' > /dev/null
            if [[ $? -eq 0 ]]; then
                cd $fd && echo $PWD && cd - > /dev/null
            else
                cd $fd && echo $PWD && cd - > /dev/null
            fi
        else
            # Unknown arguments
            echo "[ERROR] Invalid input: $fd"
        fi
    done
fi