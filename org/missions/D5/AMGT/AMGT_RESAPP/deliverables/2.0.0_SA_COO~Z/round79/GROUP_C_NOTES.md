## C1 -- `AMGT-cc-4` -- SERVE FIVE STORED RESEARCH-NOTE SECTIONS

### 1. MEASURED AT THE BASE

Read 2026-10-08 about 09:50Z to 10:25Z on the shared tree, branch `CLOUD`, HEAD `d3a73eda1a` at the first read and
`89d410b94a` at the last (other seats were committing). Store reads were read-only, bucket `opal-data-harvest`.
Nothing is committed; no file under `lib/`, `infra/`, `integrations/` or `portal/` was edited.

**The stored object.** `lib/research/corpus/dossier.py` (2,154 lines, blob `a4548412e32d`, last commit `901be95e86`),
`METHOD_VERSION = "amgt-corpus-dossier/7"`. One JSON document per company under
`amgt/harvest/gold/research_dossier/security_key=<KEY>/as_of=<date>.<hash>.json`; `read_dossier(key)` (line 1480) returns
`{"uri", "content_sha256", "document"}` and raises `LookupError` when a company has no object. `document["fields"]` holds
23 names, the same 23 on 95 of 95 covered companies. A section is one of two shapes (`_resolve_section_field`, line 535):

- a value: `{"value": <text>, "citation": {"report_key", "report_id", "locator", "passage"}}`. `report_key` is the
  address of the report file, `locator` is the zero-based page index for a pdf (`extract.py:351`) and the paragraph
  index for a Word file, `passage` is the first 300 characters of the value (105 of 105 equal).
- an absence: `{"value": null, "absent": <reason>}`.

**Who serves it today** (`lib/research/api/scoped_amgt.py`, blob `afe19b30ce43`, all on `GET /security/<name>/thesis`):

| line | function | what it reads | served under |
|---|---|---|---|
| 4992 | `_read_dossier_document` | the ONE `read_dossier` call of a request; returns `(document, reason)` | (held as `dossier_read`, line 3655) |
| 5013 | `_dossier_fields` | `thesis_pillars`, `management`, `fund_of_record`, `last_stated_position`, `pack_shape` | `dossier_fields` (line 3692) |
| 5080 | `_team_cases` | `cases.base`, `cases.upside`, `cases.downside` | `model.team_cases` (line 3656) |
| 4544 | `read_management` -> `_with_exec_roster_chain` (4488) | the same read, handed to the officer search | `management` (line 3731) |

The deployed function (`opal-amgt-scoped-api`, CodeSha256 `+s6R0/rcpQ6l...`, one read-only invoke for ASML_NA_Equity at
10:20Z) answers with `dossier_fields` holding exactly those five names and no `dossier_sections` key. The five fields
of this cell are served by no route.

**The five fields over the 95 covered names** (`covered_security_keys()`; 95 of 95 documents read, 95 of 95 at method 7,
95 of 95 dated 2026-10-07; a value = a string with one non-blank character):

| field | value | absence with a reason | nothing | length in characters, min / median / max | cited file |
|---|---|---|---|---|---|
| `company_description` | 48 of 95 | 47 | 0 | 426 / 1,533 / 2,726 | 34 pdf, 14 Word |
| `why_we_own` | 18 of 95 | 77 | 0 | 921 / 1,548 / 3,001 | 18 pdf |
| `positives` | 13 of 95 | 82 | 0 | 220 / 982 / 1,126 | 13 pdf |
| `negatives` | 13 of 95 | 82 | 0 | 240 / 855 / 1,128 | 13 pdf |
| `special_items` | 13 of 95 | 82 | 0 | 123 / 576 / 1,224 | 13 pdf |
| all five | 105 of 475 | 370 | 0 | | 91 pdf, 14 Word |

- Every value is a string; 105 of 105 carry a citation with the four keys; 0 carry leading or trailing blanks; 69 of 105
  hold a character outside ASCII (a curly quote, a dash). 20 of the 91 pdf citations have page index 0 (the first page).
- The 370 absences read in two stored forms and no other (0 unmatched):
  `no <NAME> section in class A <label> or class B <label>` (359), and
  `<NAME> heading has no prose following it in the extracted text of class A <date>` (11, all `special_items`). A third
  form the producer can write, `... heading is followed by a table and no prose ...`, is stored 0 times today. A label is
  a date (`2026-03-09`), a period (`2026-Q2`, `2026-H1`, `2026-Q3`) or the word `missing`. `missing` means no report of
  that class was picked OR the picked one carries no period (`_period_label`, line 290); 18 names read `missing` twice.
- Class A is the research pack and class B the earnings update (`dossier.py` docstring, lines 47 and 108).
- **Known cut-off values (CTO ruling msg 31382: served as stored).** Five of the six fall in these fields:
  LLY_US_Equity `negatives`, NU_US_Equity `positives`, NU_US_Equity `negatives`, QXO_US_Equity `negatives`,
  UNH_US_Equity `negatives`. The sixth, SHOP_CN_Equity `management`, is not one of the five.
- **Seen beside it, not in the ruling's list:** 14 of the 105 values do not end at a full stop. Five are the ruled ones.
  Five end a list with no full stop (8306_JP, IMB_LN, SAN_FP, TTE_FP `company_description`; AZN_LN `positives`). Four are
  `why_we_own` values that stop inside a sentence: LLY_US_Equity ("...Lilly should"), UNVGY_US_Equity ("...growth algorithm
  is"), V_US_Equity ("...it should remain a"), WDAY_US_Equity ("...wide margin of safety,"). This cell serves them as
  stored like the others; whether they join the ruled list is the issuer's row to file (section 8).
- Cross-check, not my numbers: AMGT_CORPUS `evidence/r40_ap10d2_leg_v_trim_tails_20261007.txt` prints the same tails for
  the five ruled values ("...guidance ceiling was actually lowered", "...completed digital bank", "...declined slightly",
  "...Sell-side estimates kept", "...billing practices remains").

**Two things found at the base that the first draft tripped on:**

- `lib/research/api/tests/test_dossier_fields.py` ALREADY EXISTS (13 cases, for `scoped_amgt._dossier_fields`). The module
  is therefore named `dossier_sections.py` and its test file `test_dossier_sections.py`, not `dossier_fields`.
- The api tests folder does not pass clean at the base: `1 failed, 828 passed`. The one failure is
  `test_harvest_prefixes.py::test_ii_registry_hash_matches`, present before this cell. AC3 names it.

### 2. THE ACT (worker face text)

The research notes we hold for a covered company carry five sections that no page can show, because nothing serves
them: the company description, why we own it, the positives, the negatives and the special items. Build ONE new pure
module that turns the already-read notes document into the block a page will be served. You do not serve it: another
cell of this round connects your function to the route.

Write `lib/research/api/dossier_sections.py` and `lib/research/api/tests/test_dossier_sections.py`. (A file named
`test_dossier_fields.py` already exists and tests something else. Do not edit it and do not reuse its name.)

The module exports these names:

- `FIELD_ORDER = ("company_description", "why_we_own", "positives", "negatives", "special_items")`
- `HEADINGS`, a dict: `company_description` -> `Company description`; `why_we_own` -> `Why we own it`; `positives` ->
  `Positives`; `negatives` -> `Negatives`; `special_items` -> `Special items`.
- `dossier_sections(document, read_failed=False)`, returning a list of exactly five dicts, one per name of `FIELD_ORDER`,
  in that order. Each dict has exactly these six keys, in this order:
  `field`, `heading`, `status`, `text`, `reason`, `citation`.

`document` is the notes document as stored (a dict with a `fields` dict), or `None` when the company has none.

Rules, applied per field name in `FIELD_ORDER`:

1. **A value.** If `document["fields"][name]` is a dict whose `value` is a string holding at least one character that is
   not whitespace: `status` is `"served"`, `text` is that string, `reason` is `None`, and `citation` is a deep copy of the
   stored `citation` when it is a dict, else `None`.
2. **The text is the stored text, unchanged.** Never strip it, trim it, re-join it, re-word it, shorten it, normalise its
   quotes or dashes, or remove the section name it opens with. A value that stops in the middle of a sentence is served
   exactly as it stops: there is NO special handling for it. The check compares bytes.
3. **Anything else is absent.** The field is missing, is `None`, is not a dict, or its `value` is `None`, an empty or
   blank string, or not a string: `status` is `"absent"`, `text` is `None`, `citation` is `None`, and `reason` is one
   plain sentence chosen by rule 4.
4. **The plain sentence**, from the stored `absent` text. `<H>` is the field's heading from `HEADINGS`. Match the stored
   text against these patterns in this order, with `re.match`, exactly as written:
   - `^no .+ section in class A (.+) or class B (.+)$`, the two groups being `a` and `b`:
     - `a` and `b` both equal `missing`: `No research report we hold for this company has a "<H>" section.`
     - only `b` equals `missing`: `The research pack of <a> has no "<H>" section.`
     - only `a` equals `missing`: `The research update of <b> has no "<H>" section.`
     - neither: `Neither the research pack of <a> nor the research update of <b> has a "<H>" section.`
   - `^.+ heading (has no prose following it|is followed by a table and no prose) in the extracted text of class ([AB]) (.+)$`:
     the report is `the research pack` for class `A` and `the research update` for class `B`, followed by ` of <label>`
     unless the label equals `missing`. Then
     `The "<H>" heading in <report> has no text under it.` for the first wording, and
     `The "<H>" heading in <report> is followed by a table and no text.` for the second.
   - no match, or the stored `absent` is not a string, or the field is missing:
     `This section is not in the research reports we hold for this company.`
   If the sentence you built holds a refused word (rule 7) or a character outside ASCII, use the last sentence instead.
5. **No document.** `document is None` and `read_failed` is false: five absent entries, each with the reason
   `We hold no research notes for this company.` `document is None` and `read_failed` is true, or `document` is not a
   dict: five absent entries, each with `The research notes for this company could not be read just now.` A dict with no
   `fields` dict is treated as having no fields (rule 3, five times).
6. **Only the five.** Every other section of the document is ignored, whatever it holds. The list always has five
   entries. The function never raises on any input and never changes the document it is given.
7. **Plain words.** No sentence the module writes (a heading or a reason) may contain, in any letter case: identity,
   unresolved, security key, crosswalk, dossier, landed, model block, estate, stage, input ledger, bronze. These are
   matched as substrings, so "percentage" would fail on "stage". The stored `text` and the stored `citation` are not
   sentences you write and are passed through as they are, whatever words they hold.
8. **Pure.** The module imports from the Python standard library only (`copy`, `re`). It imports nothing from `lib`, opens
   no file, reads no store and makes no network call. Its source is ASCII.
9. **Bounds.** You do NOT edit `lib/research/api/scoped_amgt.py`, `lib/research/corpus/dossier.py` or
   `lib/research/api/tests/test_dossier_fields.py`. No deploy, no store write, no vendor, SEC or model call.

The test file: cover at least a served value with characters outside ASCII and blanks at both ends (assert equality of
the whole string), each sentence of rule 4, rule 5's two sentences, a section outside the five being ignored, and the
input left unchanged. Build planted documents in the test; it must not read the store.

Report: the five served counts over the covered names that AC2 prints, and anything in the store the rules above did
not foresee (file a surprise row for it and keep working; do not bend a rule to fit).

### 3. THE CRITERIA
- **AC1** `cd "$(git rev-parse --show-toplevel)" && PYTHONPATH="$(pwd)" python "org/missions/D5/AMGT/AMGT_RESAPP/deliverables/2.0.0_SA_COO~Z/round79/checks/r79_cc4.py" --crit AC1 --where local; echo "exit=$?"`
  Expect: on planted documents a value is served byte-equal with its citation, each stored absence form reads as its plain sentence, a missing field and a section outside the five are handled, no sentence holds a refused word, the test file exists and passes; C1-C12 PASS; R79 CC4 AC1 SERVED: YES; and exit=0
- **AC2** `cd "$(git rev-parse --show-toplevel)" && PYTHONPATH="$(pwd)" python "org/missions/D5/AMGT/AMGT_RESAPP/deliverables/2.0.0_SA_COO~Z/round79/checks/r79_cc4.py" --crit AC2 --where local; echo "exit=$?"`
  Expect: the block is produced for 95 of 95 covered names; served equals stored per field at 48, 18, 13, 13 and 13 of 95; 105 of 105 served texts equal the stored text; ASML_NA_Equity and NU_US_Equity equal field by field; C1-C7 PASS; R79 CC4 AC2 SERVED: YES; and exit=0
- **AC3** `cd "$(git rev-parse --show-toplevel)" && PYTHONPATH="$(pwd)" python "org/missions/D5/AMGT/AMGT_RESAPP/deliverables/2.0.0_SA_COO~Z/round79/checks/r79_cc4.py" --crit AC3 --where local; echo "exit=$?"`
  Expect: the api tests folder shows 828 or more passed and no failure other than test_harvest_prefixes.py::test_ii_registry_hash_matches; dossier.py is byte-unchanged against HEAD and is the blob at the cut; scoped_amgt.py carries no uncommitted edit; C1-C3 PASS; R79 CC4 AC3 SERVED: YES; and exit=0

### 4. THE BASE DRY-RUN

The check passes `bash .tools/commit-gate.sh` ("OK: pre-commit gate clean for 1 of 1 file(s)"). At the base, AC1 and AC2
FAIL for the right reason (the module does not exist) and AC3 PASSES (the bound). Literal, HEAD `44fe98b15e`:

```
== BASE AC1 ==
FAIL C1 the module imports and exports dossier_sections ModuleNotFoundError: No module named 'lib.research.api.dossier_sections'
R79 CC4 AC1 SERVED: NO
exit=1
== BASE AC2 ==
FAIL C1 the module imports and exports dossier_sections ModuleNotFoundError: No module named 'lib.research.api.dossier_sections'
R79 CC4 AC2 SERVED: NO
exit=1
== BASE AC3 ==
   1 failed, 828 passed, 297 warnings in 41.42s
PASS C1 the api tests folder passes apart from what already failed at the cut passed 828 (at the cut 828); failed ['lib/research/api/tests/test_harvest_prefixes.py::test_ii_registry_hash_matches']; of them new []; errors []
PASS C2 dossier.py is byte-unchanged against HEAD and is the file at the cut working a4548412e32d; HEAD a4548412e32d; at the cut a4548412e32d; control read ok 68cd5497
PASS C3 scoped_amgt.py carries no uncommitted edit git diff --quiet rc=0
R79 CC4 AC3 SERVED: YES
exit=0
```

Against a stand-in module written from section 2's text alone, in a scratch folder OUTSIDE the repo and placed in memory
under the module's name (no repo file written). AC1 fails on one clause only, the worker's own test file, which the
stand-in does not have; AC2 passes on the real store. Literal (the one long path shortened):

```
== STUB AC1 ==
PASS C1 the module imports and exports dossier_sections lib.research.api.dossier_sections
PASS C2 a planted document builds the five entries in the fixed order, six keys each fields ['company_description', 'why_we_own', 'positives', 'negatives', 'special_items']
PASS C3 a stored value is served with its text byte-equal and its citation as stored why_we_own served 73 bytes, stored 73 bytes
PASS C4 the document handed in is not changed 
PASS C5 a section outside the five is ignored and a field the document lacks is absent with the plain sentence special_items reason 'This section is not in the research reports we hold for this company.'
PASS C6 each stored absence form reads as its plain sentence (12 forms) 
PASS C7 a value that is not text is absent, and a value with no stored citation is served with none 
PASS C8 no document, a failed read and an empty document each give five absent entries with one plain sentence 
PASS C9 no sentence the module writes uses a refused word, and each is ASCII (29 read) 
PASS C10 the module is pure: ASCII source, no store client and no import from lib imports ['copy', 're']; source <scratch>\stub\dossier_fields_stub.py
FAIL C11 the worker's test file exists lib/research/api/tests/test_dossier_sections.py
R79 CC4 AC1 SERVED: NO
exit=1
== STUB AC2 ==
PASS C1 the module imports and exports dossier_sections lib.research.api.dossier_sections
   covered names 95; research notes read 95; not read 0 []
PASS C2 the block is produced for every covered name without raising 95 of 95; raised []; wrong shape []
   company_description  served 48 of 95; stored 48 of 95; at the cut 48
   why_we_own           served 18 of 95; stored 18 of 95; at the cut 18
   positives            served 13 of 95; stored 13 of 95; at the cut 13
   negatives            served 13 of 95; stored 13 of 95; at the cut 13
   special_items        served 13 of 95; stored 13 of 95; at the cut 13
PASS C3 per field the served count equals the stored-value count read from the store now 
PASS C4 per field the stored-value count is the one measured at the cut 
PASS C5 every served text equals the stored text byte for byte, with the stored citation text 105 of 105; citation 105 of 105
   ASML_NA_Equity: company_description 1537 bytes equal; why_we_own 1546 bytes equal; positives 1120 bytes equal; negatives 858 bytes equal; special_items 635 bytes equal
   NU_US_Equity: company_description absent; why_we_own 2721 bytes equal; positives 1126 bytes equal; negatives 874 bytes equal; special_items absent
PASS C6 the two named companies are served as stored, the known cut-off value included 
   absent entries 370; of them the general sentence 0; distinct sentences 154
PASS C7 every absent entry carries a plain reason with no refused word 
R79 CC4 AC2 SERVED: YES
exit=0
```

### 5. `<paths>`

```
lib/research/api/dossier_sections.py
lib/research/api/tests/test_dossier_sections.py
org/missions/D5/AMGT/AMGT_RESAPP/surprise-channel/investigations/INVESTIGATION_v1.md
```

### 6. Risk and class

LOCAL. `worker-light`: one new module of about 80 lines and one test file; no existing product file changes, nothing is
deployed, and no route serves the block until the adapter cell lands. AC2 reads the store (95 listings, about 190 GETs,
read-only).

### 7. Edges

- None before it. After it: the round's adapter cell (the issuer's) imports the module and adds the served key; the
  deploy pair must list that hookup by name (ruling R1). Until both land, FWD outcomes do not move.
- AC2's clause C4 compares the store with the counts of 2026-10-08 (48, 18, 13, 13, 13). If AMGT_CORPUS re-mints the
  notes before the drain, C4 fails for a reason that is not the worker's; C3 (served equals stored now) still decides
  whether the module is right.
- AC3's clause C2 pins `dossier.py` to blob `a4548412e32d`. If AMGT_CORPUS lands a change to that file before the cut,
  re-pin `DOSSIER_BLOB_AT_THE_CUT` in the check.
- AC3's clause C3 only sees an UNCOMMITTED edit of `scoped_amgt.py`. A committed one by the worker is caught by the
  write-surface gate on section 5's paths, not by this check.

### 8. Not measured, and questions for the issuer

**The adapter hookup, exactly.** File `lib/research/api/scoped_amgt.py` (blob `afe19b30ce43`):

1. Beside the sibling imports at lines 127 to 137, add: `from lib.research.api import dossier_sections`
2. In `read_thesis_bundle` (defined at line 3629), inside the `bundle = {` literal, directly after line 3692
   (`"dossier_fields": _dossier_fields(dossier_read),`), add:
   `"dossier_sections": dossier_sections.dossier_sections(dossier_read[0], read_failed=dossier_read[0] is None and str(dossier_read[1] or "").startswith("dossier read failed")),`
3. The value already in hand there is `dossier_read`, set at line 3655 by `_read_dossier_document(resolved_key)`: a tuple
   `(document, reason)`. **No second store read is needed or wanted**: the /thesis path already holds the document, and
   `_team_cases`, `_dossier_fields` and `read_management` take the same tuple.
4. The served key is `dossier_sections`, a list of five, on `GET /api/scoped/amgt/security/<name>/thesis`.
5. `read_failed` is true only for the reason `_read_dossier_document` writes at line 5006 ("dossier read failed: ...").
   A company with no notes (line 5004) and a name that did not resolve (line 4998) both read
   "We hold no research notes for this company."
6. `_plain_no_block_reasons` (line 1142) rewrites any served string under a key ending `reason` that holds one of its
   refused words. The module's sentences hold none (AC1 C9), so that pass leaves the block as built.

**What a deployed check should read, for ASML_NA_Equity** (`/security/ASML_NA_Equity/thesis`): `dossier_sections` is a
list of 5 with `field` in the order `company_description`, `why_we_own`, `positives`, `negatives`, `special_items`; all
five `status` are `served`; `[0].text` is 1,537 bytes in UTF-8 (1,535 characters), opens
`COMPANY DESCRIPTION:What started as a failing joint venture`, and its SHA-256 opens `e5a71e1db8874200`;
`[0].citation.locator` is 2 and `[0].citation.report_key` ends `ASML research pack 5_5_2026.pdf`. The other four are
1,546 / 1,120 / 858 / 635 bytes (SHA-256 opening `0e5720f47c28cca5`, `af7b491315328073`, `506c2ecb7e1d3ecb`,
`b7a8276d40d1c51d`). A second read: NU_US_Equity `negatives` ends `Mexican deposits declined slightly` (874 bytes) and
its `company_description` is absent with `The research update of 2026-Q2 has no "Company description" section.`

**Questions.**
- **The module and key names.** I propose the module `dossier_sections.py` and the key `dossier_sections`, because a test
  file named for `dossier_fields` already exists and `dossier_fields` is already a served key.
- **The citation is passed through as stored**, so `report_key` is a store address and `locator` a zero-based page
  index (a Word file: a paragraph index). Turning that into "page 3 of <file>" is either the page's (DSGN_AMGTV1) or a
  later producer cell's. Rule which; the module does not do it.
- **The stored reason is not served beside the plain one.** The six keys are the ones the brief names. If the page or a
  check wants the stored words too, add a seventh key before the cut, not after.
- **The served text opens with its own section name** ("COMPANY DESCRIPTION:What started ...", with no space after the
  colon on some). That is how it is stored, and it is served so. Whether the page drops the lead is the page's call.
- **Four `why_we_own` values stop inside a sentence and are not in the ruled list of six** (LLY, UNVGY, V, WDAY; section
  1). They are AMGT_CORPUS's values. I filed no row: the channel is outside my write set. It is the issuer's to file.
- **The pre-existing api test failure** (`test_harvest_prefixes.py::test_ii_registry_hash_matches`) is not this cell's. Its
  cause was not read.
- NOT measured: the page. Nothing was rendered, and where each section shows is DSGN_AMGTV1's.
- NOT exercised: that the build script carries the new module. It is inferred from
  `infra/aws/terraform/harvest/build-and-upload-scoped-amgt.sh` line 177 (`SEED_PKG_DIRS` holds `lib/research/api`).
- NOT measured: names outside the 95. The stored pool holds 243 names; the 148 others were not read. By
  `read_dossier`'s contract they have no object and would read "We hold no research notes for this company."
- The `missing` label cannot tell "no report of that class" from "a report with no period"; the sentences in rule 4 are
  worded to be true in both cases.
