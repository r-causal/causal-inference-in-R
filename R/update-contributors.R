# Update contributors list from GitHub
# https://github.com/hadley/r4ds/blob/8412c218688ca2dde954009cdf72e49c3e98ea0a/intro.qmd#L253-L313
library(tidyverse)
library(gh)

contribs_all_json <- gh::gh(
  "/repos/:owner/:repo/contributors",
  owner = "r-causal",
  repo = "causal-inference-in-R",
  .limit = Inf
)
contribs_all <- tibble(
  login = contribs_all_json |> map_chr("login"),
  n = contribs_all_json |> map_int("contributions")
)

if (file.exists("contributors.csv")) {
  contribs_old <- read_csv("contributors.csv", col_types = list())
  contribs_new <- contribs_all |> anti_join(contribs_old, by = "login")
} else {
  contribs_old <- tibble(login = character(), name = character())
  contribs_new <- contribs_all
}

# Get info for new contributors
if (nrow(contribs_new) > 0) {
  needed_json <- map(
    contribs_new$login,
    ~ gh::gh("/users/:username", username = .x),
    .progress = TRUE
  )
  info_new <- tibble(
    login = contribs_new$login,
    name = map_chr(needed_json, "name", .default = NA)
  )

  info_old <- contribs_old |> select(login, name)
  info_all <- bind_rows(info_old, info_new)
} else {
  info_all <- contribs_old |> select(login, name)
}

contribs_all <- contribs_all |>
  left_join(info_all, by = "login") |>
  mutate(login_lowercase = str_to_lower(login)) |>
  arrange(login_lowercase) |>
  select(login, name)

write_csv(contribs_all, "contributors.csv")
