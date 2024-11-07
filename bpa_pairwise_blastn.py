#!/usr/bin/env Rscript

library(argparse)
library(Biostrings)
library(openxlsx)
library(pheatmap)

# command line
parser <- ArgumentParser(description = 'Perform BLAST and create similarity matrix')
parser$add_argument('fasta', type = 'character', help = 'Input FASTA file')
parser$add_argument('prefix', type = 'character', help = 'Output prefix')
args <- parser$parse_args()

# call blastn
blast_output <- paste0(args$fasta,"blastn.tsv")
system(paste('blastn -query', args$fasta, '-subject', args$fasta, '-outfmt "6 qseqid sseqid pident" -out', blast_output))

# parse blastn result
blast_results <- read.table(blast_output, header = FALSE, col.names = c("qseqid", "sseqid", "pident"))
blast_results <- blast_results[!duplicated(blast_results[, c("qseqid", "sseqid")]), ]

# sequence identity matrix
similarity_matrix <- matrix(0, nrow = length(seq_names), ncol = length(seq_names), dimnames = list(seq_names, seq_names))
for (i in 1:nrow(blast_results)) {
  qseqid <- blast_results$qseqid[i]
  sseqid <- blast_results$sseqid[i]
  pident <- blast_results$pident[i]
  similarity_matrix[qseqid, sseqid] <- pident
}

# output
xlsx_file <- paste0(args$prefix, '_similarity_matrix.xlsx')
write.xlsx(similarity_matrix, file = xlsx_file, rowNames = TRUE)

# output pdf
pdf_file <- paste0(args$prefix, '_heatmap.pdf')
pdf(pdf_file)
pheatmap(similarity_matrix, clustering_distance_rows = "euclidean", clustering_distance_cols = "euclidean")
dev.off()

# info
cat("Similarity matrix saved to", xlsx_file, "\n")
cat("Heatmap saved to", pdf_file, "\n")
