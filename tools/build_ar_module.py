#!/usr/bin/env python3
"""
General builder for the Advanced Rigger modules (S4_M15 .. S4_M23).

Derives a new module from its verified source, applying the settled decisions:
  renumber into the existing Stage 4 sequence, gate 6 -> 8, review_offset 17,
  re-key against the anti-cycle rules, and emit the ACS coverage map.

The source module is read, never written.

Generalises tools/build_s4_m15.py, which built S4_M15 and is kept as the record
of that build. Use this tool for M16 onward.

Usage: python3 build_ar_module.py <module_key> <src_dir> <out_dir>
"""
import json, re, sys, random
from pathlib import Path

REVIEW_OFFSET = 17

# Gate sequences already in use platform-wide. A new gate must not reuse one.
KNOWN_GATE_SEQS = {
    "BDACBD",    # S4_M01
    "ACBDCA",    # S4_M02
    "DABDCA",    # S4_M03-M09 and EM_M01 (the shared-key defect)
    "ABDCABCD",  # S4_M15
}

M16_ACS = {
    1: ["S4.M16.K4", "S4.M16.R1"], 2: ["S4.M16.K4"], 3: ["S4.M16.K3", "S4.M16.R2"],
    4: ["S4.M16.K1", "S4.M16.S1"], 5: ["S4.M16.K1"], 6: ["S4.M16.K2"], 7: ["S4.M16.K3"],
    8: ["S4.M16.S2"], 9: ["S4.M16.K5"], 10: ["S4.M16.K5"], 11: ["S4.M16.K5", "S4.M16.S3"],
    12: ["S4.M16.S3"], 13: ["S4.M16.K6", "S4.M16.R4"], 14: ["S4.M16.R2"], 15: ["S4.M16.R2"],
    16: ["S4.M16.R5", "S4.M16.S4"], 17: ["S4.M16.S5"],
    # gate q18-q25
    18: ["S4.M16.K7", "S4.M16.S4"], 19: ["S4.M16.K4", "S4.M16.R1"], 20: ["S4.M16.S2"],
    21: ["S4.M16.R1", "S4.M16.K4"], 22: ["S4.M16.K1", "S4.M16.K3"],
    23: ["S4.M16.S3", "S4.M16.K5"], 24: ["S4.M16.R2", "S4.M16.R3"],
    25: ["S4.M16.R5", "S4.M16.S4"],
}

MODULES = {
    "S4_M16": dict(
        src="S4_M02", dst="S4_M16",
        title="Unequal Leg Loading and Off-Level Pick Points",
        salt="CQ1:S4_M16_UnequalLegLoading",
        gate_code="R-201C / AR-102C",
        old_next="S4_M03", next="S4_M17",
        next_label="Sling Tension Beyond the Chart",
        total=46,
        # tail permutation: old slides 36,37,38,39 become 38,39,36,37 so the two
        # trailing formative checks land inside a contiguous t-gate block
        permute_from=36, permute_order=[38, 39, 36, 37],
        promoted={36: 1, 37: 2},          # old slide -> Final Question ordinal
        old_gate_slides=range(40, 46),    # existing t-gate slides, renumber FQ1-6 -> FQ3-8
        acs_prefix="S4.M16",
        acs_counts=dict(K=7, R=5, S=5),
        item_acs=M16_ACS,
        seed=20260808,
    ),
}


def fnv1a(s: str) -> str:
    h = 0x811C9DC5
    for c in s:
        h ^= ord(c)
        h = (h * 0x01000193) & 0xFFFFFFFF
    return format(h, "08x")


def slide_blocks(html):
    spans = [m.start() for m in re.finditer(r'<section class="slide[^"]*" id="slide-\d+"', html)]
    idxs = [int(m.group(1)) for m in re.finditer(r'<section class="slide[^"]*" id="slide-(\d+)"', html)]
    end = html.rindex("</section>") + len("</section>")
    blocks = {}
    for i, st in enumerate(spans):
        stop = spans[i + 1] if i + 1 < len(spans) else end
        blocks[idxs[i]] = html[st:stop]
    return html[:spans[0]], blocks, html[end:]


def design_key(cfg):
    rnd = random.Random(cfg["seed"])
    L = "ABCD"
    for _ in range(500000):
        gate = [0, 0, 1, 1, 2, 2, 3, 3]
        rnd.shuffle(gate)
        if any(gate[i] == gate[i - 1] for i in range(1, 8)):
            continue
        if "".join(L[g] for g in gate) in KNOWN_GATE_SEQS:
            continue
        need = [7, 6, 6, 6]
        for g in gate:
            need[g] -= 1
        if min(need) < 0:
            continue
        head = [i for i, n in enumerate(need) for _ in range(n)]
        rnd.shuffle(head)
        seq = head + gate
        if any(seq[i] == seq[i - 1] for i in range(1, 25)):
            continue
        if any(all((seq[st + k + 1] - seq[st + k]) % 4 == (seq[st + 1] - seq[st]) % 4
                   for k in range(7)) for st in range(18)):
            continue
        return seq
    raise SystemExit("no conforming key found")


def build(key, src_dir, out_dir):
    cfg = MODULES[key]
    src, dst = Path(src_dir), Path(out_dir)
    dst.mkdir(parents=True, exist_ok=True)
    html = (src / f"{cfg['src']}.html").read_text(encoding="utf-8")
    man = json.loads((src / f"{cfg['src']}_manifest.json").read_text())
    narr = json.loads(re.search(r"var NARR = (\{.*?\});", html, re.S).group(1))
    qslide = json.loads(re.search(r"var QSLIDE = (\{.*?\});", html, re.S).group(1))
    old_key = man["answer_key"]
    total = cfg["total"]

    # --- slide order ---
    p0 = cfg["permute_from"]
    order = (list(range(1, p0)) + cfg["permute_order"]
             + list(range(p0 + len(cfg["permute_order"]), total + 1)))
    assert sorted(order) == list(range(1, total + 1)), "permutation must be a bijection"

    prefix, blocks, suffix = slide_blocks(html)
    old_q_at = {int(k): v for k, v in qslide.items()}
    q_slides = [s for s in order if s in old_q_at]
    assert len(q_slides) == 25
    oldq = [old_q_at[s] for s in q_slides]
    newq = [f"{cfg['dst']}_q{i+1:02d}" for i in range(25)]
    gate_qids = newq[17:25]

    # --- options and correct text ---
    opts, correct = [], []
    for oq in oldq:
        f = {}
        for m in re.finditer(
            r"cqAnswer\(this,'%s',(\d+),'[^']*'\)[^>]*>(.*?)</button>" % re.escape(oq), html, re.S
        ):
            f[int(m.group(1))] = m.group(2)
        assert len(f) == 4, oq
        opts.append([f[i] for i in range(4)])
        correct.append(f[old_key[oq]])

    new_idx = design_key(cfg)

    rnd = random.Random(cfg["seed"] + 7)
    new_opts = []
    for p in range(25):
        ci = opts[p].index(correct[p])
        d = [o for i, o in enumerate(opts[p]) if i != ci]
        rnd.shuffle(d)
        it = iter(d)
        arr = [correct[p] if i == new_idx[p] else next(it) for i in range(4)]
        assert arr[new_idx[p]] == correct[p] and sorted(arr) == sorted(opts[p])
        new_opts.append(arr)

    # --- rebuild slides ---
    out_blocks = []
    for new_i, old_i in enumerate(order, start=1):
        b = blocks[old_i]
        b = re.sub(r'id="slide-\d+" data-idx="\d+"', f'id="slide-{new_i}" data-idx="{new_i}"', b)
        if old_i in cfg["promoted"]:
            b = b.replace('class="slide t-quiz"', 'class="slide t-gate"', 1)
            b = re.sub(r"<h2>[^<]*</h2>", f"<h2>Final Question {cfg['promoted'][old_i]}</h2>", b, count=1)
        elif old_i in cfg["old_gate_slides"]:
            n = old_i - min(cfg["old_gate_slides"]) + 1 + len(cfg["promoted"])
            b = re.sub(r"<h2>Final Question \d+</h2>", f"<h2>Final Question {n}</h2>", b, count=1)
        out_blocks.append(b)
    doc = prefix + "".join(out_blocks) + suffix

    # --- qids (two-phase to avoid collisions), then option text ---
    for p in range(25):
        doc = doc.replace(oldq[p], f"__TMP{p:02d}__")
    for p in range(25):
        doc = doc.replace(f"__TMP{p:02d}__", newq[p])
    for p in range(25):
        for i in range(4):
            doc = re.sub(
                r"(cqAnswer\(this,'%s',%d,'[^']*'\)[^>]*>)(.*?)(</button>)" % (re.escape(newq[p]), i),
                lambda m, t=new_opts[p][i]: m.group(1) + t + m.group(3),
                doc, count=1, flags=re.S,
            )

    # --- data blocks ---
    new_narr = {str(n): narr[str(o)] for n, o in enumerate(order, start=1)}
    for old_i in cfg["promoted"]:
        n = str(order.index(old_i) + 1)
        new_narr[n] = new_narr[n].rstrip() + (
            " This one is part of the final set, so it counts toward your one hundred percent."
            " Make your call."
        )
    new_qslide = {str(order.index(s) + 1): newq[i] for i, s in enumerate(q_slides)}
    hashes = {newq[p]: fnv1a(f"{cfg['salt']}:{newq[p]}:{new_idx[p]}") for p in range(25)}

    doc = re.sub(r"var NARR = \{.*?\};", "var NARR = " + json.dumps(new_narr) + ";", doc, flags=re.S)
    doc = re.sub(r"var QSLIDE = \{.*?\};", "var QSLIDE = " + json.dumps(new_qslide) + ";", doc, flags=re.S)
    doc = re.sub(r"var HASHES=\{.*?\};", "var HASHES=" + json.dumps(hashes) + ";", doc, flags=re.S)
    doc = re.sub(r"GATE=\[[^\]]*\]", "GATE=" + json.dumps(gate_qids), doc)
    doc = re.sub(r"GATE = \[[^\]]*\]", "GATE = " + json.dumps(gate_qids), doc)
    doc = re.sub(r"(\)\[1\]\)-)\d+(\))", r"\g<1>%d\g<2>" % REVIEW_OFFSET, doc)

    # next pointer first (placeholder), then salt/session/module id
    doc = doc.replace(cfg["old_next"], "__NEXT__")
    doc = doc.replace(man["salt"], cfg["salt"])
    doc = doc.replace(f"cq_answered_{cfg['src']}", f"cq_answered_{cfg['dst']}")
    doc = doc.replace(cfg["src"], cfg["dst"])
    doc = doc.replace("__NEXT__", cfg["next"])
    (dst / f"{cfg['dst']}.html").write_text(doc, encoding="utf-8")

    # --- manifest ---
    all_codes = [f"{cfg['acs_prefix']}.{b}{i}"
                 for b, n in cfg["acs_counts"].items() for i in range(1, n + 1)]
    gate_c, bank_c, item_codes = set(), set(), {}
    for p in range(25):
        c = cfg["item_acs"][p + 1]
        item_codes[newq[p]] = c
        (gate_c if p + 1 >= 18 else bank_c).update(c)
    manifest = {
        "module": cfg["dst"], "stage": "4", "gate_code": cfg["gate_code"], "version": "2026.08",
        "salt": cfg["salt"], "total": total, "next": cfg["next"], "next_label": cfg["next_label"],
        "gate": gate_qids, "review_offset": REVIEW_OFFSET,
        "answer_key": {newq[p]: new_idx[p] for p in range(25)},
        "acs_coverage": {
            "gate": sorted(gate_c),
            "bank": sorted(bank_c - gate_c),
            "taught_only": sorted(c for c in all_codes if c not in gate_c | bank_c),
        },
        "item_codes": item_codes,
        "derived_from": {"source_module": cfg["src"], "transform": "renumber+gate8+rekey+acs"},
    }
    (dst / f"{cfg['dst']}_manifest.json").write_text(json.dumps(manifest, indent=2) + "\n")

    # --- instructor script ---
    lines = [
        f"# {cfg['dst']} -- {cfg['title']} -- Instructor Script", "",
        f"Stage 4. Gate code {cfg['gate_code']}. Gate: q18-q25 (8 questions, 100% mastery).",
        f"Review offset {REVIEW_OFFSET}, so q18 renders as Final Question 1.",
        f"Derived from {cfg['src']}. Narration is unchanged except the two promoted gate",
        "slides, which now state that the question counts toward the 100%.", "", "---", "",
    ]
    for n in range(1, total + 1):
        lines += [f"## Slide {n}", "", new_narr[str(n)], ""]
    (dst / f"{cfg['dst']}_instructor_script.md").write_text("\n".join(lines), encoding="utf-8")

    print(f"built {cfg['dst']}: gate={''.join('ABCD'[new_idx[i]] for i in range(17,25))} "
          f"dist={[new_idx.count(i) for i in range(4)]} slides={total}")


if __name__ == "__main__":
    build(sys.argv[1], sys.argv[2], sys.argv[3])
