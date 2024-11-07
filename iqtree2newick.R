#!/usr/bin/env Rscript

# Load necessary libraries
suppressPackageStartupMessages({
  library(getopt)
  library(treeio)
})

# Define option specifications
spec <- matrix(c(
  'verbose', 'v', 2, "integer", "give verbose output",
  'help',    'h', 0, "logical", "print help message and exit",
  'iqtree',  'i', 1, "character", "iqtree output file: *.treefile",
  'newick',  'n', 1, "character", "output tree file in newick format"
), byrow = TRUE, ncol = 5)

# Get options from the command line
opt <- getopt(spec)

# Print help message and exit if requested
if (!is.null(opt$help)) {
  cat(getopt(spec, usage = TRUE))
  q(status = 1)
}

# Check for required arguments and set defaults
if (is.null(opt$iqtree)) {
  cat('Error: No input tree file provided!\n')
  q(status = 1)
}
if (is.null(opt$newick)) {
  cat('Error: No output filename provided!\n')
  q(status = 1)
}
if (is.null(opt$verbose)) {
  opt$verbose <- 0  # Set verbose level to 0 by default
}

# Verbose output function
vcat <- function(...) {
  if (opt$verbose > 0) cat(...)
}

# Read the input IQ-TREE file
vcat('Reading IQ-TREE file...\n')
tre <- read.iqtree(opt$iqtree)

# Write the output tree in Newick format
vcat('Writing tree to Newick format...\n')
write.tree(as.phylo(tre), file = opt$newick)

# Success message (optional) and exit
vcat('Tree successfully written to', opt$newick, '\n')
q(status = 0)

