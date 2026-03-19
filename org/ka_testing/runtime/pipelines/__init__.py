"""
Pipelines -- archetype-scoped compositions of KF stage modules.

Each pipeline directory maps to a value chain archetype:
  ingestion/       <- supplier workers
  transformation/  <- transformer workers
  assembly/        <- compositor workers
  validation/      <- operator workers

Pipelines compose modules from ../modules/ (Pe, In, Ev, De, Ac, Ad).
The archetype enforcer grants access to the pipeline directory matching
the worker's archetype.
"""
