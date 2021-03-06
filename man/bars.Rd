% Generated by roxygen2: do not edit by hand
% Please edit documentation in R/extensions.R
\name{bars}
\alias{bars}
\title{Annotate tree with bars}
\usage{
bars(plot, data, variables, box_color = "black", add_to_y = 0,
  xfactor = 1, labels = F, show_value = F, labels.text.size = 5,
  values.text.size = 3, values.text.color = "white")
}
\arguments{
\item{plot}{object created by any of the ggsunburst functions: \code{\link{sunburst}}, \code{\link{ggtree}} or \code{\link{icicle}}.}

\item{data}{data frame. It must contain \code{x} plus additional variable to be shown \code{variables}.}

\item{variables}{vector of variables to be included.}

\item{box_color}{color for bar and its box.}

\item{add_to_y}{move the tile along the \code{y} axis.}

\item{xfactor}{scale bars; xfactor < 1 shrinks bar length respect to the tree branches length.}

\item{labels}{if set to \code{TRUE}, variable names are shown.}

\item{show_value}{if set to \code{TRUE}, values are shown for each bar.}

\item{labels.text.size}{size for labels text.}

\item{values.text.size}{size for values text.}

\item{values.text.color}{color for values text.}
}
\value{
A \code{\link[ggplot2]{ggplot}} object
}
\description{
Annotate tree with bars
}
