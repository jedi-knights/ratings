# ADR-006: Use Pyright for Type Checking

## Status
Accepted

## Context
Pyright is a fast type checker meant for large Python source bases. It can be used to check for type errors, enforce type annotations, and improve code quality by catching potential bugs early.

## Decision
We will use Pyright for type checking in this project. This includes setting up Pyright configuration to ensure consistent type checking across the codebase.

## Consequences
- Type errors will be caught early, improving code quality.
- Developers need to be familiar with Pyright and type annotations in Python.
- Pyright configuration will need to be maintained as the project evolves.