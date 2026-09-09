#!/usr/bin/env python3
"""E4-AC4 POSITIVE CONTROL -- a file that DOES open a local rebuild path.

It imports the canonical loader, calls its marker-oracle rebuild entrypoint and
names the canonical store's path constant: the exact shape CG-s-8 retired and
CG-s-20 is bound not to re-create. Fed through the SAME walker as the two real
files. Never imported, never run.
"""
import os

import kuzu_nessie_load
from kuzu_nessie_load import ensure_fresh

CANONICAL_DB_PATH = os.path.join(os.path.dirname(__file__), "kuzu_nessie_db")


def rebuild_locally_if_behind():
    ensure_fresh(CANONICAL_DB_PATH)
    return kuzu_nessie_load.main(["--db", CANONICAL_DB_PATH])
