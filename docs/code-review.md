# Milestone 1 — Code Review (CS-499)

**Student:** Milfred Martinez Diaz  
**Artifact Reviewed:** `AnimalShelter.py` (CS-340 CRUD module for the Austin Animal Center database)  
**Review Date:** September 9, 2025  

**Links:**  
- **Code Review As Video:** https://1drv.ms/v/c/cc08d443ea47a64f/EannJoT6JnNPmkLsgG5TGhcBvjQLBDt4u0kdmFK7LkOZXg
- **Original code (sanitized copy):** https://github.com/Milfred08/cs499-capstone/tree/main/Artififact/cs340-animalshelter/original  
- **Enhanced drop-in:** https://github.com/Milfred08/cs499-capstone/blob/main/Artififact/cs340-animalshelter/enhanced/AnimalShelter_enhanced.py  
- **Issue backlog:** https://github.com/Milfred08/cs499-capstone/issues  


---

## 1) Existing Functionality

- Connects to **MongoDB** and pings the server on start.  
- Provides **CRUD** methods: `create`, `read`, `update`, `delete`.  
- Uses the **animals** collection in the **AAC** database.  
- Accepts Python dictionaries as inputs and returns MongoDB results.

**Value:** This is a clean starting point for refactoring into a small, secure service that supports my capstone goals.

---

## 2) Code Analysis

### Strengths
- Clear separation of CRUD actions in one class.  
- Basic input checks (required fields in `create`).  
- Connection reliability using `admin.command("ping")` with a timeout.  
- Readable Python that is easy to maintain.

### Issues & Risks (prioritized)

| ID | Severity | Issue | Why it matters | Fix Plan |
|---|---|---|---|---|
| P0-S1 | **High – Security** | Secrets/connection details in code | Risk of credential leaks; hard to rotate | Use `MONGO_URI` env var; provide `.env.example`; never commit real `.env` |
| P0-S2 | **High – Design/API** | Inconsistent returns + `print` in data layer | Hard to test/integrate | Standardize return shapes; raise typed exceptions; use `logging` |
| P1-R1 | **Med – Reliability** | No structured logging or UTC timestamps | Debugging and tracing are difficult | Add `logging` with UTC timestamps; request IDs later |
| P1-R2 | **Med – Safety** | Delete can remove many docs | Accidental wipes | Guard against empty query unless `confirm_delete=False` |
| P1-V1 | **Med – Validation** | Rules spread through code | Risk of inconsistent checks | Centralize validation; later move to pydantic |
| P1-I1 | **Med – Performance** | Helpful indexes missing | Slow queries/sorts | Index `animal_id`, `created_timestamp`, `last_modified_timestamp` |
| P2-M1 | **Low – Maintainability** | Single-file coupling | Hard to extend to web API/NLP | Prepare repository/service split in next milestone |

---

## 3) Planned Enhancements (Milestones 2–4)

**Design & Engineering (M2)**  
- Env-based config (`MONGO_URI`), structured logging, UTC timestamps.  
- Standardized returns for CRUD, typed exceptions, safe-delete guard.  
- Minimal **audit** collection to record CREATE/UPDATE/DELETE.  
- Prepare for FastAPI wrapper (routes → services → repository).

**Algorithms & Data Structures (M3)**  
- Lightweight **NLP pipeline** to draft **SOAP** sections from text: preprocess → sentence split → rule-based classification (dicts/sets) → regex entity extraction.  
- Complexity target **O(n)**; track **latency** and **edit-distance** metrics.

**Databases (M4)**  
- Add indexes; example aggregations (weekly activity, CRUD counts).  
- Store audit events; demonstrate PHI masking on sample strings.

---

## 4) Before → After Examples

**Secrets out of code**
```py
# Before
client = MongoClient("mongodb://user:pass@host:27017/")

# After
import os
uri = os.getenv("MONGO_URI", "mongodb://localhost:27017/")
client = MongoClient(uri, serverSelectionTimeoutMS=5000)

