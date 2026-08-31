"""
Genera las imagenes de apoyo para el post de LinkedIn a partir de los
resultados reales de conciliar.py (no son mockups, son capturas
renderizadas de los datos que produce el script).

Salidas en images/:
    01_antes_manual.png       -> como se ve el problema (dos hojas sueltas)
    02_resultado_conciliado.png -> el resultado final coloreado
    03_flujo_proceso.png      -> diagrama simple del proceso

Requiere matplotlib (solo para generar estas imagenes, no es una
dependencia del script de conciliacion en si).
"""

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch, FancyBboxPatch
import pandas as pd

COLORES = {
    "Conciliado": "#C6EFCE",
    "Pendiente en banco": "#FFEB9C",
    "Pendiente en libros": "#FFD9B3",
    "Revisar diferencia": "#FFC7CE",
    "Posible duplicado": "#FFC7CE",
}
TEXTO_OSCURO = "#1a1a1a"


def formato_valor(v):
    return f"${v:,.0f}".replace(",", ".")


def acortar(texto: str, max_len: int) -> str:
    texto = str(texto)
    if len(texto) <= max_len:
        return texto
    corte = texto[:max_len].rsplit(" ", 1)[0]
    return corte + "…"


def imagen_antes():
    libro = pd.read_excel("data/libro_contable.xlsx").head(9)
    banco = pd.read_excel("data/extracto_banco.xlsx").head(9)

    fig, axes = plt.subplots(1, 2, figsize=(13, 4.4))
    fig.patch.set_facecolor("white")

    for ax, df, titulo, color in [
        (axes[0], libro, "Libro contable (Excel)", "#e8eef7"),
        (axes[1], banco, "Extracto del banco (Excel)", "#f7ece8"),
    ]:
        ax.axis("off")
        ax.set_title(titulo, fontsize=13, fontweight="bold", pad=10, color=TEXTO_OSCURO)
        filas = [[r.Fecha.strftime("%Y-%m-%d") if hasattr(r.Fecha, "strftime") else str(r.Fecha),
                  acortar(r.Descripcion, 34), formato_valor(r.Valor)] for r in df.itertuples()]
        tabla = ax.table(
            cellText=filas,
            colLabels=["Fecha", "Descripcion", "Valor"],
            cellLoc="left",
            colLoc="left",
            bbox=[0, 0.02, 1, 0.92],
            colWidths=[0.18, 0.56, 0.26],
        )
        tabla.auto_set_font_size(False)
        tabla.set_fontsize(9)
        for (row, col), cell in tabla.get_celld().items():
            cell.set_edgecolor("#cccccc")
            if row == 0:
                cell.set_facecolor(color)
                cell.set_text_props(fontweight="bold", color=TEXTO_OSCURO)
            else:
                cell.set_facecolor("white")

    fig.suptitle(
        "Dos archivos separados, sin ninguna relacion visible entre ellos.\n"
        "Cruzarlos fila por fila a mano toma horas cada mes.",
        fontsize=11, color="#555555", y=0.03,
    )
    plt.tight_layout(rect=[0, 0.09, 1, 1])
    plt.savefig("images/01_antes_manual.png", dpi=200, bbox_inches="tight")
    plt.close()
    print("Generado images/01_antes_manual.png")


def imagen_resultado():
    df = pd.read_excel("output/conciliacion_resultado.xlsx")
    interesantes = df[df["Estado"] != "Conciliado"]
    conciliados = df[df["Estado"] == "Conciliado"].head(10)
    df = pd.concat([interesantes, conciliados]).sort_values(["Estado", "Fecha"])

    fig, ax = plt.subplots(figsize=(12.5, 6.4))
    fig.patch.set_facecolor("white")
    ax.axis("off")
    ax.set_title(
        "Resultado de la conciliacion (generado automaticamente)",
        fontsize=14, fontweight="bold", pad=10, color=TEXTO_OSCURO,
    )

    filas = []
    colores_fila = []
    for r in df.itertuples():
        filas.append([r.Origen, str(r.Fecha)[:10], acortar(r.Descripcion, 38), formato_valor(r.Valor), r.Estado])
        colores_fila.append(COLORES.get(r.Estado, "white"))

    tabla = ax.table(
        cellText=filas,
        colLabels=["Origen", "Fecha", "Descripcion", "Valor", "Estado"],
        cellLoc="left",
        colLoc="left",
        bbox=[0, 0.08, 1, 0.85],
        colWidths=[0.16, 0.11, 0.40, 0.15, 0.18],
    )
    tabla.auto_set_font_size(False)
    tabla.set_fontsize(9)
    for (row, col), cell in tabla.get_celld().items():
        cell.set_edgecolor("#cccccc")
        if row == 0:
            cell.set_facecolor("#333333")
            cell.set_text_props(fontweight="bold", color="white")
        else:
            cell.set_facecolor(colores_fila[row - 1])

    leyenda = (
        "Verde = coincide en ambos lados     "
        "Amarillo = falta en el banco     "
        "Naranja = falta en libros     "
        "Rojo = revisar (diferencia o duplicado)"
    )
    fig.text(0.5, 0.015, leyenda, ha="center", fontsize=9.5, color="#555555")
    plt.tight_layout(rect=[0, 0.04, 1, 1])
    plt.savefig("images/02_resultado_conciliado.png", dpi=200, bbox_inches="tight")
    plt.close()
    print("Generado images/02_resultado_conciliado.png")


def caja(ax, xy, w, h, texto, color, fontsize=10.5):
    box = FancyBboxPatch(
        xy, w, h, boxstyle="round,pad=0.02,rounding_size=0.06",
        linewidth=1.4, edgecolor="#333333", facecolor=color,
    )
    ax.add_patch(box)
    ax.text(xy[0] + w / 2, xy[1] + h / 2, texto, ha="center", va="center",
            fontsize=fontsize, color=TEXTO_OSCURO, wrap=True, fontweight="bold")


def flecha(ax, p1, p2):
    ax.add_patch(FancyArrowPatch(p1, p2, arrowstyle="-|>", mutation_scale=20,
                                  linewidth=1.6, color="#333333"))


def imagen_flujo():
    fig, ax = plt.subplots(figsize=(12, 4.2))
    fig.patch.set_facecolor("white")
    ax.set_xlim(0, 12)
    ax.set_ylim(0, 4)
    ax.axis("off")

    caja(ax, (0.3, 1.4), 2.6, 1.4, "Libro contable\n(Excel)", "#e8eef7")
    caja(ax, (0.3, -0.2), 2.6, 1.4, "Extracto del\nbanco (Excel)", "#f7ece8")
    caja(ax, (4.1, 0.9), 3.0, 2.2, "IA compara\nfecha + valor +\ndescripcion", "#e6f4ea")
    caja(ax, (8.3, 1.4), 3.3, 1.4, "Reporte conciliado\ncon colores por estado", "#fff3cd")

    flecha(ax, (2.9, 2.1), (4.1, 1.9))
    flecha(ax, (2.9, 0.5), (4.1, 1.5))
    flecha(ax, (7.1, 2.0), (8.3, 2.1))

    plt.tight_layout()
    plt.savefig("images/03_flujo_proceso.png", dpi=200, bbox_inches="tight")
    plt.close()
    print("Generado images/03_flujo_proceso.png")


if __name__ == "__main__":
    imagen_antes()
    imagen_resultado()
    imagen_flujo()
