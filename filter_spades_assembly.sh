#!/bin/bash

# Display help information
function display_help {
    echo "Usage: $0 [OPTIONS] genome_file.fa"
    echo "Filter genome sequences based on length and coverage values."
    echo "Options:"
    echo "  -l, --min-length LENGTH  Minimum length of sequences to keep"
    echo "  -c, --min-cov COVERAGE   Minimum coverage of sequences to keep"
    echo "  -h, --help               Display this help and exit"
    exit 0
}

# Check the number of arguments
if [[ "$#" -eq 0 ]]; then
    echo "Error: No arguments provided. Use -h or --help for usage."
    exit 1
fi

# Parse command-line arguments
while [[ "$#" -gt 0 ]]; do
    case $1 in
        -l|--min-length) min_length="$2"; shift ;;
        -c|--min-cov) min_cov="$2"; shift ;;
        -h|--help) display_help ;;
        *) genome_file="$1" ;;
    esac
    shift
done

# Check if genome file is provided
if [[ -z "$genome_file" ]]; then
    echo "Error: Genome file not specified. Use -h or --help for usage."
    exit 1
fi

# Filter based on sequence length
if [[ -n "$min_length" && -z "$min_cov" ]]; then
    awk -v min_len="$min_length" '
        /^>NODE/ {
            name = $1; gsub(">", "", name)
            getline
            if (match(name, /length_([0-9]+)_cov_([0-9.]+)/, arr)) {
                seq_len = arr[1]
                if (seq_len >= min_len) {
                    print ">" name
                    print $0
                }
            }
        }
    ' "$genome_file"
# Filter based on sequence coverage
elif [[ -z "$min_length" && -n "$min_cov" ]]; then
    awk -v min_coverage="$min_cov" '
        /^>NODE/ {
            name = $1; gsub(">", "", name)
            getline
            if (match(name, /length_([0-9]+)_cov_([0-9.]+)/, arr)) {
                seq_cov = arr[2]
                if (seq_cov >= min_coverage) {
                    print ">" name
                    print $0
                }
            }
        }
    ' "$genome_file"
# Filter based on both sequence length and coverage
elif [[ -n "$min_length" && -n "$min_cov" ]]; then
    awk -v min_len="$min_length" -v min_coverage="$min_cov" '
        /^>NODE/ {
            name = $1; gsub(">", "", name)
            getline
            if (match(name, /length_([0-9]+)_cov_([0-9.]+)/, arr)) {
                seq_len = arr[1]
                seq_cov = arr[2]
                if (seq_len >= min_len && seq_cov >= min_coverage) {
                    print ">" name
                    print $0
                }
            }
        }
    ' "$genome_file"
fi

