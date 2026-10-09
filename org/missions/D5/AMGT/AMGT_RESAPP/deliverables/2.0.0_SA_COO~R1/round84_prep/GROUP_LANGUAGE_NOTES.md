# AMGT_RESAPP round-84 PREP -- the source `language` stamp (row AMGT_RESAPP-D1-W332-S1)

Grounding fork of `2.0.0_SA_COO~R1`, 2026-10-09 ~10:3xZ. READ-ONLY: the five cached 20-F texts in `.scratch/r82_20f/` driven
in-process (no SEC GET, no store read or write, no model call, nothing committed).

## Cause

`lib/research/filings/fetch.py:417` (in `build_source_object`, the EDGAR-by-CIK path the store half runs) stamps
`"language": document.detect_language(text)["language"]` over the WHOLE extracted document. `detect_language`
(`document.py:397`) reads only the first `_LANG_SAMPLE = 40000` chars (`:331`) and, for an ascii-majority sample, counts stopword
hits per language (`_STOPWORDS`, `:342`); the language with the most hits wins when it reaches `_MIN_STOPWORD_HITS = 3`.

In every cached 20-F the first 40,000 chars are the **inline-XBRL fact header**, not prose (tag names, URLs, dates):

| name | head stamp | head stopword hits (top) | what drove it |
|---|---|---|---|
| ASML NA | en | en 108, pt 31 | some cover prose in the head |
| BABA US | **pt** | pt 13, it 4, es 2, **en 0** | `e` x8 (`baba:E-CommerceMember`), `com` x3 (`www.alibabagroup.com` URLs), `o` x2 |
| NU US | en | en 28, pt 9 | -- |
| PBR US | en | max 1 (< 3) | falls to `en` by the minimum-hits rule, not by evidence |
| SAP GY | **es** | es 3, en 2 | `y` x2, `se` x1 (`SAP SE`) |

BABA's head is 1,890 tokens over 175 distinct (top: `baba` 382, `us` 273, `gaap` 273, `...member`); SAP's 2,089 over 128 (`sap`
517, `ifrs` 298, `full` 298). A 0-3 hit vote over XBRL noise decides the stamp; PBR and NU read `en` by luck.

The SAME detector over each name's CUT sections (merged cutter, `document.cut(text, "20-F")`) reads `en` for all 15 cells, with
`en` 1,239-1,811 hits against a runner-up of 92-190 (`pt`, mostly `a`/`as`/`e`).

Two other call sites share the whole-text pattern and are NOT on the store half's path: `battery.py:414` (the battery path) and
`document.py:1510` (the document-layer-local object). Not changed by the repair below; named for the CTO.

## Consumers of the stamped `language`

1. `analyze.py:1419-1433` `_source_language`: the source object's OWN `language` field wins when present; only an absent field
   falls back to `detect_language(excerpt_text)`. So the bad stamp is used as-is.
2. `analyze.py:1439` -> `run_pass_1(..., language=...)` -> `analyze.py:397-403`: a non-`en` language adds `LANGUAGE_RULE_TEMPLATE`,
   asking the model to answer and quote in that language and script. That is why BABA's draft came out Portuguese (0 of 40 served:
   Portuguese quotes cannot be verbatim in an English filing).
3. The analysis carries `language`; `translate.py:128-132` makes a translation model call only when `language != "en"`
   (`:439` refuses without a key for non-`en`). With the bad stamp, an English filing would also be "translated".
4. Served: `lib/research/api/translated_text.py:13-29` and `scoped_amgt.py:5321-5322` serve `text_translated` / `translated` /
   `source_language` from the drafting sentence's `translation` block, so a wrong `source_language` would reach the page.

## Smallest repair

At `fetch.py:417`, stamp from the cut sections the object already builds a few lines up (`excerpt_text`, `:398-400`):
`"language": document.detect_language(excerpt_text)["language"]`. One line; `excerpt_text` is non-empty on every RESOLVED path
(an empty `item_keys` returns UNRESOLVED earlier, `:385-397`). Measured offline with that substitution: ASML, BABA, NU, PBR, SAP
all read `en` (en 1,453-1,625 hits on the excerpt vs pt 119-190), and the planted Portuguese filing reads `pt` (pt 2,580, es 885).
A genuinely non-English 20-F stays non-English because its cut sections are non-English prose.

**Negative control:** a planted filing whose 40,000+-char header is stopword-free XBRL noise and whose Item 3.D / 4.B / 5 sections
are Portuguese prose must be stamped `pt`. A repair that hard-codes `en` fails it; the base fails it too (the head read sees only
noise and falls to `en`).

`fetch.py` is a **site-Z producer path**: its merge is a site-Z deploy under `1.0.0_SA_CTO~Z`'s half. Not measured here: the
`language` of the PRIOR (parser 1.0.0) stored rows that BABA was rolled back to.

## Check

`round84_prep/checks/r84_language.py --crit AC1 [--cache DIR]` drives the real `fetch.build_source_object` offline
(`latest_filing`, `http_get`, `html_to_text` and `time.sleep` replaced in-process; the cached text is the document) and grades:
- L1: the five cached English filings are stamped `en`;
- L2: the planted Portuguese filing is stamped `pt`.

Dry-run at the base (box/dell1, py3.12 and py3.14):
```
PASS L1 ASML_NA_Equity   status RESOLVED language en (excerpt 145654 chars)
FAIL L1 BABA_US_Equity   status RESOLVED language pt (excerpt 210108 chars)
PASS L1 NU_US_Equity     status RESOLVED language en (excerpt 210108 chars)
PASS L1 PBR_US_Equity    status RESOLVED language en (excerpt 173378 chars)
FAIL L1 SAP_GY_Equity    status RESOLVED language es (excerpt 173860 chars)
   L1 denominator: 3 of 5 cached English filings stamped en
FAIL L2 negative control: a planted Portuguese filing behind an XBRL-noise header is stamped en (...; want pt)
R84 LANGUAGE AC1: NO
```
exit 1. ruff py39 clean (commit-gate OK).
