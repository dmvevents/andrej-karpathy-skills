# NEVER: Change Code Style While Adding a Feature

## Principle Violated
Surgical Changes — Match existing style.

## What Happened
LLM asked to "add logging to the upload function" also changed quote style
('' to ""), added type hints, added a docstring, reformatted whitespace,
and changed boolean return logic.

## The Wrong Diff
```diff
- def upload_file(file_path, destination):
+ def upload_file(file_path: str, destination: str) -> bool:  # added type hints
+     """Upload file to destination with logging."""            # added docstring
+     logger.info(f"Uploading {file_path} to {destination}")
      try:
-         with open(file_path, 'rb') as f:
+         with open(file_path, "rb") as f:      # changed quote style
              data = f.read()
-         response = requests.post(destination, files={'file': data})
-         if response.status_code == 200:
-             return True
-         else:
-             return False
+         response = requests.post(destination, files={"file": data})  # quote style
+         success = response.status_code == 200   # changed boolean pattern
+         if success:
+             logger.info(f"Upload successful: {file_path}")
+         else:
+             logger.error(f"Upload failed: status={response.status_code}")
+         return success
      except Exception as e:
-         print(f"Error: {e}")
+         logger.exception(f"Upload error for {file_path}: {e}")
          return False
```

## Why It's Wrong
- Quote style change: cosmetic, not requested
- Type hints: not in the existing codebase style
- Docstring: not requested
- Boolean refactor: changes behavior pattern unnecessarily
- Makes the diff 3x larger than necessary

## Hard Rule
Match existing style exactly. Use single quotes if the file uses single quotes.
Don't add type hints unless the codebase uses them. Only change lines that
implement the requested feature.
