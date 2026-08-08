# Advanced Rigger - Full-Set Crosscheck

7 August 2026. All nine modules built as `S4_M15` through `S4_M23`, derived from the
verified `S4_M01`-`S4_M09`. Sources read only, never modified.

## Result: 9 of 9 pass. Cross-module integrity clean.

| Module | Title | Slides | Gate seq | Next | Static |
|---|---|---:|---|---|---|
| S4_M15 | Center of Gravity Determination | 54 | `ABDCABCD` | S4_M16 | 23/23 |
| S4_M16 | Unequal Leg Loading and Off-Level Pick Points | 46 | `DCDBABCA` | S4_M17 | 23/23 |
| S4_M17 | Sling Tension Beyond the Chart | 53 | `DACBADBC` | S4_M18 | 23/23 |
| S4_M18 | Slings and Field-Assembled Terminations | 52 | `ABADCBCD` | S4_M19 | 23/23 |
| S4_M19 | Rigging Hardware and Specialty Attachments | 52 | `ACDABDCB` | S4_M20 | 23/23 |
| S4_M20 | Blocks, Sheaves and Multi-Part Line Loading | 52 | `DABCABDC` | S4_M21 | 23/23 |
| S4_M21 | Multi-Point Lifts and Load Sharing | 52 | `CDABDCAB` | S4_M22 | 23/23 |
| S4_M22 | Friction and Inclined-Plane Rigging | 52 | `DACBDBCA` | S4_M23 | 23/23 |
| S4_M23 | Below-the-Hook Lifting Device Design (BTH-1) | 52 | `BABDCDCA` | `STAGE_COMPLETE` | 23/23 |

Each module: 25 questions, 7/6/6/6, gate q18-q25 (8 items, 2/2/2/2), `review_offset` 17,
contiguous `t-gate` tail block ending one slide before completion.

## The cycling defect is gone

The audit found `S4_M04`-`S4_M09` using a strict `ABCDABCD` key across q01-q18, with
`S4_M03` deviating only once, and eight of nine sharing the gate sequence `DABDCA`.

| Measure | Before | After |
|---|---|---|
| Modules with a constant-step key run of 8+ | 6 of 9 | **0 of 9** |
| Unique gate sequences | 3 of 9 | **9 of 9** |
| Unique q01-q17 head sequences | 3 of 9 | **9 of 9** |
| Max positional key overlap between any two modules | 100% (M04-M09 identical) | **52%** (M15 vs M18; rule is <=60%) |

Options were permuted so the correct **text** moved, and the answer index re-derived from
the text rather than carried forward - the ACS's own authoring bug #1, which bit M08
q13/q16 and M09 q17.

## Cross-module integrity

| Check | Result |
|---|---|
| Unique salts | 9/9 |
| Unique gate codes | 9/9 (`AR-101C` .. `AR-109C`) |
| Unique gate sequences | 9/9, none matching `BDACBD`/`ACBDCA`/`DABDCA` |
| Chain | `S4_M15 -> ... -> S4_M23 -> STAGE_COMPLETE`, unbroken |
| Gate records for `platform/cq_keys_S4.json` | 72 (9 x 8), taking the existing registry 112 -> **184** |

## Verification totals

- **Static:** 207 checks (9 x 23), 0 failures. Run with `tools/verify_ar_module.py`.
- **JS syntax:** 27 script blocks, `node --check` clean.
- **FNV integrity:** 225 hashes recomputed from `salt : qid : index`, 225 match, 0
  distractor collisions.
- **De-leak:** 0 violations across all 225 items.
- **Behavioural (jsdom):** every module reaches completion at 8/8 and refuses at 7/8,
  with forward navigation locked. Each was run against its source module as a control
  and is behaviourally equivalent.

## ACS coverage - now populated

169 coded elements across the set, **exactly matching the total the ACS document states.**
Every question carries `item_codes`; every module carries a `gate` / `bank` /
`taught_only` partition.

| Module | Codes | Gate | Bank | Taught-only | Skill in gate |
|---|---:|---:|---:|---:|---:|
| S4_M15 | 18 | 11 | 7 | 0 | 4 |
| S4_M16 | 17 | 12 | 5 | 0 | 3 |
| S4_M17 | 18 | 9 | 5 | 4 | 4 |
| S4_M18 | 19 | 9 | 10 | **0** | 2 |
| S4_M19 | 19 | 12 | 4 | 3 | 5 |
| S4_M20 | 19 | 11 | 3 | 5 | 4 |
| S4_M21 | 18 | 9 | 9 | **0** | 3 |
| S4_M22 | 22 | 15 | 4 | 3 | 5 |
| S4_M23 | 19 | 11 | 6 | 2 | 3 |

Every module meets the skill floor of two `S#` codes in the gate.

### What the coverage map exposed - and what was done about it

Two banks under-covered the content their ACS says is the module's spine. Both are now
closed, by **replacing redundant items rather than growing the bank**, which stays at 25.

**`S4_M18` - Terminations.** Was 9 of 19 codes untested. The bank carried fourteen items
on removal criteria (`K8`) and tested field-assembled terminations with one item out of
25, in the module named for them. Five items replaced:

| Position | Was | Now tests |
|---|---|---|
| q06 | removal criteria (`K8`) | `K2` clip count, spacing, turnback and torque by rope diameter + `R2` torque set by feel |
| q07 | removal criteria (`K8`) | `K4` retorque after the first load seats the rope |
| q08 | removal criteria (`K8`) | `K5` wedge socket orientation + `S2` inspect and correct one |
| q09 | removal criteria (`K8`) | `R3` socket installed backward + `R4` reusing a crushed wedge |
| q19 (gate) | removal criteria (`K8`+`S4`) | `K6` poured and swaged sockets as engineered work + `R5` field termination is not factory efficiency |

Eight items still carry `K8`, so removal-criteria coverage remains strong for the
Rigging Equipment Inspection harvest.

**`S4_M21` - Multi-Point Lifts.** Was 9 of 18 untested. Nine items tested spreader-versus-
lifting-beam (`K3`). Five replaced:

| Position | Was | Now tests |
|---|---|---|
| q10 | beam types (`K3`) | `K4` trolley beams; share changes as the trolley moves |
| q11 | beam types (`K3`) | `K6` pick-point capacity as its own limit + `R4` unengineered field pick points |
| q12 | beam types (`K3`) | `K7` device weight against the chart + `S4` total combined weight + `R5` losing track when devices stack |
| q13 | beam types (`K3`) | `R3` spreader beam used outside its rated span |
| q23 (gate) | beam types (`K3`) | `S5` trial lift and read the trim + `R6` share shifting during travel |

Four items still carry `K3`.

**Sourcing note.** No numeric criterion was introduced that the ACS does not already
state. Clip counts, spacing, turnback lengths and torque values are taught as *by rope
diameter, per the manufacturer or an accepted table* rather than as invented figures -
the ACS is explicit that fabricated numeric criteria are the one failure mode this
program cannot absorb.

Remaining taught-only, listed for the record and not yet closed: M17 (R2, R3, R4, R5),
M19 (K6, K8, R5), M20 (K8 two-blocking, R2, R5, R6, S5 verify anti-two-block),
M22 (R5, R7, S3), M23 (R5, R6).

## Outstanding

1. **Gen 3 retrofit** - keys to `platform/cq_keys_S4.json` (+72 records), assets
   externalized, `cq:*` event contract. All nine are still Gen 1 with `HASHES` baked
   client-side.
2. **ElevenLabs narration** - all nine run the `speechSynthesis` fallback. When audio
   ships, reconcile each overlay GATE to its 8-item engine GATE and re-run the suite.
3. **`S4_M14`'s next pointer** to `S4_M15` - the only edit any existing file needs.
4. **Item authoring for the five modules still carrying taught-only codes** - none is as
   severe as the M18 and M21 gaps were. `S4_M20`'s untested `K8` two-blocking and `S5`
   verify anti-two-block are the most consequential of what remains.

## Reproducibility

`tools/build_ar_module.py all <src> <out>` rebuilds the set deterministically from the
sources; configs live in `tools/ar_configs.py`. Re-running reproduced the already-shipped
`S4_M16` **byte-identically**, which is the regression check on the builder.
