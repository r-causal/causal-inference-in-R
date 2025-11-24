# Style Guide Linter

This linter checks the causal-inference-in-R book for compliance with the style guide defined in [issue #309](https://github.com/r-causal/causal-inference-in-R/issues/309).

## Installation

This project uses [uv](https://docs.astral.sh/uv/) for Python package management. From the `linter/` directory:

```bash
# Install dependencies (if any are added in the future)
uv sync
```

## Usage

### Run on all .qmd files in the project

From the repository root:

```bash
uv run linter/style_linter.py
```

Or from the `linter/` directory:

```bash
uv run style_linter.py ..
```

### Run on specific files or directories

```bash
uv run linter/style_linter.py chapters/01-casual-to-causal.qmd
uv run linter/style_linter.py chapters/
```

### Filter by severity level

```bash
# Only show warnings and errors (hide info messages)
uv run linter/style_linter.py --severity warning

# Only show errors
uv run linter/style_linter.py --severity error
```

### Check specific rules only

```bash
# Only check for pipe operator usage
uv run linter/style_linter.py --rule code-pipe

# Check multiple specific rules
uv run linter/style_linter.py --rule code-pipe --rule code-tibble
```

## Rules Checked

### Code Rules (in R code blocks)

- **code-pipe**: Use `|>` instead of `%>%`
- **code-tibble**: Use `tibble()` instead of `data.frame()`
- **code-summarize**: Use `summarize()` instead of `summarise()`
- **code-if-else**: Use `if_else()` instead of `ifelse()`
- **code-slice-sample**: Use `slice_sample()` instead of `sample_n()` or `sample_frac()`
- **code-case-when**: Use `.default = default_value` instead of `TRUE ~ default_value` in `case_when()`
- **code-explicit-test**: Use explicit testing (e.g., `if (x == 1)`) instead of implicit boolean test (e.g., `if (x)`)
- **comment-style**: Use single `#` for comments
- **comment-lowercase**: Comments should use lowercase (except proper nouns)

### Writing Rules (in prose text)

- **writing-casual-typo**: Warns about "casual" to catch potential typos for "causal"
- **writing-time-format**: Use "9 AM" format instead of "9am"
- **writing-data-frame**: Use "data frame" (with space) instead of "dataframe"
- **writing-data-set**: Use "data set" (with space) instead of "dataset"
- **writing-upweighting**: Use "upweighting" (one word, no space)
- **writing-downweighting**: Use "downweighting" (one word, no space)

### Quarto Rules

- **quarto-code-fold**: Prefer `code-fold: true` over `echo: false`
- **quarto-package-format**: First mention of package should use `` `{pkg}` `` format

## Notes

### Manual Checks Required

The following style guide rules require manual review and are not automated:

**Code:**
- Use `grkstyle::grk_style_dir()` to style code
- When grouping by a single variable, use `group_by()` over `.by`
- When grouping by more than one variable, prefer `.by` unless `group_by()` is more readable
- `augment(data = ...)` vs. `augment(newdata = ...)` usage

**Quarto:**
- Prefer cross-references over writing about discussing something elsewhere
- Use sentence breaks (one sentence per line)

**Writing:**
- Defined terms in **bold**; *italics* for emphasis only
- Prefer "exposure" and "outcome" as generic terms
- "Extra Magic Hours" and "Extra Magic Morning/Evening" capitalization

**Figures and Tables:**
- All figures and tables have thorough captions
- Use `gt()` for code-based tables instead of `kable()`
- No time labels for EMM DAG

### Severity Levels

- **info**: Suggestions that may need manual review (e.g., "casual" might be legitimate)
- **warning**: Likely violations that should be fixed
- **error**: Clear violations that must be fixed

## Example Output

```
Found 5 style violation(s):

chapters/01-casual-to-causal.qmd:
  Line 42 [warning] code-pipe: Use |> instead of %>%
  Line 87 [info] writing-casual-typo: Found 'casual' - verify this isn't a typo for 'causal'
  Line 103 [warning] code-summarize: Use summarize() instead of summarise()

chapters/02-whole-game.qmd:
  Line 56 [warning] writing-time-format: Use '9 AM' format instead of '9am'
  Line 112 [warning] code-tibble: Use tibble() instead of data.frame()
```

## Contributing

To add new rules:

1. Add the check logic to the appropriate method in `style_linter.py`:
   - `_check_r_code()` for R code patterns
   - `_check_prose()` for writing style
   - `_check_quarto()` for Quarto-specific rules
2. Create a `Violation` with a descriptive rule name and message
3. Update this README with the new rule
