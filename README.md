# advanced-rigger

Build-control documentation for the CraneQualified **Advanced Rigger (Stage 4)**
e-learning stage: `S4_M01` through `S4_M09`.

Stage 4 is built and verified as a learning product (9 modules, 225 questions, 12
verification checks passing on all nine). This repository holds the documentation
layer that the stage shipped without, and that the seven planned downstream courses
will need.

## Contents

| Document | What it covers |
|---|---|
| [`docs/AR_module_format_spec.md`](docs/AR_module_format_spec.md) | Build format aligned to the mobile crane process (`Developer Handoff - July`). Scoring model, public/protected boundary, runtime event contract, wrong-answer behaviour, asset externalization, verification, and the retrofit sequence. |
| [`docs/AR_question_architecture.md`](docs/AR_question_architecture.md) | Gate sizing against house convention, item-writing rules, the ACS coverage-mapping layer, gate composition targets, and the protected registry. |
| [`docs/S4_source_register.md`](docs/S4_source_register.md) | Every source cited by the ACS, assigned a tier under the model adopted by the Crane Technician track (Gate Master Rev 1.3 Section 11). Identifies Tier 1 public-domain material that can replace Tier 2b grounding, and the one acquisition that is genuinely required. |
| [`docs/S4_gap_analysis.md`](docs/S4_gap_analysis.md) | Structural gaps between what the ACS asserts and what the verification suite proves. ACS-code traceability, module boundaries, negative source declarations, and the harvest-course sourcing costs. |

## Settled decisions - 7 August 2026

| Decision | Effect |
|---|---|
| **Gate size is 8** | Gate moves q19-q24 to **q18-q25**, `review_offset` 18 to **17**, gate letters balance **2/2/2/2**, ungated bank drops 19 to 17, stage gate records 54 to **72** |
| **Rename, never overwrite** | Advanced Rigger rebuilds as **`AR_M01`-`AR_M09`**, new files. Originals archived to a non-deployed path, byte-identical. Mobile crane `S4_M01`-`S4_M14` untouched and never in scope |

## The open architecture finding

**The stage is on the superseded scoring architecture.** Advanced Rigger bakes 225 FNV
hashes into module HTML. The mobile crane track moved keys server-side at Stage 3 and
now states plainly that retained FNV hashes are for standalone preview only and "must
not be accepted as the production scoring path." Advanced Rigger needs the same retrofit
Stage 3 went through - not a rebuild.

The rename decision makes this cheaper, not harder: because `AR_*` modules are generated
as new files rather than edited in place, the key extraction and the salt change happen
in the same pass that emits them.

## Still missing from this repository

- The nine module HTML files
- `S4_MXX_manifest.json` (nine)
- `S4_STAGE_crosscheck_report.md` - the stage crosscheck of record
- The Stage 4 ACS Build Map HTML itself

The CM track's standing rule applies: **build from the archive, never from a URL.**

## Related

- Second Brain: CraneQualified HQ -> Crane Technician - Open Source Register
- Companion repo: `rgalliv/mobilecranetech` (Crane Mechanic track canonical documents)
