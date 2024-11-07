#!/usr/bin/env Rscript

description <- '
gmyc.R -- a R script to conduct species delimination using GMYC methods

Author:chenyanpeng1992@outlook.com
Date  :2021-02-22
Dependency:
    ape, paran, rncl, splits, getopt
'
# Check packages
dependency_pkg <- c('ape', 'paran', 'rncl', 'splits', 'getopt')
for (pkg in dependency_pkg) {
        if ( !require(pkg, quietly = TRUE, character.only = TRUE) ) {
                quit(save = "no", status = 1, runLast = TRUE)
        }
}

# Parse command-line arguments
spec <- matrix(
    c('tree',   't', 1, 'character', 'beast_tree.nex, required',
      'method', 'm', 2, 'character', '[single|multiple] method of analysis, either "single" for single-threshold version or "multiple" for multiple-threshold version',
          'output', 'o', 1, 'character', 'output filename, required',
      'help',   'h', 0, 'logical',   'help message'),
        byrow=TRUE, ncol=5)

opt <- getopt(spec=spec)

if ( !is.null(opt$help) ) {
        cat(description, '\n')
    cat(paste(getopt(spec=spec, usage = T), '\n'))
    quit(status = 1)
}

if ( is.null(opt$tree) || is.null(opt$output) ) {
    cat('Error messsage:\n    --tree and --output arguments are required\n')
    cat(paste(getopt(spec=spec, usage = T), '\n'))
    quit(status = 1)
}

if ( is.null(opt$method) ) {
    opt$method <- 'single'
}

nexusTree <- read_nexus_phylo(opt$tree)
gmyc <- gmyc(nexusTree, method = opt$method, quiet = TRUE)

species_df <- spec.list(gmyc)
for (rowindex in seq_along(species_df[,1])) {
    species_df[rowindex,1] <- paste('species',species_df[rowindex,1], sep = '_')
}

# Rearrange column position
species_df <- species_df[, c(2,1)]
write.table(species_df, file = opt$output, quote = FALSE, sep = '\t', row.names = FALSE)
quit(status = 0)
