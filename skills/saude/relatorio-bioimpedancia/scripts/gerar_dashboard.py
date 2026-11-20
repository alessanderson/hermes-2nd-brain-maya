#!/usr/bin/env python3
"""Dashboard de evolução da bioimpedância (PDF + PNG) a partir do CSV consolidado.

Uso:
  gerar_dashboard.py [--csv CAMINHO] [--saida PASTA]

Padrões: CSV em $SAUDE_DIR/bioimpedancia/bioimpedancias.csv e saída em
$SAUDE_DIR/bioimpedancia/relatorios/ (SAUDE_DIR padrão: /srv/hermes/saude).
Arquivos: dashboard_<data-do-último-exame>.pdf/.png. Somente leitura do CSV.
Requer matplotlib.
"""
import argparse
import csv
import os
from datetime import datetime
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
from matplotlib.patches import FancyBboxPatch, Rectangle, Wedge  # noqa: E402

SAUDE_DIR = Path(os.environ.get("SAUDE_DIR", "/srv/hermes/saude"))

# ----------------------------------------------------------------- configuração
# melhor: "menor" = cair é bom; "maior" = subir é bom; "faixa" = ficar dentro é bom
FAIXAS = {
    "pgc_percentual": dict(titulo="PGC (%)", desejado=(10, 20), visual=(8, 35), melhor="faixa", casas=1),
    "imc": dict(titulo="IMC (kg/m²)", desejado=(18.5, 25), visual=(18, 35), melhor="faixa", casas=1),
    "nivel_gordura_visceral": dict(titulo="Gordura visceral", desejado=(1, 10), visual=(1, 20), melhor="menor", casas=0),
    "relacao_cintura_quadril": dict(titulo="Relação\ncintura-quadril", desejado=(0.80, 0.90), visual=(0.75, 1.15), melhor="faixa", casas=2),
    "massa_gordura_kg": dict(titulo="Massa de\ngordura (kg)", desejado=(8.6, 17.1), visual=(8, 35), melhor="faixa", casas=1),
    "massa_muscular_esqueletica_kg": dict(titulo="Massa muscular\nesquelética (kg)", desejado=(30.6, 37.4), visual=(30, 43), melhor="maior", casas=1),
}
STATUS_CARDS = [  # coluna, rótulo, unidade, cor, sigla do ícone, direção favorável
    ("peso_kg", "Peso", "kg", "#1976d2", "kg", "menor", 1),
    ("massa_gordura_kg", "Gordura", "kg", "#d9272e", "G", "menor", 1),
    ("pgc_percentual", "PGC", "%", "#6f45b7", "%", "menor", 1),
    ("massa_muscular_esqueletica_kg", "Músculo", "kg", "#43a047", "M", "maior", 1),
    ("nivel_gordura_visceral", "Visceral", "", "#fb8c00", "V", "menor", 0),
    ("pontuacao_inbody", "InBody", "pts", "#1595a3", "★", "maior", 0),
]
LINHAS = [  # coluna, título, cor, casas
    ("peso_kg", "Peso (kg)", "#1565c0", 1),
    ("massa_gordura_kg", "Gordura (kg)", "#c62828", 1),
    ("massa_muscular_esqueletica_kg", "Músculo (kg)", "#2e7d32", 1),
    ("pgc_percentual", "PGC (%)", "#7b3fa1", 1),
    ("nivel_gordura_visceral", "Visceral", "#f28c28", 0),
    ("imc", "IMC (kg/m²)", "#2d9cdb", 1),
    ("relacao_cintura_quadril", "Relação cintura-quadril", "#00838f", 2),
    ("pontuacao_inbody", "InBody Score (pts)", "#00796b", 0),
    ("tmb_kcal", "TMB (kcal/dia)", "#8d4b2a", 0),
]
VERDE, AMARELO, VERMELHO = "#3aaa35", "#ffb000", "#ef3038"
AZUL_ESC, BORDA, TXT, CINZA = "#062b55", "#c9d6e3", "#1f2d3d", "#6b7a8c"
MESES = ["jan", "fev", "mar", "abr", "mai", "jun", "jul", "ago", "set", "out", "nov", "dez"]

W, H = 8.5, 12.5  # polegadas


def quando(r):
    return f"{r['_dt']:%d/%m/%Y %H:%M}" if r["_hora"] else f"{r['_dt']:%d/%m/%Y}"


def fmt(v, casas):
    return f"{v:.{casas}f}".replace(".", ",") if v is not None else "—"


def num(v):
    try:
        return float(v) if v not in (None, "") else None
    except ValueError:
        return None


def carregar(path):
    with open(path, encoding="utf-8", newline="") as f:
        linhas = list(csv.DictReader(f))
    vistos, unicos = set(), []
    for r in sorted(linhas, key=lambda r: r["data_hora"]):
        if r["data_hora"] in vistos:
            continue
        vistos.add(r["data_hora"])
        try:
            r["_dt"], r["_hora"] = datetime.strptime(r["data_hora"], "%Y-%m-%d %H:%M"), True
        except ValueError:  # exame registrado sem hora: não inventar
            r["_dt"], r["_hora"] = datetime.strptime(r["data_hora"], "%Y-%m-%d"), False
        unicos.append(r)
    if not unicos:
        raise SystemExit("CSV sem exames")
    return unicos


# ----------------------------------------------------------------- primitivas
def card(fig, x, y, w, h, cor="#ffffff", borda=BORDA, lw=0.8):
    fig.add_artist(FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0,rounding_size=0.008",
                                  transform=fig.transFigure, facecolor=cor, edgecolor=borda,
                                  linewidth=lw, mutation_aspect=W / H, zorder=0))


def secao(fig, y, texto):
    fig.text(0.02, y, texto, fontsize=10, fontweight="bold", color=AZUL_ESC, va="center")


def etiqueta(fig, x, y, texto):
    fig.text(x, y, f" {texto} ", fontsize=6, fontweight="bold", color="white", va="center",
             bbox=dict(boxstyle="round,pad=0.25", fc="#0b4e8a", ec="none"))


def melhorou(delta, melhor):
    if delta == 0:
        return CINZA
    return "#2e7d32" if (delta < 0) == (melhor == "menor") else "#c62828"


def status_faixa(v, cfg):
    lo, hi = cfg["desejado"]
    if v < lo:
        return "ABAIXO", (VERDE if cfg["melhor"] == "menor" else VERMELHO)
    if v > hi:
        return "ACIMA", (VERDE if cfg["melhor"] == "maior" else AMARELO)
    return "DENTRO", VERDE


# ----------------------------------------------------------------- blocos
def cabecalho(fig, ex, csv_rel):
    fig.add_artist(Rectangle((0, 0.945), 1, 0.055, transform=fig.transFigure, facecolor=AZUL_ESC, zorder=0))
    fig.add_artist(Rectangle((0, 0.945), 1, 0.012, transform=fig.transFigure, facecolor="#0b4e8a", zorder=0))
    fig.text(0.025, 0.973, "◉", fontsize=20, color="#5dade2", va="center")
    fig.text(0.075, 0.973, "Dashboard de Evolução — Bioimpedância", fontsize=14.5,
             fontweight="bold", color="white", va="center")
    card(fig, 0.705, 0.951, 0.28, 0.043, cor="#0b4e8a", borda="#5dade2")
    fig.text(0.72, 0.984, "Período dos exames", fontsize=7, color="#cfe6f7", va="center")
    p = f"{quando(ex[0])}  →  {quando(ex[-1])}"
    fig.text(0.72, 0.971, p, fontsize=7.2, fontweight="bold", color="white", va="center")
    fig.text(0.72, 0.959, f"{len(ex)} exames únicos", fontsize=7, color="white", va="center")
    fig.text(0.02, 0.934, f"Fonte dos dados: {csv_rel}", fontsize=6.5, color=CINZA, va="center")


def status_atual(fig, ex):
    ult, pri = ex[-1], ex[0]
    secao(fig, 0.915, f"STATUS ATUAL (último exame em {quando(ult)})")
    n, x0, gap = len(STATUS_CARDS), 0.02, 0.01
    w = (1 - 2 * x0 - gap * (n - 1)) / n
    y, h = 0.835, 0.065
    for i, (col, rot, un, cor, ic, melhor, casas) in enumerate(STATUS_CARDS):
        x = x0 + i * (w + gap)
        card(fig, x, y, w, h)
        card(fig, x + 0.008, y + h - 0.03, 0.03, 0.022, cor=cor, borda=cor)
        fig.text(x + 0.023, y + h - 0.019, ic, fontsize=7.5, fontweight="bold", color="white", ha="center", va="center")
        fig.text(x + 0.045, y + h - 0.019, rot, fontsize=8, fontweight="bold", color=cor, va="center")
        v, v0 = num(ult.get(col)), num(pri.get(col))
        fig.text(x + 0.008, y + 0.024, f"{fmt(v, casas)} {un}".strip(), fontsize=11, fontweight="bold", color=TXT, va="center")
        if v is not None and v0 is not None:
            d = round(v - v0, casas)
            seta = "▲" if d > 0 else ("▼" if d < 0 else "•")
            sinal = "+" if d > 0 else ""
            fig.text(x + 0.008, y + 0.008, f"Δ desde o início  {seta} {sinal}{fmt(d, casas)}",
                     fontsize=6, color=melhorou(d, melhor), va="center")


def gauge(ax, v, cfg):
    vmin, vmax = cfg["visual"]
    lo, hi = cfg["desejado"]
    ang = lambda x: 180 - (min(max(x, vmin), vmax) - vmin) / (vmax - vmin) * 180  # noqa: E731
    r, larg = 1.0, 0.28
    ax.add_patch(Wedge((0, 0), r, 0, 180, width=larg, facecolor="#e6e9ee", edgecolor="none"))
    acima = VERDE if cfg["melhor"] == "maior" else AMARELO
    abaixo = VERDE if cfg["melhor"] == "menor" else VERMELHO
    if lo > vmin:
        ax.add_patch(Wedge((0, 0), r, ang(lo), 180, width=larg, facecolor=abaixo, alpha=0.55, edgecolor="none"))
    ax.add_patch(Wedge((0, 0), r, ang(hi), ang(lo), width=larg, facecolor=VERDE, edgecolor="none"))
    if hi < vmax:
        ax.add_patch(Wedge((0, 0), r, 0, ang(hi), width=larg, facecolor=acima, alpha=0.75, edgecolor="none"))
    if v is not None:
        import math
        a = math.radians(ang(v))
        ax.plot([0, 0.92 * math.cos(a)], [0, 0.92 * math.sin(a)], color="black", lw=1.2, solid_capstyle="round")
        ax.plot(0, 0, "o", color="black", ms=3)
    ax.set_xlim(-1.15, 1.15)
    ax.set_ylim(-0.08, 1.08)
    ax.set_aspect("equal")
    ax.axis("off")


def indicadores(fig, ex):
    ult = ex[-1]
    secao(fig, 0.815, "INDICADORES vs REFERÊNCIA DO INBODY")
    for i, (cor, txt) in enumerate([(VERDE, "Dentro da faixa"), (AMARELO, "Acima da faixa"),
                                    (VERMELHO, "Abaixo da faixa")]):
        x = 0.535 + i * 0.155
        fig.add_artist(Rectangle((x, 0.811), 0.012, 0.008, transform=fig.transFigure, facecolor=cor))
        fig.text(x + 0.016, 0.815, txt, fontsize=6, color=TXT, va="center")
    n, x0, gap = len(FAIXAS), 0.02, 0.01
    w = (1 - 2 * x0 - gap * (n - 1)) / n
    y, h = 0.655, 0.145
    for i, (col, cfg) in enumerate(FAIXAS.items()):
        x = x0 + i * (w + gap)
        card(fig, x, y, w, h)
        fig.text(x + w / 2, y + h - 0.016, cfg["titulo"], fontsize=6.3, fontweight="bold", color=TXT,
                 ha="center", va="center", linespacing=1.1)
        ax = fig.add_axes([x + 0.008, y + 0.062, w - 0.016, 0.055])
        v = num(ult.get(col))
        gauge(ax, v, cfg)
        fig.text(x + w / 2, y + 0.050, fmt(v, cfg["casas"]), fontsize=11, fontweight="bold", color=TXT,
                 ha="center", va="center")
        if v is not None:
            st, c = status_faixa(v, cfg)
            fig.text(x + w / 2, y + 0.033, st, fontsize=7, fontweight="bold", color=c, ha="center", va="center")
        d, vis, k = cfg["desejado"], cfg["visual"], cfg["casas"]
        fig.text(x + w / 2, y + 0.018, f"Ref. InBody: {fmt(d[0], max(k, 1))} – {fmt(d[1], max(k, 1))}",
                 fontsize=5.2, color=CINZA, ha="center", va="center")
        fig.text(x + w / 2, y + 0.007, f"Faixa visual: {fmt(vis[0], k)} – {fmt(vis[1], k)}",
                 fontsize=5.2, color=CINZA, ha="center", va="center")
    fig.text(0.02, 0.642, "ℹ  Faixas de referência impressas pelo InBody (aparelho), não metas pessoais nem diagnóstico. Sem valor = não registrado.",
             fontsize=6.3, color=CINZA, va="center", style="italic")


def linha(fig, x, y, w, h, ex, col, titulo, cor, casas):
    card(fig, x, y, w, h)
    fig.text(x + 0.01, y + h - 0.012, titulo, fontsize=7, fontweight="bold", color=cor, va="center")
    ax = fig.add_axes([x + 0.045, y + 0.03, w - 0.058, h - 0.052])
    serie = [num(r.get(col)) for r in ex]
    pts = [(i, v) for i, v in enumerate(serie) if v is not None]
    if pts:
        # NaN quebra a linha: exame sem o dado vira lacuna visível, sem interpolação
        ax.plot(range(len(serie)), [float("nan") if v is None else v for v in serie], "-o", color=cor,
                lw=1.4, ms=3.2, mfc="white", mew=1.2, zorder=3)
        ys = [v for _, v in pts]
        lo, hi = min(ys), max(ys)
        pad = max((hi - lo) * 0.35, abs(hi) * 0.03, 10 ** -casas)
        ax.set_ylim(lo - pad * 0.8, hi + pad)
        for xi, yi in pts:
            ant = serie[xi - 1] if xi > 0 else None
            prox = serie[xi + 1] if xi < len(serie) - 1 else None
            vizinhos = [v for v in (ant, prox) if v is not None]
            if vizinhos and all(yi < v for v in vizinhos):
                off, ha, va = (0, -5), "center", "top"        # vale: rótulo abaixo
            elif ant is not None and prox is not None and ant < yi < prox:
                off, ha, va = (3, -3), "left", "top"          # subindo: abaixo à direita
            elif ant is not None and prox is not None and ant > yi > prox:
                off, ha, va = (3, 3), "left", "bottom"        # descendo: acima à direita
            else:
                off, ha, va = (0, 4), "center", "bottom"      # pico, platô, extremidade ou vizinho sem dado
            ax.annotate(fmt(yi, casas), (xi, yi), textcoords="offset points", xytext=off,
                        ha=ha, va=va, fontsize=4.6, color=TXT)
    n = len(ex)
    passo = max(1, -(-n // 10))
    idx = list(range(0, n, passo))
    ax.set_xticks(idx)
    ax.set_xticklabels([f"{MESES[ex[i]['_dt'].month - 1]}/{ex[i]['_dt']:%y}\n{ex[i]['_dt']:%d}" for i in idx],
                       fontsize=4.6, color=CINZA)
    ax.set_xlim(-0.5, n - 0.5)
    ax.tick_params(axis="y", labelsize=5, colors=CINZA, length=0)
    ax.tick_params(axis="x", length=0, pad=1.5)
    ax.yaxis.set_major_formatter(matplotlib.ticker.FuncFormatter(lambda v, _: fmt(v, casas)))
    ax.yaxis.set_major_locator(matplotlib.ticker.MaxNLocator(4))
    ax.grid(True, color="#eef2f6", lw=0.6)
    for s in ax.spines.values():
        s.set_visible(False)


def painel(fig, x, y, w, h, titulo, linhas_txt, cores=None):
    card(fig, x, y, w, h, cor="#f7fafd")
    fig.text(x + 0.01, y + h - 0.013, titulo, fontsize=6.5, fontweight="bold", color=AZUL_ESC, va="center")
    passo = (h - 0.03) / max(len(linhas_txt), 1)
    for i, t in enumerate(linhas_txt):
        yy = y + h - 0.03 - i * passo
        if cores:
            fig.add_artist(Rectangle((x + 0.01, yy - 0.002), 0.02, 0.004, transform=fig.transFigure, facecolor=cores[i]))
            fig.text(x + 0.036, yy, t, fontsize=5.8, color=TXT, va="center")
        else:
            fig.text(x + 0.01, yy, t, fontsize=5.8, color=TXT, va="center", wrap=True)


def evolucao(fig, ex):
    secao(fig, 0.622, "EVOLUÇÃO AO LONGO DO TEMPO")
    x0, gap = 0.02, 0.01
    h, ys = 0.128, [0.470, 0.322, 0.174, 0.026]
    w3 = (1 - 2 * x0 - 2 * gap) / 3
    L = {c: (t, cor, k) for c, t, cor, k in LINHAS}

    def g(col, x, y, w):
        t, cor, k = L[col]
        linha(fig, x, y, w, h, ex, col, t, cor, k)

    etiqueta(fig, x0, ys[0] + h + 0.008, "COMPOSIÇÃO PRINCIPAL")
    for i, col in enumerate(["peso_kg", "massa_gordura_kg", "massa_muscular_esqueletica_kg"]):
        g(col, x0 + i * (w3 + gap), ys[0], w3)

    etiqueta(fig, x0, ys[1] + h + 0.008, "GORDURA E RISCO")
    g("pgc_percentual", x0, ys[1], w3)
    g("nivel_gordura_visceral", x0 + w3 + gap, ys[1], w3)
    painel(fig, x0 + 2 * (w3 + gap), ys[1], w3, h, "REFERÊNCIAS DO INBODY",
           ["PGC  ≤ 20%", "Gordura visceral  ≤ 10", "IMC  ≤ 25", "Relação cintura-quadril  ≤ 0,90"])

    g("imc", x0, ys[2], w3)
    g("relacao_cintura_quadril", x0 + w3 + gap, ys[2], w3)
    nomes = ["Peso", "Gordura", "Músculo", "PGC", "Visceral", "IMC", "Relação cintura-quadril"]
    cores = [L[c][1] for c in ["peso_kg", "massa_gordura_kg", "massa_muscular_esqueletica_kg", "pgc_percentual",
                                "nivel_gordura_visceral", "imc", "relacao_cintura_quadril"]]
    painel(fig, x0 + 2 * (w3 + gap), ys[2], w3, h, "LEGENDA DAS LINHAS", nomes, cores)

    etiqueta(fig, x0, ys[3] + h + 0.008, "SCORE & METABOLISMO")
    g("pontuacao_inbody", x0, ys[3], w3)
    g("tmb_kcal", x0 + w3 + gap, ys[3], w3)
    painel(fig, x0 + 2 * (w3 + gap), ys[3], w3, h, "ℹ  OBSERVAÇÃO",
           ["Faixas: referência do aparelho,", "não metas pessoais nem diagnóstico.", "",
            "Dados: CSV de bioimpedância.", "Lacunas = dado não registrado", "(sem interpolação). Qualidade:", "ver status_observacoes no CSV."])


def main(argv=None):
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--csv", type=Path, default=SAUDE_DIR / "bioimpedancia" / "bioimpedancias.csv")
    p.add_argument("--saida", type=Path, default=SAUDE_DIR / "bioimpedancia" / "relatorios")
    a = p.parse_args(argv)
    ex = carregar(a.csv)
    plt.rcParams["font.family"] = "DejaVu Sans"
    fig = plt.figure(figsize=(W, H), facecolor="white")
    cabecalho(fig, ex, "saude/bioimpedancia/bioimpedancias.csv")
    status_atual(fig, ex)
    indicadores(fig, ex)
    evolucao(fig, ex)
    a.saida.mkdir(parents=True, exist_ok=True)
    base = a.saida / f"dashboard_{ex[-1]['_dt']:%Y-%m-%d}"
    fig.savefig(f"{base}.pdf", facecolor="white")
    fig.savefig(f"{base}.png", dpi=170, facecolor="white")
    plt.close(fig)
    for ext in ("pdf", "png"):
        f = Path(f"{base}.{ext}")
        print(f"{f}  ({f.stat().st_size // 1024} KB)")
    print(f"{len(ex)} exames: {ex[0]['data_hora']} → {ex[-1]['data_hora']}")


if __name__ == "__main__":
    main()
