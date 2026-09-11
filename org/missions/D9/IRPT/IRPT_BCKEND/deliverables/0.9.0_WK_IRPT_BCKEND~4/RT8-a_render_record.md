# RT8 ARM (a) -- THE RENDER, RUN ON THE HOST

`0.9.0_WK_IRPT_BCKEND~4` on `IRPT_BCKEND.TO-IB-rt-8`, after the issuer amendment of 2026-09-11.
Ledger `irpt-bckend-rt8-render` (5 legs, CLOSED), entry
`org/critical_paths/change_management/20260911T1530Z_irpt-bckend-rt8-render_deploy_completion.md`.
Machine-readable record: `RT8-a_render_record.json`.

**THE WORD.** `1.0.0_SA_CTO` 95983 carrying Andrew-direct 2026-09-11 ~14:5xZ, VERBATIM
*"Yes ycharts runner may be started"*. Option A of the host README, exactly as written and nothing
wider: start the host FOR THE RENDER, send `irpt-export-render-run`, return the host to the state
its root declares.

**THE OUTCOME: `SESSION-GATED`.** Not a skip -- the issuer's amendment names this branch by name.
The browser opened, reached the real portal origin, loaded the print route, and found a sign-in
screen; `render_export.cjs` refuses `SESSION_ABSENT` by construction and has no credential prompt
to forget to remove. Row `IRPT_BCKEND-W4-S25`; the session belongs to IB-rtb-1.

---

## I. WHAT THE ACT LOOKED LIKE

| step | at (UTC) | result |
|---|---|---|
| submit through the DEPLOYED controller | 15:49:25 | `EXP-184aaa5454d45e8eb6312fe2a175fa01`, attempt `ATT-de6ea6df67930b8ad027f3e8204ddaa5`, bundle persisted at `.../GENRT8PROOF/attempts/1/exports/rt8-render/bundle.json` |
| `ec2 start-instances` | 16:25:49 | previous state `stopped` -> `pending` |
| instance `running` | 16:26:1x | 27 s |
| SSM agent `Online` | 16:26:16 | a SEPARATE fact from `running`; a send before it fails with an `InvalidInstanceId` that reads like a wrong id |
| `ssm send-command irpt-export-render-run` | 16:26:19 | command accepted |
| command terminal | ~16:26:4x | `Failed`, carrying `SESSION_ABSENT` |
| `ec2 stop-instances` | 16:26:44 | in a `finally` -- the stop does not depend on the render succeeding |
| instance `stopped` | 16:27:0x | confirmed again by a LIVE read inside the battery, not from this record |

**THE HOST WAS RETURNED ON EVERY ONE OF THE FIVE SENDS**, including the four that failed. The word
is a CYCLE, not a new resting state: `aws_ec2_instance_state.runner` still declares `stopped`, the
ycharts root re-plans `No changes`, and a host left running after a render would be drift against
that line rather than a permission.

## II. THE NETWORK GUARD -- A REAL BROWSER, A REAL HOST, A REAL DENOMINATOR

```
GUARD: {"requests_total":12,
        "requests_by_origin":{"opalinvest.dev":10,"fonts.googleapis.com":1,"fonts.gstatic.com":1},
        "foreign_origin_requests":2,"vendor_requests":0,"allowed_origin":"opalinvest.dev",
        "denominator":"2 foreign of 12 request(s); vendor hosts checked: ycharts.com,
                       api.ycharts.com,bd3.bdreporting.com,api.cloud.orionadvisor.com",
        "outcome":"REFUSED","refusal":"BLOCKED: SESSION_ABSENT ..."}
```

**`0 VENDOR of 12` is the number the bound is about, and it is zero. `2 FOREIGN of 12` is the
number the criterion's wording asked for, and it is NOT zero** -- the page pulls webfonts from
`fonts.googleapis.com` and `fonts.gstatic.com`. Printing "0 external connections" would have been
a claim this cell's own instrument refutes. Row `IRPT_BCKEND-W4-S23`, and it meets the font finding
in `RT8-AC2_judgment.md` s.2 from the other side: the package DECLARES Lato and the app FETCHES its
faces from a third party at render time.

**THIS MEASUREMENT ONLY EXISTS BECAUSE THE GUARD WAS MOVED OFF THE SUCCESS PATH.** The original
shape wrote `render_guard.json` beside the PDF, so a refused render produced no denominator at all
-- and the refusal is precisely the run where "what did the page talk to" is a live question.

## III. THE FOUR REFUSALS BEFORE THIS ONE -- each a real gap, each named

The host half had been written and had never run on a host. Every send produced a named refusal
rather than a silent failure, and each one is a measurement of a different gap:

| # | refusal | what it measured |
|---|---|---|
| 1 | `MODULE_NOT_FOUND: playwright` | the host half had never been DEPLOYED -- `/opt/investor-reporting-export` did not exist until the render document was made to sync its own code |
| 2 | `RENDERER_MODULE_ABSENT` | `/opt/*/node_modules` is one level too shallow on this box; the discovery step printed every candidate instead of guessing again |
| 3 | `MODULE_NOT_FOUND: @aws-sdk/client-s3` | the manifest declared a dependency the host cannot obtain (npm egress is refused). S3 now goes through the AWS CLI already on the box; the dependency was removed rather than wished for |
| 4 | `net::ERR_SSL_UNRECOGNIZED_NAME_ALERT` | `local.portal_origin` was a hostname the estate does not own. Row `IRPT_BCKEND-W4-S22` |

**WHAT THE BOX ACTUALLY CARRIES**, printed by the document's preflight rather than assumed: node
`v18.20.8`; playwright at `/opt/investor-reporting-ycharts/research/20260911/node_modules`;
Chromium `1187` and `chromium_headless_shell-1187` cached under `/root/.cache/ms-playwright`. The
render reuses all of it and installs nothing.

## IV. WHAT THIS PROVES, AND WHAT IT DOES NOT

**PROVEN END TO END ON REAL INFRASTRUCTURE:** the controller freezes and persists the bundle before
any render; the host is started on the word and returned afterwards; the render document deploys
its own code under the instance role; the box's browser is found and launched; the REAL portal
origin is opened; the network guard counts every request by origin with a denominator; and the
whole cycle leaves the estate exactly as it found it.

**NOT PROVEN, and no sentence here should be read as proving it:** that a PDF renders. No
`report.pdf` and no `render_guard.json` object were written -- `head-object` reads MISSING on both,
and that is the correct outcome for a refused render rather than a gap in the evidence. The
receipt's `artifact_hash`-equals-the-stored-object arm remains proven only where it was proven in
round 1.
