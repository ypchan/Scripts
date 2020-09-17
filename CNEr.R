#!/psd/biosoft/anaconda/envs/CNEr/bin/Rscript

# library, stop generating warnings and errors using function: suppressMessages()
suppressMessages(library("CNEr"))
suppressMessages(library("GenomicRanges"))
suppressMessages(library("getopt"))

spec <- matrix(c(
                 "help"      , "h", 0, "logical"  , "print help messages",
                 "aSbQ"      , "a", 1, "character", "input file axt alignment file:AB.net.axt, A is the subject genome and B is the query genome. Required",
                 "bSaQ"      , "b", 1, "character", "input file axt alignment file:BA.net.axt, B is the subject genome and A is the query genome. Required, required",
                 "Afilter"   , "A", 1, "character", "filter file of A genome in bed format with six columns:chromName, exon_start, exon_end, '.', '0', 'strand', without head. required",
                 "Bfilter"   , "B", 1, "character", "filter file of B genome in bed format with six columns:chromName, exon_start, exon_end, '.', '0', 'strand', without head. required",
                 "A2bit"     , "L", 1, "character", "2bit file of A genome",
                 "B2bit"     , "l", 1, "character", "2bit file of B genome",
                 "windowSize", "w", 2, "integer"  , "specify the windowSize number. By default:50",
                 "identity"  , "i", 2, "integer"  , "the minimal identity score over the scanning window. By default:50",
                 "output"    , "o", 2, "character", "set the output file name"),
               byrow = TRUE, ncol = 5)

usage <- function(x) {
        cat("*******************************************************************************************\n")
        cat("A Script Identifing Conserved Noncoding Elements(CNEs).\n")
        cat("\nAuthor: chenyanpeng@dnastories.com\n")
        cat("Date: 2019-12-09\n")
        cat("Required Packages: CNEr, GenomicRanges\n")
        cat("*******************************************************************************************\n")
        cat(getopt(x, usage = TRUE))
        q(status = 1)
}
opt = getopt(spec)

# check option: help
if ( !is.null(opt$help) ) {
  usage(spec)
}

# check required input
checkInput <- c(is.null(opt$aSbQ), is.null(opt$bSaQ), is.null(opt$Afilter), is.null(opt$Bfilter), is.null(opt$A2bit), is.null(opt$B2bit))
if ( any(checkInput) ) {
        usage(spec)
}

# set input and default parameters
## input axt format file
AB.net.axt.file <- opt$aSbQ
BA.net.axt.file <- opt$bSaQ
## input 2bit files
A2bit.file <- opt$A2bit
B2bit.file <- opt$B2bit

Aspecies <- strsplit(basename(A2bit.file), fixed = TRUE, split = ".")[[1]][1]
Bspecies <- strsplit(basename(B2bit.file), fixed = TRUE, split = ".")[[1]][1]
## input filter file in bed format
Afilter.file <- opt$Afilter
Bfilter.file <- opt$Bfilter
## set default value for the parameter windowsize
if ( is.null(opt$windowSize) ) {
  opt$windowSize <- 50
}
windowSize <- as.integer(opt$windowSize)
## set default value for the parameter identity
if ( is.null(opt$identity) ) {
  opt$identity <- 50
}
identityValue <- as.integer(opt$identity)
cneThresholds <- paste(identityValue, windowSize, sep = "_")
## set default path for output

if ( is.null(opt$outdir) ) {
  opt$output <- paste(Aspecies, Bspecies, cneThresholds, "tsv", sep = ".")
}
output <- opt$output

# read filter bed file
Afilter <- readBed(opt$Afilter)
Bfilter <- readBed(opt$Bfilter)

# creat a CNE class
cne <- CNE(
  assembly1Fn=A2bit.file,
  assembly2Fn=B2bit.file,
  axt12Fn=AB.net.axt.file,
  axt21Fn=BA.net.axt.file,
  window=windowSize,
  identity=identityValue,
  CNE12=GRangePairs(),
  CNE21=GRangePairs(),
  CNEMerged=GRangePairs(),
  CNEFinal=GRangePairs(),
  aligner="blat",
  cutoffs1=4L,
  cutoffs2=4L)

# CNE identification
cneListAB <- ceScan(x=cne,
              tFilter=Afilter,
              qFilter=Bfilter,
              window=windowSize,
              identity=identityValue)

# mergerd CNE
cneMergedListAB <- lapply(cneListAB, cneMerge)

# realignment CNEs
cneFinalListAB <- lapply(cneMergedListAB, blatCNE)

# replace "first" "second" with species names
cneFinalListAB <- cneFinalListAB[[cneThresholds]]@CNEFinal
cneFinalListAB <- as.data.frame(cneFinalListAB)
colnames(cneFinalListAB) <- lapply(colnames(cneFinalListAB), function(x){gsub("first", Aspecies, x)})
colnames(cneFinalListAB) <- lapply(colnames(cneFinalListAB), function(x){gsub("second", Bspecies, x)})

# write into txt.table
write.table(cneFinalListAB, file = output, sep = '\t', quote = FALSE, row.names = FALSE)
q(status=0)
