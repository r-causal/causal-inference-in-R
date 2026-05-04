
<!-- README.md is generated from README.Rmd. Please edit that file -->

# Causal Inference in R

<!-- badges: start -->

<!-- badges: end -->

This repository contains the source code for the book *Causal Inference
in R.*

## Installation

After cloning this repository, you can install the package dependencies
for this book with:

``` r
# install.packages("remotes")
remotes::install_deps(dependencies = TRUE)
```

We use [Quarto](https://quarto.org/) to render this book.

## Formatting and linting

This project uses [panache](https://panache.bz/) to format and lint the
Quarto documents. For the code cells, panache uses
[air](https://posit-dev.github.io/air/) and
[jarl](https://jarl.etiennebacher.com/) for formatting and linting,
respectively.

``` bash
panache format chapters/
panache lint chapters/
```
