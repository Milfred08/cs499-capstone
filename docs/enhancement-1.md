---
title: "Enhancement 1 — Software Design & Engineering"
---

# Enhancement 1 — Software Design & Engineering

**Artifact:** Refactor of CS-340 PyMongo CRUD module → `AnimalShelter_enhanced.py`  
**Goal:** Turn a single-file script into a safe, reusable repository layer.

## Why I selected this artifact
Briefly state that it represents production CRUD patterns and is the base for the capstone.

## Before → After (summary)
- Before: minimal CRUD, weak validation, risk of mass delete, inconsistent returns.
- After: repository pattern, env-based config, input validation, guarded delete/update,
  normalized IDs, index helpers, consistent `{ok, data|error}`, basic logging.

## Skills demonstrated (map to outcomes)
- **CO2/CO4:** software architecture, clean API design, unit tests.
- **CO5:** security-minded defaults (guards, validation), audit scaffolding.




_Last updated: {{ site.time | date: "%Y-%m-%d" }}_


