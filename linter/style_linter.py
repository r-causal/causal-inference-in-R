#!/usr/bin/env python3
"""
Style guide linter for causal-inference-in-R book.
Checks for style violations based on issue #309.
"""

import argparse
import re
import sys
from pathlib import Path
from dataclasses import dataclass
from typing import List, Tuple


@dataclass
class Violation:
    """Represents a style violation."""
    file: Path
    line: int
    rule: str
    message: str
    severity: str = "warning"


class StyleLinter:
    """Lints R and Quarto files for style guide compliance."""

    def __init__(self):
        self.violations: List[Violation] = []

    def check_file(self, file_path: Path) -> List[Violation]:
        """Check a single file for style violations."""
        self.violations = []

        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                lines = f.readlines()
        except Exception as e:
            print(f"Error reading {file_path}: {e}", file=sys.stderr)
            return []

        in_code_block = False
        code_block_type = None

        for i, line in enumerate(lines, start=1):
            # Track code blocks
            if line.strip().startswith('```{r'):
                in_code_block = True
                code_block_type = 'r'
                continue
            elif line.strip().startswith('```'):
                if in_code_block:
                    in_code_block = False
                    code_block_type = None
                continue

            # Apply appropriate checks
            if in_code_block and code_block_type == 'r':
                self._check_r_code(file_path, i, line)
            else:
                self._check_prose(file_path, i, line)
                self._check_quarto(file_path, i, line)

        return self.violations

    def _check_r_code(self, file_path: Path, line_num: int, line: str):
        """Check R code for style violations."""
        # Skip commented lines for some checks
        stripped = line.strip()
        is_comment = stripped.startswith('#')

        # Code pattern checks
        if not is_comment:
            # Check for pipe operator
            if '%>%' in line:
                self.violations.append(Violation(
                    file_path, line_num, "code-pipe",
                    "Use |> instead of %>%"
                ))

            # Check for data.frame()
            if re.search(r'\bdata\.frame\s*\(', line):
                self.violations.append(Violation(
                    file_path, line_num, "code-tibble",
                    "Use tibble() instead of data.frame()"
                ))

            # Check for summarise()
            if re.search(r'\bsummarise\s*\(', line):
                self.violations.append(Violation(
                    file_path, line_num, "code-summarize",
                    "Use summarize() instead of summarise()"
                ))

            # Check for ifelse()
            if re.search(r'\bifelse\s*\(', line):
                self.violations.append(Violation(
                    file_path, line_num, "code-if-else",
                    "Use if_else() instead of ifelse()"
                ))

            # Check for sample_n() or sample_frac()
            if re.search(r'\bsample_n\s*\(', line) or re.search(r'\bsample_frac\s*\(', line):
                self.violations.append(Violation(
                    file_path, line_num, "code-slice-sample",
                    "Use slice_sample() instead of sample_n() or sample_frac()"
                ))

            # Check for TRUE ~ in case_when (looking for default pattern)
            if re.search(r'TRUE\s*~', line) and 'case_when' in line:
                self.violations.append(Violation(
                    file_path, line_num, "code-case-when",
                    "Use .default = default_value instead of TRUE ~ default_value in case_when()"
                ))

            # Check for implicit boolean testing
            # This is a simplified check - looks for if (variable) patterns
            # Matches if (x) but not if (x == ...) or if (x > ...) etc.
            if_pattern = re.search(r'\bif\s*\(\s*([a-zA-Z_][a-zA-Z0-9_]*)\s*\)', line)
            if if_pattern:
                self.violations.append(Violation(
                    file_path, line_num, "code-explicit-test",
                    f"Use explicit testing (e.g., if ({if_pattern.group(1)} == 1)) instead of implicit boolean test",
                    severity="info"
                ))

        # Comment style checks
        if is_comment:
            # Check for multiple # at start (allow roxygen comments #')
            if re.match(r'^\s*##', stripped) and not stripped.startswith("#'"):
                self.violations.append(Violation(
                    file_path, line_num, "comment-style",
                    "Use single # for comments"
                ))

            # Check for uppercase at start of comment (excluding proper nouns)
            # This is a basic check - looks for capital letters after #
            comment_text = re.sub(r'^\s*#+\s*', '', line)
            if comment_text and comment_text[0].isupper():
                # Allow some exceptions like acronyms, proper nouns
                # This is conservative - only flag obvious cases
                if not re.match(r'^[A-Z]{2,}', comment_text):  # Not an acronym
                    self.violations.append(Violation(
                        file_path, line_num, "comment-lowercase",
                        "Comments should use lowercase (except proper nouns)",
                        severity="info"
                    ))

    def _check_prose(self, file_path: Path, line_num: int, line: str):
        """Check prose text for style violations."""
        # Check for "casual" typo (common typo for "causal")
        # Be careful not to flag legitimate uses of "casual"
        if 'casual' in line.lower():
            # This might be legitimate, so make it info level
            self.violations.append(Violation(
                file_path, line_num, "writing-casual-typo",
                "Found 'casual' - verify this isn't a typo for 'causal'",
                severity="info"
            ))

        # Check for time format (should be "9 AM" not "9am")
        if re.search(r'\d+\s*am\b', line, re.IGNORECASE):
            if not re.search(r'\d+\s+AM\b', line):
                self.violations.append(Violation(
                    file_path, line_num, "writing-time-format",
                    "Use '9 AM' format instead of '9am'"
                ))

        if re.search(r'\d+\s*pm\b', line, re.IGNORECASE):
            if not re.search(r'\d+\s+PM\b', line):
                self.violations.append(Violation(
                    file_path, line_num, "writing-time-format",
                    "Use '9 PM' format instead of '9pm'"
                ))

        # Check for "data frame" and "data set" (with space)
        if re.search(r'\bdataframe\b', line, re.IGNORECASE):
            self.violations.append(Violation(
                file_path, line_num, "writing-data-frame",
                "Use 'data frame' (with space) instead of 'dataframe'"
            ))

        if re.search(r'\bdataset\b', line, re.IGNORECASE):
            self.violations.append(Violation(
                file_path, line_num, "writing-data-set",
                "Use 'data set' (with space) instead of 'dataset'"
            ))

        # Check for "upweighting" and "downweighting" (one word)
        if re.search(r'\bup\s+weighting\b', line, re.IGNORECASE):
            self.violations.append(Violation(
                file_path, line_num, "writing-upweighting",
                "Use 'upweighting' (one word, no space)"
            ))

        if re.search(r'\bdown\s+weighting\b', line, re.IGNORECASE):
            self.violations.append(Violation(
                file_path, line_num, "writing-downweighting",
                "Use 'downweighting' (one word, no space)"
            ))

    def _check_quarto(self, file_path: Path, line_num: int, line: str):
        """Check Quarto-specific style."""
        # Check for echo: false in code blocks (should prefer code-fold: true)
        if re.search(r'echo:\s*false', line):
            self.violations.append(Violation(
                file_path, line_num, "quarto-code-fold",
                "Prefer 'code-fold: true' over 'echo: false'",
                severity="info"
            ))

        # Check for package name formatting
        # Looking for {pkg} pattern to ensure it's formatted correctly
        # This is informational since we can't know context
        if re.search(r'`\{[a-zA-Z0-9.]+\}`', line):
            pass  # Correct format
        elif re.search(r'\b[a-zA-Z0-9]+\s+package\b', line):
            # Might need formatting
            self.violations.append(Violation(
                file_path, line_num, "quarto-package-format",
                "First mention of package should use `{pkg}` format",
                severity="info"
            ))


def main():
    parser = argparse.ArgumentParser(
        description="Lint R and Quarto files for style guide compliance"
    )
    parser.add_argument(
        'paths',
        nargs='*',
        type=Path,
        help='Files or directories to lint (default: all .qmd files)'
    )
    parser.add_argument(
        '--severity',
        choices=['info', 'warning', 'error'],
        default='info',
        help='Minimum severity level to report (default: info)'
    )
    parser.add_argument(
        '--rule',
        action='append',
        help='Only check specific rules (can be specified multiple times)'
    )

    args = parser.parse_args()

    # Collect files to check
    files_to_check = []

    if args.paths:
        for path in args.paths:
            if path.is_file():
                files_to_check.append(path)
            elif path.is_dir():
                files_to_check.extend(path.rglob('*.qmd'))
    else:
        # Default: check all .qmd files in current directory and subdirectories
        files_to_check = list(Path('.').rglob('*.qmd'))

    if not files_to_check:
        print("No .qmd files found to check")
        return 0

    # Lint files
    linter = StyleLinter()
    all_violations = []

    for file_path in sorted(files_to_check):
        violations = linter.check_file(file_path)

        # Filter by severity
        severity_order = {'info': 0, 'warning': 1, 'error': 2}
        min_severity = severity_order[args.severity]
        violations = [
            v for v in violations
            if severity_order[v.severity] >= min_severity
        ]

        # Filter by rule if specified
        if args.rule:
            violations = [v for v in violations if v.rule in args.rule]

        all_violations.extend(violations)

    # Report violations
    if all_violations:
        print(f"Found {len(all_violations)} style violation(s):\n")

        current_file = None
        for violation in sorted(all_violations, key=lambda v: (str(v.file), v.line)):
            if violation.file != current_file:
                current_file = violation.file
                print(f"\n{violation.file}:")

            print(f"  Line {violation.line} [{violation.severity}] {violation.rule}: {violation.message}")

        return 1
    else:
        print("No style violations found!")
        return 0


if __name__ == '__main__':
    sys.exit(main())
