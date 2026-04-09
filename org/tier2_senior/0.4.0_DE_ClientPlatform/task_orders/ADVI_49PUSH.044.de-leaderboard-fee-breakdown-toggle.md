<task_order>
  <metadata>
    <id>0.4.0_DE_ClientPlatform-2026-04-09-49push-044-de</id>
    <issued_by>0.4.0_DS_ClientPlatform</issued_by>
    <issued_to>0.4.0_DE_ClientPlatform</issued_to>
    <date>2026-04-09</date>
    <status>complete -- toggle implemented (portal DEV ffc13f7); PlatinumFeeBreakdown type added; auto-switch NNA->AUA on No-Fee</status>
    <project_code>ADVI_49PUSH</project_code>
    <wave>11</wave>
    <phase>Leaderboard fee breakdown toggle</phase>
  </metadata>

  <objective>
    Add a "Fee View" toggle to the Leaderboard panel in the Advisors tab.
    DS (0024b53c) ships fee_breakdown on every leaderboard entry with two buckets:
    fee_paying and no_fee. The toggle lets the user slice the leaderboard by fee tier.
  </objective>

  <data_contract>
    DS schema (0024b53c, deployed):
    "fee_breakdown": {
      "fee_paying": { "aua": number, "account_count": number, "nna": number, "inflows": number, "outflows": number },
      "no_fee":     { "aua": number, "account_count": number, "nna": 0,      "inflows": 0,      "outflows": 0      }
    }

    DS caveats:
    1. client_count inside fee_breakdown is 0 for both buckets (join not wired yet) — hide client_count
       column entirely when any fee-breakdown toggle is active.
    2. no_fee.nna/inflows/outflows = 0 — NNA metric toggle is meaningless for No-Fee view.
       Show NNA column as "--" (not 0) when fee_view = 'no_fee'.
  </data_contract>

  <fix_1 label="Add types">
    portal/src/pages/AdvisorIntelligence/types.ts:

    export interface PlatinumFeeBreakdown {
      aua: number
      account_count: number
      nna: number
      inflows: number
      outflows: number
    }

    Add to PlatinumLeaderboardEntry:
      fee_breakdown?: {
        fee_paying: PlatinumFeeBreakdown
        no_fee: PlatinumFeeBreakdown
      }
  </fix_1>

  <fix_2 label="Add Fee View toggle to Leaderboard panel header">
    In AdvisorsTab.tsx, add a FeeView state:
      type FeeView = 'all' | 'fee_paying' | 'no_fee'
      const [feeView, setFeeView] = useState<FeeView>('all')

    Toggle group in the Leaderboard panel header (variant="secondary"):
      All | Fee-Paying | No Fee

    Place it to the left of the existing metric toggle (AUA | NNA | GRO).
    Reset to 'all' when the period changes.
  </fix_2>

  <fix_3 label="Apply fee_breakdown filter to display metrics">
    In the leaderboard rendering pipeline, when feeView !== 'all':
    - For each entry, use fee_breakdown[feeView].aua instead of entry.total_aua
    - Use fee_breakdown[feeView].nna / inflows / outflows for NNA metric
    - aua_growth_pct: recompute as (fee_bucket_aua - period_start_fee_aua) / period_start_fee_aua
      OR display "--" if period_start unavailable for the bucket (safe default)
    - new_clients: show entry.new_clients (not bucket-specific, client-level join pending)
    - Hide client_count display in Top Performers cards and leaderboard rows when feeView !== 'all'

    When feeView = 'no_fee':
    - NNA column shows "--" (not $0) since no_fee NNA is not tracked
    - NNA metric toggle should be disabled (greyed out) with tooltip:
      "No-fee NNA tracking pending data pipeline work"
  </fix_3>

  <fix_4 label="Sort and rank under fee view">
    The leaderboard sort (AUA desc default) should use the fee-bucket AUA when feeView !== 'all'.
    The rank badge number should reflect the fee-bucket ranking, not the total AUA ranking.
    rank_delta: compute from fee_bucket period_start_aua if available, else hide (show --).
  </fix_4>

  <acceptance_criteria>
    1. Toggle renders in Leaderboard header: All | Fee-Paying | No Fee
    2. Switching to Fee-Paying shows fee_paying.aua in AUA column and re-ranks accordingly
    3. Switching to No Fee shows no_fee.aua and shows "--" for NNA
    4. client_count field hidden from display when feeView !== 'all'
    5. NNA metric toggle disabled with tooltip in No-Fee view
    6. "All" (default) behavior unchanged
    7. Build clean, no TypeScript errors
  </acceptance_criteria>

  <compiler_tools>
    comp-transform schema-check AdvisorsTab
      -- Run after adding fee_breakdown to PlatinumLeaderboardEntry. Confirms
         fee_breakdown fields flow through to rendered JSX. Catches UNUSED fields.

    comp-cache key advisor-intelligence leaderboard
      -- Confirm leaderboard cache key. Fee view is local state (no refetch needed)
         but verify the key doesn't need to include feeView for correctness.
  </compiler_tools>

</task_order>
