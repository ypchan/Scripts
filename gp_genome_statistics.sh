#!/bin/bash

# Usage function to display help
usage() {
    echo "Usage: $0 [-j num_threads] <file_list.txt> or provide input through standard input"
    echo
    echo "Options:"
    echo "  -j num_threads  Number of parallel threads to use (default: 1)"
    echo "  -h              Display this help message"
    echo
    echo "Examples:"
    echo "  echo genome.name | gp_genome_statistics.sh        # one genome"
    echo "  gp_genome_statistics.sh file_list.txt             # multiple genomes"
    echo "  gp_genome_statistics.sh -j 4 file_list.txt        # multiple genomes and multiple threads"
    echo "  cat file_list.txt | gp_genome_statistics.sh       # stdin"
    echo "  cat file_list.txt | gp_genome_statistics.sh -j 4  # stdin"
    exit 1
}

# Default number of threads
num_threads=1

# Parse optional arguments
while getopts ":j:h" opt; do
    case ${opt} in
        j )
            num_threads=$OPTARG
            ;;
        h )
            usage
            ;;
        \? )
            usage
            ;;
    esac
done
shift $((OPTIND -1))

# Check if the input file list is provided, or read from standard input
if [ -z "$1" ]; then
    if [ -t 0 ]; then
        usage
    else
        file_list="/dev/stdin"
    fi
else
    file_list=$1

    # Check if the file list exists
    if [ ! -f "$file_list" ]; then
        echo "File list not found!"
        exit 1
    fi
fi

# Function to process each genome file
process_file() {
    local genome_file=$1

    # Check if the genome file exists
    if [ ! -f "$genome_file" ]; then
        echo "File not found: $genome_file"
        return
    fi

    # Read the entire file into memory once
    content=$(cat "$genome_file")

    # Count the number of contigs
    contig_count=$(echo "$content" | grep -c "^>")

    # Calculate the genome size
    genome_size=$(echo "$content" | grep -v "^>" | tr -d '\n' | wc -c)

    # Output the result
    echo -e "${genome_file}\t${contig_count}\t${genome_size}"
}

export -f process_file

# Use parallel to process files in parallel with the specified number of jobs
cat "$file_list" | parallel -j "$num_threads" process_file
