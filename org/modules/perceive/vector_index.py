"""
Pe: Vector Index (D-mode).

Builds and queries a dense vector index over file contents.
Enables semantic similarity search as a reusable module primitive.

The index lives at {directory}/.vector_index/. It persists across runs.
Build is expensive (requires embeddings); queries are <10ms.

GPT-convergent primitive: nearest(vector, k)
KF mapping: Pe stage (perceive/), D-mode (index build + query are
            deterministic given the same model and inputs)

Dependencies:
    - sentence-transformers (for embedding generation)
    - numpy (for vector operations)

Graceful degradation: if dependencies are missing, execute() returns
an empty ModuleOutput with an error in stats. No crash. Pipelines
that don't need vector search are unaffected.

Spec: ONT.CORE.KF_EXECUTION_MODES Section 3.1
       ONT.CORE.PIPELINE_ARCHITECTURE Section 2.1
       ONT.CORE.CONTEXT_SEEDING (Signal B vector retrieval)
"""

from __future__ import annotations

import json
import shutil
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

from .. import ModuleOutput

INDEX_DIR_NAME = ".vector_index"
MANIFEST_NAME = "manifest.json"

# Same skip/include as corpus_indexer
INDEXABLE_EXTENSIONS = frozenset({
    ".md", ".txt", ".rst", ".html",
    ".json", ".yaml", ".yml", ".csv", ".xml", ".toml",
    ".py", ".js", ".ts", ".go", ".rs", ".java", ".sh", ".bash",
    ".rb", ".php", ".c", ".cpp", ".h", ".hpp", ".cs",
    ".env", ".ini", ".cfg", ".conf",
    ".sql", ".graphql",
})

SKIP_DIRS = frozenset({
    "__pycache__", "node_modules", ".git", ".venv", "venv",
    ".corpus_index", ".vector_index", ".baseline",
})

# Default embedding model — small, fast, good for code + docs
DEFAULT_MODEL = "all-MiniLM-L6-v2"


@dataclass
class VectorHit:
    """Single result from a vector similarity search."""
    path: str
    filename: str
    similarity: float
    chunk_start: int = 0
    chunk_text: str = ""


class VectorIndex:
    """Persistent dense vector index over a directory of text files.

    Build: reads files, chunks them, embeds with sentence-transformers,
           stores embeddings + metadata as numpy arrays + JSON.
    Query: embeds query, computes cosine similarity, returns top-k.

    No external vector DB required (no FAISS, no Qdrant). Pure numpy
    for simplicity and zero extra dependencies beyond sentence-transformers.
    For corpora under 100K chunks, numpy cosine similarity is <10ms.
    """

    def __init__(self, directory: str | Path, model_name: str = DEFAULT_MODEL):
        self.directory = Path(directory)
        self.index_dir = self.directory / INDEX_DIR_NAME
        self.model_name = model_name
        self._model = None
        self._embeddings = None    # numpy array (N, D)
        self._metadata: list[dict] = []  # [{path, filename, chunk_start, chunk_text}, ...]

    @property
    def exists(self) -> bool:
        return (self.index_dir / MANIFEST_NAME).exists()

    def _load_model(self):
        if self._model is not None:
            return
        from sentence_transformers import SentenceTransformer
        self._model = SentenceTransformer(self.model_name)

    def build(self, force: bool = False, chunk_size: int = 512) -> dict[str, Any]:
        """Index all text files. Chunks files and embeds each chunk.

        Args:
            force: Rebuild even if index exists.
            chunk_size: Characters per chunk. Files larger than this
                        are split into multiple chunks.

        Returns stats dict.
        """
        import numpy as np

        if self.exists and not force:
            self._load_from_disk()
            return {"status": "already_indexed", "chunks": len(self._metadata)}

        self._load_model()

        if self.index_dir.exists():
            shutil.rmtree(self.index_dir)
        self.index_dir.mkdir(parents=True)

        chunks: list[str] = []
        metadata: list[dict] = []
        indexed_files = 0
        skipped = 0

        for f in sorted(self.directory.rglob("*")):
            if not f.is_file():
                continue
            if any(p in SKIP_DIRS for p in f.parts):
                continue
            if f.suffix.lower() not in INDEXABLE_EXTENSIONS:
                skipped += 1
                continue

            try:
                content = f.read_text(encoding="utf-8", errors="replace")
            except Exception:
                skipped += 1
                continue

            # Cap total content
            if len(content) > 200_000:
                content = content[:200_000]

            # Chunk
            file_chunks = _chunk_text(content, chunk_size)
            for i, chunk in enumerate(file_chunks):
                if not chunk.strip():
                    continue
                chunks.append(chunk)
                metadata.append({
                    "path": str(f),
                    "filename": f.name,
                    "chunk_start": i * chunk_size,
                    "chunk_text": chunk[:200],  # Store truncated for display
                })

            indexed_files += 1

        if not chunks:
            return {"status": "empty", "chunks": 0, "files": 0}

        # Embed all chunks
        embeddings = self._model.encode(
            chunks,
            show_progress_bar=False,
            batch_size=64,
            normalize_embeddings=True,
        )
        embeddings = np.array(embeddings, dtype=np.float32)

        # Save to disk
        np.save(str(self.index_dir / "embeddings.npy"), embeddings)
        with open(self.index_dir / "metadata.json", "w", encoding="utf-8") as mf:
            json.dump(metadata, mf)
        with open(self.index_dir / MANIFEST_NAME, "w", encoding="utf-8") as mf:
            json.dump({
                "model": self.model_name,
                "chunks": len(chunks),
                "files": indexed_files,
                "embedding_dim": int(embeddings.shape[1]),
            }, mf)

        self._embeddings = embeddings
        self._metadata = metadata

        return {
            "status": "indexed",
            "chunks": len(chunks),
            "files": indexed_files,
            "skipped": skipped,
            "embedding_dim": int(embeddings.shape[1]),
        }

    def _load_from_disk(self):
        """Load persisted index."""
        if self._embeddings is not None:
            return
        import numpy as np
        self._embeddings = np.load(str(self.index_dir / "embeddings.npy"))
        with open(self.index_dir / "metadata.json", "r", encoding="utf-8") as f:
            self._metadata = json.load(f)

    def search(self, query: str, top_k: int = 10) -> list[VectorHit]:
        """Semantic search. Embeds query and returns top-k similar chunks."""
        import numpy as np

        if not self.exists:
            return []

        self._load_model()
        self._load_from_disk()

        if self._embeddings is None or len(self._embeddings) == 0:
            return []

        # Embed query
        q_vec = self._model.encode(
            [query],
            show_progress_bar=False,
            normalize_embeddings=True,
        )
        q_vec = np.array(q_vec, dtype=np.float32)

        # Cosine similarity (embeddings are already normalized)
        scores = (self._embeddings @ q_vec.T).flatten()

        # Top-k
        if len(scores) < top_k:
            top_indices = np.argsort(-scores)
        else:
            top_indices = np.argpartition(-scores, top_k)[:top_k]
            top_indices = top_indices[np.argsort(-scores[top_indices])]

        hits = []
        for idx in top_indices:
            meta = self._metadata[idx]
            hits.append(VectorHit(
                path=meta["path"],
                filename=meta["filename"],
                similarity=round(float(scores[idx]), 4),
                chunk_start=meta.get("chunk_start", 0),
                chunk_text=meta.get("chunk_text", ""),
            ))

        return hits

    def search_vector(self, vector, top_k: int = 10) -> list[VectorHit]:
        """Search with a pre-computed vector (skip embedding step)."""
        import numpy as np

        if not self.exists:
            return []
        self._load_from_disk()
        if self._embeddings is None or len(self._embeddings) == 0:
            return []

        q_vec = np.array(vector, dtype=np.float32).reshape(1, -1)
        norm = np.linalg.norm(q_vec)
        if norm > 0:
            q_vec = q_vec / norm

        scores = (self._embeddings @ q_vec.T).flatten()

        if len(scores) < top_k:
            top_indices = np.argsort(-scores)
        else:
            top_indices = np.argpartition(-scores, top_k)[:top_k]
            top_indices = top_indices[np.argsort(-scores[top_indices])]

        hits = []
        for idx in top_indices:
            meta = self._metadata[idx]
            hits.append(VectorHit(
                path=meta["path"],
                filename=meta["filename"],
                similarity=round(float(scores[idx]), 4),
                chunk_start=meta.get("chunk_start", 0),
                chunk_text=meta.get("chunk_text", ""),
            ))

        return hits

    def chunk_count(self) -> int:
        """How many chunks are in the index."""
        if not self.exists:
            return 0
        self._load_from_disk()
        return len(self._metadata)


def _chunk_text(text: str, chunk_size: int = 512) -> list[str]:
    """Split text into chunks, trying to break at newlines."""
    if len(text) <= chunk_size:
        return [text]

    chunks = []
    start = 0
    while start < len(text):
        end = start + chunk_size
        if end >= len(text):
            chunks.append(text[start:])
            break

        # Try to break at a newline near the boundary
        newline_pos = text.rfind("\n", start + chunk_size // 2, end + 100)
        if newline_pos > start:
            end = newline_pos + 1

        chunks.append(text[start:end])
        start = end

    return chunks


# ---------------------------------------------------------------------------
# Module interface
# ---------------------------------------------------------------------------

def execute(inputs: dict, config: dict) -> ModuleOutput:
    """Build or query a vector index.

    Config:
        directory: str -- path to index
        action: "build" | "search" | "reindex" (default: "build")
        query: str -- search query (required if action=search)
        top_k: int -- max results (default: 10)
        model: str -- sentence-transformers model (default: all-MiniLM-L6-v2)
        chunk_size: int -- chars per chunk (default: 512)
    """
    directory = config.get("directory", ".")
    action = config.get("action", "build")
    model = config.get("model", DEFAULT_MODEL)

    try:
        idx = VectorIndex(directory, model_name=model)
    except Exception as e:
        return ModuleOutput(
            data=[], mode="D", stage="Pe",
            errors=[f"Failed to initialize VectorIndex: {e}"],
            stats={"error": str(e)},
        )

    if action == "search":
        query = config.get("query", "")
        top_k = config.get("top_k", 10)
        if not query:
            return ModuleOutput(
                data=[], mode="D", stage="Pe",
                stats={"error": "no query provided"},
            )
        try:
            hits = idx.search(query, top_k)
            return ModuleOutput(
                data=hits, confident=hits, mode="D", stage="Pe",
                stats={"query": query, "hits": len(hits), "top_k": top_k},
            )
        except ImportError as e:
            return ModuleOutput(
                data=[], mode="D", stage="Pe",
                errors=[f"sentence-transformers not installed: {e}"],
                stats={"error": str(e)},
            )

    # Build or reindex
    try:
        chunk_size = config.get("chunk_size", 512)
        stats = idx.build(force=(action == "reindex"), chunk_size=chunk_size)
        return ModuleOutput(
            data=stats, confident=[], mode="D", stage="Pe",
            stats=stats,
        )
    except ImportError as e:
        return ModuleOutput(
            data=[], mode="D", stage="Pe",
            errors=[f"sentence-transformers or numpy not installed: {e}"],
            stats={"error": str(e), "note": "Install: pip install sentence-transformers numpy"},
        )
