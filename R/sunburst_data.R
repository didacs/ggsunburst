#' Extracts data from the newick format in a list of data frames.
#'
#' This functions extracts relevant information from
#' a tree structure to be plotted as an adjacency diagram (sunburst and icicle)
#'
#'
#' @param newick either a string or a file, in newick format (see https://pythonhosted.org/ete2/tutorial/tutorial_trees.html#reading-and-writing-newick-trees)
#' @param ladderize if not FALSE, sort the partitions of a given tree according to their size. 'left' to invert order
#' @param ultrametric converts a tree to ultrametric topology (all leaves must have the same distance to root)
#'
#' @export
#' @return a list of data frames
#' @seealso \code{\link{sunburst}}
#' @seealso \code{\link{icicle}}

sunburst_load_data <- function(input, type="newick", sep=NULL, ladderize = F,
                          ultrametric = F, xlim=360, rot=0, node_attributes=''){
  py_run_string("def appendpath(a): import sys; sys.path.append(a)")
  py$appendpath(system.file(package="ggsunburst"))

  # python.exec( "def appendpath(a): import sys; sys.path.append(a)" )
  # python.call( "appendpath",  system.file(package="ggsunburst") )

  path <- system.file("ggsunburst.py", package="ggsunburst")
  source_python(path)
  # python.load(path)

  out <- sunburst_data(input, type, sep,
                       ladderize, ultrametric, xlim, rot, node_attributes)
  # out <- python.call('sunburst_data', input, type, sep,
                     # ladderize, ultrametric, xlim, rot, node_attributes)
  tree_data <- list()
  tree_data[['rects']]       <- read.delim(text=out[1], header=T)
  tree_data[['leaf_labels']] <- read.delim(text=out[2], header=T)
  tree_data[['node_labels']] <- read.delim(text=out[3], header=T)
  tree_data[['segments']]    <- read.delim(text=out[4], header=T)
  tree_data[['node_attributes']]<- strsplit(out[5], ",")[[1]]

  #out <- python.call('tree_data', input, ladderize, ultrametric)

  tree_data
}


#' Prints the tree structure encoded in the newick input
#'
#' Prints the tree structure encoded in the newick input
#'
#'
#' @param newick either a string or a file, in newick format (see https://pythonhosted.org/ete2/tutorial/tutorial_trees.html#reading-and-writing-newick-trees)
#' @param ladderize if not FALSE, sort the partitions of a given tree according to their size. 'left' to invert order
#' @param ultrametric converts a tree to ultrametric topology (all leaves must have the same distance to root)
#'
#' @export
#' @return NULL

nw_print <- function(newick, format = 8, ladderize = F, ultrametric = F){
  python.exec( "def appendpath(a): import sys; sys.path.append(a)" )
  python.call( "appendpath",  system.file(package="ggsunburst") )
  path <- paste(system.file(package="ggsunburst"), "ggsunburst.py", sep="/")
  python.load(path)
  t <- python.call('nw_print', newick, format, ladderize, ultrametric)
  cat(as.character(t))
}
