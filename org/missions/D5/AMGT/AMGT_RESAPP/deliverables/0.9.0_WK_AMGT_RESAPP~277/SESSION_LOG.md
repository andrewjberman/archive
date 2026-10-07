# 0.9.0_WK_AMGT_RESAPP~277 -- AMGT-ba-11 session log

Code commit 8c0c6de8c56630370dc85f3452549b64e9a02d83. Hookups 1-8 done; see the worker report.

build_pack caller census (word-boundary search of lib/ and the rest of the repo outside portal/ and org/missions/):
- lib/research/api/scoped_amgt.py `_print_pack` (the served route): now passes write_text=False; reads the PDF only.
- lib/research/print/render_pack.py `main` (CLI at the file's end): uses txt_path in its printed line; default keeps the text.
- tests reading txt_path: print/tests/test_ay1_dated_figures_and_served_thesis.py, test_ax4_brand_form.py, test_av2_export_equals_page.py, test_build_rich_text.py (sha256 of txt), api/tests/test_print_fiscal_year_sort.py (asserts txt_path exists); all use the default.
- tests calling build_pack for the PDF only: print/tests/test_aw2_print_as_document.py, api/tests/test_print_format_rich.py.
- api/tests/test_print_fiscal_year_sort.py `fake_build_pack` stub: now accepts **kw.
- NOT the same function: lib/research/posture/packs.py build_pack (posture pack, called by posture/judge.py and identity/tests/test_slash_safe_key_sites.py).
- Mentions only (no call): infra/aws/terraform/harvest/build_print_deps_layer.py (comments), integrations/bloomberg/research/tests/test_unresolved_overlay_renders_marked.py (comment).
No reader of txt_path outside lib/research/print and lib/research/api tests.

PULL_ENQUEUE_ROUTE / PULL_QUEUE_NAME census: read only by the removed /refresh branch (lib/ and infra/ searched); removed.
