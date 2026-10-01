"""HVST-p-2 AC1: the two causes, from the RECORDED run artifacts through the BASE code path.

Read-only over the collector's runtime root (progress.sqlite3 opened mode=ro, events.jsonl,
runs/*.json, run_records/*.json, harvest_listing/*). No vendor call, no S3, no collection run.
The code path is the BASE (commit b635dadc66) exported with `git archive` and imported as its own
package, so the file:line named below are the lines the recorded runs actually went through.

Run: python org/missions/D5/AMGT/AMGT_HARVST/deliverables/0.9.0_WK_AMGT_HARVST~67/scripts/p2_ac1_causes.py
"""

import importlib.util
import io
import json
from pathlib import Path
import shutil
import sqlite3
import subprocess
import sys
import tarfile
import tempfile

BASE = "b635dadc66"
RUN1 = "20260930T044003Z-run-b75f9299"
RUN2 = "20260930T045332Z-run-75d4c464"
KEY = "bbg:NM5NLQ6K50XZ01"
HERE = Path(__file__).resolve().parent
OUT = HERE.parent


def git(*args, cwd=None):
    return subprocess.run(["git"] + list(args), cwd=cwd, capture_output=True, check=True).stdout


REPO = Path(git("rev-parse", "--show-toplevel", cwd=HERE).decode().strip())
COMMON = Path(git("rev-parse", "--git-common-dir", cwd=HERE).decode().strip())
if not COMMON.is_absolute():
    COMMON = (HERE / COMMON).resolve()
RUNTIME = COMMON.parent / ".runtime" / "opal-data-harvest"


RUNPIN = "65aa9251bc"  # the code pin the recorded runs ran on (HVST-o-5's preflight); BASE adds HVST-o-1 above it


def lines_at(ref, path):
    return git("show", "%s:%s" % (ref, path), cwd=REPO).decode("utf-8").splitlines()


def base_lines(path):
    return lines_at(BASE, path)


def anchor(path, text, nth=1):
    """The 1-based line number of the nth line of `path` at BASE containing `text`."""
    hits = [i + 1 for i, line in enumerate(base_lines(path)) if text in line]
    assert len(hits) >= nth, "anchor %r not found in %s@%s" % (text, path, BASE)
    return hits[nth - 1]


def show(path, line):
    """The line at BASE and the SAME line's number at the pin the runs actually ran on (the text
    must be byte-identical there, asserted): the cause is cited on both."""
    text = base_lines(path)[line - 1]
    pinned = [i + 1 for i, candidate in enumerate(lines_at(RUNPIN, path)) if candidate == text]
    assert pinned, "line %s:%d is not present at the run pin %s" % (path, line, RUNPIN)
    return "%s:%d @%s (= :%d @%s, the pin the recorded runs ran on)  %s" % (
        path, line, BASE, pinned[0], RUNPIN, text.strip())


def section(title):
    print("\n" + "=" * 78 + "\n" + title + "\n" + "=" * 78)


W = "lib/opal_data_harvest/worker.py"
P = "lib/opal_data_harvest/publishers.py"
C = "lib/opal_data_harvest/catalog.py"

print("HVST-p-2 AC1 -- runtime root: %s (read-only)  base code: %s" % (RUNTIME, BASE))
assert RUNTIME.is_dir(), "runtime root not found"

# ---------------------------------------------------------------- load the recorded artifacts
rec1 = json.loads((RUNTIME / "run_records" / (RUN1 + ".json")).read_text(encoding="utf-8"))
rec2 = json.loads((RUNTIME / "run_records" / (RUN2 + ".json")).read_text(encoding="utf-8"))
jobs1 = {}
for job in rec1["jobs"]:
    jobs1[job["job_id"]] = json.loads((RUNTIME / "runs" / (job["job_id"] + ".json")).read_text(encoding="utf-8"))
jobs2 = {}
for job in rec2["jobs"]:
    jobs2[job["job_id"]] = json.loads((RUNTIME / "runs" / (job["job_id"] + ".json")).read_text(encoding="utf-8"))
db = sqlite3.connect("file:%s?mode=ro" % (RUNTIME / "progress.sqlite3").as_posix(), uri=True)
outbox = {row[0]: json.loads(row[1]) for row in db.execute("SELECT article_key, record_json FROM harvest_raw_outbox")}
outbox_status = {row[0]: row[1] for row in db.execute("SELECT article_key, status FROM harvest_raw_outbox")}
aliases = {(r[0], r[1]): r[2] for r in db.execute("SELECT publisher, url, article_key FROM article_aliases")}
events = (RUNTIME / "events.jsonl").read_text(encoding="utf-8").splitlines()

evidence = OUT / "p2_evidence"
evidence.mkdir(exist_ok=True)
for name in (RUN1, RUN2):
    shutil.copyfile(RUNTIME / "run_records" / (name + ".json"), evidence / ("p2_run_record_" + name + ".json"))
for job_id in list(jobs1) + list(jobs2):
    shutil.copyfile(RUNTIME / "runs" / (job_id + ".json"), evidence / ("p2_job_" + job_id + ".json"))

# ---------------------------------------------------------------- (a) run 1's 22 fetched keys
section("(a) Run 1 %s: each of its %d keys_fetched, stored or not stored" % (RUN1, len(rec1["keys_fetched"])))
print("run record counts: %s ; outbox rows (all publishers): %d" % (rec1["counts"], len(outbox)))
by_url = {}
for key, record in outbox.items():
    by_url.setdefault((record.get("publisher"), record.get("url")), []).append(key)
stored, not_stored = [], []
for key in rec1["keys_fetched"]:
    pub, _, rest = key.partition(":")
    if key in outbox:
        stored.append((key, key, "outbox key = fetched key"))
    elif (pub, rest) in by_url:
        stored.append((key, by_url[(pub, rest)][0], "outbox record url = fetched key url"))
    else:
        not_stored.append(key)
for i, (key, out_key, how) in enumerate(stored, 1):
    print("  %2d STORED      %-100s -> %s [%s, outbox status=%s]" % (i, key[:100], out_key, how, outbox_status[out_key]))
for key in not_stored:
    print("  -- NOT STORED  %s" % key)
print("classification: %d stored + %d not stored = %d of %d keys_fetched  (bbg: %d of %d stored; wsj: %d of %d stored)" % (
    len(stored), len(not_stored), len(stored) + len(not_stored), len(rec1["keys_fetched"]),
    sum(1 for k, _, _ in stored if k.startswith("bbg:")), sum(1 for k in rec1["keys_fetched"] if k.startswith("bbg:")),
    sum(1 for k, _, _ in stored if k.startswith("wsj:")), sum(1 for k in rec1["keys_fetched"] if k.startswith("wsj:"))))
assert not_stored == [KEY], not_stored

section("(a) the run-record entry, the outbox absence, the job that fetched it")
print("run 1 keys_fetched contains %s: %s" % (KEY, KEY in rec1["keys_fetched"]))
print("run 1 outbox row for %s: %s ; article_objects rows with that id: %s" % (
    KEY, "PRESENT" if KEY in outbox else "ABSENT",
    db.execute("SELECT count(*) FROM article_objects WHERE article_id='NM5NLQ6K50XZ01'").fetchone()[0]))
bbg1 = [j for j in jobs1.values() if j["publisher"] == "bbg"][0]
print("run 1 bbg job %s: status=%s accepted=%d fetched_keys=%d rejected=%d" % (
    bbg1["job_id"], bbg1["status"], len(bbg1["accepted"]), len(bbg1["fetched_keys"]), len(bbg1["rejected"])))
print("run 1 bbg job rejected entries (VERBATIM): %s" % json.dumps(bbg1["rejected"]))
print("run 1 bbg job: fetched %d = accepted %d + rejected %d ; the one fetched key with no accepted article: %s" % (
    len(bbg1["fetched_keys"]), len(bbg1["accepted"]), len(bbg1["rejected"]),
    [k for k in bbg1["fetched_keys"] if k not in {a["article_key"] for a in bbg1["accepted"]}]))
print("run record jobs[] entry for it (VERBATIM): %s" % json.dumps([j for j in rec1["jobs"] if j["job_id"] == bbg1["job_id"]][0]))
print("run record carries the rejection anywhere? keys with 'reject' in run 1's record: %s" % (
    [k for k in rec1 if "reject" in k] + [k for j in rec1["jobs"] for k in j if "reject" in k]))

section("(a) events.jsonl lines for the key (of %d lines)" % len(events))
hits = [(i + 1, line) for i, line in enumerate(events) if "NM5NLQ6K50XZ01" in line]
for number, line in hits:
    print("  events.jsonl:%d %s" % (number, line))
print("  %d event lines name the id: one story GET per run, both 200/9152 bytes; NO event of any kind records a rejection" % len(hits))
rejections = [line for line in events if json.loads(line).get("event") not in ("http",) and "reject" in json.loads(line).get("event", "")
              or json.loads(line).get("event") == "article_rejected"]
print("  event lines whose EVENT NAME is a body rejection (article_rejected / *reject*, http lines excluded): %d of %d" % (len(rejections), len(events)))

section("(a) the listing that found it, and the rejected URL joined to the id")
listing_hit = None
for path in sorted((RUNTIME / "harvest_listing").glob("bbg_*")):
    payload = json.loads(path.read_bytes().decode("utf-8"))
    for item in payload.get("results", []):
        if item.get("resourceId") == "NM5NLQ6K50XZ01":
            listing_hit = (path.name, item)
print("listing %s: resourceId=%s subtype=%s url=%s" % (
    listing_hit[0], listing_hit[1]["resourceId"], listing_hit[1].get("subtype"), listing_hit[1]["url"]))
rejected_url = bbg1["rejected"][0]["url"]
print("recorded rejected url == listing url of NM5NLQ6K50XZ01: %s" % (rejected_url == listing_hit[1]["url"]))
assert rejected_url == listing_hit[1]["url"]
print("(the rejected entry carries the URL only, no key: the id join above is by URL through the listing)")

section("(a) run 2 %s fetched it again" % RUN2)
print("run 2 keys_fetched: %s" % rec2["keys_fetched"])
bbg2 = [j for j in jobs2.values() if j["publisher"] == "bbg"][0]
print("run 2 bbg job: accepted=%s rejected=%s (same URL: %s)" % (
    [a["article_id"] for a in bbg2["accepted"]], bbg2["rejected"], bbg2["rejected"] == bbg1["rejected"]))
print("run 2 skipped the 10 stored bbg ids as known_ids (%d skipped), and NOT %s: known_ids is built from the `articles` table (worker.py:%d) which a rejected article never enters" % (
    sum(1 for e in rec2["keys_skipped_as_held"] if e["key"].startswith("bbg:")), KEY,
    anchor(W, "SELECT article_id,path FROM articles WHERE publisher=?")))

section("(a) CAUSE, on the code path the recorded artifacts went through (BASE %s)" % BASE)
steps = [
    ("1. the key is noted as fetched BEFORE the GET returns, unconditionally", show(P, anchor(P, '_note_fetch("bbg:" + str(identity))'))),
    ("2. the response is normalised; a body under 120 words / 3 blocks gets issues=[short_or_partial_body], content_status=rejected", show(P, anchor(P, 'issues.append("short_or_partial_body")'))),
    ("3. the worker drops it on purpose: appends {url, issues} (no key) and `continue`s -- before catalog.store and before _write_harvest_raw", show(W, anchor(W, 'result["rejected"].append'))),
    ("4. the worker folds EVERY key the client noted into the job's fetched_keys, rejected or not", show(W, anchor(W, 'for fetched_key in list(getattr(client, "fetched_keys"'))),
    ("5. the run record lists every job fetched_key as keys_fetched, and never reads result[rejected]", show(W, anchor(W, 'job_fetched = list(result.get("fetched_keys")'))),
    ("6. the run record's keys_fetched is that list", show(W, anchor(W, '"keys_fetched": fetched, "keys_skipped_as_held": skipped'))),
    ("7. the outbox row is written only past the reject, by _write_harvest_raw", show(W, anchor(W, "self._write_harvest_raw(article, article_key)"))),
]
for label, text in steps:
    print("  %s\n       %s" % (label, text))
print("CAUSE (a): the fetch WAS rejected on purpose (short_or_partial_body: the Superfish 2015 story is a stub), and the rejection is recorded")
print("  in the job file (rejected[] with url+issues) but the run record counts the key from step 1 as fetched. Not stored is correct; 'fetched' is the")
print("  mislabel. A rejected article is never held, so run 2 re-fetched it (one GET per run; an accepted cost, see the fix).")

# ---------------------------------------------------------------- replay through the real BASE code
section("(a)+(b) REPLAY: the recorded job results through the BASE Worker.write_run_record")
tmp = Path(tempfile.mkdtemp(prefix="p2_base_"))
buffer = io.BytesIO(git("archive", BASE, "lib/opal_data_harvest", cwd=REPO))
with tarfile.open(fileobj=buffer) as archive:
    archive.extractall(tmp)
spec = importlib.util.spec_from_file_location("p2base_odh", tmp / "lib" / "opal_data_harvest" / "__init__.py",
                                              submodule_search_locations=[str(tmp / "lib" / "opal_data_harvest")])
package = importlib.util.module_from_spec(spec)
sys.modules["p2base_odh"] = package
spec.loader.exec_module(package)
import p2base_odh.worker as base_worker  # noqa: E402

replay_root = Path(tempfile.mkdtemp(prefix="p2_replay_"))
worker = base_worker.Worker(replay_root, {"retrieval_mode": "backfill"}, publisher_factory=None, session_manager=object())
results = [jobs1[job["job_id"]] for job in rec1["jobs"]]
replayed_path = worker.write_run_record(RUN1, rec1["started_at"], results)
replayed = json.loads(Path(replayed_path).read_text(encoding="utf-8"))
worker.close()
print("BASE write_run_record over the %d recorded job files -> keys_fetched %d ; recorded run record keys_fetched %d ; identical: %s" % (
    len(results), len(replayed["keys_fetched"]), len(rec1["keys_fetched"]), replayed["keys_fetched"] == rec1["keys_fetched"]))
print("BASE counts: %s ; recorded counts: %s" % (replayed["counts"], rec1["counts"]))
print("BASE record still lists %s among keys_fetched: %s ; carries any rejection field: %s" % (
    KEY, KEY in replayed["keys_fetched"], [k for k in replayed if "reject" in k]))
assert replayed["keys_fetched"] == rec1["keys_fetched"] and KEY in replayed["keys_fetched"]

# ---------------------------------------------------------------- (b) the wsj key split
section("(b) wsj: run 1's run-record keys vs the outbox keys")
wsj_fetched = [k for k in rec1["keys_fetched"] if k.startswith("wsj:")]
print("run 1 wsj keys_fetched: %d ; outbox wsj rows: %d" % (len(wsj_fetched), sum(1 for k in outbox if k.startswith("wsj:"))))
same_key = [k for k in wsj_fetched if k in outbox]
print("run-record wsj keys that ARE an outbox key: %d of %d (bbg: %d of %d)" % (
    len(same_key), len(wsj_fetched), sum(1 for k in rec1["keys_fetched"] if k.startswith("bbg:") and k in outbox),
    sum(1 for k in rec1["keys_fetched"] if k.startswith("bbg:"))))
wsj1 = [j for j in jobs1.values() if j["publisher"] == "wsj"][0]
accepted_by_position = {a["article_key"]: a for a in wsj1["accepted"]}
for key in wsj_fetched:
    match = by_url.get(("wsj", key[4:]))
    print("  run-record key %s\n      outbox key %s  (alias table: %s)" % (
        key, match[0] if match else None, aliases.get(("wsj", key[4:])) if aliases.get(("wsj", key[4:])) else "no alias for this url"))
print("join by url (outbox record_json.url == fetched url): %d of %d ; by key equality: %d of %d" % (
    sum(1 for k in wsj_fetched if ("wsj", k[4:]) in by_url), len(wsj_fetched), len(same_key), len(wsj_fetched)))
print("the url join is INCIDENTAL, not recorded: the outbox url is `canonicalUrl or url` (publishers.py:%d), so a canonicalUrl differing from the fetched url breaks it" % (
    anchor(P, 'article.get("canonicalUrl") or url')))
section("(b) CAUSE, on the code path (BASE %s)" % BASE)
for label, text in [
    ("1. wsj/barrons note the fetch by the URL they are about to GET (the vendor id is not known until the response)", show(P, anchor(P, "self._note_fetch(self.pub + \":\" + url)"))),
    ("2. the article id is the vendor id READ FROM THE RESPONSE", show(P, anchor(P, "article_id=article.get(\"id\")"))),
    ("3. the outbox/catalog key is publisher:article_id, i.e. the UUID", show(C, anchor(C, 'article_key = article["publisher"] + ":" + str(article["article_id"])'))),
    ("4. the run record lists the step-1 key and never the step-3 key", show(W, anchor(W, "job_fetched = list(result.get(\"fetched_keys\")"))),
    ("5. the accepted[] entry holds the step-3 key but the run record does not read it", show(W, anchor(W, '"article_key": article_key, "body_sha256"'))),
]:
    print("  %s\n       %s" % (label, text))
print("CAUSE (b): two key spaces by construction -- the fetch-time key is the URL (the only thing known before the GET), the stored key is the vendor UUID (known only")
print("  from the response) -- and NOTHING RECORDS THE PAIR. bbg/sa/ft joined only because their pre-fetch identity IS the stored identity.")
print("  The pair exists only in the catalog's article_aliases (url -> article_key) and the outbox record's url field, neither in the run record; the outbox url is the")
print("  response's canonicalUrl when it has one, so that join holds for these 11 by coincidence of canonicalUrl == fetched url, not by construction.")
print("  Why one key space is not the smaller change: the pre-fetch skip decisions (known_urls, listing hits) run before any response, so they can only be URL keys.")

shutil.rmtree(tmp, ignore_errors=True)
shutil.rmtree(replay_root, ignore_errors=True)
print("\nAC1 DONE: (a) %d of %d run-1 fetched keys stored, 1 not stored (%s, rejected short_or_partial_body); (b) wsj 0 of %d run-record keys equal an outbox key" % (
    len(stored), len(rec1["keys_fetched"]), KEY, len(wsj_fetched)))
