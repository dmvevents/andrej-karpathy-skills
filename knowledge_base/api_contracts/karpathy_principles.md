# Karpathy Coding Principles — Ground Truth

## Source
Andrej Karpathy, X post (2025): observations on LLM coding pitfalls.

## The Four Principles

### 1. Think Before Coding
**Trigger:** Any ambiguous request, multiple interpretations, or unclear requirements.
**Action:** Enumerate assumptions, present alternatives, push back if simpler path exists.
**Anti-patterns:** Silent assumption, single-interpretation selection, proceeding through confusion.

### 2. Simplicity First
**Trigger:** Any feature implementation, utility function, or new code.
**Action:** Write minimum code that solves the problem. No speculative features.
**Anti-patterns:** Strategy pattern for one function, caching nobody asked for, validation without schema.
**Test:** "Would a senior engineer say this is overcomplicated?"

### 3. Surgical Changes
**Trigger:** Any edit to existing code (bug fixes, features, refactoring).
**Action:** Touch only what's needed. Match existing style. Mention improvements, don't implement.
**Anti-patterns:** Drive-by refactoring, style drift, docstring addition, adjacent improvements.
**Test:** "Does every changed line trace to the user's request?"

### 4. Goal-Driven Execution
**Trigger:** Any task that requires multiple steps or has vague requirements.
**Action:** Transform to verifiable goals. Plan as [Step] → verify: [check]. Reproduce before fixing.
**Anti-patterns:** Vague plans, fixing without reproducing, no success criteria.
**Key insight:** "Give it success criteria and watch it go."

## Evaluation Rubric

| Score | Meaning |
|-------|---------|
| 0 | Violated the principle — wrong assumptions, overcomplicated, drive-by changes, vague execution |
| 1 | Partially followed — some assumptions surfaced but not all, mostly minimal but with extras |
| 2 | Fully followed — all assumptions explicit, minimal code, surgical diff, verifiable goals |
