"""Ac: Act -- Produce output artifacts deterministically.

Always D-mode. Key generation, registry writing, catalog assembly.
"""

from .key_generator import execute as generate_keys
from .registry_writer import execute as write_registry

__all__ = ["generate_keys", "write_registry"]
