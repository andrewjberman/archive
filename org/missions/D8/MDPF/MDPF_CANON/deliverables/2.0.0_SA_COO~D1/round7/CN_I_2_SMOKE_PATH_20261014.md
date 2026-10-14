# CN-i-2: what to open and click (Andrew's look at the repaired candidate), 2.0.0_SA_COO~D1, 2026-10-14

**URL:** http://localhost:5174/ on dell1. The server is `bun run dev:live --port 5174` from a portal worktree on `cand/dell1/mdpf-canon-aua-trend-groups-repair`, head **fd5433a3a76cb8b2f05b986220b70925a9f12ed3** (its served source was read: it carries the repair and the as-of helper). Sign in normally, including MFA; it reads the live services. Open **Model Portfolios** (`/portfolios`), partner **Global (All)**.

1. **The Trend and its colours.** In the Model Overview card, click **Trend**. The legend should read: the five models, **Custom Models** (fuchsia), **Other AUA** (grey), **Client Supervised** (gold), **Client Unsupervised** (lime, no longer orange), **ETF Strategies** (cyan), **ALT Strategies** (vermilion). Client Unsupervised should not look like Ultra Short-Term.
2. **The boundary text.** Under the Trend subtitle: "Per-model detail begins May 15, 2026; earlier model assets are in the Total and are not broken out." Before about May 2026 the bars and the daily area are the grey Other AUA only; nothing is drawn for the model dollars there (the CTO's ruling).
3. **The tooltip on a pre-2026-05-15 date.** Hover the DAILY chart in its left two thirds (for example around 2025-08). The tooltip should list the Other AUA and the total, no Client row, no $0 row.
4. **The tooltip on a date that used to print a $0 Client row.** Hover the daily chart on a recent date that has no dated category-views object (for example mid-September 2026). Before the repair the tooltip printed a Client row of $0; now it should print no Client row. A Client row appears only on the dates that have a category-views object (the latest dates).
5. **Total Assets, the one change outside the Trend.** At the top, click the **Client** card. The drill-down shows **Client - Opal Unsupervised** with a **lime** dot and a lime bar (it was orange). The shared colour table moves it everywhere.
6. **The Other Models "as of".** It will NOT show today: the pool is present, so no value is carried and no stamp is drawn. It appears only on a day with no pool; this smoke cannot show it.

When you are done, tell me and I stop the server (the port is the one dev port on the box).
