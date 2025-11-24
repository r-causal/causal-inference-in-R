# Instructions for Claude Agent: Style Guide Compliance

You are tasked with checking and fixing style guide violations in the causal-inference-in-R book based on issue #309.

## Step 1: Read the Style Guide

First, read the full style guide from issue #309:

```bash
gh issue view 309 --json body --jq .body
```

Read and understand all the rules before proceeding.

## Step 2: Create a Plan

**IMPORTANT:** Before starting any work, create a comprehensive plan using the TodoWrite tool.

### For a Single Chapter

If you're checking a single chapter file:
1. Create todos for each major category of checks
2. **Read the entire chapter file first** using the Read tool
3. Run the code styler (`grkstyle::grk_style_dir()`)
4. Run the automated linter
5. Fix automated violations
6. Perform manual checks for non-lintable items
7. Verify all changes

### For the Entire Book

If you're checking the entire book:
1. **Work on ONE chapter at a time** to avoid context issues
2. Create a plan that lists each chapter as a separate todo item
3. For each chapter:
   - Read the entire file
   - Run code styler
   - Run linter
   - Fix violations
   - Manual checks
   - Move to next chapter
4. Do NOT try to process multiple chapters simultaneously

## Step 3: Run the Code Styler

**FIRST**, run the code styler using `grkstyle::grk_style_dir()` to automatically format R code according to the project's style.

For a single file:
```r
grkstyle::grk_style_file("chapters/01-casual-to-causal.qmd")
```

For a directory:
```r
grkstyle::grk_style_dir("chapters")
```

For the entire project:
```r
grkstyle::grk_style_dir(".")
```

Run this in R:
```bash
Rscript -e 'grkstyle::grk_style_file("path/to/file.qmd")'
# or
Rscript -e 'grkstyle::grk_style_dir("chapters")'
```

**Note:** The code styler will automatically fix many formatting issues. Run this BEFORE the linter to reduce manual fixes.

## Step 4: Run the Automated Linter

From the repository root, run:

```bash
uv run linter/style_linter.py <file-or-directory>
```

Examples:
```bash
# Single chapter
uv run linter/style_linter.py chapters/01-casual-to-causal.qmd

# All chapters
uv run linter/style_linter.py chapters/

# Entire book
uv run linter/style_linter.py
```

To see only warnings and errors (hiding info messages):
```bash
uv run linter/style_linter.py <path> --severity warning
```

## Step 5: Fix Automated Violations

Work through each violation reported by the linter. For each file with violations:

1. **Read the entire file first** to understand context
2. Fix violations systematically, going through the file line by line
3. Use the Edit tool to make changes
4. Re-run the linter to verify fixes

### Common Fixes

**Code patterns:**
- `%>%` → `|>`
- `data.frame()` → `tibble()`
- `summarise()` → `summarize()`
- `ifelse()` → `if_else()`
- `sample_n()` / `sample_frac()` → `slice_sample()`
- `case_when(..., TRUE ~ default)` → `case_when(..., .default = default)`
- Comments: `##` → `#`

**Writing:**
- `dataset` → `data set`
- `dataframe` → `data frame`
- `9am` → `9 AM`
- Check any instance of "casual" - verify it shouldn't be "causal"

**Quarto:**
- `echo: false` → consider `code-fold: true` (use judgment)

## Step 6: Manual Checks for Non-Lintable Items

After fixing automated violations, perform these manual checks that cannot be automated:

### Code Checks

1. **Grouping operations:**
   - When grouping by a single variable, use `group_by()` over `.by`
   - When grouping by multiple variables without persistent grouping, prefer `.by` OR use `group_by()` with `.groups = "drop"`
   - Use judgment for readability in complex `summarize()` statements

2. **`augment()` usage:**
   - Use `data = ...` when supplying the original data frame
   - Use `newdata = ...` only for truly new data (e.g., g-computation cloning)
   - Search for: `augment\(`

3. **Explicit boolean testing:**
   - Look for `if (x)` patterns where `x` could be 0 or 1
   - Should be `if (x == 1)` or `if (x == 0)` explicitly
   - The linter flags these as info; review each case

### Quarto Checks

1. **Cross-references:**
   - Look for phrases like "as we discussed earlier", "we will discuss later", "mentioned above"
   - Replace with cross-references using `@sec-`, `@fig-`, `@tbl-` where possible
   - Search for: `discuss`, `mentioned`, `earlier`, `later`, `above`, `below`

2. **Sentence breaks:**
   - Each sentence should be on its own line for easier git diffs
   - This is hard to check manually; consider using RStudio visual mode
   - Lower priority unless explicitly requested

3. **Package name formatting:**
   - First mention in a chapter: `` `{pkgname}` `` (creates link)
   - Subsequent mentions: just `pkgname` (no formatting)
   - Search for package names and verify first mention is formatted

### Writing Checks

1. **Defined terms vs. emphasis:**
   - First definition of a term: **bold**
   - Emphasis: *italics*
   - Never italics for definitions
   - Search for: `\*[^*]+\*` (single asterisk patterns)

2. **Terminology consistency:**
   - Prefer "exposure" and "outcome" for generic causal terms
   - Check for inconsistent use of "treated/untreated", "treatment/control"
   - Use judgment based on context

3. **Specific terms:**
   - "Extra Magic Hours" (all caps)
   - "Extra Magic Morning" / "Extra Magic Evening" (all caps)
   - Search for: `extra magic` (case-insensitive)

4. **"casual" vs "causal":**
   - The linter flags all instances of "casual"
   - Review each one - some are legitimate (e.g., "casual inference" is the title of Chapter 1)
   - Fix only actual typos

### Figures and Tables Checks

1. **Captions:**
   - Every figure and table must have a thorough caption
   - Caption should describe what's IN the figure/table, not just the concept
   - Search for: `#| label: fig-` and `#| label: tbl-`
   - Verify each has a corresponding `#| fig-cap:` or `#| tbl-cap:`

2. **Table creation:**
   - Use `gt()` for code-based tables, not `kable()`
   - Markdown tables are fine for simple tables
   - Search for: `kable\(`

3. **EMM DAG consistency:**
   - No time labels on EMM DAG (we don't actually know the times)
   - Search for: `emm`, `extra magic` in DAG code
   - Check multiple locations for consistency

## Step 7: Report Summary

After completing all checks, provide a summary:

1. Number of automated violations found and fixed
2. Any manual issues found and fixed
3. Any issues that need human judgment or discussion
4. Files modified

## Important Reminders

- **Run code styler FIRST** before doing any manual fixes
- **Read entire files before editing** - never edit based on search results alone
- **One chapter at a time** for full book checks
- **Use TodoWrite** to track progress through the plan
- **Mark todos as completed** as you finish each one
- **Re-run linter** after fixes to verify
- **Some "casual" instances are legitimate** - use judgment
- **Don't over-fix** - not every suggestion needs to be applied if context makes it unclear

## Example Workflow for a Single Chapter

```bash
# 1. Read the style guide
gh issue view 309 --json body --jq .body

# 2. Create a plan with TodoWrite
# Todos:
# - Read entire chapter file
# - Run code styler
# - Run automated linter
# - Fix code pattern violations
# - Fix writing violations
# - Manual check: grouping operations
# - Manual check: cross-references
# - Manual check: figure/table captions
# - Verify all changes

# 3. Read the file
Read chapters/01-casual-to-causal.qmd

# 4. Run code styler
Rscript -e 'grkstyle::grk_style_file("chapters/01-casual-to-causal.qmd")'

# 5. Run linter
uv run linter/style_linter.py chapters/01-casual-to-causal.qmd

# 6. Fix violations using Edit tool

# 7. Manual checks (search and review)

# 8. Re-run linter to verify
uv run linter/style_linter.py chapters/01-casual-to-causal.qmd --severity warning

# 9. Report summary
```

## Example Workflow for Entire Book

```bash
# 1. Read the style guide
gh issue view 309 --json body --jq .body

# 2. Run code styler on entire project FIRST
Rscript -e 'grkstyle::grk_style_dir(".")'

# 3. Create a plan listing each chapter
# Todos:
# - Process chapters/01-casual-to-causal.qmd
# - Process chapters/02-whole-game.qmd
# - Process chapters/03-po-counterfactuals.qmd
# ... (one todo per chapter)

# 4. For EACH chapter, one at a time:
#    - Read entire file
#    - Run linter on that chapter
#    - Fix violations
#    - Manual checks
#    - Mark todo as completed
#    - Move to next chapter

# 5. Final summary across all chapters
```

## Search Patterns for Manual Checks

Use Grep tool with these patterns:

```bash
# Grouping operations
pattern: "group_by|\.by"

# augment usage
pattern: "augment\("

# Cross-reference phrases
pattern: "discuss|mentioned|earlier|later|above|below"

# Package mentions (to check formatting)
pattern: "`\{[a-zA-Z0-9]+\}`"

# Bold vs italic usage
pattern: "\*[^*]+\*"

# Extra Magic references
pattern: "extra magic" (case-insensitive with -i flag)

# kable usage
pattern: "kable\("

# Figure/table labels
pattern: "#\| label: (fig-|tbl-)"
```

## Complete Checklist Template

When creating your plan, use this template:

### Single Chapter
- [ ] Read the style guide (issue #309)
- [ ] Read entire chapter file
- [ ] Run `grkstyle::grk_style_file()` on the chapter
- [ ] Run automated linter
- [ ] Fix code pattern violations
- [ ] Fix writing violations
- [ ] Manual check: grouping operations
- [ ] Manual check: `augment()` usage
- [ ] Manual check: cross-references
- [ ] Manual check: package name formatting
- [ ] Manual check: bold vs italic for definitions
- [ ] Manual check: terminology consistency
- [ ] Manual check: figure/table captions
- [ ] Manual check: table creation (`gt()` vs `kable()`)
- [ ] Verify all changes
- [ ] Report summary

### Full Book
- [ ] Read the style guide (issue #309)
- [ ] Run `grkstyle::grk_style_dir(".")` on entire project
- [ ] For each chapter (one at a time):
  - [ ] Read entire file
  - [ ] Run linter
  - [ ] Fix automated violations
  - [ ] Perform manual checks
  - [ ] Mark completed, move to next chapter
- [ ] Final summary report

Remember: Your goal is to ensure consistency with the style guide while maintaining readability and not introducing errors. When in doubt, ask for clarification rather than making assumptions.
