# Pattern: Step → Verify Plan for Multi-Step Tasks

## Principle
Goal-Driven Execution — Define success criteria. Loop until verified.

## When to Use
When implementing a multi-step feature or fixing a complex bug.

## The Pattern
```
Plan for rate limiting:

1. Add basic in-memory rate limiting (single endpoint)
   Verify:
   - Test: 100 requests → first 10 succeed, rest get 429
   - Manual: curl endpoint 11 times, see rate limit error

2. Extract to middleware (apply to all endpoints)
   Verify:
   - Test: Rate limits apply to /users and /posts
   - Existing endpoint tests still pass

3. Add Redis backend (for multi-server)
   Verify:
   - Test: Rate limit persists across app restarts
   - Test: Two app instances share rate limit counter

4. Add configuration (rates per endpoint)
   Verify:
   - Test: /search allows 10/min, /users allows 100/min
   - Config file parsed correctly

Each step is independently verifiable and deployable.
```

## Why It Works
- Each step has a concrete check (not "test it")
- Steps are ordered from simplest to most complex
- Each step is independently deployable
- If step 3 fails, steps 1-2 still work
- Verification criteria let the LLM loop without asking

## Key Insight (Karpathy)
"LLMs are exceptionally good at looping until they meet specific goals.
Don't tell it what to do, give it success criteria and watch it go."
