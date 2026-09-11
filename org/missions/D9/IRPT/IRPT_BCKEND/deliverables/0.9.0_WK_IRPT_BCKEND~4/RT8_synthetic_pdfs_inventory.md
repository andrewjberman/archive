# RT8 -- THE SYNTHETIC EVIDENCE INVENTORY

`0.9.0_WK_IRPT_BCKEND~4` on `IRPT_BCKEND.TO-IB-rt-8` -- closes row `IRPT_BCKEND-W4-S13`.

**NOTHING HERE WAS MOVED AND NOTHING WAS DELETED.** The CTO's ruling offered the evidence-surface
owner a choice: segregate the synthetic objects, or PROVE that every ordinary production reader
excludes them. Segregating is a copy plus a delete of the source key, and a delete is Andrew's
word -- so this cell took the second branch, and carries the deletion as an unexercised option on
the proof instance. `infra/aws/lambda/investor-reporting/export/exclusion.py` has no writer at all:
no `put_object`, no `copy_object`, no `delete_object`, asserted by a test rather than by this
sentence.

## THE OBJECTS

Bucket `opal-data-ycharts`, region `us-east-1`, read by `s3api list-objects-v2` + `head-object`
under this cell's serial. Sizes and metadata are the LIVE read from the battery's run, not a
record of what was written.

### The four the ruling names -- `firms/49financial/generations/GENIBS14SYN/attempts/1/exports/`

| key (under the prefix above) | bytes | metadata |
|---|---|---|
| `r1/report.pdf` | 43,848 | `irpt-synthetic=true`, `export-revision=r1`, `vendor-synthetic-holdings=false` |
| `v0-11-overview/report.pdf` | 41,859 | `irpt-synthetic=true`, `export-revision=v0-11-overview`, `vendor-synthetic-holdings=true` |
| `v0-11-comparison/report.pdf` | 41,859 | `irpt-synthetic=true`, `export-revision=v0-11-comparison`, `vendor-synthetic-holdings=true` |
| `v0-11-multicomp/report.pdf` | 41,859 | `irpt-synthetic=true`, `export-revision=v0-11-multicomp`, `vendor-synthetic-holdings=true` |

Four objects, 169,425 bytes total.

**WHY THEY EXIST.** IB-s-14's arm (g) is graded on the receipt's `artifact_hash` equalling THE
STORED OBJECT'S. Proving that required storing real objects; `_keys` validates a tenant against the
firm registry, so the only admissible prefix is a real firm's. The synthetic-ness is therefore
carried in the GENERATION id and in object metadata rather than in the firm segment, which is the
one segment that could not be fictional.

**WHY THREE OF THEM CARRY `vendor-synthetic-holdings=true`.** IB-s-14's arm (v0.11) compares the
estate's own render against the vendor's three v0.11 sections. The holdings behind those three are
SYNTHETIC and say so in their own metadata field, separate from `irpt-synthetic`, because the two
facts retire on different days: `irpt-synthetic` retires when the object does,
`vendor-synthetic-holdings` retires when real holdings land.

### The fifth, added by THIS cell -- `firms/49financial/generations/GENRT8PROOF/attempts/1/exports/`

| key (under the prefix above) | bytes | metadata |
|---|---|---|
| `rt8-a/bundle.json` | 660 | `irpt-synthetic=true`, `irpt-export-id=EXP-f4a19d4a46ec84f34c6a798552fc0a20`, `irpt-attempt-id=ATT-06e70252d2988bf71db17bb88588873e`, `irpt-bundle-sha256=5b01f8d8...fba3d`, `irpt-contract-version=investor-reporting_1` |

This is the FROZEN ExportBundle the served controller persists before any render -- the object
arm (a) reads back. It is inventoried here rather than kept off the census because **for one run it
was the exact case the exclusion arm exists to catch**: `GENRT8PROOF` does not end in `SYN`, so the
key predicate did not fire, and the controller was not yet stamping metadata, so neither did the
other. Row `IRPT_BCKEND-W4-S18` records it. Both halves were fixed -- the generation is listed in
`SYNTHETIC_GENERATIONS`, AND `handler.persist_bundle` now stamps `irpt-synthetic=true` from
`exclusion.key_is_synthetic(key)` so a synthetic generation labels its own objects without anyone
remembering to pass a flag.

## THE EXCLUSION, MEASURED

Two predicates, and a reader excludes when EITHER fires. A key filter alone is defeated by a
differently-named generation; a metadata filter alone is defeated by an object written without
metadata. `classify()` reports WHICH fired, so an object that trips only one is visible as the
partial case it is instead of passing because the other happened to catch it.

All 5 of 5 objects classify `EXCLUDED_BY_BOTH`.

| production reader | admitted, of 5 synthetic | admitted, of 1 ORDINARY control object |
|---|---|---|
| `directory` | 0 | 0 -- structural: this reader never addresses the generations prefix |
| `holdings` | 0 | 0 -- structural: this reader never addresses a `report.pdf` |
| `export_status` | 0 | **1** |
| `download` | 0 | **1** |

**THE CONTROL IS THE HALF THAT MATTERS.** Four readers admitting nothing proves nothing if they
admit nothing at all -- a filter that excludes everything is not a filter. The ordinary-object
column is the discriminator: the two readers that actually address this prefix still admit real
evidence, and only they could have shown a synthetic PDF to a person.

## 0 DELETES ISSUED

All 5 keys still `head-object` 200 AFTER the battery ran, read in the same process that ran the
census. This is asserted without CloudTrail because the assertion this cell can make directly is
stronger: the module has no writer.

## WHAT THIS DOES NOT COVER

Named here and repeated in `RT8-AC2_judgment.md`, because an inventory that reads as complete is
the failure mode: **a reader added after this commit is not covered by any of it.** The four
readers are a list this cell wrote, and nothing forces a fifth to call `exclusion.is_excluded`.
