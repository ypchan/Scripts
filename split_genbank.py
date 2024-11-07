#!/usr/bin/env python3

# yanpengch@qq.com
# 2024-10-16

import os
import argparse
from Bio import SeqIO
from tqdm import tqdm


if __name__ == "__main__":
    # Parse command-line arguments using argparse
    parser = argparse.ArgumentParser(description="Split a multi-record GenBank file into individual files.")
    parser.add_argument("input_file", metavar="input.gb", help="Path to the input multi-record GenBank file.")
    parser.add_argument("output_dir", metavar="outdirectory",  help="Directory to save the individual GenBank files.")
    args = parser.parse_args()

    # Check if the output directory exists, create it if not
    if not os.path.exists(args.output_dir):
        os.makedirs(args.output_dir)

    # Calculate the total number of records in the GenBank file for the progress bar
    with open(args.input_file, "r") as handle:
        total_records = sum(1 for _ in SeqIO.parse(handle, "genbank"))

    # Read the multi-record GenBank file and split it into individual files
    with open(args.input_file, "r") as handle:
        for record in tqdm(SeqIO.parse(handle, "genbank"), total=total_records, desc="Processing GenBank records"):
            # Use the record ID as the filename prefix
            output_filename = os.path.join(args.output_dir, f"{record.id}.gbk")
            with open(output_filename, "w") as output_handle:
                SeqIO.write(record, output_handle, "genbank")
            print(f"Saved {record.id} to {output_filename}")

