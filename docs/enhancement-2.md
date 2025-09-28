---
title: "Enhancement 2 — Algorithms & Data Structures"
---

# Enhancement 2 — Algorithms & Data Structures

**Artifact:** `nlp_soap.py` — rule-based + data-structure driven SOAP classifier (tries, maps, caching).  
**Goal:** Convert free text into structured SOAP sections efficiently.

## What I changed and why
- Implemented trie + hash map lexicons, priority queue for cues.
- Hybrid classifier; thread-safe LRU cache to cut repeated work.
- Complexity documented; benchmarks against a baseline.

## Skills demonstrated (map to outcomes)
- **CO3/CO4:** algorithm selection, complexity analysis, performance tests.
- **CO5:** thread safety for shared cache; input handling.


_Last updated: {{ site.time | date: "%Y-%m-%d" }}_


