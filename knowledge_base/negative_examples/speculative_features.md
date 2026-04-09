# NEVER: Add Features Nobody Asked For

## Principle Violated
Simplicity First — No features beyond what was asked.

## What Happened
LLM asked to "save user preferences to database" added caching, validation,
merge strategy, notification system — none of which were requested.

## The Wrong Code
```python
class PreferenceManager:
    def __init__(self, db, cache=None, validator=None):
        self.db = db
        self.cache = cache or InMemoryCache()
        self.validator = validator or DefaultValidator()
    
    def save(self, user_id: int, prefs: dict, 
             merge: bool = True, 
             validate: bool = True,
             notify: bool = False) -> bool:
        if validate:
            errors = self.validator.validate(prefs)
            if errors:
                raise ValidationError(errors)
        existing = self.get(user_id) if merge else {}
        if merge:
            existing.update(prefs)
            prefs = existing
        self.db.execute(
            "UPDATE users SET preferences = ? WHERE id = ?",
            (json.dumps(prefs), user_id)
        )
        if self.cache:
            self.cache.set(f"prefs:{user_id}", prefs)
        if notify:
            self.notify_preference_change(user_id, prefs)
        return True
```

## Why It's Wrong
- Cache: no evidence of performance problem requiring caching
- Validation: no schema defined, no bad data reported
- Merge: no requirement for merging vs overwriting
- Notifications: completely invented requirement
- 5 parameters where 3 would do

## Hard Rule
The function should do exactly what was asked: save preferences to DB.
Add caching when performance matters, validation when bad data appears,
merging when the requirement emerges. Not before.
