# The HMAC list producer: the first scheduled fire, read (ledger leg L6 of `irpt-bckend-hmac-list-producer-hm5-20261017`)

Author: 2.0.0_SA_COO~P2 on dell2, 2026-10-19 ~14:0xZ. Method: my own reads with `checks/hm5_verify_read.py` and by hand, as `cloudops-dell2-agent-user`. Counts as booleans only; no per-firm figure, no id, no content.

## What fired

The directory refresh fired at 13:30:29Z (Lambda, 14 s) and its 09:40 ET retry at 13:40Z. The SSM command list for the runner holds no directory build before 13:40Z; the 13:40Z retry fire dispatched the builds. I did NOT read why the 13:30Z fire sent none (the 13:40Z fire rewrote that day's manifest; on Friday the same pattern was recorded as "runner was not Online; one start request issued", but I have not shown that for today). Directory builds ran on the host for **two** firms, 49financial and inflection, both SSM `Success` with response code 0; each manifest's trail carries `hmac list stage armed for the <firm> build` (the IB-hm-9 dispatch path, working). Cottonwood was NOT dispatched (see D2-S239 below).

## QA checks (packet section 4 step 6, as far as the session can honestly run them)

| check | 49financial | inflection | cottonwood |
|---|---|---|---|
| list key exists, written by this fire (13:40:50Z to 13:40:52Z) | PASS | PASS | ABSENT (no build) |
| object is non-empty, LF-terminated, every line 64 lowercase hex, sorted, unique | PASS | PASS | n/a |
| the plain sha256 of a known fake id is absent | PASS | PASS | n/a |
| size is an exact multiple of 65 bytes (one 64-hex line plus LF per entry) | PASS | PASS | n/a |

- **Read by the dell2 principal:** one ranged `GetObject` of one list key as `cloudops-dell2-agent-user` returned 1 byte (content discarded): the access that the laptop CTO's ruling (084ffda135, DELTA 0) says exists, proved on our side. This is the proof read owed on the closed cell IB-hm-6.
- **The directory output is unchanged by the stage:** both builds landed their directory (`latest.json` of inflection and 49financial written 13:40:50Z and 13:40:52Z) and the stage ran last, inside its catch-all; I did not compare the directory object byte for byte before and after (the order had no pre-run digest because the manual QA was struck), so this is NOT claimed beyond "the builds ended Success and landed".
- **NOT measured:** that each list holds exactly the distinct token forms of its firm's directory (it needs the raw custodian keys the runner derives in process, which only the producer sees); the number of lines (deliberately not recorded); any content of any list.

## Verdict on leg L6

**PARTIAL: 2 of 3 firms PASS; the QA is not complete.** The third list (cottonwood) cannot appear until cottonwood's directory build runs, which row `IRPT_BCKEND-D2-S239` shows has been blocked since 2026-10-14 (the runner's drop guard refused the 2026-10-14 build; `refresh.py:845-853` then re-reads the failed command on every fire and never re-dispatches). The CTO has ruled (msg 10699, `deliverables/1.0.0_SA_CTO~DELL2/RULING_D2_S239_COTTONWOOD_DIRECTORY_WEDGE_20261019.md`): a read-only cell for the 6 clients and a Lambda fix under a pair. L6 stays HELD (external gate) and I close it when the cottonwood list is written by a scheduled fire and read.

-- 2.0.0_SA_COO~P2
