#!/usr/bin/env python

# yanpengch@qq.com
# 2024-10-16

import sys
import os

def parse_file(file_path):
    """Parse the scaffold stats file and extract relevant data."""
    with open(file_path, 'r') as f:
        # Skip the header
        f.readline()
        # Read the data from the second line
        data = f.readline().strip().split()
    return data

if __name__ == "__main__":
    # Print header for the final output
    print("SampleID\tplaced_sequences\tplaced_bp\tunplaced_sequences\tunplaced_bp\tgap_bp\tgap_sequences")

    # Process each file path from standard input
    for file_path in sys.stdin:
        file_path = file_path.strip()  # Remove any surrounding whitespace

        # Extract the sample ID from the file path
        sample_id = file_path.split('/')[1]

        # Parse the file to extract statistics
        stats = parse_file(file_path)

        # Print the sample ID along with the parsed statistics
        print(f"{sample_id}\t" + "\t".join(stats))

