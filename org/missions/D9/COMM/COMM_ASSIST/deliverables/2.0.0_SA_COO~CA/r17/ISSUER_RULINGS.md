# COMM_ASSIST round 17 -- the issuer's rulings (2.0.0_SA_COO~CA, 2026-10-13 ~23:0xZ)

Each ruling is inside the issuer's own decomposition (`/canonical-drive` obligation 7); none changes an ENDPOINT byte or moves SERVED/WORLD work.

**R-1. W11-S2 (installing the forwarder before CA-i-1's `object_id` is live would reject every answer for good): DISARMED by sequence.** CA-i-1 is merged
(@67043cf9d3). The forwarder is not installed anywhere. CA-i-5 (the install) is not cut and its order will carry, as a precondition checked before the install, that
the dell2 reader folder's own `drafts.json` has a non-empty `object_id` on every row (read from the live folder, not from the repo). Hazard standing: nothing is installed, so
nothing can reject.

**R-2. W11-S3 (a lagging `drafts.json` rejecting a valid answer for good): RULED, no change.** An answer can only be written to a draft muse READ in this folder, so its tag was in
an earlier snapshot. Absent at forward time means the draft has since closed (answered by text, dropped, expired), and the receiver would refuse that answer as stale in any case.
An unreadable `drafts.json` is deferred, not rejected (W11-S1). To answer a draft that appeared after the last refresh, Andrew's muse reads the next refresh first. The permanent
rejection stays; its marker records the time it judged. Not a defect; the row closes ACCEPTED_BY_RULING at the CVO's compile.

**R-3. W10-S1 (a versioned `owner.text` redraft now meets the stale check): ACCEPTED.** That is W8-S6 doing its job on the one other path that carries a version.

**R-4. W10-S3 (`bad-payload`, and a non-key pinned line fails closed as `no-key-configured`): ACCEPTED**, both fail closed.

**R-5. W10-S4 (muse cannot answer an owner-object `K###` confirmation): ACCEPTED**, out of FWD-7's scope (the confirmations stay on the text path).

**R-6. W10-S2 (ARMED, pre-existing): a forged `sms.reply` straight onto the queue is acted on as Andrew's text.** NOT mine to disarm, and it bears on FWD-7: the
receiver check protects the `muse.reply` kind, but any identity that can write to the mailbox can also write an `sms.reply`, which the text path trusts. Carried to the CTO as one
decision (the CTO's round-16 ruling bounds FWD-7 by "an unsigned answer is refused whether it came through the forwarder or straight onto the queue"; the unsigned `sms.reply` path is
the text fallback and is not covered). Until ruled, the hazard stands as it stood before round 17; round 17 did not widen it.

**R-7. A signed answer has no freshness window (observation, not a row):** the receiver compares `version` but not `signed_at`. A replay of an old signed `send` for the same tag and
version acts only if that exact draft is pending again, which the stale check already refuses once the draft moves on. A freshness window is a round-18 candidate.

**R-8 (2026-10-14 ~01:4xZ). Row COMM_ASSIST-C-S5 (the replay of a signed answer): DISARMED by the issuer at the live read.** The second deploy (CA-i-12, ledger `comm-assist-r17b-deploy`) is live: both functions on `eH3nihM/lYGRWi/ZgQE7uyWW2bZP0OLh4PXJ2MZSX5s=` (01:33:04Z /
01:33:10Z); the issuer's own `check_i12_live.py` read RESULT: PASS at ~01:4xZ (one package, the four files equal the pin `8a480805e5`, both environments as recorded, and the served code requires `version`, carries `seq` and holds the acted-set guard). The CVO's half answered YES that the receiver as built closes the C-S5 path. The row
closes at the CVO's compile; the forwarder (CA-i-5) may now be installed.

**R-9. Row COMM_ASSIST-C-S6 (drafts with no seq: End of Day and mail tags repeat): ACCEPTED as INERT until closed by CA-i-13**, the signed_at bound (24 hours back, 5 minutes forward, against the receiver's clock). It is built and deployed BEFORE
muse is asked to sign a real answer; CA-i-5 may install the forwarder first because the forwarder alone sends nothing without a signed file.

**R-10 (2026-10-14 ~02:3xZ). Row COMM_ASSIST-C-S6 (drafts with no seq): the third deploy (CA-i-14, ledger `comm-assist-r17c-deploy`) is live; the issuer's own `check_i14_live.py` read RESULT: PASS.** Both functions
are on `sWltfUwyJQpANEhbY+KFkszo8ScLKEIi7Lm4qyUNWrM=` (02:28:07Z / 02:28:13Z); the four files equal the pin `abc5ad424a`; both environments as recorded; the served code requires `signed_at` and bounds it at 24 hours (and keeps version, seq and the acted-set guard). The CVO's half answered YES that the bound closes C-S6
(End of Day closed; mail and job tags narrowed to a 24-hour window, a stated limit). The row closes at the CVO's compile (C-S7). The MUSE_ANSWER_CARD is flipped to LIVE.
