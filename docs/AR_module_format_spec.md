# Advanced Rigger - Module Format Spec

Rev 0.1 - 7 August 2026

Aligns the Advanced Rigger stage to the CraneQualified mobile crane build process as
delivered in `Developer Handoff - July` (SharePoint, `Crane Qualified Build Files`).

**What was taken from the mobile crane package:** gating architecture, scoring model,
runtime event contract, asset policy, packaging layout, and verification method.
**Nothing else.** No instructional content, no question wording, no crane-operator
subject matter.

---

## 1. The headline finding

**The Advanced Rigger stage is built on the superseded architecture.**

The mobile crane track has moved through three generations. The Advanced Rigger ACS
describes generation one.

| | Gen 1 - client-scored | Gen 2 - server-scored | Gen 3 - server-scored + externalized |
|---|---|---|---|
| Seen in | Stage 2 | Stage 3, Stage 6 | Stage 4 (mobile crane), Jul 24 |
| Answer keys | FNV-1a hashes baked into module HTML | Extracted to `platform/cq_keys_SN.json`, server-only | Same, plus keyseed and protected registry |
| Client key blocks | Present | **Removed** | **Removed** |
| Media | Embedded data URIs | Embedded | **Externalized, content-addressed** under `assets/` |
| Scoring authority | The module | The host platform | The host platform |
| Answer engines | Two (gate engine + overlay) that must agree | Bridge to host | Bridge to host |

The Advanced Rigger stage as documented in its ACS is squarely Gen 1: 225 FNV hashes
baked in, verified by "every baked hash recomputed from salt : qid : correct index."

The mobile crane Stage 6 handoff states the current rule directly:

> The modules retain recoverable FNV hashes for **standalone-preview compatibility.**
> Those hashes **must not be accepted as the production scoring path.**

**FNV-1a is a non-cryptographic hash.** For a four-option question, an attacker tries
four values. The hash is obfuscation, not security. The mobile crane track recognised
this and moved keys server-side; Advanced Rigger has not yet.

This does not invalidate the Advanced Rigger content. It means the stage needs a
**retrofit pass**, not a rebuild - the same retrofit Stage 3 went through ("Retrofitted
each module from its centralized `CQ_KEY` source into the real-gate iframe contract...
Removed the client-side `CQ_KEY` blocks and key markers from learner modules").

---

## 2. Module ID collision - resolved by rename, not overwrite

The mobile crane track already occupies `S4_M01` through `S4_M14` with
`data-cq-stage="4"`. Advanced Rigger uses `S4_M01` through `S4_M09` and salts of the
form `CQ1:S4_M01_...`.

**These collide.** Same module IDs, same stage attribute, different courses.

**DECIDED 7 Aug 2026.** The Advanced Rigger modules are **renamed and rebuilt as new
artifacts. Nothing is overwritten.**

| Item | Original | New build |
|---|---|---|
| Module ID | `S4_M01` .. `S4_M09` | `AR_M01` .. `AR_M09` |
| Stage attribute | `data-cq-stage="4"` | `data-cq-stage="AR"` |
| Salt | `CQ1:S4_M01_...` | `CQ1:AR_M01_...` |
| Key file | (none - baked in) | `platform/cq_keys_AR.json` |
| Gate codes | `AR-101C` .. `AR-109C` | unchanged - already unique |
| Gate items | q19-q24 | **q18-q25** (`review_offset` 17) |
| Chain terminus | `STAGE_COMPLETE` | `AR_COMPLETE` (Stage 6 uses `S6_COMPLETE`) |

### The no-overwrite rule

No existing module file is modified, replaced, or deleted. This covers **two distinct
sets** of files, and the distinction matters:

1. **The mobile crane `S4_M01`-`S4_M14` modules.** A different course. Untouched, and
   never in scope.
2. **The original Advanced Rigger `S4_M01`-`S4_M09` modules.** Preserved as the source
   of record. The new `AR_*` build is derived from them; they are not edited in place.

Consequences to plan for:

- **The retrofit is a generate-alongside, not an edit.** Read the original, emit
  `AR_MXX_*.html` as a new file. The original stays byte-identical.
- **The collision persists in storage even after the rename**, because both `S4_M01`
  sets still exist on disk. Resolve it by **path, not by filename**: the originals move
  to an archive path that is never deployed; only `modules/AR_*.html` is served.
- **Every hash is recomputed** - the salt changes, and the gate moves from 6 items to 8.
  This is free, because the retrofit takes keys off the client anyway (section 3.1).
- **Two banks now exist per module.** The original with a 6-item gate, the new with 8.
  `MODULE_MANIFEST.csv` must record which is authoritative, or a future pass will
  harvest the wrong one.

Recommended layout:

```
modules/                     AR_M01..AR_M09 - the only deployed module path
platform/cq_keys_AR.json     SERVER-SIDE ONLY
archive/s4_original/         original Advanced Rigger S4_M01..S4_M09, never deployed
```

Nothing in `archive/` is served, referenced by a manifest as authoritative, or fed to
the verifiers.

---

## 3. Target architecture

### 3.1 Scoring

Adopt the Gen 3 model.

- Answers live in `platform/cq_keys_AR.json`. **Server-side only. Never statically
  served.** Stage 3 blocks `/s3/platform/cq_keys_S3.json` at the route layer; do the
  same for AR.
- The module sends `question_id` and the **selected option index**. Nothing else.
- The platform compares against the server-only seed and returns **only the attempt
  verdict and permitted feedback**. It does **not** return `correctIndex`.
- FNV hashes may remain in the module for standalone preview. They are **not** the
  production scoring path and must be documented as such.
- Client gate state (`window.__cqGateComplete` or equivalent) is **UI state, not
  production authority.** The host independently verifies completion.

### 3.2 Public / protected boundary

Public module HTML and assets must contain **none** of:

- a correct-answer index
- a `data-good` mapping
- a `data-correct` attribute
- option-specific `data-feedback` mapping
- any keyseed reference or public key fallback
- plaintext answer copy of any kind

Public formative activities that previously carried machine-readable correctness
**record the learner selection neutrally.**

### 3.3 Runtime contract

Emit and honour the current event set:

| Event / call | Direction |
|---|---|
| `cq:module_started` | module to host |
| `cq:slide_changed` | module to host |
| `cq:kc_attempt` | module to host |
| `cq:complete_request` | module to host |
| `cq:complete_ack` | host to module |
| `CQ.scoreAnswer(...)` | module calls host |
| `CQ.requestComplete()` | module calls host |

**Advanced Rigger currently uses the older tokens** - its verification suite checks for
`requestComplete` and `cq-module-complete`. Map these onto the current contract during
retrofit. Retain `data-cq-module` and `data-cq-total`.

### 3.4 Wrong-answer behaviour

The mobile crane Stage 6 handoff specifies this precisely. Adopt verbatim as behaviour:

- A wrong response is **not retained as a completed attempt.**
- **All options are re-enabled** after a wrong server verdict.
- The next-question control **remains hidden** after a wrong response.
- A verified correct response **remains locked** and exposes the next control.
- The completion slide **stays locked** until every gate answer is correct.

Note what this is not: it is not "score at the end." Each gate item is adjudicated
individually, and a miss returns the learner to the same item with a clean slate.

### 3.5 Assets

Adopt externalization. The mobile crane pass took 885 media references out of data
URIs into 750 content-addressed files, moving 123.31 MB of HTML down to 1.59 MB.

```
modules/             public module HTML
assets/images/       content-addressed public images
assets/audio/        content-addressed public MP3 narration
platform/            SERVER-SIDE ONLY protected scoring records
docs/                audit and handoff evidence
tools/               deterministic build and validation tools
MODULE_MANIFEST.csv  module inventory, sizes, hashes, counts
ASSET_MANIFEST.csv   every public asset, size, hash, reference count
```

Rules: lowercase web-safe filenames, relative `../assets/...` references, validated on
a **case-sensitive** HTTP server, media bytes preserved exactly, no unused assets.

This matters for Advanced Rigger specifically because the ElevenLabs pass is still
outstanding. **Do the externalization before the audio pass, not after** - otherwise
nine modules absorb an MP3 payload and then have to be torn apart again.

### 3.6 The overlay / narration dependency

The Stage 2 gating handoff makes explicit what the Advanced Rigger open-work table
treats as cosmetic. Two answer-handlers compose:

| Layer | Enforces |
|---|---|
| `cq-slide-audio-flow` overlay | every question is **answered** before advancing |
| KC Gate Engine | the gate is **100% correct** before completion |

And the governing invariant:

> **The two GATE sets AGREE** (overlay GATE == engine GATE). If they drift, narration
> and completion gating disagree. **This is the check that bites.**

with the standing instruction: *never delete the overlay; only reconcile its GATE.*

**Consequence for Advanced Rigger.** All nine modules currently run the speechSynthesis
fallback. When ElevenLabs audio lands, the overlay ships with it and its GATE set must
be reconciled against the engine GATE, then re-verified. The stage's reported "13/13
jsdom pass" per module is therefore **provisional** until after the audio pass.

The ACS calls the re-record "deferred, not blocked - the only production task
outstanding." More accurate: **it is the last build step, and it invalidates the current
behavioural verification.** Sequence it accordingly.

---

## 4. Verification

Advanced Rigger's twelve checks are strong on **content** and thin on **architecture**.
The mobile crane track's ten Stage 2 invariants cover the other half. Neither set
subsumes the other.

### Already covered by the AR suite

Slide-to-question mapping, answer distribution, gate composition, full-bank run,
de-leak, FNV integrity, `node --check`, jsdom behavioural, engine tokens, ASCII
cleanliness, regulatory hygiene, cross-module integrity.

### Missing - add these

| Check | Source | Why |
|---|---|---|
| **No plaintext answer keys** - zero hits on `Correct answer:` and `data-correct` | Stage 2 invariant 3 | Security. Not currently checked at all. |
| **Two GATE sets identical** (overlay == engine) | Stage 2 invariant 6 | "The check that bites." Becomes live at the audio pass. |
| **Scoring shim wired through `window.CQ`** | Stage 2 invariant 2 | Verify by capability, not exact syntax - both `window.CQ = {...}` and guarded free functions are valid. |
| **No sub-100% passing copy** | Stage 2 invariant 7 | Careful: a "15% throat-opening" content fact is legitimate. Flag only percentages tied to passing or advancing. |
| **`data-cq-total` on `<body>`** | Stage 2 invariant 10 | Platform needs the slide count. |
| **Protected-registry parity** - every gate item has exactly one server record, module-hash matched | Stage 4/6 acceptance | Applies once keys move server-side. |
| **No public data URIs, absolute paths, local paths, keyseed refs, key fallback** | Stage 4 acceptance | Applies after externalization. |
| **Browser verification, desktop and mobile** - every slide visited, images loaded, audio load/play/pause, no 404, no console error, no horizontal overflow | Stage 4 acceptance (14/14 desktop, 14/14 mobile, 28 runs) | AR has jsdom only. jsdom does not catch overflow or 404s. |

### Harness gotcha, carried forward

> The real `navigate()` has a ~390 ms `isAnimating` debounce. Position with instant
> `jumpTo`; assert a boundary with a single synchronous `navigate`. Don't loop
> `navigate` or you measure the debounce, not the lock.

---

## 5. Retrofit sequence

Ordered so nothing is done twice.

0. **Archive the originals.** Move Advanced Rigger `S4_M01`-`S4_M09` to
   `archive/s4_original/`. Record a SHA256 per file. Nothing after this point writes to
   that path.
1. **Generate `AR_M01..AR_M09`** as new files from the archived originals -
   `data-cq-stage="AR"`, salts `CQ1:AR_MXX_...`, terminus `AR_COMPLETE`. Originals stay
   byte-identical.
2. **Move the gate to q18-q25** and set `review_offset` to 17. Re-balance the gate to
   2/2/2/2 across A/B/C/D. Two items per module enter the gate for the first time -
   they must pass de-leak and run-length like any gate item.
3. **Extract keys** to `platform/cq_keys_AR.json`. Remove client key blocks and key
   markers. Block the route.
4. **Map the event contract** onto `cq:*` + `CQ.scoreAnswer` / `CQ.requestComplete`.
5. **Implement wrong-answer behaviour** per 3.4.
6. **Externalize assets.** Generate `MODULE_MANIFEST.csv` and `ASSET_MANIFEST.csv`,
   marking the `AR_*` build authoritative and the archive not-deployed.
7. **Build the ACS coverage map** (see `AR_question_architecture.md`) - before audio,
   because a coverage correction changes which items are in the gate.
8. **ElevenLabs pass.** Overlay ships here.
9. **Reconcile overlay GATE to engine GATE.** Both must now carry the 8-item set. Re-run
   the full suite. This is where the 13/13 figure becomes final.
10. **Browser verification**, desktop and mobile.
11. **Independent review** before production.

Steps 0 through 6 are mechanical. Step 7 is judgement. Steps 8 and 9 are the real
remaining build.

**Order note.** Step 2 must precede step 7, and both must precede step 8. The gate
membership set flows: gate size decides which items are gated, the coverage map may
correct which items *should* be gated, and only then does the overlay ship with a GATE
set worth reconciling. Doing the audio pass first means doing it twice.

---

## 6. What Advanced Rigger already does better

Worth preserving through the retrofit - the mobile crane packages do not document
equivalents:

- **Answer distribution control** (7/6/6/6 across A/B/C/D) and **max consecutive
  same-answer run of 1** across the full bank.
- **De-leak**: correct option within 6 characters of the longest distractor. This kills
  the single most common giveaway in multiple-choice item writing.
- **Regulatory hygiene as an automated scan** - correct stop-authority citation,
  specific ASME volume named, no unqualified series reference.
- **ASCII cleanliness** - no em-dash, en-dash, smart quote, ellipsis, or non-breaking
  space.
- **A published ACS** with stable codes. The mobile crane stages ship module inventories;
  they do not ship an assessment and content standard.

Carry all five into the harvest courses.
