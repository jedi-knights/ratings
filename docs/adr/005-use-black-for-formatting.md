# ADR-005: Use Black for Formatting

## Status
Accepted

## Context
Black is an uncompromising Python code formatter. By using Black, we ensure that all Python code in the project adheres to a consistent style, which improves readability and reduces the likelihood of stylistic bugs.

## Decision
We will use Black for formatting all Python code in this project. This includes setting up pre-commit hooks to automatically format code before it is committed.

## Consequences
- Code will be consistently formatted, improving readability.
- Developers need to be familiar with Black's formatting rules.
- Pre-commit hooks will need to be configured to use Black.