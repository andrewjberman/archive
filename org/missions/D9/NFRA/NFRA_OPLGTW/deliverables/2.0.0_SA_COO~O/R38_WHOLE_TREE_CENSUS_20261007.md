# R38 item 4 -- the whole-tree read for the Schwab master account id, before any redaction cell is cut

By: `2.0.0_SA_COO~O` (issuer, NFRA_OPLGTW), 2026-10-07 ~15:2xZ. For `ledger/ROUND_ANALYSIS.round26.md` @c474e2d3f3, ruling R38,
row `NFRA_OPLGTW-Z-W28-S17`. Counts only. No identifier is written here, in the commit, or in the commands the rail logs:
the values were read and searched inside one Python process.

## Result: the redaction cell as ruled CANNOT be cut. The identifier is an operational key of the estate, not a leak in 52 files.

Read at site-Z CLOUD @c474e2d3f3, 15:11Z. Denominator: 62,041 tracked files. Instrument: `git grep -I` over the whole tracked
tree (binary files skipped).

| read | lines | files |
|---|---|---|
| the row's shape, `"master": "<6 or more digits>"` | 512 | 92 |
| the values behind that shape, searched as a bare word in ANY shape | 8,979 | 1,314 |
| files holding a value but not the shape | | 1,222 |

**There are TWO distinct 8-digit values behind the shape,** not one. Neither is a repeated-digit or sequential test number.

| | value A | value B |
|---|---|---|
| files with the row's shape | 84 | 36 |
| files with the bare value | 924 | 1,009 |
| of those, under `org/` (records, logs, orders) | 681 | 750 |
| of those, code or config outside `org/` | 159 | 166 |
| lines where it reads as a path or key segment | 1,704 | 1,949 |

Where the bare values sit, by top-level directory (A / B): `org` 681 / 750, `infra` 98 / 82, `data` 39 / 61,
`workflows` 39 / 43, `docs` 49 / 40, `projects` 15 / 29, `.claude` 2 / 3. By type (A / B): `.py` 102 / 128, `.tf` 13 / 17,
`.yaml` 11 / 8, `.json` 209 / 207, `.md` 441 / 530. The A and B file sets overlap (924 + 1,009 against 1,314 distinct), so
the two columns are not added.

## What that means for R38

1. **The worker's 52 files and 254 matches were one folder tree.** The same shape is in 92 files tree-wide, including
   `infra/aws/ec2/opal-gateway` (19 files), `data/assets/scripts` (3) and `workflows/atom_decomposition/runs` (14).
2. **The values are written into production code.** Pipeline scripts, Terraform, data contracts, the freshness
   configuration and two skills carry them, most often as a segment of an S3 key or a partition. Replacing them with a
   token at HEAD would change what those programs read and write.
3. **A redaction of "every file the read finds" is therefore not one cell and not safe.** It would touch 1,314 files across
   every lane of the repository.
4. **The premise of the bound needs a ruling before any cell:** either a Schwab master account id is a secret of this
   estate, in which case the remedy is a migration of every program that names it (a project, with Andrew's word), or it
   is an operational identifier like the AWS account id of R39, in which case row Z-W28-S17 closes with no redaction.

## Recommendation (the issuer's; the call is the CTO's and, for the first branch, Andrew's)

Treat it as R39 treats the AWS account id: an operational identifier, outside the bound. Restate the bound as
"a CLIENT account identifier" (an end client's account number). Row Z-W28-S17 then closes with no redaction and no history
question. The basis is the measurement above: outside `org/`, value A is in 159 code and config files and value B in 166.

If the ruling goes the other way, the narrowest defensible cell is the 92 shape files only (saved host output and
fixtures), and it still leaves 1,222 files holding the value.

## Not done

- No file was opened to read a value in context beyond the counting above, and no file was changed.
- The two values were not matched to firms. That they are the masters of two firms is the likeliest reading and is not
  measured here.
- Binary files and files outside the tracked tree were not searched.
