This is a re-run of a previous alignment thread that produced low-quality contracts. Three specific gaps must be resolved this time:
(1) cla_timeseries must include geo_drill (city-level drill within each state) -- it was missing from ADVI-001 despite being required by the PRD.
(2) colorMap values must be actual portal color token names or hex values from the existing portal color system -- not placeholder strings like '#green'. RD: read DistributionTab.tsx to confirm what color tokens are in use.
(3) The NMNC/NMEC 12-month window rule proposed in ADVI-001 was not verified against the existing header_metrics.json CLA structure. DS must confirm how NMNC/NMEC is defined in the current gold layer output, not assume it.
