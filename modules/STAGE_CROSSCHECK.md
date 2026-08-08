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
| S4_M18 | 19 | 7 | 3 | **9** | 2 |
| S4_M19 | 19 | 12 | 4 | 3 | 5 |
| S4_M20 | 19 | 11 | 3 | 5 | 4 |
| S4_M21 | 18 | 7 | 2 | **9** | 2 |
| S4_M22 | 22 | 15 | 4 | 3 | 5 |
| S4_M23 | 19 | 11 | 6 | 2 | 3 |

Every module meets the skill floor of two `S#` codes in the gate.

### What the coverage map immediately exposed

This is the payoff for building the layer. Two banks under-cover the content their ACS
says is the module's spine:

**`S4_M18` - Terminations. 9 of 19 codes untested.**
Untested: `K2` clip count, spacing, turnback and torque by rope diameter; `K4` retorque
after initial loading; `K5` wedge socket assembly; `K6` poured and swaged sockets;
`R2` too few clips or torque by feel; `R3` wedge socket backward; `R4` reusing crushed
clips; `R5` treating a field termination as factory efficiency; `S2` inspect and correct
a wedge socket.

The bank tests sling **inspection and removal criteria** thoroughly and barely tests
**field-assembled terminations** - one item (q04, clip orientation) out of 25. The module
is titled *Slings and Field-Assembled Terminations*, and `K2` and `K5` are the
highest-consequence elements in it. This is the module that donates to the Rigging
Equipment Inspection course.

**`S4_M21` - Multi-Point Lifts. 9 of 18 codes untested.**
Untested: `K4` trolley beams; `K6` pick-point capacity as its own limit; `K7` device
weight against the crane chart; `R3` spreader beam outside rated span; `R4` unengineered
pick points; `R5` losing track of total suspended weight; `R6` load shift during travel;
`S4` total combined weight against the chart; `S5` trial lift and read the trim.

The bank is weighted to beam types and share arithmetic. `K7`/`S4` - combined weight
against the chart - is a rule the ACS states twice (M21 and M23) and M21 never tests it.

Neither is a defect in what was built. Both are **item-authoring gaps that were
invisible until the codes were mapped**, which is the argument for the mapping.

Smaller gaps, listed for the record: M17 (R2, R3, R4, R5), M19 (K6, K8, R5),
M20 (K8 two-blocking, R2, R5, R6, S5 verify anti-two-block), M22 (R5, R7, S3),
M23 (R5, R6).

## Outstanding

1. **Gen 3 retrofit** - keys to `platform/cq_keys_S4.json` (+72 records), assets
   externalized, `cq:*` event contract. All nine are still Gen 1 with `HASHES` baked
   client-side.
2. **ElevenLabs narration** - all nine run the `speechSynthesis` fallback. When audio
   ships, reconcile each overlay GATE to its 8-item engine GATE and re-run the suite.
3. **`S4_M14`'s next pointer** to `S4_M15` - the only edit any existing file needs.
4. **Item authoring for M18 and M21** - close the two coverage gaps above before those
   modules are harvested.

## Reproducibility

`tools/build_ar_module.py all <src> <out>` rebuilds the set deterministically from the
sources; configs live in `tools/ar_configs.py`. Re-running reproduced the already-shipped
`S4_M16` **byte-identically**, which is the regression check on the builder.
