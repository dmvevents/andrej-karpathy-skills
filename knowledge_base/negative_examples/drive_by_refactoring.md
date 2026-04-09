# NEVER: "Improve" Adjacent Code While Fixing a Bug

## Principle Violated
Surgical Changes — Touch only what you must.

## What Happened
LLM asked to "fix the bug where empty emails crash the validator" also
improved email validation, added username validation, changed comments,
and added a docstring — none of which were requested.

## The Wrong Diff
```diff
  def validate_user(user_data):
-     # Check email format
-     if not user_data.get('email'):
+     """Validate user data."""                    # added docstring
+     email = user_data.get('email', '').strip()
+     if not email:
          raise ValueError("Email required")
-     if '@' not in user_data['email']:
+     if '@' not in email or '.' not in email.split('@')[1]:  # improved validation
          raise ValueError("Invalid email")
-     # Check username
-     if not user_data.get('username'):
+     username = user_data.get('username', '').strip()  # added .strip()
+     if not username:
          raise ValueError("Username required")
+     if len(username) < 3:                        # new validation
+         raise ValueError("Username too short")
+     if not username.isalnum():                    # new validation
+         raise ValueError("Username must be alphanumeric")
      return True
```

## Why It's Wrong
- Changed comments (orthogonal to bug fix)
- Added docstring (not requested)
- Improved email validation beyond the specific bug
- Added username validation (completely unrelated)
- Makes the diff larger and harder to review

## Hard Rule
Every changed line must trace directly to the user's request.
If you notice improvements while fixing a bug, MENTION them in a comment —
don't implement them. The bug fix PR should contain ONLY the bug fix.
