"""Ad: Adapt -- Validate output and learn from results.

Hybrid: D-mode structural validation (100% coverage) +
I-mode semantic spot-check (10% sample).
"""

from .structural_validator import execute as validate_structural

__all__ = ["validate_structural"]
