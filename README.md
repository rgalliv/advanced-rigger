# advanced-rigger

Build-control documentation for the nine **Advanced Rigger** modules.

They are **new modules added to the existing Stage 4 sequence** as `S4_M15` through
`S4_M23`, following the same format as every other stage. Nothing existing is
overwritten.

## Contents

| Document | What it covers |
|---|---|
| [`docs/module_format_spec.md`](docs/module_format_spec.md) | Numbering, scoring model, protected registry, public/protected boundary, runtime event contract, wrong-answer behaviour, asset externalization, verification, build sequence |
| [`docs/question_architecture.md`](docs/question_architecture.md) | Gate sizing, item-writing rules, ACS coverage mapping, gate composition targets, topic ownership |
| [`docs/S4_source_register.md`](docs/S4_source_register.md) | Every source cited by the ACS, assigned a tier under the model adopted by the Crane Technician track. Tier 1 substitutions, and the one acquisition genuinely required |
| [`docs/S4_gap_analysis.md`](docs/S4_gap_analysis.md) | Structural gaps between what the ACS asserts and what the verification suite proves |

## Module numbering

Stage 4 currently ends at `S4_M14`. These continue the sequence.

| ACS module | New ID | Gate code |
|---|---|---|
| Center of Gravity Determination | `S4_M15` | AR-101C |
| Unequal Leg Loading and Off-Level Pick Points | `S4_M16` | AR-102C |
| Sling Tension Beyond the Chart | `S4_M17` | AR-103C |
| Slings and Field-Assembled Terminations | `S4_M18` | AR-104C |
| Rigging Hardware and Specialty Attachments | `S4_M19` | AR-105C |
| Blocks, Sheaves and Multi-Part Line Loading | `S4_M20` | AR-106C |
| Multi-Point Lifts and Load Sharing | `S4_M21` | AR-107C |
| Friction and Inclined-Plane Rigging | `S4_M22` | AR-108C |
| Below-the-Hook Lifting Device Design (BTH-1) | `S4_M23` | AR-109C |

`data-cq-stage="4"` unchanged. Salts become `CQ1:S4_M15_...`. Keys append to the existing
`platform/cq_keys_S4.json` (112 records to 184). ACS codes renumber with the modules:
`S4.M01.K1` becomes `S4.M15.K1`. `S4_M14` now points at `S4_M15`; `S4_M23` terminates the
stage.

> **Note on the two older documents.** `S4_source_register.md` and `S4_gap_analysis.md`
> were written before the renumber and refer to modules as M01-M09 and codes as
> `S4.M01.*`. Their content is unaffected - map M01 to M15, M02 to M16, and so on.

## Settled decisions - 7 August 2026

| Decision | Effect |
|---|---|
| **New modules, existing stage** | `S4_M15`-`S4_M23`. Nothing overwritten. Only edit to an existing file is `S4_M14`'s next-module pointer |
| **Gate size 8** | Gate q19-q24 to **q18-q25**, `review_offset` 18 to **17**, letters balance **2/2/2/2**, ungated bank 19 to 17, new registry records **72** |
| **Adopt Gen 3 scoring** | Keys server-side in `cq_keys_S4.json`, assets externalized - matching `S4_M01`-`S4_M14` |
| **Ungated 17 items** | Formative plus R2 harvest reserve. Written to gate quality, scored neutrally |
| **Skill floor** | At least two `S#` codes in every gate |
| **Topic owners** | Angle factors M16, snatch-block resultant M20, combined weight M21. D/d split M17/M20 with cross-reference |

## The open architecture finding

The Advanced Rigger modules were authored on the Gen 1 client-scored model - 225 FNV
hashes baked into HTML. Stage 4 is on Gen 3, keys server-side. Stage 6 states the rule:
retained FNV hashes are for standalone preview only and "must not be accepted as the
production scoring path." FNV-1a is non-cryptographic; for a four-option item that is
four guesses.

Joining Stage 4 means adopting Stage 4's scoring. That is a retrofit pass, not a rebuild
- the same one Stage 3 went through.

## Related

- Second Brain: CraneQualified HQ, Crane Technician Open Source Register
- Mobile crane build process: SharePoint, `Crane Qualified Build Files/Developer Handoff - July`
- Companion repo: `rgalliv/mobilecranetech`
