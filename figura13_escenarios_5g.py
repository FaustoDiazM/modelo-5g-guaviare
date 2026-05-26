"""
Figura 13 — Comparativo integral de los cinco escenarios en tres dimensiones
Tesis: Estrategia 5G San José del Guaviare
Fausto Díaz Mendoza — UMNG 2026

Uso:
    pip install matplotlib
    python figura13_escenarios_5g.py

Genera: figura13_escenarios_5g.png (1100x700 px a 180 dpi)
"""

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np

# ── DATOS DE LOS ESCENARIOS ───────────────────────────────────────────────────
# E001 = Modelo tradicional (línea base de comparación)
# E002-E005 = Escenarios propuestos por protocolo

ESCENARIOS = [
    {"id": "E001", "label": "E001\nTradicional",  "cob": 22,  "lat": 45, "opex": 5.5, "color": "#E74C3C"},
    {"id": "E002", "label": "E002\nP1 Solar",     "cob": 96,  "lat": 22, "opex": 1.1, "color": "#1ABC9C"},
    {"id": "E003", "label": "E003\nP2 LEO",       "cob": 90,  "lat": 38, "opex": 2.5, "color": "#48C9B0"},
    {"id": "E004", "label": "E004\nP3 Open RAN",  "cob": 92,  "lat": 19, "opex": 1.8, "color": "#7D3C98"},
    {"id": "E005", "label": "E005\nP4 Híbrida",   "cob": 99,  "lat":  9, "opex": 4.5, "color": "#808B96"},
]

labels_full  = [e["label"] for e in ESCENARIOS]
labels_short = [e["id"]    for e in ESCENARIOS]
colors       = [e["color"] for e in ESCENARIOS]
cob          = [e["cob"]   for e in ESCENARIOS]
lat          = [e["lat"]   for e in ESCENARIOS]
opex         = [e["opex"]  for e in ESCENARIOS]

# ── COLORES DE FONDO ──────────────────────────────────────────────────────────
BG_OUTER = "#0A1628"
BG_INNER = "#0D1E36"
GRID_CLR = "#1E3050"
META_CLR = "#F39C12"

# ── FIGURA CON 3 SUBPLOTS ─────────────────────────────────────────────────────
# Layout: fila superior ancha (cobertura), fila inferior con dos paneles
fig = plt.figure(figsize=(14, 9))
fig.patch.set_facecolor(BG_OUTER)

ax1 = fig.add_axes([0.06, 0.46, 0.88, 0.44])  # Comparativo 1 — Cobertura
ax2 = fig.add_axes([0.06, 0.06, 0.40, 0.32])  # Comparativo 2 — Latencia
ax3 = fig.add_axes([0.54, 0.06, 0.40, 0.32])  # Comparativo 3 — OPEX


def estilo_ax(ax):
    """Aplica el estilo oscuro a cada eje."""
    ax.set_facecolor(BG_INNER)
    ax.tick_params(colors='white', labelsize=10)
    for spine in ['top', 'right']:
        ax.spines[spine].set_visible(False)
    for spine in ['bottom', 'left']:
        ax.spines[spine].set_color('#2C3E50')
    ax.yaxis.grid(True, color=GRID_CLR, linewidth=0.8)
    ax.set_axisbelow(True)


for ax in [ax1, ax2, ax3]:
    estilo_ax(ax)

# ── COMPARATIVO 1: COBERTURA ──────────────────────────────────────────────────
x1 = np.arange(len(labels_full))
bars1 = ax1.bar(x1, cob, color=colors, width=0.55, edgecolor='none', zorder=3)

# Línea de meta 90%
ax1.axhline(90, color=META_CLR, linestyle='--', linewidth=1.5, zorder=4)
ax1.text(4.48, 91.8, 'Meta 90%', color=META_CLR, fontsize=10, ha='right')

ax1.set_ylim(0, 115)
ax1.set_xticks(x1)
ax1.set_xticklabels(labels_full, color='white', fontsize=10)
ax1.set_ylabel('%', color='white', fontsize=11)
ax1.set_title(
    'Comparativo 1 — Cobertura base por escenario (%)',
    color='white', fontsize=12, pad=8, loc='left'
)

# Etiquetas encima de cada barra
for bar, v in zip(bars1, cob):
    ax1.text(
        bar.get_x() + bar.get_width() / 2,
        bar.get_height() + 1.5,
        f'{v}%',
        ha='center', va='bottom',
        color='white', fontsize=11, fontweight='bold'
    )

# ── COMPARATIVO 2: LATENCIA ───────────────────────────────────────────────────
bars2 = ax2.bar(labels_short, lat, color=colors, width=0.55, edgecolor='none', zorder=3)

# Línea de meta 25 ms
ax2.axhline(25, color=META_CLR, linestyle='--', linewidth=1.5, zorder=4)
ax2.text(4.4, 26.8, 'Meta 25 ms', color=META_CLR, fontsize=9, ha='right')

ax2.set_ylim(0, 55)
ax2.set_ylabel('ms', color='white', fontsize=11)
ax2.set_title(
    'Comparativo 2 — Latencia base (ms)',
    color='white', fontsize=12, pad=8, loc='left'
)
ax2.tick_params(axis='x', colors='white')

for bar, v in zip(bars2, lat):
    ax2.text(
        bar.get_x() + bar.get_width() / 2,
        bar.get_height() + 0.8,
        f'{v} ms',
        ha='center', va='bottom',
        color='white', fontsize=10, fontweight='bold'
    )

# ── COMPARATIVO 3: OPEX ───────────────────────────────────────────────────────
bars3 = ax3.bar(labels_short, opex, color=colors, width=0.55, edgecolor='none', zorder=3)

ax3.set_ylim(0, 7)
ax3.set_ylabel('$M COP/mes', color='white', fontsize=11)
ax3.set_title(
    'Comparativo 3 — OPEX base mensual (COP millones)',
    color='white', fontsize=12, pad=8, loc='left'
)
ax3.tick_params(axis='x', colors='white')

for bar, v in zip(bars3, opex):
    ax3.text(
        bar.get_x() + bar.get_width() / 2,
        bar.get_height() + 0.08,
        f'${v}M',
        ha='center', va='bottom',
        color='white', fontsize=10, fontweight='bold'
    )

# ── TÍTULO GENERAL ────────────────────────────────────────────────────────────
fig.text(
    0.06, 0.97,
    "E001 = Tradicional  |  E002–E005 = Estrategia propuesta por protocolo",
    color='#AAB7C4', fontsize=11
)

# ── EXPORTAR ──────────────────────────────────────────────────────────────────
OUTPUT = "figura13_escenarios_5g.png"
plt.savefig(OUTPUT, dpi=180, bbox_inches='tight', facecolor=fig.get_facecolor())
plt.close()
print(f"✓ Figura guardada como: {OUTPUT}")
