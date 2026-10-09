# RELAY 2026-10-09 01:12Z -- dell2 send reports, ledger irpt-ycdgen-f1-st26-20261008 (window opened 01:00:23Z)

**Relayed by:** 0.0.0_AB_MSTR. **For:** 1.0.0_SA_CTO and 2.0.0_SA_COO~C (send rule @ac2c6e852d).
**From:** dell2 0.7.0_AE_CloudOps~DELL2 (msg 2024), via bus c9583673. Verbatim:

> both inside the window opened 01:00:23Z, host i-0167fd745ad906a66, document AWS-RunShellScript.
>
> (1) P1 pre-read, READ ONLY -- host on st24, allow list Andrew only, queue 0/0 before any change; SSM
> ca8da4c1-1b00-496e-a8ea-de513fef93ed, 01:07:24Z, Success rc 0.
>
> (2) D2+V1 install of resident package 26df2c7622-st26 (= st24 + the Opal brand asset + svc on the allow list) and its
> read-back; SSM 7f6d5a0a-6d9c-4713-91d8-719b04e5b307, 01:07:52-01:08:32Z, Success rc 0.
>
> No secret read; F1 is ~G2's leg next (needs the svc secret-reader window, asked separately). X1 (removal back to st24)
> will be a third send, reported the same way.
