"""Mutant fixture (item-1b acceptance a): SYNTHETIC SOURCE TEXT carrying assumed
references to a nonexistent table and a nonexistent column on a real table.
Never a DB mutation. The sensor must classify both as orphan."""
MUTANT_QUERY_1 = "MATCH (z:ZzzNoSuchTable9999) RETURN z.anything LIMIT 1"
MUTANT_QUERY_2 = "MATCH (n:CloudNode) WHERE n.zzz_no_such_column_9999 = 'x' RETURN n.name"
