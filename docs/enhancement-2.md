---
title: "Enhancement 2 — Algorithms & Data Structures"
layout: default
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

## Evidence
- Tests: `test_nlp_soap_enhanced.py` (correctness, performance, concurrency).
- Demo/benchmark script or instructions to reproduce results.
- Brief table of complexity/perf results (from your narrative).

## Links
- Source: `nlp_soap.py` (link)  
- Tests: <link>  
- Narrative (PDF/DOCX): <link> (optional)

_Last updated: {{ site.time | date: "%Y-%m-%d" }}_
