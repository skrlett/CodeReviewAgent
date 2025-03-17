SUMMARIZE_DIFF_PROMPT = """
I would like you to succinctly summarize the diff within 100 words.
If applicable, your summary should include a note about alterations 
to the signatures of exported functions, global data structures and 
variables, and any changes that might affect the external interface or 
behavior of the code.
"""

SUMMARIZE_PR_PROMPT = """## GitHub PR Title

## Description

```
```

## Summary of changes

```
```

## IMPORTANT Instructions

Input: New hunks annotated with line numbers and old hunks (replaced code).
Task: Review new hunks for substantive issues using provided context and respond with comments if necessary.

If there are no issues found on a line range, you MUST respond with the 
text `LGTM!` for that line range in the review section. 

## Changes made to *filename* for your review

"""
