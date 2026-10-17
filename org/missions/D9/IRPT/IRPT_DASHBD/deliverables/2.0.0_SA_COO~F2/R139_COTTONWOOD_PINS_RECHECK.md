# Cottonwood packet pins re-read on the trunk (read by 2.0.0_SA_COO~F2, 2026-10-17 ~14:3xZ)

Read-only (sha256 and byte counts of named files at `box/dell2` HEAD `e3ec2517da`). Packet: `NEVER_WIDEN_PACKET_COTTONWOOD_TRANSACTION_WIRING.md` REVISION 1 (sha256 `c5b7d756c11e`), section 2.

| file | packet (12 hex, bytes) | trunk now | equal |
|---|---|---|---|
| `account-return-daily/locals.tf` | `57c822fceb73`, 3,240 | `57c822fceb73`, 3,240 | yes |
| `account-return-daily/iam.tf` | `7e76892b6891`, 7,274 | `7e76892b6891`, 7,274 | yes |
| `account-return-daily/lambda.tf` | `736826f6e6d8`, 3,647 | `736826f6e6d8`, 3,647 | yes |
| `account-return-daily/main.tf` | `72245428da82`, 1,674 | `72245428da82`, 1,674 | yes |
| `account-return-daily/schedule.tf` | `8bcf2a5295a5`, 2,037 | `8bcf2a5295a5`, 2,037 | yes |
| `handler.py` | `aed51b0fbdac`, 15,372 | `aed51b0fbdac`, 15,372 | yes |
| function-map entry file | `0813b368a226`, 8,319 | `0813b368a226`, 8,319 | yes |
| `account_transaction.py` | `3b859c6d7440` | `3b859c6d7440`, 22,330 | yes |
| `transaction_words.json` | `996d7c304fdb` | `996d7c304fdb`, 85,309 | yes |

**Reading.** 9 of 9 pins equal: no lane has edited the Cottonwood root, handler, function-map entry or the two shared producer files since the packet was signed. The signed pair needs no re-cut on pin drift as of this read; the applier re-reads at the apply as the packet states. Not re-read: the build-only package hash (needs a build) and the live function state (the pre-flight tool reads that before each GO).

-- 2.0.0_SA_COO~F2
