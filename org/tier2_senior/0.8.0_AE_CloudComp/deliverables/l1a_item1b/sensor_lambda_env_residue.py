"""L1a residue sensor (item-1b RE-TARGET per CTO~Z ruling 20260725T114444Z) --
a Lambda's ASSUMED env keys vs the LIVE function configuration.
THE NON-TEXT SHAPE: the per-variable surface has NO prose facility -- doc_only
is N/A BY SHAPE, demonstrated at FIELD level (the bounce's lesson applied).

Subject: inf-gold-trigger (the kill-switch holder). READ-ONLY ALWAYS:
`get-function-configuration` only; the INF_GOLD_DISPATCH_RELEASE kill-switch is
LAW-protected (never write, never trigger) and env-var VALUES are never printed
(keys only).

THE FIELD-LEVEL SHAPE ARGUMENT (pre-checked before build, per the ruling):
  get-function-configuration top-level fields enumerated live; `Environment`
  carries exactly ONE field, `Variables` -- a flat str->str map. There is no
  third slot per variable, so no per-variable prose facility exists ANYWHERE on
  this surface. Function-level `Description` and `Tags` (get-function) are
  FUNCTION-kind surfaces, explicitly distinct -- a prose plane about the
  FUNCTION is not a prose plane about a VARIABLE. The sensor's --oracle-check
  re-enumerates these field lists every run so the claim remains falsifiable
  by its own instrument (the comment-column lesson, closed).

DERIVED, NEVER HAND-DECLARED:
  ASSUMED plane: literal os.environ reads extracted from the subject's own
  source via ast (os.environ.get('K') / os.environ['K'] / os.getenv('K')).
  A NON-LITERAL key expression is UNKNOWN (reported, never guessed).
  LIVE plane: aws lambda get-function-configuration (read-only), keys of
  Environment.Variables. API failure -> REFUSE UNKNOWN-grade (throttle/denied/
  absent-function are not FAILs of the surface and never silent PASSes).

CELLS (units = env-var names on the source-assumed ∪ live-set surface;
address_space=lambda_env_key -- native, new, BR008-visible):
  covered  = source-read AND live-set
  member   = live-set, never source-read (the deploy plane declares it; a row
             under a known axis -- set-but-unread, the inverse direction)
  orphan   = source-read but ABSENT live (the read silently defaults -- the
             dangerous direction)
  doc_only = applicable=false, count=null -- N/A BY SHAPE (above)

EXIT: 0 CLEAN / 2 VERDICT / 3 REFUSE / 1 FAIL. ASCII-only.
"""
from __future__ import annotations

import argparse
import ast
import json
import sys
from pathlib import Path

_THIS = Path(__file__).resolve()
_WORKSPACE = _THIS.parents[5]
sys.path.insert(0, str(_WORKSPACE / "org" / "modules" / "graph"))

import boundary_report  # noqa: E402

DEFAULT_FUNCTION = "inf-gold-trigger"
DEFAULT_SOURCE = _WORKSPACE / "infra" / "aws" / "lambda" / "inf-pipeline" / "inf-gold-trigger" / "lambda_function.py"


def assumed_env_keys(src_path: Path):
    """(literal_keys:set, unknown:list) -- ast walk for os.environ/os.getenv reads."""
    try:
        tree = ast.parse(src_path.read_text(encoding="utf-8", errors="replace"))
    except SyntaxError:
        return None, [("-", "source unparseable by ast")]
    keys, unknown = set(), []

    def _env_key_arg(node):
        if isinstance(node, ast.Constant) and isinstance(node.value, str):
            keys.add(node.value)
        else:
            unknown.append((ast.dump(node)[:60], "non-literal env key expression"))

    for node in ast.walk(tree):
        # os.environ['K'] / os.environ.get('K') / os.getenv('K')
        if isinstance(node, ast.Subscript):
            v = node.value
            if (isinstance(v, ast.Attribute) and v.attr == "environ"
                    and isinstance(v.value, ast.Name) and v.value.id == "os"):
                _env_key_arg(node.slice)
        elif isinstance(node, ast.Call):
            f = node.func
            if (isinstance(f, ast.Attribute) and f.attr == "get"
                    and isinstance(f.value, ast.Attribute) and f.value.attr == "environ"
                    and isinstance(f.value.value, ast.Name) and f.value.value.id == "os"
                    and node.args):
                _env_key_arg(node.args[0])
            elif (isinstance(f, ast.Attribute) and f.attr == "getenv"
                    and isinstance(f.value, ast.Name) and f.value.id == "os" and node.args):
                _env_key_arg(node.args[0])
    return keys, unknown


def live_env(function_name: str):
    """(config:dict, err) -- read-only get-function-configuration.

    Routed via .tools/msys_argv_guard.msys_safe_run per CLAUDE.md's generalized
    native-parent/POSIX-child rule (2026-07-25): a bare `aws` in native-Python
    argv CreateProcess-fails (the estate's aws shim is a bash script; mechanism C
    -- exercised live by this sensor's first oracle-check, FileNotFoundError)."""
    sys.path.insert(0, str(_WORKSPACE / ".tools"))
    from msys_argv_guard import msys_safe_run  # noqa: E402
    try:
        r = msys_safe_run(
            ["aws", "lambda", "get-function-configuration",
             "--function-name", function_name, "--output", "json"],
            capture_output=True, text=True, timeout=60, cwd=str(_WORKSPACE))
    except Exception as e:  # noqa: BLE001
        return None, "%s: %s" % (type(e).__name__, e)
    if r.returncode != 0:
        return None, "aws rc=%d: %s" % (r.returncode, (r.stderr or "").strip()[:200])
    try:
        return json.loads(r.stdout), None
    except ValueError as e:
        return None, "unparseable API response: %s" % e


def main() -> int:
    ap = argparse.ArgumentParser(
        prog="sensor_lambda_env_residue",
        description="item-1b re-target: assumed env keys vs live Lambda config. "
                    "Exit: 0 CLEAN / 2 VERDICT / 3 REFUSE / 1 FAIL.")
    ap.add_argument("--function", default=DEFAULT_FUNCTION)
    ap.add_argument("--source", default=str(DEFAULT_SOURCE),
                    help="the subject's own source file (mutant: point at the fixture)")
    ap.add_argument("--oracle-check", action="store_true",
                    help="field-level control of the LIVE oracle, then exit")
    ap.add_argument("--out", default=None)
    args = ap.parse_args()

    if args.oracle_check:
        cfg, err = live_env(args.function)
        if err:
            print("REFUSE: live oracle unevaluable (%s) -- UNKNOWN-grade." % err)
            return 3
        print("ORACLE fields: get-function-configuration -> %s" % sorted(cfg.keys()))
        env = cfg.get("Environment", {})
        print("ORACLE fields: Environment -> %s" % sorted(env.keys()))
        v = env.get("Variables", {})
        print("ORACLE per-variable shape: flat map, %d key(s), value types %s -- NO third "
              "slot, NO per-variable prose facility (keys only, values withheld)."
              % (len(v), sorted({type(x).__name__ for x in v.values()})))
        print("ORACLE distinct-surface note: function-level Description=%r (present-but-"
              "function-kind) and Tags (get-function) are NOT per-variable planes."
              % (cfg.get("Description", "")))
        cfg2, err2 = live_env(args.function + "-zzz-nonexistent-9999")
        if err2:
            print("ORACLE negative: nonexistent function errored as required (%s). "
                  "Oracle discriminates both ways." % err2.split(":")[0])
        else:
            print("FAIL: oracle cannot say NO (nonexistent function returned a config).")
            return 1
        return 0

    src = Path(args.source)
    if not src.is_file():
        print("FAIL: source does not exist: %s (a nonexistent domain is not an empty one)." % src)
        return 1
    keys, unknown = assumed_env_keys(src)
    if keys is None:
        print("FAIL: source unparseable by ast -- cannot derive the assumed plane.")
        return 1
    if not keys and not unknown:
        print("REFUSE: zero env reads extracted from %s -- nothing could be compared." % src.name)
        return 3

    cfg, err = live_env(args.function)
    if err:
        print("REFUSE (API-UNAVAILABLE/UNKNOWN-grade): %s -- never a FAIL of the surface, "
              "never a silent PASS." % err)
        return 3
    live = set(cfg.get("Environment", {}).get("Variables", {}).keys())
    revision = cfg.get("RevisionId", "UNRESOLVED")

    covered = sorted(keys & live)
    orphan = sorted(keys - live)
    member = sorted(live - keys)
    surface_total = len(covered) + len(member) + len(orphan)

    report = {
        "tool": "inf-gold-trigger (lambda env reader)",
        "source": "%s (assumed plane) vs live get-function-configuration %s" % (
            src.name, args.function),
        "address_space": "lambda_env_key",
        "head": "revision:%s" % revision,
        "surface_total": surface_total,
        "cells": {
            "covered": {"applicable": True, "count": len(covered), "method": "mention"},
            "member": {"applicable": True, "count": len(member), "method": "traversal"},
            "doc_only": {"applicable": False, "count": None, "method": None},
            "orphan": {"applicable": True, "count": len(orphan), "method": "mention"},
        },
        "doc_only_na_reason": (
            "N/A BY SHAPE, demonstrated at FIELD level (--oracle-check re-derives every "
            "run): Environment carries exactly one field, Variables, a flat str->str map "
            "with no third slot -- no per-variable prose facility exists on this surface. "
            "Function-level Description and Tags are FUNCTION-kind surfaces, explicitly "
            "distinct: prose about the function is not prose about a variable. A schema "
            "element here structurally CANNOT be named-in-prose-but-unwalked."),
        "items": (
            [{"address": "env:%s" % k, "cell": "orphan", "method": "mention",
              "evidence": "source reads this key; ABSENT from live Variables -- the read "
                          "silently takes its default at runtime"} for k in orphan]
            + [{"address": "env:%s" % k, "cell": "member", "method": "traversal",
                "evidence": "live-set (deploy plane declares it); never read by this source "
                            "-- set-but-unread"} for k in member]
        ),
    }

    violations = boundary_report.validate(report)
    hard = [v for v in violations if v.code != "BR008"]
    for v in violations:
        print("CONFORMANCE%s: %s at %s: %s"
              % ("" if v.code != "BR008" else " (expected, new shape)", v.code, v.where, v.message))
    if hard:
        print("FAIL: emitted report NON-CONFORMANT (%d hard violation(s))." % len(hard))
        return 1

    print("SENSOR lambda-env residue -- function=%s revision=%s" % (args.function, revision))
    print("  ACCOUNTING: N=%d = covered %d + member %d + orphan %d   (doc_only: N/A-DECLARED, "
          "by shape, field-demonstrated)" % (surface_total, len(covered), len(member), len(orphan)))
    print("  DENOMINATOR (assumed side): %d literal env key(s) from %s; UNKNOWN (first-class, "
          "EXCLUDED from N): %d non-literal read(s)%s"
          % (len(keys), src.name, len(unknown),
             " -- " + "; ".join("%s (%s)" % u for u in unknown[:5]) if unknown else ""))
    print("  DENOMINATOR (live side): %d Variables key(s) on %s (values withheld)"
          % (len(live), args.function))
    print("  DIRECTION: assumed side is ast-literal extraction (mention, UNDER-reports -- a "
          "dynamically composed key is invisible); live side is the API's own map (exact).")
    for it in report["items"]:
        print("  RESIDUE [%s] %s -- %s" % (it["cell"], it["address"], it["evidence"]))

    if args.out:
        out_path = Path(args.out).resolve()
        payload = json.dumps(report, indent=2) + "\n"
        try:
            out_path.write_text(payload, encoding="utf-8")
        except OSError as e:
            print("FAIL: could not write report to %s (%s: %s)" % (out_path, type(e).__name__, e))
            return 1
        if not out_path.is_file() or out_path.stat().st_size < len(payload):
            print("FAIL: report write did not land at %s." % out_path)
            return 1
        print("  REPORT WRITTEN (verified on disk): %s" % out_path)

    if orphan or member:
        print("VERDICT: %d residue key(s) (orphan %d + set-but-unread member %d) of %d -- "
              "boundary statement, not materiality." % (len(orphan) + len(member), len(orphan),
                                                        len(member), surface_total))
        return 2
    print("CLEAN: every source-read key is live-set and every live key is source-read.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
