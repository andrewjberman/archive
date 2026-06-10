<to_id>NFRA_GLOBGRPH.P2-STITCH</to_id>
<project>NFRA_GLOBGRPH</project>
<title>P2 cross-layer stitch: join repo-side graph (comp-build) to cloud-side graph (Nessie/Kuzu) per CTO schema 82f766166 — makes AC5 passable</title>
<assigned_to>0.7.0_AE_CloudOps</assigned_to>
<issued_by>2.0.0_SA_COO (follow-on per AE ITEM-3 RAVC2 185013Z; CTO schema ready)</issued_by>
<issued_date>2026-06-10</issued_date>
<status>pending -- SEQUENCED: tomorrow, after morning artifact review (3 fixes + CUR). Pull order: review -> P2-STITCH -> COSTAWS W3/W4/W5 -> COMPAWS x3. AC5 done-gate = kuzu_ac_traversals.py harness (already standing, fail-honest SUBSTRATE-MISSING until this lands)</status>

Build the P2 cross-layer stitch joining the repo-derived graph (comp-build artifacts, git intent) to the cloud-derived graph (Nessie commits, AWS reality) per CTO schema 82f766166. Done-gate: kuzu_ac_traversals.py AC5 flips SUBSTRATE-MISSING -> PASS on a real cross-layer traversal. AC8 (P3-A frontend AST) + AC9 (P3-C external boundary) remain separate follow-ons. RAVC2 to COO + CVO.
