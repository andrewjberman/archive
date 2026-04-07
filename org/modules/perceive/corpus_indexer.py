"""
Pe: Corpus Indexer (D-mode).

Builds a tantivy inverted index over file contents. First call indexes
the corpus. Subsequent calls query the index in milliseconds.

The index lives at {directory}/.corpus_index/. It persists across runs.
If files change, call reindex() or delete the index directory.

Usage:
    idx = CorpusIndex("path/to/corpus")
    idx.build()                              # ~1s for 500 files
    results = idx.search("position_cube")    # <5ms
    results = idx.search("rebalance", top_k=20)
"""

from __future__ import annotations

import hashlib
import shutil
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

from .. import ModuleOutput

INDEX_DIR_NAME = ".corpus_index"
MANIFEST_NAME = "manifest.txt"

# Extensions worth indexing (text-readable)
INDEXABLE_EXTENSIONS = frozenset({
    ".md", ".txt", ".rst", ".html",
    ".json", ".yaml", ".yml", ".csv", ".tsv", ".xml", ".toml",
    ".py", ".js", ".ts", ".go", ".rs", ".java", ".sh", ".bash",
    ".rb", ".php", ".c", ".cpp", ".h", ".hpp", ".cs",
    ".env", ".ini", ".cfg", ".conf",
    ".sql", ".graphql",
})

# Skip these directories
SKIP_DIRS = frozenset({
    "__pycache__", "node_modules", ".git", ".venv", "venv",
    ".corpus_index", ".baseline",
})


@dataclass
class SearchHit:
    path: str
    filename: str
    score: float
    snippet: str = ""


class CorpusIndex:
    """Persistent inverted index over a directory of text files."""

    def __init__(self, directory: str | Path):
        self.directory = Path(directory)
        self.index_dir = self.directory / INDEX_DIR_NAME
        self._index = None
        self._schema = None

    @property
    def exists(self) -> bool:
        return (self.index_dir / "meta.json").exists()

    def build(self, force: bool = False) -> dict[str, Any]:
        """Index all text files in the directory. Returns stats."""
        import tantivy

        if self.exists and not force:
            self._open()
            return {"status": "already_indexed", "path": str(self.index_dir)}

        # Clean and create
        if self.index_dir.exists():
            shutil.rmtree(self.index_dir)
        self.index_dir.mkdir(parents=True)

        # Build schema
        builder = tantivy.SchemaBuilder()
        builder.add_text_field("path", stored=True)
        builder.add_text_field("filename", stored=True)
        builder.add_text_field("extension", stored=True)
        builder.add_text_field("body", stored=True)
        self._schema = builder.build()

        self._index = tantivy.Index(self._schema, path=str(self.index_dir))
        writer = self._index.writer()

        indexed = 0
        skipped = 0
        errors = 0

        for f in sorted(self.directory.rglob("*")):
            if not f.is_file():
                continue
            # Skip excluded dirs
            if any(p in SKIP_DIRS for p in f.parts):
                continue
            if f.suffix.lower() not in INDEXABLE_EXTENSIONS:
                skipped += 1
                continue
            try:
                content = f.read_text(encoding="utf-8", errors="replace")
                # Cap file size to avoid bloating the index
                if len(content) > 500_000:
                    content = content[:500_000]
                writer.add_document(tantivy.Document(
                    path=str(f),
                    filename=f.name,
                    extension=f.suffix.lower(),
                    body=content,
                ))
                indexed += 1
            except Exception:
                errors += 1

        writer.commit()
        self._index.reload()

        return {
            "status": "indexed",
            "indexed": indexed,
            "skipped": skipped,
            "errors": errors,
            "path": str(self.index_dir),
        }

    def _open(self):
        """Open existing index."""
        if self._index is not None:
            return
        import tantivy

        builder = tantivy.SchemaBuilder()
        builder.add_text_field("path", stored=True)
        builder.add_text_field("filename", stored=True)
        builder.add_text_field("extension", stored=True)
        builder.add_text_field("body", stored=True)
        self._schema = builder.build()
        self._index = tantivy.Index(self._schema, path=str(self.index_dir))
        self._index.reload()

    def search(self, query: str, top_k: int = 10, fields: list[str] | None = None) -> list[SearchHit]:
        """Search the index. Returns ranked results."""
        if not self.exists:
            return []

        self._open()
        searcher = self._index.searcher()
        search_fields = fields or ["body", "filename", "path"]
        parsed = self._index.parse_query(query, search_fields)
        results = searcher.search(parsed, top_k)

        hits = []
        for score, addr in results.hits:
            doc = searcher.doc(addr)
            try:
                path = doc["path"][0]
            except (KeyError, IndexError):
                path = ""
            try:
                filename = doc["filename"][0]
            except (KeyError, IndexError):
                filename = ""
            try:
                body = doc["body"][0]
            except (KeyError, IndexError):
                body = ""

            snippet = _extract_snippet(body, query.split(), max_len=200)

            hits.append(SearchHit(
                path=path,
                filename=filename,
                score=round(score, 3),
                snippet=snippet,
            ))

        return hits

    def reindex(self) -> dict[str, Any]:
        """Force rebuild the index."""
        return self.build(force=True)

    def file_count(self) -> int:
        """How many documents are in the index."""
        if not self.exists:
            return 0
        self._open()
        searcher = self._index.searcher()
        return searcher.num_docs


def _extract_snippet(body: str, terms: list[str], max_len: int = 200) -> str:
    """Extract a snippet around the first occurrence of any search term."""
    body_lower = body.lower()
    best_pos = len(body)
    for term in terms:
        pos = body_lower.find(term.lower())
        if 0 <= pos < best_pos:
            best_pos = pos

    if best_pos >= len(body):
        return body[:max_len].strip()

    start = max(0, best_pos - 50)
    end = min(len(body), best_pos + max_len - 50)
    snippet = body[start:end].strip()
    if start > 0:
        snippet = "..." + snippet
    if end < len(body):
        snippet = snippet + "..."
    return snippet


# ---------------------------------------------------------------------------
# Additional primitives: read, count, extract
# ---------------------------------------------------------------------------

def read_chunk(file_path: str | Path, start: int = 0, length: int = 200) -> str:
    """Read a bounded chunk of a file. Lines, not bytes.

    Prevents reading whole documents when you only need context around
    a specific location.
    """
    p = Path(file_path)
    if not p.exists():
        return ""
    try:
        lines = p.read_text(encoding="utf-8", errors="replace").split("\n")
        end = min(start + length, len(lines))
        return "\n".join(lines[start:end])
    except Exception:
        return ""


def count_pattern(pattern: str, directory: str | Path, use_index: bool = True) -> dict[str, int]:
    """Count occurrences of a pattern across files. Returns {path: count}.

    If an index exists, searches the index first to narrow files,
    then counts exact matches in those files only.
    If no index, falls back to scanning all files (slower).
    """
    import re
    directory = Path(directory)
    results: dict[str, int] = {}
    regex = re.compile(pattern, re.IGNORECASE)

    if use_index:
        idx = CorpusIndex(directory)
        if idx.exists:
            # Use index to find candidate files
            hits = idx.search(pattern.replace("\\b", "").replace("\\", ""), top_k=100)
            for hit in hits:
                try:
                    content = Path(hit.path).read_text(encoding="utf-8", errors="replace")
                    n = len(regex.findall(content))
                    if n > 0:
                        results[hit.path] = n
                except Exception:
                    pass
            return results

    # Fallback: scan all files
    for f in sorted(directory.rglob("*")):
        if not f.is_file() or f.suffix.lower() not in INDEXABLE_EXTENSIONS:
            continue
        if any(p in SKIP_DIRS for p in f.parts):
            continue
        try:
            content = f.read_text(encoding="utf-8", errors="replace")
            n = len(regex.findall(content))
            if n > 0:
                results[str(f)] = n
        except Exception:
            pass
    return results


def extract_pattern(pattern: str, file_path: str | Path) -> list[dict[str, Any]]:
    """Extract all regex matches from a file with line numbers.

    Returns [{match, line, start, end}, ...]
    """
    import re
    p = Path(file_path)
    if not p.exists():
        return []

    results = []
    regex = re.compile(pattern)
    try:
        lines = p.read_text(encoding="utf-8", errors="replace").split("\n")
        for line_num, line in enumerate(lines, 1):
            for m in regex.finditer(line):
                results.append({
                    "match": m.group(),
                    "line": line_num,
                    "start": m.start(),
                    "end": m.end(),
                    "context": line.strip(),
                })
    except Exception:
        pass
    return results


# ---------------------------------------------------------------------------
# Module interface
# ---------------------------------------------------------------------------

def execute(inputs: dict, config: dict) -> ModuleOutput:
    """Build or query a corpus index.

    Config:
        directory: str -- path to index
        action: "build" | "search" | "reindex" (default: "build")
        query: str -- search query (required if action=search)
        top_k: int -- max results (default: 10)
    """
    directory = config.get("directory", ".")
    action = config.get("action", "build")
    idx = CorpusIndex(directory)

    if action == "search":
        query = config.get("query", "")
        top_k = config.get("top_k", 10)
        if not query:
            return ModuleOutput(data=[], mode="D", stage="Pe",
                                stats={"error": "no query provided"})
        hits = idx.search(query, top_k)
        return ModuleOutput(
            data=hits, confident=hits, mode="D", stage="Pe",
            stats={"query": query, "hits": len(hits), "top_k": top_k},
        )

    # Build or reindex
    stats = idx.build(force=(action == "reindex"))
    return ModuleOutput(
        data=stats, confident=[], mode="D", stage="Pe",
        stats=stats,
    )
