# NEVER: Pick One Interpretation When Multiple Exist

## Principle Violated
Think Before Coding — Present multiple interpretations.

## What Happened
LLM asked to "make search faster" silently chose one optimization strategy
(caching + async) without asking which dimension of "faster" matters.

## The Wrong Code
```python
@lru_cache(maxsize=1000)
async def search(query: str) -> List[Result]:
    # 200 lines of optimization combining caching, database indexes,
    # and async processing — without asking which "faster" matters
```

## Why It's Wrong
"Faster" has at least 3 interpretations:
1. Lower latency (response time) — add indexes, cache
2. Higher throughput (concurrent searches) — async, connection pool
3. Better perceived speed (UX) — partial results, progressive loading

Each requires different code. Implementing all three wastes effort and
adds complexity for 2 dimensions that may not matter.

## Hard Rule
When a requirement word has multiple technical interpretations
(faster, better, secure, scalable), enumerate them with effort estimates
and ask which matters before coding.
