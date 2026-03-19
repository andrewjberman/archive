"""
Corpus Ingestion Pipeline -- supplier-layer, KF_EXECUTION_MODES for unstructured data.

Handles messy client data dumps where directory structure is meaningless.
Composes: Pe (filesystem_scanner) -> In (corpus_fingerprinter) ->
Ev (cluster_classifier). Produces cluster assignments + I-mode prompts
for labeling.

Archetype access: supplier workers only.

Usage:
    from pipelines.ingestion import run_corpus_ingestion
    result = run_corpus_ingestion("/path/to/dump", output_dir="/path/to/output")

CLI:
    python -m system.os.runtime.pipelines.ingestion.corpus_ingestion \
        --directory /path/to/dump --output-dir /path/to/output

Spec: ONT.CORE.KF_EXECUTION_MODES + ONT.CORE.HYBRID_CLASSIFICATION
"""

from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any

# Import from modules (shared KF stage primitives)
from ...modules import ModuleOutput
from ...modules.perceive.filesystem_scanner import FileMetadata, execute as pe_execute
from ...modules.interpret.corpus_fingerprinter import CorpusFingerprint, execute as in_execute
from ...modules.evaluate.cluster_classifier import Cluster, ClusterAssignment, execute as ev_execute


def run_corpus_ingestion(
    directory: str,
    output_dir: str = "",
    extensions: tuple[str, ...] | None = None,
    k_clusters: int | None = None,
    outlier_threshold: float = 2.0,
) -> dict[str, Any]:
    """Run the full corpus ingestion pipeline (D-mode stages only).

    Returns the data needed for I-mode (cluster labeling + outlier
    resolution) but does not make LLM calls. The runtime's worker
    nodes handle I-mode.
    """
    # Default: scan all common file types
    if extensions is None:
        extensions = (
            ".md", ".json", ".yaml", ".yml", ".txt", ".csv", ".tsv",
            ".py", ".js", ".ts", ".go", ".java", ".rs", ".rb",
            ".sh", ".bash", ".sql", ".html", ".css", ".xml",
            ".toml", ".ini", ".cfg", ".conf", ".env",
            ".pdf", ".docx", ".xlsx", ".pptx",
        )

    # --- Pe: Perceive (D-mode) ---
    print("[Pe] Scanning filesystem...", file=sys.stderr)
    pe_result = pe_execute({}, {
        "directory": directory,
        "extensions": extensions,
        "excludes": ("__pycache__/", "node_modules/", ".git/", ".venv/"),
    })
    pe_output: list[FileMetadata] = pe_result.data
    print(f"[Pe] Found {len(pe_output)} files", file=sys.stderr)

    if not pe_output:
        return {
            "clusters": [], "assignments": [], "outliers": [],
            "cluster_label_prompts": [], "outlier_prompts": [],
            "stats": {"total_files": 0, "status": "empty"},
        }

    # --- In: Interpret with extended fingerprinting (D-mode) ---
    print("[In] Fingerprinting content (extended)...", file=sys.stderr)
    in_result = in_execute({"pe_output": pe_output}, {})
    in_output: list[CorpusFingerprint] = in_result.data
    print(
        f"[In] Fingerprinted {len(in_output)} files. "
        f"Classes: {in_result.stats.get('content_class_distribution', {})}",
        file=sys.stderr,
    )

    # --- Ev: Cluster (D-mode) ---
    print(f"[Ev] Clustering (k={'auto' if k_clusters is None else k_clusters})...", file=sys.stderr)
    ev_result = ev_execute(
        {"in_output": in_output},
        {"k": k_clusters, "outlier_threshold": outlier_threshold},
    )
    clusters: list[Cluster] = ev_result.data["clusters"]
    assignments: list[ClusterAssignment] = ev_result.data["assignments"]
    outliers = [a for a in assignments if a.is_outlier]
    print(
        f"[Ev] {len(clusters)} clusters, {len(assignments) - len(outliers)} assigned, "
        f"{len(outliers)} outliers",
        file=sys.stderr,
    )

    for c in clusters:
        print(
            f"  Cluster {c.cluster_id}: {c.size} files, "
            f"dominant={c.dominant_content_class}/{c.dominant_extension}, "
            f"reps={[Path(p).name for p in c.representative_paths[:3]]}",
            file=sys.stderr,
        )

    # --- Build I-mode prompts ---
    cluster_label_prompts = _build_cluster_prompts(clusters)
    outlier_prompts = _build_outlier_prompts(outliers)

    # --- Write output ---
    if output_dir:
        _write_output(output_dir, pe_output, clusters, assignments, cluster_label_prompts, outlier_prompts)

    return {
        "clusters": clusters,
        "assignments": assignments,
        "outliers": outliers,
        "cluster_label_prompts": cluster_label_prompts,
        "outlier_prompts": outlier_prompts,
        "stats": {
            "total_files": len(pe_output),
            "num_clusters": len(clusters),
            "outliers": len(outliers),
            "api_calls_for_labeling": len(clusters),
            "api_calls_for_outliers": len(outliers),
            "total_api_calls_needed": len(clusters) + len(outliers),
            "content_class_distribution": in_result.stats.get("content_class_distribution", {}),
        },
    }


def _build_cluster_prompts(clusters: list[Cluster]) -> list[dict]:
    """Build I-mode prompts for cluster labeling."""
    prompts = []
    for c in clusters:
        samples = []
        for rp in c.representative_paths[:5]:
            try:
                content = Path(rp).read_text(encoding="utf-8", errors="replace")
                preview = "\n".join(content.split("\n")[:20])
                samples.append({"path": rp, "preview": preview})
            except Exception:
                samples.append({"path": rp, "preview": "[could not read]"})

        prompts.append({
            "cluster_id": c.cluster_id,
            "size": c.size,
            "dominant_content_class": c.dominant_content_class,
            "dominant_extension": c.dominant_extension,
            "samples": samples,
            "prompt": (
                f"This cluster contains {c.size} files. "
                f"Dominant type: {c.dominant_content_class} ({c.dominant_extension}). "
                f"Below are 5 representative files (first 20 lines each).\n\n"
                + "\n\n".join(
                    f"### {Path(s['path']).name}\n```\n{s['preview']}\n```"
                    for s in samples
                )
                + "\n\nProvide a short label (1-5 words) and a one-sentence description "
                f"of what this cluster contains. Return JSON: "
                f'{{"label": "...", "description": "..."}}'
            ),
        })
    return prompts


def _build_outlier_prompts(outliers: list[ClusterAssignment]) -> list[dict]:
    """Build I-mode prompts for outlier classification."""
    prompts = []
    for o in outliers:
        try:
            content = Path(o.path).read_text(encoding="utf-8", errors="replace")
            preview = "\n".join(content.split("\n")[:30])
        except Exception:
            preview = "[could not read]"

        prompts.append({
            "path": o.path,
            "cluster_id": o.cluster_id,
            "distance": o.distance_to_centroid,
            "prompt": (
                f"This file did not fit well into any cluster (outlier). "
                f"Nearest cluster: {o.cluster_id} (distance: {o.distance_to_centroid:.3f}).\n\n"
                f"### {Path(o.path).name}\n```\n{preview}\n```\n\n"
                f"Provide a category label and description. Return JSON: "
                f'{{"label": "...", "description": "..."}}'
            ),
        })
    return prompts


def _write_output(
    output_dir: str,
    pe_output: list,
    clusters: list,
    assignments: list,
    cluster_prompts: list,
    outlier_prompts: list,
) -> None:
    """Write all output artifacts."""
    out = Path(output_dir)
    out.mkdir(parents=True, exist_ok=True)

    cluster_data = {
        "stats": {
            "total_files": len(pe_output),
            "num_clusters": len(clusters),
            "outliers": sum(1 for a in assignments if a.is_outlier),
            "api_calls_needed": len(clusters) + sum(1 for a in assignments if a.is_outlier),
        },
        "clusters": [
            {
                "cluster_id": c.cluster_id,
                "size": c.size,
                "label": c.label,
                "dominant_content_class": c.dominant_content_class,
                "dominant_extension": c.dominant_extension,
                "representatives": c.representative_paths[:5],
            }
            for c in clusters
        ],
        "assignments": [
            {
                "path": a.path,
                "cluster_id": a.cluster_id,
                "confidence": round(a.confidence, 3),
                "is_outlier": a.is_outlier,
            }
            for a in assignments
        ],
    }
    (out / "corpus_analysis.json").write_text(json.dumps(cluster_data, indent=2), encoding="utf-8")
    (out / "cluster_label_prompts.json").write_text(json.dumps(cluster_prompts, indent=2), encoding="utf-8")
    if outlier_prompts:
        (out / "outlier_prompts.json").write_text(json.dumps(outlier_prompts, indent=2), encoding="utf-8")

    print(f"\n[Output] Written to {out}/", file=sys.stderr)


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def main():
    import argparse

    parser = argparse.ArgumentParser(description="Corpus Ingestion Pipeline")
    parser.add_argument("--directory", required=True)
    parser.add_argument("--output-dir", default="")
    parser.add_argument("--k", type=int, default=None)
    parser.add_argument("--outlier-threshold", type=float, default=2.0)
    args = parser.parse_args()

    result = run_corpus_ingestion(
        directory=args.directory,
        output_dir=args.output_dir or str(Path(args.directory) / "ingestion_output"),
        k_clusters=args.k,
        outlier_threshold=args.outlier_threshold,
    )

    print(f"\nCorpus ingestion complete.", file=sys.stderr)
    print(f"  Files: {result['stats']['total_files']}", file=sys.stderr)
    print(f"  Clusters: {result['stats']['num_clusters']}", file=sys.stderr)
    print(f"  Outliers: {result['stats']['outliers']}", file=sys.stderr)
    print(f"  API calls needed: {result['stats']['total_api_calls_needed']}", file=sys.stderr)


if __name__ == "__main__":
    main()
