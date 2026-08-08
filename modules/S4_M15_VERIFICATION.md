# S4_M15 - Verification Record

Built 7 August 2026 by `tools/build_s4_m15.py` from the verified `S4_M01` source.
Source read only; never modified.

## What changed from S4_M01

| | S4_M01 | S4_M15 |
|---|---|---|
| Module ID | `S4_M01` | `S4_M15` |
| Salt | `CQ1:S4_M01_CenterOfGravity` | `CQ1:S4_M15_CenterOfGravity` |
| Session key | `cq_answered_S4_M01` | `cq_answered_S4_M15` |
| Next | `S4_M02` | `S4_M16` |
| Gate | q19-q24 (6) | **q18-q25 (8)** |
| Gate slides | 48-53 | **46-53** |
| `review_offset` | 18 | **17** |
| Review renderer | `...-18)` | **`...-17)`** |
| Gate letter balance | B D A C B D | **A B D C A B C D = 2/2/2/2** |
| ACS mapping | absent | **`item_codes` + `acs_coverage`** |
| Slides / questions | 54 / 25 | 54 / 25 (unchanged) |

### How the gate reached 8 items without growing the bank

The gate was a contiguous `t-gate` tail block of 6 slides behind a divider. Two
trailing formative checks were promoted into it by permuting four slides:

```
old: 43 content | 44 quiz q17 | 45 content | 46 quiz q18 | 47 divider | 48-53 gate
new: 43 content | 44 content  | 45 divider | 46 gate     | 47 gate    | 48-53 gate
```

The slide *set* is unchanged - only the order of four slides. Questions were then
renumbered to slide order, which makes the gate exactly `q18`-`q25` and puts the
out-of-sequence `q25` (formerly on slide 19) back in position. Headings renumbered to
Final Question 1 through 8. The two promoted narrations now state that the question
counts toward the 100%.

### Re-key

Options were **permuted so the correct text moved**; the answer index was **re-derived
from the option text**, never carried forward. That is authoring bug #1 in the ACS - it
bit M08 q13/q16 and M09 q17 - and it is the failure mode a careless reorder walks into.

New key satisfies: 7/6/6/6 full bank, max consecutive run 1, gate exactly 2/2/2/2, no
constant-step run of 8 or more (anti-cycle), and a gate sequence not already in use
platform-wide.

Gate sequence: **A B D C A B C D** - distinct from `BDACBD` (M01), `ACBDCA` (M02), and
`DABDCA` (the sequence shared by M03-M09 and EM_M01).

## Static verification - 23/23

| Check | Result |
|---|---|
| Slide-to-question mapping | 25 unique qids, 4 options each |
| QSLIDE integrity | 25 entries, matches answer key |
| Answer distribution | 7/6/6/6 |
| Gate composition | `ABDCABCD` = 2/2/2/2, max run 1 |
| Gate uniqueness platform-wide | not a known sequence |
| Full-bank run | max consecutive run 1 |
| Anti-cycle | no constant-step run of 8+ |
| De-leak | worst +5 chars (limit +6) |
| FNV integrity | 25/25 match, 0 distractor collisions |
| Engine tokens | `.every(`, `requestComplete`, `cq-module-complete`, `Math.imul`, `0x01000193`, `scoreAnswer`, `window.CQ`, `advanceWhenReady` |
| GATE parity | 2 declarations, identical, 8 items |
| No plaintext keys | no `data-correct` / `Correct answer:` / `data-good` |
| ASCII | pure ASCII, base64 stripped |
| Regulatory | no `1926.1418`, no bare `B30`, no vendor name |
| Identity | `data-cq-module="S4_M15"`, `data-cq-stage="4"`, zero `S4_M01` residue |
| Slide count | manifest 54 = `data-cq-total` 54 = 54 sections |
| Review offset | renderer uses `-17`, no `-18` remains |
| Gate contiguity | slides 46-53, completion at 54 |
| Gate headings | Final Question 1-8 |
| ACS referential | 18 cited codes all declared |
| ACS partition | 18 codes across gate/bank/taught_only, no overlap |
| ACS gate derivation | `acs_coverage.gate` == union of gate `item_codes` |
| ACS skill floor | 4 skill codes in gate (rule: >= 2) |

`node --check`: **3/3 script blocks clean.**

## Behavioural (jsdom)

| Check | Result |
|---|---|
| Engine + bridge load | `cqAnswer` function, `CQ.requestComplete` present |
| Internals not global | `GATE` and `HASHES` are script-scoped, not on `window` |
| 99% refused | 7/8 returns `passed=false` |
| Forward navigation locked | `jumpTo(54)` stops at slide 53 |
| Clean run at 100% | **8/8, `passed=true`, reaches slide 54** |

Control run against the original `S4_M01` under the identical harness: 6/6, `passed=true`,
slide 54. **Behaviourally equivalent.**

### Two inherited behaviours, confirmed not introduced

Both reproduce identically on the original `S4_M01`:

1. **A wrong gate answer is sticky.** Re-clicking the correct option does not raise the
   score; the design routes the learner to a "Review and Retest" control that reloads the
   module. Gen 1 behaviour. Stage 6's corrected spec - *a wrong response is not retained,
   all options are re-enabled* - closes this, and it is already on the Gen 3 retrofit list.
2. **`cq-module-complete` did not fire under this harness** on either module. Calling
   `CQ.requestComplete()` directly is not the dispatch path; the handshake goes through the
   gate submit control. This is a limitation of my harness, not a defect - the house jsdom
   verifier drives it correctly and reports 13/13.

## Still outstanding for this module

- **Gen 3 retrofit** - keys to `platform/cq_keys_S4.json` (adds 8 gate records), assets
  externalized, `cq:*` event contract. `S4_M15` is still Gen 1: `HASHES` baked client-side.
- **ElevenLabs narration.** Runs on the `speechSynthesis` fallback; no embedded audio.
  When audio ships, the overlay GATE must be reconciled to the 8-item engine GATE and the
  suite re-run.
- **`S4_M14`'s next pointer** must be repointed to `S4_M15`. That is the only edit any
  existing file needs.
