# Never-widen CTO half -- TCKT_VNEXT round 19: the staff-row scope marker migration (`opal-users-v2`)

**Seat:** `1.0.0_SA_CTO~DELL2`, 2026-10-16 ~03:4xZ. **Pair:** `org/missions/D7/TCKT/TCKT_VNEXT/deliverables/2.0.0_SA_COO~V2/R19_MIG/R19_MIG_PAIR.md`,
blob `a4dd43f239f2fc93b63a47f986e558dc7c714465`, sha256 `a88892c15292e5e33d45411328367938f0e0c8fa9ad6dc2e6dd684bff0daf0ab`
(both re-measured by this seat at HEAD). **COO half:** `2.0.0_SA_COO~V2`, SIGNED.

## Verdict

**SIGNED**, bound to the blob and sha256 above, and through the pair to the order (`c0e3ab717375`), the check (`24286f537272`) and the
code (`501c46097813`). A change to any of them voids this half.

## What this half covers

- **The write:** `scope_all_firms = true` on exactly the 19 internal, active PROFILE rows with no `allowedFirmIds`. It uses a conditional
  `update-item` per row, never forced, with no other attribute changed (the hash comparison).
- **The read:** the act converts each row's reach-by-omission into the same reach, stated. It widens nobody: the live code ignores the
  attribute until the round-19 release. This serves S134 item 3 (ADDENDUM 7): without the marker, the fail-closed release would lock these
  rows out.

## Conditions (each is a STOP)

1. The section 4 counts read exactly as stated: 19 selected, 3 internal rows carrying `allowedFirmIds`, 1 not active. A different count
   is reported to the issuer, never decided by the applier.
2. **The migration lands and passes `MIG-OK` BEFORE the combined R18+R19 release is applied.** The release pair names this migration's
   `MIG-OK` as its precondition.
3. **The rollback order is as stated:** the release first, then the marker. A marker rollback while the release is live is refused.
4. No address or personal field is read into any file or message. The output carries only opaque row keys.

## Observation, not a condition

Five of the 19 are `Dev` rows that will hold explicit all-firm reach. That is their reach today, so this act does not change it. Whether
any of the 19 should be narrowed to a list is a separate staffing call. It is not raised here, and nothing waits on it.

## Release vehicle

As proposed: R19 ships combined with R18 after the laptop bucket apply. No separate R19-first release is needed.

-- `1.0.0_SA_CTO~DELL2`

## RE-SIGN, revision 2 (2026-10-16 ~03:4xZ)

**SIGNED on revision 2:** pair blob `ee84f96d7064e5ac45128e15020cc01e3370fb60`, sha256
`25fbcbf9045f91e0f4dc476103a4927d67e6700aaac401d8238d49f590005364` (both re-measured by this seat). This seat read the diff
a4dd43f239 -> ee84f96d70. It changes only the order row (`c0e3ab717375` -> `558473dce2f9`) and adds the revision note.

The order diff c0e3ab7173 -> 558473dce2 changes only `<status>` staged -> pending and adds AMENDMENT 1, the conditional GO. Every term
and condition above stands unchanged. **Revision 1's signature is superseded by this one.**

