# NEVER: Fix a Bug Without Reproducing It First

## Principle Violated
Goal-Driven Execution — Reproduce first, then fix.

## What Happened
LLM asked "sorting breaks when there are duplicate scores" immediately
changed the sort logic without writing a test to confirm the bug exists
or verifying the fix works.

## The Wrong Approach
```python
# Immediately changes sort logic without confirming the bug
def sort_scores(scores):
    return sorted(scores, key=lambda x: (-x['score'], x['name']))
```

## Why It's Wrong
- No test proves the bug exists (maybe it's already fixed, maybe it's elsewhere)
- No way to verify the fix actually works
- If the fix is wrong, you won't know until production
- No regression protection — could break again later

## Hard Rule
1. Write a test that FAILS (reproduces the bug)
2. Run it multiple times to confirm it's reproducible
3. Fix the code
4. Run the test — it should PASS
5. Run the full test suite — no regressions

The reproduction test IS the success criterion. If you can't reproduce it,
you can't verify the fix.
