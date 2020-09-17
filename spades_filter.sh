#!/usr/bin/env bash

<<COMMENT
Author:chenyanpeng
Date  :2020-09-16
Update: None
COMMENT

function usage {
cat << EOF
$0 -- A shell script to calculates the average depth of sequencing coverage(X)

SYNOPSIS:
    spades_filter.sh  -i <fasta_file> [-l <int>] [-d <int>]

OPTION:
    -h|--help                  print help message and exit           
    -i|--input  <fasta-file>   input file in FASTA format 
    -l|--length <int>          minimal length of contigs
    -d|--depth  <int>          minimal depth of contigs

Bugs:
    Any bugs in fastqInfo should be reported to chenyanpeng1992@outlook.com
EOF
}

# parse long command-line arguments with getopt
ARGS=$(getopt -a -n spades.filter.sh -o hi:l:d: --long help,input:,length:,depth: -- "$@")
VALID_ARGS=$?

if [ "$VALID_ARGS" != "0" ]
then
    usage
    exit 2
fi

eval set -- "$ARGS"

while :
do
	case $1 in
		-h | --help)
            usage
            exit 1 ;;
        -i | --input)
            FASTA=$2
            shift 2 ;;
        -l | --length)
            LENGTH=$2
            shift 2 ;;
        -d | --depth)
            DEPTH=$2
            shift 2 ;;
        --)
            shift
            break ;;
        *)
            echo "Unknown option: $1"
            usage
            exit 1;;
    esac
done

if [[ $# == 0 ]]
then
	usage
	exit 1
fi

function filter_by_length {
	grep '>' $FASTA | awk -F 

}


function filter_by_depth {

}

function filter_by_length_depth {

}
