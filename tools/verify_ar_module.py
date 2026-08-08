#!/usr/bin/env python3
"""
Static verification for a built Advanced Rigger module.

Runs the 12-point house suite plus the checks added after the 7 Aug 2026 audit:
anti-cycle, cross-module gate uniqueness, review-offset derivation, gate
contiguity, and ACS coverage integrity.

Usage: python3 verify_ar_module.py <module.html> <manifest.json>
Exit 0 only if every check passes.
"""
import json, re, sys, html as H

KNOWN_GATE_SEQS = {
    "BDACBD": "S4_M01", "ACBDCA": "S4_M02",
    "DABDCA": "S4_M03-M09 / EM_M01", "ABDCABCD": "S4_M15",
    "DCDBABCA": "S4_M16",
}


def fnv1a(s):
    h = 0x811C9DC5
    for c in s:
        h ^= ord(c)
        h = (h * 0x01000193) & 0xFFFFFFFF
    return format(h, "08x")


def main(html_path, man_path):
    s = open(html_path, encoding="utf-8").read()
    d = json.load(open(man_path))
    mod, salt, ak, gate = d["module"], d["salt"], d["answer_key"], d["gate"]
    L = "ABCD"
    P, F = [], []
    def chk(n, ok, detail=""):
        (P if ok else F).append(f"{n}" + (f": {detail}" if detail else ""))

    opts = {}
    for m in re.finditer(r"cqAnswer\(this,'([^']+)',(\d+),'[^']*'\)[^>]*>(.*?)</button>", s, re.S):
        opts.setdefault(m.group(1), {})[int(m.group(2))] = H.unescape(
            re.sub("<[^>]+>", "", m.group(3))).strip()
    chk("01 slide-to-question", len(opts) == 25 and all(len(v) == 4 for v in opts.values()),
        f"{len(opts)} unique qids, 4 options each")
    qs = json.loads(re.search(r"var QSLIDE = (\{.*?\});", s, re.S).group(1))
    chk("02 QSLIDE integrity", len(qs) == 25 and set(qs.values()) == set(ak), f"{len(qs)} entries")

    seq = [ak[f"{mod}_q{i:02d}"] for i in range(1, 26)]
    dist = [seq.count(i) for i in range(4)]
    chk("03 distribution", dist == [7, 6, 6, 6], str(dist))
    g = seq[17:25]
    gseq = "".join(L[x] for x in g)
    chk("04 gate composition", [g.count(i) for i in range(4)] == [2, 2, 2, 2]
        and all(g[i] != g[i - 1] for i in range(1, 8)), f"{gseq} = 2/2/2/2, max run 1")
    owner = KNOWN_GATE_SEQS.get(gseq)
    chk("05 gate uniqueness", owner in (None, mod),
        f"{gseq} " + ("registered to this module" if owner == mod
                      else f"COLLIDES with {owner}" if owner else "unused"))
    chk("06 full-bank run", all(seq[i] != seq[i - 1] for i in range(1, 25)), "max consecutive run 1")
    cyc = any(all((seq[st + k + 1] - seq[st + k]) % 4 == (seq[st + 1] - seq[st]) % 4
                  for k in range(7)) for st in range(18))
    chk("07 anti-cycle", not cyc, "no constant-step run of 8+")

    worst = max(len(opts[q][i]) - max(len(v) for k, v in opts[q].items() if k != i)
                for q, i in ak.items())
    chk("08 de-leak", worst <= 6, f"worst {worst:+d} chars (limit +6)")

    baked = json.loads(re.search(r"var HASHES=(\{.*?\});", s, re.S).group(1))
    ok = sum(baked.get(q) == fnv1a(f"{salt}:{q}:{i}") for q, i in ak.items())
    coll = sum(1 for q, i in ak.items() for j in range(4)
               if j != i and fnv1a(f"{salt}:{q}:{j}") == baked.get(q))
    chk("09 FNV integrity", ok == 25 and coll == 0, f"{ok}/25 match, {coll} collisions")

    toks = [".every(", "requestComplete", "cq-module-complete", "Math.imul", "0x01000193",
            "scoreAnswer", "window.CQ", "advanceWhenReady"]
    chk("10 engine tokens", all(t in s for t in toks), "all present")
    gates = re.findall(r"GATE\s*=\s*(\[[^\]]*\])", s)
    chk("11 GATE parity", len(gates) == 2 and json.loads(gates[0]) == json.loads(gates[1]) == gate,
        f"{len(gates)} decls identical, {len(gate)} items")
    chk("12 no plaintext keys", not any(t in s for t in ["data-correct", "Correct answer:", "data-good"]),
        "none")

    body = re.sub(r"(data:[a-z]+/[a-z0-9.+-]+;base64,)[A-Za-z0-9+/=]+", r"\1AA", s)
    chk("13 ASCII", not [c for c in body if ord(c) > 127], "pure ASCII")
    chk("14 regulatory", not re.search(r"1926\.1418", body) and not re.search(r"B30(?![.\d])", body)
        and not re.search(r"\b(ITI|NCCCO|Tucker|SC&RA)\b", body),
        "no 1418, no bare B30, no vendor")

    src = d.get("derived_from", {}).get("source_module", "")
    chk("15 identity", f'data-cq-module="{mod}"' in s and 'data-cq-stage="4"' in s
        and (not src or src not in s), f"{mod}, stage 4, no {src} residue")
    tot = re.search(r'data-cq-total="(\d+)"', s).group(1)
    secs = len(re.findall(r'<section class="slide', s))
    chk("16 slide count", tot == str(d["total"]) == str(secs),
        f"manifest={d['total']} data-cq-total={tot} sections={secs}")
    chk("17 review offset", f")-{d['review_offset']})" in s
        and not re.search(r"\)\[1\]\)-(?!%d\))\d+\)" % d["review_offset"], s),
        f"renderer uses -{d['review_offset']}")
    gs = sorted(int(k) for k, v in qs.items() if v in gate)
    chk("18 gate contiguity", gs == list(range(gs[0], gs[0] + 8)) and gs[-1] == d["total"] - 1,
        f"slides {gs[0]}-{gs[-1]}, completion at {d['total']}")
    fq = [int(x) for x in re.findall(r"Final Question (\d+)</h2>", s)]
    chk("19 gate headings", fq == list(range(1, 9)), "Final Question 1-8")

    cov, ic = d["acs_coverage"], d["item_codes"]
    cited = set(sum(ic.values(), []))
    allc = set(cov["gate"]) | set(cov["bank"]) | set(cov["taught_only"])
    chk("20 ACS referential", cited <= allc, f"{len(cited)} cited codes all declared")
    chk("21 ACS partition", not (set(cov["gate"]) & set(cov["bank"]))
        and not (set(cov["gate"]) & set(cov["taught_only"])), f"{len(allc)} codes, no overlap")
    chk("22 ACS gate derivation", set(cov["gate"]) == set(sum((ic[q] for q in gate), [])),
        "gate coverage == union of gate item codes")
    sk = [c for c in cov["gate"] if ".S" in c]
    chk("23 ACS skill floor", len(sk) >= 2, f"{len(sk)} skill codes in gate")

    print(f"--- {mod} ---")
    for x in P:
        print("  OK  ", x)
    for x in F:
        print("  XX  ", x)
    print(f"{len(P)} passed, {len(F)} failed")
    return 1 if F else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1], sys.argv[2]))
