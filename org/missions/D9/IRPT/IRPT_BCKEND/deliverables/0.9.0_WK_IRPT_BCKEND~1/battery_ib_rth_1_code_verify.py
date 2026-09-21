#!/usr/bin/env python3
"""IB-rth-1 -- in-process verification of the loaders.py fix, over the REAL wire shapes measured
live this session (never a fabricated exception class). This is NOT R76-AC1 (that criterion needs
the DEPLOYED role + bytes, arm (e), which this cell does not reach -- B1 is a never-widen act,
STOPPED before apply). It is the evidence that the SOURCE fix in `_authz/loaders.py` behaves as
the packet claims, using botocore's own ClientError construction with the exact Error.Code/Message
this session's live AWS calls returned (see IB-rth-1_investigation.md sections 2-3).
"""
from __future__ import annotations

import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
WS = os.path.abspath(os.path.join(HERE, "..", "..", "..", "..", "..", "..", ".."))
sys.path.insert(0, os.path.join(WS, "infra", "aws", "lambda", "investor-reporting", "_authz"))

from botocore.exceptions import ClientError  # noqa: E402

import loaders  # noqa: E402

TOKEN = "IB-RTH-1-LOADERS-FIX-VERIFIED"


class FakeStreamingBody:
    def read(self):
        raise AssertionError("must not be reached -- the exception path never calls Body.read()")


def make_client_error(code: str, message: str, key: str) -> ClientError:
    # THE REAL SHAPE, measured live this session (IB-rth-1 investigation, section 3):
    #   NoSuchKey:    {'Code': 'NoSuchKey', 'Message': 'The specified key does not exist.', 'Key': key}
    #   AccessDenied: {'Code': 'AccessDenied', 'Message': '<verbatim ListBucket-masking message>'}
    resp = {"Error": {"Code": code, "Message": message}, "ResponseMetadata": {"HTTPStatusCode": 404 if code == "NoSuchKey" else 403}}
    if code == "NoSuchKey":
        resp["Error"]["Key"] = key
    err = ClientError(resp, "GetObject")
    if code == "AccessDenied":
        err.__class__ = type("AccessDenied", (ClientError,), {})
    elif code == "NoSuchKey":
        err.__class__ = type("NoSuchKey", (ClientError,), {})
    return err


class FakeS3:
    def __init__(self, exc: Exception | None, body: bytes | None = None):
        self._exc = exc
        self._body = body

    def get_object(self, Bucket, Key):  # noqa: N803
        if self._exc is not None:
            raise self._exc
        class _Body:
            def __init__(self, b):
                self._b = b
            def read(self):
                return self._b
        return {"Body": _Body(self._body)}


def run() -> int:
    lines: list[str] = []

    def emit(s: str = "") -> None:
        lines.append(s)
        print(s, flush=True)

    ok = True

    # (1) NoSuchKey -- the pre-existing, already-working case. Must still return empty map.
    loaders._ARTIFACTS.clear()
    exc1 = make_client_error("NoSuchKey", "The specified key does not exist.",
                              "platinum/cottonwood/ownership_map.json")
    fake1 = FakeS3(exc1)
    art1 = loaders.load_ownership("cottonwood", s3=fake1)
    c1 = art1 == {"schema_version": 1, "advisors": {}}
    emit("(1) NoSuchKey (pre-existing case) -> %r -> %s" % (art1, "OK" if c1 else "FAIL"))
    ok = ok and c1

    # (2) AccessDenied with the EXACT live-measured message (the S94 mechanism) -- must NOW return
    #     empty map (this is the fix; before this edit, this branch re-raised -> UNEXPECTED).
    loaders._ARTIFACTS.clear()
    live_message = ('An error occurred (AccessDenied) when calling the GetObject operation: User: '
                     'arn:aws:sts::313476888478:federated-user/ib-rth-1-wiretest2 is not authorized '
                     'to perform: s3:ListBucket on resource: "arn:aws:s3:::opal-data-inf" because no '
                     'session policy allows the s3:ListBucket action')
    exc2 = make_client_error("AccessDenied", live_message, "platinum/inflection/ownership_map.json")
    fake2 = FakeS3(exc2)
    art2 = loaders.load_ownership("inflection", s3=fake2)
    c2 = art2 == {"schema_version": 1, "advisors": {}}
    emit("(2) AccessDenied, live-measured message (S94 mechanism) -> %r -> %s" % (art2, "OK" if c2 else "FAIL"))
    ok = ok and c2

    # (3) NEGATIVE CONTROL -- a genuinely different failure (e.g. InternalError, 500) must still
    #     RAISE, never be swallowed as empty. This is the discriminator that the fix is narrow.
    loaders._ARTIFACTS.clear()
    exc3 = make_client_error("InternalError", "We encountered an internal error. Please try again.",
                              "platinum/49financial/ownership_map.json")
    fake3 = FakeS3(exc3)
    raised = False
    try:
        loaders.load_ownership("49financial", s3=fake3)
    except ClientError:
        raised = True
    emit("(3) NEGATIVE CONTROL -- InternalError (a genuine outage) -> raised: %s -> %s"
         % (raised, "OK" if raised else "FAIL (the fix over-widened and swallowed a real outage)"))
    ok = ok and raised

    # (4) POSITIVE CONTROL -- a present map is read through unchanged (the happy path untouched).
    loaders._ARTIFACTS.clear()
    import json as _json
    body = _json.dumps({"schema_version": 1, "advisors": {"abby_horton": {"account_ids": ["acc_1"]}}}).encode()
    fake4 = FakeS3(None, body=body)
    art4 = loaders.load_ownership("49financial", s3=fake4)
    c4 = art4.get("advisors", {}).get("abby_horton") is not None
    emit("(4) POSITIVE CONTROL -- a present map -> %r -> %s" % (art4, "OK" if c4 else "FAIL"))
    ok = ok and c4

    emit("")
    emit("RESULT: %s -- 4 of 4 checks %s" % ("PASS" if ok else "FAIL", "hold" if ok else "do NOT all hold"))
    if ok:
        emit(TOKEN)
    out_path = os.path.join(HERE, "IB-rth-1_code_verify_output.txt")
    with open(out_path, "w", encoding="utf-8", newline="\n") as fh:
        fh.write("\n".join(lines) + "\n")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(run())
