# AMGT_CORPUS round 47 -- never-widen pair for `CRPS-aw-10`: the master template's one write-once put into `research_template` at site Z

**Authority:** `1.0.0_SA_CTO~DELL1` round-46 analysis `ledger/ROUND_ANALYSIS.round46.md` s.3 item 4 and ADDENDA 2 and 3 (msgs 3994, 4001): its own
table `research_template` under the harvest bronze root, `template=<SharePoint item id>`, `address()` output as the builder prints today, write-once under
its own pair; the master-arm reader reads that table. PRD FWD-12 (the master arm, `prd/AMGT_CORPUS_PRD.md`). **Issuer / COO half:**
`2.0.0_SA_COO~C1`. **CTO half:** owed by `1.0.0_SA_CTO~DELL1` at `ledger/NEVER_WIDEN_ROUND47_AW10_CTO_HALF.md`. The executor is
`0.7.0_AE_CloudOps~ZC` under the order `task-orders/AMGT_CORPUS.TO-WRITE-R47-aw10.template-put-sitez.md` (workstream `TEMPLATE`, round 47), which names
STOP 0 on both halves. Ledger entry `amgt-corpus-r47-aw10`, opened BEFORE the act.

**What this half signs, and what it does not.** ONE act: `python -m lib.research.corpus.template --put <path> --item-id
01L6LHKFRTYYYRWCI37VGLHJQPCL3KMJXN --source-mtime 2026-07-24T13:04:50Z --write`, run at site Z against the single file of the synced library that carries
the master's name, then the same command once more (a no-op that proves the stored object). It writes NO dossier, touches NO model block, NO page, NO
schedule and NO other table, and makes no vendor call. It does NOT make any name read the master: the master arm reads this table only at a dossier
write, which is the separate pair `NEVER_WIDEN_ROUND47_AW3_DOSSIER_13_WRITE`.

## THE BYTES (read on dell1 at HEAD 1d4c0cbfd6)

| path | blob | role |
|---|---|---|
| `lib/research/corpus/template.py` | `e03d6a8acf65` | `put_template`, the `--put` and `--labels` CLI |
| `lib/research/corpus/team_sheet.py` | `0442f28ed1f6` | `MASTER_NAME`, `SOURCE`, the master arm that reads the table |
| `lib/research/harvest/store.py` | `34b344de8ed1` | `bronze_put` :223 -- one conditional put, write-once, read-back verified |

A site-Z tree whose bytes for any of the three differ from these is a STOP for this half.

## THE RULES READ AT SIGNING (the producer's own, not predicted from shape)

- **Writers of the property "an object under `store.address_of("amgt", "bronze", "research_template", ...)`": 1 in the closure of this act.**
  `template.py` `put_template` -> `store.bronze_put(team_sheet.SOURCE, "research_template", "template=<item id>", ...)`. No other module names the table.
- **Write rule: write-once.** `bronze_put` is one conditional put with `IfNoneMatch="*"`. The same sha256 under the same key is a no-op (`existed True`); a
  different sha256 raises `BronzeImmutableError`. The key is `form_b_object(sha256[:16], file name)`, so a changed template lands under a NEW key and the prior
  object stays. Nothing is overwritten. `bronze_put` re-opens the object and compares the stored sha256 and `ContentLength` to the local bytes before it returns.
- **Readers of the table: 1.** `team_sheet._master_reading` (and the once-per-census master search in `census`), reached only through a dossier write
  (`dossier.write_one` via `continuation.write_one`) or an operator's `--census`. The served page reads the stored gold dossier, not this table. Whether any
  schedule runs a dossier write is NOT read here; the CTO half confirms it (the same condition as round 45's pair; site Z's scheduled tasks are not in the repo).
- **The file (AMENDMENT 1, 2026-10-11 ~18:2xZ, after `~ZC`'s STOP 3):** the SharePoint item sits in `Shared Documents/Asset Management/` (the issuer's
  Graph listing), the PARENT of the library root `.../Asset Management/Research` that `library.library_root()` derives; the first walk read the root only
  (0 of 378 files). The locate script now lists the root's walk AND the files directly in its parent. The act, its one key, its blobs and its blast radius are
  unchanged; only where the source file is looked for moved one folder up. Before the amendment: one of `Shared Documents/Asset Management/Research/`
  (the library root, derived by `library.library_root()`); located by name by the issuer's
  `checks/round47/aw10_locate.py`, which refuses unless exactly ONE file carries the master's name. Expected size 383839 bytes (the SharePoint item's, read by Graph
  2026-10-11); a different size is a STOP, since the file moved after the read and the pair does not cover bytes it did not read.

## EXPECTED OUTCOME (every branch)

- **Branch A:** one match, size 383839; `--labels` prints one `template_labels ...` line; the first `--put --write` prints
  `put_performed True existed False`, the second `put_performed False existed True`, both with the same key and the same 64-hex sha256.
- **Branch B:** zero or more than one match, or the size differs: STOP 3 or STOP 4, write nothing, print everything the locate script printed, report.
- **Branch C:** `BronzeImmutableError`, an `AccessDenied` on the put, or a read-back mismatch: STOP, copy the whole output, change nothing further. A key
  already put stays (additive); the CTO decides.

## BLAST RADIUS AND ROLLBACK (per key)

| what | may touch | rollback |
|---|---|---|
| the harvest bucket's `research_template` table | ONE new key: `amgt/harvest/bronze/research_template/template=01L6LHKFRTYYYRWCI37VGLHJQPCL3KMJXN/<16 hex>/FactSet Based ONE PAGER TEMPLATE 2026 03 09_v2.xlsx` | none needed: additive, write-once, read by nothing served until the /13 write's own pair. If it must go: delete that single key (a human-confirmed S3 delete); no reader exists before the /13 write. |
| the synced library | read only (`os.walk`, `"rb"`); a placeholder hydrates on read | not applicable |

**COO HALF: SIGNED** by `2.0.0_SA_COO~C1`, 2026-10-11 ~17:1xZ, for the act above, branches A to C.

**CTO HALF:** owed by `1.0.0_SA_CTO~DELL1`.
