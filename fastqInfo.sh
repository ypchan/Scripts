#!/usr/bin/env bash

<<COMMENT
Author: Y.P. CHEN
E-mail: 764022822@qq.com
Date  : 2020-09-07
COMMENT

# print information, synopsis, options and usage of this shell script.
function usage {
cat << EOF
fastqInfo -- A shell script to calculates the average depth of sequencing coverage(X)

SYNOPSIS:
    fastqInfo -f fq_R1(.gz) -r fq_R2(.gz)
              [-g|--genome genome.fa(.gz)]

OPTION:
    -h|--help                       print help message and exit
    -f|--forward fastq_R1           forward fastq(.gz) file, required
    -r|--reverse fastq_R2           reverse fastq(.gz) file, required
    -g|--genome  genome.fa(.gz)     genome file in FASTA format, .gz allowed

Bugs:
    Any bugs in fastqInfo should be reported to chenyanpeng1992@outlook.com
EOF
}

# parse long command-line arguments with getopt
ARGS=$(getopt -a -n fastqInfo.sh -o hf:r:g:l: --long help,forward:,reverse:,genome:,length_read: -- "$@")
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
        -f|--forward)
            FQ1=$2
            shift 2 ;;
        -r|--reverse)
            FQ2=$2
            shift 2 ;;
        -g|--genome)
            GENOME=$2
            shift 2 ;;
        -l|--read_length)
            READ_LEN=$2
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


#check for mandatory parameters: --forward, --reverse
if [[ ! $FQ1 || ! $FQ2 ]]
then
    echo "[ERROR] --forward and --reverse is required argument"
    exit 2
fi

# calculate read counts
function read_count {
    # number of read in fq1
    SUFFIX1=${FQ1: -3}
    if [[ SUFFX1 == ".gz" ]]
    then
        NUM_FQ1=$(zcat $FQ1| echo $((`wc -l`/4)))
    else
        NUM_FQ1=$(cat $FQ1| echo $((`wc -l`/4)))
    fi

    # number of read in fq2
    SUFFIX2=${FQ2: -3}
    if [[ SUFFX2 == ".gz" ]]
    then
        NUM_FQ2=$(zcat $FQ1 | echo "$(wc -l) / 4" | bc)
    else
        NUM_FQ2=$(cat $FQ2 | echo "$(wc -l) / 4" | bc)
    fi

    echo "Num_read in ${FQ1##*/}: ${} "
    echo "Num_read in ${FQ1##*/}: ${} "

}

function depth_of_sequencing_coverage {
  # calucate teh depth of sequencing coverage LN/G
  ## LN = number_read * length_read
  ## depth = number_bases / number_bases_of_genome
  length_all_reads=$(echo "($NUM_FQ1 + $NUM_FQ2) * $READ_LEN "| bc)
  length_genome=$(grep -V '>' | awk '{print length}' | awk '{num += $1} END {print sum}')
  depth=$(($length_all_reads / $length_genome))
  echo "Depth:" $depth
}

if [[ $# == 0 ]]
then
    usage
fi

read_count
depth_of_sequencing_coverage