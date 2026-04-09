# Pattern: Match Existing Code Style Exactly

## Principle
Surgical Changes — Match existing style, even if you'd do it differently.

## When to Use
When adding a feature to an existing codebase.

## The Pattern
```diff
+ import logging
+ 
+ logger = logging.getLogger(__name__)
+ 
  def upload_file(file_path, destination):
+     logger.info(f'Starting upload: {file_path}')
      try:
          with open(file_path, 'rb') as f:
              data = f.read()
          
          response = requests.post(destination, files={'file': data})
          
          if response.status_code == 200:
+             logger.info(f'Upload successful: {file_path}')
              return True
          else:
+             logger.error(f'Upload failed: status={response.status_code}')
              return False
      except Exception as e:
-         print(f"Error: {e}")
+         logger.exception(f'Upload error: {file_path}')
          return False
```

## Why It Works
- Single quotes match existing style (file used single quotes)
- No type hints added (existing function has none)
- No docstring added (existing function has none)
- Boolean return pattern preserved (if/else, not variable assignment)
- Spacing matches exactly
- Only the print→logger change and new log lines appear in diff

## Checklist
Before submitting, verify:
- [ ] Quote style matches existing file
- [ ] Type annotation style matches existing file
- [ ] Whitespace/indentation matches
- [ ] Boolean/return patterns match
- [ ] No cosmetic changes snuck in
