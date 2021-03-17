#!/usr/bin/env Rscript

# -------------------------------------------------------------------------- #
### R funciton for displaying the SpeciesDA.jar pairwise similarity matrix ###
# -------------------------------------------------------------------------- #

## Authors
# Core code taken from http://www.indriid.com/2014/species-delim-paper-SuppIinfo-v8.pdf
# by Graham Jones, art@gjones.name, Feb 2014

# Code modified for automatized pairwise distance matrix sorting, labelling, and line drawing
# by Simon Crameri, simon.crameri@env.ethz.ch, Aug 2018


### Install dependencies if needed ###
dependent_pkgs <- c("ape", 'getopt')
need_install_pkgs <- dependent_pkgs[ which(!dependent_pkgs %in% installed.packages()) ]

if ( length(need_install_pkgs) > 0 ) {
    for ( i in need_install_pkgs ) install.packages(i)
}

# Display package version of loaded packages
for ( i in dependent_pkgs ) {
    suppressWarnings(suppressPackageStartupMessages(do.call(library, list(i))))
}

spec <- matrix(c('help'            , 'h', 0, 'logical'  , 'print help message and exit',
                 'input'           , 'i', 1, 'character', 'speciesDA.jar output file.See http://www.indriid.com/software.html, Species Delimitation Analyzer. This program takes species trees as input, and outputs clustering solutions.',
                 'tree'            , 't', 2, 'character', 'SEMI-OPTIONAL nexus-formatted tree file from with the topology is read, which is used to order the similarity matrix accordingly File is read using the ape::read.nexus() function. This argument MUST be specified if <ownorder> is NULL.',
                 'labelfile'       , 'f', 2, 'character', 'OPTIONAL file where the labels used in <summarized.tree> [FIRST column in <labelfile>] are referenced to labels used for the similarity matrix plot [SECOND     column in <labelfile>]. Column header expected. All tips need to be included in this table. Their order is not important (will be ordered according to <summarized.tree>). If <labelfile>     is specified, uses the labels specified in the SECOND column of the <labelfile> for plotting.',
                 'ownorder'        , 'o', 2, 'integer'  , 'If NULL, ordering will be performed automatically based on the topoplogy of <summarized.tree>. If a numeric vector of length equalling the number of tips,     ordering will be performed using the manual ordering specification: the first index comes in the top left corner of the plot, etc.',
                 'ownline'         , 'O', 2, 'integer'  , 'If NULL, line drawing will be performed automatically based on the <PP.thresh> criterion. If a numeric vector of length equalling the number of lines, line drawing will be performed using the manual line specification: the first line is drawn below the the first index, etc.',
                 'pp_thresh'       , 'p', 2, 'double'   , 'Posterior probability threshold to draw a line between clades if <ownlines> = NULL. For each grid point along the diagonal in the pairwise distance matrix, it is assessed whether the posterior probability in the grid square below/to the right of that grid point is equal to or lower than PP.thresh. If yes, a line will be drawn to delineate species clades.',
                 'mar'             , 'm', 2, 'character', 'numeric vector of lenght 4 specifying the plot margins below (1), to the left (2), to the top (3) and to the right (4) of the plot. Format 1,2,3,4',
                 'label_size'      , 's', 2, 'double'   , 'numeric giving the size of labels on x and y axes.',
                 'legendlabel_size', 'S', 2, 'double'   , 'numeric giving the size of labels next to the color legend.',
                 'cols'            , 'c', 2, 'character', 'color vector of length >=2 containing valid R colors to which low and high similarity indices are mapped to.',
                 'border_col'      , 'C', 2, 'character', 'color vector of length 1 containing a valid R color specifying the border color of all plotted rectangles. If NULL, the borders will have the same color as the rectangles.',
                 'legend'          , 'l', 0, 'logical'  , 'If TRUE, the color legend will be plotted.',
                 'plot_phylo'      , 'P', 0, 'logical'  , 'If TRUE and <summarized.tree> is specified, a phylogram of <summarized.tree> will be plotted before the similarity matrix.',
                 'save_pdf'        , 'n', 0, 'logical'  , 'If TRUE, a .pdf file with the similarity matrix plot named <pdf.name> will be saved.',
                 'pdf_name'        , 'N', 2, 'character', 'File name for output file (should have extension ".pdf")'),
                byrow=TRUE, ncol=5)

opt <- getopt(spec)

if ( !is.null(opt$help) ) {
    cat(getopt(spec, usage=TRUE))
    q(status=1)
}

# Required parameter
if ( is.null(opt$input) ) {
    cat('Error message:\n    --input is required\n')
    q(status=1)
}

# set some reasonable defaults for the options that are needed,
# but were not specified.
if ( is.null(opt$tree)             ) { opt$tree <- NULL }
if ( is.null(opt$lablefile)        ) { opt$lablefile <- NULL }
if ( is.null(opt$ownorder)         ) { opt$ownorder <- NULL }
if ( is.null(opt$ownlines)         ) { opt$ownlines <- NULL }
if ( is.null(opt$pp_thresh)        ) { opt$pp_thresh <- 0.05 }

if ( is.null(opt$mar) ) {
    opt$mar <- c(0,10,10,1)
} else {
    opt$mar <- unlist(strsplit(opt$mar,','))
}

if ( is.null(opt$label_size)       ) { opt$label_size <- 1}
if ( is.null(opt$legendlabel_size) ) { opt$legendlabel_size <- 1 }

if ( is.null(opt$cols) ) {
    opt$cols <- c("blue", "orange", "white")
} else {
    opt$cols <- unlist(strsplit(opt$cols, ','))
}
if ( is.null(opt$border_col)       ) { opt$border_col <- NULL }

if ( is.null(opt$legend) ) {
    opt$legend <- TRUE
} else {
    opt$legend <- FALSE
}
if ( is.null(opt$plot_phylo) ) { opt$plot_phylo <- FALSE }
if ( is.null(opt$save_pdf)   ) { opt$save_pdf <- FALSE }
if ( is.null(opt$pdf_name)   ) { opt$pdf_name <- 'SimMatrix.pdf' }

plot.simmatrix <- function(speciesDAout,
                           summary_tree,
                           lablefile,
                           ownorder,
                           ownlines,
                           pp_thresh,
                           mar,
                           label_size,
                           legendlabel_size,
                           cols,
                           border_col,
                           legend,
                           plot_phylo,
                           save_pdf,
                           pdf_name) {

    # Check required <speciesDAout> file
    stopifnot(is.character(speciesDAout), file.exists(speciesDAout))

    # Read in the table of clusterings
    x <- read.table(speciesDAout, header = TRUE, check.names = FALSE)

    # Check spaciesDA.jar output format
    if ( !identical(names(x)[1:4], c("count", "fraction", "similarity", "nclusters")) ) {
        cat('Error message:\n    ', speciesDAout, ' file does not seem to be a valid speciesDA.jar output text file.\n')
    }

    ### Sanity-check input arguments ###
    # Validity of colors
    areColors <- function(x) {
        sapply(x, function(X) { tryCatch(is.matrix(col2rgb(X)), error = function(e) FALSE) })
    }

    # Check required arguments
    stopifnot(
        # cols must be a valid color vector of length >= 2
        length(cols) >=2,
        areColors(cols),

        # checks other specifications
        is.logical(save_pdf),
        is.logical(legend),
        is.logical(plot_phylo),
        is.numeric(mar),
        is.numeric(label_size),
        is.numeric(legendlabel_size),
        length(mar) == 4,
        label_size >= 0,
        legendlabel_size >= 0,
        mar >= 0
    )

    # Check optional arguments
    if ( is.null(summary_tree) & plot_phylo ) { message("no <summary_tree> specified, so no phylogram will be plotted.") }
    if ( !is.null(lablefile) ) { stopifnot(is.character(lablefile), file.exists(lablefile)) }
    if ( save_pdf ) { stopifnot(is.character(pdf_name), substring(pdf_name, nchar(pdf_name)-3, nchar(pdf_name)) == ".pdf") }

    if ( is.null(ownlines) ) {
        stopifnot(is.numeric(pp_thresh), pp_thresh >= 0, pp_thresh <=1)
    } else {
        if (!is.null(pp_thresh)) message("no automatic line drawing since <ownlines> is not NULL, so <pp_thresh> specification is not used.")
    }

    if (!is.null(summary_tree)) {
        # Check file
        stopifnot(is.character(summary_tree), file.exists(summary_tree))

        # Read summary_tree
        sumtree <- read.nexus(summary_tree)
        if ( plot_phylo ) { plot.phylo(sumtree) }

        # Get tip label order as in the tree topology
        is_tip <- sumtree$edge[,2] <= length(sumtree$tip.label)
        ordered_tips <- sumtree$edge[is_tip, 2]
        labs <- sumtree$tip.label[ordered_tips]
        stopifnot(labs %in% names(x)[-c(1:4)])
    } else {
        labs <- names(x)[-c(1:4)]
    }

    # Check plot margins
    if ( mar[4] < 2.5 & legend ) { warning("Right plot margin might be too small for the legend to be displayed. Consider increasing mar[4].") }

    # Check ownorder and ownlines specifications
    nInd <- length(labs)
    if ( !is.null(ownorder) ) { stopifnot(is.numeric(ownorder), min(ownorder) >= 1, max(ownorder) <= nInd, length(ownorder) == nInd, !any(duplicated(ownorder))) }
    if ( !is.null(ownlines) ) { stopifnot(is.numeric(ownlines), min(ownlines) >= 0, max(ownlines) <= nInd, !any(duplicated(ownlines))) }

    # Check <speciesDAout> minimal cluster columns
    if (any( !labs %in% names(x)) ) { stop("Column names in <speciesDAout> do not match tip labels in <summary_tree>.") }

    # Check lablefile
    if ( !is.null(lablefile) ) {
        labels <- read.table(lablefile, header = TRUE, row.names = 1)
        if (any(labs %in% rownames(labels)) == FALSE) {
            labelcheck <- labs[which(! labs %in% rownames(labels))]
            check <- labelcheck[1]
            for (i in 2:length(labelcheck)) {
                ls <- labelcheck[i]
                check <- paste(check, ls, sep = ", ")
                }
        stop(paste0("The following tips were not found in the first <lablefile> column:\n", check, "\nPlease check <lablefile> ", lablefile, "."))
        }
    }

    ### Done Reading and Checking Input
    # Reorder <speciesDAout> minimal cluster columns
    if ( is.null(ownorder) ) {
        # Reorder x columns such that columns match <summary_tree> topology
        x <- x[,c(names(x)[1:4], labs)]
    } else {
        # Reorder x columns according to <ownorder>
        x <- x[,c(names(x)[1:4], names(x)[-c(1:4)][ownorder])]
    }

    # Abbreviations for display
    ids <- names(x)[-c(1:4)]
    renames <- matrix(rep(ids, each = 2), nrow = length(ids), ncol = 2, byrow = TRUE)

    # Use user-specified labels
    if ( !is.null(lablefile) ) {
        labels <- cbind(labels, rep(NA, nrow(labels)))
        labels <- labels[renames[,1], ]
        renames[,2] <- as.character(labels[, 1])
    }

    # Make the similarity matrix
    displaynames <- renames[,2]
    nmincls <- length(displaynames) # similarity matrix labels
    sim <- matrix(0, ncol=nmincls, nrow=nmincls, dimnames=list(displaynames, displaynames))
    for (i in 1:nmincls) {
        for (j in 1:nmincls) {
            coli <- x[,ids[i]]
            colj <- x[,ids[j]]
            w <- coli == colj
            sim[i,j] <- sum(x[w,"fraction"])
        }
    }

    # Ensure rounding errors don't make probabilities sum to more than 1.
    sim <- pmin(sim,1)

    # Plot lines
    if ( is.null(ownlines) ) {
        # Plot lines according to pp_threshold
        draw <- numeric()
        for (i in 1:(nrow(sim))-1) {
            ls <- ifelse(sim[i,i+1] <= pp_thresh, 1, 0)
            draw <- c(draw, ls)
            rm(ls)
        }
        dividers <- c(0, which(draw == 1), nrow(sim))
    } else {
    # Plot lines according to <ownlines>
        dividers <- c(0, ownlines, nrow(sim))
        if ( any(duplicated(dividers)) ) { dividers <- dividers[-which(duplicated(dividers))] }
    }

    # Currently recognised groups
    plot.rectangle <- function(v1,v2,...) {
        polygon(c(v1[1],v2[1],v2[1],v1[1]), c(v1[2],v1[2],v2[2],v2[2]), ...)
    }

    # Map values [0,1] in sim to user-specified color palette
    map2color<-function(x, palette, limits = NULL) {
        if( is.null(limits) ) { limits = range(x) }
        palette[findInterval(x, seq(limits[1], limits[2], length.out = length(palette) + 1), all.inside = TRUE)]
    }

    # Main plotting routine
    plot.simmatrix <- function() {
        # Set plot margins
        par(mar= mar)

        ## Plot pairwise similarity matrix ##
        # Create empty plot
        if ( legend ) {
            add <- 1 # leave some space for the legend
            plot(NULL, xlim=c(0,nmincls+add), ylim=c(nmincls,0), axes=FALSE, ylab="", xlab="")
        } else {
            plot(NULL, xlim=c(0,nmincls-1), ylim=c(nmincls,0), axes=FALSE, ylab="", xlab="")
        }

        # Plot labels
        axis(side=3, at=(1:nmincls)-.5, labels=displaynames, tick=FALSE, las=2, line=-1, cex.axis = label_size) # column labels
        axis(side=2, at=(1:nmincls)-.5, labels=displaynames, tick=FALSE, las=2, line=-1, cex.axis = label_size) # row labels

        # Plot rectangles
        for (i in 1:nmincls) { # for all tip columns
            for (j in 1:nmincls) { # for all tip rows
                d <- 1 - sim[i,j] # similarity value mapped to color
                n <- 100 # number of color intervals: the higher n, the higher the resolution, the longer it takes for plotting
                col <- map2color(x = d, pal = colorRampPalette(cols, space = "rgb") (n), limits = c(0,1))
                colorlegend <- map2color(x = seq(1, 0, length.out = n), pal = colorRampPalette(cols, space = "rgb") (n), limits = c(0,1))
                if (is.null(border_col)) bordercol <- col else bordercol <- border_col
              plot.rectangle(c(i-1,j-1), c(i,j), col = col, border = bordercol)
            }
        }

        # Plot lines around clusters
        for (b in dividers) {
            lines(x=c(-.5,nmincls), y=c(b,b))
            lines(x=c(b,b), y=c(-.5,nmincls))
        }

        ## Plot color legend ##
        if ( legend ) {
            levels <- seq(0, nmincls, length.out = n)
            rect(nmincls+.5, levels[-length(levels)], nmincls+.5+add, levels[-1L], col = colorlegend, border = NA, xpd = TRUE)
            axis(4, at = seq(0, nmincls, length.out = 11), labels = seq(0, 1, length.out = 11), las = 1, pos = c(nmincls+1.5,0), cex.axis = legendlabel_size)
            lines(x=c(nmincls+.5,nmincls+.5), y=c(0,nmincls))
            lines(x=c(nmincls+.5,nmincls+1.5), y=c(nmincls,nmincls), xpd = TRUE)
            lines(x=c(nmincls+.5,nmincls+1.5), y=c(0,0), xpd = TRUE)
        }

        # Reset default plotting parameters
        par(mar= c(5, 4, 4, 2) + 0.1)
        par(mfrow=c(1,1))
    }

    # Plot similarity matrix on plot device
    plot.simmatrix()

    # Safe similarity matrix to PDF
    if ( save_pdf ) {
        pdf(file = pdf_name)
        plot.simmatrix()
        dev.off()
    }

    # Return similarity matrix
    return(sim)
}

# main
plot.simmatrix(opt$input, opt$tree, opt$lablefile, opt$ownorder, opt$ownlines, opt$pp_thresh, opt$mar, opt$label_size, opt$legendlabel_size, opt$cols, opt$border_col, opt$legend, opt$plot_phylo, opt$save_pdf, opt$pdf_name)