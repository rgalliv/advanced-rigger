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
| **Advanced Rigger** | **9** | **25** | **6** (q19-q24) | **24%** | **client FNV (Gen 1)** |

Two things stand out.

**The house gate size is 8, not 6.** Stage 3 uses 8 across twelve of thirteen modules;
mobile crane Stage 4 uses 8 across eleven of twelve gated modules. Six is the Stage 2
minimum and the Stage 3 exception. Advanced Rigger sits at the low end.

**Advanced Rigger has by far the largest bank.** 25 items per module against Stage 6's
5. That is not a criticism - a 25-item bank with distribution control is a genuinely
better instrument. But it means **19 of 25 items per module carry no gate consequence**,
and that ratio needs a stated purpose.

### Recommendation

Keep the 25-item bank. **Raise the gate from 6 to 8** to match house convention, and -
more importantly - because six items cannot cover the ACS. See section 3.

If the gate stays at 6, say why in the ACS. An unexplained deviation from house
convention is the kind of thing that looks like an oversight during an audit even when
it was a decision.

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
module (7 K, 6 R, 5 S is typical). Each module gates **6 items**.

**Six items cannot measure twenty codes.** At most 6 codes per module are gate-measured;
the remaining 14 are either measured in the ungated 19 or not measured at all. Nothing
currently records which.

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

### Suggested gate composition target

For an 8-item gate against a ~20-code module:

| Band | Items | Rationale |
|---|---:|---|
| `K#` Knowledge | 3 | The definitions and mechanisms the rest depends on |
| `R#` Risk | 2 | The failure modes - what actually hurts people |
| `S#` Skill | 3 | Computation and procedure - the things a rigger does |

Skill-weighted, because Advanced Rigger is a doing stage. Adjust per module, but state
the split in the manifest so it is a decision on the record.

---

## 4. Gate item selection

Current: `q19-q24`, a fixed contiguous tail block, `review_offset` 18.

This is the same shape the mobile crane stages use - a fixed final block rather than a
sample - and it is right for a mastery gate. Keep it. Two notes:

**`review_offset` must track the gate start.** Advanced Rigger uses 18 with a gate at
q19, so the first gate item renders as "Final Question 1." CM-101 uses `review_offset` 6
with a gate at q07 for the same effect. If the gate moves to 8 items, it becomes
q18-q25 and `review_offset` becomes 17. Easy to miss.

**The 19 ungated items need a stated role.** They are currently just "the bank." Give
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
  of which **72 are gate** at an 8-item gate (54 at the current 6).
- Records carry module-hash matching, as the mobile crane Stage 4 registry does
  (112 records, "exact deterministic conversion").
- Verify **uniqueness and well-formedness** of every record before deployment.
- `platform/cq_keys_AR.json` is **never statically served.** Block the route.

For comparison, the mobile crane Stage 4 registry holds 112 records across 12 gated
modules; Stage 3 holds 291 rows with 102 gated. Advanced Rigger's 225 is the largest
bank in the platform, which is an argument for getting the registry right rather than an
argument against the bank size.

---

## 7. Open decisions

These need Russ, not analysis:

1. **Gate size: 6 or 8?** House convention says 8. Six is defensible if stated.
2. **Does the 25-item bank feed R2 exam prep directly**, or is it formative only? Changes
   how the ungated 19 are written and how neutrally they must record selections.
3. **Skill-coverage floor** - is "at least one `S#` in every gate" a rule or a
   preference?
4. **Who owns each of the four overlapping topics?** Four one-line decisions.
5. **Is the coverage map built before or after the ElevenLabs pass?** Recommend before -
   a coverage correction changes gate membership, and gate membership changes the overlay
   GATE set that the audio pass ships.
