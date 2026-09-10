"""F6-AC3 CONTROL -- a planted LOCAL KUZU BUILDER.

This file exists to be CAUGHT. It does four things at once so one run grades the
walker on every axis it claims:

  1. a WRITE-open of kuzu.Database on a repo-anchored path  -> must be a BUILDER
  2. a READ-ONLY open of kuzu.Database on the same path     -> must NOT be one
  3. a docstring naming kuzu_stitch_db and kuzu_stitch_load -> must score ZERO
  4. a comment naming kuzu.Database(                        -> must score ZERO

If the walker returns 0 builders here, the 0 it returns on the real tree is a
constant wearing a measurement's clothes. Never imported, never run.
"""
from __future__ import annotations

import os

import kuzu

_HERE = os.path.dirname(os.path.abspath(__file__))
PLANTED_DB = os.path.join(_HERE, "out", "planted_stitch_db")


def build() -> None:
    # kuzu.Database( on a repo path with no read_only -- the one-command path back
    db = kuzu.Database(PLANTED_DB)
    conn = kuzu.Connection(db)
    conn.execute("CREATE NODE TABLE IF NOT EXISTS CloudNode(node_id STRING PRIMARY KEY)")


def read() -> None:
    d = kuzu.Database(PLANTED_DB, read_only=True)
    kuzu.Connection(d).execute("MATCH (n:CloudNode) RETURN count(*)")
