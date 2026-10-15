# G2 client adapter protocol -- the one interface every `client_*` vendor adapter is built against (issuer's, round 37, OG-cl-1 .. OG-cl-6)

Why this file exists: the six vendor adapters are built IN PARALLEL in separate worktrees, so none of them can import another's code. This file fixes the seam. The core (`app/client_core.py`, OG-cl-1) implements the CONTEXT side; each adapter implements the ADAPTER side; the issuer hooks the adapters into the core at the merge (CUT BY WRITE SET). The binding behaviour of the five tools is `G2_CLIENT_TOOLS_CONTRACT.md` (in `deliverables/0.9.0_WK_NFRA_OPLGTW~83/`); this file adds only the seam.

## Adapter side (what a vendor adapter module exports)

Module `app/client_adapter_<vendor>.py`, no import of any other adapter, no import of `app.tools`, no boto3 client at module scope.

```python
VENDOR = "schwab"                      # the vendor key; lower case, one word
FIRMS = ("49financial",)               # the canonical firms this vendor can answer for (contract "Firm fence kinds")

class AdapterRefusal(Exception):       # defined in EACH adapter file in the same shape; the core catches any exception with a `.code` str attribute
    def __init__(self, code, detail=None): self.code, self.detail = code, detail

def resolve_account(ctx, firm, account_last4, platform=None, as_of=None) -> dict
def get_holdings(ctx, firm, account, platform=None, as_of=None) -> dict
def get_transactions(ctx, firm, account, platform=None, from_date=None, to_date=None) -> dict
def get_allocation(ctx, firm, account, platform=None, as_of=None) -> dict
def get_fees(ctx, firm, account, platform=None, from_date=None, to_date=None) -> dict
```

- Every function returns a dict of the contract's BODY fields (`candidates`, `positions`, `cash`, `transactions`, `allocation`, `fees` ... as the tool section names them) PLUS the keys `_as_of`, `_partition_date`, `_source_keys` (list), `_denominator` (dict), `_platform_label`, `_platform_label_source`, `_label_claim` ("measured" or "inferred"). The core builds the shared envelope from the `_`-keys and strips them.
- A function a vendor does not serve raises `AdapterRefusal(<the contract's refusal code>)` (for example `no_source_49f_a2`, `vendor_no_holdings`, `no_fee_source`, `no_resolve_source`); it never returns an empty body without a code.
- `firm` arrives CANONICAL (`49financial`, `cottonwood` or `inflection`); `account` arrives as a resolved `account_ref` the same adapter issued; a bare number or a last-4 is refused by the core before the adapter is called. The adapter still re-checks that the `account_ref` belongs to `firm`'s segment.
- NO S3 bucket, prefix, role ARN or key is typed in adapter code as a literal that the naming gate would grade: every prefix is built through `ctx.prefix(vendor, firm_segment, "silver", table)` which the core derives from the DATA_CATALOG rows; a table with no catalog row is `AdapterRefusal("no_catalog_row")`.

## Context side (what `ctx` offers; the core implements it, an adapter test fakes it)

```python
class Ctx:
    def prefix(self, vendor, segment, layer, table) -> str          # "<bucket-relative prefix>/" or raises AdapterRefusal("no_catalog_row")
    def list_partitions(self, prefix) -> list                       # sorted partition ids (dates as YYYY-MM-DD strings), oldest first
    def newest_partition(self, prefix, as_of=None) -> str | None    # newest partition at or before as_of (default: newest)
    def read_rows(self, prefix, partition, columns=None, filters=None) -> list   # list of dict rows of ONE partition (all parts of that partition: the newest part per partition only)
    def freshness_td(self, partition_date) -> int                   # trading days behind the T-1 frontier (lib/trading_calendar.py)
    def firm_segments(self, vendor, firm) -> list                   # the key segments the firm may read for this vendor (the fence), from the contract
```

`read_rows` reads ONE partition only: the adapter never sums partitions (contract decision 3) unless the contract says a table is an event file read over a window, in which case the adapter loops `list_partitions` itself and says so in `_denominator`.

## The fake `ctx` every adapter test starts from (copy it into your own test file; do not import it)

```python
class FakeCtx:
    """In-memory ctx: tables = {(vendor, segment, layer, table): {partition: [row dicts]}}."""
    def __init__(self, tables, frontier="2026-10-13", segments=None, lag=None):
        self.tables, self.frontier, self.segments, self.lag, self.reads = tables, frontier, segments or {}, lag or {}, []
    def prefix(self, vendor, segment, layer, table):
        key = (vendor, segment, layer, table)
        if key not in self.tables:
            raise AdapterRefusal("no_catalog_row")
        return "%s/%s/%s/%s/" % key
    def _t(self, prefix):
        v, s, l, t = prefix.rstrip("/").split("/")
        return self.tables[(v, s, l, t)]
    def list_partitions(self, prefix):
        return sorted(self._t(prefix))
    def newest_partition(self, prefix, as_of=None):
        ps = [p for p in self.list_partitions(prefix) if as_of is None or p <= as_of]
        return ps[-1] if ps else None
    def read_rows(self, prefix, partition, columns=None, filters=None):
        self.reads.append((prefix, partition))
        rows = self._t(prefix).get(partition, [])
        for k, v in (filters or {}).items():
            rows = [r for r in rows if r.get(k) == v]
        return [dict(r) for r in rows]
    def freshness_td(self, partition_date):
        return self.lag.get(partition_date, 0)
    def firm_segments(self, vendor, firm):
        return self.segments.get((vendor, firm), [])
```

(`AdapterRefusal` is the class of the adapter module under test.) Every adapter test file asserts, at minimum: the contract's own refusal arms for that vendor, the fence negative arm (a request for one firm reads zero rows of another firm's segment: assert `ctx.reads` names only that firm's segments), that a snapshot table is read from ONE partition, and that no returned key or body field carries a full account number (only the masked `account_ref`).

## Privacy line every cell obeys

Client data is Opal-principal-only and client-derived: never print a row, an account number, a person's name or an amount into a report, a row, a log or a message. Probes print COUNTS and booleans only. Client data never reads through `gateway-global-internal-reader-role` (PRD v3.2); an adapter's S3 client comes from `ctx` (the core builds it from the vendor's own role; the probe runs with the box's credentials).
