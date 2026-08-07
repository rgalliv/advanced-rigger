# Advanced Rigger (Stage 4) - Source Register

Rev 0.1 - 7 August 2026 - CraneQualified Program

Companion to the Stage 4 ACS Build Map (S4_M01 through S4_M09).

This register applies the tier model already adopted by the Crane Technician track
(Open Source Register, Gate Master Rev 1.3 Section 11, amendments A1 and A2) to the
Advanced Rigger stage. Stage 4 shipped with a prose "Sources" line per module and no
tier assignment. That is the gap this document closes.

---

## Why this exists

Every source in the Stage 4 ACS is free to *access*. That is not the same as free to
*quote*. The Crane Technician register states the rule plainly and it carries over
unchanged:

> The tier is the only thing that matters when building content.

Stage 4 is finished and verified as a learning product. It is not yet documented to
the standard the harvest courses will need, because the moment M04 removal criteria
and M05 hardware become the Rigging Equipment Inspection course, **the numbers become
the product** - and a number sourced from a Tier 2b commercial manual is a liability
in a way that the same number sourced from Tier 1 is not.

---

## Tier model (inherited, unchanged)

| Tier | Status | Build rule |
|---|---|---|
| **Tier 0** | MSC / CCOS / CraneQualified own IP - 141 decks, 17,094 slides | It is ours. Quote freely, reuse freely. **Check here first, before any external source.** |
| **Tier 1** | U.S. Government work - public domain, no copyright | Quote and adapt freely. Attribute for credibility, not for permission. |
| **Tier 2a** | ASME B30.x, BTH-1, OEM literature | State requirements **in our own words with attribution** ("per ASME B30.9..."). Never reproduce their tables, figures or wording; never track their sentence structure. (Rev 1.3 amendment A1) |
| **Tier 2b** | NCCER, IPT, ITI, NCCCO, SC&RA - owned or licensed commercial curriculum | **Reference, never quote, always reword.** The underlying content is common knowledge; rewording removes any copyright question. |
| **Tier 3** | Paid, gated, or licensed - not held | Listed so the team never assumes coverage that does not exist. |

**Standing caution.** Some Tier 1 documents reproduce ASME/ANSI text verbatim under
their own licensing arrangements. The government document is public domain; the
consensus-standard text inside it is not ours to lift. Flagged with a dagger below.

---

## Verification marks

| Mark | Meaning |
|---|---|
| OK | Retrieved and content-verified against the source's own text |
| LIVE | Located and identified; content not independently re-read this pass |
| ? | **Tier not yet assigned** - provenance unconfirmed |
| GAP | Named in the ACS but no copy located in Drive or the vault |

---

## Stage 4 cited sources, tiered

Sources are taken from the `Sources` line in each module's ACS plate.

| Source as cited in the ACS | Tier | Mark | Cited by | Notes |
|---|---|---|---|---|
| Russ's rigging worksheet (house method) | **0** | LIVE | M02 | `Rigging Worksheet - Version 2.docx`, Drive, rev 24 Apr 2025. The LAF = leg length / headroom house method. Worked examples reuse its numbers so classroom and e-learning agree. |
| MSC Journeyman Rigger Reference Card | **0** | LIVE | M04, M05 | Five dated revisions in Drive `Rigger Cards/`, latest `5-12-20aa.pdf`. **Pin one revision as canonical** before harvest - the ACS cites the card, not a revision. |
| Stage 2 M04 (Load Weight & CG) | **0** | LIVE | M01 | Parity cross-check already done: same reaction/weighing formula, same far-end reading convention, same stability rule. |
| Rigger 2 Incline Plane Sample | **0** | LIVE | *(uncited)* | Drive, 5 Mar 2025. **Not cited by M08 but directly on topic.** See gap analysis. |
| TR244C | **?** | ? | **all 9** | **Highest-priority unknown.** Cited by every module in the stage and carries no tier. Determine whether this is a CCOS internal code (Tier 0), a government TM (Tier 1), or third-party (Tier 2b) before any harvest course cites it. |
| Basic Rigging Workbook | **?** | ? | M01, M03 | **Likely Tier 1.** If this is the Brookhaven National Laboratory / DOE *Basic Rigging* workbook, it is public domain and quotable. Confirm the exact document - the title is generic and several unrelated commercial workbooks share it. |
| Sling tension image set | **?** | ? | M02, M03 | **Provenance must be documented.** The stage's own regulatory rail asserts "no third-party imagery is used." An image set cited as a source without provenance cannot support that claim. Same for the hitch-type image set. |
| B30.5 mobile extract | **2a** | LIVE | M06 | Paraphrase with attribution. Never reproduce tables or figures. |
| ASME B30.9 / B30.20 / B30.26 | **2a** | GAP | M02-M05, M07, M09 | Full volumes not held. See open work. |
| ASME BTH-1 | **2a** | GAP | M09 | Full text not held. Numeric design criteria currently second-hand. See open work. |
| NCCCO Rigger Reference Manual / Booklet | **2b** | LIVE | **M01-M07, M09 (8 of 9)** | `nccco-rigger-reference-manual_060419a.pdf`, Drive. Reference, never quote, always reword. See the naming conflict below. |
| Tucker Advanced Rigging | **2b** | LIVE | M04-M09 | `Tucker Advanced Rigging 1-30 (1).pptm`, Drive. Reference, never quote, always reword. |
| SC&RA Bull Rigging Competency Guidebook | **2b** | GAP | M08 | No copy located in Drive this pass. Locate or drop the citation. |
| Drifting With Chain Hoist | **?** | GAP | M08 | No copy located. Provenance and tier unknown. |

---

## The naming conflict

The Stage 4 regulatory rail states, as non-negotiable across the stage:

> No third-party training vendor is named, cited, or sourced in any output, and no
> third-party imagery is used.

The ACS Build Map then names NCCCO in eight of nine modules, Tucker in six, and SC&RA
in one, in its own `Sources` lines.

**This is most likely a scope boundary that was never written down**, not a breach:
the rail is about *learner-facing* output, and the ACS is an internal build-control
document. But the rail says "any output," and the ACS is an output. Two fixes, either
is fine, but one must be chosen and stated:

1. **Amend the rail** to read "no third-party training vendor is named in any
   learner-facing text; internal build-control documents record full provenance."
   This is the honest version and matches how the CM register already operates.
2. **Strip vendor names from the ACS** and carry them only in the source register.
   Cleaner externally, worse for traceability.

Recommendation: **option 1.** Provenance you cannot see is provenance you cannot
audit, and the CM track's whole tier discipline depends on naming what was actually
read. Note that Rev 1.3 amendment A1 already sanctions attributed paraphrase for
ASME/OEM, which is the same principle.

Also worth noting: NCCCO is a **certification body**, and CCOS is an ATP. Naming it as
a reference read is a different act from naming a competing training vendor. The rail
does not currently draw that distinction and probably should.

---

## Tier 1 material that Stage 4 does not yet use

This is the substantive finding. The CM track's Tier 1 shelf already holds
public-domain material that covers Stage 4 content currently grounded on Tier 2b.

### S4_M04 - Slings and Field-Assembled Terminations

M04's knowledge spine can be re-grounded almost entirely on Tier 1:

| ACS code | Current grounding | Tier 1 source available now |
|---|---|---|
| `S4.M04.K2` clip count, spacing, turnback, torque by rope diameter | NCCCO / Tucker (2b) | **TM 3-34.86 Table 2-3** - clip count, spacing and torque by rope diameter. Supersedes TM 5-725. Public domain, **quotable verbatim.** |
| `S4.M04.K3` saddle on the live line, U-bolt on the dead end | NCCCO / Tucker (2b) | **29 CFR 1926.1414** - clips attach to the unloaded dead end only. Regulation, quotable. |
| `S4.M04.K5` wedge socket - live line in line with the load, tail is the dead end | NCCCO / Tucker (2b) | **MSHA IG 43 Module 14** - live end on the eye side, at least one rope lay of dead end past the wedge. Also carries drum anchorage and the 5%/15% criteria. |
| `S4.M04.K6` poured and swaged sockets as engineered terminations | NCCCO / Tucker (2b) | **NSTM Ch 613 Rev 3** - poured sockets, seizing. Plus **Navy Wire-Rope Handbook Vol III**. |
| `S4.M04.K8` removal-from-service criteria by sling type | NCCCO / Tucker (2b) | **DOE Hanford Hoisting & Rigging Manual** Ch 8 Ropes. See below. |

This matters because M04 is a donor to the Rigging Equipment Inspection course, where
these numbers stop being teaching points and become the deliverable.

### S4_M03 through S4_M05 - the "B30.9 / B30.10 / B30.26 full volumes" open item

The ACS lists acquiring these volumes as open work, on the grounds that it "would
tighten removal-criteria precision before those modules are harvested into the
inspection course, where the numbers become the product."

**The CM track answered the equivalent question without buying B30.10.**

**DOE Hanford Hoisting & Rigging Manual (DOE/RL-92-36)** - 20 chapters, roughly 100k
words, currently maintained (revisions dated Feb 2024), Tier 1, quotable:

- Chapter 4 - personnel qualifications
- **Chapter 5 - Hooks**
- **Chapter 8 - Ropes**
- **Chapter 10 - Rigging Hardware**
- Chapter 13 - overhead and gantry
- **Chapter 17 - Interpretations** (the edge cases already answered)

Chapter 5 is the model for how this works. Under a heading called *Inconsistent
Standards* it states **both** figures and then rules on each: OSHA sets 15% throat
opening and 10 degrees twist; ASME B30.10 sets 5% not to exceed 1/4 inch plus any
visible bend or twist; **follow the ASME requirement.** It rules the other way on
records - OSHA requires monthly documented hook inspections and B30.10 does not, so
**follow OSHA there.**

That is a Tier 1 document doing the conflict resolution for you, in public-domain
text, on exactly the removal-criteria precision the ACS flagged as open.

**Caveat, and it is a real one.** Watch the dagger exception. Chapters 8 and 10 sit
close to B30.9 and B30.26 territory, and a Tier 1 document that reproduces consensus
standard text verbatim does not launder it. Hanford is **not** currently dagger-flagged
in the CM register (NAVFAC P-307 and DOE-STD-1090 are), but M03-M05 lean hard on B30.9
and B30.26, so **verify per passage, not per document.**

Net: this does not fully close the open item, but it downgrades it from "blocking the
inspection course" to "verify coverage, then buy only what Hanford genuinely leaves
open." That is a materially cheaper position than the ACS currently records.

### S4_M09 - ASME BTH-1

**Nothing in Tier 1 closes this.** This one stays open, and it is the sharpest
exposure in the stage.

The ACS is already honest about it in its own Source gap note. Two things make it
worse than the note implies:

1. The cited route is **NCCCO Rigger Reference Booklet (B30.20 Section 20-1,
   paraphrased)** - which is a paraphrase of ASME text taken out of a **Tier 2b
   commercial document**. That is a double hop. Rev 1.3 amendment A1 sanctions
   paraphrasing ASME with attribution; it does not sanction paraphrasing someone
   else's paraphrase of ASME.
2. The values at risk are **hard numbers**, not concepts: Design Category A design
   factor of 2 against yield, Category B factor of 3, and Service Class 0 through 4
   cycle counts (roughly 20,000 at Class 0 to over 2,000,000 at Class 4). These are
   the ACS codes `S4.M09.K3`, `K5` and `K6`. A learner is gate-tested on them at 100%
   mastery.

**Recommendation: acquire ASME BTH-1.** It is the one place in Stage 4 where a
gate-tested numeric criterion rests on a secondary commercial source, and it is the
capstone module. The concepts are safe; the numbers need a primary.

---

## Tier 0 assets located but not cited by Stage 4

The register's own build rule is "check here first, before any external source."
Stage 4 cites Tier 0 three times. These were found in Drive this pass and are
candidates for the harvest courses at minimum:

| Asset | Location | Relevant to |
|---|---|---|
| `Rigger 2 Incline Plane Sample.docx` | Drive, `Rigger Cards/` | **M08** friction and inclined plane - directly on topic, uncited |
| `WD-RIG-001_Rigging_Environment.pptx` | Drive | Stage context |
| `WD-RIG-002_Rigging_Gear_Fundamentals.pptx` | Drive | M03, M04, M05 |
| `Company_EQ-TRAIN-004_Stage2_M1_RiggingFundamentals` (PPTX + facilitator guide) | Drive | Sling types, tag reading, design factor. Feeds **RI** course |
| `Company_EQ-TRAIN-004_Stage2_M2_RiggingInspection.pptx` | Drive | **Largest single donor candidate for the RI course** |
| `Qualified Rigger & Signalperson Certification - EM 385-1-1 Rigging Requirements.pptx` | Drive | EM 385-1-1 Ch 15. Feeds **PH** course |
| `4 HR Rigger Test.docx`, `new rigger test` (3 variants), `2023 Rigger Review Questions Key.pdf` | Drive, `Rigger Cards/` | Item-bank raw material for **R2** exam prep |

**Do not harvest `Advanced_Rigging_40_Question_Test.docx` as-is.** It is Tier 0 and it
is ours, but it fails every check the Stage 4 verification suite now enforces: of 40
items, question 8 repeats verbatim at 14, 16, 21 and 22; question 10 repeats at 11 and
18; the answer key resolves to "Rigger" eight times and "Date of purchase" six. It is
a useful record of where the item-writing standard used to be, and a good argument for
the current one. It is not a bank.

---

## What to do next

1. **Assign a tier to TR244C.** It is cited by all nine modules and is the single
   largest unknown in the stage.
2. **Confirm the Basic Rigging Workbook identity.** If it is the DOE/BNL document it
   is Tier 1 and quotable, which changes M01 and M03 grounding for free.
3. **Document image-set provenance** for M02 and M03, or amend the "no third-party
   imagery" rail claim.
4. **Resolve the vendor-naming conflict** - amend the rail (recommended) or strip the
   ACS.
5. **Pull the Tier 1 shelf into M04** before the RI harvest: TM 3-34.86 Table 2-3,
   29 CFR 1926.1414, MSHA IG 43 Module 14, NSTM Ch 613.
6. **Read Hanford Ch 5, 8, 10 and 17** against the M03-M05 removal criteria and record
   what it does and does not cover. Buy only the remainder.
7. **Acquire ASME BTH-1.** The capstone's gate-tested numbers need a primary source.
8. **Archive locally with SHA256.** The CM register holds 48 sources archived locally
   and its standing instruction is "build from the archive, never from a URL." Two of
   its three Rev 1.1 failures were link rot on live, reputable hosts. Stage 4 has no
   archive of record.
