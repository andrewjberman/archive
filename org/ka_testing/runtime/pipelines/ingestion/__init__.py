"""
Ingestion Pipelines -- supplier-layer archetype.

Supplier workers have access to these pipelines. They compose
KF stage modules (Pe, In, Ev) for data intake and discovery work.
"""

from .corpus_ingestion import run_corpus_ingestion
from .classification_pipeline import run_classification_pipeline

__all__ = ["run_corpus_ingestion", "run_classification_pipeline"]
