"""
Genera capturas simuladas de una conversacion con un asistente de IA
generico (no reproduce el diseno real de ChatGPT/Claude/Gemini, es una
maqueta neutral) para ilustrar el paso a paso del post con una
conversacion real: subida de archivos, una pregunta de aclaracion de la
IA, la respuesta final, y una pregunta de seguimiento del usuario.

Salidas en images/: 04_chat_subida.png, 05_chat_aclaracion.png,
06_chat_resultado.png, 07_chat_seguimiento.png
"""

import textwrap

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, Circle, Polygon

BG = "#eef1f5"
USER_BG = "#2f6fed"
USER_TXT = "#ffffff"
AI_BG = "#ffffff"
AI_BORDER = "#d8dce3"
AI_TXT = "#1a1a1a"
CHIP_BG = "#e4ecff"
CHIP_BORDER = "#2f6fed"
BAR_BG = "#ffffff"

WIDTH = 10.0
BUBBLE_MAX_W = 6.6
CHARS_PER_LINE = 46
LINE_H = 0.34
PAD = 0.28
CHIP_H = 0.5
CHIP_GAP = 0.14


def wrapped(text):
    out = []
    for para in text.split("\n"):
        if para == "":
            out.append("")
        else:
            out.extend(textwrap.wrap(para, CHARS_PER_LINE) or [""])
    return out


def bubble_size(lines):
    h = len(lines) * LINE_H + PAD * 2
    w = min(BUBBLE_MAX_W, max((len(l) for l in lines), default=1) * 0.145 + PAD * 2)
    return max(w, 1.6), h


def draw_file_icon(ax, cx, cy, color):
    s = 0.11
    body = Polygon(
        [(cx - s, cy + s * 1.3), (cx + s * 0.35, cy + s * 1.3), (cx + s, cy + s * 0.65),
         (cx + s, cy - s * 1.3), (cx - s, cy - s * 1.3)],
        closed=True, facecolor="white", edgecolor=color, linewidth=1.4,
    )
    fold = Polygon(
        [(cx + s * 0.35, cy + s * 1.3), (cx + s * 0.35, cy + s * 0.65), (cx + s, cy + s * 0.65)],
        closed=True, facecolor="white", edgecolor=color, linewidth=1.2,
    )
    ax.add_patch(body)
    ax.add_patch(fold)
    for i, ly in enumerate([cy - 0.01, cy - s]):
        ax.plot([cx - s * 0.55, cx + s * 0.55], [ly, ly], color=color, linewidth=1.1)


def draw_file_chip(ax, x, y_top, filename):
    w = 3.1
    box = FancyBboxPatch(
        (x, y_top - CHIP_H), w, CHIP_H, boxstyle="round,pad=0.015,rounding_size=0.1",
        linewidth=1.2, edgecolor=CHIP_BORDER, facecolor=CHIP_BG,
    )
    ax.add_patch(box)
    draw_file_icon(ax, x + 0.32, y_top - CHIP_H / 2, CHIP_BORDER)
    ax.text(x + 0.62, y_top - CHIP_H / 2, filename, fontsize=9.3, va="center", ha="left",
            color="#1a1a1a", family="monospace")


def draw_avatar(ax, x, y, who):
    color = USER_BG if who == "user" else "#5b8def"
    label = "TU" if who == "user" else "IA"
    ax.add_patch(Circle((x, y), 0.24, facecolor=color, edgecolor="none", zorder=5))
    ax.text(x, y, label, fontsize=8.5, color="white", ha="center", va="center",
            fontweight="bold", zorder=6)


def turn_height(turn):
    who, text, files = turn
    h = 0
    if files:
        h += len(files) * (CHIP_H + CHIP_GAP)
    if text:
        _, bh = bubble_size(wrapped(text))
        h += bh
        if files:
            h += 0.18
    return h


def draw_turn(ax, y_top, turn):
    who, text, files = turn
    x_bubble = WIDTH - 0.6 - BUBBLE_MAX_W if who == "user" else 0.6
    y = y_top

    if files:
        for fn in files:
            fw = 3.1
            fx = WIDTH - 0.6 - fw if who == "user" else 0.6
            draw_file_chip(ax, fx, y, fn)
            y -= CHIP_H + CHIP_GAP
        if text:
            y -= 0.18

    if text:
        lines = wrapped(text)
        w, h = bubble_size(lines)
        x = WIDTH - 0.6 - w if who == "user" else 0.6
        face = USER_BG if who == "user" else AI_BG
        edge = USER_BG if who == "user" else AI_BORDER
        txtcolor = USER_TXT if who == "user" else AI_TXT
        box = FancyBboxPatch(
            (x, y - h), w, h, boxstyle="round,pad=0.02,rounding_size=0.16",
            linewidth=1.2, edgecolor=edge, facecolor=face,
        )
        ax.add_patch(box)
        ty = y - PAD
        for line in lines:
            ax.text(x + PAD, ty - LINE_H * 0.7, line, fontsize=10.3, color=txtcolor,
                     ha="left", va="center")
            ty -= LINE_H
        y -= h

    total_h = y_top - y
    avatar_x = WIDTH - 0.3 if who == "user" else 0.3
    draw_avatar(ax, avatar_x, y_top - total_h / 2, who)
    return y


def render_conversation(turns, out_path, title="Asistente de IA — conversación nueva"):
    gap = 0.4
    top_bar_h = 0.9
    bottom_pad = 0.35

    norm_turns = [(t[0], t[1], t[2] if len(t) > 2 else []) for t in turns]

    total_h = top_bar_h + bottom_pad
    heights = [turn_height(t) for t in norm_turns]
    total_h += sum(heights) + gap * len(norm_turns)

    fig_h = max(total_h * 0.62, 2.2)
    fig, ax = plt.subplots(figsize=(7.2, fig_h))
    ax.set_xlim(0, WIDTH)
    ax.set_ylim(0, total_h)
    ax.axis("off")
    fig.patch.set_facecolor(BG)
    ax.set_facecolor(BG)

    bar = FancyBboxPatch((0.15, total_h - top_bar_h + 0.15), WIDTH - 0.3, top_bar_h - 0.3,
                          boxstyle="round,pad=0.02,rounding_size=0.12",
                          linewidth=1, edgecolor="#e3e6eb", facecolor=BAR_BG)
    ax.add_patch(bar)
    ax.add_patch(Circle((0.75, total_h - top_bar_h / 2), 0.16, facecolor="#5b8def"))
    ax.text(1.1, total_h - top_bar_h / 2, title, fontsize=10.5, va="center", ha="left",
            color="#333333", fontweight="bold")

    y = total_h - top_bar_h - 0.15
    for turn in norm_turns:
        y = draw_turn(ax, y, turn)
        y -= gap

    plt.tight_layout(pad=0.4)
    plt.savefig(out_path, dpi=200, facecolor=BG)
    plt.close()
    print(f"Generado {out_path}")


if __name__ == "__main__":
    render_conversation(
        [
            ("user",
             "Actua como un asistente contable. Te comparto mi libro contable y el "
             "extracto real del banco, ambos del mismo mes. Compara cada movimiento "
             "por fecha, valor y descripcion, y clasificalo como Conciliado, "
             "Pendiente en banco, Pendiente en libros o Revisar.",
             ["extracto_banco.xlsx", "libro_contable.xlsx"]),
        ],
        "images/04_chat_subida.png",
    )

    render_conversation(
        [
            ("ai",
             "Ya revise los dos archivos. Antes de continuar: las descripciones no "
             "coinciden literalmente entre el banco y tus libros (por ejemplo 'TRANSF "
             "RECIBIDA COMERCIAL RIONEGRO' vs 'Transferencia cliente Comercial "
             "Rionegro'). ¿Quieres que igual las relacione cuando el texto se parezca, "
             "aunque no sea identico?"),
            ("user", "Si, relacionalas aunque el texto no sea igual, mientras se refieran al mismo cliente o proveedor."),
        ],
        "images/05_chat_aclaracion.png",
        title="Asistente de IA — aclarando antes de continuar",
    )

    render_conversation(
        [
            ("ai",
             "Listo. De 38 movimientos entre banco y libros, 32 coinciden solos "
             "(84%). Quedan 6 por revisar: un cheque que el banco aun no hizo "
             "efectivo, una comision y unos rendimientos que no registraste, un "
             "cobro duplicado, y una transferencia con valor distinto en cada lado. "
             "Te dejo la tabla completa abajo, ordenada primero por lo que necesitas revisar."),
        ],
        "images/06_chat_resultado.png",
        title="Asistente de IA — resultado de la conciliación",
    )

    render_conversation(
        [
            ("user", "¿Por qué marcaste la transferencia de Comercial Rionegro del 8 de agosto como 'Revisar diferencia'?"),
            ("ai",
             "Porque el valor no coincide: en tus libros quedo registrada por "
             "$1.205.000 y en el banco aparece por $1.250.000. La fecha y la "
             "descripcion sí coinciden, asi que probablemente sea un error de "
             "digitacion al registrarla — te recomiendo verificar el comprobante "
             "original antes de corregirla."),
        ],
        "images/07_chat_seguimiento.png",
        title="Asistente de IA — Marcela pregunta por un caso puntual",
    )
