# D11 / NFRA -- a MACRO level of the project tree (pointers only; nothing here is a carrier)

`NFRA` is a namespace, not a project: it has a charter and a folder per directive it appears in, never
a status or a DONE (spec s.5a). Every fact about it lives in DATA a gate reads; this file only says where.

| what | the ONE carrier |
|---|---|
| the macro's one-line charter | `org/missions/MACROS.yaml` -> `charters.NFRA` |
| whether `NFRA` is a ratified macro under D11 (and Andrew's verbatim) | `org/missions/MACROS.yaml` -> `directives.D11.macros` / `.ratification` |
| the projects registered under it | the `{PROJECT_CODE}/project.json` folders beside this file, and `org/missions/DIRECTIVES.yaml` -> `directives.D11.members.projects` |
| the folder contract and the validator | `org/standards/PROJECT_TREE.contract.json`; `python .tools/missions-tree-index.py check` |

Do not copy any value from those carriers into this file.
