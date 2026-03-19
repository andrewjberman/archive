"""
Ev: Evaluate -- Cluster-Based Classifier (R-mode).

For unstructured/messy data where path-based rules don't work.
Clusters files by fingerprint features, then assigns files to
clusters. Cluster labels are resolved by I-mode (one LLM call
per cluster, not per file).

Pipeline:
1. Feature extraction from fingerprints (D-mode)
2. Clustering via k-means or hierarchical (D-mode)
3. Cluster labeling (I-mode -- one call per cluster)
4. File assignment to clusters (D-mode)

Spec: ONT.CORE.KF_EXECUTION_MODES Section 3.3 (extended for unstructured data)
"""

from __future__ import annotations

import math
from collections import Counter, defaultdict
from dataclasses import dataclass, field
from typing import Any

from .. import ModuleOutput
from ..interpret.corpus_fingerprinter import CorpusFingerprint


@dataclass
class ClusterAssignment:
    """A file assigned to a cluster."""
    path: str
    cluster_id: int
    cluster_label: str = ""         # Set by I-mode labeling
    distance_to_centroid: float = 0.0
    confidence: float = 0.0         # 1.0 - normalized distance
    is_outlier: bool = False        # Too far from any cluster


@dataclass
class Cluster:
    """A group of similar files."""
    cluster_id: int
    size: int = 0
    label: str = ""                 # Set by I-mode
    centroid: list[float] = field(default_factory=list)
    representative_paths: list[str] = field(default_factory=list)  # 5 files closest to centroid
    dominant_content_class: str = ""
    dominant_extension: str = ""


# ---------------------------------------------------------------------------
# Feature extraction (D-mode)
# ---------------------------------------------------------------------------

def _extract_features(fp: CorpusFingerprint) -> list[float]:
    """Convert a CorpusFingerprint into a numeric feature vector.

    17 features capturing content shape, structure, and type.
    """
    # Content type one-hot (6 classes)
    content_classes = ["narrative", "tabular", "code", "config", "document", "data"]
    content_onehot = [1.0 if fp.content_class == c else 0.0 for c in content_classes]

    return [
        # Character ratios (3)
        fp.letter_ratio,
        fp.digit_ratio,
        fp.whitespace_ratio,
        # Structure (4)
        min(fp.line_count / 1000.0, 1.0),           # normalized line count
        min(fp.avg_line_length / 200.0, 1.0),        # normalized avg line length
        min(fp.paragraph_count / 50.0, 1.0),          # normalized paragraph count
        min(fp.column_count / 20.0, 1.0),             # normalized column count
        # Entropy (1)
        fp.entropy / 8.0,                              # normalized (max entropy ~8 bits)
        # Code signals (3)
        1.0 if fp.has_imports else 0.0,
        1.0 if fp.has_functions else 0.0,
        1.0 if fp.has_classes else 0.0,
    ] + content_onehot  # + 6 = 17 total


def _euclidean_distance(a: list[float], b: list[float]) -> float:
    """Euclidean distance between two feature vectors."""
    return math.sqrt(sum((x - y) ** 2 for x, y in zip(a, b)))


# ---------------------------------------------------------------------------
# K-Means clustering (D-mode, no external dependencies)
# ---------------------------------------------------------------------------

def _kmeans(
    vectors: list[list[float]],
    k: int,
    max_iterations: int = 50,
) -> tuple[list[int], list[list[float]]]:
    """Simple k-means clustering. Returns (assignments, centroids).

    No numpy/scipy dependency — pure Python. Fast enough for 5,000 items
    with 17 features.
    """
    import random

    if not vectors or k <= 0:
        return [], []

    n = len(vectors)
    dim = len(vectors[0])
    k = min(k, n)

    # Initialize centroids with k-means++ style
    centroids = [vectors[random.randint(0, n - 1)][:]]
    for _ in range(k - 1):
        # Pick next centroid with probability proportional to distance squared
        dists = []
        for v in vectors:
            min_d = min(_euclidean_distance(v, c) for c in centroids)
            dists.append(min_d * min_d)
        total = sum(dists) or 1.0
        probs = [d / total for d in dists]
        r = random.random()
        cumulative = 0.0
        chosen = 0
        for i, p in enumerate(probs):
            cumulative += p
            if cumulative >= r:
                chosen = i
                break
        centroids.append(vectors[chosen][:])

    assignments = [0] * n

    for _ in range(max_iterations):
        # Assign each point to nearest centroid
        changed = False
        for i, v in enumerate(vectors):
            dists = [_euclidean_distance(v, c) for c in centroids]
            nearest = dists.index(min(dists))
            if assignments[i] != nearest:
                changed = True
                assignments[i] = nearest

        if not changed:
            break

        # Update centroids
        for ci in range(k):
            members = [vectors[i] for i in range(n) if assignments[i] == ci]
            if members:
                centroids[ci] = [
                    sum(m[d] for m in members) / len(members)
                    for d in range(dim)
                ]

    return assignments, centroids


def _estimate_k(n: int) -> int:
    """Estimate number of clusters using rule of thumb.

    sqrt(n/2) works well for document collections. Capped at 30.
    """
    k = max(3, int(math.sqrt(n / 2)))
    return min(k, 30)


# ---------------------------------------------------------------------------
# Cluster analysis (D-mode)
# ---------------------------------------------------------------------------

def cluster_files(
    fingerprints: list[CorpusFingerprint],
    k: int | None = None,
    outlier_threshold: float = 2.0,
) -> tuple[list[Cluster], list[ClusterAssignment]]:
    """Cluster files by fingerprint features.

    Args:
        fingerprints: Extended fingerprints from corpus_fingerprinter
        k: Number of clusters (auto-estimated if None)
        outlier_threshold: Distance multiplier for outlier detection

    Returns:
        (clusters, assignments)
    """
    if not fingerprints:
        return [], []

    # Extract features
    vectors = [_extract_features(fp) for fp in fingerprints]

    # Estimate k
    if k is None:
        k = _estimate_k(len(fingerprints))

    # Run k-means
    labels, centroids = _kmeans(vectors, k)

    # Build cluster objects
    cluster_map: dict[int, list[int]] = defaultdict(list)
    for i, label in enumerate(labels):
        cluster_map[label].append(i)

    clusters: list[Cluster] = []
    for cid in sorted(cluster_map.keys()):
        member_indices = cluster_map[cid]
        member_fps = [fingerprints[i] for i in member_indices]

        # Dominant content class
        class_counts = Counter(fp.content_class for fp in member_fps)
        dominant_class = class_counts.most_common(1)[0][0] if class_counts else ""

        # Dominant extension
        ext_counts = Counter(Path(fp.path).suffix.lower() for fp in member_fps
                             if fp.path)
        dominant_ext = ext_counts.most_common(1)[0][0] if ext_counts else ""

        # Representatives: 5 files closest to centroid
        dists = [(i, _euclidean_distance(vectors[i], centroids[cid]))
                 for i in member_indices]
        dists.sort(key=lambda x: x[1])
        reps = [fingerprints[i].path for i, _ in dists[:5]]

        clusters.append(Cluster(
            cluster_id=cid,
            size=len(member_indices),
            centroid=centroids[cid],
            representative_paths=reps,
            dominant_content_class=dominant_class,
            dominant_extension=dominant_ext,
        ))

    # Build assignments with confidence
    # Confidence = 1 - (distance / max_distance_in_cluster)
    assignments: list[ClusterAssignment] = []
    for i, (fp, label) in enumerate(zip(fingerprints, labels)):
        dist = _euclidean_distance(vectors[i], centroids[label])

        # Calculate cluster radius (max distance in this cluster)
        cluster_dists = [
            _euclidean_distance(vectors[j], centroids[label])
            for j in cluster_map[label]
        ]
        max_dist = max(cluster_dists) if cluster_dists else 1.0
        avg_dist = sum(cluster_dists) / len(cluster_dists) if cluster_dists else 1.0

        confidence = max(0.0, 1.0 - (dist / (max_dist + 1e-10)))
        is_outlier = dist > avg_dist * outlier_threshold

        assignments.append(ClusterAssignment(
            path=fp.path,
            cluster_id=label,
            distance_to_centroid=dist,
            confidence=confidence,
            is_outlier=is_outlier,
        ))

    return clusters, assignments


# Need Path for extension counting
from pathlib import Path


def execute(inputs: dict, config: dict) -> ModuleOutput:
    """Cluster files by fingerprint features.

    Inputs:
        in_output: list[CorpusFingerprint]

    Config:
        k: int | None -- number of clusters (auto if None)
        outlier_threshold: float -- distance multiplier for outliers
    """
    fingerprints = inputs.get("in_output", [])
    k = config.get("k", None)
    outlier_threshold = config.get("outlier_threshold", 2.0)

    clusters, assignments = cluster_files(fingerprints, k, outlier_threshold)

    outliers = [a for a in assignments if a.is_outlier]
    confident = [a for a in assignments if not a.is_outlier]

    return ModuleOutput(
        data={"clusters": clusters, "assignments": assignments},
        confident=confident,
        ambiguous=outliers,
        mode="R",
        stage="Ev",
        stats={
            "total_files": len(assignments),
            "num_clusters": len(clusters),
            "outliers": len(outliers),
            "confident": len(confident),
            "cluster_sizes": {c.cluster_id: c.size for c in clusters},
        },
    )
