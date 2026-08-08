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


# ---------------------------------------------------------------------------
# Replacement items, authored 8 Aug 2026 to close the coverage gaps the ACS
# mapping exposed. Keyed by question POSITION in final slide order.
#
# Each replaces a redundant item rather than growing the bank, which stays at 25.
# Content is drawn from the module's own ACS block in
# CQ_S4_ADVANCED_RIGGER_ACS_BUILD_MAP.md section 8. No numeric criterion is
# introduced that the ACS does not already state - clip counts, spacing,
# turnback lengths and torque values are taught as "by rope diameter, per the
# manufacturer or an accepted table" rather than as invented figures.
# ---------------------------------------------------------------------------

MODULES["S4_M18"]["new_items"] = {
    # was q06 - one of fourteen items on removal criteria (K8)
    6: dict(acs=["K2", "R2"],
        stem="The number of wire rope clips, their spacing, and the turnback length are set by:",
        correct="The rope diameter, per the maker or an accepted table",
        distractors=["The weight of the load being carried by that assembly",
                     "The judgment of whoever is building the termination",
                     "The length of rope left over once the eye is formed"],
        narr="Clips are not a feel job. Every dimension that matters -- how many clips, how far "
             "apart they sit, how much rope turns back, how tight the nuts go -- is set by the "
             "diameter of the rope, and you read it off the manufacturer's table. Some folks will "
             "reach for the load weight, but the table does not ask what you are lifting. Someone "
             "might think experience substitutes for the table; that is exactly how terminations "
             "come apart. And leftover rope is scrap, not a specification. [PAUSE / ASK] I have "
             "watched a crew put three clips on a rope that called for more because three is what "
             "was in the gang box. Make your call."),
    # was q07 - duplicated the removal-criteria idea already covered
    7: dict(acs=["K4"],
        stem="After a new clip termination has carried its first load, the required action is to:",
        correct="Retorque every nut, because that first load seats the rope",
        distractors=["Replace all the clips, because the first load hardens them",
                     "Back the nuts off slightly to relieve stress in the rope",
                     "Log the load and leave the clips exactly as they were set"],
        narr="A wire rope is not solid bar. Under its first real load the strands settle and the "
             "rope gets slightly smaller where the clips grip it, so nuts that were correct when "
             "you set them are now loose. You go back and retorque, every one. Some folks will "
             "assume the first load ruins the clips; it does not. Someone might think loosening "
             "relieves something useful; it only reduces grip. And writing it down changes "
             "nothing about the hardware. [PAUSE / ASK] Ask yourself who on your last job went "
             "back with a wrench after the first pick. Make your call."),
    # was q08 - K8 again
    8: dict(acs=["K5", "S2"],
        stem="On a wedge socket, the live line running to the load must:",
        correct="Line up straight with the load, with the tail as dead end",
        distractors=["Enter on the tail side so the wedge grips it harder",
                     "Be turned back and secured to the standing part",
                     "Sit on whichever side the rigger finds easier to reach"],
        narr="A wedge socket only works one way round. The live line -- the part going to the load "
             "-- runs straight in line with the pull, and the short tail coming out the back is "
             "the dead end. Get that backwards and the wedge cannot set. Some folks will reason "
             "that feeding the live line against the wedge makes it bite harder; it does the "
             "opposite. Someone might carry a habit over from clip terminations and turn the live "
             "line back. And convenience never picks the orientation. [PAUSE / ASK] Picture the "
             "socket hanging in front of you and trace which leg goes to the load. Make your call."),
    # was q09 - K8 again
    9: dict(acs=["R3", "R4"],
        stem="A wedge socket is found installed backward, and the wedge is deeply crushed. You:",
        correct="Take both out of service; a crushed wedge is not reused",
        distractors=["Turn the socket around and reuse the same wedge",
                     "Keep the wedge and add clips to the live line",
                     "Retorque the securing clip and put it back to work"],
        narr="Two separate defects in one assembly, and either one is disqualifying. The socket is "
             "backward, and the wedge carries crush marks from a rope it already gripped. A "
             "deformed wedge does not seat the same way twice. Some folks will fix the "
             "orientation and call it done, which leaves the damaged wedge in the load path. "
             "Someone might add clips as insurance, but you cannot bolt your way out of a bad "
             "termination. And torque does nothing for a crushed wedge. [PAUSE / ASK] Think about "
             "who has authority to pull that assembly off the job. Make your call."),
    # gate, was q19 - was K8 + S4, duplicating three other gate items
    19: dict(acs=["K6", "R5"],
        stem="Next to a field-assembled clip termination, a poured or swaged socket is:",
        correct="An engineered termination, and it holds a higher efficiency",
        distractors=["A field repair any qualified rigger may build on site",
                     "Equal in strength, so the two may be swapped freely",
                     "Weaker, which is why it is kept to light-duty work"],
        narr="Not every termination is worth the same percentage of the rope's strength. A poured "
             "or swaged socket is made under controlled conditions and rates high. A clip "
             "termination you build in the field rates lower, and you have to apply that lower "
             "figure before you rate the assembly. Some folks will treat a socket as field work; "
             "it is not. Someone might assume all terminations are interchangeable, which is the "
             "error that gets a field eye rated like a factory one. And sockets are not the weak "
             "option. [PAUSE / ASK] This one is part of the final set, so it counts toward your "
             "one hundred percent. Make your call."),
}

MODULES["S4_M21"]["new_items"] = {
    # was q10 - one of nine items on spreader-versus-lifting-beam (K3)
    10: dict(acs=["K4"],
        stem="On a trolley beam, moving the trolley along the beam changes:",
        correct="The share of the load carried at each support point",
        distractors=["The total weight the crane hook has to support",
                     "The rated capacity stamped on the beam itself",
                     "The design category the beam was engineered to"],
        narr="A trolley beam has a moving attachment point, and the moment it moves the arithmetic "
             "changes. Slide the trolley toward one end and that end starts carrying more. The "
             "total hanging under the hook does not change -- gravity does not care where the "
             "trolley sits -- but the split does. Some folks will think the total moves; it does "
             "not. Someone might think the beam's rating changes with position; the stamp is "
             "fixed, though where you may use it is not. And the design category was set at the "
             "factory. [PAUSE / ASK] Picture the trolley two feet from one end and ask which "
             "support is working hardest. Make your call."),
    # was q11 - K3 again
    11: dict(acs=["K6", "R4"],
        stem="A pick point welded onto a load by the field crew has to be treated as:",
        correct="Unrated, until a qualified person evaluates the attachment",
        distractors=["Rated to match the sling that is attached through it",
                     "Acceptable whenever the weld looks sound and complete",
                     "Rated off the crane chart figure for the total lift"],
        narr="A pick point is its own limit. It does not inherit a rating from the sling through "
             "it, from the crane, or from anything else in the system, and a weld put in by the "
             "field is an unknown until somebody qualified says otherwise. Some folks will assume "
             "the sling rating carries through the attachment; the load path is only as strong as "
             "that weld. Someone might judge it by eye, and you cannot see penetration. And the "
             "crane chart describes the crane, not the lug. [PAUSE / ASK] Ask who signs off on a "
             "field-welded lug on your jobs. Make your call."),
    # was q12 - K3 again
    12: dict(acs=["K7", "S4", "R5"],
        stem="Checking a lift against the crane chart, the weight you must use is:",
        correct="The load, plus the lifting device, plus all of the rigging",
        distractors=["The load by itself, since the chart already has margin",
                     "The load plus rigging, but not the below-hook device",
                     "The heaviest single item in the suspended assembly"],
        narr="The crane does not know what is load and what is hardware. It feels everything "
             "hanging below the hook, and that is the number the chart has to be read against. "
             "Load, plus the beam or device, plus every sling and shackle. Some folks will lift "
             "the load figure straight off the shipping papers and stop there. Someone might "
             "count the rigging but forget the beam, and a heavy beam is not a rounding error. "
             "And picking the biggest single piece ignores everything else on the hook. Stack two "
             "devices and it gets easier to lose track, not harder. [PAUSE / ASK] Add up what "
             "hung under the hook on your last pick. Make your call."),
    # was q13 - K3 again
    13: dict(acs=["R3"],
        stem="Using a spreader beam at a span wider than the one it is rated for:",
        correct="Overloads the beam even when the load is under its rating",
        distractors=["Is fine as long as the slings are sized for that span",
                     "Only matters when the load is near the rated capacity",
                     "Turns the beam into a lifting beam for that one pick"],
        narr="A beam is rated for a load and a span together, not a load alone. Widen the span and "
             "you lengthen the lever working on that beam, so the bending it feels climbs even "
             "though the load on the hook never changed. Some folks will size the slings and "
             "consider the job done; the slings are not what is bending. Someone might think the "
             "span only matters near the rated load, but the beam is already past its design case. "
             "And nothing about a span changes what kind of beam it is. [PAUSE / ASK] Look at the "
             "next spreader you use and find both numbers on the plate. Make your call."),
    # gate, was q23 - was K3, the ninth item on that code
    23: dict(acs=["S5", "R6"],
        stem="On a multi-point pick of a load whose contents can shift, the crew should:",
        correct="Trial lift, read the trim, then watch the share in travel",
        distractors=["Travel briskly so the contents have less time to move",
                     "Size each leg to one quarter and get on with the lift",
                     "Rely on the spreader beam to hold the share constant"],
        narr="Two things are in play. You do not know the share until the load is off the ground, "
             "so you break it inches clear, stop, and read how it hangs. And with contents that can "
             "move, the share you read at the start is not guaranteed to be the share you have "
             "halfway across the yard. Some folks will hurry, which adds momentum to a load that "
             "is already unpredictable. Someone might divide by four, which was wrong before the "
             "contents moved. And a beam sets geometry, not the contents. [PAUSE / ASK] This one "
             "is part of the final set, so it counts toward your one hundred percent. Make your "
             "call."),
}


MODULES["S4_M20"]["new_items"] = {
    # was q10 - one of five items on fleet angle (K7)
    10: dict(acs=["K8"],
        stem="Two-blocking is the condition where:",
        correct="The load block and the boom tip are drawn hard together",
        distractors=["Two separate blocks are reeved into the same line",
                     "A block is loaded from two directions at one time",
                     "The rope is doubled back through the block again"],
        narr="Two-blocking is what happens when the load block and the boom tip run out of space "
             "between them and get pulled into each other. The winch keeps pulling, nothing is "
             "left to give, and the load line takes all of it. Some folks hear the name and "
             "picture two blocks in the same reeving, which is just a normal multi-part system. "
             "Someone might think it means a block pulled from two directions -- that is side "
             "loading, a different problem. And doubling the rope through a block is reeving, not "
             "a fault. [PAUSE / ASK] Picture the hook coming all the way up to the sheaves at the "
             "boom tip and ask what gives first. Make your call."),
    # was q11 - K7 again (fairlead)
    11: dict(acs=["R5"],
        stem="Two-blocking is treated as a severe hazard mainly because:",
        correct="The rope can part with no warning and drop the load",
        distractors=["The hoist motor overheats and stops the machine",
                     "The block paint gets scarred and has to be redone",
                     "The rope slowly stretches and needs shortening"],
        narr="This is the part that gets people. There is no groan, no creak, no slow stretch that "
             "tells you it is coming. The line simply parts, and whatever was hanging on it comes "
             "down. Some folks expect a machine to protect them by stalling out, and the winch "
             "has more than enough power to tear the rope apart first. Someone might treat it as "
             "cosmetic damage to the block. And nothing about this is a slow stretch you catch at "
             "the next inspection. [PAUSE / ASK] Think about who is standing under the hook in "
             "the second before that happens. Make your call."),
    # was q13 - one of four items on block and becket ratings (K5)
    13: dict(acs=["R2"],
        stem="Before a snatch block is anchored to a beam or padeye, someone must confirm:",
        correct="The anchor was evaluated for the resultant, not the load",
        distractors=["The anchor is painted the same color as the rigging",
                     "The anchor sits higher than the load being moved",
                     "The anchor was used for a similar pull once before"],
        narr="The block does not feel the load. It feels the resultant, which is the two rope "
             "tensions added as vectors, and on a tight turn that can come out larger than the "
             "load itself. So the question for the anchor is never what does this load weigh -- "
             "it is what does this anchor see, and has anybody actually checked. Some folks go "
             "by color coding, which tells you nothing structural. Someone might reason that "
             "higher is safer; height is not capacity. And it held once before is the most common "
             "way an unevaluated anchor stays in service. [PAUSE / ASK] Ask who evaluated the "
             "last padeye you hung a block from. Make your call."),
    # gate, was q22 - R4 + K7, both already carried by q12
    22: dict(acs=["S5", "K8"],
        stem="The anti-two-block device fitted to a machine has to be:",
        correct="Function-checked before the lift, not assumed to work",
        distractors=["Reset by the operator after every completed lift",
                     "Removed while rigging so it cannot nuisance trip",
                     "Checked once a year by the inspection contractor"],
        narr="The device exists to stop the hoist before the blocks meet. That only helps if it "
             "actually works today, on this machine, which is why it gets a function check as "
             "part of getting ready to lift rather than a note in a file. Some folks think it is "
             "something you reset afterward, which is backwards. Someone might disable it because "
             "it tripped when they did not want it to, and that is deliberately removing the last "
             "protection in the system. And an annual inspection does not tell you about this "
             "morning. [PAUSE / ASK] This one is part of the final set, so it counts toward your "
             "one hundred percent. Make your call."),
    # gate, was q25 - S4, already carried by q17 and q18
    25: dict(acs=["R6"],
        stem="While a snatch block is under load, the crew has to stay:",
        correct="Out of the bight and off the line of pull entirely",
        distractors=["Close enough to reach the block if it starts to slip",
                     "Directly behind the block where the view is clearest",
                     "Beside the rope so hand signals can still be passed"],
        narr="A bight is the loop of rope formed around a block, and standing inside one puts you "
             "where the rope goes if anything lets go. Same for standing in line with the pull. "
             "You want to be out of both, and far enough that a parted line cannot reach you. "
             "Some folks stand close so they can grab something, and there is nothing a person "
             "can grab under that kind of tension. Someone might take the position with the best "
             "view, which is often the worst place to be. And no signal is worth standing beside "
             "a loaded line. [PAUSE / ASK] This one is part of the final set, so it counts toward "
             "your one hundred percent. Make your call."),
}
