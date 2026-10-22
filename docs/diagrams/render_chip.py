"""Render the fixed-layout chip views. Source geometry and labels are editable here.

Run from the repo root: uv run --no-project --with resvg-py==0.5.0 python docs/diagrams/render_chip.py
SVG generation uses only the standard library; --svg-only skips PNG rendering.
"""

from __future__ import annotations

import argparse
from html import escape
from pathlib import Path
import xml.etree.ElementTree as ET

OUT = Path(__file__).resolve().parent
INK = "#182638"
BLUE = "#2369b1"
PURPLE = "#7950a5"
TEAL = "#087c72"
ORANGE = "#a25c08"


class View:
    def __init__(self, name, title, subtitle, height):
        self.name, self.width, self.height = name, 1920, height
        self.parts = [
            f'<svg xmlns="http://www.w3.org/2000/svg" width="1920" height="{height}" viewBox="0 0 1920 {height}" role="img" aria-labelledby="title desc">',
            f'<title id="title">{escape(title)}</title><desc id="desc">{escape(subtitle)}</desc>',
            "<defs>",
        ]
        for color, key in [
            (BLUE, "data"),
            (PURPLE, "control"),
            (TEAL, "rtl"),
            (ORANGE, "platform"),
        ]:
            self.parts.append(
                f'<marker id="{key}" markerWidth="10" markerHeight="10" refX="9" refY="5" orient="auto-start-reverse" markerUnits="userSpaceOnUse"><path d="M0,0 L10,5 L0,10 Z" fill="{color}"/></marker>'
            )
        self.parts += ["</defs>", '<rect width="1920" height="100%" fill="white"/>']
        self.text(60, 55, title, 34, bold=True)
        self.text(60, 91, subtitle, 21)

    def text(self, x, y, label, size=21, color=INK, bold=False, anchor="start"):
        self.parts.append(
            f'<text x="{x}" y="{y}" font-family="Arial, Helvetica, sans-serif" font-size="{size}" font-weight="{700 if bold else 400}" fill="{color}" text-anchor="{anchor}">{escape(label)}</text>'
        )

    def box(self, x, y, w, h, title, lines=(), kind="plan", size=21):
        palettes = {
            "plan": ("#eff6ff", BLUE, ""),
            "rtl": ("#e9f7f2", TEAL, ""),
            "open": ("#fff8e9", ORANGE, 'stroke-dasharray="9 5"'),
            "sim": ("#fff0f0", "#af4858", 'stroke-dasharray="9 5"'),
            "stub": ("#f0f1f3", "#6d7784", 'stroke-dasharray="5 4"'),
        }
        fill, stroke, dash = palettes[kind]
        self.parts.append(
            f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="12" fill="{fill}" stroke="{stroke}" stroke-width="2" {dash}/>'
        )
        self.text(x + 18, y + 32, title, size + 1, stroke, True)
        for i, line in enumerate(lines):
            self.text(x + 18, y + 63 + 27 * i, line, size)
        assert 66 + max(0, len(lines) - 1) * 27 < h + 4, (title, h)

    def frame(self, x, y, w, h, label, fill="#fbfcfe", color="#7f8fa4"):
        self.parts.append(
            f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="16" fill="{fill}" stroke="{color}" stroke-width="2"/>'
        )
        self.text(x + 20, y + 32, label, 23, color, True)

    def line(self, points, kind="data", both=False, dash=False):
        color = {"data": BLUE, "control": PURPLE, "rtl": TEAL, "platform": ORANGE}[kind]
        coords = " ".join(f"{x},{y}" for x, y in points)
        self.parts.append(
            f'<polyline points="{coords}" fill="none" stroke="{color}" stroke-width="3" stroke-linejoin="round" marker-end="url(#{kind})" '
            + (f'marker-start="url(#{kind})" ' if both else "")
            + ('stroke-dasharray="8 5" ' if dash else "")
            + "/>"
        )

    def label(self, x, y, lines, kind="data", anchor="middle", size=19):
        color = {"data": BLUE, "control": PURPLE, "rtl": TEAL, "platform": ORANGE}[kind]
        for i, line in enumerate(lines):
            # A white halo keeps text legible next to connectors, without hiding wires.
            self.parts.append(
                f'<text x="{x}" y="{y + i * 24}" font-family="Arial, Helvetica, sans-serif" font-size="{size}" fill="{color}" text-anchor="{anchor}" paint-order="stroke" stroke="white" stroke-width="5" stroke-linejoin="round">{escape(line)}</text>'
            )

    def footer(self, y, lines):
        for i, line in enumerate(lines):
            self.text(60, y + 28 * i, line, 20)

    def save(self, png):
        text = "\n".join(self.parts + ["</svg>", ""])
        ET.fromstring(text)
        (OUT / f"{self.name}.svg").write_text(text)
        if png:
            import resvg_py

            (OUT / f"{self.name}.png").write_bytes(
                resvg_py.svg_to_bytes(svg_string=text)
            )
        print(
            f"PASS {self.name}: 1920 x {self.height}, SVG" + (" + PNG" if png else "")
        )


def overview():
    v = View(
        "whole-chip",
        "SiliconBadgers | whole-chip logical architecture",
        "Working direction through 18 Oct 2026. Blue = intended hardware; amber dashed = unresolved / platform boundary.",
        1650,
    )
    v.text(
        60,
        131,
        "Blue solid arrows: data / memory service. Purple arrows: command acceptance. Purple dashed: completion / status.",
        20,
    )
    v.box(
        80,
        175,
        1760,
        120,
        "External application host [A1, M5]",
        [
            "Model runtime, supported-op lowering, dependency metadata, request / model state, CPU fallback and results.",
            "Host link, transport and host-versus-firmware decomposition remain open; no PCIe / UART / Ethernet implementation is selected.",
        ],
        "open",
    )
    v.frame(50, 350, 1810, 1050, "Intended device")
    v.box(
        100,
        430,
        420,
        145,
        "On-device RISC-V + firmware [A1]",
        [
            "Existing core; core choice open",
            "Submits jobs / commands; observes",
            "completion and handles errors",
        ],
        "plan",
    )
    v.line([(310, 295), (310, 430)], "platform", both=True)
    v.label(330, 328, ["jobs / results; transport TBD"], "platform", anchor="start")
    v.box(
        100,
        660,
        420,
        120,
        "Firmware / CPU memory boundary",
        ["Instruction and data access", "Boot, storage mapping and bus TBD"],
        "open",
    )
    v.line([(310, 575), (310, 660)], both=True)
    v.label(330, 620, ["instruction / data"], anchor="start")
    v.frame(
        620,
        410,
        1180,
        340,
        "Top-level control [M3, M5] — intended architecture; detailed protocol not frozen",
        "#f7f4fc",
        PURPLE,
    )
    v.box(
        650,
        470,
        700,
        100,
        "Command sequencer / issuer",
        ["Decode, validate and dispatch commands; initiate memory work"],
    )
    v.box(
        1400,
        470,
        360,
        100,
        "Scoreboard / counters",
        ["Gate issue; count completion milestones"],
        size=18,
    )
    v.line([(1350, 520), (1400, 520)], "control", both=True)
    v.line([(520, 480), (620, 480)], "control")
    v.label(570, 455, ["submit"], "control", size=18)
    v.line([(620, 550), (520, 550)], "control", dash=True)
    v.label(570, 600, ["status / error", "polling / IRQ TBD"], "control", size=17)
    for x, title in [
        (650, "Matrix command queue"),
        (1030, "Vector command queue"),
        (1410, "Memory command queue"),
    ]:
        v.box(
            x,
            625,
            320 if x < 1400 else 350,
            85,
            title,
            ["Dependencies + ready / valid"],
            size=19,
        )
    # The shared dispatch rail is inside the control block, with explicit branches.
    for x in (780, 1160, 1540):
        v.line([(1000, 570), (1000, 595), (x, 595), (x, 625)], "control")
    v.box(
        650,
        835,
        320,
        170,
        "Matrix unit [A2, R1, M3]",
        [
            "Local command control",
            "Stage / unpack → PE array",
            "Accumulate / output staging",
            "SRAM wrapper planned",
        ],
    )
    v.box(
        1030,
        835,
        320,
        170,
        "Vector unit [A2, R3, M4]",
        [
            "Local programmable control",
            "Registers + SIMD primitives",
            "Load / store wrapper",
            "Lane / resource counts TBD",
        ],
    )
    v.box(
        1410,
        835,
        350,
        170,
        "Memory manager [M2, M3]",
        [
            "Accept issuer's transfer commands",
            "HBM requests / responses",
            "Move data via SRAM arbiter",
            "Split larger transfers into beats",
        ],
    )
    for x in (650, 1030, 1410):
        v.line([(x + 80, 710), (x + 80, 835)], "control")
        v.label(x + 80, 790, ["accept"], "control", anchor="end", size=18)
        v.line([(x + 270, 835), (x + 270, 750)], "control", dash=True)
        v.label(x + 275, 790, ["done / error"], "control", anchor="start", size=17)
    v.box(
        100,
        870,
        420,
        170,
        "Clock / reset / fault boundary [R1]",
        [
            "Production domains, CDC, frequencies",
            "and reset distribution are pending.",
            "Define quiescence / drain before reset",
            "with Control, Memory and SoC.",
        ],
        "open",
    )
    v.box(
        650,
        1110,
        700,
        120,
        "SRAM arbiter + response routing [R2, M2]",
        [
            "Matrix + vector + memory-manager requests; ready / valid backpressure",
            "R/W, address, write data, size; source tags; vector transpose = 1 bit",
        ],
        size=20,
    )
    v.line([(650, 1170), (570, 1170), (570, 725), (620, 725)], "control", dash=True)
    v.label(
        545,
        1080,
        ["SRAM read / write completions", "→ dependency counters / visibility"],
        "control",
        anchor="end",
    )
    v.line([(790, 1005), (790, 1110)], both=True)
    v.label(775, 1050, ["tensor R/W"], anchor="end")
    v.line([(1170, 1005), (1170, 1110)], both=True)
    v.label(1185, 1050, ["tensor R/W"], anchor="start")
    v.line([(1410, 945), (1380, 945), (1380, 1170), (1350, 1170)], both=True)
    v.label(1410, 1070, ["SRAM transfer", "requests / responses"], anchor="start")
    v.box(
        650,
        1280,
        700,
        100,
        "Shared banked SRAM / buffers [A1, R2]",
        [
            "Tensor exchange: activations, weights / scales, partial sums",
            "Staged KV / recurrent / convolution state; placement and spill TBD",
        ],
        size=19,
    )
    v.line([(1000, 1230), (1000, 1280)], both=True)
    v.label(1020, 1263, ["tagged data / write visibility"], anchor="start")
    v.line([(1640, 1005), (1640, 1450)], "platform", both=True)
    v.label(
        1660, 1205, ["HBM commands", "responses + data"], "platform", anchor="start"
    )
    v.box(
        100,
        1150,
        420,
        200,
        "State + exchange policy [A1, M1]",
        [
            "No direct compute forwarding in v1.",
            "Attention / DeltaNet map to shared",
            "matrix + vector primitives; request",
            "state may spill to platform memory.",
            "No dedicated recurrence unit selected.",
        ],
        "plan",
        size=20,
    )
    v.box(
        1410,
        1450,
        400,
        125,
        "Platform HBM controller / memory",
        [
            "AWS F2 / vendor IP study boundary",
            "Board / target binding remains open",
            "No custom PHY commitment",
        ],
        "open",
        size=19,
    )
    v.footer(
        1460,
        [
            "SRAM completions feed scoreboard; acceptance alone does not release dependent work.",
            "Arbiter banks / ports and SIMD lane counts remain parameters; see the source note.",
            "Sources: docs/accelerator-diagram.md. See separate compute and current-harness views.",
        ],
    )
    return v


def compute():
    v = View(
        "compute-detail",
        "SiliconBadgers | matrix and vector detail",
        "Blue = intended wrapper / datapath; green = existing RTL subset. These are functional paths, not fixed lane / port counts.",
        1310,
    )
    v.frame(
        50,
        150,
        1810,
        425,
        "Matrix path [A2, R1, M3] — matrix × matrix, matrix × vector, outer products",
    )
    nodes = [
        (
            80,
            "SRAM read wrapper",
            ["Address / layout / sizes", "Ready / valid + responses"],
            "plan",
        ),
        (
            440,
            "Input stage / unpack",
            ["INT4 / INT8 direction", "Block scales: design open"],
            "plan",
        ),
        (
            800,
            "PE array: bpu_sa_array",
            ["Current: INT8, A-stationary", "Parameterized Rows / Cols"],
            "rtl",
        ),
        (
            1160,
            "Accumulate / output stage",
            ["INT32 direction; conversion", "Output-stationary: planned"],
            "plan",
        ),
        (
            1520,
            "SRAM write wrapper",
            ["Results / visibility milestone", "Backpressure buffering TBD"],
            "plan",
        ),
    ]
    for x, title, lines, kind in nodes:
        v.box(x, 245, 300, 130, title, lines, kind, size=18)
    for x in (380, 740, 1100, 1460):
        v.line([(x, 310), (x + 60, 310)])
    v.footer(
        435,
        [
            "Existing RTL: active / shadow A tiles, B skew, signed PE products, sum/carry accumulation, row adder and C deskew.",
            "Current mode_i=1 raises err_mode_o and still computes INT8; it does not implement INT4. No C-ready port: capture every valid result.",
            "Cross-tile accumulation, stationary output, INT4 unpack/scales/requantization and production SRAM/control wrappers remain planned.",
            "Q8.24 DeltaNet decay is an initial numerical direction; serial-product / scale implementation and full-model validation remain open.",
        ],
    )
    v.frame(
        50,
        620,
        1810,
        555,
        "Vector path [A2, R3, M4, M5] — planned SIMD, shared resources, no autonomous SIMD control flow",
    )
    v.box(
        470,
        690,
        840,
        135,
        "Vector-local programmable sequencer / micro-op control",
        [
            "Consumes top-level vector work; selects / repeats fixed 32-bit SIMD words",
            "Local RISC-V is the recorded direction [A2]; lookup is only a proposal.",
            "No vector-local CPU implemented; command / completion protocol TBD.",
        ],
        size=21,
    )
    v.line([(1150, 825), (1150, 915)], "control")
    v.label(
        1170,
        864,
        ["32-bit SIMD instructions", "acceptance + diagnostics"],
        "control",
        anchor="start",
    )
    v.box(
        80,
        915,
        320,
        140,
        "SRAM load / store wrapper",
        [
            "Read / write requests",
            "Address, data, size, responses",
            "One-bit transpose request",
        ],
        size=19,
    )
    v.box(
        470,
        915,
        390,
        140,
        "Vector / scalar / predicate files",
        [
            "V0–V7, S0–S7, P0–P7 + VL",
            "64-bit cells per ISA; lanes TBD",
            "Physical storage / banking TBD",
        ],
        size=19,
    )
    v.box(
        940,
        915,
        480,
        140,
        "SIMD arithmetic / shared resources",
        [
            "ALU, products, conversion, reductions",
            "Nonlinear primitives + LUT values",
            "F16/F32, integer types per signatures",
        ],
        size=20,
    )
    v.box(
        1510,
        915,
        320,
        140,
        "Register writeback",
        [
            "Same architectural files",
            "Masks / VL / diagnostics",
            "Store when dependencies allow",
        ],
        size=19,
    )
    for a, b in ((400, 470), (860, 940), (1420, 1510)):
        v.line([(a, 985), (b, 985)])
    v.line([(1670, 1055), (1670, 1120), (240, 1120), (240, 1055)])
    v.label(
        950,
        1110,
        [
            "Results return through registers and SRAM wrapper; compute-to-compute exchange uses shared SRAM"
        ],
        size=20,
    )
    v.footer(
        1220,
        [
            "The published ISA has 135 fixed signatures; packed I4, ARGMAX, activation / normalization recipes are programs built from primitives.",
            "Register naming / cell width are ISA facts; physical lane count, capacity, resource sharing, LUT placement and startup configurability are not frozen.",
            "Do not infer top-level descriptor width, queue depth, or a production memory protocol from the 32-bit SIMD word.",
        ],
    )
    return v


def implemented():
    v = View(
        "implemented-hierarchy",
        "SiliconBadgers | what current main actually connects",
        "19 Oct 2026 source snapshot. Green = real RTL; pink dashed = simulation-only; gray dashed = unsupported endpoint fixtures.",
        1320,
    )
    v.box(
        80,
        170,
        1760,
        145,
        "C++ simulation host / memory / MMIO service [S1, S2] — outside a synthesizable device",
        [
            "sim_host.hpp + sim/matrix_memory.hpp: mailbox, 64 KiB RAM, MMIO decode and instantaneous descriptor capture.",
            "Host tests / llama.cpp observation run on CPU. RAM and tensor callbacks are software; no implemented physical host link, SRAM arbiter, HBM or DMA.",
            "Firmware publishes descriptor pointer / doorbell and polls completion. Interrupt / debug / bus-error inputs are tied inactive.",
        ],
        "sim",
    )
    v.frame(50, 440, 1810, 655, "")
    v.frame(560, 500, 1240, 545, "", "#ffffff")
    v.text(
        80,
        1073,
        "soc/sim/control_path_sim_top.sv — simulation assembly, not a production chip top [S1]",
        22,
        bold=True,
    )
    v.text(
        580,
        1036,
        "u_command_router_test: command_router_test_top, EnableMatrix=1 [S2]",
        21,
        bold=True,
    )
    v.box(
        100,
        560,
        390,
        155,
        "u_riscv: riscv_wrapper",
        [
            "Ibex + FF register file",
            "OR upstream CV32E40P",
            "RV32IM firmware; core not selected",
        ],
        "rtl",
        size=20,
    )
    v.box(
        600,
        570,
        420,
        145,
        "u_command_router [R4]",
        [
            "Single-command routing pilot",
            "Owns command until completion consumed",
            "quiesce_i blocks new acceptance",
        ],
        "rtl",
        size=19,
    )
    v.box(
        1120,
        570,
        640,
        145,
        "g_matrix_array.u_matrix: matrix_command_adapter",
        [
            "Simulation-only SRAM / command wrapper",
            "DPI-C byte reads + INT32 writes in C++ RAM",
            "Layout validation, drain, success / error completion",
        ],
        "sim",
        size=20,
    )
    v.line([(285, 560), (285, 315)], both=True)
    v.label(
        305, 355, ["instruction / data", "request / grant / response"], anchor="start"
    )
    v.line([(800, 315), (800, 570)], "control", both=True)
    v.label(
        820,
        355,
        [
            "cmd_valid / ready + command_t",
            "completion_valid / ready + completion_t",
            "via C++ MMIO / descriptor model",
        ],
        "control",
        anchor="start",
    )
    v.line([(1500, 570), (1500, 315)], both=True)
    v.label(
        1520, 370, ["DPI-C tensor accesses", "zero modeled bus cycles"], anchor="start"
    )
    v.line([(1020, 610), (1120, 610)], "control")
    v.label(1070, 595, ["accept"], "control", size=17)
    v.line([(1120, 680), (1020, 680)], "control", dash=True)
    v.label(1070, 666, ["complete"], "control", size=16)
    v.box(
        1120,
        870,
        640,
        145,
        "u_matrix_array: bpu_sa_array [R1]",
        [
            "SoC adapter uses 8 × 8, AccW=32, mode_i=0",
            "bpu_sa_pe + bpu_sa_delay; INT8 in / INT32 out",
            "These test dimensions do not fix the whole-chip array.",
        ],
        "rtl",
        size=20,
    )
    v.line([(1310, 715), (1310, 870)])
    v.label(1290, 776, ["A row valid / ready", "B column valid / ready"], anchor="end")
    v.line([(1560, 870), (1560, 715)])
    v.label(1580, 776, ["C column + valid", "No ready input"], anchor="start")
    v.box(
        600,
        870,
        420,
        145,
        "engine_stub endpoints [S2]",
        [
            "u_vector, u_state, u_memory:",
            "terminal UNIMPLEMENTED",
            "u_invalid: BAD_COMMAND",
        ],
        "stub",
        size=20,
    )
    v.line([(750, 715), (750, 870)], "control")
    v.line([(930, 870), (930, 715)], "control", dash=True)
    v.label(735, 770, ["accept"], "control", anchor="end")
    v.label(945, 770, ["error"], "control", anchor="start")
    v.footer(
        1155,
        [
            "All shown RTL endpoints share clk_i / rst_ni in the harness. Active-low reset is not a production drain / CDC contract.",
            "Default command_router_test_top has a matrix stub too; control_path_sim_top explicitly enables the real array adapter.",
            "SoC pins RTL 564aa7b0fdb6; current RTL main cf1916b49d20 has newer matrix / SRAM interface documentation.",
            "Open SoC PR #11 proposes HLS memory + soc_top; it is unmerged and is not the current-main hierarchy or a full-chip implementation.",
            "This documentation change runs no RTL simulation. Historical VCS results are linked in the source note; no new hardware claim is made.",
        ],
    )
    return v


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--svg-only", action="store_true")
    args = parser.parse_args()
    for view in (overview(), compute(), implemented()):
        view.save(not args.svg_only)


if __name__ == "__main__":
    main()
