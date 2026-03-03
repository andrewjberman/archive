This is a Pattern 0 pre-implementation alignment thread for two interface-dependent work streams in the AdvisorIntelligence completion PRD.

Stream A1: adv_drill — The publisher Lambda needs to generate per-architect NNA time series (analogous to the existing geo_drill per-city series). This does NOT yet exist. DS must describe what advisor/client-level NNA data is currently available in the gold layer and what an adv_drill output can realistically look like.

Stream A2: cla_timeseries — A new time-series view showing NMNC (new client) vs NMEC (existing client) AUM composition over time. This data does NOT exist anywhere in the current pipeline. DS must describe what classification data (NMNC vs NMEC) is available in the gold layer and what a realistic cla_timeseries output looks like.

Knowledge source: 0.4.0_DS_ClientPlatform (what the gold layer can produce).
Interface specifier: 0.4.0_DE_ClientPlatform (what TypeScript shape the portal needs).
Layout specifier: 0.4.2_RD_AdvisorIntelligence (what the chart component requires from the data).

Deliverable of this thread: agreed JSON output schemas for adv_drill and cla_timeseries, agreed TypeScript interface names and shapes, agreed S3 key patterns. The final turn must contain this as a structured contract. The COO will embed this receipt in the DS and RD task orders as the binding specification.
