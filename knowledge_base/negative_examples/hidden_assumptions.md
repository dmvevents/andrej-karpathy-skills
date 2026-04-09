# NEVER: Silently Assume Scope, Format, or Fields

## Principle Violated
Think Before Coding — Don't assume. Surface tradeoffs.

## What Happened
LLM asked to "export user data" silently assumed ALL users, file output,
specific fields, and CSV column names — none of which were specified.

## The Wrong Code
```python
def export_users(format='json'):
    """Export all users to a file."""
    users = User.query.all()  # assumed ALL users
    
    if format == 'json':
        with open('users.json', 'w') as f:  # assumed file location
            json.dump([u.to_dict() for u in users], f)
    elif format == 'csv':
        with open('users.csv', 'w') as f:
            writer = csv.DictWriter(f, fieldnames=['id', 'email', 'name'])  # assumed fields
            writer.writeheader()
            writer.writerows([u.to_dict() for u in users])
    
    return f"Exported {len(users)} users"
```

## Why It's Wrong
- Privacy: exporting ALL users without asking about scope
- Security: assumed which fields to include (some might be sensitive)
- Architecture: assumed file-based output (could be API, stream, background job)
- Data model: assumed CSV fieldnames without checking actual schema

## Hard Rule
When a request has ambiguous scope, format, or field selection, STOP and enumerate
assumptions before writing code. Present alternatives, don't pick silently.
