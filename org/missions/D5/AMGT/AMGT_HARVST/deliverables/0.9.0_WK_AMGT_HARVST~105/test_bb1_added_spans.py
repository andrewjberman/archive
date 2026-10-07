"""HVST-bb-1 AC2: planted-article tests of the ADDED definition (no network)."""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import bb1_census as C  # noqa: E402

META = ["Meta Platforms", "Facebook"]
LLY = ["Eli Lilly", "Lilly & Co"]


def art(title="", blocks=()):
    return {"article_key": "x:1", "title": title, "text_blocks": list(blocks)}


def test_title_meta_one_added_new_pair():
    r = C.added_for(art("Meta rallies"), META, [], "Meta")
    assert len(r["hits"]) == 1 and r["base_count"] == 0 and r["title_flip"]


def test_meta_platforms_longer_alias_takes_span():
    r = C.added_for(art("x", ["Meta Platforms rose"]), META, [], "Meta")
    assert r["hits"] == []


def test_word_bounded():
    r = C.added_for(art("metadata and Metaverse", ["metadata Metaverse"]), META, [], "Meta")
    assert r["hits"] == []


def test_lilly():
    assert C.added_for(art("Eli Lilly shares"), LLY, [], "Lilly")["hits"] == []
    assert len(C.added_for(art("Lilly said"), LLY, [], "Lilly")["hits"]) == 1


def test_control_existing_alias_adds_zero():
    r = C.added_for(art("Facebook and Meta Platforms", ["Facebook"]), META, [], "Facebook")
    assert r["hits"] == []
