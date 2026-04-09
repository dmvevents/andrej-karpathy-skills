# NEVER: Start Implementation Without Verifiable Success Criteria

## Principle Violated
Goal-Driven Execution — Define success criteria. Loop until verified.

## What Happened
LLM asked to "fix the authentication system" produced a vague plan
("review code, identify issues, make improvements, test") with no
specific success criteria, then made changes without verifying anything.

## The Wrong Approach
```
I'll fix the authentication system by:
1. Reviewing the code
2. Identifying issues
3. Making improvements
4. Testing the changes

[Proceeds to make changes without clear success criteria]
```

## Why It's Wrong
- "Reviewing the code" is not a verifiable step
- "Identifying issues" — which issues? How do you know you found them all?
- "Making improvements" — improvements to what? Measured how?
- "Testing" — what tests? What passes/fails?
- No reproduction of the actual bug before fixing

## Hard Rule
Transform every imperative task into a verifiable goal:
- "Fix auth" → "What specific symptom? Write a test that reproduces it, make it pass"
- "Add validation" → "Write tests for invalid inputs, then make them pass"
- "Refactor X" → "Ensure tests pass before AND after"

State the plan as: [Step] → verify: [specific check]
