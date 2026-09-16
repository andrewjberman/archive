#!/usr/bin/env python3
"""blind_seat.py -- LGIC_NAMING round 3's clean-context seat (RULING B, round-1 analysis s.3 @de52d3db04; the briefing
per 1.0.0_SA_CTO's round-2 analysis s.3 and s.5 @02f08322af, RULINGS DM and POS).

Issued by 2.0.0_SA_COO~G with the round-3 issuance. Round 2's seat (fixed_inputs/r2/blind_seat.py) is unchanged in
mechanism; what changed is the briefing:
- the namers (e1, e2) read the naming schema and the identity REGISTRY's three row files, never the seed
  05_IDENTITY_SPINE.md (the registry governs where it and the seed differ: NAMING_SCHEMA.json v1.7 rows_owner);
- the reader (e4) is told how each name family is built (its grammar line, verbatim from the schema) and the closed
  firm spellings (firm_forms), and reads the same three registry files. It is never given the item set or the key.

A worker subagent starts with the workspace CLAUDE.md and the auto-memory in context (row LGIC_NAMING-S12), so it
cannot be the blind party. This file seats the blind party instead: a `claude -p` session with NO tools, launched in a
fresh empty folder outside the workspace, whose whole input is the prompt this file builds from committed sources. It
cannot read a file, so it cannot read the channel, the other namer's answer or any analysis (RULING C by construction).

Run from the worktree root:
    python <this file> run <cell>              cell in: e1 e2 e4
    python <this file> prompt <cell> [BASE]    print the prompt the builder makes at BASE (default HEAD)

`run` writes, under org/missions/D14/LGIC/LGIC_NAMING/deliverables/exercises/r3/:
    seats/<cell>.seat.json     the seat record (folder, parent-chain scan, argv, hashes, rc, session id)
    seats/<cell>.prompt.txt    the prompt, byte for byte
    seats/<cell>.raw.json      the session's JSON reply, byte for byte
    seats/<cell>.answer.txt    the reply's text, verbatim
    seats/<cell>.canary.txt    the two canary answers, for reading (the checker reads answer.txt, never this file)
    <the cell's answer file>   parsed from answer.txt by parse() below
It prints `SEAT: OK ...` and exits 0, or `SEAT: ERROR <reason>` and exits 1. The worker never writes the prompt and
never edits an answer: check_ln_r3.py re-derives the prompt with build() and re-parses the reply with parse().
"""
import datetime
import hashlib
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile

BASE = "org/missions/D14/LGIC/LGIC_NAMING"
EXR3 = BASE + "/deliverables/exercises/r3"
SEATS = EXR3 + "/seats"
FIX = BASE + "/deliverables/2.0.0_SA_COO~G/fixed_inputs"
SCHEMA = "org/standards/NAMING_SCHEMA.json"
REGISTRY = ("infra/logic/registry/scopes.json", "infra/logic/registry/systems.json", "infra/logic/registry/tiers.json")
ANSWER_FILE = {"e1": EXR3 + "/n3-namer-a.tsv", "e2": EXR3 + "/n3-namer-b.tsv", "e4": EXR3 + "/n3-reader.tsv"}
TIMEOUT = 540
DROP_ENV = ("CLAUDECODE", "CLAUDE_CODE_ENTRYPOINT")

CANARY = (
    "Before the task, answer two questions about the software workspace these instructions come from. "
    "If you do not know an answer, write unknown. Do not guess.\n"
    "Q1: Which version of the Git Bash default utilities is that workspace's local shell pinned to?\n"
    "Q2: Which broker port does that workspace's second agent fabric use?\n\n")

FORMAT = (
    "\nHOW TO ANSWER. First write the line Q1: <answer>, then the line Q2: <answer>. Then write the line ANSWERS. "
    "Then write exactly one line per {unit}, in the order given, as {shape}. Write nothing after the last of those lines.\n")


def now():
    return datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def sha(text):
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def show(base, path):
    """A file's bytes at a commit, decoded; the builder reads only committed sources, so a prompt is reproducible."""
    r = subprocess.run(["git", "show", "%s:%s" % (base, path)], capture_output=True)
    if r.returncode != 0:
        raise SystemExit("ERROR: cannot read %s at %s: %s" % (path, base, r.stderr.decode("utf-8", "replace").strip()))
    return r.stdout.decode("utf-8").replace("\r\n", "\n")


def tsv_rows(text):
    rows = []
    for ln in text.splitlines():
        s = ln.strip()
        if not s or s.startswith("#"):
            continue
        rows.append([c.strip() for c in ln.split("\t")])
    return rows


def reader_names(base):
    """The reader's input: namer A's round-3 names at BASE, a RAISE answer removed, unique, ascending."""
    rows = tsv_rows(show(base, ANSWER_FILE["e1"]))
    return sorted(set(r[1] for r in rows if len(r) >= 2 and r[1] and r[1] != "RAISE"))


def registry_docs(base, first):
    """The identity registry's three row files, as numbered documents starting at FIRST."""
    out = []
    for n, path in enumerate(REGISTRY, first):
        out.append("=== DOCUMENT %d: %s ===\n%s" % (n, path.rsplit("/", 1)[1], show(base, path)))
    return "\n".join(out)


def grammar_lines(base):
    """Each name family's slot order, verbatim from the schema, and the closed firm spellings (RULING POS)."""
    s = json.loads(show(base, SCHEMA))
    fams = [("resource names", s["resource"]["grammar"]), ("IAM policy names", s["iam_policy"]["grammar"]),
            ("secret names", s["secret"]["grammar"]), ("S3 keys", s["key"]["grammar"]),
            ("data bucket names", json.dumps(s["bucket"]["data_bucket"], ensure_ascii=True))]
    lines = "\n".join("- %s: %s" % (label, g) for label, g in fams)
    return lines + "\nThe firm spellings, long and short (firm_forms):\n" + json.dumps(s["firm_forms"], indent=1, ensure_ascii=True)


def build(cell, base):
    """The whole input of the cell's seat, from committed sources at BASE."""
    if cell in ("e1", "e2"):
        items = json.loads(show(base, FIX + "/N3_ITEMS.json"))["items"]
        lines = "\n".join("- %s (%s): %s" % (i["id"], i["type"], i["description"]) for i in items)
        task = ("TASK. You name NEW cloud resources for one organization. Your ONLY briefing is the documents below: "
                "its naming schema (JSON) and its identity registry (three JSON files: its scopes, its systems and its "
                "tiers). Derive every name from them alone. If a name cannot be derived from them, the answer for that "
                "item is RAISE.\n"
                "For a resource, give the full name. For an S3 key, give the key without the bucket, up to and including "
                "the partition, as the item says. For a bucket, give the bucket name.\n\n"
                "=== DOCUMENT 1: NAMING_SCHEMA.json ===\n" + show(base, SCHEMA)
                + "\n" + registry_docs(base, 2)
                + "\n=== THE ITEMS ===\n" + lines + "\n")
        return CANARY + task + FORMAT.format(unit="item", shape="<item id> -> <name>")
    if cell == "e4":
        task = ("TASK. Below is a list of names of cloud resources and storage keys from one organization. You have never "
                "seen this organization. You are told how its names are built -- the order of the parts of each kind of "
                "name -- and how its firms are spelled, and you have its identity registry (three JSON files). For each "
                "name, point at the part of the name that is the FIRM -- the client firm the resource or the data "
                "belongs to -- exactly as it is spelled in the name, or answer none if no part of the name is a firm.\n\n"
                "=== HOW NAMES ARE BUILT ===\n" + grammar_lines(base) + "\n\n"
                + registry_docs(base, 1)
                + "\n=== THE NAMES ===\n" + "\n".join(reader_names(base)) + "\n")
        return CANARY + task + FORMAT.format(unit="name", shape="<name> -> <the firm, exactly as spelled, or none>")
    raise SystemExit("ERROR: unknown cell %r (one of e1 e2 e4)" % cell)


def parse(result):
    """(canary, rows) from the seat's verbatim reply: Q1/Q2 before the ANSWERS line, then '<left> -> <right>' lines."""
    canary, rows, seen = {}, [], False
    for ln in result.splitlines():
        s = ln.strip().strip("`").strip()
        m = re.match(r"^\**(Q[12])\**\s*:\s*(.*)$", s)
        if not seen and m:
            canary[m.group(1)] = m.group(2).strip()
            continue
        if re.match(r"^\**ANSWERS\**\s*:?$", s):
            seen = True
            continue
        if seen and " -> " in s:
            left, right = s.split(" -> ", 1)
            rows.append([left.strip().lstrip("-*").strip(), right.strip()])
    return canary, rows


def parent_chain_claude_md(folder):
    found, d = [], folder
    while True:
        for f in ("CLAUDE.md", "CLAUDE.local.md", os.path.join(".claude", "CLAUDE.md")):
            if os.path.exists(os.path.join(d, f)):
                found.append(os.path.join(d, f).replace("\\", "/"))
        parent = os.path.dirname(d)
        if parent == d:
            return found
        d = parent


def write(path, text):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8", newline="") as fh:
        fh.write(text)


def fail(reason):
    print("SEAT: ERROR " + reason)
    return 1


def run(cell):
    if cell not in ANSWER_FILE:
        return fail("unknown cell %r (one of e1 e2 e4)" % cell)
    if not (os.path.isdir("org") and os.path.isdir(".tools")):
        return fail("run from the worktree root (org/ and .tools/ not found in %s)" % os.getcwd())
    root = os.path.realpath(os.getcwd())
    base = subprocess.run(["git", "rev-parse", "HEAD"], capture_output=True).stdout.decode().strip()
    prompt = build(cell, base)
    exe = shutil.which("claude")
    if not exe:
        return fail("the claude CLI is not on PATH")
    seat = os.path.realpath(tempfile.mkdtemp(prefix="opal_blindseat_r3_%s_" % cell))
    inside = os.path.normcase(seat).startswith(os.path.normcase(root) + os.sep)
    before = sorted(os.listdir(seat))
    chain = parent_chain_claude_md(seat)
    in_repo = subprocess.run(["git", "rev-parse", "--show-toplevel"], cwd=seat, capture_output=True).returncode == 0
    if inside or before or chain or in_repo:
        return fail("the seat folder is not clean: inside=%s files=%s claude_md=%s in_a_repo=%s" % (inside, before, chain, in_repo))
    env = {k: v for k, v in os.environ.items() if k not in DROP_ENV}
    argv = [exe, "-p", "--tools", "", "--output-format", "json"]
    started = now()
    try:
        r = subprocess.run(argv, input=prompt.encode("utf-8"), cwd=seat, env=env, capture_output=True, timeout=TIMEOUT)
        rc, out, err = r.returncode, r.stdout.decode("utf-8", "replace"), r.stderr.decode("utf-8", "replace")
    except subprocess.TimeoutExpired:
        rc, out, err = 124, "", "timeout after %d s" % TIMEOUT
    ended = now()
    left_behind = sorted(os.listdir(seat))
    if not left_behind:
        os.rmdir(seat)
    try:
        reply = json.loads(out)
    except ValueError:
        reply = {}
    result = reply.get("result") if isinstance(reply.get("result"), str) else ""
    canary, rows = parse(result)
    rec = {
        "cell": cell, "base": base, "started_utc": started, "ended_utc": ended,
        "seat_dir": seat.replace("\\", "/"), "seat_dir_inside_workspace": inside, "seat_dir_in_a_git_repo": in_repo,
        "files_in_seat_dir_before": len(before), "files_in_seat_dir_after": len(left_behind),
        "claude_md_in_parent_chain": chain,
        "argv": [os.path.basename(exe)] + argv[1:], "env_removed": [k for k in DROP_ENV if k in os.environ],
        "prompt_sha256": sha(prompt), "prompt_bytes": len(prompt.encode("utf-8")),
        "rc": rc, "is_error": reply.get("is_error"), "session_id": reply.get("session_id"),
        "num_turns": reply.get("num_turns"), "models": sorted((reply.get("modelUsage") or {}).keys()),
        "result_sha256": sha(result), "rows_parsed": len(rows), "stderr_head": err[:400],
    }
    write(SEATS + "/%s.prompt.txt" % cell, prompt)
    write(SEATS + "/%s.raw.json" % cell, out)
    write(SEATS + "/%s.answer.txt" % cell, result)
    write(SEATS + "/%s.canary.txt" % cell, "Q1: %s\nQ2: %s\n" % (canary.get("Q1"), canary.get("Q2")))
    write(SEATS + "/%s.seat.json" % cell, json.dumps(rec, indent=2) + "\n")
    body = "".join("%s\t%s\n" % (a, b) for a, b in rows)
    write(ANSWER_FILE[cell], "# base %s\n# seat %s\n%s" % (base, rec["session_id"], body))
    if rc != 0 or reply.get("is_error") is not False or not rows:
        return fail("cell %s rc=%s is_error=%s rows=%d stderr=%s" % (cell, rc, reply.get("is_error"), len(rows), err[:200]))
    print("SEAT: OK cell=%s rows=%d session=%s base=%s Q1=%r Q2=%r" % (
        cell, len(rows), rec["session_id"], base[:10], canary.get("Q1"), canary.get("Q2")))
    return 0


def main(argv):
    if len(argv) >= 3 and argv[1] == "run":
        return run(argv[2])
    if len(argv) >= 3 and argv[1] == "prompt":
        base = argv[3] if len(argv) > 3 else "HEAD"
        sys.stdout.write(build(argv[2], base))
        return 0
    print("usage: blind_seat.py run <e1|e2|e4>  |  blind_seat.py prompt <e1|e2|e4> [BASE]")
    return 1


if __name__ == "__main__":
    sys.exit(main(sys.argv))
