# Pattern: Enumerate Assumptions Before Implementing

## Principle
Think Before Coding — State assumptions explicitly.

## When to Use
When a request has ambiguous scope, format, fields, or architecture.

## The Pattern
Before writing any code, output a numbered list:
```
Before implementing, I need to clarify:

1. **Scope**: Export all users or filtered subset? (privacy implications)
2. **Format**: Download file? Background job? API endpoint?
3. **Fields**: Which user fields? (some might be sensitive)
4. **Volume**: How many users typically? (affects approach)

Simplest approach: Add an API endpoint that returns paginated JSON.
What's your preference?
```

## Why It Works
- Forces the LLM to reason about ambiguity before committing to code
- Gives the user control over decisions that affect architecture
- Prevents rework from wrong assumptions
- The "simplest approach" line shows the default without forcing it

## Key Elements
1. Number each assumption (easy to reference in response)
2. Include WHY it matters in parentheses
3. Offer the simplest default
4. End with an explicit question
