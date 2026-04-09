<task_order>
  <metadata>
    <id>1.0.0_SA_CTO-2026-04-09-49push-043-de</id>
    <issued_by>1.0.0_SA_CTO</issued_by>
    <issued_to>0.4.0_DE_ClientPlatform~A</issued_to>
    <date>2026-04-09</date>
    <status>complete -- rank delta column implemented (portal DEV 3588971); DS .042 done (10df0f0f); comp-transform PASS; no cache collisions</status>
    <project_code>ADVI_49PUSH</project_code>
    <wave>10</wave>
    <phase>Advisors tab rank delta UI</phase>
    <mcp_identity>Register with MCP as "0.4.0_DE_ClientPlatform" before starting.</mcp_identity>
  </metadata>

  <objective>
    Add a RANK column to the Advisors tab leaderboard showing each advisor's rank
    change since the period start. Display as an up/down icon + number colored
    green (rose) or red (fell). Appears as the last column after "New Clients".
  </objective>

  <context>
    File: portal/src/pages/AdvisorIntelligence/tabs/AdvisorsTab.tsx

    Rank delta logic:
      current_rank  = position in entries[] sorted by total_aua descending (1-indexed)
      start_rank    = position in entries[] sorted by period_start_aua descending (1-indexed)
      rank_delta    = current_rank - start_rank
        negative → advisor moved UP (current rank # is lower = better position)
        positive → advisor moved DOWN (current rank # is higher = worse position)
        zero     → no change

    Display:
      rank_delta < 0:  ↑ {|rank_delta|}  green   (e.g. ↑ 3)
      rank_delta > 0:  ↓ {rank_delta}    red     (e.g. ↓ 10)
      rank_delta = 0:  —                 white/30 (em dash, neutral)
      period_start_aua = null: —         white/30 (new advisor, no history)

    Rank is always computed relative to AUA, regardless of the active metric toggle
    (AUA/NNA/GRO). AUA rank is the primary standing metric.
  </context>

  <fix_1 label="Add period_start_aua to PlatinumLeaderboardEntry type">
    <description>
      In portal/src/pages/AdvisorIntelligence/types.ts, add to PlatinumLeaderboardEntry:
        period_start_aua?: number | null
      Optional because newly active advisors may have null.
    </description>
  </fix_1>

  <fix_2 label="Compute rank delta for all entries">
    <description>
      In AdvisorsTab.tsx, after the entries array is derived for the active window,
      compute ranks and deltas in a useMemo:

        const entriesWithRank = useMemo(() => {
          // current rank: sort by total_aua desc, assign 1-indexed position
          const byCurrentAua = [...entries].sort((a, b) => b.total_aua - a.total_aua)
          const currentRankMap = new Map(byCurrentAua.map((e, i) => [e.advisor_id, i + 1]))

          // start rank: sort by period_start_aua desc, skip nulls (they go to end)
          const byStartAua = [...entries].sort((a, b) => {
            if (a.period_start_aua == null) return 1
            if (b.period_start_aua == null) return -1
            return b.period_start_aua - a.period_start_aua
          })
          const startRankMap = new Map(byStartAua.map((e, i) => [e.advisor_id, i + 1]))

          return entries.map(e => ({
            ...e,
            current_rank:  currentRankMap.get(e.advisor_id) ?? null,
            start_rank:    e.period_start_aua != null ? startRankMap.get(e.advisor_id) ?? null : null,
            rank_delta:    (currentRankMap.get(e.advisor_id) != null && e.period_start_aua != null)
                             ? (currentRankMap.get(e.advisor_id)! - (startRankMap.get(e.advisor_id) ?? 0))
                             : null,
          }))
        }, [entries])

      Use entriesWithRank wherever the leaderboard list is rendered.
    </description>
  </fix_2>

  <fix_3 label="Render RANK column in leaderboard list">
    <description>
      The leaderboard list (LeaderboardCards component or equivalent) currently shows
      columns: Name | AUA | NNA | GRO | New Clients

      Add a final column: RANK

      Column header: "RANK" (same style as other headers, uppercase, white/50, text-xs)

      Cell render for each entry:
        const delta = entry.rank_delta

        if delta === null:
          render: <span className="text-white/30 text-xs">—</span>

        if delta === 0:
          render: <span className="text-white/30 text-xs">—</span>

        if delta < 0:  (moved UP -- lower rank number = better)
          render:
            <span className="flex items-center gap-0.5 text-emerald-400 text-xs font-medium">
              <ArrowUp size={11} />
              {Math.abs(delta)}
            </span>

        if delta > 0:  (moved DOWN -- higher rank number = worse)
          render:
            <span className="flex items-center gap-0.5 text-red-400 text-xs font-medium">
              <ArrowDown size={11} />
              {delta}
            </span>

      Use ArrowUp and ArrowDown from lucide-react (already imported for other icons).

      Column width: narrow, ~48px. The number rarely exceeds 3 digits.
      Align right like the other numeric columns.

      The column updates automatically when the period toggle changes (QTD/YTD/1Y/Max)
      because the entries array is sourced from the active window data.
    </description>
  </fix_3>

  <fix_4 label="RANK in bar chart tooltip (optional enhancement)">
    <description>
      In the AUA bar chart tooltip (.039 fix_2), consider adding a "Rank" line:
        Rank    #{current_rank}  (▲3 since period start)
      This gives full context in the hover without requiring the user to look at the list.
      Only implement if it fits cleanly in the tooltip layout. Skip if it makes the
      tooltip feel crowded -- the list column is sufficient.
    </description>
  </fix_4>

  <acceptance_criteria>
    1. RANK column appears as the last column in the leaderboard list
    2. Up arrow + number in emerald-400 for advisors who rose in AUA rank
    3. Down arrow + number in red-400 for advisors who fell
    4. Em dash in white/30 for no change or new advisors (null period_start_aua)
    5. Rank delta is consistent: sum of rises and falls across all advisors = 0
       (same people, same pool -- total rank movements cancel out)
    6. Column responds correctly when period toggle switches QTD ↔ YTD ↔ 1Y
    7. PlatinumLeaderboardEntry type updated with period_start_aua?: number | null
    8. Build clean, no TypeScript errors
  </acceptance_criteria>


  <compiler_tools>
    comp-transform schema-check AdvisorsTab
      -- Run after adding period_start_aua to PlatinumLeaderboardEntry and wiring
         rank_delta to JSX. Confirms the field flows from type definition to rendered
         output and is not stuck as UNUSED. Also catches if any existing field
         accidentally became orphaned during the type update.

    comp-cache key advisor-intelligence leaderboard
      -- Confirms the leaderboard React Query key. When the window toggle changes
         (QTD → YTD), the cache must bust and re-fetch so rank deltas recompute
         against the correct window's period_start_aua. Run to verify the key
         includes the window/period so stale rank deltas don't persist.
  </compiler_tools>

</task_order>
