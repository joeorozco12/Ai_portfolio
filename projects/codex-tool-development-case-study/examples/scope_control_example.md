# Scope Control Example

[SYNTHETIC — FOR DEMONSTRATION ONLY]

> Human Review Required: AI-generated outputs are decision-support artifacts only. A qualified engineer owns final review and approval.

## Publication Classification

Needs review

## Purpose

This example shows how Codex work can be constrained so a portfolio task changes only the intended project files.

## Scope Rule

```text
Work only inside:
projects/example-engineering-workflow/

Do not edit homepage files.
Do not edit Task 1, Task 2, Task 4, Task 5, or Task 6 files.
Do not modify unrelated generated outputs.
```

## Review Method

After the task, review changed files with:

```text
git status --short
git show --name-only --stat HEAD
```

Expected result:

```text
Only files under the approved project folder are staged or committed.
```

## Human Review Controls

- Review the changed-file list before committing.
- Keep unrelated working-tree changes unstaged.
- Reject scope drift before public use.
- Confirm the artifact uses synthetic or sanitized examples.

## Risks and Mitigations

- Risk: A tool edit may spill into unrelated files. Mitigation: constrain the folder and review changed files.
- Risk: Generated outputs may overwrite previous work. Mitigation: name protected areas explicitly.
- Risk: Scope language may be ambiguous. Mitigation: list the exact allowed folder and protected folders.

## Proof Gaps

- Example needs final review before public use.
- No screenshot of a scoped changed-file review is included yet.

## Safe to Publish Status

Needs review. This example uses synthetic folder names and generic commands only.
