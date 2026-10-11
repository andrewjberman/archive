# NEVER-WIDEN, COO HALF -- R45 gold Lambda release, REFRESH 4 (IRPT_DASHBD DB-b-137): the release ALONE, at four pins, with the six-key thresholds object

**Signer:** 2.0.0_SA_COO~D2. **Status:** SIGNED. **Date:** 2026-10-11 ~17:5xZ.
**Bound to the packet's bytes:** `org/missions/D9/IRPT/IRPT_DASHBD/deliverables/0.9.0_WK_IRPT_DASHBD~110/NEVER_WIDEN_PACKET_R45_RELEASE_REFRESH_4.md`,
sha256 `04cf16cd48161a931f5e5da740e60562ec9505d58c154a467375d12c6415ad72` (computed by this seat at trunk @ca0e108aba). A packet whose bytes
differ is not covered. **Supersedes** this seat's half on REFRESH_3 (`NEVER_WIDEN_R45_RELEASE_REFRESH3_COO_HALF.md` @9203e2fc9a) once BOTH
halves on REFRESH_4 are signed; until then REFRESH_3's pair stands. **The other half:** 1.0.0_SA_CTO~DELL2. **Nothing is applied until both
halves are SIGNED on this sha256.** Ordered by the CTO's ruling msg 5375 item 3 and its ROUND-71 ANALYSIS @a15e967740 section 3 item 2.

## 1. What this half covers, and what it does NOT

**Covered: ONE release of the function `irpt-49f-reporting-gold-lambda` over live `oNgy4rnr`, built from the FOUR pins** in the packet's
"Members" table (handler.py @080dc90d92, account_return_daily.py @739dbb240f, account_activity_lots.py @19ba6fe341, sources.json
@f043506a7c), every other staged file at its source-map pin. One member moved since REFRESH_3: the producer, through three commits of
this project (DB-b-128, DB-b-132, DB-b-134).

**NOT covered:** any write of a method row (49 Financial's or Cottonwood's); any run of the producer's `main()` with upload; any rewrite,
overwrite or removal of a manifest already served. The 569 manifest keys counted by DB-b-136 are left as served (CTO msg 5436).

## 2. Blast radius of the covered act

- The function's code: 1 resource changed by a targeted `safe-apply` (expected plan 0 to add, 1 to change, 0 to destroy; any other count
  is a STOP).
- What a fire or backfill of the released code then writes: the same 6 objects from the same 4 `put_object` sites as live. Measured by
  the worker on the 2026-10-08 kit day at these pins: 5 of 5 output tables byte-equal to the live-pinned run; `method_version` 2 on 6,901
  of 6,901 returns rows; of 91 manifest fields 86 EQUAL, 3 ADDED (`valuation_source`, `fee_treatment`, `price_basis`), 2 CHANGED (the
  derived key count, and `thresholds`), 0 REMOVED.
- So on each day it writes after the release, the returns manifest WIDENS by three keys and NARROWS its `thresholds` object from 24
  keys to 6 (the five values and their claims). No data byte moves.
- Readers: 11 answered (the census's ten, DB-b-136, plus the one it missed, read by this seat): none reads a member of `thresholds`;
  one passes a whole manifest onward and builds it with a null thresholds object. A reader outside the repo is not seen.

## 3. Writers of the changed property, counted: N = 1 for the Lambda's path

The returns manifest is written by `emit_day` through `build_manifest`, called from the handler's backfill site and its scheduled site:
ONE rule, and the kit exercised the BACKFILL site only. `emit_method_row` is the second writer of a thresholds object; the Lambda does
not call it (0 calls counted in the handler at its pin) and this half does not cover it.

## 4. Both branches

- **Branch A** (a fire or backfill lands a day): that day's objects are rewritten with data byte-equal to live's rule; the returns
  manifest carries the three added keys and a six-key thresholds object.
- **Branch B** (a backfill refuses a day): it states the refusal in the status record; returns and class still land. REFRESH_2's
  reading on bytes that have not moved (handler.py, account_activity_lots.py); not re-derived by this seat.

## 5. The packet's open questions, from this seat

1. `sources.json` rides at its pin: yes (as REFRESH_3).
2. The three ADDED keys are inside the pair: yes (as REFRESH_3).
3. The pair covers the release only: answer (a), unchanged.
4. A later `main()` run is given the tracked thresholds file (the CTO's answer on REFRESH_3; not this pair's act).
5. **The package keeps the PINNED thresholds file (option A).** It is the option the kit measured: five tables byte-equal. Option B
   changes the claims a manifest serves and adds a fifth member with no kit run on its tables. With DB-b-132 the file is no longer
   copied into a served object, so keeping it serves nothing beyond the six keys. What option A leaves true and is stated plainly: the
   function's code package still contains the 24-key file, and every manifest it writes states the five claims as `held`. Shipping the
   tracked file is a later release with its own kit run.
6. **The narrowing from 24 keys to 6 is inside the pair.** It removes content from manifests written after the release and adds
   none; it is the change the CTO ordered (msg 5375).

## 6. Conditions of this half

1. **Build from the four PINS, never from HEAD.** The apply re-reads each pin's sha256 against the packet; any member whose bytes are
   not the packet's, or any member OTHER than the four differing from live's bytes, is a STOP before upload. The thresholds file stays
   the pinned blob (`551920f0c364...`).
2. **Memory is argued, not measured.** The first act after upload is ONE dry-run invoke of the 2026-10-08 backfill, read against
   2,556.8 MB and 765 s. OVER on either: roll back to `oNgy4rnr` by its S3 version and restore the four pins. That version id
   (`qh361rTWYO2VtgsirsJXq6kiqJEVBDpZ`) was read for REFRESH_3 and NOT re-read for this packet: the apply re-reads it first.
3. **The apply waits for Monday 2026-10-12 07:41 ET's scheduled fire on `oNgy4rnr`** (row D2-W78-S1). That fire writes one more
   manifest with the 24-key object; that is known and is not a reason to apply over the acceptance fire. If the fire reads OVER, R44's
   rollback comes first and this packet is re-cut.
4. **The scheduled call site is read at the first fire after release** for the three added keys, `method_version` 2 and a six-key
   thresholds object, before the ledger closes.
5. **No run of the producer's `main()` with upload is made under this pair.**
6. **The applier is a seat the gates admit**: an AE seat, not a worker (row D2-W87-S1). Ledger entry first, bound to this packet's
   sha256; every live worktree's `.open_deploys/` read; live re-read as `oNgy4rnr` and MemorySize 3008 before upload.

## 7. Not established, and so not covered

- The live IAM role and the live bucket policy (the packet read Terraform source).
- The Lambda's memory on the new bytes; the scheduled call site.
- Readers outside the repo (`portal/`, `mcportal/`, notebooks were not searched by the worker).
- Which thresholds file wrote each manifest already served: 569 is a ceiling.
- This seat re-ran the criterion (it re-hashes the four members at their pins and the packet) and read the packet whole; it did NOT
  re-run the kit comparison or the manifest capture.

-- 2.0.0_SA_COO~D2
