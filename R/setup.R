options(
  tidyverse.quiet = TRUE,
  propensity.quiet = TRUE,
  tipr.verbose = FALSE,
  htmltools.dir.version = FALSE,
  width = 55,
  digits = 4,
  ggplot2.discrete.colour = ggokabeito::palette_okabe_ito(),
  ggplot2.discrete.fill = ggokabeito::palette_okabe_ito(),
  ggplot2.continuous.colour = "viridis",
  ggplot2.continuous.fill = "viridis",
  book.base_family = "sans",
  book.base_size = 14
)

library(ggplot2)

theme_set(
  theme_minimal(
    base_size = getOption("book.base_size"),
    base_family = getOption("book.base_family")
  ) %+replace%
    theme(
      panel.grid.minor = element_blank(),
      legend.position = "bottom"
    )
)

theme_dag <- function() {
  ggdag::theme_dag(base_family = getOption("book.base_family"))
}

geom_dag_label_repel <- function(..., seed = 10) {
  ggdag_geom_dag_label_repel(
    aes(x, y, label = label),
    box.padding = 3.5,
    inherit.aes = FALSE,
    max.overlaps = Inf,
    family = getOption("book.base_family"),
    seed = seed,
    label.size = NA,
    label.padding = 0.1,
    size = getOption("book.base_size") / 3,
    ...
  )
}

est_ci <- function(.df, rsample = FALSE) {
  if (!is.data.frame(.df) && is.numeric(.df)) {
    return(
      glue::glue(
        "{round(.df[[1]], digits = 1)} (95% CI {round(.df[[2]], digits = 1)}, {round(.df[[3]], digits = 1)})"
      )
    )
  }

  if (rsample) {
    glue::glue(
      "{round(.df$.estimate, digits = 1)} (95% CI {round(.df$.lower, digits = 1)}, {round(.df$.upper, digits = 1)})"
    )
  } else {
    glue::glue("{.df$estimate} (95% CI {.df$conf.low}, {.df$conf.high})")
  }
}

# based on https://github.com/hadley/r-pkgs/blob/main/common.R
status <- function(type) {
  status <- switch(
    type,
    unstarted = "is unstarted, but don't worry, it's on our roadmap",
    polishing = "has its foundations written but is still undergoing changes",
    wip = "is actively undergoing work and may be restructured or changed. It may also be incomplete",
    complete = "is mostly complete, but we might make small tweaks or copyedits",
    stop("Invalid `type`", call. = FALSE)
  )

  class <- switch(
    type,
    complete = ,
    polishing = "callout-note",
    wip = "callout-warning",
    unstarted = "callout-warning"
  )

  knitr::asis_output(paste0(
    "::: ",
    class,
    "\n",
    "## Work-in-progress 🚧\n",
    "You are reading the work-in-progress first edition of *Causal Inference in R*. ",
    "This chapter ",
    status,
    ". \n",
    ":::\n"
  ))
}
