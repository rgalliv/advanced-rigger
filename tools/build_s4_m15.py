#!/usr/bin/env python3
"""
Build S4_M15 (Center of Gravity Determination) from the verified S4_M01 source.

Applies the settled decisions:
  1. New module in the existing Stage 4 sequence: S4_M01 -> S4_M15, salt/SKEY/next
     retargeted. Source is read, never written.
  2. Gate size 6 -> 8. Two trailing formative checks are promoted into the gate
     block so the gate stays a contiguous t-gate tail. Bank stays at 25.
  3. review_offset 18 -> 17 (the hardcoded -18 in the review renderer moves too).
  4. Answer key regenerated: no cycle, gate letters exactly 2/2/2/2, gate sequence
     unique platform-wide. Options are permuted so the correct TEXT moves; the
     answer index is re-derived from the text, never carried forward.
  5. ACS coverage map emitted into the manifest.

Deterministic: seeded, no wall-clock, same input -> same output.

Usage: python3 build_s4_m15.py <src_dir> <out_dir>
"""
import json, re, sys, random, html as H
from pathlib import Path

SRC_MOD, NEW_MOD = "S4_M01", "S4_M15"
NEW_SALT = "CQ1:S4_M15_CenterOfGravity"
NEW_GATE_CODE = "R-201C / AR-101C"
NEW_NEXT, NEW_NEXT_LABEL = "S4_M16", "Unequal Leg Loading and Off-Level Pick Points"
REVIEW_OFFSET = 17
GATE_QIDS = [f"{NEW_MOD}_q{i:02d}" for i in range(18, 26)]

# Gate sequences already in use across the platform. The new gate must not match.
KNOWN_GATE_SEQS = {"BDACBD", "ACBDCA", "DABDCA"}

# ACS coverage. Codes renumber with the module: S4.M01.* -> S4.M15.*
# Keyed by question POSITION (1-25) in final slide order.
ITEM_ACS = {
    1: ["S4.M15.K1"], 2: ["S4.M15.K1"], 3: ["S4.M15.K2"], 4: ["S4.M15.K2", "S4.M15.R4"],
    5: ["S4.M15.K6"], 6: ["S4.M15.K6", "S4.M15.R2"], 7: ["S4.M15.K4"], 8: ["S4.M15.K3"],
    9: ["S4.M15.K3", "S4.M15.S1"], 10: ["S4.M15.K5"], 11: ["S4.M15.K5", "S4.M15.R3"],
    12: ["S4.M15.K7"], 13: ["S4.M15.R1"], 14: ["S4.M15.R6"], 15: ["S4.M15.R5"],
    16: ["S4.M15.S2"], 17: ["S4.M15.S3"],
    # gate
    18: ["S4.M15.S1", "S4.M15.K3"], 19: ["S4.M15.K2", "S4.M15.S3"], 20: ["S4.M15.S1"],
    21: ["S4.M15.R3", "S4.M15.K5"], 22: ["S4.M15.R1"], 23: ["S4.M15.S4"],
    24: ["S4.M15.S5", "S4.M15.R5"], 25: ["S4.M15.K6", "S4.M15.S4"],
}
ALL_ACS_CODES = (
    [f"S4.M15.K{i}" for i in range(1, 8)]
    + [f"S4.M15.R{i}" for i in range(1, 7)]
    + [f"S4.M15.S{i}" for i in range(1, 6)]
)


def fnv1a(s: str) -> str:
    h = 0x811C9DC5
    for c in s:
        h ^= ord(c)
        h = (h * 0x01000193) & 0xFFFFFFFF
    return format(h, "08x")


def split_slides(html):
    """Return (prefix, [(idx, block)], suffix)."""
    spans = [(m.start(), m.end(), int(m.group(1)))
             for m in re.finditer(r'<section class="slide[^"]*" id="slide-(\d+)"', html)]
    ends = []
    for i, (s, e, idx) in enumerate(spans):
        stop = spans[i + 1][0] if i + 1 < len(spans) else html.index("</section>", e) + len("</section>")
        ends.append(stop)
    # recompute properly: each slide runs to the start of the next, last to its closing tag
    blocks = []
    for i, (s, e, idx) in enumerate(spans):
        stop = spans[i + 1][0] if i + 1 < len(spans) else html.rindex("</section>") + len("</section>")
        blocks.append((idx, html[s:stop]))
    return html[:spans[0][0]], blocks, html[blocks and (spans[-1][0] + len(blocks[-1][1])):]


def design_key(correct_texts, options_by_pos, seed=20260807):
    """Pick a new correct-index per position satisfying all constraints."""
    rnd = random.Random(seed)
    letters = "ABCD"
    for _ in range(200000):
        # gate: exactly 2 of each letter, no consecutive repeat
        gate = [0, 0, 1, 1, 2, 2, 3, 3]
        rnd.shuffle(gate)
        if any(gate[i] == gate[i - 1] for i in range(1, 8)):
            continue
        if "".join(letters[g] for g in gate) in KNOWN_GATE_SEQS:
            continue
        # head 17 items: distribution must bring the total to 7/6/6/6
        need = [7, 6, 6, 6]
        for g in gate:
            need[g] -= 1
        if min(need) < 0:
            continue
        head = []
        for i, n in enumerate(need):
            head += [i] * n
        rnd.shuffle(head)
        seq = head + gate
        if any(seq[i] == seq[i - 1] for i in range(1, 25)):
            continue
        # anti-cycle: no run of 8+ with constant step mod 4
        bad = False
        for st in range(25 - 7):
            d = (seq[st + 1] - seq[st]) % 4
            if all((seq[st + k + 1] - seq[st + k]) % 4 == d for k in range(7)):
                bad = True
                break
        if bad:
            continue
        return seq
    raise SystemExit("no conforming key found")


def main(src_dir, out_dir):
    src = Path(src_dir); out = Path(out_dir); out.mkdir(parents=True, exist_ok=True)
    html = (src / f"{SRC_MOD}.html").read_text(encoding="utf-8")
    man = json.loads((src / f"{SRC_MOD}_manifest.json").read_text())
    narr = json.loads(re.search(r"var NARR = (\{.*?\});", html, re.S).group(1))
    old_key = man["answer_key"]

    prefix, blocks, _ = split_slides(html)
    by_idx = dict(blocks)

    # --- 1. permute the tail so the gate block is 8 contiguous t-gate slides ---
    # old 44(q17,quiz) 45(content) 46(q18,quiz) 47(divider)
    # new 44=old45 content, 45=old47 divider, 46=old44 quiz->gate, 47=old46 quiz->gate
    order = list(range(1, 44)) + [45, 47, 44, 46] + list(range(48, 55))
    assert sorted(order) == list(range(1, 55)) and len(order) == 54

    # --- 2. renumber qids by new slide order ---
    qslide_old = json.loads(re.search(r"var QSLIDE = (\{.*?\});", html, re.S).group(1))
    slide_of_old_q = {v: int(k) for k, v in qslide_old.items()}
    old_q_at_slide = {int(k): v for k, v in qslide_old.items()}
    q_positions = [s for s in order if s in old_q_at_slide]          # new slide order
    assert len(q_positions) == 25
    oldq_for_pos = [old_q_at_slide[s] for s in q_positions]          # pos-1 -> old qid
    newq_for_pos = [f"{NEW_MOD}_q{i+1:02d}" for i in range(25)]

    # --- 3. extract options and correct text per position ---
    opts, correct_txt = [], []
    for oq in oldq_for_pos:
        found = {}
        for m in re.finditer(
            r"cqAnswer\(this,'%s',(\d+),'[^']*'\)[^>]*>(.*?)</button>" % re.escape(oq), html, re.S
        ):
            found[int(m.group(1))] = m.group(2)
        assert len(found) == 4, oq
        opts.append([found[i] for i in range(4)])
        correct_txt.append(found[old_key[oq]])

    new_idx = design_key(correct_txt, opts)

    # --- 4. permute option order so correct TEXT lands on new index ---
    rnd = random.Random(99991)
    new_opts = []
    for pos in range(25):
        cur, ci = opts[pos], opts[pos].index(correct_txt[pos])
        distract = [o for i, o in enumerate(cur) if i != ci]
        rnd.shuffle(distract)
        arranged, d = [], iter(distract)
        for i in range(4):
            arranged.append(correct_txt[pos] if i == new_idx[pos] else next(d))
        assert arranged[new_idx[pos]] == correct_txt[pos]
        assert sorted(arranged) == sorted(cur)
        new_opts.append(arranged)

    # --- 5. rebuild slide blocks ---
    promoted = {44: 1, 46: 2}   # old slide -> gate ordinal (Final Question 1 / 2)
    new_blocks = []
    for new_i, old_i in enumerate(order, start=1):
        b = by_idx[old_i]
        b = re.sub(r'id="slide-\d+" data-idx="\d+"', f'id="slide-{new_i}" data-idx="{new_i}"', b)
        if old_i in promoted:
            b = b.replace('class="slide t-quiz"', 'class="slide t-gate"', 1)
            b = b.replace("<h2>Knowledge Check</h2>", f"<h2>Final Question {promoted[old_i]}</h2>", 1)
        elif old_i in range(48, 54):
            n = old_i - 47 + 2                      # old FQ1..6 -> new FQ3..8
            b = re.sub(r"<h2>Final Question \d+</h2>", f"<h2>Final Question {n}</h2>", b, count=1)
        new_blocks.append(b)
    body = prefix + "".join(new_blocks)
    tail = html[html.rindex("</section>") + len("</section>"):]
    doc = body + tail

    # --- 6. swap qids and option text ---
    for pos in range(25):
        oq, nq = oldq_for_pos[pos], f"__TMP{pos:02d}__"
        doc = doc.replace(oq, nq)
    for pos in range(25):
        tmp, nq = f"__TMP{pos:02d}__", newq_for_pos[pos]
        doc = doc.replace(tmp, nq)
    for pos in range(25):
        nq = newq_for_pos[pos]
        for i in range(4):
            doc = re.sub(
                r"(cqAnswer\(this,'%s',%d,'[^']*'\)[^>]*>)(.*?)(</button>)" % (re.escape(nq), i),
                lambda m, t=new_opts[pos][i]: m.group(1) + t + m.group(3),
                doc, count=1, flags=re.S,
            )

    # --- 7. NARR / QSLIDE / GATE / HASHES / identifiers ---
    new_narr = {str(n): narr[str(o)] for n, o in enumerate(order, start=1)}
    for old_i, ordinal in promoted.items():
        n = str(order.index(old_i) + 1)
        new_narr[n] = (
            new_narr[n].rstrip()
            + " This one is part of the final set, so it counts toward your one hundred percent. Make your call."
        )
    new_qslide = {str(order.index(s) + 1): newq_for_pos[i] for i, s in enumerate(q_positions)}
    hashes = {newq_for_pos[p]: fnv1a(f"{NEW_SALT}:{newq_for_pos[p]}:{new_idx[p]}") for p in range(25)}

    doc = re.sub(r"var NARR = \{.*?\};", "var NARR = " + json.dumps(new_narr) + ";", doc, flags=re.S)
    doc = re.sub(r"var QSLIDE = \{.*?\};", "var QSLIDE = " + json.dumps(new_qslide) + ";", doc, flags=re.S)
    doc = re.sub(r"var HASHES=\{.*?\};", "var HASHES=" + json.dumps(hashes) + ";", doc, flags=re.S)
    doc = re.sub(r"GATE=\[[^\]]*\]", "GATE=" + json.dumps(GATE_QIDS), doc)
    doc = re.sub(r"GATE = \[[^\]]*\]", "GATE = " + json.dumps(GATE_QIDS), doc)
    doc = doc.replace("(/(\\d+)$/)[1])-18)", "(/(\\d+)$/)[1])-%d)" % REVIEW_OFFSET)
    doc = doc.replace(r"match(/(\d+)$/)[1])-18)", r"match(/(\d+)$/)[1])-%d)" % REVIEW_OFFSET)
    doc = doc.replace(man["salt"], NEW_SALT)
    doc = doc.replace(f"cq_answered_{SRC_MOD}", f"cq_answered_{NEW_MOD}")
    doc = doc.replace(SRC_MOD, NEW_MOD)
    doc = doc.replace("S4_M02", NEW_NEXT) if "S4_M02" in doc else doc

    (out / f"{NEW_MOD}.html").write_text(doc, encoding="utf-8")

    # --- 8. manifest ---
    gate_codes, bank_codes = set(), set()
    item_codes = {}
    for p in range(25):
        codes = ITEM_ACS[p + 1]
        item_codes[newq_for_pos[p]] = codes
        (gate_codes if p + 1 >= 18 else bank_codes).update(codes)
    taught_only = [c for c in ALL_ACS_CODES if c not in gate_codes | bank_codes]
    manifest = {
        "module": NEW_MOD, "stage": "4", "gate_code": NEW_GATE_CODE, "version": "2026.08",
        "salt": NEW_SALT, "total": 54, "next": NEW_NEXT, "next_label": NEW_NEXT_LABEL,
        "gate": GATE_QIDS, "review_offset": REVIEW_OFFSET,
        "answer_key": {newq_for_pos[p]: new_idx[p] for p in range(25)},
        "acs_coverage": {
            "gate": sorted(gate_codes),
            "bank": sorted(bank_codes - gate_codes),
            "taught_only": sorted(taught_only),
        },
        "item_codes": item_codes,
        "derived_from": {"source_module": SRC_MOD, "transform": "renumber+gate8+rekey+acs"},
    }
    (out / f"{NEW_MOD}_manifest.json").write_text(json.dumps(manifest, indent=2) + "\n")

    # --- 9. instructor script ---
    src_script = (src / f"{SRC_MOD}_instructor_script.md").read_text(encoding="utf-8")
    lines = [
        f"# {NEW_MOD} -- Center of Gravity Determination -- Instructor Script",
        "",
        f"Stage 4, module 15. Gate code {NEW_GATE_CODE}. Gate: q18-q25 (8 questions, 100% mastery).",
        f"Review offset {REVIEW_OFFSET}, so q18 renders as Final Question 1.",
        f"Derived from {SRC_MOD}. Narration is unchanged except the two promoted gate slides,",
        "which now state that the question counts toward the 100%.",
        "", "---", "",
    ]
    for n in range(1, 55):
        lines += [f"## Slide {n}", "", new_narr[str(n)], ""]
    (out / f"{NEW_MOD}_instructor_script.md").write_text("\n".join(lines), encoding="utf-8")

    print(f"built {NEW_MOD}: gate={''.join('ABCD'[new_idx[i]] for i in range(17,25))} "
          f"dist={[new_idx.count(i) for i in range(4)]}")


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
