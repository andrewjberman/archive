# Cottonwood account matching -- the packet and the one ask (2.0.0_SA_COO~C1, 2026-10-16)

**For Andrew, to send to Cottonwood himself (call `f48a` (a): "We can do (a), and id need to send them that list. but we should do everything in our power to get as much done as possible before referring to them."). No seat contacts Cottonwood.**

## The ask, in one sentence

**Please send Commonwealth's account-registration file: for each account number, the owner's tax ID (or name and date of birth). An export that links each account number to its household would also do.**

Why this and nothing else: every other route is exhausted. The CRM export carries no account number and its tax ID has no partner on the account side (laptop read of the local `Files.zip`, 2026-10-16 ~01:4xZ: `org/tier1_exec/1.0.0_SA_CTO/deliverables/ANDREW_DIRECT_20261016_013xZ_F086_9987_RELAYED.md` @dc3206a808). The two systems share only an advisor code with four values. The packet below is what automatic matching could do without it; a registration file would turn the rest into a deterministic join.

## What automatic matching produced (nothing is applied)

The packet: `org/missions/D8/ADVI/ADVI_COTBKF/deliverables/0.9.0_WK_ADVI_COTBKF~180/NEAR_MATCH_REVIEW_PACKET.csv` (sha256 `0ebc168bfe3ab8d628ec964f2448277177148ebd5ac1b2f7591a7c0e8b84244d`, 118 rows) and its page `NEAR_MATCH_REVIEW_PACKET.md` (sha256 `c356f1bf738e50903be2fa2ea8b278235cefe69539f9f977942ebc75631f7e48`), merged @a1383db444. The key that turns a link id into two account numbers is outside the repository (`C:/dev/_cotbkf_match_20261015/NEAR_MATCH_REVIEW_KEY.csv`, 118 rows, on dell1 only).

| Measure | Count |
|---|---|
| Distinct candidate pairs (a Commonwealth account and a Black Diamond account) | 118 |
| Found by the household-and-holdings route / the exact-name route / both | 104 / 8 / 6 |
| Already deterministic (rest on the holdings fingerprint; nothing to confirm) | 11 |
| To confirm | 107 |
| Among the 219 reachable unmatched active accounts | 102 |
| Pairs with a competing pair (two candidates for one account) | 44 |

Of the 387 unmatched active accounts, 168 are clients new since the migration (no Commonwealth predecessor exists, nothing to match) and 219 are reachable. The packet reaches 102 of the 219 with a candidate; 10 more of its pairs sit on accounts already waiting on a person, and 5 on new-client accounts.

## What the packet cannot say

It cannot say which candidate is RIGHT, only that it passed the rule's tests. A link applies only on a person's word. The identity of the confirmer (you, or a Cottonwood operator you name) is yours to choose; the key file goes to whoever confirms, off git.

## Other routes considered and closed

- A second read of the CRM zip (the second one-job window): not needed; the laptop's read answered the key question.
- A CRM-household flag on the packet (the document-listing name bridge, 27 of 83 portfolio accounts to one CRM contact): ruled out by the CTO (msg 6391); it links a Commonwealth account to a CRM contact, not to a Black Diamond account, and the packet's household route already uses the same listing names.
- A mapping file from Black Diamond or Orion: the same ask as above, from the other side.

-- 2.0.0_SA_COO~C1
