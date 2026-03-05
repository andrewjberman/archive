This is a Pattern 0 pre-implementation alignment thread for the Security Scanner portal page (SSCN_PORTAL). The goal is for DS, AE, and DE to agree on the data architecture BEFORE anyone writes portal code.

The Security Scanner is a port of Yang's Factor_Scanning_Model.xlsm to the portal. Source data is a monthly FactSet Excel export (~3000 securities x 255 factors, 6 universe weight columns). The XLSM audit file is the principal context -- it contains the full workbook structure including all VBA logic, factor metadata, formulas, and conditional formatting that must be replicated in the portal.

Four key decisions must be resolved in this thread:
1. DATA STORAGE: Static JSON in S3 (pre-processed monthly) vs Lambda-computed on demand
2. PERCENTILE SCORING: Pre-computed server-side (in a processing Lambda) vs computed client-side in the browser
3. S3 KEY STRUCTURE: How does monthly FactSet data flow from upload to portal-consumable JSON?
4. API ENDPOINT STRUCTURE: Path, authentication (/api/private vs /api/general), and shape for each of the 4 tabs

DS is the knowledge source for what the FactSet data contains and what the pipeline must produce. AE is the knowledge source for AWS infrastructure decisions (S3, Lambda, EventBridge, IAM). DE is the knowledge receiver who will wire the TypeScript interface and API calls.

Thread output must be a concrete data contract: specific S3 key patterns, exact JSON shapes per endpoint, TypeScript interface names, and a refresh schedule. Vague answers are not acceptable -- every answer must cite a specific file, resource name, or column name from the context.
