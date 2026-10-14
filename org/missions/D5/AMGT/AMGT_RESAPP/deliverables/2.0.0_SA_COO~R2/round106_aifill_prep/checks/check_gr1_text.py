"""check_gr1_text.py -- acceptance arms for AMGT-gr-1 (whole text: real sentence ends, and answer segments joined with a space).

  PYTHONPATH=<repo root> python check_gr1_text.py
Offline. Imports lib.research.aifill.sentences (new) and lib.research.aifill.model.parse_response. The defects (CVO C-S143/C-S146, measured on the stored documents):
a block ended mid-sentence on `... totaling Ps.` because the cut took the abbreviation `Ps.` for a sentence end, and 14 places over 7 blocks read `2022.She has served` because
two answer text blocks were joined with no space.
"""
from __future__ import annotations

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import aifill_check_lib as L  # noqa: E402

KOF = ("Kof reported results for the year. The board proposed a 2025 ordinary dividend of Ps. 7.36 per unit, totaling Ps. 15.5 billion, payable in two instalments. "
       "Management expects a recovery in Mexico next year.")


def main():
    from lib.research.aifill import sentences as S

    arms = L.Arms("GR-1")
    sp = S.split_sentences

    arms.run("split: two plain sentences", lambda: (sp("He joined in 2008. She left in 2012.") == ["He joined in 2008.", "She left in 2012."], sp("He joined in 2008. She left in 2012.")))
    arms.run("split: 'Ps. 7.36' and 'Ps. 15.5' are not ends (one sentence)", lambda: (len(sp("The dividend is Ps. 7.36 per unit, totaling Ps. 15.5 billion.")) == 1, sp("The dividend is Ps. 7.36 per unit, totaling Ps. 15.5 billion.")))
    arms.run("split: the KOF text is three sentences", lambda: (len(sp(KOF)) == 3, [s[:30] for s in sp(KOF)]))
    arms.run("split: company suffix then lowercase is not an end", lambda: (len(sp("Apple Inc. announced a deal. It grew.")) == 2, sp("Apple Inc. announced a deal. It grew.")))
    arms.run("split: company suffix then a capital IS an end", lambda: (sp("He runs Apple Inc. The firm grew.") == ["He runs Apple Inc.", "The firm grew."], sp("He runs Apple Inc. The firm grew.")))
    arms.run("split: titles and St. are not ends", lambda: (len(sp("Dr. Smith joined St. Louis Co. in 2010.")) == 1, sp("Dr. Smith joined St. Louis Co. in 2010.")))
    arms.run("split: initials are not ends", lambda: (len(sp("J. P. Morgan hired him in 2001.")) == 1, sp("J. P. Morgan hired him in 2001.")))
    arms.run("split: U.S. before a lowercase word is not an end", lambda: (len(sp("The U.S. economy grew. Rates fell.")) == 2, sp("The U.S. economy grew. Rates fell.")))
    arms.run("split: decimals are not ends", lambda: (len(sp("Growth was 7.36% in Q1. Next quarter looks better.")) == 2, sp("Growth was 7.36% in Q1. Next quarter looks better.")))
    arms.run("split: ! and ? end a sentence", lambda: (len(sp("Is it true? Yes! It is.")) == 3, sp("Is it true? Yes! It is.")))
    arms.run("split: a closing quote after the mark still ends it", lambda: (len(sp('He said "we grew." Then he left.')) == 2, sp('He said "we grew." Then he left.')))
    arms.run("split: an abbreviation at the very end is the end", lambda: (sp("He is chair of the subsidiary AIA Co.")[-1].endswith("AIA Co."), sp("He is chair of the subsidiary AIA Co.")))
    arms.run("split: empty and whitespace give no sentences", lambda: (sp("") == [] and sp("   ") == [], "ok"))

    def coverage():
        for text in (KOF, "He joined in 2008.  She left.\nThen came Dr. Lee.", "One sentence only"):
            if " ".join(sp(text)).split() != text.split():
                return False, text[:40]
        return True, "words preserved"
    arms.run("split: no word is lost or reordered", coverage)

    cut = S.cut_at_sentence_end
    arms.run("cut: text within the cap is returned unchanged", lambda: (cut("Short text. Fine.", 100) == "Short text. Fine.", cut("Short text. Fine.", 100)))

    def cut_kof():
        cap = KOF.index("Ps. 15.5") + len("Ps.") + 4
        got = cut(KOF, cap)
        return got is not None and got == "Kof reported results for the year." and not got.rstrip().endswith("Ps."), got
    arms.run("cut: never leaves 'Ps.' as the ending (the KOF defect)", cut_kof)

    def cut_last_fit():
        cap = len(KOF) - 5
        got = cut(KOF, cap)
        return got is not None and got.endswith("payable in two instalments."), got
    arms.run("cut: takes the LAST real end that fits", cut_last_fit)
    arms.run("cut: None when no real end fits", lambda: (cut("A very long opening clause with no stop at all and then Ps. 7 more words", 30) is None, cut("A very long opening clause with no stop at all and then Ps. 7 more words", 30)))
    arms.run("cut: the cut text is itself whole sentences", lambda: (sp(cut(KOF, 120)) == sp(KOF)[:len(sp(cut(KOF, 120)))], cut(KOF, 120)))

    join = S.join_segments
    arms.run("join: sentence end then a capital gets one space", lambda: (join(["board since February 2022.", "She has served as chair."]) == "board since February 2022. She has served as chair.", join(["board since February 2022.", "She has served as chair."])))
    arms.run("join: text already spaced is unchanged", lambda: (join(["revenue rose ", "5%."]) == "revenue rose 5%." and join(["It grew.", " Then it fell."]) == "It grew. Then it fell.", "ok"))
    arms.run("join: a closing quote or bracket then a capital gets a space", lambda: (join(['He said "yes."', "Then left"]) == 'He said "yes." Then left' and join(["(see note.)", "Next"]) == "(see note.) Next", "ok"))
    arms.run("join: a name split across blocks is not spaced", lambda: (join(["Nestl", "e SA"]) == "Nestle SA" and join(["Nestle", " SA"]) == "Nestle SA", join(["Nestl", "e SA"])))
    arms.run("join: a decimal split across blocks is not spaced", lambda: (join(["rose 7.", "36 percent"]) == "rose 7.36 percent", join(["rose 7.", "36 percent"])))
    arms.run("join: empty and None parts are ignored", lambda: (join(["A.", "", None, "B"]) == "A. B", join(["A.", "", None, "B"])))

    def seam():
        from lib.research.aifill import model

        resp = {"id": "m", "type": "message", "role": "assistant", "model": "claude-opus-5", "stop_reason": "end_turn",
                "content": [{"type": "text", "text": "She joined the board in February 2022."}, {"type": "text", "text": "She has served as chair since."}],
                "usage": {"input_tokens": 10, "output_tokens": 10}}
        got = model.parse_response(resp)
        return got.text == "She joined the board in February 2022. She has served as chair since.", got.text
    arms.run("seam: parse_response joins the final segments with a space", seam)

    def seam_recorded():
        from lib.research.aifill import model

        got = model.parse_response(L.web_response()["response"] if "response" in L.web_response() else L.web_response())
        return got.text.strip() != "" and ".A" not in got.text and ".T" not in got.text, got.text[:80]
    arms.run("seam: the recorded real response still parses, no joined sentence", seam_recorded)

    def ascii_src():
        src = open(S.__file__, "rb").read()
        return src.isascii() and b"import boto3" not in src and b"import urllib" not in src, "non-ASCII or network import"
    arms.run("the module is ASCII, stdlib only, no network", ascii_src)

    return arms.finish()


if __name__ == "__main__":
    sys.exit(main())
