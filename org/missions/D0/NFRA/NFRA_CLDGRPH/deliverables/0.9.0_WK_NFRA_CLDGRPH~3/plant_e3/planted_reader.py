#!/usr/bin/env python3
"""E3-AC2 POSITIVE CONTROL -- a file that DOES read a residual local store.

This module is never imported and never run. It exists so that
`no_readers.sh` can prove its walker is able to return non-zero: a detector
that cannot fire on the positive case is a constant, not a measurement.
"""
import os

import kuzu  # noqa: F401  (control file; the import is part of the specimen)

HERE = os.path.dirname(os.path.abspath(__file__))
AC7_DB_PATH = os.path.join(HERE, "kuzu_ac7.db")


def read_the_store():
    db = kuzu.Database(AC7_DB_PATH)
    conn = kuzu.Connection(db)
    return conn.execute("MATCH (n:CloudNode) RETURN count(*)")


def also_opens_the_june_scratch():
    with open(os.path.join(HERE, "kuzu_db", "catalog.kz"), "rb") as fh:
        return fh.read(16)
