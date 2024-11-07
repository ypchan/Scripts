#!/usr/bin/env bash

# A script to convert a multiple sequence alignment file in FASTA format to a strict PHYLIP format
# yanpengch@qq.com
# 2023-04-23

# Help function
function usage {
    echo ""
    echo "Usage: $0 -i input.fa -o output.phy"
    echo ""
    echo "Options:"
    echo "    -i, --in    Input file in FASTA format"
    echo "    -o, --out   Output file in PHYLIP format"
    echo "    -h, --help  Display this help message"
    echo ""
}

# Get command line options
while [[ $# -gt 0 ]]
do
key="$1"
case $key in
    -i|--in)
    FASTA="$2"
    shift # past argument
    shift # past value
    ;;
    -o|--out)
    PHYLIP="$2"
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
if [ -z "$FASTA" ] || [ -z "$PHYLIP" ]
then
    echo ""
    echo "Error: Input and output files are required."
    usage
    exit 1
fi

# Check if sequence IDs are longer than 10 characters
LENGTH_LONGEST_ID=$(grep '^>' ${FASTA} | sed 's/>//' | awk '{print length($0)}' | sort -nr | head -n 1)
if [[ $LENGTH_LONGEST_ID -gt 10 ]]
then
    echo ""
    echo "Error: Some sequence IDs are longer than 10 characters and will be truncated."
    echo "       simple_fasta_id input.fa > output.abbrevoated_id.fa"
    echo ""
    exit 1
fi

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
NUM_SEQ=$(grep '^>' -c ${FASTA})
LENGTH=${#SEQ_DICT[$SEQ_ID]}

# Convert input file to one-line FASTA format
echo "    ${NUM_SEQ}    ${LENGTH}" > ${PHYLIP}

for KEY in "${!SEQ_DICT[@]}"; do
    printf "%-10s" $KEY >> ${PHYLIP}
    echo ${SEQ_DICT[$KEY]} >> ${PHYLIP}
done

echo "Conversion done!"
exit 0