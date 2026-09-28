"""AC1 -- HVST-z-2: STATE THE MAPPING BEFORE COUNTING ANYTHING.

Prints FWD-4's DONE WHEN clause (i) verbatim, as read live from the PRD bytes (never from a
paraphrase). For each of the six ratified facts in that clause, names the GOLD_MENTION_SCHEMA
column that carries it -- read from the schema object itself (`publication_gold.GOLD_MENTION_SCHEMA`),
never from the task order's table -- or reports it ABSENT with where the fact actually lives.

`share` is checked separately: C-HV-ABSOLUTE-ONLY bars a ratio from gold, so `share` is EXPECTED
ABSENT from the schema and must be reported as contract-compliant, never as a missing/gap field.

READ-ONLY: imports the schema object (a module-level constant, no I/O) and reads the PRD file off
disk. No S3 call, no write, no vendor call.
"""

import json
import os
import sys


def _ensure_repo_root_on_path():
    """Walk up from this file's own directory to the first ancestor carrying both `lib/` and
    `.tools/` -- the invocation is `python <this file>` with no `cd` and no PYTHONPATH set."""
    here = os.path.abspath(os.path.dirname(__file__))
    path = here
    for _ in range(15):
        if os.path.isdir(os.path.join(path, "lib")) and os.path.isdir(os.path.join(path, ".tools")):
            if path not in sys.path:
                sys.path.insert(0, path)
            return path
        parent = os.path.dirname(path)
        if parent == path:
            break
        path = parent
    raise RuntimeError("_ensure_repo_root_on_path: no ancestor of %r carries both lib/ and .tools/" % (here,))


REPO_ROOT = _ensure_repo_root_on_path()

import lib.research.harvest.publication_gold as pg  # noqa: E402

PRD_PATH = os.path.join(
    REPO_ROOT, "org", "missions", "D5", "AMGT", "AMGT_HARVST", "prd", "AMGT_HARVST_PRD.md"
)


def read_prd_clause_i():
    """Reads the PRD off disk (live bytes) and returns the FWD-4 block verbatim, split into the
    DONE WHEN clause (i) text and the ACCEPT/SOURCE lines that follow it, plus the raw line range
    used so the read is checkable."""
    with open(PRD_PATH, "r", encoding="utf-8") as f:
        lines = f.readlines()

    start_idx = None
    for i, line in enumerate(lines):
        if line.strip().startswith("FWD-4 "):
            start_idx = i
            break
    if start_idx is None:
        raise RuntimeError("read_prd_clause_i: no 'FWD-4' block found in %r" % (PRD_PATH,))

    # FWD-4's block runs from its own line to (but not including) the next 'FWD-' line.
    end_idx = start_idx + 1
    while end_idx < len(lines) and not lines[end_idx].strip().startswith("FWD-5"):
        end_idx += 1

    block_lines = lines[start_idx:end_idx]
    block_text = "".join(block_lines)

    # Extract the DONE WHEN paragraph specifically (up to ACCEPT).
    done_when_lines = []
    in_done_when = False
    for line in block_lines:
        stripped = line.strip()
        if stripped.startswith("DONE WHEN"):
            in_done_when = True
        if stripped.startswith("ACCEPT"):
            break
        if in_done_when:
            done_when_lines.append(line)
    done_when_text = "".join(done_when_lines)

    return {
        "prd_path": os.path.relpath(PRD_PATH, REPO_ROOT).replace("\\", "/"),
        "prd_line_range_1indexed": [start_idx + 1, end_idx],
        "fwd4_block_verbatim": block_text,
        "done_when_verbatim": done_when_text,
    }


# The two DONE WHEN clauses are joined by "; the grade is re-derived..." -- clause (i) is the
# EXERCISED list of carried facts up to that semicolon; clause (ii) (re-derivation matching) is
# HVST-y-2's, not this cell's.
CLAUSE_I_SEPARATOR = "; the grade is re-derived"


def split_clauses(done_when_verbatim):
    normalized = " ".join(done_when_verbatim.split())
    idx = normalized.find(CLAUSE_I_SEPARATOR.replace("\n", " "))
    if idx == -1:
        return normalized, None
    clause_i = normalized[:idx].strip()
    clause_ii = normalized[idx + 2:].strip()  # drop leading '; '
    return clause_i, clause_ii


# The six ratified facts named in clause (i), in the order the PRD states them, each paired with
# the GOLD_MENTION_SCHEMA column name to be VERIFIED against the schema object below (never
# assumed true because it is written here).
RATIFIED_FACTS = [
    ("in the headline", "mention_in_title"),
    ("in the opening", "mention_in_lead"),
    ("how often it is named", "mention_count"),
    ("how much of the article names it", ["blocks_hit", "blocks_total"]),
    ("which other covered companies it names", "co_mentioned_securities"),
    ("a strength grade", "signal_tier"),
]


def main():
    prd_read = read_prd_clause_i()
    clause_i, clause_ii = split_clauses(prd_read["done_when_verbatim"])

    schema_field_names = list(pg.GOLD_MENTION_SCHEMA.names)
    schema_field_types = {name: str(pg.GOLD_MENTION_SCHEMA.field(name).type) for name in schema_field_names}

    mapping_rows = []
    all_mapped_columns = []
    unmapped_facts = []
    for fact, expected_cols in RATIFIED_FACTS:
        cols = expected_cols if isinstance(expected_cols, list) else [expected_cols]
        present = [c for c in cols if c in schema_field_names]
        absent = [c for c in cols if c not in schema_field_names]
        if absent:
            unmapped_facts.append({"fact": fact, "expected_columns": cols, "absent_columns": absent})
            status = "ABSENT" if not present else "PARTIAL"
        else:
            status = "MAPPED"
            all_mapped_columns.extend(cols)
        mapping_rows.append({
            "ratified_fact": fact,
            "gold_mention_schema_column(s)": cols,
            "status": status,
            "column_types": {c: schema_field_types.get(c) for c in cols},
        })

    # `share` -- EXPECTED ABSENT by C-HV-ABSOLUTE-ONLY, checked against the live schema object,
    # never assumed and never reported as a gap.
    share_present = "share" in schema_field_names
    share_finding = {
        "column": "share",
        "present_in_schema": share_present,
        "expected": "ABSENT",
        "reason": "C-HV-ABSOLUTE-ONLY bars a ratio from gold; share is computed at serve time from blocks_hit/blocks_total",
        "contract_compliant": (share_present is False),
    }

    other_absent_facts = [row for row in mapping_rows if row["status"] != "MAPPED"]
    closable = len(other_absent_facts) == 0

    out = {
        "prd_read": prd_read,
        "fwd4_clause_i_verbatim": clause_i,
        "fwd4_clause_ii_verbatim": clause_ii,
        "gold_mention_schema_field_count": len(schema_field_names),
        "gold_mention_schema_fields": schema_field_names,
        "gold_mention_schema_field_types": schema_field_types,
        "ratified_fact_to_column_mapping": mapping_rows,
        "unmapped_facts": unmapped_facts,
        "share_column_finding": share_finding,
        "verdict": (
            "clause (i) IS CLOSABLE by a census of this table -- column set: %s"
            % ", ".join(all_mapped_columns)
            if closable else
            "clause (i) is NOT CLOSABLE by a census of this table -- unmapped facts: %s"
            % ", ".join(row["ratified_fact"] for row in other_absent_facts)
        ),
    }
    print(json.dumps(out, indent=2, sort_keys=False, default=str))


if __name__ == "__main__":
    main()
