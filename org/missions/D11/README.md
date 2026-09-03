# D11 -- a DIRECTIVE level of the project tree (pointers only; nothing here is a carrier)

This folder is one level of `org/missions/D{n}/{MACRO}/{PROJECT}/`. Every fact about it lives in DATA
a gate reads; this file only says where.

| what | the ONE carrier |
|---|---|
| the directive itself (title, placement, members, stance) | `org/missions/DIRECTIVES.yaml` -> `directives.D11` |
| which macro folders may exist under it, and whether the enum is RATIFIED | `org/missions/MACROS.yaml` -> `directives.D11` |
| the folder contract, regexes, refusal ids, index shape | `org/standards/PROJECT_TREE.contract.json` |
| the validator (runs on every commit that stages a tree or register path) | `python .tools/missions-tree-index.py check` |

A project folder here is `{MACRO}_{NAME}` with a `project.json`; its flat index entry
`org/projects/{PROJECT_CODE}.json` is GENERATED (`derive --write`), never hand-edited.
Do not copy any value from those carriers into this file.
