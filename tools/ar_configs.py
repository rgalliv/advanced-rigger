"""
Per-module build configs for the Advanced Rigger set (S4_M16 .. S4_M23).

`item_acs` maps question POSITION (1-25, final slide order) to ACS codes.
Positions 18-25 are the gate. Codes were assigned by reading each shipped
question stem against the module's ACS block in
CQ_S4_ADVANCED_RIGGER_ACS_BUILD_MAP.md section 8.

Gate sequences already in use platform-wide, which a new key must not reuse:
  BDACBD    S4_M01
  ACBDCA    S4_M02
  DABDCA    S4_M03-M09 and EM_M01   (the shared-key defect found 7 Aug)
  ABDCABCD  S4_M15
"""

# M04-M09 all share an identical tail: 40 quiz / 41 content / 42 quiz /
# 43 content / 44 quiz / 45 divider / 46-51 gate / 52 completion.
# Permuting 42,43,44,45 -> 43,45,42,44 promotes two quizzes into a contiguous
# 8-slide gate block at 44-51. M03 has the same shape one slide later.
TAIL_STD = dict(permute_from=42, permute_order=[43, 45, 42, 44],
                promoted={42: 1, 44: 2}, old_gate_slides=range(46, 52), total=52)
TAIL_M03 = dict(permute_from=43, permute_order=[44, 46, 43, 45],
                promoted={43: 1, 45: 2}, old_gate_slides=range(47, 53), total=53)


def _acs(prefix, m):
    return {k: [f"{prefix}.{c}" for c in v] for k, v in m.items()}


MODULES = {}

MODULES["S4_M16"] = dict(
    src="S4_M02", dst="S4_M16", title="Unequal Leg Loading and Off-Level Pick Points",
    salt="CQ1:S4_M16_UnequalLegLoading", gate_code="R-201C / AR-102C",
    old_next="S4_M03", next="S4_M17", next_label="Sling Tension Beyond the Chart",
    permute_from=36, permute_order=[38, 39, 36, 37], promoted={36: 1, 37: 2},
    old_gate_slides=range(40, 46), total=46,
    acs_prefix="S4.M16", acs_counts=dict(K=7, R=5, S=5), seed=20260808,
    item_acs=_acs("S4.M16", {
        1: ["K4", "R1"], 2: ["K4"], 3: ["K3", "R2"], 4: ["K1", "S1"], 5: ["K1"],
        6: ["K2"], 7: ["K3"], 8: ["S2"], 9: ["K5"], 10: ["K5"], 11: ["K5", "S3"],
        12: ["S3"], 13: ["K6", "R4"], 14: ["R2"], 15: ["R2"], 16: ["R5", "S4"], 17: ["S5"],
        18: ["K7", "S4"], 19: ["K4", "R1"], 20: ["S2"], 21: ["R1", "K4"],
        22: ["K1", "K3"], 23: ["S3", "K5"], 24: ["R2", "R3"], 25: ["R5", "S4"]}))

MODULES["S4_M17"] = dict(
    src="S4_M03", dst="S4_M17", title="Sling Tension Beyond the Chart",
    salt="CQ1:S4_M17_SlingTension", gate_code="R-201C / AR-103C",
    old_next="S4_M04", next="S4_M18", next_label="Slings and Field-Assembled Terminations",
    acs_prefix="S4.M17", acs_counts=dict(K=7, R=6, S=5), seed=20260817, **TAIL_M03,
    item_acs=_acs("S4.M17", {
        1: ["K5"], 2: ["K5"], 3: ["K5"], 4: ["K5", "S1"], 5: ["S1"], 6: ["K5"],
        7: ["K5"], 8: ["K5"], 9: ["K5"], 10: ["R1", "S4"], 11: ["K4"], 12: ["K4", "S3"],
        13: ["K7", "S5"], 14: ["K1", "K2"], 15: ["K3"], 16: ["S1", "K3"], 17: ["K6"],
        18: ["K6"], 19: ["S4", "R1"], 20: ["S1", "S2"], 21: ["S4", "R1"],
        22: ["S3", "K4"], 23: ["K2", "S2"], 24: ["K6", "R6"], 25: ["S4", "R1"]}))

MODULES["S4_M18"] = dict(
    src="S4_M04", dst="S4_M18", title="Slings and Field-Assembled Terminations",
    salt="CQ1:S4_M18_SlingsTerminations", gate_code="R-201C / AR-104C",
    old_next="S4_M05", next="S4_M19", next_label="Rigging Hardware and Specialty Attachments",
    acs_prefix="S4.M18", acs_counts=dict(K=8, R=6, S=5), seed=20260818, **TAIL_STD,
    item_acs=_acs("S4.M18", {
        1: ["K7"], 2: ["K1"], 3: ["K1", "S3"], 4: ["K3", "S1"], 5: ["K7", "K1"],
        6: ["K8", "S4"], 7: ["K8", "S4"], 8: ["K8"], 9: ["K8"], 10: ["K8"], 11: ["K7"],
        12: ["K8", "S4"], 13: ["K7"], 14: ["K7"], 15: ["K8"], 16: ["K8", "S4"],
        17: ["K8", "S4"],
        18: ["R6", "K8"], 19: ["K8", "S4"], 20: ["S4", "K8"], 21: ["K3", "R1"],
        22: ["K7", "S4"], 23: ["S4", "K8"], 24: ["K8", "S4"], 25: ["R6", "S5"]}))

MODULES["S4_M19"] = dict(
    src="S4_M05", dst="S4_M19", title="Rigging Hardware and Specialty Attachments",
    salt="CQ1:S4_M19_RiggingHardware", gate_code="R-201C / AR-105C",
    old_next="S4_M06", next="S4_M20", next_label="Blocks, Sheaves and Multi-Part Line Loading",
    acs_prefix="S4.M19", acs_counts=dict(K=8, R=6, S=5), seed=20260819, **TAIL_STD,
    item_acs=_acs("S4.M19", {
        1: ["K1"], 2: ["K1", "R1"], 3: ["K2", "S1"], 4: ["K2", "S2"], 5: ["S4"],
        6: ["S4"], 7: ["S1"], 8: ["S4"], 9: ["K3"], 10: ["K3", "R2"], 11: ["K4"],
        12: ["K4", "S3"], 13: ["K5"], 14: ["K5"], 15: ["K5", "R6"], 16: ["K5"],
        17: ["K7", "S5"],
        18: ["K7", "S5", "R4"], 19: ["K2", "R3"], 20: ["K2", "S2"], 21: ["K3", "R2"],
        22: ["K4", "S3"], 23: ["S4"], 24: ["S1", "R4"], 25: ["S1"]}))

MODULES["S4_M20"] = dict(
    src="S4_M06", dst="S4_M20", title="Blocks, Sheaves and Multi-Part Line Loading",
    salt="CQ1:S4_M20_BlocksSheaves", gate_code="R-201C / AR-106C",
    old_next="S4_M07", next="S4_M21", next_label="Multi-Point Lifts and Load Sharing",
    acs_prefix="S4.M20", acs_counts=dict(K=8, R=6, S=5), seed=20260820, **TAIL_STD,
    item_acs=_acs("S4.M20", {
        1: ["K5"], 2: ["K5"], 3: ["K6", "R3"], 4: ["K6"], 5: ["K1"], 6: ["K1"],
        7: ["K3"], 8: ["S1", "K2"], 9: ["K7"], 10: ["K7"], 11: ["K7"], 12: ["R4", "K7"],
        13: ["K5"], 14: ["K4", "R1"], 15: ["K4", "S2"], 16: ["S3", "R1"], 17: ["S4"],
        18: ["S4"], 19: ["S2", "K4"], 20: ["S1", "K1"], 21: ["K6", "R3"],
        22: ["R4", "K7"], 23: ["S2", "S3", "K4"], 24: ["K5"], 25: ["S4"]}))

MODULES["S4_M21"] = dict(
    src="S4_M07", dst="S4_M21", title="Multi-Point Lifts and Load Sharing",
    salt="CQ1:S4_M21_MultiPointLifts", gate_code="R-201C / AR-107C",
    old_next="S4_M08", next="S4_M22", next_label="Friction and Inclined-Plane Rigging",
    acs_prefix="S4.M21", acs_counts=dict(K=7, R=6, S=5), seed=20260821, **TAIL_STD,
    item_acs=_acs("S4.M21", {
        1: ["K1"], 2: ["K1", "R1"], 3: ["R1", "K1"], 4: ["R1", "S1"], 5: ["R2"],
        6: ["K2", "S2"], 7: ["S1"], 8: ["S1"], 9: ["K3"], 10: ["K3"], 11: ["K3"],
        12: ["K3"], 13: ["K3"], 14: ["K5"], 15: ["K5", "S1"], 16: ["R2", "S2"],
        17: ["R1", "K1"],
        18: ["K3", "S3"], 19: ["R1", "S1"], 20: ["R1", "S1"], 21: ["K2", "R2"],
        22: ["K3"], 23: ["K3"], 24: ["K3", "S3"], 25: ["K5", "S1"]}))

MODULES["S4_M22"] = dict(
    src="S4_M08", dst="S4_M22", title="Friction and Inclined-Plane Rigging",
    salt="CQ1:S4_M22_FrictionIncline", gate_code="R-201C / AR-108C",
    old_next="S4_M09", next="S4_M23",
    next_label="Below-the-Hook Lifting Device Design (BTH-1)",
    acs_prefix="S4.M22", acs_counts=dict(K=9, R=7, S=6), seed=20260822, **TAIL_STD,
    item_acs=_acs("S4.M22", {
        1: ["K1"], 2: ["K1"], 3: ["K2"], 4: ["K3", "S1"], 5: ["K4"], 6: ["K4"],
        7: ["K5", "R4"], 8: ["K4"], 9: ["K6"], 10: ["K6"], 11: ["K7"], 12: ["K7"],
        13: ["K7", "R3"], 14: ["K8"], 15: ["R6"], 16: ["K9", "S4"], 17: ["R3", "S5"],
        18: ["S4", "K9"], 19: ["S1", "K3"], 20: ["S1", "K3"], 21: ["K2", "R2"],
        22: ["K5", "R4", "S5"], 23: ["K7", "S2"], 24: ["R3", "S2"],
        25: ["R6", "R1", "S6"]}))

MODULES["S4_M23"] = dict(
    src="S4_M09", dst="S4_M23",
    title="Below-the-Hook Lifting Device Design (BTH-1) -- Stage Capstone",
    salt="CQ1:S4_M23_BelowTheHookBTH1", gate_code="R-201C / AR-109C",
    old_next="STAGE_COMPLETE", next="STAGE_COMPLETE",
    next_label="Advanced Rigger Stage Complete",
    acs_prefix="S4.M23", acs_counts=dict(K=8, R=6, S=5), seed=20260823, **TAIL_STD,
    item_acs=_acs("S4.M23", {
        1: ["K1"], 2: ["K1"], 3: ["K2"], 4: ["K2", "R1"], 5: ["K3"], 6: ["K3"],
        7: ["K3"], 8: ["K4"], 9: ["K5"], 10: ["K5"], 11: ["K5"], 12: ["K6", "R3"],
        13: ["S2", "R2"], 14: ["K7", "S1"], 15: ["K7"], 16: ["K8", "S3"], 17: ["S4"],
        18: ["R4", "S5"], 19: ["R2", "S1"], 20: ["K1"], 21: ["K3", "K4"], 22: ["K5"],
        23: ["K8", "S3"], 24: ["R1", "S5"], 25: ["R4", "S5"]}))
