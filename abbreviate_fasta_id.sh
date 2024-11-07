#!/usr/bin/env bash

# A script to convert long sequence identifiers in a multiple sequence alignment file to a short sequence identifiers
# yanpengch@qq.com
# 2023-04-24

# Help function
function usage {
    echo ""
    echo "Usage: $0 -i input.fa -o output.abbreviated.fa"
    echo ""
    echo "Options:"
    echo "    -i, --in    Input file with long sequence identifiers"
    echo "    -o, --out   Output file with short sequence identifiers"
    echo "    -h, --help  Display this help message"
    echo ""
}

# Get command line options
while [[ $# -gt 0 ]]
do
key="$1"
case $key in
    -i|--in)
    INFILE="$2"
    shift # past argument
    shift # past value
    ;;
    -o|--out)
    OUTFILE="$2"
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
if [ -z "$INFILE" ] || [ -z "$OUTFILE" ]
then
    echo ""
    echo "Error: Input and output files are required."
    usage
    exit 1
fi

# Check if file is in Fasta format
if grep -q "^>" $INFILE; then
    format="Fasta"
else
    echo "Error: Input file must be in FASTA format."
    echo ""
    exit 1
fi

# Check if sequence IDs are longer than 10 characters
LENGTH_LONGEST_ID=$(grep '^>' ${INFILE} | sed 's/>//' | awk '{print length($0)}' | sort -nr | head -n 1)
if [[ $LENGTH_LONGEST_ID -lt 10 ]]
then
    echo ""
    echo "Error: sequence IDs are shorter than 10 characters and no need abbreviation"
    echo ""
    exit 1
fi

# Count number of sequences and sequence length
NUM_SEQ=$(grep '^>' -c ${INFILE})
paste <(grep '^>' ${INFILE} | sed 's/^>//') <(for i in $(seq $NUM_SEQ);do echo t${i};done) > ${OUTFILE}_idmap.list
paste <(grep '^>' ${INFILE} | sed 's/^>//') <(for i in $(seq $NUM_SEQ);do echo t${i};done) | awk 'NR==FNR {a[$1]=$2;next} {for (i in a) {sub(i,a[i])};print}' - ${INFILE} > ${OUTFILE}

date "+%Y-%m-%d %H:%M:%S" | tr -d '\n'
echo "-- Abbreviation done!"
exit 0