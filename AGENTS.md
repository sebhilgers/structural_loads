# AGENTS

## Zweck
Dieses Repository entwickelt ein Python-Paket für die strukturierte Modellierung und Weiterleitung von Lasten in Tragwerken.

## Core development rules
- Work in very small, reviewable steps.
- Keep the domain explicit and engineering-oriented.
- Do not introduce abstractions unless a concrete use case exists.

## Domain separation rules
- `Action` classifies a load but is not itself a concrete load.
- `LoadCase` identifies the calculation case and must always be preserved.
- A concrete load object is the primary operational object.
- Do not mix classification, value storage, and transfer logic in one class.

## Load transfer rules
- Load transfer must always be explicit.
- Do not derive transfer paths automatically from geometry in V1.
- A transfer step may transform the load type, but only through an explicit rule.
- Preserve traceability of the load origin through all transfer steps.

## Summation rules
- Never sum loads from different load cases.
- Never sum incompatible load types implicitly.
- Never sum loads with different units or directions implicitly.
- Prefer returning separated results over hidden conversions.

## Scope restrictions for V1
- No load combinations
- No automatic geometry-based routing
- No code generation magic
- No complex inheritance trees
- No unnecessary dependencies