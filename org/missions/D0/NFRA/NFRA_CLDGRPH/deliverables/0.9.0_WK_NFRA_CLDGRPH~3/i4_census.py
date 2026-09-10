#!/usr/bin/env python3
"""NFRA_CLDGRPH TO-CG-I-4 / I4-AC1 -- CG-s-44. COUNT THE CITATIONS AT RISK.

THE QUESTION. A dated archive key reads immutable and is a mutable pointer. Nobody has
counted how many citations in this project's record point at bytes that are no longer
there. This counts them, against the LIVE object, and refuses to fold the ones that
cannot be decided into either of the ones that can.

THE THREE CLASSES ARE MECE OVER A DECLARED DOMAIN, and the domain is the printed
denominator MINUS the printed exclusions -- not a forward list of what I thought of:

    STILL_VALID   the citation carries a discriminator and it MATCHES the live object
    OVERWRITTEN   the citation carries a discriminator and it DIFFERS from the live object
    UNDECIDABLE   everything else in the denominator

and the script asserts STILL_VALID + OVERWRITTEN + UNDECIDABLE == CITATIONS_FOUND before
it prints, so a member cannot be lost without the count disagreeing.

UNDECIDABLE IS NOT A RESIDUE. On an UNVERSIONED bucket it is the load-bearing class: a
citation with no discriminator names bytes that no instrument, now or later, can recover
or refute. Its sub-reasons are printed so the reader can see WHY each one is undecidable.

THE CLASSIFIER IS DELIBERATELY CONSERVATIVE and the bias has a direction. A discriminator
is attached to a citation only when this citation is the NEAREST one in the file to that
discriminator and it lies within ATTACH_CHARS. So STILL_VALID and OVERWRITTEN are LOWER
bounds and UNDECIDABLE is an UPPER bound. A second, LOOSE arm (bare timestamps with no cue
word) is run and reported separately as a sensitivity check -- it is NOT folded into the
primary counts, because an instrument that decides by proximity alone would be deciding
what it cannot see.

TWO POPULATIONS, BOTH PRINTED, because choosing a domain is itself a claim. The ORDERED
population is this project's record, which is what the cell asks for. The UNSCOPED arm
walks the WHOLE worktree with the same regex and prints its own denominator: if the term
lives outside the ordered domain, the ordered domain does not hold the whole population
and the subtraction over it is void as an estate claim. It does live outside. Said here
rather than discovered later.

TREE. The corpus is walked by this file's OWN os.walk from the caller's cwd, and a control
file that exists only on this branch must appear in the hits. That control does not depend
on the comp-rail's caller-tree fix being present -- it is a property of the checkout this
process is standing in, which is the only place the question can be answered from.

usage: python i4_census.py
"""

import datetime
import json
import os
import re
import subprocess
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import i4_lib  # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))
PROJECT_RECORD = "org/missions/D0/NFRA/NFRA_CLDGRPH"
CONTROL_NAME = "i4_tree_control.txt"
CAPTURE = os.path.join(HERE, "i4_census.capture.json")

ATTACH_CHARS = 300      # strict arm: a cued discriminator must be this close
LOOSE_CHARS = 150       # sensitivity arm: a bare timestamp must be this close
MAX_BYTES = 8_000_000
SKIP_DIRS = {".git", "node_modules", "__pycache__", ".venv", ".terraform"}

# A dated archive citation. Written as character classes so this file does not match
# itself: the population must be the whole tree, and a scanner that excludes one file is
# a scanner whose population is no longer the one it claims.
KEY_RE = re.compile(r"(?:snapshots/([0-9]{8})/)?graph-([0-9]{8}[A-Za-z0-9T_-]*)[.]tar[.]gz")

ISO_RE = r"[0-9]{4}-[0-9]{2}-[0-9]{2}[T ][0-9]{2}:[0-9]{2}:[0-9]{2}(?:[.][0-9]+)?(?:Z|\+00:00|\+0000)?"
GMT_RE = r"[A-Z][a-z]{2}, [0-9]{2} [A-Z][a-z]{2} [0-9]{4} [0-9]{2}:[0-9]{2}:[0-9]{2} GMT"

ETAG_CUE = re.compile(r"(?i)([A-Za-z0-9_]{0,24}?)etag[^0-9a-f]{0,12}([0-9a-f]{32})")
LM_CUE = re.compile(r"(?i)([A-Za-z0-9_]{0,24}?)(?:lastmodified|last_modified|last-modified|modified)\D{0,24}("
                    + ISO_RE + r"|" + GMT_RE + r")")
GMT_SELF = re.compile(GMT_RE)
SIZE_CUE = re.compile(r"(?i)([A-Za-z0-9_]{0,24}?)(?:contentlength|content_length|\"size\"|size=|size )\D{0,6}([0-9]{3,12})")
BARE_TS = re.compile(ISO_RE + r"|" + GMT_RE)
AT_ETAG = re.compile(r"@([0-9a-f]{32})")

# A CUE CAN BELONG TO A DIFFERENT OBJECT, AND PROXIMITY CANNOT SEE THAT.
# Measured while building this: f3_marker_capture.json carries "marker_etag" two lines
# above "aws_snapshot": "<a dated archive key>", and nearest-neighbour attachment lent the
# MARKER's ETag to the SNAPSHOT -- a false OVERWRITTEN, and exactly the kind of green a
# proximity classifier produces. So a cue carried by a QUALIFIED identifier (word_etag,
# word_last_modified) is attached only when the qualifier names this object family;
# anything else is REJECTED and counted, never silently attached.
CUE_QUALIFIERS_OK = {"", "snapshot", "snapshots", "archive", "tarball", "object", "graph",
                     "s3", "content", "tar", "gz", "http", "x_amz", "amz"}


def parse_ts(text):
    t = text.strip()
    for fmt in ("%a, %d %b %Y %H:%M:%S GMT",):
        try:
            return datetime.datetime.strptime(t, fmt).replace(tzinfo=datetime.timezone.utc)
        except ValueError:
            pass
    t2 = t.replace("Z", "+00:00").replace(" ", "T", 1)
    if t2.endswith("+0000"):
        t2 = t2[:-5] + "+00:00"
    try:
        d = datetime.datetime.fromisoformat(t2)
    except ValueError:
        return None
    if d.tzinfo is None:
        d = d.replace(tzinfo=datetime.timezone.utc)
    return d.astimezone(datetime.timezone.utc).replace(microsecond=0)


def walk(root, rel):
    base = os.path.join(root, rel) if rel else root
    for dp, dn, fn in os.walk(base):
        dn[:] = [d for d in dn if d not in SKIP_DIRS]
        for f in fn:
            yield os.path.join(dp, f)


def read_text(path):
    try:
        if os.path.getsize(path) > MAX_BYTES:
            return None, "OVERSIZE"
        b = open(path, "rb").read()
    except OSError:
        return None, "UNREADABLE"
    if b"\x00" in b[:4096]:
        return None, "BINARY"
    return b.decode("utf-8", "replace"), None


def scan_file(text):
    """Return citation occurrences with their attached discriminators.

    Attachment is by NEAREST citation, computed over the whole file, so a window holding
    two keys cannot silently lend one key's ETag to the other."""
    keys = [(m.start(), m.end(), m.group(1), m.group(2)) for m in KEY_RE.finditer(text)]
    if not keys:
        return [], 0
    cites = []
    for s, e, datepart, stem in keys:
        key = "snapshots/%s/graph-%s.tar.gz" % (datepart, stem) if datepart else None
        inferred = False
        if key is None:
            key = "snapshots/%s/graph-%s.tar.gz" % (stem[:8], stem)
            inferred = True
        cites.append({"span": (s, e), "key": key, "key_inferred": inferred,
                      "etag": None, "etag_form": None, "lm": None, "size": None,
                      "loose_ts": None, "line": text.count("\n", 0, s) + 1})

    def nearest(pos):
        best, bi = None, None
        for i, c in enumerate(cites):
            s, e = c["span"]
            d = 0 if s <= pos <= e else min(abs(pos - e), abs(s - pos))
            if best is None or d < best:
                best, bi = d, i
        return bi, best

    rejected = [0]

    def attach(rx, field, limit, group=1, qual_group=None):
        for m in rx.finditer(text):
            if qual_group is not None:
                q = m.group(qual_group).strip("_").lower()
                if q not in CUE_QUALIFIERS_OK:
                    rejected[0] += 1
                    continue
            i, d = nearest(m.start())
            if i is None or d > limit:
                continue
            if cites[i][field] is None:
                cites[i][field] = m.group(group)

    # THE PROPOSED GRAMMAR IS SYNTACTIC, SO READ IT SYNTACTICALLY. A citation written as
    # bucket/key@<32 hex> carries no cue WORD -- and a classifier that only understands
    # "ETag: <hex>" would score the very grammar this cell argues for as UNDECIDABLE. The
    # suffix binds to the key it is attached to with no proximity guess at all, which is
    # precisely why the grammar is worth having.
    for c in cites:
        m = AT_ETAG.match(text, c["span"][1])
        if m:
            c["etag"] = m.group(1)
            c["etag_form"] = "AT_SUFFIX"

    attach(ETAG_CUE, "etag", ATTACH_CHARS, group=2, qual_group=1)
    attach(LM_CUE, "lm", ATTACH_CHARS, group=2, qual_group=1)
    attach(GMT_SELF, "lm", ATTACH_CHARS, group=0)
    attach(SIZE_CUE, "size", ATTACH_CHARS, group=2, qual_group=1)
    attach(BARE_TS, "loose_ts", LOOSE_CHARS, group=0)
    return cites, rejected[0]


def classify(cite, live):
    """MECE over the declared domain. Returns (class, reason)."""
    obj = live.get(cite["key"])
    if obj is None:
        return "UNDECIDABLE", "KEY_ABSENT_FROM_LIVE_BUCKET"
    if cite["etag"]:
        # The reason carries HOW the ETag was attached: _AT_SUFFIX means the citation was
        # written as key@<hex> and bound with no proximity guess at all. That is the
        # difference between a grammar and a heuristic, and it should be visible in the
        # count rather than inferable from the source.
        form = "_AT_SUFFIX" if cite.get("etag_form") == "AT_SUFFIX" else ""
        return ("STILL_VALID", "ETAG_MATCH" + form) if cite["etag"].lower() == obj["etag"] \
            else ("OVERWRITTEN", "ETAG_DIFFERS" + form)
    if cite["lm"]:
        a, b = parse_ts(cite["lm"]), parse_ts(obj["last_modified"])
        if a is None or b is None:
            return "UNDECIDABLE", "TIMESTAMP_UNPARSEABLE"
        return ("STILL_VALID", "LASTMODIFIED_MATCH") if a == b else ("OVERWRITTEN", "LASTMODIFIED_DIFFERS")
    if cite["size"]:
        if int(cite["size"]) != obj["size"]:
            return "OVERWRITTEN", "SIZE_DIFFERS"
        # A size match is NOT identity: two derives of the same graph can share a length.
        return "UNDECIDABLE", "SIZE_ONLY_NOT_DECISIVE"
    return "UNDECIDABLE", "NO_DISCRIMINATOR_IN_THE_CITATION"


def main():
    root = i4_lib.repo_root()
    tf = i4_lib.tree_facts(root)
    now = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

    live, listmeta = i4_lib.live_objects(root)

    print("=" * 78)
    print("I4-AC1 -- THE CITATIONS AT RISK, COUNTED AGAINST THE LIVE OBJECT")
    print("=" * 78)
    print("RUN_UTC                 : %s" % now)
    print("TREE_READ=%s" % tf["kind"])
    print("  worktree root         : %s" % tf["root"])
    print("  branch / HEAD         : %s / %s" % (tf["branch"], tf["head"]))
    print("  git-dir               : %s" % tf["git_dir"])
    print("  git-common-dir        : %s" % tf["git_common_dir"])
    print("  (the two differ on a linked worktree; that is the measurement, not an assumption)")
    print("")
    print("CUT DISCIPLINE -- the four things every number here has to carry")
    print("  INSTRUMENT COVERAGE   : this file's own os.walk over the tree above; every")
    print("                          file except %s dirs, files over %d bytes, and files" % (sorted(SKIP_DIRS), MAX_BYTES))
    print("                          with a NUL in the first 4096 bytes. Exclusions counted below.")
    print("  HARNESS GRAIN         : ONE CITATION OCCURRENCE = one regex match of a dated")
    print("                          archive key. Not one file, not one distinct key.")
    print("  BASELINE ENVIRONMENT  : NO stored baseline. The live table is s3api")
    print("                          list-objects-v2 on bucket %s" % i4_lib.BUCKET)
    print("                          prefix %s, read in THIS run at %s" % (i4_lib.PREFIX, now))
    print("                          through .tools/aws (CLI v1) from this worktree.")
    print("  TREE                  : %s (%s)" % (tf["kind"], tf["root"]))
    print("")
    print("LIVE TABLE COVERAGE     : %d object(s) returned; KeyCount=%s IsTruncated=%s NextToken=%s"
          % (listmeta["returned"], listmeta["key_count"], listmeta["is_truncated"], listmeta["next_token_present"]))
    print("  the table spans the WHOLE prefix, not the cited subset, so 'cited key is not")
    print("  in the bucket' is an outcome this instrument can return rather than a blind spot.")
    print("")

    # ---------------- ORDERED POPULATION -------------------------------------
    files_scanned = 0
    excl = {"BINARY": 0, "OVERSIZE": 0, "UNREADABLE": 0}
    control_hits = 0
    control_path = None
    foreign_rejected = 0
    instr_files = 0
    instr_cites = 0
    rows = []
    hit_files = set()

    for path in walk(root, PROJECT_RECORD):
        rel = os.path.relpath(path, root).replace(os.sep, "/")
        text, why = read_text(path)
        if text is None:
            excl[why] += 1
            continue
        files_scanned += 1
        cites, rej = scan_file(text)
        foreign_rejected += rej
        if not cites:
            continue
        base = os.path.basename(rel)
        if base == CONTROL_NAME:
            control_hits += len(cites)
            control_path = rel
            continue                      # EXCLUDED from classification; printed below
        if base.startswith("i4_"):
            # THE INSTRUMENT'S OWN OUTPUT IS NOT A CITATION IN THE RECORD, IT IS A REPORT
            # OF ONE. i4_census.capture.json restates every citation this sweep found, so
            # counting it would count each citation twice and every re-run would DOUBLE
            # the population -- measured here at 111 -> 222 before this branch existed.
            instr_files += 1
            instr_cites += len(cites)
            continue
        hit_files.add(rel)
        for c in cites:
            klass, reason = classify(c, live)
            rows.append({"file": rel, "line": c["line"], "key": c["key"],
                         "key_inferred": c["key_inferred"], "etag_cited": c["etag"],
                         "etag_form": c["etag_form"],
                         "lastmodified_cited": c["lm"], "size_cited": c["size"],
                         "loose_ts": c["loose_ts"], "class": klass, "reason": reason})

    # tree positive control: present in the hits AND absent from the shared branch
    ctl_on_cloud = subprocess.run(
        ["git", "-C", root, "cat-file", "-e", "CLOUD:%s/%s" % (
            PROJECT_RECORD + "/deliverables/0.9.0_WK_NFRA_CLDGRPH~3", CONTROL_NAME)],
        capture_output=True, text=True)
    if tf["kind"] == "MAIN":
        ctl = "N/A-MAIN-TREE"
    elif control_hits > 0 and ctl_on_cloud.returncode != 0:
        ctl = "FIRED"
    else:
        ctl = "DID-NOT-FIRE"
    print("TREE_POSITIVE_CONTROL=%s" % ctl)
    print("  control file          : %s" % (control_path or "NOT FOUND IN THE SWEEP"))
    print("  citations inside it   : %d (EXCLUDED from every count below)" % control_hits)
    print("  same path on CLOUD    : %s (rc=%d) -- so it exists only on this branch"
          % ("ABSENT" if ctl_on_cloud.returncode != 0 else "PRESENT", ctl_on_cloud.returncode))
    if ctl == "DID-NOT-FIRE":
        print("BLOCKED: the sweep did not read this branch's own work; every number below is void.")
        return 2
    print("")

    n = len(rows)
    sv = [r for r in rows if r["class"] == "STILL_VALID"]
    ov = [r for r in rows if r["class"] == "OVERWRITTEN"]
    un = [r for r in rows if r["class"] == "UNDECIDABLE"]
    assert len(sv) + len(ov) + len(un) == n, "ERROR: the three classes do not partition the domain"

    print("POPULATION (ORDERED)    : %s -- this project's record, the domain the cell names" % PROJECT_RECORD)
    print("DENOMINATOR             : %d file(s) read" % files_scanned)
    print("  EXCLUDED from the denominator, by reason (a denominator that does not say what")
    print("  it excluded is refused at the flip):")
    print("    BINARY (NUL in first 4096 bytes) : %d" % excl["BINARY"])
    print("    OVERSIZE (> %d bytes)       : %d" % (MAX_BYTES, excl["OVERSIZE"]))
    print("    UNREADABLE (OS error)            : %d" % excl["UNREADABLE"])
    print("    TREE CONTROL FILE                : 1 file, %d citation(s)" % control_hits)
    print("    THIS INSTRUMENT'S OWN OUTPUT     : %d file(s), %d citation(s) -- i4_* under this" % (instr_files, instr_cites))
    print("                                       order's deliverables. The capture RESTATES every")
    print("                                       citation found, so counting it would count each")
    print("                                       one twice and DOUBLE the population per re-run.")
    print("")
    print("CITATIONS_FOUND=%d of %d file(s)" % (n, files_scanned))
    print("  reading: %d citation OCCURRENCES, found across %d of the %d files read."
          % (n, len(hit_files), files_scanned))
    print("  distinct keys cited   : %d" % len(set(r["key"] for r in rows)))
    print("")
    print("CLASSIFICATION (MECE over the denominator above; the assert has already run)")
    print("STILL_VALID=%d" % len(sv))
    print("OVERWRITTEN=%d" % len(ov))
    print("UNDECIDABLE=%d" % len(un))
    print("  SUM CHECK             : %d + %d + %d = %d == CITATIONS_FOUND"
          % (len(sv), len(ov), len(un), n))
    print("")

    def by_reason(rs):
        d = {}
        for r in rs:
            d[r["reason"]] = d.get(r["reason"], 0) + 1
        return sorted(d.items(), key=lambda x: -x[1])

    for label, rs in (("STILL_VALID", sv), ("OVERWRITTEN", ov), ("UNDECIDABLE", un)):
        print("  %s by reason:" % label)
        for reason, c in by_reason(rs):
            print("    %-34s %d" % (reason, c))
    print("")

    print("FOREIGN CUES REJECTED   : %d" % foreign_rejected)
    print("  a discriminator carried by a QUALIFIED identifier naming a different object")
    print("  (marker_etag, marker_last_modified) is refused rather than attached. Without")
    print("  this guard the classifier lent a MARKER's ETag to a SNAPSHOT and printed a")
    print("  confident OVERWRITTEN. Proximity is not attachment.")
    print("")

    # CROSS-INSTRUMENT ARM. Every verdict above rests on ONE table (list-objects-v2).
    # A check scoped to the members cannot see a defect in what the members SHARE, so the
    # shared dependency is re-read with a DIFFERENT API, on EVERY key that bears a verdict
    # -- not a sample, so the coverage denominator here is the whole cited key set.
    cited_keys = sorted(set(r["key"] for r in rows))
    agree, disagree, absent = 0, 0, 0
    print("CROSS-INSTRUMENT CONTROL -- s3api head-object vs the list table, on %d of %d"
          % (len(cited_keys), len(cited_keys)))
    print("  distinct cited key(s) (full coverage of the keys that bear a verdict):")
    for k in cited_keys:
        h = i4_lib.head(root, k, "cross-instrument control for the classifier's live table")
        lv = live.get(k)
        if h is None or lv is None:
            absent += 1
            print("    %-46s head=ABSENT list=%s" % (k, "PRESENT" if lv else "ABSENT"))
            continue
        same = (h["etag"] == lv["etag"] and h["size"] == lv["size"]
                and parse_ts(h["last_modified"]) == parse_ts(lv["last_modified"]))
        agree += 1 if same else 0
        disagree += 0 if same else 1
        print("    %-46s %s  ETag %s / %s / %d B"
              % (k, "AGREE" if same else "DISAGREE", h["etag"], h["last_modified"], h["size"]))
    print("  CROSS_INSTRUMENT_AGREE=%d DISAGREE=%d NOT_COMPARABLE=%d" % (agree, disagree, absent))
    print("")

    print("EVERY OVERWRITTEN CITATION, NAMED (this is the evidential problem, in full):")
    if not ov:
        print("    none")
    for r in sorted(ov, key=lambda r: (r["file"], r["line"])):
        cited = r["etag_cited"] or r["lastmodified_cited"] or r["size_cited"]
        obj = live[r["key"]]
        print("    %s:%d" % (r["file"], r["line"]))
        print("        key    %s" % r["key"])
        print("        cited  %s (%s)" % (cited, r["reason"]))
        print("        live   ETag %s / LastModified %s / %d bytes"
              % (obj["etag"], obj["last_modified"], obj["size"]))
    print("")

    print("UNDECIDABLE, BY FILE (top 12) -- these are citations no instrument can settle,")
    print("now or later, because the bucket keeps ONE version and the key is a pointer:")
    perfile = {}
    for r in un:
        perfile[r["file"]] = perfile.get(r["file"], 0) + 1
    for f, c in sorted(perfile.items(), key=lambda x: -x[1])[:12]:
        print("    %3d  %s" % (c, f))
    print("    ... %d file(s) with undecidable citations in total" % len(perfile))
    print("")

    # ---------------- SENSITIVITY (LOOSE) ARM --------------------------------
    flips = {"STILL_VALID": 0, "OVERWRITTEN": 0, "UNPARSEABLE": 0}
    for r in un:
        if r["reason"] != "NO_DISCRIMINATOR_IN_THE_CITATION" or not r["loose_ts"]:
            continue
        a, b = parse_ts(r["loose_ts"]), parse_ts(live[r["key"]]["last_modified"])
        if a is None or b is None:
            flips["UNPARSEABLE"] += 1
        elif a == b:
            flips["STILL_VALID"] += 1
        else:
            flips["OVERWRITTEN"] += 1
    print("SENSITIVITY (LOOSE ARM, NOT FOLDED IN): if a BARE timestamp within %d chars were" % LOOSE_CHARS)
    print("  accepted as a vintage claim, of the %d NO_DISCRIMINATOR citations, %d would read"
          % (len([r for r in un if r['reason'] == 'NO_DISCRIMINATOR_IN_THE_CITATION']),
             flips["STILL_VALID"] + flips["OVERWRITTEN"] + flips["UNPARSEABLE"]))
    print("  as decided: STILL_VALID %d / OVERWRITTEN %d / UNPARSEABLE %d. They are NOT counted"
          % (flips["STILL_VALID"], flips["OVERWRITTEN"], flips["UNPARSEABLE"]))
    print("  above: proximity is not attachment, and the direction of this bias is stated")
    print("  rather than hidden -- UNDECIDABLE is an UPPER bound, the other two are LOWER bounds.")
    print("")

    # ---------------- UNSCOPED ARM -------------------------------------------
    out_files, out_cites = set(), 0
    all_files = 0
    scratch_excl = 0
    for path in walk(root, ""):
        rel = os.path.relpath(path, root).replace(os.sep, "/")
        if rel.startswith(PROJECT_RECORD):
            continue
        if rel.startswith(".scratch/"):
            # THIS ORDER'S OWN SCRATCH IS NOT THE ESTATE'S RECORD. It holds this cell's
            # trial runs, which restate every key the census printed; counting them would
            # measure my own output and call it the estate's exposure. Excluded by name,
            # counted below, and it is the same defect as the capture-file doubling.
            scratch_excl += 1
            continue
        text, why = read_text(path)
        if text is None:
            continue
        all_files += 1
        c, _rej = scan_file(text)
        if c:
            out_files.add(rel)
            out_cites += len(c)
    print("UNSCOPED ARM -- the domain choice, falsified before it is trusted (rule 24(i)):")
    print("  the SAME regex over the WHOLE worktree MINUS the ordered population:")
    print("  OUTSIDE_PROJECT_CITATIONS=%d across %d file(s), from %d file(s) read"
          % (out_cites, len(out_files), all_files))
    print("  EXCLUDED from this arm: %d file(s) under .scratch/ -- this cell's own trial runs" % scratch_excl)
    print("  READING: the ordered domain is NOT the whole population. Dated-archive citations")
    print("  live outside this project's record, so the count above is this PROJECT's exposure")
    print("  and NOT the estate's. Any estate-level claim needs this wider arm re-run per owner.")
    for f in sorted(out_files)[:14]:
        print("      %s" % f)
    if len(out_files) > 14:
        print("      ... and %d more" % (len(out_files) - 14))
    print("")

    cap = {
        "claim_provenance": "measured",
        "run_utc": now,
        "tree": tf,
        "live_table": listmeta,
        "population_ordered": PROJECT_RECORD,
        "files_scanned": files_scanned,
        "excluded": dict(excl, TREE_CONTROL_FILE=1, TREE_CONTROL_CITATIONS=control_hits,
                         INSTRUMENT_OUTPUT_FILES=instr_files, INSTRUMENT_OUTPUT_CITATIONS=instr_cites),
        "foreign_cues_rejected": foreign_rejected,
        "cross_instrument": {"agree": agree, "disagree": disagree, "not_comparable": absent,
                             "keys": cited_keys},
        "citations_found": n,
        "files_with_citations": len(hit_files),
        "still_valid": len(sv),
        "overwritten": len(ov),
        "undecidable": len(un),
        "loose_arm_would_flip": flips,
        "unscoped_arm": {"citations": out_cites, "files": len(out_files), "files_read": all_files},
        "rows": rows,
    }
    with open(CAPTURE, "w", encoding="ascii", newline="\n") as fh:
        json.dump(cap, fh, indent=1, sort_keys=True)
    print("CAPTURE                 : %s" % os.path.relpath(CAPTURE, root).replace(os.sep, "/"))
    print("OK: I4-AC1 complete -- %d citations classified, %d of them undecidable." % (n, len(un)))
    return 0


if __name__ == "__main__":
    sys.exit(main())
