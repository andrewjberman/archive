"""
Pe: Corpus Aggregator (D-mode).

Produces corpus-level statistics from filesystem_scanner output.
Answers "what is the shape of this corpus?" before any interpretation.

Zero file reads -- operates entirely on FileMetadata from the scanner.
Informs pipeline selection, budget estimation, and complexity tier
classification.

GPT-convergent primitive: aggregate(results, operation)
KF mapping: Pe stage (perceive/), D-mode (always deterministic)

Spec: ONT.CORE.KF_EXECUTION_MODES Section 3.1
       ONT.CORE.PIPELINE_ARCHITECTURE Section 2.1
"""

from __future__ import annotations

from collections import Counter
from dataclasses import dataclass, field
from typing import Any

from .. import ModuleOutput


@dataclass
class CorpusProfile:
    """Aggregate statistics about a corpus."""
    total_files: int = 0
    total_lines: int = 0
    total_bytes: int = 0

    # Distribution by extension (.md, .py, .json, ...)
    extension_counts: dict[str, int] = field(default_factory=dict)

    # Distribution by directory (top-level grouping)
    directory_counts: dict[str, int] = field(default_factory=dict)

    # Distribution by file group (DOCUMENT, CODE, DATA, CONFIG, ASSET)
    group_counts: dict[str, int] = field(default_factory=dict)

    # Size statistics
    median_file_bytes: int = 0
    max_file_bytes: int = 0
    max_file_path: str = ""

    # Structural indicators
    deepest_path: str = ""
    deepest_depth: int = 0
    unique_directories: int = 0
    empty_files: int = 0

    # Top directories by file count
    top_directories: list[tuple[str, int]] = field(default_factory=list)

    # Top extensions by file count
    top_extensions: list[tuple[str, int]] = field(default_factory=list)


# Extension to group mapping (same as content_fingerprinter)
EXTENSION_GROUPS = {
    ".md": "DOCUMENT", ".txt": "DOCUMENT", ".rst": "DOCUMENT", ".html": "DOCUMENT",
    ".pdf": "DOCUMENT",
    ".json": "DATA", ".yaml": "DATA", ".yml": "DATA", ".csv": "DATA",
    ".tsv": "DATA", ".xml": "DATA", ".toml": "DATA",
    ".py": "CODE", ".js": "CODE", ".ts": "CODE", ".go": "CODE",
    ".rs": "CODE", ".java": "CODE", ".sh": "CODE", ".bash": "CODE",
    ".rb": "CODE", ".php": "CODE", ".c": "CODE", ".cpp": "CODE",
    ".h": "CODE", ".hpp": "CODE", ".cs": "CODE", ".sql": "CODE",
    ".env": "CONFIG", ".ini": "CONFIG", ".cfg": "CONFIG", ".conf": "CONFIG",
    ".dockerfile": "CONFIG", ".makefile": "CONFIG",
    ".png": "ASSET", ".jpg": "ASSET", ".gif": "ASSET", ".svg": "ASSET",
    ".zip": "ASSET", ".tar": "ASSET", ".gz": "ASSET", ".exe": "ASSET",
}


def aggregate(files: list, config: dict | None = None) -> CorpusProfile:
    """Build a corpus profile from FileMetadata list.

    This is the pure aggregation function. Can be called standalone
    or via the execute() module interface.
    """
    config = config or {}

    if not files:
        return CorpusProfile()

    ext_counter: Counter = Counter()
    dir_counter: Counter = Counter()
    group_counter: Counter = Counter()
    sizes: list[int] = []
    total_lines = 0

    max_bytes = 0
    max_path = ""
    deepest = 0
    deepest_path = ""
    empty = 0
    all_dirs: set[str] = set()

    for f in files:
        path = getattr(f, "path", "")
        ext = getattr(f, "extension", "")
        parent_chain = getattr(f, "parent_chain", "")
        size = getattr(f, "file_size_bytes", 0)
        lines = getattr(f, "line_count", 0)

        ext_counter[ext] += 1
        total_lines += lines
        sizes.append(size)

        # Top-level directory (first segment of parent_chain)
        top_dir = parent_chain.split("/")[0] if parent_chain and parent_chain != "." else "(root)"
        dir_counter[top_dir] += 1
        all_dirs.add(parent_chain)

        # Group
        group = EXTENSION_GROUPS.get(ext, "OTHER")
        group_counter[group] += 1

        # Track maximums
        if size > max_bytes:
            max_bytes = size
            max_path = path

        depth = parent_chain.count("/") + 1 if parent_chain and parent_chain != "." else 0
        if depth > deepest:
            deepest = depth
            deepest_path = parent_chain

        if size == 0:
            empty += 1

    # Median
    sorted_sizes = sorted(sizes)
    median = sorted_sizes[len(sorted_sizes) // 2] if sorted_sizes else 0

    return CorpusProfile(
        total_files=len(files),
        total_lines=total_lines,
        total_bytes=sum(sizes),
        extension_counts=dict(ext_counter),
        directory_counts=dict(dir_counter),
        group_counts=dict(group_counter),
        median_file_bytes=median,
        max_file_bytes=max_bytes,
        max_file_path=max_path,
        deepest_path=deepest_path,
        deepest_depth=deepest,
        unique_directories=len(all_dirs),
        empty_files=empty,
        top_directories=dir_counter.most_common(10),
        top_extensions=ext_counter.most_common(10),
    )


def execute(inputs: dict, config: dict) -> ModuleOutput:
    """Aggregate corpus statistics from filesystem scanner output.

    Inputs:
        pe_output: list[FileMetadata] -- from filesystem_scanner

    Config:
        (none required -- operates on scanner output)

    Returns ModuleOutput with CorpusProfile as data.
    """
    files = inputs.get("pe_output", [])
    profile = aggregate(files, config)

    return ModuleOutput(
        data=profile,
        confident=[profile],
        ambiguous=[],
        mode="D",
        stage="Pe",
        stats={
            "total_files": profile.total_files,
            "total_lines": profile.total_lines,
            "total_bytes": profile.total_bytes,
            "groups": dict(profile.group_counts),
            "top_extensions": profile.top_extensions[:5],
            "unique_directories": profile.unique_directories,
            "deepest_depth": profile.deepest_depth,
        },
    )
