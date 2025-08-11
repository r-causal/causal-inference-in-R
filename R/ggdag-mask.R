# this is all a hack to make work with quick plotting
# TODO: when `geom_dag_label_repel2` exists, add to namespace as 1 then delete this first bit
# copied from source to avoid recursion issue in overriding in ggdag namsespace
ggdag_geom_dag_label_repel <- function(
  mapping = NULL,
  data = NULL,
  parse = FALSE,
  ...,
  box.padding = grid::unit(0.35, "lines"),
  label.padding = grid::unit(0.25, "lines"),
  point.padding = grid::unit(1.5, "lines"),
  label.r = grid::unit(0.15, "lines"),
  label.size = 0.25,
  segment.color = "grey50",
  segment.size = 0.5,
  arrow = NULL,
  force = 1,
  max.iter = 2000,
  nudge_x = 0,
  nudge_y = 0,
  na.rm = FALSE,
  show.legend = NA,
  inherit.aes = TRUE
) {
  ggplot2::layer(
    data = data,
    mapping = mapping,
    stat = ggdag:::StatNodesRepel,
    geom = ggrepel::GeomLabelRepel,
    position = "identity",
    show.legend = show.legend,
    inherit.aes = inherit.aes,
    params = list(
      parse = parse,
      box.padding = box.padding,
      label.padding = label.padding,
      point.padding = point.padding,
      label.r = label.r,
      label.size = label.size,
      segment.colour = segment.color %||%
        segment.colour,
      segment.size = segment.size,
      arrow = arrow,
      na.rm = na.rm,
      force = force,
      max.iter = max.iter,
      nudge_x = nudge_x,
      nudge_y = nudge_y,
      segment.alpha = 1,
      ...
    )
  )
}

geom_dag_label_repel_internal <- function(..., seed = 10) {
  ggdag_geom_dag_label_repel(
    mapping = aes(x, y, label = label),
    # TODO: make sure this looks ok. slightly different from above
    box.padding = 2,
    max.overlaps = Inf,
    inherit.aes = FALSE,
    family = getOption("book.base_family"),
    seed = seed,
    label.size = NA,
    label.padding = 0.01
  )
}

# apply to quick functions as well
assignInNamespace(
  "geom_dag_label_repel",
  geom_dag_label_repel_internal,
  ns = "ggdag"
)

# override some other clumsy internals in ggdag until addressed

assignInNamespace(
  "scale_color_hue",
  ggplot2::scale_color_discrete,
  ns = "ggplot2"
)
assignInNamespace(
  "scale_edge_colour_hue",
  \(...) {
    ggraph::scale_edge_colour_manual(
      ...,
      values = ggokabeito::palette_okabe_ito()
    )
  },
  ns = "ggraph"
)

# force ggraph to respect palette
assignInNamespace(
  "scale_edge_color_discrete",
  ggokabeito::scale_edge_color_okabe_ito,
  ns = "ggraph"
)
