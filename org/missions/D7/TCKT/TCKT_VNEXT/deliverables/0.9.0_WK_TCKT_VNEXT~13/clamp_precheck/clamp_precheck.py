"""TCKT_VNEXT round 3 -- the clamp precheck: which of the 27 formerly-MORE_THAN_ONE routes run the firm clamp LIVE, read from each
host's DEPLOYED bytes. Replaces the role of R1_RUN/reread_27.py (which is left as it was).

  - Investor Reporting hosts: the deployed `served.py` must hash to a member of SERVED_RELEASES (the other project's signed
    release list, copied unchanged from reread_27.py).
  - opal-ticket-api: decided from the deploy record and the deployed content, with no typed list of builds. CLAMPED only when
      1. the live CodeSha256 equals the source map's `artifact_sha256`                       (else MAP-STALE)
      2. the deployed lambda_function.py hashes to `git show <last_deployed_commit>:<source_dir>/lambda_function.py`
                                                                                            (else NOT-THE-RECORDED-FILE)
      3. the DEPLOYED source (parsed with ast, never imported) defines _profile_scope, _resolve_scope and _in_profile_scope
         and each handler in HANDLERS calls one of them, directly or through a defined wrapper (_firm_allowed /
         _create_firm_allowed) that itself calls one of them                                (else CLAMP-ABSENT, naming it)
    Anything that cannot be read is UNREADABLE and never counted as clamped.

Prints one line per host and `READ27 <clamped>/<total>`; writes the table as JSON to the REQUIRED --out path. Exit 0 only when
every route is clamped. Run from the workspace root with the `.tools/aws` shim available (read-only: lambda get-function and the
presigned package download). Importing this module makes no AWS, network or git call.
"""
import argparse
import ast
import collections
import hashlib
import io
import json
import subprocess
import sys
import urllib.request
import zipfile
from pathlib import Path

CENSUS = "org/missions/D7/TCKT/TCKT_VNEXT/deliverables/0.9.0_WK_TCKT_VNEXT~6/SA_ROUTE_CENSUS.json"
SOURCE_MAP = "infra/aws/lambda/ci/lambda-source-map.json"
TICKET_FN = "opal-ticket-api"
TICKET_MEMBER = "lambda_function.py"
IRPT_MEMBER = "served.py"

# The other project's signed release list, copied from reread_27.py unchanged.
SERVED_RELEASES = {
    "87d9ecc49747f777fd6ec02c3aa82cbe5b9f53edf9d903faf2d87d7582e1b3b6": "IB-pr-390",
    "ada9bf5bcfd107398eacf49d8051e61551ff253c33cf216d9dd404363f7e630e": "IB-pr-409 (390 + 405)",
}

CLAMP_HELPERS = ("_profile_scope", "_resolve_scope", "_in_profile_scope")
CLAMP_WRAPPERS = ("_firm_allowed", "_create_firm_allowed")
HANDLERS = ("create_ticket", "list_tickets", "metrics", "get_ticket", "claim_ticket", "complete_ticket", "report_ticket")


# ---- the three outside reads (each replaceable by a test) -------------------------------------------------------------------

def read_function(name):
    """AWS read of one function: returns (configuration dict, package zip bytes). Raises on any failure."""
    r = subprocess.run(["bash", ".tools/aws", "lambda", "get-function", "--function-name", name, "--output", "json"],
                       capture_output=True, text=True, timeout=120)
    if r.returncode != 0:
        raise RuntimeError("get-function %s rc=%d %s" % (name, r.returncode, r.stderr.strip()[:200]))
    f = json.loads(r.stdout)
    pkg = urllib.request.urlopen(f["Code"]["Location"], timeout=120).read()
    return f["Configuration"], pkg


def read_git_file(commit, path):
    """git read of one file at one commit: returns the bytes. Raises on any failure."""
    r = subprocess.run(["git", "show", "%s:%s" % (commit, path)], capture_output=True, timeout=120)
    if r.returncode != 0:
        raise RuntimeError("git show %s:%s rc=%d" % (commit, path, r.returncode))
    return r.stdout


def read_source_map(path):
    """Source-map read: returns the parsed JSON document. Raises on any failure."""
    return json.loads(Path(path).read_text(encoding="utf-8"))


# ---- pure helpers -----------------------------------------------------------------------------------------------------------

def census_routes(census_path):
    census = json.loads(Path(census_path).read_text(encoding="utf-8"))
    routes = collections.defaultdict(list)
    for row in census["rows"]:
        if any(v.get("verdict") == "MORE_THAN_ONE" for v in row["per_token"].values()):
            routes[row["function"]].append(row["method"] + " " + row["route"])
    return dict(routes)


def _member_bytes(pkg, member):
    z = zipfile.ZipFile(io.BytesIO(pkg))
    return z.read(member) if member in z.namelist() else None


def _sha_hex(b):
    return hashlib.sha256(b).hexdigest()


def _called_names(node):
    return {n.func.id for n in ast.walk(node) if isinstance(n, ast.Call) and isinstance(n.func, ast.Name)}


def clamp_absent(source):
    """Parse the deployed source (never import it). Returns None when the clamp is present, else a string naming what failed.

    Rule (encoded from infra/aws/lambda/ticket_center/lambda_function.py): the three helpers are module-level functions; a
    handler is clamped when it calls a helper directly, or calls a defined wrapper (_firm_allowed / _create_firm_allowed)
    whose own body calls a helper. At the recorded code every handler calls _resolve_scope directly."""
    try:
        tree = ast.parse(source)
    except (SyntaxError, ValueError) as e:
        return "source does not parse: %s" % type(e).__name__
    funcs = {n.name: n for n in tree.body if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef))}
    missing = [h for h in CLAMP_HELPERS if h not in funcs]
    if missing:
        return "helper not defined: %s" % ", ".join(missing)
    reach = set(CLAMP_HELPERS)
    for w in CLAMP_WRAPPERS:
        if w in funcs and _called_names(funcs[w]) & set(CLAMP_HELPERS):
            reach.add(w)
    bad = []
    for h in HANDLERS:
        if h not in funcs:
            bad.append("%s (not defined)" % h)
        elif not (_called_names(funcs[h]) & reach):
            bad.append("%s (calls no clamp helper)" % h)
    if bad:
        return "handler without the clamp: %s" % ", ".join(bad)
    return None


def ticket_decision(cfg, pkg, entry, git_reader):
    """Returns (verdict, detail, member_sha256_hex_or_None) for opal-ticket-api. verdict is CLAMPED or a named refusal."""
    try:
        deployed = _member_bytes(pkg, TICKET_MEMBER)
    except Exception as e:  # noqa: BLE001 -- an unreadable package is UNREADABLE, never clamped
        return "UNREADABLE", "package: %s" % type(e).__name__, None
    if deployed is None:
        return "UNREADABLE", "package has no %s" % TICKET_MEMBER, None
    h = _sha_hex(deployed)
    try:
        want_sha = entry["artifact_sha256"]
        commit = entry["last_deployed_commit"]
        src_dir = entry["source_dir"]
        if not (want_sha and commit and src_dir):
            raise KeyError("empty")
    except (KeyError, TypeError):
        return "UNREADABLE", "map entry lacks artifact_sha256 / last_deployed_commit / source_dir", h
    if cfg.get("CodeSha256") != want_sha:
        return "MAP-STALE", "live CodeSha256 %s is not the map's" % str(cfg.get("CodeSha256"))[:12], h
    try:
        recorded = git_reader(commit, src_dir.rstrip("/") + "/" + TICKET_MEMBER)
    except Exception as e:  # noqa: BLE001
        return "UNREADABLE", "recorded file at %s: %s" % (commit[:10], type(e).__name__), h
    if _sha_hex(recorded) != h:
        return "NOT-THE-RECORDED-FILE", "deployed %s is not the file at %s" % (h[:8], commit[:10]), h
    try:
        why = clamp_absent(deployed.decode("utf-8"))
    except UnicodeDecodeError:
        return "UNREADABLE", "deployed member is not utf-8", h
    if why:
        return "CLAMP-ABSENT", why, h
    return "CLAMPED", "map, recorded file and clamp agree", h


def irpt_decision(pkg):
    try:
        data = _member_bytes(pkg, IRPT_MEMBER)
    except Exception as e:  # noqa: BLE001
        return "UNREADABLE", "package: %s" % type(e).__name__, None
    if data is None:
        return "NOT-RELEASED", "package has no %s" % IRPT_MEMBER, None
    h = _sha_hex(data)
    return ("CLAMPED" if h in SERVED_RELEASES else "NOT-RELEASED"), SERVED_RELEASES.get(h, ""), h


def build_table(routes, source_map_path):
    """One row per host. Looks the three readers up at call time, so a test can replace them on the module."""
    table = []
    entry, entry_err = None, None
    if TICKET_FN in routes:
        try:
            entry = read_source_map(source_map_path)["functions"][TICKET_FN]
        except Exception as e:  # noqa: BLE001
            entry_err = type(e).__name__
    for fn, rs in sorted(routes.items()):
        row = {"function": fn, "routes": rs, "n_routes": len(rs), "code_sha256": None, "last_modified": None,
               "member": TICKET_MEMBER if fn == TICKET_FN else IRPT_MEMBER, "member_sha256": None, "verdict": "UNREADABLE",
               "detail": "", "clamp_live": False, "release": None, "claim": "measured"}
        try:
            cfg, pkg = read_function(fn)
            row["code_sha256"], row["last_modified"] = cfg.get("CodeSha256"), cfg.get("LastModified")
        except Exception as e:  # noqa: BLE001
            row["detail"] = "function read: %s" % type(e).__name__
            table.append(row)
            continue
        if fn == TICKET_FN:
            if entry is None:
                v, d, h = "UNREADABLE", "source map entry: %s" % entry_err, None
            else:
                v, d, h = ticket_decision(cfg, pkg, entry, read_git_file)
        else:
            v, d, h = irpt_decision(pkg)
            row["release"] = d or None
        row.update(verdict=v, detail=d, member_sha256=h, clamp_live=(v == "CLAMPED"))
        table.append(row)
    return table


def main(argv=None):
    ap = argparse.ArgumentParser(description="TCKT_VNEXT clamp precheck (read-only)")
    ap.add_argument("--out", required=True, help="path the table JSON is written to")
    ap.add_argument("--source-map", default=SOURCE_MAP, help="lambda-source-map.json path")
    ap.add_argument("--census", default=CENSUS, help="route census JSON path")
    a = ap.parse_args(argv)
    table = build_table(census_routes(a.census), a.source_map)
    for t in table:
        print("%-26s %d %s %s %s%s" % (t["function"], t["n_routes"], (t["last_modified"] or "-")[:19],
                                       (t["member_sha256"] or "ABSENT")[:8], t["verdict"],
                                       (" " + t["detail"]) if t["verdict"] != "CLAMPED" and t["detail"] else ""))
    done = sum(t["n_routes"] for t in table if t["clamp_live"])
    total = sum(t["n_routes"] for t in table)
    Path(a.out).write_text(json.dumps(table, indent=1) + "\n", encoding="utf-8")
    print("READ27 %d/%d" % (done, total))
    return 0 if total and done == total else 1


if __name__ == "__main__":
    sys.exit(main())
