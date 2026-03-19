"""
OOK Query Layer — in-memory filter over INDEX.json.

Agents use this instead of loading INDEX.json into context.
Load once, query many times. O(n) filter but n < 10K is instant.

Usage:
    from runtime.query_ook import OOKIndex

    idx = OOKIndex.load("system/registry/ook/INDEX.json")

    # Recent changes
    results = idx.recent(20)

    # Filter by classification
    results = idx.filter(category="spec")
    results = idx.filter(otr="SRC", otb="DOC")
    results = idx.filter(category="runtime", subcategory="core")

    # Search by path pattern (substring match)
    results = idx.search("worker")
    results = idx.search("runtime/nodes")

    # Lookup by OOK key
    obj = idx.get("CORP-MAIN-CREATE-0001-20260317-O-0042-0003")

    # Lookup by path
    obj = idx.by_path("os/runtime/state.py")

For scale beyond 10K objects, replace the filter loops with a tantivy
index over the same INDEX.json records. The API stays the same.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any


class OOKIndex:
    """In-memory queryable index over OOK registry records."""

    def __init__(self, records: list[dict], metadata: dict):
        self._records = records  # Live objects, sorted by last_modified desc
        self._metadata = metadata
        # Build lookups
        self._by_key: dict[str, dict] = {}
        self._by_path: dict[str, dict] = {}
        for r in records:
            self._by_key[r.get("ook_key", "")] = r
            self._by_path[r.get("path", "")] = r

    @classmethod
    def load(cls, index_path: str | Path) -> OOKIndex:
        """Load INDEX.json and build the queryable index."""
        p = Path(index_path)
        if not p.exists():
            return cls([], {})
        with open(p, "r", encoding="utf-8") as f:
            data = json.load(f)
        # Filter to live objects only
        live = [
            o for o in data.get("objects", [])
            if o.get("changelog", [{}])[-1].get("change") != "deleted"
        ]
        return cls(live, {k: v for k, v in data.items() if k != "objects"})

    @property
    def total(self) -> int:
        return len(self._records)

    @property
    def metadata(self) -> dict:
        return self._metadata

    def recent(self, limit: int = 20) -> list[dict]:
        """Return the N most recently modified objects."""
        return self._records[:limit]

    def get(self, ook_key: str) -> dict | None:
        """Lookup a single object by OOK key."""
        return self._by_key.get(ook_key)

    def by_path(self, path: str) -> dict | None:
        """Lookup a single object by its file path."""
        return self._by_path.get(path)

    def search(self, pattern: str, limit: int = 50) -> list[dict]:
        """Search objects by substring match on path.

        Case-insensitive. Returns matches sorted by recency.
        """
        pattern_lower = pattern.lower()
        results = []
        for r in self._records:
            if pattern_lower in r.get("path", "").lower():
                results.append(r)
                if len(results) >= limit:
                    break
        return results

    def filter(
        self,
        category: str | None = None,
        subcategory: str | None = None,
        otr: str | None = None,
        otb: str | None = None,
        otg: str | None = None,
        extension: str | None = None,
        min_version: int | None = None,
        limit: int = 100,
    ) -> list[dict]:
        """Filter objects by classification fields.

        All parameters are AND-combined. None = no filter on that field.
        Returns matches sorted by recency (most recent first).
        """
        results = []
        for r in self._records:
            c = r.get("classification", {})
            if category and c.get("category") != category:
                continue
            if subcategory and c.get("subcategory") != subcategory:
                continue
            if otr and c.get("otr") != otr:
                continue
            if otb and c.get("otb") != otb:
                continue
            if otg and otg not in c.get("otg", []):
                continue
            if extension and r.get("extension") != extension:
                continue
            if min_version and r.get("object_version", 1) < min_version:
                continue
            results.append(r)
            if len(results) >= limit:
                break
        return results

    def stats(self) -> dict:
        """Return aggregate statistics."""
        return self._metadata.get("stats", {})

    def changed_since(self, timestamp: str, limit: int = 100) -> list[dict]:
        """Return objects modified after the given ISO timestamp."""
        results = []
        for r in self._records:
            if r.get("last_modified", "") > timestamp:
                results.append(r)
                if len(results) >= limit:
                    break
            else:
                break  # Already sorted by recency, so we can stop
        return results

    def summary(self) -> str:
        """Human-readable summary for agent orientation."""
        s = self._metadata.get("stats", {})
        lines = [
            f"OOK Index: {self.total} objects in {self._metadata.get('domain', '?')} domain",
            f"Last indexed: {self._metadata.get('last_indexed', '?')}",
            f"Index runs: {self._metadata.get('index_count', 0)}",
        ]
        by_cat = s.get("by_category", {})
        if by_cat:
            lines.append("By category: " + ", ".join(f"{k}={v}" for k, v in sorted(by_cat.items())))
        by_otr = s.get("by_lifecycle_role", {})
        if by_otr:
            lines.append("By role: " + ", ".join(f"{k}={v}" for k, v in sorted(by_otr.items())))
        last = s.get("last_run", {})
        if last:
            lines.append(
                f"Last run: +{last.get('added', 0)} added, "
                f"~{last.get('modified', 0)} modified, "
                f"-{last.get('deleted', 0)} deleted, "
                f"={last.get('unchanged', 0)} unchanged"
            )
        return "\n".join(lines)
