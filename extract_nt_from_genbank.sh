#!/bin/bash

# date: 2024-07-04
# bugs: yanpengch@qq.com

# Check if a filename argument is provided
if [ $# -eq 0 ]; then
    echo "Usage: $0 filename"
    exit 1
fi

# Get the filename argument
filename=$1

# Check if the file exists
if [ ! -f "$filename" ]; then
    echo "File not found!"
    exit 1
fi

head_line=$(basename $filename)
echo ">${head_line%.gbk}"

# Use grep and sed to process the file
grep -E '^[ ]+[0-9]+ [atgc]' "$filename" | sed 's/ //g;s/[0-9]//g'

