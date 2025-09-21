#  (Enhanced) Script for — CS-499 Capstone

Repository layer for a MongoDB collection used in my CS-499 capstone (**VoiceNote MD**) and derived from my CS-340 CRUD artifact.  
This enhanced version focuses on **software design and engineering quality**: clear contracts, validation, safe delete, structured logging, environment-based configuration, and basic observability.

> **Why this repo exists:** keep data access logic small, testable, and safe so it can be reused by a simple web API in the capstone.

---

## Key Features (Enhancement One)

- **Consistent return envelopes** from CRUD methods (`{"ok": bool, ...}`).
- **Input validation** helpers for required fields and payload types.
- **Defensive delete**: refuses empty filters unless explicitly confirmed.
- **Structured logging** via the `logging` module (no `print` statements).
- **Environment configuration** (`MONGO_URI`), no secrets in code.
- **Light observability**: `_audit(action, target_id, meta)` helper and `_ensure_indexes()` for common indexes (ids/timestamps).
- **Docstrings & type hints** for maintainability.

---

## Quick Start

### 1) Requirements
- Python 3.10+  
- MongoDB Atlas or local MongoDB  
- `pip install pymongo python-dotenv` (and `pytest` if you will run the tests)

### 2) Environment variable
Create a `.env` file (or set the variable in your shell):

```bash
# .env (example)
MONGO_URI=mongodb://localhost:27017
