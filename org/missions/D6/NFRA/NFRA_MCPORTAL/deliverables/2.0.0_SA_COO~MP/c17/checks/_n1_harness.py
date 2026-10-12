"""MP-n-1 (PRD v0.6 C17) offline harness: imports the gateway's app.admin_fabric_gitstate and runs _compute against a
planted, call-counting fake store. argv[1] = "ac1" | "ac2". Prints one result line, then "RESULT: PASS" or "RESULT: FAIL".

The gateway root is the worktree's infra/aws/ec2/opal-gateway, or $N1_GW when set (the issuer's positive control).
Run from the worktree root (the .sh wrappers cd there).
"""
from __future__ import annotations

import json
import os
import sys
from datetime import datetime, timedelta, timezone

GW = os.environ.get("N1_GW") or os.path.join("infra", "aws", "ec2", "opal-gateway")
sys.path.insert(0, os.path.abspath(GW))
os.environ.setdefault("MOCK_GRAPH", "1")

from botocore.exceptions import ClientError  # noqa: E402

g = __import__("app.admin_fabric_gitstate", fromlist=["_compute"])

PFX = "fabric/activity/v1/gitstate"
ROSTER = ["laptop", "sitez"]
NOW = datetime(2026, 10, 12, 8, 0, 0, tzinfo=timezone.utc)
SHA_OLD, SHA_NEW = "1" * 40, "2" * 40


class FakeS3:
    """list_objects_v2 paginator (Prefix, optional StartAfter, 1000 keys a page) + get_object over {key: body dict}.
    Counts every get_object call."""

    def __init__(self, store):
        self.store = store
        self.gets = 0

    def get_paginator(self, name):
        assert name == "list_objects_v2"
        outer = self

        class Pag:
            def paginate(self, Bucket, Prefix, StartAfter="", **_kw):
                keys = sorted(k for k in outer.store if k.startswith(Prefix) and k > StartAfter)
                for i in range(0, max(len(keys), 1), 1000):
                    yield {"Contents": [{"Key": k} for k in keys[i:i + 1000]]}

        return Pag()

    def get_object(self, Bucket, Key):
        self.gets += 1
        if Key not in self.store:
            raise ClientError({"Error": {"Code": "NoSuchKey", "Message": "no such key"}}, "GetObject")
        body = json.dumps(self.store[Key]).encode()

        class Body:
            def read(self_inner):
                return body

        return {"Body": Body()}


def _iso(t):
    return t.strftime("%Y-%m-%dT%H:%M:%SZ")


def _rec(box, t, trunk, mode="box", rc=0, note="n"):
    return {"schema": "fabric-gitstate/1", "box": box, "at": _iso(t),
            "pass": {"mode": mode, "rc": rc, "serial": "s-" + box, "note": note},
            "box_branch": "box/" + box, "box_head": "a" * 40, "origin_box_head": "a" * 40, "trunk_head": trunk,
            "unpushed": {"count": 0, "shas": [], "capped": False},
            "pushed_not_on_trunk": {"count": 0, "shas": [], "capped": False},
            "behind_trunk": 0, "unread": []}


def _put(store, rec, latest=False):
    stamp = rec["at"].replace("-", "").replace(":", "")
    store["%s/box=%s/%s.json" % (PFX, rec["box"], stamp)] = rec
    if latest:
        store["%s/box=%s/latest.json" % (PFX, rec["box"])] = rec


def _run(store):
    g._BODY_CACHE.clear()
    g._roster = lambda: list(ROSTER)
    g._now = lambda: NOW
    client = FakeS3(store)
    body = g._compute(client)
    return body, client.gets


def _history_store(days):
    """Per box: one record an hour for `days` days back from NOW. The trunk head moves to SHA_NEW 12 h before NOW, inside
    the 48 h window. Every pass is mode 'box', rc 0: no refusal and no integrate pass anywhere."""
    store = {}
    for box in ROSTER:
        n = days * 24
        for h in range(n, 0, -1):
            t = NOW - timedelta(hours=h) + timedelta(minutes=5)
            _put(store, _rec(box, t, SHA_NEW if h <= 12 else SHA_OLD), latest=(h == 1))
    return store


def ac1():
    s1, s10 = _history_store(5), _history_store(50)
    h1 = sum(1 for k in s1 if not k.endswith("latest.json"))
    h10 = sum(1 for k in s10 if not k.endswith("latest.json"))
    b1, n1 = _run(s1)
    b10, n10 = _run(s10)
    head_ok = b1["trunk"]["head"] == SHA_NEW[:12] and b10["trunk"]["head"] == SHA_NEW[:12]
    print("history 1x=%d 10x=%d; get_object 1x=%d 10x=%d; trunk head moved inside the window=%s"
          % (h1, h10, n1, n10, "yes" if head_ok else "no"))
    return n1 == n10 and n1 > 0 and h10 == 10 * h1 and head_ok


def ac2():
    base = NOW - timedelta(hours=20)
    # box laptop: a refusal, then a LATER successful integrate -> superseded -> "not recorded".
    # box sitez: a successful integrate, then a NEWER refusal -> {at, note}.
    store = {}
    for box in ROSTER:
        for h in range(30, 0, -1):
            _put(store, _rec(box, NOW - timedelta(hours=h), SHA_NEW), latest=(h == 1))
    _put(store, _rec("laptop", base, SHA_NEW, mode="integrate", rc=1, note="planted-superseded"))
    _put(store, _rec("laptop", base + timedelta(hours=3, minutes=1), SHA_NEW, mode="integrate", rc=0, note="ok"))
    _put(store, _rec("sitez", base, SHA_NEW, mode="integrate", rc=0, note="ok"))
    refused_at = base + timedelta(hours=3, minutes=1)
    _put(store, _rec("sitez", refused_at, SHA_NEW, mode="integrate", rc=1, note="planted-live"))
    body, _n = _run(store)
    rows = {b["box"]: b["integration_refused"] for b in body["boxes"]}
    sup, live = rows.get("laptop"), rows.get("sitez")
    print("superseded refusal reads %r; refusal newer than every integrate reads %r" % (sup, live))
    return (sup == "not recorded" and isinstance(live, dict) and live.get("at") == _iso(refused_at)
            and live.get("note") == "planted-live")


if __name__ == "__main__":
    ok = {"ac1": ac1, "ac2": ac2}[sys.argv[1]]()
    print("RESULT: PASS" if ok else "RESULT: FAIL")
    sys.exit(0 if ok else 1)
