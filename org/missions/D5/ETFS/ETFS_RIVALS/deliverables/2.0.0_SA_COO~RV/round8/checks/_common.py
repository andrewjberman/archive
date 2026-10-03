"""Shared helpers for the ETFS_RIVALS round-7 and round-8 checks (issuer-written, 2.0.0_SA_COO~RV): re-exports round 6's helpers
(Verdict, guarded, setup_path, tmpdir, the page fixture, the A1/AI fixtures) and adds `offline_guards`. Every
round-7 check runs offline on a `local:` sink: no S3 read or write, no Secrets Manager read, no Lambda invoke, no
vendor call."""
from __future__ import annotations

import importlib.util
import pathlib
import sys
import types

_R6 = pathlib.Path(__file__).resolve().parents[2] / "round6" / "checks" / "_common.py"
_spec = importlib.util.spec_from_file_location("_rivals_r6_common", _R6)
_r6 = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(_r6)

Verdict, guarded, setup_path, tmpdir = _r6.Verdict, _r6.guarded, _r6.setup_path, _r6.tmpdir
page_fixture, ai2_tables, ai2_readings, ai2_reply, StubClient, AI_DAY = (
    _r6.page_fixture, _r6.ai2_tables, _r6.ai2_readings, _r6.ai2_reply, _r6.StubClient, _r6.AI_DAY)
contribution_rows = _r6.contribution_rows

ROOT = pathlib.Path(__file__).resolve().parents[9]  # the tree this check file lives in


def offline_guards() -> None:
    """Refuse every off-box act for the rest of the process: any boto3 client or resource (S3, Secrets Manager, Lambda)
    and `requests.post` raise PermissionError, so a stub that fails to bind can never reach AWS or the vendor."""
    fake = types.ModuleType("boto3")

    def _refuse(*a, **k):
        raise PermissionError("offline check: boto3 is refused (no S3, no Secrets Manager, no Lambda)")

    fake.client = fake.resource = fake.Session = _refuse
    sys.modules["boto3"] = fake
    try:
        import requests
    except ImportError:
        return

    def _no_post(*a, **k):
        raise PermissionError("offline check: requests.post is refused (no vendor call)")

    requests.post = _no_post
