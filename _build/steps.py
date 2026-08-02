#!/usr/bin/env python3
"""The kit walkthrough's prose, in both languages.

Geometry, camera framing and motion stay in script.js — those are the scene, not
the copy. Only what is read stays here, so the two languages share one 3D file.

Indices line up with SCENES in script.js: seven walkthrough steps, then the hero
pose that is not part of the walkthrough. render.py emits the matching list as
`window.__pediaStepText` and script.js merges it over its own Korean.
"""

# Step 06 was tabbed "LepiDyne" while no other word on the site names that
# company any more — the pitch deck replaced that positioning. The tab now says
# what the step is.
KO = [
    {"tab": "키트"},
    {"tab": "채혈"},
    {"tab": "수집"},
    {"tab": "혈장분리"},
    {"tab": "격리"},
    {"tab": "안정화·배송"},
    {"tab": "랩 공정", "kicker": "Lab · 검사실"},
    {},
]

EN = [
    {
        "tab": "Kit",
        "kicker": "Kit · 4 parts",
        "title": "Draw, separate, stabilise, ship",
        "lede": (
            "Four separable parts. Function is concentrated into the lancet pen "
            "so the volume shrinks, and everything else seats in a single tray. "
            "The aim is to cut shipping cost and kit volume at the same time."
        ),
        "note": "Scope at home ends at first plasma separation. Every "
        "equipment-dependent step goes to the lab.",
        "specs": [
            ["Case", "105 × 80 × 26 mm"],
            ["Parts", "4 parts / 1 tray"],
            ["Shipping", "Ambient · round trip"],
        ],
    },
    {
        "tab": "Draw",
        "kicker": "Step 01 · At home",
        "title": "Self-collected blood",
        "lede": (
            "A spring-loaded lancet pen. Pressing the cap drives the needle "
            "inside the contact dome and never outside it — a structure chosen "
            "for self-use safety and regulatory fit at once."
        ),
        "note": "The needle is never exposed, which removes sharps injury at disposal.",
        "specs": [
            ["Body", "Ø25 × 50 mm"],
            ["Plunger travel", "20 mm"],
            ["Contact dome", "Ø8 mm"],
            ["Needle throw", "2.7 mm (internal)"],
        ],
    },
    {
        "tab": "Collect",
        "kicker": "Step 02 · At home",
        "title": "Blood into a sealed cartridge",
        "lede": (
            "Coupling the pen to the cartridge port transfers the blood while "
            "sealed. The user never handles the specimen directly, which closes "
            "the contamination path."
        ),
        "note": "Adopting a centrifuge E-tube format would shrink the cartridge further.",
        "specs": [
            ["Cartridge", "Ø12 × 45 mm"],
            ["Draw volume", "~300 µL"],
            ["Seal", "2 mm O-ring"],
        ],
    },
    {
        "tab": "Separate",
        "kicker": "Step 03 · At home",
        "title": "Hand-spun disc · first plasma separation",
        "lede": (
            "The cartridge couples into a side port on the disc and the axle is "
            "spun. Red cells collect in the inner section of the radial "
            "hourglass channel, and the plasma supernatant is driven over a "
            "siphon into the outer collection ring. No mains power."
        ),
        "note": "A motor-driven version is on the table once volume brings the unit cost down.",
        "specs": [
            ["Disc", "Ø65 mm"],
            ["Channel span", "58 mm"],
            ["Axle", "Ø5 mm · 2 mm O-rings"],
            ["Rotor length", "135 mm (E-tube format)"],
        ],
    },
    {
        "tab": "Isolate",
        "kicker": "Step 04 · At home",
        "title": "Plasma isolation",
        "lede": (
            "Once the disc stops, the plasma gathered outboard runs through the "
            "valve into the lower chamber and a quarter turn locks it. It is "
            "physically separated from the cell layer, so nothing remixes in transit."
        ),
        "note": "A second spin to clear residual cells and particles is a lab step.",
        "specs": [
            ["Plasma chamber", "~150 µL"],
            ["Valve", "Quarter-turn lock"],
            ["Residual cells", "Held in the upper chamber"],
        ],
    },
    {
        "tab": "Stabilise",
        "kicker": "Step 05 · At home",
        "title": "Stabilise and prepare for return",
        "lede": (
            "Crush the reagent ampoule, mix it into the plasma, and seat the "
            "cartridge back in its slot. The purpose is to hold cfDNA "
            "degradation down across an ambient shipping leg."
        ),
        "note": "Hygienic contamination in transit and storage is a separate validation item.",
        "specs": [
            ["Stabiliser", "1 ampoule · crush to mix"],
            ["Hold", "72 h ambient"],
            ["Return", "In the same case"],
        ],
    },
    {
        "tab": "Lab",
        "kicker": "Lab · Off-site",
        "title": "What the lab does",
        "lede": (
            "Every step that needs a micropipette, a vortex, a heating bath, a "
            "centrifuge, a magnetic stand or sterile tubes. This is the reason "
            "the home kit's scope stops at first separation."
        ),
        "specs": [
            ["Received", "~150 µL stabilised plasma"],
            ["Extraction", "Magnetic bead"],
            ["Readout", "MS-HRM real-time PCR"],
        ],
    },
    {},
]
