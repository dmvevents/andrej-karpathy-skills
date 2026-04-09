# NEVER: Use Design Patterns for Single-Use Code

## Principle Violated
Simplicity First — No abstractions for single-use code.

## What Happened
LLM asked to "add a function to calculate discount" produced a Strategy pattern
with ABC, Protocol, Enum, dataclass — 40+ lines for what should be 3 lines.

## The Wrong Code
```python
from abc import ABC, abstractmethod
from dataclasses import dataclass

class DiscountStrategy(ABC):
    @abstractmethod
    def calculate(self, amount: float) -> float:
        pass

class PercentageDiscount(DiscountStrategy):
    def __init__(self, percentage: float):
        self.percentage = percentage
    def calculate(self, amount: float) -> float:
        return amount * (self.percentage / 100)

class FixedDiscount(DiscountStrategy):
    def __init__(self, fixed_amount: float):
        self.fixed_amount = fixed_amount
    def calculate(self, amount: float) -> float:
        return min(self.fixed_amount, amount)

@dataclass
class DiscountConfig:
    strategy: DiscountStrategy
    min_purchase: float = 0.0
    max_discount: float = float('inf')

class DiscountCalculator:
    def __init__(self, config: DiscountConfig):
        self.config = config
    def apply_discount(self, amount: float) -> float:
        if amount < self.config.min_purchase:
            return 0
        discount = self.config.strategy.calculate(amount)
        return min(discount, self.config.max_discount)
```

## Why It's Wrong
- 40+ lines for what should be 3
- Strategy pattern assumes multiple discount types exist — they don't yet
- User has to instantiate 3 objects just to calculate a percentage
- Premature abstraction makes code harder to read, test, and modify

## Hard Rule
One function until complexity is actually needed. Three similar lines of code
is better than a premature abstraction. Refactor when a second use case appears,
not before.
