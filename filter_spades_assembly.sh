#!/bin/bash

# Display help information
function display_help {
    echo "Usage: $0 [OPTIONS] genome_file.fa"
    echo "Filter genome sequences based on length and coverage values."
    echo "Options:"
    echo "  -l, --length LENGTH  Minimum length of sequences to keep"
    echo "  -c, --cov COVERAGE   Minimum coverage of sequences to keep"
    echo "  -h, --help           Display this help and exit"
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
        -l|--length) length="$2"; shift ;;
        -c|--cov) cov="$2"; shift ;;
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

# Filter based on length
if [[ -n "$length" && -z "$cov" ]]; then
    awk -v length="$length" '
        /^>NODE/ {
            name = $1; gsub(">", "", name)
            getline
            if (match(name, /length_([0-9]+)_cov_([0-9.]+)/, arr)) {
                len = arr[1]
                if (len >= length) {
                    print ">" name
                    print $0
                }
            }
        }
    ' "$genome_file"
# Filter based on coverage
elif [[ -z "$length" && -n "$cov" ]]; then
    awk -v cov="$cov" '
        /^>NODE/ {
            name = $1; gsub(">", "", name)
            getline
            if (match(name, /length_([0-9]+)_cov_([0-9.]+)/, arr)) {
                coverage = arr[2]
                if (coverage >= cov) {
                    print ">" name
                    print $0
                }
            }
        }
    ' "$genome_file"
# Filter based on both length and coverage
elif [[ -n "$length" && -n "$cov" ]]; then
    awk -v length="$length" -v cov="$cov" '
        /^>NODE/ {
            name = $1; gsub(">", "", name)
            getline
            if (match(name, /length_([0-9]+)_cov_([0-9.]+)/, arr)) {
                len = arr[1]
                coverage = arr[2]
                if (len >= length && coverage >= cov) {
                    print ">" name
                    print $0
                }
            }
        }
    ' "$genome_file"
fi
