# Pattern: Bug Fix Touches Only Bug-Related Lines

## Principle
Surgical Changes — Every changed line traces to the request.

## When to Use
When fixing a specific bug in existing code.

## The Pattern
```diff
  def validate_user(user_data):
      # Check email format
-     if not user_data.get('email'):
+     email = user_data.get('email', '')
+     if not email or not email.strip():
          raise ValueError("Email required")
      
      # Basic email validation
-     if '@' not in user_data['email']:
+     if '@' not in email:
          raise ValueError("Invalid email")
      
      # Check username
      if not user_data.get('username'):
          raise ValueError("Username required")
      
      return True
```

## Why It Works
- Only 3 lines changed — all directly fix the empty email crash
- Existing comments untouched
- No docstring added
- Username validation untouched (not part of the bug)
- Style matches existing code exactly
- Diff is reviewable in seconds

## The Test
For every changed line, ask: "Does this line fix the reported bug?"
If the answer is "no, but it's an improvement" — revert it and mention it instead.
