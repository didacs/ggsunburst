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
#' @param  labels if set to \code{TRUE}, variable names are shown.
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
  size=0,
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

  subsetdf <- data[,c('x',variables)]
  m <- reshape2::melt(subsetdf, id.vars='x')
  m <- within(m, {newy=add_to_y + (match(variable,levels(m$variable))-1) * height})
  p <- p + geom_tile(data=m,
                     aes(x=x, y=newy, fill=value),
                     height=height,
                     width=width,
                     color=color,
                     size=size)

  if (labels) {
    labs <- data.frame( x=max(m$x) + xlabels, unique(m[ c('variable','newy') ]))
    p <- p + geom_text(data=labs,
                       aes(x=x,
                           y=newy,
                           label=variable),
                       angle=angle,
                       hjust=0,
                       size=text.size) + xlim(NA,max(m$x)*xfactor)
  }
  p
}





#' Annotate tree with bars
#'
#' Annotate tree with bars
#'
#' @param  plot object created by any of the ggsunburst functions: \code{\link{sunburst}}, \code{\link{ggtree}} or \code{\link{icicle}}.
#' @param  data data frame. It must contain \code{x} plus additional variable to be shown \code{variables}.
#' @param  variables vector of variables to be included.
#' @param  box_color color for bar and its box.
#' @param  add_to_y move the tile along the \code{y} axis.
#' @param  xfactor scale bars; xfactor < 1 shrinks bar length respect to the tree branches length.
#' @param  labels if set to \code{TRUE}, variable names are shown.
#' @param  labels.text.size size for labels text.
#' @param  show_value if set to \code{TRUE}, values are shown for each bar.
#' @param  values.text.size size for values text.
#' @param  values.text.color color for values text.
#'
#' @export
#' @return A \code{\link[ggplot2]{ggplot}} object

bars <- function (plot, data, variables, box_color = "black",
                  add_to_y = 0, xfactor = 1, labels = F, show_value = F,
                  labels.text.size = 5, values.text.size = 3, values.text.color = "white")
{
  if (!requireNamespace("reshape2", quietly = TRUE)) {
    stop("reshape2 needed for this function to work. Please install it.",
         call. = FALSE)
  }
  subsetdf <- sb$leaf_labels[, c("x", node_attrs)]
  m <- reshape2::melt(subsetdf, id.vars = c("x"))
  m <- within(m, {
    xmin = x - .4
    xmax = x + .4
    ymin = add_to_y + ((match(variable, levels(m$variable))-1) * xfactor)
    ymax = ymin + (xfactor * .95)
    ymax_bar = ymin + (xfactor * .95 * value)
    label = round(value, digits = 2)
  })

  p <- p + geom_rect(data=m, aes(xmin=xmin, xmax=xmax, ymin=ymin, ymax=ymax), fill="white", color=box_color) +
    geom_rect(data=m, aes(xmin=xmin, xmax=xmax, ymin=ymin, ymax=ymax_bar), fill=box_color)

  if (labels) {
    labs <- data.frame(x = max(m$x) + 1, unique(m[c("variable", "ymin")]))
    names(labs) <- c('x','label','y')
    p <- p + geom_text(data=labs, aes(x=x, y=y, label=label), hjust=0, size = labels.text.size)
  }

  if (show_value){
    p <- p + geom_text(data=m, aes(x=x, y=ymin, label=label), hjust=-.1, color=values.text.color, size = values.text.size)

  }
  p
}



#' Highlight nodes in the tree
#'
#' Highlight nodes in the tree
#'
#' @param  plot object created by any of the ggsunburst function \code{\link{ggtree}}
#' @param  data object obtained using the \code{\link{sunburst_data}} function
#' @param  node_names list of nodes to be highlighted
#' @param  fill fill color for highlight rectangle
#' @param  color outline color for highlight rectangle
#' @param  ymax rightmost coordinate for rectangle, default 0
#'
#' @export
#' @return a \code{\link[ggplot2]{ggplot}} object


highlight_nodes <- function(plot, data, fill= "grey82", color = "white", ymax=0, node_names,
                            alpha=1){
  hl <- geom_rect(data = data$rects[data$rects$name %in% node_names,],
                  aes(xmin=xmin, xmax=xmax, ymin=ymin + (ymax-ymin)/2),
                  ymax=ymax, fill = fill, color = color, alpha = alpha)
  p$layers <- c(hl, p$layers)
  p
}
