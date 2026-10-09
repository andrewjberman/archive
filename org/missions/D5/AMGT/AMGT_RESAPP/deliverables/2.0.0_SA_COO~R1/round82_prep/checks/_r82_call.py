"""Shared GET helper for the round-82 API checks: --where local runs the handler in-process on the tree, --where deployed
invokes the live function (read only, GET-shaped, as round79/checks/r79_cc6.py does)."""
from __future__ import annotations

import json
import subprocess
import sys

FN = "opal-amgt-scoped-api"
PREFIX = "/api/scoped/amgt"


def caller(where):
    root = subprocess.run(["git", "rev-parse", "--show-toplevel"], capture_output=True, text=True).stdout.strip()
    if root not in sys.path:
        sys.path.insert(0, root)
    if where == "deployed":
        import boto3

        lam = boto3.client("lambda", region_name="us-east-1")

        def raw(event):
            return json.loads(lam.invoke(FunctionName=FN, Payload=json.dumps(event).encode())["Payload"].read())
    else:
        from lib.research.api import scoped_amgt

        def raw(event):
            return scoped_amgt.handler(event)

    def get(path, query=None):
        event = {"rawPath": PREFIX + path, "requestContext": {"http": {"method": "GET"}}, "headers": {"x-firm-id": "opal"},
                 "queryStringParameters": query}
        try:
            r = raw(event)
            return r.get("statusCode"), json.loads(r.get("body") or "{}")
        except Exception as err:  # noqa: BLE001 -- a failed read is a FAIL line, never a crash
            return "%s: %s" % (type(err).__name__, str(err)[:120]), {}

    return get


def find(node, key):
    if isinstance(node, dict):
        if key in node:
            return node[key]
        for value in node.values():
            hit = find(value, key)
            if hit is not None:
                return hit
    elif isinstance(node, list):
        for value in node:
            hit = find(value, key)
            if hit is not None:
                return hit
    return None


def say(ok, label):
    print("%s %s" % ("PASS" if ok else "FAIL", label))
    return ok
