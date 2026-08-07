# Advanced Rigger - Module Format Spec

Rev 0.2 - 7 August 2026

The nine Advanced Rigger modules are **new modules added to the existing Stage 4
sequence.** They follow the same format as every other stage. Nothing existing is
overwritten.

Benchmarked against the CraneQualified mobile crane build process in
`Developer Handoff - July` (SharePoint, `Crane Qualified Build Files`). Architecture,
gating model, and conventions only - no instructional content taken.

---

## 1. Numbering

Stage 4 currently ends at `S4_M14`. The Advanced Rigger modules continue the sequence.

| ACS module | New module ID | Gate code |
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

Everything else stays on the house pattern:

| Item | Value |
|---|---|
| Stage attribute | `data-cq-stage="4"` - unchanged, same as every other stage |
| Salt | `CQ1:S4_M15_...` through `CQ1:S4_M23_...` |
| Key file | `platform/cq_keys_S4.json` - **appended to the existing file**, not a new one |
| Manifests | `S4_M15_manifest.json` .. `S4_M23_manifest.json` |
| Gate codes | `AR-101C` .. `AR-109C` - already unique, unchanged |
| Chain | `S4_M14` chains to `S4_M15`; `S4_M23` becomes the Stage 4 terminus |

**ACS codes renumber with the modules.** `S4.M01.K1` becomes `S4.M15.K1`, and so on
through `S4.M09.*` to `S4.M23.*`. The codes themselves - what they say and how many
there are - do not change. Only the module number moves.

**Nothing is overwritten.** `S4_M01` through `S4_M14` are untouched. The only edit to an
existing file is `S4_M14`'s next-module pointer, which moves from the stage terminus to
`S4_M15`. The Advanced Rigger modules are added, not substituted.

---

## 2. Scoring - adopt the current Stage 4 model

The mobile crane track has moved through three generations, and Stage 4 is on the
newest. The Advanced Rigger modules were authored on the oldest.

| | Gen 1 | Gen 2 | Gen 3 - current Stage 4 |
|---|---|---|---|
| Seen in | Stage 2 | Stage 3, Stage 6 | **Stage 4**, Jul 24 |
| Answer keys | FNV hashes baked into HTML | Server-only `cq_keys_SN.json` | Server-only, plus keyseed and protected registry |
| Client key blocks | Present | Removed | Removed |
| Media | Embedded data URIs | Embedded | **Externalized, content-addressed** |
| Scoring authority | The module | The host | The host |

The Advanced Rigger build is Gen 1 - 225 FNV hashes baked in, verified by "every baked
hash recomputed from salt : qid : correct index." **Joining Stage 4 means adopting
Gen 3.**

Stage 6 states the rule plainly:

> The modules retain recoverable FNV hashes for **standalone-preview compatibility.**
> Those hashes **must not be accepted as the production scoring path.**

FNV-1a is non-cryptographic. For a four-option question that is four guesses. It is
obfuscation, not security.

### 2.1 Protected registry

The existing `platform/cq_keys_S4.json` holds **112 records - gate items only**
(M01 gate 24, M02-M05 and M08-M14 gate 8 each, M06 and M07 ungated). It does not hold
the full bank.

Follow that. Nine new modules at 8 gate items each add **72 records**:

| | Records |
|---|---|
| Existing `cq_keys_S4.json` | 112 |
| Added by `S4_M15`-`S4_M23` | **72** |
| **Total** | **184** |

The ungated 17 items per module are formative and **record the learner selection
neutrally** - no machine-readable correctness, so no registry record.

Rules, unchanged from the existing package:
- Server-side only. Never statically served. Block the route.
- The module sends `question_id` and the selected option index. Nothing else.
- The platform returns **only the attempt verdict and permitted feedback**. Never
  `correctIndex`.
- Records are unique, well formed, and module-hash matched.
- Client gate state is UI state, not production authority.

### 2.2 Public / protected boundary

Public module HTML and assets contain **none** of: a correct-answer index, a `data-good`
mapping, a `data-correct` attribute, option-specific `data-feedback`, any keyseed
reference or public key fallback, or plaintext answer copy.

---

## 3. Runtime contract

Same as every other Stage 4 module:

| Event / call | Direction |
|---|---|
| `cq:module_started` | module to host |
| `cq:slide_changed` | module to host |
| `cq:kc_attempt` | module to host |
| `cq:complete_request` | module to host |
| `cq:complete_ack` | host to module |
| `CQ.scoreAnswer(...)` | module calls host |
| `CQ.requestComplete()` | module calls host |

The Advanced Rigger build uses the older `requestComplete` / `cq-module-complete`
tokens. Map them onto the above. Retain `data-cq-module` and `data-cq-total`.

---

## 4. Wrong-answer behaviour

Specified by Stage 6, adopt verbatim:

- A wrong response is **not retained as a completed attempt.**
- **All options are re-enabled** after a wrong server verdict.
- The next-question control **remains hidden** after a wrong response.
- A verified correct response **remains locked** and exposes the next control.
- The completion slide **stays locked** until every gate answer is correct.

---

## 5. Assets

Externalize, matching the existing Stage 4 package. That pass took 885 media references
out of data URIs into 750 content-addressed files and moved 123.31 MB of HTML to
1.59 MB.

```
modules/             public module HTML - S4_M01 .. S4_M23
assets/images/       content-addressed public images
assets/audio/        content-addressed public MP3 narration
platform/            SERVER-SIDE ONLY protected scoring records
docs/                audit and handoff evidence
tools/               deterministic build and validation tools
MODULE_MANIFEST.csv  module inventory, sizes, hashes, counts
ASSET_MANIFEST.csv   every public asset, size, hash, reference count
```

Lowercase web-safe filenames, relative `../assets/...` references, validated on a
**case-sensitive** HTTP server, media bytes preserved exactly, no unused assets. The
nine new modules append rows to the existing two manifests.

**Do this before the ElevenLabs pass**, not after - otherwise nine modules absorb an MP3
payload and get torn apart again.

---

## 6. The narration dependency

The Stage 2 gating handoff makes explicit what the Advanced Rigger open-work table
treats as cosmetic. Two answer-handlers compose:

| Layer | Enforces |
|---|---|
| `cq-slide-audio-flow` overlay | every question is **answered** before advancing |
| KC Gate Engine | the gate is **100% correct** before completion |

And the governing invariant:

> **The two GATE sets AGREE** (overlay GATE == engine GATE). If they drift, narration
> and completion gating disagree. **This is the check that bites.**

Standing instruction: *never delete the overlay; only reconcile its GATE.*

All nine modules currently run the speechSynthesis fallback. When ElevenLabs audio
lands, the overlay ships with it and its GATE set must be reconciled against the engine
GATE - now the 8-item set - then re-verified. **The reported 13/13 jsdom pass per module
is provisional until after the audio pass.** It is the last build step, not a deferred
extra.

---

## 7. Verification

The Advanced Rigger suite is strong on **content** and thin on **architecture**. The
Stage 2 invariants cover the other half. Add these:

| Check | Source | Why |
|---|---|---|
| **No plaintext answer keys** - zero hits on `Correct answer:` and `data-correct` | Stage 2 inv. 3 | Security. Not currently checked at all. |
| **Two GATE sets identical** (overlay == engine) | Stage 2 inv. 6 | "The check that bites." Live at the audio pass. |
| **Scoring shim wired through `window.CQ`** | Stage 2 inv. 2 | Verify by capability, not exact syntax. |
| **No sub-100% passing copy** | Stage 2 inv. 7 | A "15% throat-opening" content fact is legitimate - flag only percentages tied to passing. |
| **`data-cq-total` on `<body>`** | Stage 2 inv. 10 | Platform needs the slide count. |
| **Registry parity** - 184 records, unique, well formed, module-hash matched | Stage 4 acceptance | After key extraction. |
| **No public data URIs, absolute paths, keyseed refs, key fallback** | Stage 4 acceptance | After externalization. |
| **Browser verification, desktop and mobile** - every slide visited, images loaded, audio load/play/pause, no 404, no console error, no horizontal overflow | Stage 4 acceptance | jsdom catches none of these. |

Retain all twelve existing Advanced Rigger checks. Nothing there is redundant.

**Harness gotcha, carried forward:** the real `navigate()` has a ~390 ms `isAnimating`
debounce. Position with instant `jumpTo`; assert a boundary with a single synchronous
`navigate`. Don't loop `navigate` or you measure the debounce, not the lock.

---

## 8. Build sequence

1. **Renumber** to `S4_M15`-`S4_M23`. Salts `CQ1:S4_M15_...`, ACS codes `S4.M15.*` ..
   `S4.M23.*`, manifests renamed. Point `S4_M14` at `S4_M15`.
2. **Move the gate to q18-q25**, `review_offset` 17, letters balanced 2/2/2/2. Two items
   per module enter the gate for the first time and must clear de-leak and run-length.
3. **Extract keys** into the existing `platform/cq_keys_S4.json` (112 to 184). Remove
   client key blocks and key markers.
4. **Map the event contract** onto `cq:*` + `CQ.scoreAnswer` / `CQ.requestComplete`.
5. **Implement wrong-answer behaviour** per section 4.
6. **Externalize assets.** Append to `MODULE_MANIFEST.csv` and `ASSET_MANIFEST.csv`.
7. **Build the ACS coverage map** - see `question_architecture.md`.
8. **ElevenLabs pass.** The overlay ships here.
9. **Reconcile overlay GATE to engine GATE.** Re-run the full suite. The 13/13 becomes
   final here.
10. **Browser verification**, desktop and mobile.
11. **Independent review** before production.

Steps 1-6 are mechanical. Step 7 is judgement. Steps 8-9 are the real remaining build.

**Order matters in one place:** gate membership must settle (2) before the coverage map
(7), and both before the audio pass (8). The overlay ships with a GATE set; if that set
is still moving, the audio pass gets done twice.

---

## 9. What Advanced Rigger brings that Stage 4 does not have

Preserve these through the retrofit - no mobile crane package documents an equivalent:

- **Answer distribution control** (7/6/6/6 across A/B/C/D) and **max consecutive
  same-answer run of 1** across the full bank.
- **De-leak**: correct option within 6 characters of the longest distractor. Kills the
  most common giveaway in multiple-choice item writing.
- **Regulatory hygiene as an automated scan** - correct stop-authority citation, specific
  ASME volume named, no unqualified series reference.
- **ASCII cleanliness** - no em-dash, en-dash, smart quote, ellipsis, non-breaking space.
- **A published ACS** with stable codes. The mobile crane stages ship module inventories;
  they do not ship an assessment and content standard.

These are candidates for promotion to house-wide checks, not just Advanced Rigger ones.
