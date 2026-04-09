# Pattern: Reproduce Bug With Failing Test Before Fixing

## Principle
Goal-Driven Execution — Test-first verification.

## When to Use
When fixing any reported bug.

## The Pattern
```python
# Step 1: Write a test that FAILS (reproduces the bug)
def test_sort_with_duplicate_scores():
    scores = [
        {'name': 'Alice', 'score': 100},
        {'name': 'Bob', 'score': 100},
        {'name': 'Charlie', 'score': 90},
    ]
    result = sort_scores(scores)
    assert result[0]['score'] == 100
    assert result[1]['score'] == 100
    assert result[2]['score'] == 90

# Step 2: Verify test fails (confirms bug exists)
# Run test 10 times → fails with inconsistent ordering

# Step 3: Fix with stable sort
def sort_scores(scores):
    return sorted(scores, key=lambda x: (-x['score'], x['name']))

# Step 4: Verify test passes consistently
# Step 5: Run full test suite — no regressions
```

## Why It Works
- Proves the bug exists before touching production code
- The test IS the success criterion
- Provides permanent regression protection
- If the fix is wrong, the test catches it immediately
- Documents the expected behavior for future developers

## Hard Rule
No fix without a reproduction test. If you can't write a failing test,
you don't understand the bug well enough to fix it.
