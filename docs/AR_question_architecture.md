# Advanced Rigger - Question Architecture

Rev 0.1 - 7 August 2026

Companion to `AR_module_format_spec.md`. That document covers the module shell and the
scoring transport. This one covers the items: how many, how they are selected, how they
map to the ACS, and what makes one conformant.

Benchmarked against the mobile crane process in `Developer Handoff - July`. Architecture
and conventions only - no crane-operator content, no question wording.

---

## 1. House gate conventions, observed

| Stage | Modules | Bank per module | Gate per module | Gate as share of bank | Scoring |
|---|---:|---|---:|---|---|
| Stage 2 | 10 | full slide-linked bank | 6 or 8 | - | client FNV, two-engine |
| Stage 3 | 13 | 291 rows total, 102 gate | 8 (M02: 6) | - | server |
| Stage 4 (mobile crane) | 14 | - | 8 (M01: 24; M06/M07: 0) | - | server, protected registry |
| Stage 6 | 7 | 5 | 5 | 100% | server, runtime-scored |
| **Advanced Rigger** | **9** | **25** | **8** (q18-q25) | **32%** | **client FNV (Gen 1) - retrofit pending** |

**DECIDED 7 Aug 2026: gate size is 8.** This matches house convention - Stage 3 uses 8
across twelve of thirteen modules, mobile crane Stage 4 across eleven of twelve gated
modules. The original Advanced Rigger build used 6 (q19-q24), which was the Stage 2
minimum and the Stage 3 exception.

### What moving 6 to 8 changes

| | Was | Now |
|---|---|---|
| Gate items | q19-q24 | **q18-q25** |
| `review_offset` | 18 | **17** |
| Ungated bank | 19 items | **17 items** |
| Gate records per stage | 54 of 225 | **72 of 225** |
| Max ACS codes gate-measured per module | 6 | **8** |
| Gate letter balance | 4 letters over 6 items - cannot be even | **2/2/2/2 - exactly even** |

That last row is a real gain, not bookkeeping. With 6 items across 4 letters the gate
can never be balanced; two letters always appear once and two appear twice. **With 8 it
balances exactly.** Tighten the gate-composition check accordingly:

| Check | Was | Now |
|---|---|---|
| Gate composition | All four letters present; max consecutive run of 1 | **Exactly 2 of each letter**; max consecutive run of 1 |

The full-bank 7/6/6/6 distribution across all 25 items is unaffected and stays as is.

**Advanced Rigger still has by far the largest bank** - 25 items per module against
Stage 6's 5. That is a strength, not a problem. But 17 of 25 items still carry no gate
consequence, and that ratio needs a stated purpose. See section 4.

---

## 2. Item-writing rules (retain - these are the stage's best asset)

Advanced Rigger already enforces these. No mobile crane package documents an equivalent.
They are the reason the bank is worth harvesting, and they carry forward unchanged.

| Rule | Criterion |
|---|---|
| Answer distribution | 7/6/6/6 across A/B/C/D per 25-item bank |
| Full-bank run | Max consecutive same-answer run of 1 |
| Gate composition | All four letters present; max consecutive run of 1 |
| De-leak | Correct option within 6 characters of the longest distractor |
| Slide mapping | 25 unique slide references, no duplicates, none missing |
| ASCII | No em-dash, en-dash, smart quote, ellipsis, non-breaking space |
| Regulatory | Correct stop-authority citation; specific ASME volume named; no unqualified series reference; no named vendor |

**Why de-leak matters more than it looks.** The single most reliable way to guess a
multiple-choice answer without knowing the content is to pick the longest, most-qualified
option. A 6-character band removes that tell. Most commercial rigging banks - including
the legacy `Advanced_Rigging_40_Question_Test` in Drive - fail this badly.

### One rule to add

**Distractor plausibility must be traceable to a risk code.** Every distractor should be
a thing a real rigger would actually do wrong, and the ACS already enumerates those:
the `R#` codes. A distractor that maps to no `R#` is either implausible (free point) or
tests something the ACS does not claim to teach.

This is cheap to check and it forces the risk column to earn its place.

---

## 3. ACS coverage mapping - the missing layer

This is the substantive gap, and it is the thing the mobile crane packages cannot help
with, because none of them ship an ACS at all.

### The problem, stated precisely

Advanced Rigger defines roughly **180 ACS codes** across 9 modules - averaging 20 per
module (7 K, 6 R, 5 S is typical). Each module gates **8 items**.

**Eight items cannot measure twenty codes.** At most 8 codes per module are
gate-measured; the remaining 12 are either measured in the ungated 17 or not measured at
all. Nothing currently records which. Moving 6 to 8 improved the ceiling by two codes
per module - it did not remove the need for the map.

The ACS masthead states the purpose of the codes:

> cite them in question banks, instructor scripts, and practical evaluations so a
> question can always be traced back to the element it tests

The verification suite checks **slide-to-question** mapping. It never checks
**code-to-question**. So the stage's central claim about its own coding scheme is
asserted and unproven.

### The pattern to adopt

The Crane Mechanic track (Second Brain, `05 - Modules`) already solved this for CM-101:

> **Measured ACS coverage: K1, K3, K5, K6, K8.** K2, K4 and K7 are taught without being
> gate-tested - **a visible decision rather than an accident.**

That last phrase is the whole design. Untested coverage is fine and unavoidable.
Untested coverage you cannot enumerate is not.

It paid off concretely: a duplicate gate question was found and swapped for one testing
a different code, "so the demonstrated-problem-resolution test at the centre of the
definition is now measured." **That correction was only findable because the map
existed.**

### Manifest schema

Add to each `AR_MXX_manifest.json`:

```json
{
  "acs_coverage": {
    "gate":        ["AR.M01.K3", "AR.M01.K5", "AR.M01.R3", "AR.M01.S1", "..."],
    "bank":        ["AR.M01.K1", "AR.M01.K2", "..."],
    "taught_only": ["AR.M01.K7", "AR.M01.R6"]
  },
  "item_codes": {
    "q01": ["AR.M01.K1"],
    "q19": ["AR.M01.S1", "AR.M01.K3"]
  }
}
```

`item_codes` is the primary record; `acs_coverage` is derived from it and from which
question ids sit in the gate. Store both - the derived view is what a reviewer reads.

### New verification checks

| Check | Criterion |
|---|---|
| Coverage completeness | Every code in the module's ACS plate appears in exactly one of `gate` / `bank` / `taught_only` |
| Referential integrity | Every code in `item_codes` exists in the module's ACS plate |
| Gate derivation | `acs_coverage.gate` equals the union of `item_codes` for the gate question ids |
| Taught-only declared | `taught_only` is non-empty **or** explicitly declared empty - never absent |
| Skill coverage floor | At least one `S#` code in the gate. A gate of pure recall does not test a rigger |

That last one is a judgement call worth encoding. The ACS separates Knowledge, Risk and
Skill deliberately. A gate that samples only `K#` codes measures whether the learner
read the slides, not whether they can rig.

### Gate composition target

For the 8-item gate against a ~20-code module:

| Band | Items | Rationale |
|---|---:|---|
| `K#` Knowledge | 3 | The definitions and mechanisms the rest depends on |
| `R#` Risk | 2 | The failure modes - what actually hurts people |
| `S#` Skill | 3 | Computation and procedure - the things a rigger does |

Skill-weighted, because Advanced Rigger is a doing stage. Adjust per module, but state
the split in the manifest so it is a decision on the record.

---

## 4. Gate item selection

**Target: `q18-q25`, a fixed contiguous tail block, `review_offset` 17.**

A fixed final block rather than a random sample is the right shape for a mastery gate,
and it is what every mobile crane stage uses. Two notes:

**`review_offset` must track the gate start.** With the gate at q18, `review_offset` 17
makes the first gate item render as "Final Question 1." The original build used 18 with a
gate at q19; CM-101 uses 6 with a gate at q07. **This is the single easiest thing to get
wrong in the 6-to-8 move** - an unchanged offset of 18 would label the gate
"Final Question 0" and silently misnumber all eight.

Add a check: `review_offset` equals `(first gate question index) - 1`.

**The 17 ungated items need a stated role.** They are currently just "the bank." Give
them a purpose in the ACS - formative practice, spaced review, or item-bank reserve for
the R2 exam prep harvest. Whichever it is, the public formative activities must
**record the learner selection neutrally** with no machine-readable correctness, per the
public/protected boundary.

---

## 5. Cross-module integrity

Advanced Rigger already checks unique salts, unique gate codes, and an unbroken
next-chain. Retain, with the renames from the format spec, and add:

| Check | Criterion |
|---|---|
| Code uniqueness | No ACS code appears in two modules' plates. Shared concepts are declared via the boundary block, not duplicated codes |
| Boundary declaration | Where two modules touch the same topic, exactly one declares `owns` and the other declares `reinforces` |
| Gate code chain | `AR-101C` .. `AR-109C`, unique, no gaps |
| Terminus | `AR_M09` chains to `AR_COMPLETE` |

The boundary check matters for four known overlaps: angle factors (M02/M03), snatch-block
resultant (M06/M08), combined weight against the chart (M07/M09), and D/d ratio
(M03/M06). None is an error. All four are undeclared.

---

## 6. Protected registry

Once keys move server-side per the format spec:

- One record per scored item. Advanced Rigger: **9 modules x 25 items = 225 records**,
  of which **72 are gate** (9 x 8).
- Records carry module-hash matching, as the mobile crane Stage 4 registry does
  (112 records, "exact deterministic conversion").
- Verify **uniqueness and well-formedness** of every record before deployment.
- `platform/cq_keys_AR.json` is **never statically served.** Block the route.

For comparison, the mobile crane Stage 4 registry holds 112 records across 12 gated
modules; Stage 3 holds 291 rows with 102 gated. Advanced Rigger's 225 is the largest
bank in the platform, which is an argument for getting the registry right rather than an
argument against the bank size.

---

## 7. Decisions

### Settled

| # | Decision | Date |
|---|---|---|
| 1 | **Gate size is 8** (q18-q25, `review_offset` 17, 2/2/2/2 letter balance) | 7 Aug 2026 |
| 2 | **New modules are renamed, not overwritten.** `AR_M01`-`AR_M09` are built as new artifacts. No existing module file is modified or replaced. | 7 Aug 2026 |

### Still open

3. **Does the 25-item bank feed R2 exam prep directly**, or is it formative only? Changes
   how the ungated 17 are written and how neutrally they must record selections.
4. **Skill-coverage floor** - is "at least one `S#` in every gate" a rule or a
   preference? With 8 items and a 3/2/3 target it is comfortably satisfiable either way.
5. **Who owns each of the four overlapping topics?** Angle factors (M02/M03),
   snatch-block resultant (M06/M08), combined weight (M07/M09), D/d ratio (M03/M06).
   Four one-line decisions.
6. **Is the coverage map built before or after the ElevenLabs pass?** Recommend before -
   a coverage correction changes gate membership, and gate membership changes the overlay
   GATE set that the audio pass ships. The 6-to-8 move makes this sharper, not softer:
   two items per module are entering the gate for the first time.
