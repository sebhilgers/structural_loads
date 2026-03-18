# PROJECT_CONTEXT

## Project
structural_loads

## Goal
Build a Python package for defining, generating, assigning, transferring, and summarizing structural loads in simple structural models.

## Main concepts
The project distinguishes clearly between:
1. classification objects:
   - Action
   - LoadCase
   - LoadGroup
2. concrete mechanical loads:
   - AreaLoad
   - LineLoad
   - PointLoad
3. structural elements:
   - Slab
   - Wall
   - Node
4. transfer objects:
   - LoadPath
   - LoadTransferStep

## V1 scope
Version 1 shall support:
- definition of actions and load cases
- definition of area, line, and point loads
- explicit assignment of loads to structural elements
- explicit transfer of loads along predefined paths
- strict separation by load case
- per-load-case summaries at target nodes

## Explicit assumptions
- Transfer paths are user-defined, not geometry-derived.
- Load transformations are explicit.
- Traceability of each load must be preserved.
- Summation is only allowed for compatible loads.

## Out of scope for V1
- load combinations
- automatic routing from geometry
- design code checks
- FE analysis
- complex 3D modeling