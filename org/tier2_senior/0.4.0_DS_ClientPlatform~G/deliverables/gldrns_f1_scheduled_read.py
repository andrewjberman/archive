"""GLD-f-1/2/3 -- the AC7 READ of the SCHEDULED twr_daily emission (OPAL_GLDRNS.TO-R1-DS).

RE-ADDRESSED to this seat by 1.0.0_SA_CTO 69386 after 0.4.0_DS_ClientPlatform~H went
dark with 21 of 23 cells delivered and this one open. THE NEW HOLDER BUILDS NOTHING --
the remedy is deployed and APPLIED-verified at b9a665364f / 77ecd4f0de / 2ee5f8ca43.
This file is a READ, and it is written BEFORE the 12:45Z fire so that the fire is a
run-and-read rather than a build.

============================================================================
WHY THIS HARNESS TAKES NO EXPECTED VALUES FROM ITS AUTHOR
============================================================================
CTO named the cost of putting me on this read and I am taking the mirror obligation.
I am one of the arms that CORROBORATED this census: my own emitter derived
{COMPUTED 6329, NOT_COMPUTED_INPUTS_PRESENT 909} against CVO's producer-side
{OK 6329, UNCOMPUTABLE-ZERO-BMV 901, REFUSED-NO-BMV 8}. If I walk into the fire
carrying 6329 as the expected value, I am running a SELF-COMPARISON and it will confirm.

  EVERY CHECK BELOW DERIVES ITS EXPECTATION FROM THE ARTIFACTS.
  My prior figures appear ONCE, in a clearly-labelled corroboration line that NO CHECK
  READS. If they disagree with the fire, that is a FINDING -- not a failed check, and
  not something the harness can quietly absorb.

An expected value supplied by the author is an instrument that could not have said
otherwise. CVO's independent re-derivation must likewise not lean on this file's output.

============================================================================
WHAT AC7 ACTUALLY REQUIRES, and the three traps in it
============================================================================
"REAL RETURNS EMITTING ON THE *SCHEDULED* RUN -- an ad-hoc run is a QA instrument and
NEVER production evidence. REFUSED-NO-BMV -> ZERO FOR ACCOUNTS PRESENT AT BOTH D AND
D-1; residual is accounts absent at D-1, reported with its count and the D/D-1
account-set delta beside it."

TRAP 1 -- THE SCOPE OF THE ZERO. `REFUSED-NO-BMV -> 0` is FALSE as a bare statement and
  true only over accounts present at BOTH days. An account that did not exist on D-1
  has no BMV to find, and refusing it is CORRECT. A harness testing the bare form fails
  a correct run; a harness ignoring the scope passes a broken one.

TRAP 2 -- THE STATUSES THAT MUST NOT GO TO ZERO. `NO-PRIOR-TRADING-DAY` and
  `UNCOMPUTABLE-ZERO-BMV` are REPORTED AND EXPLAINED, never driven to zero. CTO s.14(a):
  a bar that cannot be satisfied is broken, not high. A zero on either would mean the
  remedy MANUFACTURED a BMV, which AC3 forbids.

TRAP 3 -- THE INSTRUMENT THAT CANNOT SAY OTHERWISE. The c04 validation battery is NOT
  corroboration here: its check 7 passes `twr_daily=None` and has never evaluated a
  return. It sits exactly where a reader reaches for a second opinion. This harness
  prints that exclusion beside the verdict so nobody reaches for it later.

EVIDENCE VINTAGE: live 49F plane; deployed-bytes read resolved at run time and printed.
"""
from __future__ import annotations

import datetime as _dt
import argparse
import hashlib
import io
import json
import subprocess
import sys

import boto3
import pyarrow.parquet as pq

GOLD = "opal-data-49financial"
CANON = "gold/advi/canonical/"
DIMS = "gold/advi/dimensions/"

# The producer and the chain whose DEPLOYED bytes AC7 reads at the APPLIED layer.
CODE_UNDER_READ = (
    "data/assets/scripts/gold/runners_49f/c02_twr_engine.py",
    "data/assets/scripts/gold/runners_49f/chain_49f_entrypoint.py",
)

# Statuses that must be REPORTED and EXPLAINED, never driven to zero (trap 2).
NEVER_ZERO = ("NO-PRIOR-TRADING-DAY", "UNCOMPUTABLE-ZERO-BMV")

# Named rather than written inline: an escaped line-ending literal is the one thing in
# this file that cannot survive being retyped through a shell, and it got mangled twice
# while this harness was being written -- in the function whose whole subject is line
# endings. chr() is unambiguous at every layer.
CRLF = (chr(13) + chr(10)).encode("ascii")
LF = chr(10).encode("ascii")

# The EXECUTING code plane and the run's own log, both from the SSM document at
# infra/aws/terraform/opal-assets/advi_49f_floor.tf (:226 sync, :230 log upload).
CODE_PREFIX = "_code/"
LOG_PREFIX = "gold/advi/_logs/"

# CORROBORATION ONLY -- NO CHECK READS THIS. See the header. Disagreement is a finding.
PRIOR_CORROBORATION = {
    "0.4.0_DS_ClientPlatform~G (me, consumer-side, an earlier partition)":
        "{COMPUTED 6329, NOT_COMPUTED_INPUTS_PRESENT 909}",
    "3.0.0_SA_CVO (producer-side, same partition)":
        "{OK 6329, UNCOMPUTABLE-ZERO-BMV 901, REFUSED-NO-BMV 8}  (901+8=909)",
    "0.4.0_DS_ClientPlatform~H (ad-hoc QA chain, --date 2026-08-19, NOT production)":
        "{OK 6393, UNCOMPUTABLE-ZERO-BMV 922, REFUSED-NO-BMV 17}",
}

s3 = boto3.client("s3")


def _partitions(prefix):
    """MATERIALISE the list. A --query length() over a paginated list-* returns the
    PAGE count, and an absence verdict from a truncated page is indistinguishable from
    a real absence."""
    out, tok = set(), None
    while True:
        kw = dict(Bucket=GOLD, Prefix=prefix, Delimiter="/")
        if tok:
            kw["ContinuationToken"] = tok
        r = s3.list_objects_v2(**kw)
        for c in r.get("CommonPrefixes", []) or []:
            seg = c["Prefix"].rstrip("/").split("/")[-1]
            if seg.startswith("date="):
                out.add(seg.split("=", 1)[1])
        tok = r.get("NextContinuationToken")
        if not tok:
            return sorted(out)


class PartitionShapeChanged(Exception):
    """A partition stopped being one file. Raised, never absorbed -- see _read."""


def _read(prefix, date):
    """Read ONE partition, and REFUSE if it is not one file.

    MEASURED 2026-08-25 across every partition this harness touches: twr_daily 529/529,
    canonical_valuation 530/530, dim_calendar 5/5 are all single-file. So taking the one
    key is correct TODAY.

    IT IS ALSO A LATENT ASSUMPTION, and the failure mode is the one this whole TO keeps
    producing: if the producer ever emits two files, `keys[0]` returns a FRACTION of the
    partition and every count below it -- row totals, the status census, the D/D-1
    account sets, the AC7 scoped zero -- is computed over part of the data and reads as
    complete. A REFUSED-NO-BMV count taken over half a partition can be zero for the
    worst possible reason.
    Nothing in the output would say so, which is why this is an assertion rather than a
    comment. A loud refusal on a shape change costs one run; a silent fraction costs the
    verdict.
    """
    r = s3.list_objects_v2(Bucket=GOLD, Prefix="%sdate=%s/" % (prefix, date))
    keys = [o["Key"] for o in r.get("Contents", []) if o["Key"].endswith(".parquet")]
    if not keys:
        return None
    if len(keys) > 1:
        raise PartitionShapeChanged(
            "%sdate=%s/ holds %d parquet files; this harness reads one and every count "
            "it prints would be a FRACTION reported as a total. Read them all, or "
            "establish why there is more than one, before trusting any number below."
            % (prefix, date, len(keys)))
    body = s3.get_object(Bucket=GOLD, Key=keys[0])["Body"].read()
    return pq.read_table(io.BytesIO(body)).to_pandas()


def _manifest(prefix, date):
    try:
        return json.loads(s3.get_object(
            Bucket=GOLD, Key="%sdate=%s/manifest.json" % (prefix, date))["Body"].read())
    except Exception as exc:                       # absence is a RESULT, not an error
        return {"__absent__": "%s: %s" % (type(exc).__name__, exc)}


def _deployed_vs_ref(path, ref):
    """Rule 22a CODE layer -- read the bytes that EXECUTE, not the ones on this disk.

    CORRECTED. The first version of this harness compared the WORKTREE to a git ref.
    That is the wrong plane, and Rule 22a says so in its own words: reading an artifact
    proves what is THERE, never what RUNS. The SSM document at
    infra/aws/terraform/opal-assets/advi_49f_floor.tf:226 does

        aws s3 sync s3://opal-data-49financial/_code/ /tmp/advi_49f_code/ --delete
        cd /tmp/advi_49f_code && python3 chain_49f_entrypoint.py --production

    so THE EXECUTED BYTES COME FROM `_code/`. A file in this checkout has no causal
    relationship to the 12:45Z run at all.

    AND THIS IS THE CASE RULE 22a WARNS IS USUALLY *NOT* SAFE -- it says an S3-staged
    object may be INERT, because a first-boot-only pull lets a box run a baked copy.
    THAT EXEMPTION IS EARNED HERE FOR A SPECIFIC REASON, not assumed: the sync is INSIDE
    the runCommand, so it re-pulls on EVERY invocation.

    THREE PLANES, ALL PRINTED, because they answer different questions and tonight has
    produced four separate errors from conflating two of them:
      DEPLOYED (_code/)  what will run          <- the plane AC7 is about
      BLOB (git ref)     what was committed
      WORKTREE           what is on this disk   <- carries CRLF; says nothing about the run
    core.autocrlf=true here, so the worktree diverges from the blob on 8 of 79 tracked
    .py under runners_49f/ -- both files this reads included -- by line endings ALONE.
    A raw worktree-vs-ref compare reports drift where there is none: exactly the false
    provenance accusation CTO hit against DS~H's deploy.
    """
    blob = subprocess.run(["git", "show", "%s:%s" % (ref, path)],
                          capture_output=True).stdout
    if not blob:
        return {"error": "git show returned EMPTY for %s:%s -- a retrieval failure "
                         "returns a VALUE; not reporting this as absent" % (ref, path)}
    name = path.split("/")[-1]
    try:
        dep = s3.get_object(Bucket=GOLD, Key=CODE_PREFIX + name)["Body"].read()
    except Exception as exc:                    # absence is a RESULT, not an error
        return {"error": "deployed object %s%s unreadable: %s: %s"
                         % (CODE_PREFIX, name, type(exc).__name__, exc)}
    try:
        with io.open(path, "rb") as fh:
            work = fh.read()
    except OSError:
        work = None

    def norm(b):
        return b.replace(CRLF, LF)

    def h(b):
        return hashlib.sha256(b).hexdigest()[:16]

    return {
        "deployed_matches_ref": dep == blob,            # THE check AC7 rests on
        "deployed_sha256": h(dep),
        "blob_sha256": h(blob),
        "worktree_sha256": h(work) if work is not None else "UNREADABLE",
        "worktree_raw_match": (work == blob) if work is not None else None,
        "worktree_norm_match": (norm(work) == norm(blob)) if work is not None else None,
        "deployed_bytes": len(dep),
        "deployed_crlf": dep.count(CRLF),
        "worktree_crlf": work.count(CRLF) if work is not None else -1,
    }



CHAIN_DOCUMENT = "advi-49f-chain-dispatch"
SCHEDULED_SRC = "advi.49f.scheduled-floor"


def _dispatch_record(limit_pages=20):
    """The SCHEDULER-SIDE attribution, and the dispatch's own exit status.

    ADDED after I told CVO and CTO that scheduled-ness was EVIDENCE-FOR and not proof
    because the manifest carries no trigger field. THAT WAS TRUE OF THE ARTIFACT AND
    FALSE OF THE WORLD -- the dispatcher writes the scheduler's own source tag into the
    SSM command Comment (lambda_function.py:133,
    Comment=f"advi 49f dispatch src={event.get('source','manual')}"), and the schedule's
    Input supplies source=advi.49f.scheduled-floor. A MANUAL DISPATCH DEFAULTS TO
    src=manual. So the two are distinguishable in a queryable record written by the
    dispatcher, not by the thing being judged.

    AND THE STATUS IS THE HALF THAT MATTERS MORE. On 2026-08-23 and 2026-08-24 the
    scheduled dispatch returned Failed -- the chain aborted at a06_identity_crosswalk on
    an empty allocation-map partition, nine stages before c02_twr_daily. The ARTIFACT
    plane cannot show that: it looks identical to "the run has not happened yet".
    A HARNESS THAT READS ONLY THE PARTITION CANNOT TELL A RUN THAT NEVER FIRED FROM ONE
    THAT FIRED AND DIED.

    PAGINATION IS LOAD-BEARING HERE, not a detail: ssm.list_commands returned an EMPTY
    FIRST PAGE WITH A NextToken. Reading page one and stopping yields zero commands and
    reads as "no dispatch history", which is CLAUDE.md's own trap in its worst form --
    a clean zero that is a page artifact.

    TIMEZONE IS ALSO LOAD-BEARING: RequestedDateTime carries tzlocal(), so strftime
    renders LOCAL time. I rendered 12:45:41Z as "08:45Z" once and typed the Z myself.
    Every timestamp below is .astimezone(utc)-pinned before formatting.
    """
    try:
        ssm = boto3.client("ssm")
    except Exception as exc:
        return {"error": "ssm client: %s: %s" % (type(exc).__name__, exc)}
    cmds, tok, pages = [], None, 0
    while pages < limit_pages:
        kw = {"MaxResults": 50}
        if tok:
            kw["NextToken"] = tok
        try:
            r = ssm.list_commands(**kw)
        except Exception as exc:
            return {"error": "list_commands: %s: %s" % (type(exc).__name__, exc)}
        cmds += r.get("Commands", [])
        pages += 1
        tok = r.get("NextToken")
        if not tok:
            break
    chain = [c for c in cmds if c.get("DocumentName") == CHAIN_DOCUMENT]
    chain.sort(key=lambda c: c["RequestedDateTime"], reverse=True)
    out = []
    for c in chain[:6]:
        u = c["RequestedDateTime"].astimezone(_dt.timezone.utc)
        comment = c.get("Comment", "")
        out.append({
            "at_utc": u.strftime("%Y-%m-%dT%H:%M:%SZ"),
            "status": c.get("Status"),
            "comment": comment,
            "scheduled": SCHEDULED_SRC in comment,
        })
    return {"pages": pages, "exhausted": not bool(tok), "total_commands": len(cmds),
            "chain_dispatches": len(chain), "recent": out}


def _execution_record(date):
    """The SCHEDULED-vs-AD-HOC discriminator, which the ARTIFACT cannot supply.

    The first version of this harness said scheduled-ness was not decidable and stopped.
    It is not decidable FROM THE PARTITION -- the manifest carries no trigger field --
    but the chain uploads its own log on every run (advi_49f_floor.tf:230) and the log's
    FIRST LINE is:

        CHAIN START date=YYYY-MM-DD mode=production workdir=... stages=16

    WHAT EACH SIGNAL DOES AND DOES NOT ESTABLISH, kept separate because they are not
    equivalent and a verdict must not rest on the weakest one wearing the strongest
    one's name:
      mode=production  proves the FLAG the chain ran under. It does NOT prove the
                       SCHEDULER fired it -- a human passing --production produces the
                       identical line.
      bare chain_<TS>.log key  proves the SSM document's own command line wrote it.
                       Ad-hoc runs in this bucket have carried descriptive infixes
                       (chain_adhoc_qa_..., chain_backfill_...) -- but that is a HUMAN
                       CONVENTION, and a convention is not a control.
      TS in the 12:45Z window  consistent with aws_scheduler_schedule
                       advi-49f-gold-floor (flexible_time_window OFF, so exact).
    TOGETHER: strong evidence, NOT proof. The airtight source is the scheduler's own
    invocation history, which is outside this read. Reported as EVIDENCE-FOR with its
    limit named, never as a discharged fact.
    """
    out, tok = [], None
    while True:
        kw = dict(Bucket=GOLD, Prefix=LOG_PREFIX)
        if tok:
            kw["ContinuationToken"] = tok
        r = s3.list_objects_v2(**kw)
        out += [(o["Key"], o["LastModified"]) for o in r.get("Contents", [])]
        tok = r.get("NextContinuationToken")
        if not tok:
            break
    rows = []
    for key, mod in sorted(out, key=lambda t: t[1], reverse=True)[:6]:
        try:
            head = s3.get_object(Bucket=GOLD, Key=key)["Body"].read(400).decode(
                "utf-8", "replace").splitlines()
        except Exception:
            head = []
        first = head[0] if head else ""
        leaf = key.split("/")[-1]
        rows.append({
            "key": leaf,
            "modified": mod.isoformat(),        # boto3 = UTC; never `aws s3 ls` local
            "first_line": first[:92],
            "mode_production": "mode=production" in first,
            "bare_ssm_name": leaf.startswith("chain_20"),
            "covers_date": ("date=%s" % date) in first,
        })
    return rows


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--date", help="the partition to read; default = newest present")
    ap.add_argument("--ref", default="HEAD", help="the ref the deployed bytes are read against")
    a = ap.parse_args()

    print("GLD-f-1/2/3 -- AC7 READ OF THE SCHEDULED twr_daily EMISSION")
    print("OPAL_GLDRNS.TO-R1-DS, re-addressed to 0.4.0_DS_ClientPlatform~G (CTO 69386)")
    print("=" * 108)

    parts = _partitions(CANON + "twr_daily/")
    D = a.date or parts[-1]
    print("\n0. FRAME -- every denominator materialised, never a --query length()")
    print("   twr_daily partitions ......... {:,}  ({} .. {})".format(
        len(parts), parts[0], parts[-1]))
    print("   partition under read ......... {}{}".format(
        D, "" if a.date else "   <- newest present, not a date I typed"))
    if D not in parts:
        print("   REFUSED: date={} is not present. This is a MEASURED absence over {:,} "
              "partitions, not a failed read.".format(D, len(parts)))
        return 2

    # ---------- 1. the prior TRADING day, from dim_calendar ----------
    print("\n1. THE PRIOR TRADING DAY -- from dim_calendar, never wall-clock (AC2)")
    cal = _read(DIMS + "dim_calendar/", D)
    if cal is None:
        print("   REFUSED: dim_calendar absent at date=%s; the D-1 question is not "
              "answerable and I will not substitute wall-clock arithmetic." % D)
        return 2
    prev_map = dict(zip(cal["trading_day"].astype(str), cal["prev_trading_day"].astype(str)))
    prev = prev_map.get(D)
    print("   calendar rows ................ {:,}".format(len(cal)))
    print("   prev_trading_day({}) ... {}".format(D, prev))
    print("   The oracle is THE PRIOR TRADING DAY, not 'yesterday' and not 'Friday on a")
    print("   Monday'. ~H measured a wall-clock D-1 resolving the WRONG partition on")
    print("   118/533 = 22.1% of runs (102 Mondays + 16 post-holiday).")

    checks = []

    def chk(name, got, want, note=""):
        ok = got == want
        checks.append((ok, name))
        print("   [{}] {:<54} got={!s:<9} want={!s}{}".format(
            "PASS" if ok else "FAIL", name, got, want, ("  -- " + note) if note else ""))

    # ---------- 2. the emission ----------
    print("\n2. THE EMITTED PARTITION")
    twr = _read(CANON + "twr_daily/", D)
    man = _manifest(CANON + "twr_daily/", D)
    census = twr["status"].value_counts().to_dict()
    print("   rows ......................... {:,}".format(len(twr)))
    print("   columns ...................... {}  {}".format(
        len(twr.columns),
        "(9 = pre-remedy shape; 13 = the mirror landed)" if len(twr.columns) in (9, 13) else ""))
    print("   status census (from the DATA, not the manifest):")
    for k in sorted(census):
        print("     {:<26} {:>8,}".format(k, census[k]))
    print("   manifest bmv_source .......... {}".format(man.get("bmv_source", man)))
    mcensus = man.get("status_census")
    chk("manifest census == data census", mcensus, census,
        "the manifest is a CLAIM; the parquet is the artifact")

    # ---------- 3. AC7's scoped zero ----------
    print("\n3. AC7 -- REFUSED-NO-BMV ZERO *FOR ACCOUNTS PRESENT AT BOTH D AND D-1*")
    val_d = _read(CANON + "canonical_valuation/", D)
    val_p = _read(CANON + "canonical_valuation/", prev) if prev else None
    if val_d is None:
        print("   REFUSED: canonical_valuation absent at D; the both-days set is not")
        print("   derivable and the scoped zero cannot be evaluated. NOT a pass.")
        return 2
    set_d = set(val_d["account_id"].astype(str))
    set_p = set(val_p["account_id"].astype(str)) if val_p is not None else set()
    both = set_d & set_p
    only_d = set_d - set_p
    print("   accounts at D ................ {:,}".format(len(set_d)))
    print("   accounts at D-1 ({}) .. {:,}{}".format(
        prev, len(set_p), "   <- D-1 partition ABSENT" if val_p is None else ""))
    print("   present at BOTH .............. {:,}   <- AC7's denominator".format(len(both)))
    print("   at D but NOT at D-1 .......... {:,}   <- the legitimate residual".format(
        len(only_d)))

    refused = twr[twr["status"] == "REFUSED-NO-BMV"]
    ref_accts = set(refused["account_id"].astype(str))
    refused_in_both = ref_accts & both
    print("   REFUSED-NO-BMV rows .......... {:,}".format(len(refused)))
    print("   ...of which are in BOTH ...... {:,}   <- MUST BE ZERO".format(
        len(refused_in_both)))
    print("   ...of which are D-only ....... {:,}   <- CORRECT refusals, no BMV exists".format(
        len(ref_accts & only_d)))
    # ⛔ THE DENOMINATOR GUARD. Without this the next check passes VACUOUSLY whenever
    # the both-days set is empty -- prev_trading_day unresolvable, or the D-1
    # valuation partition absent. 0 refusals out of 0 accounts compares 0 == 0 and
    # reports PASS on the criterion Andrew's condition rests on.
    # A CRITERION EVALUATED OVER AN EMPTY SET IS UNEVALUABLE, NOT SATISFIED.
    chk("AC7 denominator is NON-EMPTY (both-days set)", len(both) > 0, True,
        "an empty both-set makes the scoped zero pass vacuously")
    if not both:
        print("   REFUSING to score the scoped zero: the both-days population is EMPTY.")
        print("   prev={!r}; accounts at D-1={}. Either the calendar did not resolve the".format(
            prev, len(set_p)))
        print("   prior trading day, or its canonical_valuation partition is absent.")
        print("   THAT IS UNCOMPUTABLE, NOT SATISFIED -- and the difference is the whole")
        print("   point of the guard above.")
    else:
        chk("REFUSED-NO-BMV == 0 over accounts present at BOTH days",
            len(refused_in_both), 0, "the bare form of this check is FALSE and would fail a good run")
        if refused_in_both:
            print("     first 5 offenders: {}".format(sorted(refused_in_both)[:5]))
    unexplained = ref_accts - both - only_d
    chk("every REFUSED account is accounted for by the D/D-1 delta",
        len(unexplained), 0, "a refusal outside both populations is unexplained")

    # ---------- 4. the statuses that must NOT be zero ----------
    print("\n4. REPORTED AND EXPLAINED, NEVER DRIVEN TO ZERO (CTO s.14(a))")
    for st in NEVER_ZERO:
        n = census.get(st, 0)
        print("   {:<26} {:>8,}   {}".format(st, n, "present" if n else "ABSENT at this partition"))
    print("   These are NOT checked for zero and NOT checked for non-zero. Their value is")
    print("   a fact about the data, and a bar demanding either would be broken, not high.")
    print("   A ZERO on these WITH real returns present would mean the remedy MANUFACTURED")
    print("   a BMV, which AC3 forbids -- so they are reported for a reader, not scored.")

    # ---------- 5. real returns ----------
    print("\n5. REAL RETURNS EMITTING -- the substance of AC7")
    computed = twr[twr["r_net"].notna()]
    print("   rows with a non-null r_net ... {:,} of {:,}  ({:.2f}%)".format(
        len(computed), len(twr), 100.0 * len(computed) / len(twr) if len(twr) else 0.0))
    chk("real returns are present", len(computed) > 0, True,
        "this is the criterion; a 100%-refused partition is the pre-remedy state")

    # ---------- 6. deployed bytes ----------
    print()
    print("6. RULE 22a CODE LAYER -- the bytes that WILL EXECUTE, not the ones on disk")
    _read_at = _dt.datetime.now(_dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    print("   IDENTITY READ AT %s -- and that stamp is the point (CVO 69674)." % _read_at)
    print("   DEPLOYED == BLOB IS A MOMENT, NOT A PROPERTY OF THE PATH. This harness",
          "re-reads")
    print("   `_code/` live on every run, so the premise is never baked -- but a",
          "safe-deploy")
    print("   from any tree between this read and the fire moves the executing bytes,",
          "and a")
    print("   verdict quoting an earlier read would be true of a moment that had passed.")
    print("   The SSM doc syncs s3://%s/%s on EVERY invocation and runs THAT"
          % (GOLD, CODE_PREFIX))
    print("   (advi_49f_floor.tf:226). A file in this checkout has no causal relationship")
    print("   to the run. Rule 22a warns a staged object may be INERT -- that exemption is")
    print("   earned here because the sync is INSIDE the runCommand, not first-boot-only.")
    for path in CODE_UNDER_READ:
        r = _deployed_vs_ref(path, a.ref)
        n = path.split("/")[-1]
        if "error" in r:
            print("   {:<26} ERROR: {}".format(n, r["error"]))
            checks.append((False, "deployed bytes readable: " + n))
            continue
        print("   {:<26} deployed={} blob={} worktree={}".format(
            n, r["deployed_sha256"], r["blob_sha256"], r["worktree_sha256"]))
        print("   {:<26}   deployed_bytes={:,}  deployed_crlf={}  worktree_crlf={}".format(
            "", r["deployed_bytes"], r["deployed_crlf"], r["worktree_crlf"]))
        print("   {:<26}   worktree raw={!s:<6} normalised={!s}   <- NEITHER is the AC7 check".format(
            "", r["worktree_raw_match"], r["worktree_norm_match"]))
        chk("DEPLOYED bytes == the ref that built them: " + n,
            r["deployed_matches_ref"], True,
            "the only compare on this rung that is about the run")
        if r.get("worktree_raw_match") is False and not r.get("worktree_norm_match"):
            print("   {:<26}   !! WORKTREE DIFFERS FROM THE REF BEYOND LINE ENDINGS --"
                  " a deploy".format(""))
            print("   {:<26}      from this tree would change the executing bytes."
                  .format("")) 

    print("\n7. EXCLUDED AS CORROBORATION, DELIBERATELY")
    print("   The c04 validation battery is NOT a second opinion on this read: its check 7")
    print("   passes twr_daily=None and has never evaluated a return. It sits exactly where")
    print("   a reader reaches for confirmation, and it could not have said otherwise.")
    print("\n   PRIOR FIGURES -- CORROBORATION ONLY. NO CHECK ABOVE READS THESE.")
    for who, what in PRIOR_CORROBORATION.items():
        print("     {:<62} {}".format(who[:62], what))
    print("   If the fire disagrees with these, that is a FINDING to route, not a failed")
    print("   check. I am one of these arms; scoring against them would be self-comparison.")

    # ---------- 8. the execution record ----------
    print()
    print("8. SCHEDULED OR AD-HOC -- the artifact cannot say, so read the RUN'S OWN LOG")
    print("   The manifest carries NO trigger field, so scheduled-ness is not decidable")
    print("   from the partition. The chain uploads its own log every run and the first")
    print("   line records the mode (advi_49f_floor.tf:230).")
    recs = _execution_record(D)
    print("   {:<44} {:>22} {:>7}".format("log object", "modified (UTC)", "prod"))
    for r in recs:
        print("   {:<44} {:>22} {:>7}".format(
            r["key"][:44], r["modified"][:19], str(r["mode_production"])))
    covering = [r for r in recs if r["covers_date"]]
    if covering:
        r = covering[0]
        print("   COVERING date={}: {}".format(D, r["key"]))
        print("     first line: {}".format(r["first_line"]))
        print("     mode=production {} | bare SSM-style name {}".format(
            r["mode_production"], r["bare_ssm_name"]))
    else:
        print("   NO log covering date={} among the {} most recent.".format(D, len(recs)))
        print("   That is a MEASURED absence over the objects listed, NOT a claim the run")
        print("   did not happen -- the log upload is best-effort in the SSM doc")
        print("   (|| echo WARN), so a successful run CAN leave no log.")
    print("   EVIDENCE-FOR, NOT PROOF, and the distinction is load-bearing:")
    print("     mode=production proves the FLAG, never that the SCHEDULER fired it --")
    print("     a human passing --production writes the identical line.")
    print("     The ad-hoc runs here carry descriptive infixes (chain_adhoc_qa_...,")
    print("     chain_backfill_...), but THAT IS A HUMAN CONVENTION AND NOT A CONTROL.")
    print("     The airtight source is the scheduler's invocation history, outside this read.")

    # ---------- 8b. the dispatch record ----------
    print()
    print("8b. THE DISPATCH ITSELF -- scheduler-side attribution AND its exit status")
    dr = _dispatch_record()
    if "error" in dr:
        print("   UNREADABLE: {}".format(dr["error"]))
        print("   That is a LIMIT, not evidence the dispatch did not happen.")
    else:
        print("   materialised {:,} SSM command(s) over {} page(s), exhausted={}"
              .format(dr["total_commands"], dr["pages"], dr["exhausted"]))
        print("   (the FIRST page can be EMPTY with a NextToken -- reading page one",
              "and stopping")
        print("    yields a clean zero that is a page artifact, not a history)")
        print("   {:<22} {:>9}  {}".format("dispatch (UTC)", "status", "comment"))
        for d in dr["recent"]:
            print("   {:<22} {:>9}  {}".format(d["at_utc"], d["status"], d["comment"][:52]))
        if dr["recent"]:
            top = dr["recent"][0]
            chk("most recent dispatch was SCHEDULER-fired, not manual",
                top["scheduled"], True,
                "src=%s in the dispatcher-written Comment" % SCHEDULED_SRC)
            IN_FLIGHT = ("Pending", "InProgress", "Delayed")
            if top["status"] in IN_FLIGHT:
                # RUNNING IS NOT FAILING. The 08-22 green took 96.8s end to end, so a
                # read taken too soon after 12:45Z can catch the dispatch mid-flight --
                # and a bare status != "Success" test would report a RUNNING chain as a
                # failed one. That is the false-outage direction on the artifact Andrew
                # is waiting for, produced by reading too early rather than by any defect.
                print("   DISPATCH IS STILL {} -- NOT a failure. Re-read after it settles;"
                      .format(top["status"]))
                print("   the 2026-08-22 end-to-end green took 96.8s, so this should be",
                      "brief.")
                print("   NOT scoring this limb: an in-flight run is neither PASS nor FAIL.")
            else:
                chk("most recent dispatch SUCCEEDED", top["status"], "Success",
                    "a Failed dispatch means the chain died; the partition plane cannot show it")
        else:
            print("   NO chain dispatches in the materialised history -- a MEASURED",
                  "absence over")
            print("   {:,} commands, not a claim none occurred.".format(dr["total_commands"]))

    npass = sum(1 for ok, _ in checks if ok)
    print("\n" + "=" * 108)
    print("DENOMINATOR: {}/{} checks PASS over {:,} rows / {:,} accounts at D / {:,} at D-1"
          .format(npass, len(checks), len(twr), len(set_d), len(set_p)))
    for ok, name in checks:
        if not ok:
            print("  FAILED: {}".format(name))
    print("AC7 VERDICT: {}".format(
        "SATISFIED at this partition" if npass == len(checks)
        else "NOT SATISFIED -- see FAILs above"))
    print("SCOPE, UPDATED when section 8b landed -- an earlier version of this line said")
    print("  the scheduler's invocation history was OUTSIDE this read. IT IS NOW INSIDE IT,")
    print("  and leaving the old sentence would have been a status line outliving its body.")
    print("  WHAT IS ESTABLISHED: the dispatcher-written SSM Comment carries the scheduler's")
    print("    own source tag (src=advi.49f.scheduled-floor; a manual dispatch defaults to")
    print("    src=manual), so SCHEDULED-vs-AD-HOC is now attributed from a record written")
    print("    by the dispatcher rather than by the thing being judged -- and the dispatch's")
    print("    EXIT STATUS is visible, which the partition plane cannot show at all.")
    print("  WHAT IS NOT: this still reads ONE partition. An ad-hoc run is NEVER production")
    print("    evidence, and nobody accelerates the run.")
    return 0 if npass == len(checks) else 1


if __name__ == "__main__":
    sys.exit(main())
