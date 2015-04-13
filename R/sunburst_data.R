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

sunburst_data <- function(newick, ladderize = F, ultrametric = F,
                          xlim=360, rot=0, node_attributes=''){
  python.exec( "def appendpath(a): import sys; sys.path.append(a)" )
  python.call( "appendpath",  system.file(package="ggsunburst") )
  
  path <- system.file("ggsunburst.py", package="ggsunburst")
  python.load(path)

  out <- python.call('sunburst_data', newick, ladderize, ultrametric,
                     xlim, rot, node_attributes)
  tree_data <- list()
  tree_data[['rects']]       <- read.delim(text=out[1], header=T)
  tree_data[['leaf_labels']] <- read.delim(text=out[2], header=T)
  tree_data[['node_labels']] <- read.delim(text=out[3], header=T)

  out <- python.call('tree_data', newick, ladderize, ultrametric)
  tree_data[['segments']]       <- read.delim(text=out[1], header=T)
  
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

nw_print <- function(newick, ladderize = F, ultrametric = F){
  python.exec( "def appendpath(a): import sys; sys.path.append(a)" )
  python.call( "appendpath",  system.file(package="ggsunburst") )
  path <- paste(system.file(package="ggsunburst"), "ggsunburst.py", sep="/")
  python.load(path)
  t <- python.call('nw_print', newick, ladderize, ultrametric)
  cat(as.character(t))
}
