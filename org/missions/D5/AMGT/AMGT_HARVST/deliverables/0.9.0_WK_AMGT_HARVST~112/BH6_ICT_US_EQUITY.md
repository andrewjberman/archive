# BH6: what `ICT_US_Equity` is and where its key came from

All figures are from `bh6_ict_source.out` (5 of 5 sources read, RECORD OK).

The key is a Bloomberg US-form of the Philippine port operator. In the pool universe (`universe/v1/2026-10-06.json`, 302 entries) the entry `ICT_US_Equity` has ticker `ICT US`, `source: coverage`, a null name, and a resolution reason that says it was measured through the Positioning chain on ticker root `ICT`, with SEDOL 6455819 and domicile PH. That SEDOL and domicile are those of International Container Terminal Services, the company the registry holds under `ICT_PM_Equity` as "INTL CONTAINER TERM SVCS INC" (registry source b, 1 of 72 records).

No source gives the key its own company name. The gold list (a, 242 records) and the collector identity record (c, 234 records) both show "International Container Termin" (30 characters, cut), but source c labels the evidence "pool name as read", and the pool entry for `ICT_US_Equity` has name null. The cut name is on a different pool entry: ticker `ICT`, `source: holding`, book IDVZ weight 1.63, `security_key` null, resolution UNRESOLVED, whose reason names `ICT_PM_Equity` and `ICT_US_Equity` as root-equal candidates "NAMED, NOT merged". So the name reached the key through the join on the ticker root, not through any record of the key.

Which source put the key on the list: the pool universe entry above (coverage source), carried through the collector identity record into the gold list. The registry (b) does not carry `ICT_US_Equity`; it has no entry for it, as the reviewer found.

Not known: whether the coverage-book entry `ICT US` was added on purpose or only by the root join. `ICT_US_Equity` and `ICT_PM_Equity` are NOT SHOWN BY ANY FIELD to be one issuer in the sources read: no shared LEI, CIK or name. The shared SEDOL 6455819 is in the pool reason text only, not a registry field. Source e (the landed fallback universe, 89 records) carries no ICT record. `research_names` and `sa_symbols` are caller-named options of `build()` with no default path, so no further input was read.
