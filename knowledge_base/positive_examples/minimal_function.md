# Pattern: One Function Until Complexity Is Needed

## Principle
Simplicity First — Minimum code that solves the problem.

## When to Use
When asked to add a calculation, transformation, or utility function.

## The Pattern
```python
def calculate_discount(amount: float, percent: float) -> float:
    """Calculate discount amount. percent should be 0-100."""
    return amount * (percent / 100)

# Usage
discount = calculate_discount(100.0, 10.0)  # $10 off
```

## Why It Works
- 3 lines instead of 40+
- Instantly readable — no indirection
- Easy to test: one input, one output
- When a second discount type is needed, refactor THEN — not before

## Contrast with Anti-Pattern
Anti-pattern uses Strategy + ABC + dataclass + Config for a single calculation.
That's appropriate for a plugin system with 5+ strategies. For one function? Overkill.

## The Test
Ask: "Would a senior engineer say this is overcomplicated?" If yes, simplify.
Three similar lines > premature abstraction.
