# Advanced Rigger - Question Architecture

Rev 0.2 - 7 August 2026

Companion to `module_format_spec.md`. That document covers the module shell and the
scoring transport. This one covers the items: how many, how they are selected, how they
map to the ACS, and what makes one conformant.

The nine Advanced Rigger modules join Stage 4 as `S4_M15` through `S4_M23` and follow
house conventions throughout.

---

## 1. Gate size - 8, matching the stage

| Stage | Modules | Bank per module | Gate per module | Scoring |
|---|---:|---|---:|---|
| Stage 2 | 10 | slide-linked bank | 6 or 8 | client FNV, two-engine |
| Stage 3 | 13 | 291 rows, 102 gated | 8 (M02: 6) | server |
| **Stage 4 M01-M14** | 14 | - | **8** (M01: 24; M06/M07: 0) | server, protected registry |
| Stage 6 | 7 | 5 | 5 | server, runtime-scored |
| **Stage 4 M15-M23** | **9** | **25** | **8** (q18-q25) | server, protected registry |

Eight is the Stage 4 norm - eleven of the twelve gated modules use it. The Advanced
Rigger build used 6 (q19-q24), which was the Stage 2 minimum. It moves to 8.

### What the move changes

| | Was | Now |
|---|---|---|
| Gate block | q19-q24 | **q18-q25** |
| `review_offset` | 18 | **17** |
| Ungated bank | 19 items | **17 items** |
| New registry records | 54 | **72** |
| Max ACS codes gate-measured per module | 6 | **8** |
| Gate letter balance | cannot be even across 4 letters | **2/2/2/2 - exactly even** |

That last row is a real gain. With 6 items across 4 letters the gate can never balance;
two letters appear once and two appear twice. **At 8 it balances exactly.** Tighten the
check:

| Check | Was | Now |
|---|---|---|
| Gate composition | All four letters present; max consecutive run of 1 | **Exactly 2 of each letter**; max consecutive run of 1 |

The full-bank 7/6/6/6 distribution across all 25 items is unaffected.

**Two items per module enter the gate for the first time.** They were written as bank
items and were never held to gate standards. They must now clear de-leak and run-length
like any gate item. Do not assume they pass.

### Gate item selection

`q18-q25`, a fixed contiguous tail block, `review_offset` **17**.

A fixed final block rather than a random sample is right for a mastery gate and is what
every stage uses.

**`review_offset` is the easiest thing to get wrong in this move.** It must equal the
first gate index minus 1. Leaving it at 18 with a gate starting at q18 would label the
block "Final Question 0" and silently misnumber all eight. Add a check:
`review_offset == first_gate_index - 1`.

### The 17 ungated items

They are formative. They **record the learner selection neutrally** - no
machine-readable correctness, no registry record, per the public/protected boundary.

Their stated role: **practice plus item-bank reserve for the R2 exam prep harvest.**
Write them to gate quality even though they are not gated, because R2 will draw from
them and the harvest should not require a rewrite.

---

## 2. Item-writing rules

Advanced Rigger already enforces these and no mobile crane package documents an
equivalent. They carry forward unchanged.

| Rule | Criterion |
|---|---|
| Answer distribution | 7/6/6/6 across A/B/C/D per 25-item bank |
| Full-bank run | Max consecutive same-answer run of 1 |
| Gate composition | Exactly 2 of each letter; max consecutive run of 1 |
| De-leak | Correct option within 6 characters of the longest distractor |
| Slide mapping | 25 unique slide references, no duplicates, none missing |
| ASCII | No em-dash, en-dash, smart quote, ellipsis, non-breaking space |
| Regulatory | Correct stop-authority citation; specific ASME volume named; no unqualified series reference; no named vendor |

**Why de-leak matters more than it looks.** The most reliable way to guess a
multiple-choice answer without knowing the content is to pick the longest, most-qualified
option. A 6-character band removes that tell. Most commercial rigging banks - including
the legacy `Advanced_Rigging_40_Question_Test` in Drive - fail this badly.

### One rule added

**Distractor plausibility must trace to a risk code.** Every distractor should be
something a real rigger would actually do wrong, and the ACS already enumerates those:
the `R#` codes. A distractor mapping to no `R#` is either implausible - a free point -
or tests something the ACS does not claim to teach.

Cheap to check, and it forces the risk column to earn its place.

---

## 3. ACS coverage mapping

This is the substantive gap, and no mobile crane package helps, because none ships an
ACS at all.

### The problem

Advanced Rigger defines roughly **180 ACS codes** across 9 modules - averaging 20 per
module (7 K, 6 R, 5 S is typical). Each module gates **8 items**.

**Eight items cannot measure twenty codes.** At most 8 codes per module are
gate-measured; the remaining 12 are measured in the ungated 17 or not at all. Nothing
records which. Moving 6 to 8 raised the ceiling by two codes per module; it did not
remove the need for the map.

The ACS states the purpose of its own codes:

> cite them in question banks, instructor scripts, and practical evaluations so a
> question can always be traced back to the element it tests

The suite checks **slide-to-question**. It never checks **code-to-question**. The stage's
central claim about its coding scheme is asserted and unproven.

### The pattern to adopt

The Crane Mechanic track solved this for CM-101:

> **Measured ACS coverage: K1, K3, K5, K6, K8.** K2, K4 and K7 are taught without being
> gate-tested - **a visible decision rather than an accident.**

That phrase is the design. Untested coverage is fine and unavoidable. Untested coverage
you cannot enumerate is not.

It paid off concretely: a duplicate gate question was found and swapped for one testing a
different code. **That correction was only findable because the map existed.**

### Manifest schema

Add to each `S4_M15_manifest.json` .. `S4_M23_manifest.json`:

```json
{
  "acs_coverage": {
    "gate":        ["S4.M15.K3", "S4.M15.K5", "S4.M15.R3", "S4.M15.S1", "..."],
    "bank":        ["S4.M15.K1", "S4.M15.K2", "..."],
    "taught_only": ["S4.M15.K7", "S4.M15.R6"]
  },
  "item_codes": {
    "q01": ["S4.M15.K1"],
    "q18": ["S4.M15.S1", "S4.M15.K3"]
  }
}
```

`item_codes` is the primary record; `acs_coverage` is derived from it and from gate
membership. Store both - the derived view is what a reviewer reads.

### New checks

| Check | Criterion |
|---|---|
| Coverage completeness | Every code in the module's ACS plate appears in exactly one of `gate` / `bank` / `taught_only` |
| Referential integrity | Every code in `item_codes` exists in the module's ACS plate |
| Gate derivation | `acs_coverage.gate` equals the union of `item_codes` for q18-q25 |
| Taught-only declared | `taught_only` is non-empty **or** explicitly declared empty - never absent |
| Skill coverage floor | **At least two `S#` codes in every gate** |
| Review offset | `review_offset == first_gate_index - 1` |

### Gate composition target

For the 8-item gate against a ~20-code module:

| Band | Items | Rationale |
|---|---:|---|
| `K#` Knowledge | 3 | The definitions and mechanisms the rest depends on |
| `R#` Risk | 2 | The failure modes - what actually hurts people |
| `S#` Skill | 3 | Computation and procedure - what a rigger does |

Skill-weighted, because Advanced Rigger is a doing stage. The skill floor is set at
**two**, not one: at a 3-item skill target, a floor of one allows a module to drift to
near-pure recall while still passing. State the split per module in the manifest.

---

## 4. Cross-module integrity

Retain the existing checks - unique salts, unique gate codes, unbroken next-chain - and
add:

| Check | Criterion |
|---|---|
| Code uniqueness | No ACS code appears in two modules' plates. Shared concepts are declared via the boundary block, not duplicated codes |
| Boundary declaration | Where two modules touch the same topic, exactly one declares `owns` and the other declares `reinforces` |
| Gate code chain | `AR-101C` .. `AR-109C`, unique, no gaps |
| Stage chain | `S4_M14` to `S4_M15`; `S4_M23` terminates Stage 4 |

Four known overlaps need a declared owner. Calling them, defaulting to the module that
teaches the mechanism rather than the one that applies it:

| Topic | Modules | Owner | Other |
|---|---|---|---|
| Angle factors / leg tension | M16, M17 | **M16 owns** - house LAF method is taught there | M17 reinforces |
| Snatch block resultant | M20, M22 | **M20 owns** - resultant is a blocks-and-sheaves mechanism | M22 reinforces |
| Combined weight vs chart | M21, M23 | **M21 owns** - introduced with lifting devices | M23 reinforces as capstone |
| D/d ratio | M17, M20 | **Split - not an overlap.** M17 owns sling efficiency; M20 owns sheave groove fit | Declare both, cross-reference |

D/d is the one worth care: the two modules use the same term for different quantities.
Define each at first use and cross-reference explicitly, or learners will conflate them.

---

## 5. Decisions

### Settled

| # | Decision |
|---|---|
| 1 | **Gate size 8** - q18-q25, `review_offset` 17, letters 2/2/2/2 |
| 2 | **New modules in an existing stage** - `S4_M15`-`S4_M23`, nothing overwritten |
| 3 | **Ungated 17 are formative plus R2 harvest reserve** - written to gate quality, scored neutrally |
| 4 | **Skill floor is a rule, set at two `S#` per gate** |
| 5 | **Topic owners assigned** - see section 4 |
| 6 | **Coverage map before the ElevenLabs pass** - gate membership must be final before the overlay ships |

### Open

Nothing blocking. The remaining judgement calls sit inside step 7 of the build sequence -
which specific codes land in each module's gate - and those are made module by module
while building the map.
