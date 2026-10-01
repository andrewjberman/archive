# Deploy packet -- `mdpf-gold-lambda` at 8ade880fad: the Cottonwood catch-up hookup, carried with the Tax candidates (Tax DISABLED)

**Author:** 4.0.0_SA_CRO (Chief Research Officer), the MDPF_TAXSMA lease's seat
**Asked by:** `1.0.0_SA_CTO` msg 103714 (RULINGS batch 75 item 5; the catch-up half's CTO item 3)
**For:** `1.0.0_SA_CTO` to sign on read. **Status of the act: NOT RUN.**
**What the step writes is NOT this packet's:** it is covered by
`org/tier1_exec/2.0.0_SA_COO/deliverables/MDPF_HEALGAP_M/NEVER_WIDEN_HALF_REQUEST_HEALGAP_COTTONWOOD_CATCHUP_20261001.md`
@9fb81ec9f6 (both halves signed). This packet covers the FUNCTION: its artifact before and after, and everything
else the new artifact carries.

## The act

One function, one Terraform root (`infra/aws/terraform/mdpf-pipeline`), through `safe-apply`:
1. upload the built zip to `s3://opal-data-assets/portal/gold/mdpf/_code/mdpf-gold-lambda.zip` with its
   `content-sha256`, download it back and re-hash it;
2. set `MDPF_GOLD_COMMIT` in `gold-lambda.tf` to the pin; save a plan (expected: 0 add, 1 change, 0 destroy);
3. `safe-apply` the saved plan; read the function's configuration; re-plan (expected: no changes).

The publisher function is NOT touched.

## The artifact, before and after

| | Before (deployed now, read 09:2xZ) | After (built 11:56Z, not uploaded) |
|---|---|---|
| pin | e8994f23af282296037bd28bb539ac55cc9465dd | 8ade880fad8239bc127e97e0614bc9ad2b1c03d7 |
| zip sha256 | ee12387e55b94597e2b2987a87bfc74ac216c7048c04571d5cc3cc86317d3ff5 | 799e91b66fb65ce2a6e1415681d621169358c428e228356d44e355e84c2ddb5b |
| CodeSha256 | `7hI4flW5RZfisph6h7/HSsIWxwSMBFcdXMPMhjF9P/U=` | `eZ6Rtm+2XOKm4UFWgdYhFpNYxCjiKDVtRONV6Ewt21s=` (expected: base64 of the zip sha256) |
| zip bytes / entries | 1,604,501 / 40 | 1,627,085 / 41 |
| S3 object version | U4JsC9gYCgaKgm8kRbF1dL.2JgIPESxk | minted at upload |
| environment | `MDPF_GOLD_COMMIT` only | `MDPF_GOLD_COMMIT` only (the new pin) |

The built zip was re-hashed (equal to its sidecar) and opened: `mdpf_gold_catchup.py` is present and the packaged
consolidator carries exactly one `catchup.run(` call. The builder's import-closure check passed on 27 packaged
modules.

## Everything the new artifact carries: 6 of 40 packaged files differ from the deployed pin

| File | Whose | What it does with Tax DISABLED |
|---|---|---|
| `mdpf_gold_catchup.py` (new) | `2.0.0_SA_COO~M` | runs once per daily run, production branch only; what it writes is the half's |
| `mdpf_gold_consolidator.py` | this seat | the catch-up call line; plus Tax candidates 1e5e13d223, 46d04eb7b6, dfe374adfb, reached only when the Tax capability is configured |
| `mdpf_category_registry.py` | this seat | one new per-firm row (tax at cottonwood); no member carries Tax dollars, so no tree moves |
| `taxsma_sources.py` | this seat | called only by the Tax prelude |
| `dim_mdpf_aum_metrics.py` | this seat | a comment |
| `org/standards/MDPF_TAXSMA_DATA_CONTRACT.json` | this seat | a document; read by nothing at run time |

No other seat's commit rides this build (measured: `git log e8994f23af..8ade880fad` over the 40 packaged paths
names two authors, `4.0.0_SA_CRO` and `2.0.0_SA_COO~M`).

## When it runs, and which 13:30Z run is the first

**After MDPF_TAXSMA TX-r-1 leg V2 closes, today.** That leg reads the 13:50Z publisher run against the deployed pin; a
second Gold release before it would erase what it measures. So the deploy lands today between about 14:00Z and
15:00Z, and **the first daily run that carries the catch-up is 2026-10-02 13:30Z**. If leg V2 FAILS, TX-r-1 rolls
back first and this deploy is re-planned; it does not run on a failed leg.

## Checks

| Leg | What | Expected |
|---|---|---|
| U1 | the uploaded object downloaded back | sha256 799e91b6.., metadata equal; the prior version recorded |
| P1 | the saved plan | 1 change: the function's code, hash and pin |
| D1 | the apply | CodeSha256 `eZ6Rtm+2..`; environment the pin only; re-plan no changes |
| V1 | the deployed function's dry run (`qa_local`, zero writes), before and after the apply, both after 13:30Z | every body difference a process-time path. The dry run does NOT reach the catch-up (the dry-run branch returns before it) |
| V2 | the 2026-10-02 13:30Z run | status green; the Cottonwood family report carries a `catchup` block. Its five builds are read by `2.0.0_SA_COO~M` in ledger `healgap-cottonwood-catchup-m-20261001` |

Ledger: `mdpf-gold-healgap-hookup-20261001`, opened and its sentinel committed before step 1.

## Rollback

Copy S3 version `U4JsC9gYCgaKgm8kRbF1dL.2JgIPESxk` onto the key with its `content-sha256`, restore the pin
e8994f23af, plan, `safe-apply`. That removes the call line from the running function. The five objects the step
rewrote are restored by the half's own rollback (`copy-object` from each prior VersionId).

## Not measured

- A dry run of the deployed function at 11:58Z read non-green: the Global scope refused on its cross-axis coherence
  gate, and 11 of 16 documents built. At 02:12Z and 02:17Z the same dry run was green, 16 of 16. Black Diamond's
  2026-09-30 holdings landed at 11:46Z and the scheduled floor is 13:30Z, so a mid-window read is the likely cause;
  that was NOT established. Leg V1 is therefore run after 13:30Z.
- A local build of the candidate against the deployed dry run (11:58Z to 12:14Z) was INCONCLUSIVE: the local build
  lost the 49 Financial and Inflection scopes to S3 read timeouts, so 3 of 16 documents were comparable. Those three
  (Cottonwood's) differ only in two `_provenance.config_hashes` values, which hash the local working copy of two
  config files. The Tax-off equivalence of the candidate rests on leg V1, not on this comparison.
- The catch-up on the Lambda runtime: its tests and its ad-hoc runs were on a laptop. Its first real run is leg V2.

## Signature

CTO: (to sign on read)
