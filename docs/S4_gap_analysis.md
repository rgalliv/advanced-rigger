# Advanced Rigger (Stage 4) - ACS Gap Analysis

Rev 0.1 - 7 August 2026

Read alongside `S4_source_register.md`. That document covers sourcing and tiers. This
one covers structure: what the ACS asserts, what the verification suite actually
proves, and what the harvest courses will need that neither currently provides.

**Scope note.** This analysis is built from the Stage 4 ACS Build Map HTML and the
Second Brain (Notion). The `.md` file referenced in the request did not arrive - see
"Inputs" at the end.

---

## What is solid

Worth stating first, because the rest of this document is gaps.

- **The verification suite is genuinely strong.** Twelve checks, all nine modules,
  including FNV-1a hash integrity over 225 items with 0 collisions, `node --check` on
  27 script blocks, and 117 jsdom behavioural checks with 0 failures. The de-leak
  check (correct option within 6 characters of the longest distractor) and the
  max-consecutive-run-of-1 constraint are the kind of item-writing discipline most
  training vendors never apply at all.
- **The regulatory rail is precise where it matters.** Pinning stop-work authority to
  29 CFR 1926.1419(j) and scanning every build for the commonly confused neighbouring
  section is exactly right. So is holding the 1926.1419(a) signal-person condition
  count at exactly three and refusing to inflate it.
- **The physics honesty rule in M08** - "No standard is cited for a mechanics result
  that no standard actually states" - is a discipline worth propagating to every
  other stage.
- **M01's parity cross-check against Stage 2 M04** is the right instinct: same
  formula, same convention, same stability rule, confirmed with no edits.

---

## Gap 1 - ACS codes are not traceable to questions

This is the most consequential structural gap.

The ACS masthead states the purpose of the coding scheme:

> Codes are stable identifiers - cite them in question banks, instructor scripts, and
> practical evaluations so a question can always be traced back to the element it
> tests.

The verification suite checks **slide-to-question** mapping (25 unique references, no
duplicates, none missing). It does **not** check **code-to-question** mapping. So the
traceability the ACS exists to provide is asserted but never demonstrated.

Stage 4 defines roughly 180 ACS codes across 9 modules and carries 225 questions. With
no map between them, three questions cannot currently be answered:

- Which codes are gate-tested (the gate questions at 100% mastery) versus merely present
  in the 25-item bank?
- Which codes are taught but never tested at all?
- When the R2 exam prep harvests "M01-M05 and M07," which codes come with it?

**The CM track already solved this.** CM-101's build spec states:

> **Measured ACS coverage: K1, K3, K5, K6, K8.** K2, K4 and K7 are taught without
> being gate-tested - a visible decision rather than an accident.

That last clause is the whole point. Untested coverage is fine. Untested coverage you
cannot enumerate is not.

CM-101 also records a specific correction of exactly this kind: a K3 question was
swapped in on 1 August, replacing a duplicate K6 question, "so the
demonstrated-problem-resolution test at the centre of the 1401 definition is now
measured." That correction was only findable because the coverage map existed.

**Fix.** Add two fields to each `S4_MXX_manifest.json` and one check to the suite:

- `acs_coverage.gate` - codes measured by the gate block (q18-q25 as of the 8-item
  decision; see `AR_question_architecture.md`)
- `acs_coverage.bank` - codes measured elsewhere in the 25
- `acs_coverage.taught_only` - codes present in slides, deliberately untested
- New verification check: every code in the module's ACS plate appears in exactly one
  of the three lists, and every code referenced by a question exists in the ACS.

Given the stage is built and verified, this is a documentation pass over existing
content, not a rebuild.

---

## Gap 2 - no declared module boundaries

CM-101 names what it does **not** teach and says who owns it:

> **Boundary only - named, not taught:** 1429(a) diagnostic operation -> CM-207
> (Phase II, discrete gated module with a signed acknowledgment; the highest drift
> risk in the track). CM-101 states the standing rule and hands off.

Stage 4 has several topics living in two modules with no declared owner:

| Topic | Appears in | Risk |
|---|---|---|
| Angle factors / leg tension | `S4.M02.K1-K3` and `S4.M03.K5` | M02 teaches the house method (LAF = leg length / headroom); M03 teaches "angle factors as a lookup and as trigonometry." Two methods, same quantity. **Which is canonical on a conflict?** |
| Snatch block resultant force | `S4.M06.K4`, `S4.M06.S2` and `S4.M08.S4` | M08 says "size a snatch block and its anchor to the resultant" - is it re-teaching M06 or assuming it? |
| Combined weight against the crane chart | `S4.M07.K7`, `S4.M07.S4` and `S4.M09.K8`, `S4.M09.S3` | Stated twice as a rule. Capstone reinforcement is legitimate, but it should say so. |
| D/d ratio | `S4.M03.K4` and `S4.M06.K6` | Sling efficiency vs sheave groove fit. Related but not identical - easy for a learner to conflate. |

None of these are errors. All of them are decisions that were made and not recorded,
which means the harvest courses will have to re-make them from scratch.

**Fix.** Add a `boundaries` block to each module's ACS plate: `owns`, `reinforces`,
`hands off to`. Cheap, and it makes the seven downstream courses far less expensive to
scope.

---

## Gap 3 - no negative source declaration

CM-101 closes its source list with a single sentence that does a lot of work:

> **Not used:** EM 385-1-1 18-4 (not re-verified) and NAVFAC P-307's Crane Mechanic
> category (still unopened). **The module cites no document the team has not read.**

Stage 4 has no equivalent. That matters most for M09, whose Source gap note admits the
BTH-1 numeric criteria are paraphrased from a secondary reference - but does not say
which documents were considered and set aside, or why.

**Fix.** Add a `Not used` line per module. One sentence. It is the cheapest audit
artifact in the entire CM pattern and the most useful under challenge.

---

## Gap 4 - "per manifest" is load-bearing and unverifiable here

Seven of nine modules show `per manifest` for slide count and salt. The ACS footer is
explicit and correct about why:

> Fields shown as "per manifest" live in the shipped `S4_MXX_manifest.json` and are
> not restated here rather than approximated.

That is the right call - restating drifts. But it means the ACS cannot be audited
standalone, and **no manifest files, module HTML, or the
`S4_STAGE_crosscheck_report.md` are present in this repository or in Drive.** The
stage's own crosscheck report of record is currently unlocatable.

M01, M02 and M09 do carry concrete values (54, 46 and 52 slides; two full salts), which
suggests the others are simply not transcribed rather than unknown.

**Fix.** Get the nine manifests and the crosscheck report into version control. The CM
register's standing rule applies directly: *build from the archive, never from a URL.*

---

## Gap 5 - the audio item is understated

The ACS calls the ElevenLabs re-record pass "the only production task outstanding" and
"deferred, not blocked." All nine modules run on the speechSynthesis fallback.

The CM track flags a dependency Stage 4's open-work table does not mention. From the
CM-101 build status:

> **Behavioural verify** - 3 of 4 groups pass. TEST 1 (per-question lock) belongs to
> the `cq-slide-audio-flow` overlay, **which ships with narration**.

and

> **Re-run pipeline after narration** - retrofit then reconciles the overlay GATE to
> the manifest.

So narration is not a cosmetic layer. On the CM architecture it carries a
behavioural test and requires a **post-narration pipeline re-run** to reconcile the
overlay gate against the manifest.

Stage 4 reports 117 jsdom checks with 0 failures and 13/13 per module, which reads like
full behavioural coverage. If Stage 4 shares the `cq-slide-audio-flow` overlay, then
either the per-question lock is covered by a different mechanism here, or those 13
checks do not include it and the count will change after the audio pass.

**This is a question, not a finding** - I do not have the module HTML to confirm which
overlay Stage 4 uses. But it should be answered before the stage is called done:
**does the ElevenLabs pass require a retrofit re-run and re-verification, or not?** If
it does, "the only production task outstanding" is really "the last build step,"
and the 13/13 figure is provisional.

---

## Gap 6 - the harvest plan has no source-cost column

The downstream table lists seven courses, 35 modules, with donor modules and a revenue
note each. It has no column for **what each course must acquire before it can ship.**

From the source register, the acquisitions are unevenly distributed:

| Course | Blocking acquisition | Severity |
|---|---|---|
| **RI** - Rigging Equipment Inspection | Removal criteria precision for M04/M05. Hanford Ch 5/8/10/17 likely covers much of it (Tier 1, free). Residual B30.26 exposure. | **High** - "the numbers become the product" |
| **R2** - NCCCO Rigger Level II Prep | Harvests M01-M05 and M07, all currently leaning on the NCCCO Rigger Reference Manual (Tier 2b). An exam-prep product grounded on the certifying body's own manual needs the reword discipline applied hard. | **High** |
| **TM** - Tandem and Multi-Crane | Sits on M07 load-share math, which is the most Tier-1-thin module in the stage (Tucker + TR244C + NCCCO, all 2b or unknown). | **Medium** |
| **BR** - Bull Rigging | M08 seed. SC&RA guidebook and "Drifting With Chain Hoist" are both GAP - no copy located. | **Medium** |
| **PH** - Personnel Hoisting | Anchors to 1926.1431 (Tier 1, free) and B30.23 (Tier 2a, not held). | **Medium** |
| **LT** - Load Turning | Extends M01, which has the best Tier 0 grounding in the stage. | **Low** |
| **LP** - Lift Planning | Pairs with the existing field kit. Largely Tier 0. | **Low** |

The two courses flagged highest revenue (R2 and RI) are also the two with the highest
sourcing exposure. That is worth knowing before build order is set.

---

## Build-method warning that applies to the harvest courses

The CM track recorded a corrected build method that Stage 4's successors should not
have to rediscover. From `05 - Modules`:

> **Build method - corrected from the earlier recommendation.** This page previously
> recommended authoring in Stage-1 forge lineage with FNV hashes baked in by hand.
> **That was wrong** - there is no Stage-1 reference module to copy a validated engine
> from, so hand-writing one risks drift from the byte-validated original.
>
> **What was done instead:** author the DOM to the Stage-2 contract and let `retrofit`
> inject the kit's own validated engine. Same destination, no hand-rolled crypto, and
> the module rebuilds from its manifest forever.

And one concrete trap:

> **One DOM requirement:** the tooling reads slide numbers from
> `<section class="slide" id="sN">`. Sections without ids make the verifier map every
> question to `null` and report false failures.

Stage 4 is already built and passing, so this is not retroactive. It applies to the 35
harvest modules.

---

## Priority order

1. **Assign a tier to TR244C** - cited by all nine modules, currently unknown. Blocks
   clean provenance on the entire stage.
2. **Build the ACS code-to-question map** - documentation pass over built content,
   unblocks every harvest course's scoping.
3. **Answer the narration/retrofit question** - determines whether the stage is done
   or one step from done.
4. **Get manifests + crosscheck report into version control** - the stage's audit
   trail currently has no home.
5. **Read Hanford Ch 5/8/10/17 against M03-M05** - free, and likely retires most of the
   B30.9/B30.26 open item before the RI build.
6. **Acquire ASME BTH-1** - the only gate-tested numeric criteria in the stage resting
   on a Tier 2b secondary source.
7. **Resolve the vendor-naming rail conflict** - one sentence either way.
8. **Declare module boundaries** - makes the seven harvest courses cheaper to scope.

Items 1 through 4 are documentation over work already done. Items 5 through 8 are
decisions. Only item 6 costs money.

---

## Inputs

| Input | Status |
|---|---|
| Stage 4 ACS Build Map (HTML) | Received in full (transmitted twice, identical) |
| The `.md` file | **Not received.** The repository was empty at session start (no commits) and no matching file was found in Drive. If this is `S4_STAGE_crosscheck_report.md`, it is also the file named in Gap 4. |
| Notion Second Brain | Scanned - CraneQualified HQ, Crane Technician Open Source Register (pages 01-06), Prolevari Master KB |
| Google Drive | Scanned for Advanced Rigger, rigging, rigger, TR244, Journeyman, worksheet, S4_, crosscheck, ACS |

**Nothing in this document depends on the missing `.md` file** - it is built from the
ACS and the Second Brain. But Gap 4 and Gap 5 would likely be answered by it.
