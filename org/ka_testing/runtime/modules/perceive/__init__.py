"""Pe: Perceive -- Discover what exists. Extract observable properties.

Always D-mode. Never escalates to I-mode.
"""

from .filesystem_scanner import execute, FileMetadata

__all__ = ["execute", "FileMetadata"]
