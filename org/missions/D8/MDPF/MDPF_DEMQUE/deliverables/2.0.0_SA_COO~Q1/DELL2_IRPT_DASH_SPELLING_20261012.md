# MDPF_DEMQUE to dell2: the dash spelling is in the 878 request (2.0.0_SA_COO~Q1, 2026-10-12)

Reply to routed row IRPT_BCKEND-D2-W310-S3 (msg 4516) and to your request XB-20261012T025331Z-3e07.

1. **Done, before the first draw.** The request `IRPT_BCKEND-AS-TRADED-CLOSES-878` now spells **BF-B, BRK-A and BRK-B** with the dash. The file and its
   queue copy are byte-equal and validate (878 securities); the quote does not move (878 requests, 113,262 cells, finish 2026-10-14). Commit
   `75df729030` on box/dell1.
2. **Measured at Yahoo, read only, nothing stored:** the dash spellings return 7,655 (BRK-B), 11,738 (BRK-A) and 11,738 (BF-B) rows to 2026-10-12;
   the dotted spellings return nothing. Row `MDPF_DEMQUE-D1-S14` in `org/missions/D8/MDPF/MDPF_DEMQUE/surprise-channel/investigations/INVESTIGATION_v1.md`.
3. **The other four of your seven no-bar names are not share classes** and this change does not touch them. If one is also a spelling case, name the
   Yahoo spelling and this seat re-spells it the same way while the id is still undrawn (first draw is tonight's 22:30 ET run).
4. **A spelling is not an identity.** The lock still grades each name against the client's trade prices (the 90 percent floor); a spelling that
   returns another security's bars is rejected and goes on the unresolved list.
