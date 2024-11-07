#!/usr/bin/env bash

# A script to convert a multiple sequence alignment file in FASTA format to a strict PHYLIP format
# yanpengch@qq.com
# 2023-04-23

set -o pipefail

# Help function
function usage {
    echo ""
    echo "Usage: $0 -i input.fa -o output.nex"
    echo ""
    echo "Options:"
    echo "    -i, --in    Input file in FASTA format"
    echo "    -o, --out   Output file in Nexus format"
    echo "    -h, --help  Display this help message"
    echo ""
}

# Get command line options
while [ $# -gt 0 ]
do
    key="$1"
    case $key in
        -i|--in)
        FASTA=$2
        shift # past argument
        shift # past value
        ;;
        -o|--out)
        NEXUS=$2
        shift # past argument
        shift # past value
        ;;
        -h|--help)
        usage
        exit 0
        ;;
        *)
        echo "Unknown option: $1"
        usage
        exit 1
        ;;
    esac
done

# Check for required input and output files
if [[ -z $FASTA ]] || [[ -z $NEXUS ]]
then
    echo ""
    echo "Error: Input and output files are required."
    usage
    exit 1
fi

# characters not allowed
if [[ -n $(grep "^>" $FASTA | grep -e ' ' -e ':' -e ',' -e ';' ) ]]; then
    echo "Error: special characters [ space : , ; > ]are not allowed in sequence IDs" 
    exit 1
fi
  #-e ':' -e ',' -e ';' -e '.' -e '>' ||  

# Read FASTA into shell array
declare -A SEQ_DICT
while read LINE; do
    LINE=$(echo $LINE | tr -d '\n')
    if [[ ${LINE:0:1} == '>' ]]; then
        SEQ_ID=${LINE:1} 
        SEQ_DICT[$SEQ_ID]=""
    else
        SEQ_DICT[$SEQ_ID]="${SEQ_DICT[$SEQ_ID]}$LINE" 
    fi
done < ${FASTA}

# Count number of sequences and sequence length
WIDTH_LONGEST_ID=$(grep '^>' $FASTA | sed 's/>//' | awk '{print length($1)}' | sort -nr | head -n 1)
LENGTH=${#SEQ_DICT[$SEQ_ID]}

# Write Nexus file header
echo "#NEXUS" > ${NEXUS}
echo "" >> ${NEXUS}
echo "BEGIN DATA;" >> ${NEXUS}
echo "    Dimensions NTax=${NUM_SEQ} NChar=${LENGTH};" >> ${NEXUS}
echo "    Format Dstatype=DNA Missing=? GAap=- interleave=yes;" >> ${NEXUS}
echo "    Matrix" >> ${NEXUS}

# add sequences
for KEY in "${!SEQ_DICT[@]}"; do
  SEQUENCE=${SEQ_DICT[$KEY]}
  printf "        %-${WIDTH_LONGEST_ID}s    %-s\n" $KEY $SEQUENCE >> ${NEXUS}
done


# Write Nexus file footer
echo "  ;" >> ${NEXUS}
echo "END;" >> ${NEXUS}

date "+%Y-%m-%d %H:%M:%S" | tr -d '\n'
echo "-- Conversition done!"
exit 0