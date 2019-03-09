#' Creates sunburst diagram using ggplot2.
#'
#' Creates sunburst diagram using ggplot2.
#'
#' @param data object obtained using the \code{\link{sunburst_data}} function
#' @param rects.fill color of space-filled nodes
#' @param rects.fill.aes color of space-filled nodes mapped to a variable
#' @param rects.color color of line delimiter between partitions
#' @param rects.size size of line delimiter between partitions
#' @param blank if TRUE, a blank theme is applied
#' @param leaf_labels if TRUE, shows leaf labels
#' @param leaf_labels.size size for text of labels
#' @param leaf_labels.color color for text of labels
#' @param node_labels if TRUE, shows leaf labels
#' @param node_labels.size size for text of labels
#' @param node_labels.color color for text of labels
#'
#' @export
#' @return A \code{\link[ggplot2]{ggplot}} object
#' @seealso \code{\link{sunburst_data}}

sunburst <- function(
	data,
	rects.fill="white",
	rects.fill.aes=0,
	rects.color="black",
	rects.size=.5,
	blank=T,
	leaf_labels=T,
	leaf_labels.size = 2,
	leaf_labels.color = "black",
  node_labels = F,
	node_labels.size = 2,
	node_labels.color = "black",
	node_labels.min = 90
  ){

	p <- ggplot(data$rects)

	if (blank) p <- p + theme_void()

	# arcs
	if (rects.fill.aes == 0){
		p <- p + geom_rect(
	    	aes_string(xmin="xmin", xmax="xmax", ymin="ymin",	ymax="ymax"),
	    	fill=rects.fill, size=rects.size, color=rects.color)
	} else {
		p <- p + geom_rect(
	    	aes_string(xmin="xmin", xmax="xmax", ymin="ymin",	ymax="ymax", fill=rects.fill.aes),
   	    	size=rects.size,	color=rects.color)
	}
	if (leaf_labels){
		p <- p + geom_text(data=data$leaf_labels,
			aes_string(x="x", y="y", label="label", angle="angle"),
			size=leaf_labels.size, color=leaf_labels.color, hjust=.5)
 	}
  if (node_labels){
    p <- p + geom_text(data=data$node_labels[data$node_labels$delta_angle >= node_labels.min, ],
       aes_string(x="x", y="y", label="label", angle="pangle", vjust="pvjust"),
       size=node_labels.size, color=node_labels.color, hjust=.5)
  }
	p + xlab("") + ylab("") + coord_polar() + ylim(min(data$rects$ymin)-1,NA)
}



#' Creates icicle diagram using ggplot2.
#'
#' Creates icicle diagram using ggplot2.
#'
#' @param data object obtained using the \code{\link{sunburst_data}} function
#' @param rects.fill color of space-filled nodes
#' @param rects.fill.aes color of space-filled nodes mapped to a variable
#' @param rects.color color of line delimiter between partitions
#' @param rects.size size of line delimiter between partitions
#' @param blank if TRUE, a blank theme is applied
#' @param leaf_labels if TRUE, shows leaf labels
#' @param leaf_labels.size size for text of labels
#' @param leaf_labels.color color for text of labels
#' @param node_labels if TRUE, shows leaf labels
#' @param node_labels.size size for text of labels
#' @param node_labels.color color for text of labels
#'
#' @export
#' @return A \code{\link[ggplot2]{ggplot}} object
#' @seealso \code{\link{sunburst_data}}

icicle <- function(
	data,
	rects.fill="white",
	rects.fill.aes=0,
	rects.color="black",
	rects.size=.5,
	blank=T,
	leaf_labels=T,
	leaf_labels.size = 2,
	leaf_labels.color = "black",
	node_labels = F,
	node_labels.size = 2,
	node_labels.color = "black",
	node_labels.min = .25
){

	p <- ggplot(data$rects)

	if (blank) p <- p + theme_void()

	# rects
	if (rects.fill.aes == 0){
		p <- p + geom_rect(
	    	aes_string(xmin="xmin", xmax="xmax", ymin="ymin", ymax="ymax"),
	    	fill=rects.fill, size=rects.size, color=rects.color)
	} else {
		p <- p + geom_rect(
	    	aes_string(xmin="xmin", xmax="xmax", ymin="ymin", ymax="ymax",
                   fill=rects.fill.aes),
   	    size=rects.size, color=rects.color)
	}

	if (leaf_labels){
		p <- p + geom_text(data=data$leaf_labels,
			aes_string(x="x", y="y", label="label"),
			size=leaf_labels.size, color=leaf_labels.color, angle=90, hjust=0.5)
	}
	if (node_labels){
	  p <- p + geom_text(data=data$node_labels[data$node_labels$xfraction >= node_labels.min, ],
	    aes_string(x="x", y="y", label="label"),
	    size=node_labels.size, color=node_labels.color)
	}

  p + xlab("") + ylab("") + scale_y_reverse()

}


#' Creates tree diagram using ggplot2.
#'
#' Creates tree diagram using ggplot2.
#'
#' @param   data object obtained using the \code{\link{sunburst_data}} function
#' @param   plot a \code{\link[ggplot2]{ggplot}} object
#' @param   rotate if TRUE (default), the root appears on the left
#' @param   color color of the segments (branches)
#' @param   size size of the segments (branches)
#' @param   blank if TRUE, a blank theme is applied
#' @param   labels if TRUE, leaf labels are shown
#' @param   text.size size for text of labels
#' @param   text.color color for text of labels
#' @param   show_scale show branch length scale
#' @param   polar show circular tree
#'
#' @export
#' @return A \code{\link[ggplot2]{ggplot}} object
#' @seealso \code{\link{sunburst_data}}


ggtree <- function(
  data=0,
  plot=0,
  rotate=T,
  color="black",
  size=1,
  blank=T,
  labels=T,
  text.size=3,
  text.color="black",
  show_scale = F,
  show_scale_length = 0,
  polar=F
){

  p <- plot
  if (class(p)[1] == 'numeric') p <- ggplot(data=data$segments)
  if (rotate) p <- p + coord_flip()
  if (blank)  p <- p + theme_void()

  # segments along x axis
  p <- p + geom_segment(
    aes_string(x="px", xend="pxend", y="ryend", yend="ryend"),
    na.rm=T, size=size, color=color, lineend="square")

  # segments along y axis
  p <- p + geom_segment(
    aes_string(x="rx", xend="rx", y="ry", yend="ryend"),
    na.rm=T, size=size, color=color, lineend="square")

  p <- p + xlab("") + ylab("")

  if (polar)  {
    if (labels){
      y <- max(data$segments$ryend, na.rm=T)
      p <- p + geom_segment(data=data$leaf_labels,
                            aes_string(x="x", xend="x", y="y", yend=y),
                            size=size/2, color="grey10")
      p <- p + geom_text(data=data$leaf_labels,
                         aes_string(x="x", y=y+.1, label="label", angle="angle",
                                    hjust="hjust"),
                         size=text.size, color=text.color)
    }
    p + xlim(0.5, nrow(data$leaf_labels) + 0.5) + coord_polar()
  } else {
    if (labels){
      y <- max(data$segments$ryend, na.rm=T)
      p <- p + geom_text(data=data$leaf_labels,
                         aes_string(x="x", y="y_out+.1", label="label"),
                         size=text.size, color=text.color, angle=0, hjust=0)
    }
    if (show_scale){
      y <- min(data$segments$ry)
      if (show_scale_length > 0){
        l <- show_scale_length
      } else {
        l <- abs(round(y/10, digits = 2))
      }
      scale.df <- data.frame(x=-1, xend=-1, y=y, yend=y + l, label=l)

      p <- p + geom_segment(data = scale.df, aes(x=x, xend=xend, y=y, yend=yend)) +
        geom_text(data = scale.df, aes(x=x,y=y + (yend-y)/2, label=label), vjust=-.5)

    }
    p
  }
}



ggtree2 <- function (
  data=0,
  plot=0,
  rotate=T,
  color="black",
  size=1,
  blank=T,
  labels=T,
  text.size=3,
  text.color="black",
  show_scale = F,
  show_scale_length = 0,
  polar=F,
  highlight.ymax = 0
){
  p <- plot
  if (class(p)[1] == "numeric") p <- ggplot(data = data$segments)

  # highlight nodes
  y_out <- max(data$leaf_labels$y_out)
  p <- p + geom_rect( data = data$rects[ data$rects$highlight, ] ,
                      aes(xmin=xmin, xmax=xmax, ymin=ymin + .5, fill=name),
                      ymax=highlight.ymax)

  if (rotate) p <- p + coord_flip()
  if (blank) p <- p + theme_void()

  p <- p + geom_segment(aes_string(x = "px", xend = "pxend",
                                   y = "ryend", yend = "ryend"), na.rm = T, size = size,
                        color = color, lineend = "square")
  p <- p + geom_segment(aes_string(x = "rx", xend = "rx", y = "ry",
                                   yend = "ryend"), na.rm = T, size = size, color = color,
                        lineend = "square")
  p <- p + xlab("") + ylab("")
  if (polar) {
    if (labels) {
      y <- max(data$segments$ryend, na.rm = T)
      p <- p + geom_segment(data = data$leaf_labels, aes_string(x = "x",
                                                                xend = "x", y = "y", yend = y), size = size/2,
                            color = "grey10")
      p <- p + geom_text(data = data$leaf_labels, aes_string(x = "x",
                                                             y = y + 0.5, label = "label", angle = "angle",
                                                             hjust = "hjust"), size = text.size, color = text.color)
    }
    p + xlim(0.5, nrow(data$leaf_labels) + 0.5) + coord_polar()
  }
  else {
    if (labels) {
      y <- max(data$segments$ryend, na.rm = T)
      p <- p + geom_text(data = data$leaf_labels, aes_string(x = "x",
                                                             y = "y_out+.1", label = "label"), size = text.size,
                         color = text.color, angle = 0, hjust = 0)
    }
    p
  }
}


blank_bg <- function(p){
	p + xlab("") + ylab("") +
    theme(
        axis.line        = element_blank(),
        axis.ticks       = element_blank(),
        axis.text.y      = element_blank(),
        axis.text.x      = element_blank(),
        panel.grid.major = element_blank(),
        panel.grid.minor = element_blank(),
        panel.border     = element_blank(),
        panel.background = element_blank()
    )
}
