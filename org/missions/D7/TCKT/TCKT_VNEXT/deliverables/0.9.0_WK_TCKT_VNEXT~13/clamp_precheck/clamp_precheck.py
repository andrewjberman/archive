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
every route is clamped.

A SECOND READ follows those lines (TO-R5-pc2): READ27 is a closed list of 27 routes and says nothing of a handler added later, so
from the SAME deployed lambda_function.py the precheck derives, with ast, every handler `lambda_handler` dispatches to (a module-level
function it returns a call of, passing the event as the first argument), gives each ONE class (PROFILE_SCOPE, ENV_FIRM_LIST,
SUBMIT_CONTEXT_FIRM, else UNCLASSED), prints `handler <name> <CLASS>` per handler and `TICKET_HANDLERS <classed>/<dispatched>`, and
writes the rows beside --out as <out stem>_ticket_handlers.json (the --out table is a JSON list, which has no top-level key to add).
Any UNCLASSED handler, or a deployed member whose handlers cannot be derived, makes the exit non-zero. Run from the workspace root with the `.tools/aws` shim available (read-only: lambda get-function and the
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
HANDLER_CLASSES = ("PROFILE_SCOPE", "ENV_FIRM_LIST", "SUBMIT_CONTEXT_FIRM")   # in the order a handler is classed; else UNCLASSED
ENV_LIST_SUFFIX = "_ALLOWED_FIRMS"
ACTOR_READER, FIRM_KEY = "_actor", "firmId"   # the authorizer-context reader and the key it puts the caller's firm under
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


def _module_funcs(tree):
    return {n.name: n for n in tree.body if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef))}


def dispatched_handlers(source):
    """The denominator, derived and never typed: the module-level functions that lambda_handler RETURNS a call of with its event
    (its first parameter) as the first argument, in source order. `return _resp(404, ...)` passes no event and is not a handler.
    Raises ValueError when the source does not parse or defines no lambda_handler."""
    try:
        tree = ast.parse(source)
    except (SyntaxError, ValueError) as e:
        raise ValueError("source does not parse: %s" % type(e).__name__)
    funcs = _module_funcs(tree)
    lh = funcs.get("lambda_handler")
    if lh is None or not lh.args.args:
        raise ValueError("no lambda_handler(event, ...) in the deployed member")
    event = lh.args.args[0].arg
    hits = []
    for n in ast.walk(lh):
        v = n.value if isinstance(n, ast.Return) else None
        if (isinstance(v, ast.Call) and isinstance(v.func, ast.Name) and v.func.id in funcs and v.args
                and isinstance(v.args[0], ast.Name) and v.args[0].id == event):
            hits.append((n.lineno, v.func.id))
    names = []
    for _ln, name in sorted(hits):
        if name not in names:
            names.append(name)
    return names, funcs


def _env_list_line(fn):
    """Line of a comparison of something against a module constant named *_ALLOWED_FIRMS, read in this function's own body."""
    for n in ast.walk(fn):
        if isinstance(n, ast.Compare):
            for side in [n.left] + list(n.comparators):
                if isinstance(side, ast.Name) and side.id.endswith(ENV_LIST_SUFFIX):
                    return n.lineno
    return None


def _context_firm_line(fn):
    """Line where the function takes the firm from the authorizer context: <var>["firmId"] where <var> = _actor(...)."""
    actors = {t.id for n in ast.walk(fn) if isinstance(n, ast.Assign) and isinstance(n.value, ast.Call)
              and isinstance(n.value.func, ast.Name) and n.value.func.id == ACTOR_READER
              for t in n.targets if isinstance(t, ast.Name)}
    for n in ast.walk(fn):
        if (isinstance(n, ast.Subscript) and isinstance(n.value, ast.Name) and n.value.id in actors
                and isinstance(n.slice, ast.Constant) and n.slice.value == FIRM_KEY):
            return n.lineno
    return None


def classify_handler(fn):
    """One row for one handler: the FIRST class that holds, the other classes that also hold, and the lines that decide."""
    called = _called_names(fn)
    held = {}
    direct = sorted(called & (set(CLAMP_HELPERS) | set(CLAMP_WRAPPERS)))
    if direct:
        held["PROFILE_SCOPE"] = "calls " + ", ".join(direct)
    ln = _env_list_line(fn)
    if ln:
        held["ENV_FIRM_LIST"] = "compares against a *_ALLOWED_FIRMS constant at line %d" % ln
    ln = _context_firm_line(fn)
    if ln:
        held["SUBMIT_CONTEXT_FIRM"] = "reads the firm from the authorizer context at line %d" % ln
    order = [c for c in HANDLER_CLASSES if c in held]
    return {"handler": fn.name, "line": fn.lineno, "class": order[0] if order else "UNCLASSED",
            "also": order[1:], "basis": held, "claim": "measured"}


def ticket_handler_rows(deployed):
    """Returns (rows, why). rows is None with a reason when the handlers cannot be derived (never an empty pass)."""
    if deployed is None:
        return None, "the deployed %s was not read" % TICKET_MEMBER
    try:
        names, funcs = dispatched_handlers(deployed.decode("utf-8"))
    except UnicodeDecodeError:
        return None, "deployed member is not utf-8"
    except ValueError as e:
        return None, str(e)
    if not names:
        return None, "lambda_handler dispatches to no module-level function"
    return [classify_handler(funcs[n]) for n in names], ""


def build_table(routes, source_map_path, capture=None):
    """One row per host. Looks the three readers up at call time, so a test can replace them on the module.
    `capture`, when a dict, receives the deployed ticket member's bytes under "ticket_member" (the second read's input)."""
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
        if capture is not None and fn == TICKET_FN:
            try:
                capture["ticket_member"] = _member_bytes(pkg, TICKET_MEMBER)
            except Exception:  # noqa: BLE001 -- ticket_decision names an unreadable package; the second read then reads nothing
                capture["ticket_member"] = None
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
    captured = {}
    table = build_table(census_routes(a.census), a.source_map, captured)
    for t in table:
        print("%-26s %d %s %s %s%s" % (t["function"], t["n_routes"], (t["last_modified"] or "-")[:19],
                                       (t["member_sha256"] or "ABSENT")[:8], t["verdict"],
                                       (" " + t["detail"]) if t["verdict"] != "CLAMPED" and t["detail"] else ""))
    done = sum(t["n_routes"] for t in table if t["clamp_live"])
    total = sum(t["n_routes"] for t in table)
    Path(a.out).write_text(json.dumps(table, indent=1) + "\n", encoding="utf-8")
    print("READ27 %d/%d" % (done, total))
    rc = 0 if total and done == total else 1
    if any(t["function"] == TICKET_FN for t in table):
        rows, why = ticket_handler_rows(captured.get("ticket_member"))
        out2 = Path(a.out)
        out2 = out2.with_name(out2.stem + "_ticket_handlers.json")
        if rows is None:
            print("TICKET_HANDLERS UNREADABLE %s" % why)
            out2.write_text(json.dumps({"ticket_handlers": None, "why": why, "claim": "absent"}, indent=1) + "\n", encoding="utf-8")
            return 1
        for r in rows:
            print("handler %s %s" % (r["handler"], r["class"]))
        classed = [r for r in rows if r["class"] != "UNCLASSED"]
        bad = [r["handler"] for r in rows if r["class"] == "UNCLASSED"]
        print("TICKET_HANDLERS %d/%d%s" % (len(classed), len(rows), (" UNCLASSED " + ",".join(bad)) if bad else ""))
        out2.write_text(json.dumps({"ticket_handlers": rows, "dispatched": len(rows), "classed": len(classed)}, indent=1) + "\n",
                        encoding="utf-8")
        if bad:
            rc = 1
    return rc


if __name__ == "__main__":
    sys.exit(main())
