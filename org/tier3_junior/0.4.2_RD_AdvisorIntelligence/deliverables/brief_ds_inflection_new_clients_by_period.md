# Brief — Add `new_clients_by_period` to Inflection `cumulative_chart.json`

**Author:** 0.4.2_RD_AdvisorIntelligence
**For:** 0.4.0_DS_ClientPlatform~A
**Date:** 2026-05-15
**Origin:** Andrew direct — "next D run grabs it, no FE work"
**Lane:** DS — single gold script edit. **No FE change. No portal work.**

---

## 1. Problem

Inflection ADVI → Distribution → Segment Analytics → **Continuous** view shows
`0 New Clients` in the left-rail tile, both AUA mode and NNA mode (Andrew
screenshots 2026-05-15 13:07).

The FE is correct and already shipped. Both "New Clients" tiles in
`DistributionTab.tsx` (NNA-mode L1655–1687, AUA-mode L2491–2522) read:

```ts
const periods = data?.new_clients_by_period?.[periodKey]   // periodKey ∈ quarterly|monthly|annually
```

then sum `count` over periods inside the selected Window. When the key is
**absent** the tile falls back to `0`. This is the **same code path that works
for 49Financial** — 49F's `cumulative_chart.json` carries `new_clients_by_period`;
Inflection's does not.

**Root cause:** `data/orion/scripts/gold/INF_D_00d.cumulative_chart.py` never emits
`new_clients_by_period`. Its `main()` assembles the `chart` dict (L567–578) with
`geo/geo_drill/adv/nna_geo/nna_adv` only. The 49F builder
(`data/black_diamond/scripts/gold/D_04.client_portal_summary.py:2129–2172`) has
the block; the Inflection script was never given parity.

Verified by direct S3 inspection:
- `s3://opal-data-inf/platinum/firm/cumulative_chart.json` — **no** `new_clients_by_period` key
- `s3://opal-data-bd/platinum/firm/cumulative_chart.json` — **has** it (quarterly/monthly/annually)

---

## 2. Exact FE-expected shape (do not deviate — this is the contract)

`types.ts` → `PlatinumCumulativeChartResponse.new_clients_by_period` (L2210–2214):

```ts
new_clients_by_period?: {
  quarterly?: NewClientsByPeriodPoint[]
  monthly?:   NewClientsByPeriodPoint[]
  annually?:  NewClientsByPeriodPoint[]
}
// NewClientsByPeriodPoint = { period: string; label: string; count: number }
```

**All three granularity keys are required** — the FE picks one based on the
Interval toggle (Month/Quarter/Year). String formats, copied verbatim from the
working 49F artifact:

| Granularity | `period` format | `label` format | Example |
|---|---|---|---|
| quarterly | `YYYY-Q{n}` | `Q{n} '{yy}` | `{"period":"2026-Q2","label":"Q2 '26","count":10}` |
| monthly | `YYYY-MM` | `{Mon} '{yy}` | `{"period":"2026-05","label":"May '26","count":3}` |
| annually | `YYYY` | `YYYY` | `{"period":"2026","label":"2026","count":29}` |

Each list **sorted ascending by `period`**. `count` is a plain `int`.

The block goes at the **top level of the `chart` dict** (sibling of `geo`,
`nna_geo`, etc.) — exactly where 49F puts it.

---

## 3. Source field — Inflection grain

Inflection "client" = **household** (HH), not account, not relationship-id.
"New client" = the period a household's **earliest account opened**.

Use `account_start_date` from `accounts_v2`. The script **already loads this** in
`main()` as the local var `accounts_v2` (`load_accounts_v2()`, L546) — **do not
add a new S3 read.** Relevant columns: `household_id`, `account_start_date`.

`account_start_date` is stored as mixed `datetime.date` / float-NaN — you **must**
`pd.to_datetime(..., errors='coerce')` then `dropna`.

`household` dim has no inception date — `accounts_v2.account_start_date` is the
only onboarding signal. This mirrors 49F, which uses `client_dimension.first_seen_date`.

---

## 4. Implementation — drop-in for `INF_D_00d.cumulative_chart.py`

### 4a. Add this builder function (anywhere above `main()`)

```python
_MONTH_SHORT = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun',
                'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']


def build_new_clients_by_period(accounts_v2):
    """new_clients_by_period — new HOUSEHOLDS per period for the DistributionTab
    Continuous 'New Clients' tile. Parity with BD D_04 L2129-2172.

    Inflection grain = household; a household is 'new' in the period of its
    earliest account_start_date. accounts_v2 is the latest snapshot already
    loaded in main() -- no extra S3 read. Returns None on missing inputs so
    main() can omit the key (FE treats absent as 0, same as BD's omit path).
    """
    if (accounts_v2 is None or accounts_v2.empty
            or 'household_id' not in accounts_v2.columns
            or 'account_start_date' not in accounts_v2.columns):
        log('WARN: new_clients_by_period: accounts_v2 missing required columns -- omitting')
        return None

    df = accounts_v2[['household_id', 'account_start_date']].copy()
    df['account_start_date'] = pd.to_datetime(df['account_start_date'], errors='coerce')
    df = df.dropna(subset=['household_id', 'account_start_date'])
    if df.empty:
        log('WARN: new_clients_by_period: no usable account_start_date rows -- omitting')
        return None

    # earliest account open per household = household onboarding date
    hh_first = df.groupby('household_id')['account_start_date'].min()

    def _periods(gran):
        freq = 'Q' if gran == 'quarterly' else 'M' if gran == 'monthly' else 'Y'
        out = []
        for period, grp in hh_first.groupby(hh_first.dt.to_period(freq)):
            y = period.start_time.year
            m = period.start_time.month
            yy = str(y)[2:]
            if gran == 'quarterly':
                q = (m - 1) // 3 + 1
                pk, label = f'{y}-Q{q}', f"Q{q} '{yy}"
            elif gran == 'monthly':
                pk, label = f'{y}-{m:02d}', f"{_MONTH_SHORT[m - 1]} '{yy}"
            else:
                pk = label = str(y)
            out.append({'period': pk, 'label': label, 'count': int(len(grp))})
        return sorted(out, key=lambda x: x['period'])

    result = {
        'quarterly': _periods('quarterly'),
        'monthly':   _periods('monthly'),
        'annually':  _periods('annually'),
    }
    total = sum(e['count'] for e in result['annually'])
    log(f'new_clients_by_period: {total} households across annual series')
    return result
```

### 4b. Wire into `main()` — after `nna_adv_view` is built (after L565), before the `chart` dict

```python
    new_clients = build_new_clients_by_period(accounts_v2)
```

### 4c. Add the key to the `chart` dict (L567–578)

Append after `'nna_adv': nna_adv_view,`:

```python
    chart = {
        'generated_at': _now_str(),
        ...
        'nna_adv': nna_adv_view,
    }
    if new_clients is not None:
        chart['new_clients_by_period'] = new_clients
```

(The conditional omit mirrors BD's `try/except ... omitting` pattern. The FE
handles an absent key gracefully — but with this data present it never will be.)

That's the whole change — ~45 lines, one file, additive only. No change to any
existing view builder, no schema change to `geo/adv/nna_*`. The `chart` dict
feeds both `CUMULATIVE_CHART_KEY` (platinum) and `GOLD_ARTIFACTS_KEY`
(side-write), so both outputs pick it up automatically.

---

## 5. Verification — ground-truth expected counts

Probed `s3://opal-data-inf/silver/api_dims/accounts_v2/snapshot_date=2026-05-15/data.parquet`
(862 accounts, 298 households). Earliest `account_start_date` per household,
bucketed by quarter — your emit should match this exactly:

```
2020Q2 111   2021Q4 10   2023Q1 7    2024Q3 7
2020Q3 7     2022Q1 11   2023Q2 8    2024Q4 10
2020Q4 5     2022Q2 10   2023Q3 4    2025Q1 4
2021Q1 5     2022Q3 5    2023Q4 8    2025Q2 4
2021Q2 3     2022Q4 10   2024Q1 4    2025Q3 23
2021Q3 7     2023... ...  2024Q2 4    2025Q4 10
                                      2026Q1 9
                                      2026Q2 10
```
**Total all-time: 296 households** (296 of 298 have a usable `account_start_date`).
`annually` sums to the same 296; `2026` annual = 19. The 2020Q2 spike of 111 is
the firm's original-book migration onto Orion — accurate, leave it.

FE behavior sanity check: in the screenshot (1Y window, Quarter interval) the
tile should land around **~56–60** (the FE sums the in-window quarters). Anything
non-zero confirms the wire; exact value is the FE's window math, not yours.

Quick check after the run:
```bash
aws s3 cp s3://opal-data-inf/platinum/firm/cumulative_chart.json - | \
  python3 -c "import json,sys; d=json.load(sys.stdin); n=d.get('new_clients_by_period'); \
print('present:', n is not None); \
print('quarterly tail:', n['quarterly'][-3:] if n else None); \
print('total:', sum(e['count'] for e in n['annually']) if n else 0)"
```

---

## 6. Deploy

Standard DS gold cycle (CLAUDE.md Rule 13/14/15):
1. `from __future__ import annotations` is already L49 — OK.
2. `.tools/ds-commit-gate.sh data/orion/scripts/gold/INF_D_00d.cumulative_chart.py`
3. `comp-pipescript io data/orion/scripts/gold/INF_D_00d.cumulative_chart.py`
   (no new columns *loaded* — `account_start_date` is already in the `accounts_v2`
   frame; no COLUMN GAP expected)
4. commit (`.tools/safe-commit.sh`, `--author "0.4.0_DS_ClientPlatform~A ..."`) → push CLOUD → S3 upload → `comp-pipescript deployed` MATCH
5. Next INF_D chain run materializes it — or SSM-direct `--single INF_D_00d` per the
   single-script runbook if you want it before the 2026-05-16 06:00Z full chain.

**No portal release, no FE commit, no DT bundle.** Once the artifact carries the
key the existing FE tiles render it on next page load.

---

## 7. Contacts

- FE contract questions → 0.4.2_RD_AdvisorIntelligence
- 49F reference implementation → `data/black_diamond/scripts/gold/D_04.client_portal_summary.py:2129–2172`
