"""
Pe: Perceive -- Filesystem Scanner (D-mode).

Discovers all classifiable files in a directory tree and extracts
observable metadata. Zero API calls. Pure filesystem operations.

Spec: ONT.CORE.KF_EXECUTION_MODES Section 3.1
"""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

from .. import ModuleOutput


@dataclass
class FileMetadata:
    """Observable properties of a single file."""
    path: str
    filename: str
    extension: str
    parent_dir: str
    parent_chain: str           # e.g., "contracts/archetypes"
    file_size_bytes: int = 0
    line_count: int = 0
    first_line: str = ""


# Default file extensions to scan
# Scan everything by default. The fingerprinter handles classification.
DEFAULT_EXTENSIONS = (
    ".md", ".txt", ".rst", ".html",
    ".json", ".yaml", ".yml", ".csv", ".tsv", ".xml", ".toml",
    ".py", ".js", ".ts", ".go", ".rs", ".java", ".sh", ".bash",
    ".env", ".ini", ".cfg", ".conf",
    ".dockerfile", ".makefile",
)

DEFAULT_EXCLUDES = ("__pycache__/", "node_modules/", ".git/", ".venv/", "venv/")


def extract_metadata(file_path: Path, domain_root: Path) -> FileMetadata:
    """Extract filesystem metadata for a single file."""
    try:
        rel = file_path.relative_to(domain_root)
        parent_chain = str(rel.parent).replace("\\", "/")
    except ValueError:
        parent_chain = str(file_path.parent).replace("\\", "/")

    first_line = ""
    line_count = 0
    try:
        with open(file_path, "r", encoding="utf-8", errors="replace") as f:
            first_line = f.readline().strip()
            line_count = 1 + sum(1 for _ in f)
    except Exception:
        pass

    return FileMetadata(
        path=str(file_path),
        filename=file_path.name,
        extension=file_path.suffix.lower(),
        parent_dir=file_path.parent.name,
        parent_chain=parent_chain,
        file_size_bytes=file_path.stat().st_size if file_path.exists() else 0,
        line_count=line_count,
        first_line=first_line,
    )


def execute(inputs: dict, config: dict) -> ModuleOutput:
    """Scan a directory and extract metadata for all classifiable files.

    Config:
        directory: str -- path to scan
        extensions: tuple[str, ...] -- file extensions to include
        excludes: tuple[str, ...] -- path patterns to skip
    """
    directory = Path(config["directory"])
    extensions = tuple(config.get("extensions", DEFAULT_EXTENSIONS))
    excludes = tuple(config.get("excludes", DEFAULT_EXCLUDES))

    files: list[FileMetadata] = []

    for f in sorted(directory.rglob("*")):
        if not f.is_file():
            continue
        if f.suffix.lower() not in extensions:
            continue
        rel = str(f.relative_to(directory)).replace("\\", "/")
        if any(pat in rel for pat in excludes):
            continue
        files.append(extract_metadata(f, directory))

    return ModuleOutput(
        data=files,
        confident=files,   # Pe never produces ambiguous items
        ambiguous=[],
        mode="D",
        stage="Pe",
        stats={
            "total_files": len(files),
            "directory": str(directory),
            "extensions": list(extensions),
        },
    )
