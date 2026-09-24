# DOSSIER_INTERFACE -- `research-dossier`'s field list against `ThesisBundle`

**CRPS-d-3, `0.9.0_WK_AMGT_CORPUS~1`, 2026-09-24.** This is what `AMGT_RESAPP`'s round cuts the render adapter
against (ISSUER NOTES: "the issuer delivers it to `2.0.0_SA_COO~Z` at the drain as an interface publication").
It is a document, not code: it names the INTERSECTION between `lib/research/corpus/dossier.py`'s composed
fields and the portal's `ThesisBundle` type, and says "no slot today" for every dossier field the portal does
not yet carry, rather than mapping one onto the other by force.

**READ CAVEAT, surprise row `AMGT_CORPUS-Z-W1-S3`:** `portal/src/pages/SecurityAnalysis/types.ts` is this
order's READ-ONLY reference for `ThesisBundle`'s shape, but this worktree cannot read it -- `.gitmodules` is a
tracked, genuinely EMPTY blob at HEAD (no submodule URL recorded for `portal` at all; confirmed by
`git rev-parse HEAD:.gitmodules` returning git's well-known empty-blob hash and `git cat-file -s` on it
returning `0`), and `portal/` is an empty directory with no cached submodule objects anywhere in the shared
git-common-dir. **The `ThesisBundle` column below is built entirely from this task order's OWN inlined
quotation** of the file (section 1, verbatim: `portal/src/pages/SecurityAnalysis/types.ts:955` --
`drafted_sections` ids `company_description`, `investment_thesis`, `risks`, `ceo_bio`, `recommendation` with
`generated: true|false` per sentence; `management`; `model_cases`; `model_status`/`fiscal_year_figures`;
`posture`) -- not from an independent live read. `3.0.0_SA_CVO~X` should re-verify this sheet against the file
directly once the submodule is reachable.

## THE SIDE-BY-SIDE

| dossier field (`lib/research/corpus/dossier.py`, `fields{}`) | `ThesisBundle` slot | note |
|---|---|---|
| `recommendation` | `drafted_sections.recommendation` | TRUE INTERSECTION. Dossier's value is narrower by design (<=160 chars, the lead's own line/inline remainder, not a drafted multi-sentence block) -- an adapter reads it as ungenerated (`generated: false`) source text, not a drafted sentence. |
| `company_description` | `drafted_sections.company_description` | TRUE INTERSECTION. Dossier's value is the full cited block. |
| `investment_thesis_summary` | `drafted_sections.investment_thesis` | TRUE INTERSECTION by content, different NAME (this cell's field is named for what it is -- a summary block under the INVESTMENT THESIS lead -- not for the portal's slot id; an adapter maps the name, not the data). |
| `risks` | `drafted_sections.risks` | TRUE INTERSECTION. |
| `risks.pre_mortem` | -- | **no slot today.** A sub-field of `risks`; `ThesisBundle`'s `drafted_sections.risks` has no equivalent decomposition named in this order's quotation. |
| `management` | `management` | TRUE INTERSECTION by NAME, different SHAPE: dossier's `management` is one cited passage (`C-EXEC-MANAGEMENT`: "the filing roster stays the authority on the page; the dossier's `management` is the team's cited passage BESIDE it, never a replacement") -- it is evidence to display alongside the roster, not a replacement for whatever `ThesisBundle.management` currently renders. |
| `cases` (`upside`/`base`/`downside`) | `model_cases` | TRUE INTERSECTION by concept; dossier's three cases are each an independently cited section (or ABSENT with a reason), never a computed/derived case. |
| `model_rows` | `model_status` / `fiscal_year_figures` (PARTIAL) | Dossier's `model_rows` names the ROWS (the typecast's shared mnemonic core + the sector template's KPI set, ordered) but carries **NO FIGURES** -- every row's `figure` is `{"value": null, "absent": "Bloomberg figure pull not authorized (R-16 V3)"}` (FWD-12). So `model_rows` can answer "is a model shape resolved for this name" (closer to `model_status`) but cannot populate `fiscal_year_figures`, which by its own name implies actual figures. Not claimed as a full intersection. |
| `growth_algorithm` | -- | **no slot today.** |
| `ownership` | -- | **no slot today.** |
| `special_items` | -- | **no slot today.** |
| `why_we_own` | -- | **no slot today.** |
| `positives` | -- | **no slot today.** |
| `negatives` | -- | **no slot today.** |
| `comparison_set` | -- | **no slot today.** |
| `thesis_pillars` (carried through from `continuation`) | -- | **no slot today.** (Distinct from `investment_thesis_summary` -- pillars are the bold-lead-plus-paragraph list; `ThesisBundle`'s `drafted_sections.investment_thesis` is quoted as one drafted section, not a pillar list.) |
| `thesis_summary` (carried through from `continuation`) | -- | **no slot today.** |
| `kpi_set` (carried through from `continuation`) | -- | **no slot today.** |
| `fund_of_record` (carried through from `continuation`) | -- | **no slot today.** |
| `last_stated_position` (carried through from `continuation`) | -- | **no slot today.** |
| `sector_template_ref` / `fund_form_ref` / `typecast_ref` | -- | **no slot today.** References (`{uri, content_sha256}`), not content -- an adapter that wants the underlying artifact's own fields reads them through `gold.gold_get(uri)`. |
| -- | `ceo_bio` | **Named in `ThesisBundle` with no dossier counterpart.** This cell builds no biography field of any kind (out of scope: "no synthesis of any field"; a bio is not a section this corpus's reports carry under a SECTION_NAMES lead). Recorded here for symmetry, though the order only asks for the dossier-side gap. |
| -- | `posture` | **Named in `ThesisBundle` with no dossier counterpart.** `posture` reads as a computed/derived stance, not a cited passage this cell could produce under `C-DOSSIER-IS-COMPOSED-NEVER-AUTHORED` ("no cell authors a new judgment into it"). |

**Count:** 21 dossier fields (`thesis_pillars`, `thesis_summary`, `kpi_set`, `fund_of_record`,
`last_stated_position`, `sector_template_ref`, `fund_form_ref`, `typecast_ref`, `model_rows`,
`recommendation`, `company_description`, `growth_algorithm`, `investment_thesis_summary`, `risks`,
`risks.pre_mortem`, `ownership`, `management`, `special_items`, `cases` (as one field of three), `why_we_own`,
`positives`, `negatives`, `comparison_set` -- 23 counting `cases`' three sub-fields and `risks.pre_mortem`
separately). Of those: **5 TRUE INTERSECTIONS** (`recommendation`, `company_description`,
`investment_thesis_summary`, `risks`, `cases`/`model_cases`), **1 NAME-MATCHED, SHAPE-NARROWER**
(`management`), **1 PARTIAL** (`model_rows` vs `model_status`/`fiscal_year_figures`), **the rest carry no
slot today**. Two `ThesisBundle` slots (`ceo_bio`, `posture`) have no dossier counterpart either.

## TWO EXAMPLE PAYLOADS

**ACCEPTED** -- `IMB_LN_Equity`, a served name with a stored dossier (trimmed: `inputs` to 2 of 4,
`model_rows` to 2 of 94, long passages truncated with `...`; every other field un-elided):

```json
{
  "artifact": "research-dossier",
  "method_version": "amgt-corpus-dossier/1",
  "subject": {"security_key": "IMB_LN_Equity"},
  "as_of": "2026-09-24",
  "inputs": [
    {
      "key": "amgt/harvest/bronze/research-report-extract/security_key=IMB_LN_Equity/a1caf1eec85230eb/extract.v2.json",
      "sha256": "4aa730f3ca32ecc8b80ef3dfb91435e331da9e41cdba6ee0d059d848cb7f4c61"
    },
    {
      "key": "amgt/harvest/gold/research-continuation/security_key=IMB_LN_Equity/f14d3e6eb29cec15.json",
      "sha256": "0df44e8d95398eb72a12b2c395dc58bd386f710af818d61087589ea9da09403c"
    },
    {"...": "2 more"}
  ],
  "fields": {
    "recommendation": {
      "value": "Potential ADD in IDVZ (currently ~2.5%)",
      "citation": {
        "report_key": "s3://opal-data-harvest/amgt/harvest/bronze/research-report/security_key=IMB_LN_Equity/a1caf1eec85230eb/Imperial Brands Research Pack 2026 07 17_v1.docx",
        "report_id": "a1caf1eec85230eb", "locator": 2,
        "passage": "Potential ADD in IDVZ (currently ~2.5%)"
      }
    },
    "company_description": {
      "value": "COMPANY DESCRIPTION: 4th largest international tobacco company, located in Bristol, UK. It makes and sells cigarettes including Davidoff, Gauloises, JPS, West globally; Winston, Ko...",
      "citation": {
        "report_key": "s3://opal-data-harvest/amgt/harvest/bronze/research-report/security_key=IMB_LN_Equity/a1caf1eec85230eb/Imperial Brands Research Pack 2026 07 17_v1.docx",
        "report_id": "a1caf1eec85230eb", "locator": 5,
        "passage": "COMPANY DESCRIPTION: 4th largest international tobacco company, located in Bristol, UK. It makes and sells cigarettes including Davidoff, Gauloises, JPS, West globally; Winston, Kool, Maverick & backwoods cigars in the US via its ITG Brands subsidiary), rolling tobacco and papers (Rizla), and a grow"
      }
    },
    "risks": {
      "value": "RISKS AND CONSDIERATIONS: Structural volume decline: the core product's user base shrinks ~2-5% a year in developed markets; the model only works while pricing elasticity holds. NG...",
      "citation": {
        "report_key": "s3://opal-data-harvest/amgt/harvest/bronze/research-report/security_key=IMB_LN_Equity/a1caf1eec85230eb/Imperial Brands Research Pack 2026 07 17_v1.docx",
        "report_id": "a1caf1eec85230eb", "locator": 19,
        "passage": "RISKS AND CONSDIERATIONS: Structural volume decline: the core product's user base shrinks ~2-5% a year in developed markets; the model only works while pricing elasticity holds. NGP losses and credibility: the April 2026 trading update warning that NGP adjusted operating losses would be \"moderately "
      },
      "pre_mortem": {"value": null, "absent": "no Pre-mortem: lead in the risks block"}
    },
    "cases": {
      "upside": {"value": null, "absent": "no UPSIDE CASE section in class A 2026-07-17 or class B missing"},
      "base": {"value": null, "absent": "no BASE CASE section in class A 2026-07-17 or class B missing"},
      "downside": {"value": null, "absent": "no DOWNSIDE CASE section in class A 2026-07-17 or class B missing"}
    },
    "thesis_pillars": [
      {
        "pillar": "Cash-return machine",
        "text": "~6% div yield plus a large buyback (£1.25bn completed in FY25) & £1.45bn launched for FY26). FY21-FY25 £10bn returned to shareholders",
        "citation": {
          "report_key": "s3://opal-data-harvest/amgt/harvest/bronze/research-report/security_key=IMB_LN_Equity/a1caf1eec85230eb/Imperial Brands Research Pack 2026 07 17_v1.docx",
          "extract_key": "s3://opal-data-harvest/amgt/harvest/bronze/research-report-extract/security_key=IMB_LN_Equity/a1caf1eec85230eb/extract.json",
          "locator": 11,
          "passage": "Cash-return machine: ~6% div yield plus a large buyback (£1.25bn completed in FY25) & £1.45bn launched for FY26). FY21-FY25 £10bn returned to shareholders"
        }
      }
    ],
    "sector_template_ref": {"value": null, "absent": "business type unmapped: conflict: consumer-non-cyclicals, technology"},
    "model_rows": [
      {"mnemonic": "ARD_SHARES_OUTSTANDING", "source": "typecast", "figure": {"value": null, "absent": "Bloomberg figure pull not authorized (R-16 V3)"}},
      {"mnemonic": "ARD_TOTAL_CURRENT_LIABILITIES", "source": "typecast", "figure": {"value": null, "absent": "Bloomberg figure pull not authorized (R-16 V3)"}},
      {"...": "92 more rows"}
    ]
  },
  "content_sha256": "85eeeffede334e4ae1b31943638590ee6202414a9218fdda9e03f4d4aefe2a87"
}
```

Live: `s3://opal-data-harvest/amgt/harvest/gold/research-dossier/security_key=IMB_LN_Equity/as_of=2026-09-24.85cd0367e4920671.json`
(`dossier.read_dossier("IMB_LN_Equity")`, this worker, 2026-09-24).

**REFUSED** -- a name with no dossier stored (`dossier.read_dossier("NOT_A_REAL_SECURITY_Equity")`, this
worker, 2026-09-24):

```json
{
  "exception": "LookupError",
  "message": "no research-dossier object under s3://opal-data-harvest/amgt/harvest/gold/research-dossier/security_key=NOT_A_REAL_SECURITY_Equity/"
}
```

The folder-shaped reason (the partition prefix that was searched and found empty) is the whole message, per
this order's own `read_dossier` spec ("`LookupError` with the folder-shaped reason when none exists").
