"""
compress-context.py — Embedding-based context compression for thread orchestrator.

Takes a thread's full context/ directory, embeds all content, retrieves the top-K
most relevant chunks against the opening message + inline briefing, and writes a
compressed CONTEXT_COMPILED.md that fits within a token budget.

Usage:
    python org/threads/compress-context.py \
        --thread ADVI_MVPLVL-005-addendum-a-mix-timeseries-alignment \
        --max-chars 40000

The script reads:
  - context/agents/**  (logs, task orders, READMEs, commits)
  - context/refs/**    (code files, documents)
  - context/inline_notes.md
  - messages/000.md    (opening message — used as the query)

It writes:
  - context/CONTEXT_COMPILED.md  (overwritten with compressed version)
"""

import argparse
import os
import re
import sys
from pathlib import Path

import numpy as np
from sentence_transformers import SentenceTransformer


def chunk_text(text: str, source: str, chunk_size: int = 600, overlap: int = 100) -> list[dict]:
    """Split text into overlapping chunks, preserving paragraph boundaries where possible."""
    chunks = []
    # Split on double newlines first (paragraph boundaries)
    paragraphs = re.split(r'\n\s*\n', text)

    current = ""
    for para in paragraphs:
        para = para.strip()
        if not para:
            continue
        if len(current) + len(para) + 2 <= chunk_size:
            current = current + "\n\n" + para if current else para
        else:
            if current:
                chunks.append({"text": current, "source": source})
            # If single paragraph exceeds chunk_size, split by lines
            if len(para) > chunk_size:
                lines = para.split('\n')
                current = ""
                for line in lines:
                    if len(current) + len(line) + 1 <= chunk_size:
                        current = current + "\n" + line if current else line
                    else:
                        if current:
                            chunks.append({"text": current, "source": source})
                        current = line
            else:
                current = para

    if current:
        chunks.append({"text": current, "source": source})

    return chunks


def gather_files(context_dir: Path) -> list[dict]:
    """Walk context/ and read all text files into (source, text) pairs."""
    files = []
    for root, dirs, filenames in os.walk(context_dir):
        for fname in filenames:
            fpath = Path(root) / fname
            rel = fpath.relative_to(context_dir)
            try:
                text = fpath.read_text(encoding='utf-8', errors='replace')
                if text.strip():
                    files.append({"source": str(rel), "text": text})
            except Exception:
                continue
    return files


def main():
    parser = argparse.ArgumentParser(description="Compress thread context via embeddings")
    parser.add_argument("--thread", required=True, help="Thread ID (folder name)")
    parser.add_argument("--max-chars", type=int, default=40000,
                        help="Max chars for compressed output (~10K tokens)")
    parser.add_argument("--threads-dir", default=None,
                        help="Path to org/threads/ (auto-detected from script location)")
    args = parser.parse_args()

    if args.threads_dir:
        threads_dir = Path(args.threads_dir)
    else:
        threads_dir = Path(__file__).parent

    thread_dir = threads_dir / args.thread
    context_dir = thread_dir / "context"
    messages_dir = thread_dir / "messages"

    if not thread_dir.exists():
        print(f"ERROR: Thread directory not found: {thread_dir}", file=sys.stderr)
        sys.exit(1)

    # --- Read the query (opening message + inline notes) ---
    query_parts = []

    opening = messages_dir / "000.md"
    if opening.exists():
        query_parts.append(opening.read_text(encoding='utf-8', errors='replace'))

    inline = context_dir / "inline_notes.md"
    if inline.exists():
        query_parts.append(inline.read_text(encoding='utf-8', errors='replace'))

    query_text = "\n\n".join(query_parts)
    if not query_text.strip():
        print("ERROR: No opening message or inline notes found for query", file=sys.stderr)
        sys.exit(1)

    # --- Gather all context files ---
    all_files = gather_files(context_dir)
    print(f"Found {len(all_files)} context files, total {sum(len(f['text']) for f in all_files):,} chars")

    # --- Chunk everything ---
    all_chunks = []
    for f in all_files:
        chunks = chunk_text(f["text"], f["source"])
        all_chunks.extend(chunks)

    print(f"Chunked into {len(all_chunks)} segments")

    if not all_chunks:
        print("WARNING: No chunks to compress. Skipping.", file=sys.stderr)
        sys.exit(0)

    # --- Embed ---
    print("Loading embedding model...")
    model = SentenceTransformer('all-MiniLM-L6-v2')

    print("Encoding query...")
    query_embedding = model.encode([query_text], normalize_embeddings=True)[0]

    print("Encoding chunks...")
    chunk_texts = [c["text"] for c in all_chunks]
    chunk_embeddings = model.encode(chunk_texts, normalize_embeddings=True, batch_size=64)

    # --- Score and rank ---
    scores = chunk_embeddings @ query_embedding
    ranked_indices = np.argsort(-scores)

    # --- Select top chunks within budget ---
    # Always include inline_notes.md verbatim (operational context)
    selected = []
    char_budget = args.max_chars
    forced_sources = set()

    # Force-include inline notes
    if inline.exists():
        inline_text = inline.read_text(encoding='utf-8', errors='replace')
        selected.append({
            "text": inline_text,
            "source": "inline_notes.md",
            "score": 1.0,
            "forced": True
        })
        char_budget -= len(inline_text)
        forced_sources.add("inline_notes.md")

    # Force-include opening message as-is (it's the thread anchor)
    if opening.exists():
        opening_text = opening.read_text(encoding='utf-8', errors='replace')
        # Don't add to selected — it's already in messages/000.md
        # But deduct from budget since orchestrator includes it

    for idx in ranked_indices:
        chunk = all_chunks[idx]
        if chunk["source"] in forced_sources:
            continue
        text_len = len(chunk["text"])
        if text_len > char_budget:
            continue
        selected.append({
            "text": chunk["text"],
            "source": chunk["source"],
            "score": float(scores[idx]),
            "forced": False
        })
        char_budget -= text_len
        if char_budget <= 0:
            break

    print(f"Selected {len(selected)} chunks ({args.max_chars - char_budget:,} chars used of {args.max_chars:,} budget)")

    # --- Group by source for readable output ---
    by_source = {}
    for s in selected:
        src = s["source"]
        if src not in by_source:
            by_source[src] = []
        by_source[src].append(s)

    # --- Write compressed CONTEXT_COMPILED.md ---
    output_path = context_dir / "CONTEXT_COMPILED.md"
    lines = [
        "# Thread Context (embedding-compressed)\n",
        f"Budget: {args.max_chars:,} chars | Chunks: {len(selected)} of {len(all_chunks)} | "
        f"Score range: {min(s['score'] for s in selected if not s.get('forced')):.3f} - "
        f"{max(s['score'] for s in selected if not s.get('forced')):.3f}\n",
        "---\n"
    ]

    for source in sorted(by_source.keys()):
        chunks = by_source[source]
        lines.append(f"\n## Source: `{source}`\n")
        for c in chunks:
            tag = "[FORCED]" if c.get("forced") else f"[score={c['score']:.3f}]"
            lines.append(f"\n{tag}\n")
            lines.append(c["text"])
            lines.append("\n")

    compiled = "\n".join(lines)
    output_path.write_text(compiled, encoding='utf-8')
    print(f"Wrote {len(compiled):,} chars to {output_path.relative_to(thread_dir)}")


if __name__ == "__main__":
    main()
