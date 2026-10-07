# /freshness body attribution (AMGT-ba-2, step 1)

Measured on `opal-amgt-scoped-api` CodeSha256 `OVpDhfwDG3BzKE++wDxMlFA6JrwpTnH3FiHC+NrzsrE=` at 2026-10-07T01:14:11Z,
GET `/api/scoped/amgt/freshness` by direct invoke. Decoded body 2,889,557 B (gzip -6 of it: 725,079 B). Source:
`BODY_ATTRIBUTION.json`.

| Top-level key | Bytes | Share |
|---|---|---|
| reads | 2,758,275 | 95.5% |
| rows | 130,341 | 4.5% |
| denominators | 589 | <0.1% |
| snapshot | 164 | <0.1% |
| rot | 141 | <0.1% |
| generated_at | 35 | <0.1% |
| (sum of the above) | 2,889,545 | 12 B of separators unattributed |

| `reads` record | Bytes |
|---|---|
| seeking_alpha_bronze | 2,139,235 |
| bloomberg_bronze | 611,274 |
| packs | 6,626 |
| lists | 417 |
| universe | 412 |
| bright_data_serp | 290 |

Largest record `seeking_alpha_bronze`: field `last_modified` 2,139,028 B; the other seven fields total 167 B.

| Row field (all 302 rows) | Bytes |
|---|---|
| rot | 42,582 |
| per_input | 24,387 |
| security_key_basis | 12,930 |
| security_key | 8,810 |
| last_refreshed | 8,650 |
| name | 6,168 |
| pack | 5,630 |
| source | 5,567 |
| covered | 4,737 |
| reason | 4,228 |

Rows: 302 total, 95 covered (43,965 B); the 207 other rows are 85,764 B. (The round-76 analysis said 242 keys; the route returns 302 rows.)

**The bytes are in `reads`: 95.5% of the body, and 2,139,028 B of that is the single `last_modified` map inside `reads.seeking_alpha_bronze` (plus 611 KB in `bloomberg_bronze`), while all 302 rows together are 4.5%.**
