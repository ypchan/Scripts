#!/usr/bin/env Rscript

cat("ftk_get_netgpi -- detect signature of GPI-anchored proteins\n")
cat("\n")
cat("AUTHOR: yanpengch@qq.com\n")
cat("DATE  : 2022-10-22\n")

cat("Load required packages...\n")
if ( !require('ragp') ) {
    remotes::install_git("https://github.com/missuse/ragp",
                     build_vignettes = FALSE)
    library('ragp')
}

# read.fasta will read protein fasta and return a seqfastaAA object
if ( !require('seqinr') ) {
    install.packages('seqinr')
    library('seqinr')
}

# use getopt to parse command-line agrumnets
if ( !require('getopt') ) {
    install.packages('getopt')
    library('getopt')
}

# get options, using the spec as defined by the enclosed list.
# we read the options from the default: commandArgs(TRUE).
spec = matrix(c(
  'verbose', 'v', 2, "integer"  , '',
  'help'   , 'h', 0, "logical"  , 'show help message and exit',
  'input'  , 'i', 1, "caharcter", 'input filename',
  'output' , 'o', 1, "character", 'output filename'
), byrow=TRUE, ncol=5)
opt = getopt(spec)

# if help was asked for print a friendly message 
# and exit with a non-zero error code
if ( !is.null(opt$help) || is.null(opt$input) || is.null(opt$output)) {
  cat(getopt(spec, usage=TRUE), '\n')
  q(status=1)
}

# read a FASTA file to a list of SeqFastaAA objects
At_seq_fas = seqinr::read.fasta(opt$input, seqtype = 'AA', as.string = TRUE)
in_prot = scan_ag(data = At_seq_fas)

res <- get_netGPI(in_prot, sequence='sequence', id ='id')

df <- data.frame(res)
output <-  file(opt$output, open = "w")
write.table(x=df, file = output, quote = FALSE, sep = "\t")
close(output)

# signal success and exit.
q(status=0)