#/usr/bin/env bash

<<COMMENT
Author: chenyanpeng
Date  : 2020-09-17
COMMENT

function usage {
cat << EOF

$0 -- get the sequence(s) that match the given id(s) as bait(s).

SYNOPSIS: 
    $0 <id_file.txt> <fasta-file>

OPTIONS:
    -h | --help             print help message and exit
    -v | --invert           select non-matching lines

BUGS:
    Any bugs in fastqInfo should be reported to chenyanpeng1992@outlook.com

EOF
}

# parse long command-line arguments with getopt
ARGS=$(getopt -a -n $0 -o hv --long help,invert -- "$@")
VALID_ARGS=$?

if [ "$VALID_ARGS" != "0" ]
then
    usage
    exit 2
fi

eval set -- "$ARGS"

while :
do
    case "$1" in
        -h|--help)
            usage
            exit 2 ;;
        -v|--invert)
            $INVERT=1
            shift 1 ;;
        --)
            shift
            break ;;
        *)
            echo "Unknown option: $1"
            usage
            exit 1;;
    esac
done

declare -a idArray
idArray=($(cat $BAIT_FILE | sed 's/^>//' | cut -f 1))

cat $FILENAME | while read LINE
do
echo $LINE
done







