# Professional Self-Assessment

**Milfred Martinez Diaz**

## Introduction

This ePortfolio represents what I can do as a computer science professional. During CS-499, I refined earlier coursework and focused on building reliable, secure, and testable software. I worked on three areas: software design and engineering, algorithms and data structures, and databases. I also created a complete code review and used the feedback to improve quality. My goal was simple: show practical skills that are ready for work.

## Career Goals

I live in Orlando, Florida and work as a Systems Analyst. My next step is a role where I design and build secure backend services and data workflows—ideally in healthcare or another data-sensitive field. Long term, I want to lead small engineering teams and own services from design to deployment. I enjoy solving problems with clear code, clean interfaces, and measurable results.

## Professional Identity and Strengths

I write software that is easy to understand and easy to maintain. I prefer small, well-named functions, defensive validation, and tests that run fast. I design simple APIs with clear request/response models. I use logging, environment-based configuration, and safe defaults. Security is part of my design, not an afterthought. I am comfortable explaining decisions to non-engineers with diagrams, short notes, and examples.

## Evidence of Program Outcomes

### 1) Build collaborative environments and support organizational decisions

**What I did:** I performed a formal code review on my prior artifact and documented findings: missing input checks, unclear naming, weak error handling, and lack of tests. I created an improvement backlog and tracked changes in Git commits.

**Why it matters:** Code review is collaboration. It builds shared standards and makes decisions visible. My issue list gave a clear plan for the work and helped me communicate progress.

### 2) Professional-quality communication (oral, written, and visual)

**What I did:** I published a structured ePortfolio with short narratives, before/after code snippets, and quick visuals (test output, logs, and timing numbers). I also recorded the code review as a guided walkthrough.

**Why it matters:** The content is short and direct. A hiring manager or teammate can scan the page and understand the reason for each change and the result. This is what real projects need—clear, honest communication.

### 3) Design and evaluate solutions using algorithms and CS standards

**What I did:** I implemented an NLP pipeline to convert free-text clinical notes into a structured SOAP object. I used tokenization, rule-based classification, simple entity extraction, and composition into S/O/A/P sections. I measured latency and used small accuracy checks (edit distance and section coverage).

**Why it matters:** The solution shows algorithmic thinking and tradeoffs. I avoided heavy ML to keep the pipeline transparent, fast, and testable. The result is practical and can be improved later with learned models.

### 4) Use well-founded techniques and tools to deliver value

**What I did:** I refactored a MongoDB CRUD repository into a small, layered service with validation, structured errors, and unit tests (pytest). I added environment variables for configuration and simple observability through logging.

**Why it matters:** The repository is now safer and easier to reuse in a web API. Design choices match common backend practices (FastAPI-style layers, DTOs, RBAC hooks). Tests prove behavior, not just syntax.

### 5) Apply a security mindset to protect data and systems

**What I did:** For the database enhancement, I introduced field-level validation, unique indexes, audit logging, and example PHI masking at the presentation layer. I also grouped queries into safe repository methods to reduce injection risks and added a place for role checks.

**Why it matters:** Security is built in from the start: least privilege, input validation, safe query patterns, and audit trails. These practices reduce the chance of data leaks and help with compliance.

## What I Learned

- Small changes add up. Good names, pure functions, and simple data models make code easier to test and reason about.
- Tests drive clarity. Writing tests forced me to define real behavior: what is valid, what fails, and what we return.
- Evidence beats opinion. Timing numbers, test output, and logs make a stronger case than long paragraphs.
- Security is design. Index choices, data models, and boundaries affect risk as much as any library.

## Challenges and How I Addressed Them

**Balancing features and scope:** I kept the NLP pipeline rule-based to ship a working, testable solution. I documented how to extend it later with statistical models.

**Legacy code clean-up:** I handled refactoring in steps—first validation and return contracts, then error handling, then tests—so I could keep progress visible and reduce risk.

**Database correctness:** I used indexes and uniqueness rules to push data quality into the database. This prevents entire classes of bugs at runtime.

## Ethical Practice and Data Privacy

The portfolio uses only synthetic or public sample data. I treat personal data as a liability that must be protected. I added PHI masking patterns, audit records, and safe defaults. I believe engineers have a duty to make privacy the default, not an optional feature.

## Growth Plan (Next 6–12 Months)

- Add JWT-based RBAC and request-scoped audit context to the service.
- Expand tests: property-based tests for the NLP parser and integration tests for the database layer.
- Introduce CI (GitHub Actions) for linting, tests, and type checks.
- Package the service with Docker and add minimal deployment docs.
- Explore a lightweight ML model to improve entity extraction accuracy while keeping latency under control.

## Conclusion

This ePortfolio shows consistent habits: clear structure, security by design, and practical testing. I focused on work that a team can trust—defensive inputs, safe data access, and results that are easy to explain. I am ready to contribute as a backend and data-focused engineer, especially in environments where correctness and privacy matter.
