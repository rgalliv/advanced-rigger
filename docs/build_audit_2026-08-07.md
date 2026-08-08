# Advanced Rigger - Independent Build Audit

7 August 2026. Run against the shipped artifacts, not the reports.

**Inputs:** 9 module HTML + 9 manifests + 9 instructor scripts, `S4_STAGE_crosscheck_report.md`,
`STATE.md`, `CQ_COURSE_MAP.md`, `CQ_STAGE_HANDOFF.md`, the pipeline tools,
`CQ_S4_ADVANCED_RIGGER_ACS_BUILD_MAP.md`, and one module from a second course
(`EM_M01`) built on the same template.

Every check below was recomputed from the shipped bytes.

---

## Verdict

**The build is high quality and the crosscheck report is accurate on everything it
measures.** I independently confirmed fourteen separate claims, including the two
hardest ones.

**But the answer keys are mechanically predictable, and the 12-point suite cannot see
it.** Six modules have a strict A-B-C-D repeating key. Eight of nine share an identical
gate sequence. The defect has already propagated to a second course.

This is not a content problem. The instruction is sound, the regulatory hygiene is
clean, the engine is correct. It is an item-security problem, and it is fixable
mechanically.

---

## 1. Confirmed PASS - independently recomputed

| # | Claim | Method | Result |
|---|---|---|---|
| 1 | FNV hash integrity | Recomputed `fnv1a(salt:qid:index)` for all 225 items, compared to baked hex | **225/225 exact match** |
| 2 | No distractor collisions | Hashed all 3 wrong indices per item against the baked value | **0 collisions** in 675 tests |
| 3 | Two-engine GATE parity | Parsed both `GATE = [...]` declarations per module | **Identical in all 9.** This is the Stage 2 "check that bites" - it passes |
| 4 | No plaintext answer keys | Searched `data-correct`, `Correct answer:`, `data-good` | **0 hits, all 9** |
| 5 | Platform metadata | `data-cq-total`, `data-cq-stage`, `data-cq-module` | Present, all 9 |
| 6 | FNV implementation | `Math.imul` + `0x01000193` | Present, all 9 - no overflow bug |
| 7 | Scoring shim | `scoreAnswer` + `window.CQ` | Present, all 9 |
| 8 | Engine tokens | `.every(`, `requestComplete`, `cq-module-complete` | Present, all 9 |
| 9 | Auto-advance | `advanceWhenReady` present, no fixed-delay timer | Confirmed, all 9 |
| 10 | Slide counts | `manifest.total` vs `data-cq-total` vs actual `<section class="slide">` | **Three-way match on all 9** |
| 11 | Slide-to-question mapping | Parsed every `cqAnswer(...)` call from HTML | **25 unique per module, 0 dupes, 0 missing** |
| 12 | De-leak | Extracted all 4 option texts per item, compared correct vs longest distractor | **0 violations.** Worst case +6 chars (spec is <=6) |
| 13 | Answer distribution + run | Recomputed from manifests | **7/6/6/6 and max-run-1 on all 9** |
| 14 | Regulatory hygiene | Scanned learner HTML, base64-stripped | **0 hits** on `1926.1418`, bare `B30`, non-ASCII, or vendor names |

On #14 - my first pass flagged vendor hits. That was my error: a case-insensitive `ITI`
match firing on "pos**iti**on" and "defin**iti**on". Case-sensitive with word boundaries
gives **zero** vendor references in any module. The crosscheck report was right.

---

## 2. FAIL - answer keys are mechanically predictable

### 2.1 Six modules use a strict ABCD cycle

Recomputed answer sequences, q01 through q18:

| Module | q01-q18 | Strict A,B,C,D cycle? |
|---|---|---|
| S4_M01 | `CADBACBDCABDACDBCA` | No - genuinely varied |
| S4_M02 | `ABDACBDCBDABDACABD` | No - genuinely varied |
| S4_M03 | `ABCDABCDABCDABC` `ABC` | **Near-total** - deviates only at position 16 |
| S4_M04 | `ABCDABCDABCDABCDAB` | **YES** |
| S4_M05 | `ABCDABCDABCDABCDAB` | **YES** |
| S4_M06 | `ABCDABCDABCDABCDAB` | **YES** |
| S4_M07 | `ABCDABCDABCDABCDAB` | **YES** |
| S4_M08 | `ABCDABCDABCDABCDAB` | **YES** |
| S4_M09 | `ABCDABCDABCDABCDAB` | **YES** |

A learner who notices the pattern answers eighteen of twenty-five questions correctly
without reading a single stem.

### 2.2 Eight of nine share an identical gate sequence

| Gate sequence | Modules |
|---|---|
| **D-A-B-D-C-A** | **M03, M04, M05, M06, M07, M08, M09** (+ EM_M01) |
| B-D-A-C-B-D | M01 |
| A-C-B-D-C-A | M02 |

Pass the M03 gate and you hold the gate key for M04 through M09 - six modules, each at
100% mastery, each blocking forward navigation.

### 2.3 Why the 12-point suite cannot catch this

Every relevant check is per-module and pattern-blind. Worse, a cycle **passes them
optimally**:

| Check | On a cycling key |
|---|---|
| Answer distribution 7/6/6/6 | Passes - a cycle is near-perfectly balanced by construction |
| Full-bank max consecutive run of 1 | **Passes perfectly** - a cycle never repeats consecutively. This is the best possible score |
| Gate all four letters present | Passes |
| Gate max consecutive run of 1 | Passes |
| De-leak | Unaffected - lengths, not positions |
| FNV integrity | Passes - the hash is correct *for whatever key it is given* |

**The max-run-1 rule is the trap.** It was written to stop `AAAA`, and a cycle is the
most efficient way to satisfy it. The check that was meant to enforce unpredictability
is the one the pattern optimises against.

The crosscheck report *prints* the gate sequence in a column - `DABDCA` appears seven
times in a row - and marks every row PASS. The evidence is on the page. There is no
cross-module uniqueness check to fire on it.

### 2.4 It has already propagated

`EM_M01` - a different course (`stage: "EM"`, salt `CQ1:EM_M01_ScopeAndApplicability`) -
has a **structurally identical answer key** to M04-M09: same ABCD cycle q01-q18, same
`DABDCA` gate, same `q25 = C`.

This is a template artifact, not nine independent authoring slips. Every module built
from the current `cq_content_MODEL_TEMPLATE.py` inherits it. **The fix has to land in
the template, or it regenerates.**

### 2.5 The fix

Bounded and mechanical. Question content is fine - only option *order* changes.

1. For each affected question, **permute the four options**.
2. **Re-derive `answer` from the correct option text**, never carry the old index
   forward. This is authoring bug #1 already documented in the ACS - it bit M08 q13/q16
   and M09 q17. It will bite again here if the reorder is done carelessly.
3. Re-bake the FNV hash from `salt : qid : new_index`.
4. Re-run the full suite. De-leak is unaffected by reordering (same text set), but
   verify anyway.

Scope: M03-M09 (7 modules) plus EM_M01. M01 and M02 are already clean and should not be
touched.

### 2.6 Checks to add

| Check | Criterion |
|---|---|
| **Key unpredictability** | No run of 8 or more items where the index advances by a constant step mod 4. Catches ABCD and DCBA alike |
| **Cross-module gate uniqueness** | No two modules in the platform share a gate answer sequence - including across courses |
| **Cross-module key correlation** | No two modules share more than 60% of their full 25-item key sequence position-for-position |

Run the last two **platform-wide**, not per stage. The EM_M01 collision only shows up
across courses.

---

## 3. Other findings

### 3.1 Zero ACS traceability in shipped artifacts

Searched every shipped file for the `S4.M0X.K#` / `.R#` / `.S#` pattern:

| Artifact set | ACS code references |
|---|---|
| 9 module HTML | **0** |
| 9 manifests | **0** |
| 9 instructor scripts | **0** |

The manifest key union across all nine is `answer_key, gate, gate_code, module, next,
review_offset, salt, stage, total, version`. **There is no `acs` field.**

Section 9 of the ACS specifies an `acs` array on every slide and every question. Section
0 states the purpose: *"Question banks, instructor scripts, and practical evaluations
cite those codes so any item traces back to the element it tests."*

169 coded elements are defined. **None is cited anywhere in a shipped artifact.** The
traceability layer exists as specification only. This confirms empirically what the
earlier gap analysis inferred.

### 3.2 Gate codes are compound; the shared half is not unique

Manifests carry `"gate_code": "R-201C / AR-101C"`. The `R-201C` half is **identical
across all nine AR modules and EM_M01**.

The crosscheck and `STATE.md` both claim "unique gate codes." That is true of the
`AR-10XC` half only. Not a defect if `R-201C` is a deliberate role-level code, but the
uniqueness claim should say which half it applies to.

### 3.3 Section ids will break CM-track tooling

Modules use `<section class="slide t-content" id="slide-4" data-idx="4">`.

The Second Brain build note for the Crane Mechanic track states: *"the tooling reads
slide numbers from `<section class="slide" id="sN">`. Sections without ids make the
verifier map every question to `null` and report false failures."*

`id="slide-N"` is not `id="sN"`. Zero modules match the expected pattern. Not a module
defect - the modules are internally consistent and carry `data-idx` - but any shared
verifier must be taught this selector, or it will report nine false failures.

Related: the ACS already notes `verify_module.cjs` is incompatible with the current
cohort, and `cq_verify_module.cjs` ships anyway.

### 3.4 Architecture generation confirmed

The audit confirms the earlier finding. These modules are **Gen 1**: keys baked into the
HTML as `HASHES={...}` hex, client-scored, `speechSynthesis`, no embedded audio
(`data:audio` absent - consistent with the deferred ElevenLabs pass), no externalized
assets.

Mobile crane Stage 4 is Gen 3 - server-only registry, externalized assets. Joining that
stage means the retrofit already specified in `module_format_spec.md`.

**The cycling-key defect sharpens this.** With keys baked client-side, anyone can read
`HASHES` and brute-force four values per item. A predictable key means they do not even
need to. Moving keys server-side removes the brute-force path; fixing the cycle removes
the guessing path. **Both are needed - neither substitutes for the other.**

---

## 4. Priority

| # | Item | Severity | Cost |
|---|---|---|---|
| 1 | **Fix `cq_content_MODEL_TEMPLATE.py` key generation** | **High** | Small - it regenerates otherwise |
| 2 | **Re-key M03-M09 and EM_M01** | **High** | Medium - 8 modules x 25 items, mechanical |
| 3 | **Add the three unpredictability checks** | **High** | Small |
| 4 | Build the ACS coverage map | Medium | Medium - judgement work |
| 5 | Gen 3 retrofit (keys server-side, assets out) | Medium | Medium |
| 6 | Gate 6 to 8 (q18-q25, `review_offset` 17) | Medium | Small - do it in the same pass as #2 |
| 7 | Teach the shared verifier the `id="slide-N"` selector | Low | Small |
| 8 | Clarify the compound gate-code uniqueness claim | Low | Trivial |

**Items 2, 6 and 5 should be one pass.** All three rewrite the question block and
re-bake hashes. Doing them separately means baking the hashes three times.

---

## 5. What this does not change

The instructional content is not implicated. The ACS is well constructed, the regulatory
rail holds under scan, the de-leak discipline is real and measurably tight (+6 worst
case against a +6 limit), the engine is correct, and the two-engine GATE parity - the
single hardest invariant in the house architecture - passes on all nine.

The stage is closer to done than this document's length suggests. But **"COMPLETE and
fully verified end to end" is not currently accurate**, and the gap is in the
verification, not the build.
