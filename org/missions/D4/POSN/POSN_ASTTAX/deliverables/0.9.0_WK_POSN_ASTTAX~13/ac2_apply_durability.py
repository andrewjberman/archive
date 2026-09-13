#!/usr/bin/env python3
"""
POSN_ASTTAX.TO-T4-1 / cell AT3-s-4 / T4-AC2 -- APPLY the durability change.

THE SHAPE CHOSEN, IN ONE SENTENCE: the seeder stops doing an unconditional full-item put
and instead does a PRE-READ + NON-DESTRUCTIVE MERGE in which a module PLACEHOLDER can never
overwrite a real value the table already serves, and a module value that genuinely DISAGREES
with a served value REFUSES THE WHOLE RUN instead of reverting it silently.

WHY THIS SHAPE AND NOT THE OTHER TWO:
  - "populate the map" alone fixes SIX TICKERS and leaves 37 of 136 tickers still writing
    management_style="unknown" over whatever the table serves; it is a fix for this round's
    rows, not for the property. It is applied here as LIMB A anyway, because the module is
    the seeder's own source of truth and leaving it wrong is leaving a second defect.
  - "make the put conditional" cannot be done where the write happens: DynamoDB's
    BatchWriteItem -- which is what boto3's table.batch_writer() issues -- accepts NO
    ConditionExpression at all. Making every put conditional means abandoning batching for
    136 individual calls, and a condition still needs the expected value, which is the
    pre-read this shape does once.

WHAT THIS DOES NOT FIX (stated, not implied):
  1. A module value that is REAL BUT STALE still wins on an explicit --accept-module-truth
     run. The guard converts a silent revert into a REFUSAL plus a named list; it does not
     decide who is right. In particular: if AT3-s-6 retags asset_class in DYNAMODB ONLY, the
     module still says 'hedge' for all six and a re-seed will report the conflict and refuse
     -- but an operator who passes --accept-module-truth reverts the retag. THE RETAG MUST
     ALSO LAND IN ETF_CLASSIFICATIONS. This cell does not retag and must not.
  2. The two OTHER copies of the module are NOT edited -- they are outside this order's
     <paths> write grant. They are also not on this hazard's path: the seeder imports from
     _shared ONLY (sys.path.insert(.../"_shared")), so the revert vector runs through one
     copy. The other two remain third copies that can drift; that is a separate finding.
  3. It is a read-modify-write, not an atomic one. A writer that changes a row between the
     pre-read and the batch flush is still clobbered. BatchWriteItem cannot express the
     condition that would close this.
  4. It adds no trigger, no schedule and no monitor. The seeder stays manual-only.
  5. It protects the FIELDS THE SEEDER WRITES. A curated attribute the module does not emit
     at all is carried forward untouched, but nothing here audits attributes it never sees.

IDEMPOTENT: re-running after a successful apply reports ALREADY-APPLIED and changes nothing.
"""
import hashlib
import os
import sys

REPO_FILES = {
    "seeder": "infra/aws/lambda/v2_portal/yang_pipeline/seed-etf-classifications.py",
    "shared": "infra/aws/lambda/v2_portal/_shared/etf_classification.py",
}

# The exact bytes this applier expects to replace. If the world is not what the order said,
# the applier REFUSES rather than patching something it did not read.
SEEDER_TAIL_MARKER = "def seed_table("
SEEDER_TAIL_SHA256_EXPECTED = "b964763e265a008554f6d6ed029aa7f3743a8a5b93d5cd5e47b48d717d552f5c"

APPLIED_MARKER = "A PLACEHOLDER MUST NEVER OVERWRITE A SERVED VALUE"

SHARED_ANCHOR = "    'UVXY': 'passive', 'VXX': 'passive', 'VIXY': 'passive',\n"

# LIMB A. Values are NOT invented here: each is the determination AT2-s-5 made, with its
# basis, in deliverables/0.9.0_WK_POSN_ASTTAX~3/ac3_set_management_style.py, and each was
# read back from the live table by a second instrument in that order's S5-AC4.
SHARED_INSERT = """
    # Passive - Commodity and precious-metal trusts. ADDED by POSN_ASTTAX.TO-T4-1 (cell
    # AT3-s-4) because their ABSENCE here is what made a re-seed write management_style
    # "unknown" over the values AT2-s-5 set. The values are AT2-s-5's determinations, not
    # new ones: DBC/GSG track rules-based commodity indices, GLD/IAU/SLV are grantor trusts
    # holding bullion with no manager discretion, and USO tracks a published benchmark
    # futures contract -- all index/beta tracking under this field's own definition at
    # :298. The counter-example that proves the field discriminates is PDBC below, an
    # actively managed commodity fund, marked 'active'.
    'DBC': 'passive', 'GLD': 'passive', 'GSG': 'passive',
    'IAU': 'passive', 'SLV': 'passive', 'USO': 'passive',
"""

SIX = ["DBC", "GLD", "GSG", "IAU", "SLV", "USO"]


SEEDER_NEW_TAIL = '''TABLE_NAME = "etf-classifications"

# The attributes this script derives from the canonical module.
SEED_FIELDS = ("asset_class", "sub_asset_class", "management_style", "sector", "name")

# Written by this script on every item; never treated as curated content.
PROVENANCE_FIELDS = ("last_updated", "updated_by")


def is_placeholder(field, value, ticker):
    """True when `value` carries NO classification information for `field`.

    A PLACEHOLDER MUST NEVER OVERWRITE A SERVED VALUE. The module returns a placeholder for
    any ticker it does not carry -- "unknown" for asset_class/management_style, "" for
    sub_asset_class/sector, and the ticker itself for name -- and the previous version of
    this script wrote those placeholders as part of an unconditional full-item put. Measured
    2026-09-11 on the module at HEAD: 37 of 136 tickers resolve management_style to
    "unknown" and 16 of 136 resolve sub_asset_class to "". Every one of those was a revert
    waiting to happen over whatever the table served.
    """
    if value is None:
        return True
    text = str(value).strip()
    if text == "" or text.lower() == "unknown":
        return True
    if field == "name" and text == ticker:
        return True
    return False


def module_values(ticker):
    """The classification this module asserts for `ticker`, placeholders included."""
    return {
        "asset_class": ETF_CLASSIFICATIONS.get(ticker, "unknown"),
        "sub_asset_class": ETF_SUB_ASSET_CLASS.get(ticker, ""),
        "management_style": ETF_MANAGEMENT_STYLE.get(ticker, "unknown"),
        "sector": ETF_SECTOR_MAPPING.get(ticker, ""),
        "name": ETF_NAME_OVERRIDES.get(ticker, ticker),
    }


def merge_item(ticker, existing, timestamp):
    """Build the item to write. Returns (item, preserved_fields, conflicts).

    THE RULE: the module wins where it knows something; the TABLE wins where the module only
    has a placeholder; and where BOTH know something and they DISAGREE, nothing is decided
    here -- the disagreement is returned as a conflict for the caller to refuse on.
    """
    mod = module_values(ticker)
    existing = existing or {}
    item = {"ticker": ticker}
    preserved = []
    conflicts = []

    for field in SEED_FIELDS:
        mod_value = mod[field]
        live_value = existing.get(field)
        mod_blank = is_placeholder(field, mod_value, ticker)
        live_blank = is_placeholder(field, live_value, ticker)
        if mod_blank and not live_blank:
            item[field] = live_value
            preserved.append(field)
            continue
        if not mod_blank and not live_blank and str(mod_value) != str(live_value):
            conflicts.append((ticker, field, live_value, mod_value))
        item[field] = mod_value

    # Carry forward any attribute a curator added that this script does not derive.
    for field, live_value in existing.items():
        if field == "ticker" or field in item or field in PROVENANCE_FIELDS:
            continue
        item[field] = live_value
        preserved.append(field)

    item["last_updated"] = timestamp
    item["updated_by"] = "seed-script"

    # DROP EMPTY VALUES, NOT JUST None. MEASURED 2026-09-11 against this very table with a
    # conditional put that could not land: PutItem returns
    #   ValidationException ... A value specified for a secondary index key is not
    #   supported. The AttributeValue for a key attribute cannot contain an empty string
    #   value. IndexName: sub-asset-class-index, IndexKey: sub_asset_class
    # while the identical request carrying a NON-empty sub_asset_class returns
    # ConditionalCheckFailedException -- so the empty string, not the request shape, is what
    # the table rejects. An ABSENT attribute is valid; the item simply does not appear in
    # that index, which is the correct outcome for a security nothing has classified. The
    # consumer reads these through registry_field(), where "" and absent are both falsy and
    # collapse to the same default, so dropping them changes no served value.
    return ({k: v for k, v in item.items() if v is not None and v != ""},
            preserved, conflicts)


def item_differs(item, existing):
    """Whether the merged item would change anything a consumer can read."""
    for key in set(item) | set(existing):
        if key in PROVENANCE_FIELDS:
            continue
        if str(item.get(key, "")) != str(existing.get(key, "")):
            return True
    return False


def read_existing(table):
    """Every row currently in the table, paginated to exhaustion.

    A scan returns ONE PAGE plus LastEvaluatedKey; treating the first page as the table is
    how a merge silently degrades into an overwrite for everything past the page boundary.
    """
    items = {}
    kwargs = {}
    pages = 0
    while True:
        resp = table.scan(**kwargs)
        pages += 1
        for row in resp.get("Items", []):
            key = row.get("ticker")
            if key is not None:
                items[str(key)] = dict(row)
        last = resp.get("LastEvaluatedKey")
        if not last:
            break
        kwargs["ExclusiveStartKey"] = last
    print("PRE-READ: %d existing row(s) over %d scan page(s) -- the merge baseline."
          % (len(items), pages))
    return items


def seed_table(region="us-east-1", dry_run=False, accept_module_truth=False,
               force_overwrite=False):
    """Sync DynamoDB from the canonical module WITHOUT reverting what it does not know."""

    dynamodb = boto3.resource("dynamodb", region_name=region)
    table = dynamodb.Table(TABLE_NAME)

    timestamp = datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')

    all_tickers = set()
    all_tickers.update(ETF_CLASSIFICATIONS.keys())
    all_tickers.update(ETF_MANAGEMENT_STYLE.keys())
    all_tickers.update(ETF_SUB_ASSET_CLASS.keys())
    all_tickers.update(ETF_SECTOR_MAPPING.keys())

    print("Found %d unique ETF tickers" % len(all_tickers))
    print("Timestamp: %s" % timestamp)

    if dry_run:
        print("")
        print("[DRY RUN MODE] - No changes will be made")
        print("")

    if force_overwrite:
        print("")
        print("WARN: --force-overwrite -- the pre-read is SKIPPED and every item is written")
        print("WARN: whole from the module. This RE-ARMS the revert the merge exists to")
        print("WARN: prevent. Every curated value the module does not carry will be lost.")
        existing = {}
    else:
        try:
            existing = read_existing(table)
        except Exception as exc:
            print("")
            print("ERROR: could not read the existing table: %s: %s"
                  % (type(exc).__name__, exc))
            print("ERROR: FAILING CLOSED, nothing written. Without the current rows this")
            print("ERROR: script cannot tell a curated value from a placeholder, and a")
            print("ERROR: full-item put would revert every curated row in the table.")
            return 2

    items_to_write = []
    preserved_report = []
    conflicts = []
    unchanged = 0

    for ticker in sorted(all_tickers):
        live = existing.get(ticker)
        item, preserved, ticker_conflicts = merge_item(ticker, live, timestamp)
        conflicts.extend(ticker_conflicts)
        if preserved:
            preserved_report.append((ticker, preserved))
        if live is not None and not item_differs(item, live):
            unchanged += 1
            continue
        items_to_write.append(item)

    print("")
    print("MERGE SUMMARY")
    print("  tickers in the module union   : %d" % len(all_tickers))
    print("  rows read from the table      : %d" % len(existing))
    print("  rows whose values PRESERVED   : %d of %d ticker(s)"
          % (len(preserved_report), len(all_tickers)))
    print("  rows already correct (skipped): %d of %d" % (unchanged, len(all_tickers)))
    print("  rows to write                 : %d of %d" % (len(items_to_write), len(all_tickers)))

    if preserved_report:
        print("")
        print("PRESERVED -- the module had no value and the table did; the table's value stands:")
        for ticker, fields in preserved_report:
            print("  %-8s %s" % (ticker, ", ".join(sorted(fields))))

    if conflicts:
        print("")
        print("CONFLICT -- the module and the table BOTH carry a real value and they differ:")
        for ticker, field, live_value, mod_value in conflicts:
            print("  %-8s %-18s table=%-24s module=%s"
                  % (ticker, field, repr(live_value), repr(mod_value)))
        if not accept_module_truth:
            print("")
            print("BLOCKED: %d field(s) on %d ticker(s) would be overwritten with a DIFFERENT"
                  % (len(conflicts), len(set(c[0] for c in conflicts))))
            print("BLOCKED: value than the table serves today. NOTHING WAS WRITTEN.")
            print("BLOCKED: A re-seed must not silently revert a value a person or another")
            print("BLOCKED: job curated. If the MODULE is right, re-run with")
            print("BLOCKED: --accept-module-truth. If the TABLE is right, fix the module first.")
            return 3
        print("")
        print("WARN: --accept-module-truth -- the module value above WILL overwrite the")
        print("WARN: table's on every conflicting field listed.")

    print("")
    print("Writing %d item(s) to DynamoDB..." % len(items_to_write))

    with table.batch_writer() as batch:
        for i, item in enumerate(items_to_write):
            if not dry_run:
                batch.put_item(Item=item)

            if (i + 1) % 50 == 0:
                status = "[DRY RUN]" if dry_run else "[WRITTEN]"
                print("  %s %d/%d" % (status, i + 1, len(items_to_write)))

    print("")
    print("OK: Seeding complete!")
    print("  Items written   : %d" % len(items_to_write))
    print("  Items untouched : %d" % unchanged)
    print("  Table           : %s" % TABLE_NAME)
    print("  Region          : %s" % region)

    print("")
    print("Sample items:")
    for item in items_to_write[:5]:
        print("  %s: %s / %s" % (item["ticker"], item.get("asset_class", "<absent>"),
                                 item.get("sub_asset_class", "<absent>")))
    return 0


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Seed etf-classifications DynamoDB table (non-destructive merge)"
    )
    parser.add_argument(
        "--region",
        default="us-east-1",
        help="AWS region (default: us-east-1)"
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Show what would be written without actually writing"
    )
    parser.add_argument(
        "--accept-module-truth",
        action="store_true",
        help="Proceed even where the module disagrees with a value the table already "
             "serves, overwriting the table. Without this flag such a run REFUSES."
    )
    parser.add_argument(
        "--force-overwrite",
        action="store_true",
        help="Skip the pre-read and write every item whole from the module. Re-arms the "
             "revert; use only when the module is known to be the only source."
    )

    args = parser.parse_args()
    sys.exit(seed_table(region=args.region, dry_run=args.dry_run,
                        accept_module_truth=args.accept_module_truth,
                        force_overwrite=args.force_overwrite))
'''


def read_bytes(path):
    with open(path, "rb") as fh:
        return fh.read()


def write_text(path, text):
    """Write LF-terminated UTF-8. Python text mode CRLF-ifies repo files on this device."""
    with open(path, "wb") as fh:
        fh.write(text.encode("utf-8"))


def apply_limb_a(path):
    src = read_bytes(path).decode("utf-8")
    if "'DBC': 'passive'" in src:
        return "ALREADY-APPLIED", src
    if src.count(SHARED_ANCHOR) != 1:
        return "REFUSED: anchor not unique (%d occurrence(s))" % src.count(SHARED_ANCHOR), src
    new = src.replace(SHARED_ANCHOR, SHARED_ANCHOR + SHARED_INSERT, 1)
    write_text(path, new)
    return "APPLIED", new


def apply_limb_b(path):
    src = read_bytes(path).decode("utf-8")
    if APPLIED_MARKER in src:
        return "ALREADY-APPLIED", src
    if SEEDER_TAIL_MARKER not in src:
        return "REFUSED: marker %r absent" % SEEDER_TAIL_MARKER, src
    idx = src.index(SEEDER_TAIL_MARKER)
    head, tail = src[:idx], src[idx:]
    got = hashlib.sha256(tail.encode("utf-8")).hexdigest()
    if got != SEEDER_TAIL_SHA256_EXPECTED:
        return ("REFUSED: the region to replace is not the bytes this applier read.\n"
                "         expected sha256 %s\n         got      sha256 %s"
                % (SEEDER_TAIL_SHA256_EXPECTED, got)), src
    # `argparse` is already imported at module top; the new tail uses it in __main__.
    new = head + SEEDER_NEW_TAIL
    write_text(path, new)
    return "APPLIED", new


def apply_limb_b2(path):
    """Drop the seeder's unused `import json`.

    NOT a tidy-up and not scope creep: Rule 14's commit gate runs ruff and REFUSES the file,
    so without this the durability change cannot be committed at all. It is provably unused
    -- ruff F401, and `json` appears nowhere in the module at HEAD either. Measured on the
    HEAD bytes for the record: the original file fails ruff with FOUR errors (this F401 plus
    three F541 f-strings-without-placeholders at :80, :82, :86). The three F541s are gone
    because the rewritten tail replaced those lines; this one survived because it sits in
    the import block the rewrite does not touch.
    """
    src = read_bytes(path).decode("utf-8")
    if "\nimport json\n" not in src:
        return "ALREADY-APPLIED"
    if "json." in src or "json(" in src:
        return "REFUSED: `json` is referenced somewhere; not removing the import"
    write_text(path, src.replace("\nimport json\n", "\n", 1))
    return "APPLIED"


def verify(path_seeder, path_shared):
    """Re-read from disk and check the properties, rather than trusting the writer."""
    import ast

    ok = True
    shared = read_bytes(path_shared).decode("utf-8")
    tree = ast.parse(shared)
    mgmt = None
    for node in tree.body:
        targets = node.targets if isinstance(node, ast.Assign) else (
            [node.target] if isinstance(node, ast.AnnAssign) else [])
        for tgt in targets:
            if isinstance(tgt, ast.Name) and tgt.id == "ETF_MANAGEMENT_STYLE":
                mgmt = ast.literal_eval(node.value)
    print("")
    print("VERIFY LIMB A -- re-parsed from disk, not from the writer's return value:")
    if mgmt is None:
        print("  FAIL: ETF_MANAGEMENT_STYLE not parseable after the edit")
        return False
    print("  map size: %d key(s)" % len(mgmt))
    for t in SIX:
        state = ("PRESENT=%s" % mgmt[t]) if t in mgmt else "ABSENT"
        print("  %-5s %s" % (t, state))
        ok = ok and t in mgmt and mgmt[t] == "passive"
    print("  six present with value 'passive': %d of %d"
          % (sum(1 for t in SIX if mgmt.get(t) == "passive"), len(SIX)))
    # the untouched neighbour proves the edit was an INSERT, not a rewrite
    print("  neighbour control VIXY still %s" % mgmt.get("VIXY", "<LOST>"))

    seeder = read_bytes(path_seeder).decode("utf-8")
    print("")
    print("VERIFY LIMB B -- re-read from disk:")
    compiled = True
    try:
        ast.parse(seeder)
    except SyntaxError as exc:
        compiled = False
        print("  FAIL: the rewritten seeder does not parse: %s" % exc)
    print("  parses            : %s" % ("yes" if compiled else "NO"))
    checks = [
        ("pre-read present", "def read_existing(" in seeder),
        ("merge present", "def merge_item(" in seeder),
        ("placeholder rule", APPLIED_MARKER in seeder),
        ("fails closed on read error", "FAILING CLOSED" in seeder),
        ("refuses on conflict", "BLOCKED:" in seeder),
        ("drops empty GSI key values", 'v != ""' in seeder),
        ("no unconditional whole-item put left",
         seeder.count("batch.put_item(Item=item)") == 1 and "merge_item(" in seeder),
    ]
    for label, passed in checks:
        print("  %-34s %s" % (label, "yes" if passed else "NO"))
        ok = ok and passed
    ok = ok and compiled
    return ok


def main():
    root = os.getcwd()
    print("T4-AC2 -- APPLY THE DURABILITY CHANGE")
    print("=" * 100)
    print("SHAPE: pre-read + non-destructive merge in the SEEDER (limb B), plus populating the")
    print("       six commodity tickers in the canonical map the seeder reads (limb A).")
    print("WHY  : a placeholder is the thing that did the reverting, so the fix is to make a")
    print("       placeholder unable to win -- not to chase the six values that exposed it.")
    print("=" * 100)

    for label, rel in REPO_FILES.items():
        path = os.path.join(root, rel)
        if not os.path.exists(path):
            print("BLOCKED: %s missing at %s" % (label, rel))
            return 1

    print("")
    print("LIMB A -- populate ETF_MANAGEMENT_STYLE in the copy the seeder imports")
    status_a, _ = apply_limb_a(os.path.join(root, REPO_FILES["shared"]))
    print("  %s  <- %s" % (status_a, REPO_FILES["shared"]))

    print("")
    print("LIMB B -- replace the unconditional full-item put with a merge")
    status_b, _ = apply_limb_b(os.path.join(root, REPO_FILES["seeder"]))
    print("  %s  <- %s" % (status_b, REPO_FILES["seeder"]))

    print("")
    print("LIMB B2 -- drop the inherited unused import that Rule 14's ruff gate refuses on")
    status_b2 = apply_limb_b2(os.path.join(root, REPO_FILES["seeder"]))
    print("  %s  <- %s (import json)" % (status_b2, REPO_FILES["seeder"]))

    if (status_a.startswith("REFUSED") or status_b.startswith("REFUSED")
            or status_b2.startswith("REFUSED")):
        print("")
        print("BLOCKED: nothing further attempted.")
        return 1

    ok = verify(os.path.join(root, REPO_FILES["seeder"]),
                os.path.join(root, REPO_FILES["shared"]))

    print("")
    print("=" * 100)
    print("PER-COPY REACH -- against the 3 defining copies T4-AC1 enumerated:")
    print("  1/3 _shared/etf_classification.py        EDITED (limb A). In grant, and the ONLY")
    print("      copy the seeder imports: seed-etf-classifications.py does")
    print("      sys.path.insert(0, Path(__file__).parent.parent / '_shared') before importing,")
    print("      so this copy alone is on the revert path.")
    print("  2/3 partners/.../etf_classification.py   LEFT ALONE -- outside this order's <paths>")
    print("      write grant. Not on the seeder's import path.")
    print("  3/3 yang-generate-etf-returns/etf_classification.py  LEFT ALONE -- same reason.")
    print("  The two untouched copies still lack the six; that drift is stated, not fixed.")
    print("")
    print("WHAT THIS DOES NOT FIX: see this file's module docstring, items 1-5. The headline:")
    print("  a REAL-but-STALE module value still wins under --accept-module-truth, so the")
    print("  AT3-s-6 retag must land in ETF_CLASSIFICATIONS and not in DynamoDB alone.")
    print("=" * 100)
    print("")
    print("RESULT: %s" % ("OK: durability change applied and verified from disk"
                          if ok else "ERROR: verification failed"))
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
