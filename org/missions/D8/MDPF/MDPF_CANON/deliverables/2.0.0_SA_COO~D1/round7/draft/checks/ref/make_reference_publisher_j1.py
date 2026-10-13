"""Scratch REFERENCE publisher for CN-j-1 (the history leaf).  Issuer tool, never a product path.

Copies infra/aws/lambda/opal-assets/opal-assets-mdpf-portal-publisher (lambda_function.py + tests/*.py only) from a repo root into
<dest>/infra/aws/lambda/opal-assets/opal-assets-mdpf-portal-publisher and applies the MINIMUM edit the order describes.  It proves the three arms
of r7_cn_j_1.py can pass; it is not the worker's code and is never copied back.

    python make_reference_publisher_j1.py <repo_root> <dest_root> [--mutant m1|m2]

m1: absent becomes zero (a missing Client node is read as 0.0).   m2: the history leaf ignores the pointer (always rewritten).
"""
from __future__ import annotations

import os
import re
import shutil
import sys

REL = "infra/aws/lambda/opal-assets/opal-assets-mdpf-portal-publisher"

HISTORY_BLOCK = '''# --- FWD-9 history leaf (MDPF_CANON CN-j-1) --------------------------------------------------------------------
# ONE derived leaf per scope that holds dated category-views objects: platinum/mdpf/{scope}/category-views-history.json,
# carrying only dates[] and the two Client aum arrays.  This is the one place this publisher assembles a served object that
# is not a 1:1 projection of a gold key (CTO ruling msgs 5086-5088, PRD v2.15); it reads only the dated category-views
# objects it already lists, never the platinum plane, and adds no field to any gold-projected leaf.
HISTORY_LEAF = "category-views-history"
HISTORY_SCHEMA = "mdpf-category-views-history/v1"
HISTORY_SOURCE_TYPE = "category-views"
CLIENT_SUPERVISED = "Client - Opal Supervised"
CLIENT_UNSUPERVISED = "Client - Opal Unsupervised"


def _client_aum(doc, name):
    """The Client child's aum, or None.  Absent is not zero: a missing node and a non-number are None; a measured 0.0 stays 0.0."""
    try:
        v = doc["nodes"]["Client"]["children"][name]["aum"]
    except (KeyError, TypeError, IndexError):
        return None
    if isinstance(v, bool) or not isinstance(v, (int, float)):
        return None
    return v


def assemble_history_leaf(scope, dated):
    """dated: iterable of (YYYY-MM-DD, body bytes) -> (content dict, omitted list).  Pure and deterministic: ascending by date;
    an unparseable or non-object body, or a body whose own as_of differs from its key date, is OMITTED and named, never filled."""
    rows, omitted = [], []
    for date, body in sorted(dated, key=lambda t: t[0]):
        try:
            doc = json.loads(body)
        except Exception:  # noqa: BLE001 -- named below
            omitted.append({"date": date, "reason": "unparseable"})
            continue
        if not isinstance(doc, dict):
            omitted.append({"date": date, "reason": "not_an_object"})
            continue
        as_of = doc.get("as_of")
        if as_of is not None and str(as_of)[:10] != date:
            omitted.append({"date": date, "reason": "as_of_differs_from_key"})
            continue
        rows.append((date, _client_aum(doc, CLIENT_SUPERVISED), _client_aum(doc, CLIENT_UNSUPERVISED)))
    content = {"schema": HISTORY_SCHEMA, "leaf": HISTORY_LEAF, "scope": scope, "n_dates": len(rows),
               "dates": [r[0] for r in rows],
               "client_supervised": [r[1] for r in rows],
               "client_unsupervised": [r[2] for r in rows],
               "omitted": omitted}
    return content, omitted


def _content_sha(content):
    return _sha256(json.dumps(content, sort_keys=True, separators=(",", ":")).encode("utf-8"))


def _publish_history_one(s3, scope, prior_history):
    """D5+D6 for the history leaf: rebuild from the dated objects, hash the content, unchanged => no write; failure never sinks the run."""
    pair = f"{scope}/{HISTORY_LEAF}"
    serve_key = f"{SERVE_ROOT}/{scope}/{HISTORY_LEAF}.json"
    row = {"serve_key": serve_key, "status": "error", "published": False}
    try:
        root = GOLD_ROOT.rstrip("/") + "/"
        dated_keys = []
        for obj in _list_all(s3, GOLD_BUCKET, f"{root}{scope}/{HISTORY_SOURCE_TYPE}/"):
            m = _KEY_RE.match(obj["Key"][len(root):])
            if m and m.group(1) == scope and m.group(2) == HISTORY_SOURCE_TYPE:
                dated_keys.append((m.group(3), obj["Key"]))
        dated_keys.sort()
        dated = [(d, s3.get_object(Bucket=GOLD_BUCKET, Key=k)["Body"].read()) for d, k in dated_keys]
        content, omitted = assemble_history_leaf(scope, dated)
        sha = _content_sha(content)
        row.update({"content_sha256": sha, "n_dates": content["n_dates"], "n_source_objects": len(dated_keys), "omitted": omitted})
        prior = prior_history.get(pair)
        if prior and prior.get("content_sha256") == sha and _list_one(s3, SERVE_BUCKET, serve_key) is not None:
            row["status"] = "unchanged"
            _log(f"UNCHANGED: {pair} (content sha unchanged) -- no write")
            return row
        doc = dict(content)
        doc["_provenance"] = {
            "written_by": "opal-assets-mdpf-portal-publisher",
            "written_at": dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
            "source_keys": [f"s3://{GOLD_BUCKET}/{dated_keys[0][1]}", f"s3://{GOLD_BUCKET}/{dated_keys[-1][1]}"] if dated_keys else [],
            "source_count": len(dated_keys),
            "source_vintages": {pair: dated_keys[-1][0] if dated_keys else None},
        }
        payload = json.dumps(doc, separators=(",", ":")).encode("utf-8")
        s3.put_object(Bucket=SERVE_BUCKET, Key=serve_key, Body=payload, ContentType="application/json")
        dst = _list_one(s3, SERVE_BUCKET, serve_key)
        if dst is None:
            row["status"] = "verify_absent"
            return row
        _log(f"OK: published {pair} ({content['n_dates']} dates, {len(omitted)} omitted) -> s3://{SERVE_BUCKET}/{serve_key} ({dst['Size']:,}B)")
        row.update({"status": "published", "published": True, "size": dst["Size"], "etag": dst.get("ETag")})
        return row
    except Exception as exc:  # noqa: BLE001 -- per-key isolation (D6)
        _log(f"ERROR: history leaf failed {pair}: {type(exc).__name__}: {exc}")
        row["error"] = f"{type(exc).__name__}: {exc}"
        return row


def load_latest_pointer_doc(s3):
    """The pointer document (rows + history_rows), one read.  Absent/unreadable => ({}, reason): first-run semantics, recorded."""
    try:
        raw = s3.get_object(Bucket=SERVE_BUCKET, Key=_latest_pointer_key())["Body"].read()
        return json.loads(raw), None
    except Exception as exc:  # noqa: BLE001 -- publish-all, recorded
        return {}, f"{type(exc).__name__}: {exc}"


'''


def _replace_once(text, old, new, what):
    n = text.count(old)
    if n != 1:
        raise SystemExit("reference patch: anchor %r found %d times (expected 1)" % (what, n))
    return text.replace(old, new)


def build(repo_root, dest_root, mutant=None):
    src = os.path.join(repo_root, *REL.split("/"))
    dst = os.path.join(dest_root, *REL.split("/"))
    if os.path.exists(dst):
        shutil.rmtree(dst)
    os.makedirs(os.path.join(dst, "tests"))
    shutil.copy(os.path.join(src, "lambda_function.py"), os.path.join(dst, "lambda_function.py"))
    for name in os.listdir(os.path.join(src, "tests")):
        if name.endswith(".py"):
            shutil.copy(os.path.join(src, "tests", name), os.path.join(dst, "tests", name))
    p = os.path.join(dst, "lambda_function.py")
    t = open(p, encoding="utf-8", newline="").read()
    t = _replace_once(t, "def _publish_one(", HISTORY_BLOCK + "def _publish_one(", "_publish_one")
    t = _replace_once(t, "    prior_rows, pointer_err = load_latest_pointer(s3)\n",
                      "    pointer_doc, pointer_err = load_latest_pointer_doc(s3)\n"
                      "    prior_rows = pointer_doc.get(\"rows\", {})\n"
                      "    prior_history = pointer_doc.get(\"history_rows\", {})\n", "pointer read")
    t = _replace_once(t, "    # --- bidirectional completeness (D8)\n",
                      "    history_scopes = sorted({s for (s, ty) in publish if ty == HISTORY_SOURCE_TYPE})\n"
                      "    history_rows = {f\"{s}/{HISTORY_LEAF}\": _publish_history_one(s3, s, prior_history) for s in history_scopes}\n\n"
                      "    # --- bidirectional completeness (D8)\n", "completeness marker")
    t = _replace_once(t, "        \"rows\": results,\n", "        \"rows\": results,\n        \"history_rows\": history_rows,\n", "manifest rows")
    t = _replace_once(t, "                                   \"rows\": pointer_rows}, indent=2)",
                      "                                   \"rows\": pointer_rows, \"history_rows\": pointer_history}, indent=2)", "pointer write")
    t = _replace_once(t, "    s3.put_object(Bucket=SERVE_BUCKET, Key=_latest_pointer_key(),\n",
                      "    pointer_history = {}\n"
                      "    for pair, r in history_rows.items():\n"
                      "        if r[\"status\"] in (\"published\", \"unchanged\") and r.get(\"content_sha256\"):\n"
                      "            pointer_history[pair] = {\"content_sha256\": r[\"content_sha256\"]}\n"
                      "        elif pair in prior_history:\n"
                      "            pointer_history[pair] = prior_history[pair]\n"
                      "    s3.put_object(Bucket=SERVE_BUCKET, Key=_latest_pointer_key(),\n", "pointer put")
    if mutant == "m1":
        t = _replace_once(t, "    except (KeyError, TypeError, IndexError):\n        return None\n    if isinstance(v, bool)",
                          "    except (KeyError, TypeError, IndexError):\n        return 0.0\n    if isinstance(v, bool)", "m1")
    if mutant == "m2":
        t = _replace_once(t, "        if prior and prior.get(\"content_sha256\") == sha and _list_one(",
                          "        if False and prior and prior.get(\"content_sha256\") == sha and _list_one(", "m2")
    open(p, "w", encoding="utf-8", newline="").write(t)
    # the existing completeness test counts the 18 gold pairs' serve writes; the history leaves are asserted in their own tests
    q = os.path.join(dst, "tests", "test_completeness.py")
    u = open(q, encoding="utf-8", newline="").read()
    u2 = re.sub(r'if not (k2?)\.startswith\("platinum/mdpf/_manifests/"\)\]',
                lambda m: 'if not %s.startswith("platinum/mdpf/_manifests/") and not %s.endswith("category-views-history.json")]' % (m.group(1), m.group(1)),
                u)
    if u2 == u:
        raise SystemExit("reference patch: no serve-write filter found in test_completeness.py")
    open(q, "w", encoding="utf-8", newline="").write(u2)
    return dst


if __name__ == "__main__":
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    mut = None
    if "--mutant" in sys.argv:
        mut = sys.argv[sys.argv.index("--mutant") + 1]
        args = [a for a in args if a != mut]
    if len(args) != 2:
        raise SystemExit(__doc__)
    print(build(args[0], args[1], mut))
