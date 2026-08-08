# S4_M16 - Verification Record

Built 7 August 2026 by `tools/build_ar_module.py` from the verified `S4_M02` source.
Source read only; never modified.

## What changed from S4_M02

| | S4_M02 | S4_M16 |
|---|---|---|
| Module ID | `S4_M02` | `S4_M16` |
| Salt | `CQ1:S4_M02_UnequalLegLoading` | `CQ1:S4_M16_UnequalLegLoading` |
| Session key | `cq_answered_S4_M02` | `cq_answered_S4_M16` |
| Next | `S4_M03` | `S4_M17` |
| Gate | q19-q24 (6) | **q18-q25 (8)** |
| Gate slides | 40-45 | **38-45** |
| `review_offset` | 18 | **17** |
| Gate letters | A C B D C A | **D C D B A B C A = 2/2/2/2** |
| ACS mapping | absent | **`item_codes` + `acs_coverage`** |
| Slides / questions | 46 / 25 | 46 / 25 (unchanged) |

### Reaching 8 gate items

M02's tail was cleaner than M01's - three consecutive `t-quiz` slides sat immediately
before the content/divider pair. Four slides were permuted:

```
old: 35 quiz | 36 quiz | 37 quiz | 38 content | 39 divider | 40-45 gate
new: 35 quiz | 36 content | 37 divider | 38 gate | 39 gate | 40-45 gate
```

The slide *set* is unchanged - only the order of four. Questions renumbered to slide
order, which makes the gate exactly `q18`-`q25` and pulls `q25` (previously stranded on
slide 37, out of numeric sequence) back into position. Headings renumbered to Final
Question 1 through 8. The two promoted narrations now state that the question counts
toward the 100%.

Same shape as the M15 transform, which is why the builder generalised cleanly.

### Re-key

Options permuted so the correct text moved; the answer index re-derived from the option
text, never carried forward.

Gate sequence **D C D B A B C A** - 2/2/2/2, and distinct from every sequence in use:
`BDACBD` (M01), `ACBDCA` (M02), `DABDCA` (M03-M09, EM_M01), `ABDCABCD` (M15).

## Static verification - 23/23

Run with `tools/verify_ar_module.py`. Full output in the build log; headline results:

| Check | Result |
|---|---|
| Slide-to-question mapping | 25 unique qids, 4 options each |
| Answer distribution | 7/6/6/6 |
| Gate composition | `DCDBABCA` = 2/2/2/2, max run 1 |
| Gate uniqueness platform-wide | unused |
| Full-bank run | max consecutive run 1 |
| Anti-cycle | no constant-step run of 8+ |
| De-leak | worst +4 chars (limit +6) |
| FNV integrity | 25/25 match, 0 distractor collisions |
| Engine tokens | all 8 present |
| GATE parity | 2 declarations identical, 8 items |
| No plaintext keys | none |
| ASCII | pure ASCII |
| Regulatory | no `1926.1418`, no bare `B30`, no vendor |
| Identity | `data-cq-module="S4_M16"`, stage 4, zero `S4_M02` residue |
| Slide count | manifest 46 = `data-cq-total` 46 = 46 sections |
| Review offset | renderer uses `-17` |
| Gate contiguity | slides 38-45, completion at 46 |
| Gate headings | Final Question 1-8 |
| ACS referential / partition / derivation | 17 codes, no overlap, gate == union of gate item codes |
| ACS skill floor | 3 skill codes in gate (rule: >= 2) |

`node --check`: **3/3 script blocks clean.**

## Behavioural (jsdom)

| Check | S4_M16 | S4_M02 control |
|---|---|---|
| Engine + bridge load | pass | pass |
| Internals not global (`GATE`/`HASHES`) | pass | pass |
| One wrong gate answer refused | 7/8, `passed=false` | 5/6, `passed=false` |
| Forward navigation locked | slide 45 | slide 45 |
| Clean run at 100% | **8/8, slide 46/46** | 6/6, slide 46/46 |

**Behaviourally equivalent to the source.** The two inherited Gen-1 behaviours documented
for M15 - sticky wrong answers pending a Review-and-Retest reload, and
`cq-module-complete` not firing when `CQ.requestComplete()` is called directly rather
than through the gate submit control - reproduce identically here and on `S4_M02`.

## ACS coverage

All 17 codes covered; `taught_only` is empty.

- **Gate (12):** K1, K3, K4, K5, K7, R1, R2, R3, R5, S2, S3, S4
- **Bank (5):** K2, K6, R4, S1, S5

`S1` (measure or scale headroom and leg length, compute LAF) sits in the bank rather than
the gate. It is a measurement skill and the gate item that comes closest - the LAF
formula question - is coded `K1` + `S1` at position 4, which is a bank slot. Worth
revisiting if a stronger `S1` item is authored.

## Still outstanding

- **Gen 3 retrofit** - keys to `platform/cq_keys_S4.json` (8 more gate records), assets
  externalized, `cq:*` event contract. Still Gen 1: `HASHES` baked client-side.
- **ElevenLabs narration.** Runs on `speechSynthesis`; no embedded audio. When audio
  ships, reconcile the overlay GATE to the 8-item engine GATE and re-run the suite.
- **`S4_M15`'s next pointer** already targets `S4_M16`, so the chain
  `S4_M14 -> S4_M15 -> S4_M16 -> S4_M17` needs only the `S4_M14` edit noted for M15.
