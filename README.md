# ggsunburst

ggsunburst offers a set of tools to plot adjacency diagrams using `ggplot2`.

Adjacency diagrams are space-filling variants of node-link diagrams; rather than drawing a link between parent and child in the hierarchy, nodes are drawn as solid areas (either arcs or bars), and their placement relative to adjacent nodes reveals their position in the hierarchy.

* In the `icicle` layout the root node appears at the top, with child nodes underneath. Because the nodes are space-filling, it reveals an additional dimension that would be difficult to show in a node-link diagram.

* The `sunburst` layout is equivalent to the "icicle" layout, but in polar coordinates.

* `sunburst_data` extracts the information from a tree structure, either a string or a file in newick format.

The results can be passed to `ggplot()`.

This package uses some code from the python module `ETE`, a python Environment for phylogenetic Tree Exploration (http://ete.cgenomics.org/)

ggsunburst depends on `ggplot2` and `reticulate` packages. You will need to install them before using it.

http://genome.crg.es/~didac/ggsunburst/

## Example
    
    if (!require(ggplot2)) install.packages("ggplot2")
    if (!require(reticulate)) install.packages("reticulate")
    library(ggsunburst)
    
    # newick format
    nw <- "(((a, b, c), (d, e, f, g)), (f, i, h));"
    
    # extract data
    sb <- sunburst_data(nw)
    icicle(sb)
    sunburst(sb)
    
    # demonstrate use of data with ggplot()
    p <- ggplot(sb$rects)
    
    # icicle diagram
    p + geom_rect(aes(xmin=xmin, xmax=xmax, ymin=ymin, ymax=ymax), size=1, color="white") + scale_y_reverse()
    
    # sunburst diagram
    p + geom_rect(aes(xmin=xmin, xmax=xmax, ymin=ymin, ymax=ymax), size=1, color="white") + coord_polar()
  




