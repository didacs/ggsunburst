#' Adds a geom_tile layer.
#' 
#' Adds a geom_tile layer.
#' 
#' @param  plot object created by any of the ggsunburst functions: \code{\link{sunburst}}, \code{\link{ggtree}} or \code{\link{icicle}}.
#' @param  data data frame. It must contain \code{x} and \code{y} variables, plus the other variables passed as parameter \code{variables}.
#' @param  variables vector of variables to be included in the tile.
#' @param  color color passed to \code{geom_tile}.
#' @param  height height of the tiles.
#' @param  width width of the tiles.
#' @param  add_to_y move the tile along the \code{y} axis.
#' @param  xlabels \code{x} mapping for labels.
#' @param  xfactor xfactor.
#' @param  angle angle for labels text.
#' @param  text.size size for labels text.
#' @param  labels if set to \code{TRUE}, variables names are shown.
#'  
#' @export
#' @return A \code{\link[ggplot2]{ggplot}} object

tile <- function(
  plot,
  data,
  variables,
  color="white",
  height=1,
  width=1,
  add_to_y=0,
  xlabels=1,
  xfactor=1.1,
  angle=90,
  text.size=3,
  labels=F
){
  if (!requireNamespace("reshape2", quietly = TRUE)) {
    stop("reshape2 needed for this function to work. Please install it.",
         call. = FALSE)}
    
  subsetdf <- data[,c('x','y',variables)]
  m <- reshape2::melt(subsetdf, id.vars=c('x','y'))
  m <- within(m, {newy=max(y) + add_to_y + match(variable,levels(m$variable)) * height})
  p <- p + geom_tile(data=m[!is.na(m$value),],
                     aes(x=x,
                         y=newy,
                         fill=value),
                     height=height,
                     width=width,
                     color=color)
  
  if (labels) {
    labs <- data.frame( x=max(m$x) + xlabels, unique(m[ c('variable','newy') ]))
    p <- p + geom_text(data=labs,
                       aes(x=x,
                           y=newy,
                           label=variable),
                       angle=angle,
                       hjust=0,
                       size=text.size) + xlim(0,max(m$x)*xfactor)
  }
  p
}



