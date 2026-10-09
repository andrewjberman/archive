#!/usr/bin/env python3
"""check_firm_schedules_r14 -- LGIC_BLANKFIX round 14, cell BF-ac-2 (ruling R2, row D1-W1-S7).

Every schedule or event-rule line the root check lists as FIX whose new name carries the firm token 49f or cot is
  (1) read back through lib/opal_naming.py name(system, firm-long-scope, function, kind): the listed string must EQUAL the
      builder's output (a string that is not is "hand composed"),
  (2) fed through the real .tools/naming-gate.py --diff --enforce on a temporary copy of its .tf in which the resource's
      name attribute is the opal_name module's output (the form the gate's context rule permits); the repository file is
      never written, the diff goes to a scratch directory,
  (3) fed through the same gate with the listed string typed into the .tf as a literal (the DIFFERENCE CONTROL): the gate
      must refuse it as a hand-kept carrier of the firm token.
A line whose name() call is refused counts as an owed row when REGISTRY_ROWS_round14.json (next to this file) drafts it.

    python org/missions/D14/LGIC/LGIC_BLANKFIX/deliverables/0.9.0_WK_LGIC_BLANKFIX~2/check_firm_schedules_r14.py

Prints one line per name and, last,
    FIRM-SCHEDULES ok=<bool> lines=N builder_names=N gate_pass=N owed_rows=N hand_composed=N
Python 3.9; ASCII only; no AWS, no network, no terraform; the repository is not written.
"""
import concurrent.futures
import difflib
import json
import os
import re
import subprocess
import sys
import tempfile
import time

HERE = os.path.dirname(os.path.abspath(__file__))
FIRM_TOKENS = ("49f", "cot")
MAP = "infra/logic/registry/root_map.json"
ROWS_FILE = os.path.join(HERE, "REGISTRY_ROWS_round14.json")


def repo_root():
    d = HERE
    for _ in range(12):
        if os.path.isdir(os.path.join(d, ".tools")) and os.path.isdir(os.path.join(d, "lib")):
            return d
        d = os.path.dirname(d)
    raise SystemExit("FIRM-SCHEDULES ok=False: no repository root above " + HERE)


REPO = repo_root()
sys.path.insert(0, os.path.join(REPO, "lib"))
os.chdir(REPO)

import opal_naming  # noqa: E402
import opal_naming_rootcheck as rc  # noqa: E402
import opal_naming_rootmap  # noqa: E402


def firm_lines_of(key):
    """[(root key, type, current, new, where, kind, detail)] for the schedule lines of one root whose decided new name
    (or refused name) carries a firm token. Run in a worker process."""
    out, sink = [], []
    rc.check_root("infra/aws/terraform/" + key, MAP, out=lambda line: None, report_only=True, sink=sink)
    for row in sink[1:]:
        it, _ans, kind, detail = row
        if it["type"] not in ("EVENT_RULE", "SCHEDULE") or kind not in ("FIX", "HOLE"):
            continue
        d = str(detail)
        if kind == "HOLE":
            if rc.BUILDER_REFUSED not in d:
                continue
            m = re.search(r"\((\S+)\):", d)
            d_name = m.group(1) if m else ""
        else:
            d_name = d
        if any(t in d_name.split("-") for t in FIRM_TOKENS):
            out.append((key, it["type"], it["current"], d_name, it["where"], kind, d))
    return out


def discover():
    doc = opal_naming_rootmap.load_map(MAP)
    keys = [k for k in sorted(doc["roots"]) if not opal_naming_rootmap.nothing_to_name(doc["roots"][k])]
    rows = []
    with concurrent.futures.ProcessPoolExecutor(max_workers=6) as pool:
        for part in pool.map(firm_lines_of, keys):
            rows.extend(part)
    return len(keys), rows


def drafted_rows():
    """The set of names the drafted registry rows cover (a row's _cite or evidence names the schedule name)."""
    if not os.path.isfile(ROWS_FILE):
        return {}, "REGISTRY_ROWS_round14.json absent"
    with open(ROWS_FILE, "rb") as fh:
        doc = json.loads(fh.read().decode("utf-8"))
    per_file = {}
    for fname, rows in doc.items():
        if fname.startswith("_") or not isinstance(rows, list):
            continue
        per_file[fname] = rows
    return per_file, None


def read_tf(path):
    with open(os.path.join(REPO, path), "rb") as fh:
        return fh.read().decode("utf-8")


def name_line_index(lines, where_line, current):
    """Index of the name attribute line of the resource declared at where_line (1-based): the first `name = "..."` line
    after it and before the next block opening at column 0. The line holds the literal `current`, or an interpolation that
    builds it (`"${local.x}-daily"`). None when there is none."""
    pat = re.compile(r'^(\s*name\s*=\s*)"(?:[^"\\]|\\.)*"\s*(#.*)?$')
    for i in range(where_line - 1, min(len(lines), where_line + 60)):
        if i >= where_line and re.match(r"^(resource|data|module|locals|variable|output)\b", lines[i]):
            return None
        if pat.match(lines[i]):
            return i
    return None


def make_diffs(items, mode):
    """{path: unified diff text} and {item index: (path, set of post-image line numbers owned by the item)}.
    mode "builder": the name attribute reads module.<label>.name and the module block is appended;
    mode "literal": the name attribute holds the listed string typed as a literal."""
    by_file = {}
    for n, it in enumerate(items):
        by_file.setdefault(it["path"], []).append(n)
    diffs, owned = {}, {}
    for path, idxs in by_file.items():
        text = read_tf(path)
        nl = "\r\n" if "\r\n" in text else "\n"
        lines = text.split(nl)
        post = list(lines)
        blocks = []
        for n in idxs:
            it = items[n]
            at = name_line_index(post, it["line"], it["current"])
            if at is None:
                owned[n] = (path, None)
                continue
            m = re.match(r'^(\s*name\s*=\s*)"', post[at])
            if mode == "literal":
                post[at] = m.group(1) + '"%s"' % it["new"]
                owned[n] = (path, {at + 1})
            else:
                label = "opal_name_fs_%d" % n
                post[at] = m.group(1) + "module.%s.name" % label
                p = it["parts"]
                blocks.append((n, [
                    "",
                    'module "%s" {' % label,
                    '  source   = "../../modules/opal_name"',
                    '  system   = "%s"' % p[0],
                    '  scope    = "%s"' % p[1],
                    '  function = "%s"' % p[2],
                    '  kind     = "%s"' % p[3],
                    "}"]))
                owned[n] = (path, {at + 1})
        if blocks:
            if post and post[-1] == "":
                post.pop()
            for n, blk in blocks:
                start = len(post) + 1
                post.extend(blk)
                owned[n][1].update(range(start, len(post) + 1))
            post.append("")
        a = [x + nl for x in lines[:-1]] + ([lines[-1]] if lines[-1] else [])
        b = [x + nl for x in post[:-1]] + ([post[-1]] if post[-1] else [])
        diffs[path] = "".join(difflib.unified_diff(a, b, "a/" + path, "b/" + path))
    return diffs, owned


def run_gate(diff_text, tag, tmpdir):
    path = os.path.join(tmpdir, tag + ".diff")
    with open(path, "wb") as fh:
        fh.write(diff_text.encode("utf-8"))
    return subprocess.Popen([sys.executable, os.path.join(REPO, ".tools", "naming-gate.py"), "--diff", path, "--enforce"],
                            cwd=REPO, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)


_REFUSE_RE = re.compile(r"^NAMING REFUSE (\S+?):(\d+) ", re.M)


def refusals(output):
    return [(m.group(1), int(m.group(2))) for m in _REFUSE_RE.finditer(output)]


def main():
    t0 = time.time()
    n_roots, rows = discover()
    sys.stderr.write("STAGE discover %.1fs\n" % (time.time() - t0))
    items = []
    for key, typ, cur, new, where, kind, detail in rows:
        path, _, line = where.rpartition(":")
        items.append({"root": key, "type": typ, "current": cur, "new": new, "path": path, "line": int(line),
                      "kind": kind, "detail": detail, "parts": rc.firm_schedule_parts(new)})
    problems = []
    for it in items:
        it["built"], it["refusal"] = None, None
        if it["parts"] is None:
            it["refusal"] = "the name does not read as {system}-{firm}-{function}-{kind}"
            continue
        try:
            it["built"] = opal_naming.name(*it["parts"])
        except ValueError as exc:
            it["refusal"] = str(exc)
    # the gate arms run only on lines whose name the builder produced; one gate process per root and arm, all at once
    live = [it for it in items if it["built"] is not None]
    scratch = os.path.join(REPO, ".scratch")
    tmpdir = tempfile.mkdtemp(prefix="fs_r14_", dir=scratch if os.path.isdir(scratch) else None)
    groups = {}
    for it in live:
        groups.setdefault(it["root"], []).append(it)
    runs = []
    for root, grp in sorted(groups.items()):
        for mode in ("builder", "literal"):
            diffs, owned = make_diffs(grp, mode)
            runs.append((root, mode, grp, owned, run_gate("".join(diffs.values()), "%s_%s" % (root.replace("/", "_"), mode),
                                                          tmpdir)))
    b_rc, l_rc, b_ref, l_ref = 0, 0, 0, 0
    for root, mode, grp, owned, proc in runs:
        try:
            text = proc.communicate(timeout=110)[0].decode("utf-8", "replace")
            rcode = proc.returncode
        except subprocess.TimeoutExpired:
            proc.kill()
            text, rcode = "", "timeout"
        refs = refusals(text)
        for k, it in enumerate(grp):
            it["owned_" + mode] = owned.get(k)
            it["rc_" + mode] = rcode
            it["refs_" + mode] = refs
        if mode == "builder":
            b_ref += len(refs)
            b_rc = b_rc if b_rc not in (0, None) else rcode
        else:
            l_ref += len(refs)
            l_rc = l_rc if l_rc not in (0, None) else rcode
    sys.stderr.write("STAGE gates done %.1fs\n" % (time.time() - t0))
    drafted, drafted_err = drafted_rows()
    n_builder = n_pass = n_owed = n_hand = n_ctl = 0
    for it in items:
        ctl = gate = "n/a"
        if it["built"] is not None:
            pb, ownb = it["owned_builder"]
            pl, ownl = it["owned_literal"]
            if ownb is None or ownl is None:
                gate = "UNPLACED"
                problems.append("no name attribute found for %s at %s:%d" % (it["current"], it["path"], it["line"]))
            else:
                hit_b = [r for r in it["refs_builder"] if r[0] == pb and r[1] in ownb]
                hit_l = [r for r in it["refs_literal"] if r[0] == pl and r[1] in ownl]
                gate = "REFUSED" if hit_b else ("PASS" if it["rc_builder"] == 0 else "FAIL(rc=%s)" % (it["rc_builder"],))
                ctl = "REFUSED" if hit_l else "NOT-REFUSED"
        if it["built"] is None:
            pass
        elif it["built"] == it["new"]:
            n_builder += 1
        else:
            n_hand += 1
        if gate == "PASS":
            n_pass += 1
        if ctl == "REFUSED":
            n_ctl += 1
        owed = ""
        if it["refusal"] is not None:
            covered = any(it["new"] in json.dumps(r) for rs in drafted.values() for r in rs)
            if covered:
                n_owed += 1
            owed = " builder-refused=%r drafted-row=%s" % (it["refusal"], covered)
        print("FIRM-SCHEDULE %s %s -> %s  builder=%s gate=%s control=%s%s  [%s:%d]" % (
            it["root"], it["current"], it["new"],
            "OK" if it["built"] == it["new"] else ("DIFFERS" if it["built"] else "REFUSED"), gate, ctl, owed,
            it["path"], it["line"]))
    n = len(items)
    print("GATE-ARMS builder rc=%s refusals=%d | literal-control rc=%s refusals=%d | roots read=%d" % (
        b_rc, b_ref, l_rc, l_ref, n_roots))
    if drafted_err:
        problems.append(drafted_err)
    if n_ctl != len(live):
        problems.append("the difference control refused %d of %d hand-typed names" % (n_ctl, len(live)))
    unattributed = [r for it in live for r in it["refs_builder"] if not any(
        o is not None and o[0] == r[0] and r[1] in o[1] for o in [x["owned_builder"] for x in live if x["root"] == it["root"]])]
    if unattributed:
        problems.append("builder-arm refusals outside every line: %r" % (unattributed,))
    for p in problems:
        print("FAIL: " + p)
    ok = (n > 0 and not problems and n_hand == 0 and n_builder + n_owed == n and n_pass + n_owed == n)
    print("FIRM-SCHEDULES ok=%s lines=%d builder_names=%d gate_pass=%d owed_rows=%d hand_composed=%d" % (
        ok, n, n_builder, n_pass, n_owed, n_hand))
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
