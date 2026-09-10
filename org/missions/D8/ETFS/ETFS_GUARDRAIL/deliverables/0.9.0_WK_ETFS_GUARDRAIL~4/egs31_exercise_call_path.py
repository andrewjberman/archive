#!/usr/bin/env python3
"""EG-s-31 -- EXERCISE the served renderer's `--no-ladder` call path against a
NAMED `coverage` package and report what it did.

WHY THIS EXISTS. `render_month_end.py:1162` calls `remediate._provider_for(p)` on the
`--no-ladder` branch. Whether the box can run that line is not answerable from an
upload receipt, an ETag or a directory listing -- only from RESOLVING THE SYMBOL
THROUGH THE IMPORT THE RENDERER ITSELF PERFORMS. This script is that resolution, and
it is the DIFFERENCE CONTROL for `S31-AC1` arm (d): same code, same spec, two package
states, both printed.

TWO MODES, one code path for the exercise itself:

  --in-place <dir>      exercise the box exactly as it is. <dir> holds
                        render_month_end.py with a `coverage/` SIBLING -- the reporter
                        box layout (/opt/etfs-reports). NOTHING IS COPIED and nothing
                        is staged: what runs is what the box holds. This is the mode
                        the on-box arms (c) and (d) use.

  --coverage-dir <dir> --renderer <file> [--extra <file>...]
                        BUILD that layout in a throwaway directory from named inputs
                        and exercise it. This is how a PINNED, RE-RUNNABLE
                        reproduction of a package state is obtained after the world
                        has moved on -- arm (a)'s "before" side reads the pre-act
                        DEPLOYED bytes out of this order's fixtures, so the defect
                        stays reproducible for a grader long after the prefix is
                        fixed. `.pyfixture` inputs are materialised as `.py`.

ZERO AWS CALLS AND ZERO WRITES, ASSERTED NOT ASSUMED. `coverage_gate`'s `--no-ladder`
branch reaches `_skipped_branch_egress_ask`, which really does `put_object` the
rung-3-EQUIVALENT ask. That would be a live S3 write, so the renderer module's `s3`
client is REPLACED with a recording stub before the call and every intercepted PUT is
printed with its key. The count printed on the `EGS31-S3-PUTS` line is the number of
writes that WOULD have happened and DID NOT. `probe` is a stub, so no Lambda is
invoked, and `ladder=False` means `remediate_month` is never called -- this is not,
and cannot become, EG-s-21's driven run.

THE SPEC IS FIXED AND NARROW: partner `cottonwood`, month `2026-08`, exactly one
class-C day, `2026-08-14`. Every other trading day of the month is present in the
series, so `classify_month` returns COVERED for it and the probe is never consulted;
`2026-08-14` is absent and the probe answers "upstream partition present, priced > 0",
which is the definition of class C -- the one class that gates publication. Expected
of a package that satisfies the renderer: `VERDICT: REFUSE holes=1`.
"""
from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
import os
import shutil
import sys
import tempfile
import traceback

MONTH = "2026-08"
PARTNER = "cottonwood"
HOLE = "2026-08-14"


class RecordingS3:
    """A boto3-s3-shaped stub that FORWARDS NOTHING.

    `get_object` RAISES because that is how `remediate._read_prior_asks` reads the
    ordinary "no ask artifact written yet this month" case (`readable=True`, no prior
    asks) -- the common first-partner case. Deliberately NOT an absent capability: a
    stub without `get_object` would make the ask declare itself partner-only, which
    would exercise a different branch than a real box run does.
    """

    def __init__(self) -> None:
        self.puts: list = []

    def get_object(self, Bucket, Key, **kw):  # noqa: N803 - boto3 kwarg casing
        raise RuntimeError("EGS31 stub: no prior object at s3://%s/%s" % (Bucket, Key))

    def put_object(self, Bucket, Key, Body, **kw):  # noqa: N803 - boto3 kwarg casing
        self.puts.append({"bucket": Bucket, "key": Key, "bytes": len(Body)})
        return {}


def sha256_of(path: str) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        for chunk in iter(lambda: fh.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


def stage_box_layout(coverage_dir: str, renderer: str, extras: list, workdir: str) -> str:
    """Materialise the reporter-box layout: <box>/render_month_end.py with a
    <box>/coverage/ sibling. Returns <box>."""
    box = os.path.join(workdir, "etfs-reports")
    cov = os.path.join(box, "coverage")
    os.makedirs(cov)
    shutil.copyfile(renderer, os.path.join(box, "render_month_end.py"))
    sources = [os.path.join(coverage_dir, n) for n in sorted(os.listdir(coverage_dir))]
    sources += list(extras)
    for src in sources:
        if not os.path.isfile(src):
            continue
        stem, ext = os.path.splitext(os.path.basename(src))
        if ext not in (".py", ".pyfixture"):
            continue
        shutil.copyfile(src, os.path.join(cov, stem + ".py"))
    return box


def load_renderer(box: str):
    path = os.path.join(box, "render_month_end.py")
    spec = importlib.util.spec_from_file_location("egs31_render_month_end", path)
    mod = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = mod
    spec.loader.exec_module(mod)
    return mod


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--in-place", dest="in_place", default=None,
                    help="exercise this box directory as-is; copy nothing")
    ap.add_argument("--coverage-dir", default=None)
    ap.add_argument("--renderer", default=None)
    ap.add_argument("--extra", action="append", default=[],
                    help="an additional module to place inside coverage/ (vendored member)")
    ap.add_argument("--label", default="unlabelled")
    args = ap.parse_args()

    tmp = None
    if args.in_place:
        box = os.path.abspath(args.in_place)
    else:
        if not (args.coverage_dir and args.renderer):
            print("EGS31-HARNESS-ERROR: need --in-place, or --coverage-dir with --renderer")
            return 2
        tmp = tempfile.mkdtemp(prefix="egs31-")
        box = stage_box_layout(args.coverage_dir, args.renderer, args.extra, tmp)

    print("EGS31-EXERCISE label=%s" % args.label)
    print("EGS31-BOX-DIR %s" % box)
    print("EGS31-MODE %s" % ("in-place" if args.in_place else "staged"))

    try:
        mod = load_renderer(box)
    except Exception:
        print("EGS31-RESULT IMPORT-FAILED")
        traceback.print_exc(file=sys.stdout)
        return 0

    # GRAIN: name the files that were actually imported, and hash them. A claim about
    # "the package" that cannot say which bytes it ran is not a measurement.
    print("EGS31-RENDERER-FILE %s sha256=%s"
          % (mod.__file__, sha256_of(mod.__file__)))
    for name in ("classifier", "remediate"):
        m = getattr(mod, name, None)
        if m is None:
            print("EGS31-MODULE %s ABSENT-FROM-RENDERER-NAMESPACE" % name)
            continue
        print("EGS31-MODULE %s file=%s sha256=%s"
              % (name, m.__file__, sha256_of(m.__file__)))

    has_attr = hasattr(mod.remediate, "_provider_for")
    print("EGS31-SYMBOL remediate._provider_for present=%s" % has_attr)

    stub = RecordingS3()
    mod.s3 = stub

    tcal = mod.classifier.tcal
    trading = [d for d in mod.classifier._month_dates(MONTH) if tcal.is_trading_day(d)]
    series = {d.isoformat(): {"egs31_stub_row": True}
              for d in trading if d.isoformat() != HOLE}
    print("EGS31-SPEC partner=%s month=%s hole=%s trading_days=%d series_days=%d"
          % (PARTNER, MONTH, HOLE, len(trading), len(series)))

    probed: list = []

    def probe(partner: str, date_str: str):
        probed.append(date_str)
        # upstream partition present and priced > 0, no slice -> class C, the only
        # class that gates publication.
        return {"partition": True, "priced": 5}

    try:
        result = mod.coverage_gate(
            MONTH, [PARTNER], {PARTNER: series}, [],
            ladder=False, probe=probe,
            run_id="egs31-exercise", run_id_source="EG-s-31 battery (not a driven run)")
    except Exception as exc:
        print("EGS31-RESULT RAISED %s: %s" % (type(exc).__name__, exc))
        traceback.print_exc(file=sys.stdout)
        print("EGS31-S3-PUTS n=%d (intercepted, none forwarded)" % len(stub.puts))
        if tmp:
            shutil.rmtree(tmp, ignore_errors=True)
        return 0

    print("EGS31-RESULT OK")
    print("VERDICT: %s holes=%d C=%d"
          % (result["verdict"], result["holes"],
             result["per_partner"][PARTNER]["summary"]["C"]))
    print("EGS31-PROBED %s" % json.dumps(sorted(probed)))
    for rec in result.get("unresolved", {}).get(PARTNER, []):
        print("EGS31-UNRESOLVED date=%s class=%s provider=%s"
              % (rec.get("date"), rec.get("class"), rec.get("provider")))
    print("EGS31-S3-PUTS n=%d (intercepted, none forwarded)" % len(stub.puts))
    for p in stub.puts:
        print("EGS31-S3-PUT-INTERCEPTED s3://%s/%s bytes=%d"
              % (p["bucket"], p["key"], p["bytes"]))
    if tmp:
        shutil.rmtree(tmp, ignore_errors=True)
    return 0


if __name__ == "__main__":
    sys.exit(main())
