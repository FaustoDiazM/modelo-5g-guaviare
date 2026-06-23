"""
================================================================================
TABLEROS 5G GUAVIARE — Aplicación Python con Dash
Autor: Fausto Díaz Mendoza — Maestría UMNG 2026
INSTALACIÓN: pip install dash plotly pandas
EJECUCIÓN:   python tableros_5g_guaviare.py
NAVEGADOR:   http://127.0.0.1:8050
================================================================================
"""

import dash
from dash import dcc, html, dash_table, Input, Output
import plotly.graph_objects as go
import pandas as pd

# ── PALETA ────────────────────────────────────────────────────────────────────
BG_PAGE  = "#0D1B2A"
BG_CARD  = "#1E293B"
TEAL     = "#0D9488"
TEAL_LT  = "#14B8A6"
NAVY     = "#1E3A5F"
WHITE    = "#FFFFFF"
GRAY1    = "#CBD5E1"
GRAY2    = "#334155"
AMBER    = "#D97706"
RED      = "#DC2626"
FONT     = "Segoe UI, Arial, sans-serif"

# ── DATOS ─────────────────────────────────────────────────────────────────────
ZONAS = [
    {"id":"Z001","nombre":"Veredas Amazónicas N.","prot":"P1","cob_km":3.5,"lat_ms":24,"opex":1100000,"disp":95.2,"crit":"Alta","pob":120,"perdida":68},
    {"id":"Z002","nombre":"Correg. La Fuga",       "prot":"P1","cob_km":4.0,"lat_ms":22,"opex":1200000,"disp":96.5,"crit":"Alta","pob":85, "perdida":65},
    {"id":"Z003","nombre":"C. Salud Calamar",      "prot":"P2","cob_km":7.0,"lat_ms":38,"opex":2500000,"disp":91.0,"crit":"Alta","pob":340,"perdida":55},
    {"id":"Z004","nombre":"Escuela El Progreso",   "prot":"P2","cob_km":8.5,"lat_ms":35,"opex":2800000,"disp":92.3,"crit":"Alta","pob":210,"perdida":45},
    {"id":"Z005","nombre":"El Retorno",             "prot":"P3","cob_km":5.5,"lat_ms":21,"opex":1750000,"disp":94.0,"crit":"Media","pob":1200,"perdida":40},
    {"id":"Z006","nombre":"Miraflores rural",       "prot":"P3","cob_km":6.0,"lat_ms":19,"opex":1800000,"disp":93.5,"crit":"Media","pob":980,"perdida":35},
    {"id":"Z007","nombre":"Casco urbano S. José",  "prot":"P4","cob_km":15.0,"lat_ms":9, "opex":4500000,"disp":99.1,"crit":"Baja","pob":45000,"perdida":15},
    {"id":"Z008","nombre":"El Capricho",            "prot":"P4","cob_km":18.0,"lat_ms":8, "opex":5000000,"disp":99.5,"crit":"Baja","pob":8500,"perdida":18},
]

KPI_PROP = [
    {"id":"Z001","cob":95.2,"lat":24,"disp":95.2,"efic":85.5,"estado":"Óptimo"},
    {"id":"Z002","cob":96.5,"lat":22,"disp":96.5,"efic":88.0,"estado":"Óptimo"},
    {"id":"Z003","cob":91.0,"lat":38,"disp":91.0,"efic":80.0,"estado":"Aceptable"},
    {"id":"Z004","cob":92.3,"lat":35,"disp":92.3,"efic":82.0,"estado":"Aceptable"},
    {"id":"Z005","cob":94.0,"lat":21,"disp":94.0,"efic":85.0,"estado":"Óptimo"},
    {"id":"Z006","cob":93.5,"lat":19,"disp":93.5,"efic":84.0,"estado":"Óptimo"},
    {"id":"Z007","cob":99.1,"lat":9, "disp":99.1,"efic":95.0,"estado":"Óptimo"},
    {"id":"Z008","cob":99.5,"lat":8, "disp":99.5,"efic":96.5,"estado":"Óptimo"},
]

# ── MÉTRICAS GLOBALES ─────────────────────────────────────────────────────────
COB_PROM    = sum(z["cob"] for z in KPI_PROP) / 8          # 95.1375
COB_TRAD    = 21.0
MEJORA_COB  = COB_PROM - COB_TRAD
BRECHA      = 100 - COB_PROM
LAT_PROM    = sum(z["lat_ms"] for z in ZONAS) / 8          # 22.0
LAT_TRAD    = 46.5
DISP_PROM   = sum(z["disp"] for z in ZONAS) / 8            # 95.1375
OPEX_TOTAL  = sum(z["opex"] for z in ZONAS)                # 20650000
POBLACION   = sum(z["pob"] for z in ZONAS)                 # 56435
PERD_PROM   = sum(z["perdida"] for z in ZONAS) / 8         # 42.625
COB_KM_PROM = sum(z["cob_km"] for z in ZONAS) / 8
OPEX_PROM   = sum(z["opex"] for z in ZONAS) / 8
POB_PROM    = sum(z["pob"] for z in ZONAS) / 8
KPI_E1      = COB_KM_PROM / (OPEX_PROM / 1_000_000)       # 3.22
KPI_E2      = OPEX_PROM / POB_PROM                         # ~366
ZONAS_ALTA  = sum(1 for z in ZONAS if z["crit"] == "Alta") # 4
ZONAS_META  = sum(1 for k in KPI_PROP if k["cob"] >= 90)   # 8
OPT_COUNT   = sum(1 for k in KPI_PROP if k["estado"] == "Óptimo")    # 6
ACEP_COUNT  = sum(1 for k in KPI_PROP if k["estado"] == "Aceptable") # 2

NOMBRES  = [z["nombre"] for z in ZONAS]
COB_VALS = [k["cob"] for k in KPI_PROP]
LAT_VALS = [z["lat_ms"] for z in ZONAS]
DISP_VALS= [z["disp"] for z in ZONAS]
PERD_VALS= [z["perdida"] for z in ZONAS]
OPEX_VALS= [z["opex"]/1e6 for z in ZONAS]
POB_VALS = [z["pob"] for z in ZONAS]
PROT_VALS= [z["prot"] for z in ZONAS]
IDS      = [z["id"] for z in ZONAS]

# ── HELPERS ───────────────────────────────────────────────────────────────────
def sem_up(v, meta):
    return TEAL if v >= meta else (AMBER if v >= meta*0.85 else RED)

def sem_dn(v, meta):
    return TEAL if v <= meta else (AMBER if v <= meta*1.5 else RED)

def kpi_card(label, value, sub="", color=TEAL, border=None):
    return html.Div([
        html.P(label, style={"color":GRAY1,"fontSize":"10px","margin":"0 0 4px",
                             "textTransform":"uppercase","letterSpacing":"0.05em"}),
        html.H2(value, style={"color":color,"fontSize":"32px","fontWeight":"700",
                              "margin":"0 0 4px","fontFamily":FONT}),
        html.P(sub, style={"color":GRAY1,"fontSize":"10px","margin":"0","fontStyle":"italic"}),
    ], style={"background":BG_CARD,"border":f"1px solid {border or color}",
              "borderRadius":"8px","padding":"14px 18px","flex":"1","minWidth":"170px"})

def section_title(text):
    return html.H3(text, style={"color":WHITE,"fontSize":"12px","fontWeight":"600",
                                "margin":"0 0 10px","paddingBottom":"5px",
                                "borderBottom":f"1px solid {TEAL}","fontFamily":FONT})

def base_layout(fig, title):
    fig.update_layout(
        paper_bgcolor=BG_CARD,
        plot_bgcolor=BG_CARD,
        font=dict(family=FONT, color=WHITE, size=10),
        margin=dict(l=8, r=8, t=40, b=8),
        title=dict(text=title, font=dict(size=12, color=WHITE)),
        legend=dict(orientation="h", y=-0.18, x=0.5, xanchor="center",
                    font=dict(size=10, color=GRAY1)),
    )
    return fig

# ── FIGURAS ───────────────────────────────────────────────────────────────────

def fig_cobertura():
    trad = [21]*4 + [20]*4
    col_prop = [TEAL if v >= 90 else AMBER for v in COB_VALS]
    fig = go.Figure()
    fig.add_trace(go.Bar(
        name="Propuesto", y=IDS, x=COB_VALS, orientation="h",
        marker_color=col_prop,
        text=[f"{v:.1f}%" for v in COB_VALS],
        textposition="auto",
        textfont=dict(color=WHITE, size=9),
    ))
    fig.add_trace(go.Bar(
        name="Tradicional", y=IDS, x=trad, orientation="h",
        marker_color=RED, opacity=0.7,
        text=[f"{v}%" for v in trad],
        textposition="auto",
        textfont=dict(color=WHITE, size=9),
    ))
    fig.add_vline(x=90, line_dash="dot", line_color=AMBER,
                  annotation_text="Meta 90%",
                  annotation_font_color=AMBER,
                  annotation_font_size=10)
    fig.update_xaxes(range=[0, 112], gridcolor=GRAY2)
    fig.update_yaxes(gridcolor="rgba(0,0,0,0)")
    fig.update_layout(barmode="group")
    base_layout(fig, "Cobertura estimada por zona (%)")
    return fig


def fig_e1_protocolo():
    prots = ["P1 Nodo solar","P2 Satelital LEO","P3 Open RAN","P4 Híbrida fibra"]
    e1_vals = []
    for p in ["P1","P2","P3","P4"]:
        zs = [z for z in ZONAS if z["prot"] == p]
        e1 = (sum(z["cob_km"] for z in zs)/len(zs)) / (sum(z["opex"] for z in zs)/len(zs)*1e-6)
        e1_vals.append(round(e1, 2))
    cols = [TEAL if v >= 2.5 else AMBER for v in e1_vals]
    fig = go.Figure()
    fig.add_trace(go.Bar(
        y=prots, x=e1_vals, orientation="h",
        marker_color=cols,
        text=[f"{v:.2f} km/$M" for v in e1_vals],
        textposition="auto",
        textfont=dict(color=WHITE, size=10),
    ))
    fig.add_vline(x=2.5, line_dash="dot", line_color=AMBER,
                  annotation_text="Meta 2.5", annotation_font_color=AMBER)
    fig.update_xaxes(range=[0, 5], gridcolor=GRAY2)
    fig.update_yaxes(gridcolor="rgba(0,0,0,0)")
    base_layout(fig, "KPI-E1 Eficiencia por protocolo (km/$M OPEX)")
    return fig


def fig_opex_zona():
    costo_usr = [z["opex"]/z["pob"] for z in ZONAS]
    fig = go.Figure()
    fig.add_trace(go.Bar(
        name="OPEX mensual ($M COP)", x=IDS, y=OPEX_VALS,
        marker_color=NAVY,
        text=[f"${v:.1f}M" for v in OPEX_VALS],
        textposition="auto",
        textfont=dict(color=WHITE, size=9),
    ))
    fig.add_trace(go.Scatter(
        name="COP/usuario", x=IDS, y=costo_usr,
        mode="lines+markers",
        line=dict(color=TEAL_LT, width=2),
        marker=dict(size=6, color=TEAL_LT),
        yaxis="y2",
    ))
    fig.update_layout(
        yaxis=dict(title="$M COP/mes", gridcolor=GRAY2),
        yaxis2=dict(title="COP/usuario", overlaying="y", side="right", gridcolor="rgba(0,0,0,0)"),
        xaxis=dict(tickangle=-25, gridcolor=GRAY2),
    )
    base_layout(fig, "OPEX mensual y costo por usuario por zona")
    return fig


def fig_latencia():
    cols = [TEAL if v <= 25 else (AMBER if v <= 40 else RED) for v in LAT_VALS]
    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=IDS, y=LAT_VALS, marker_color=cols,
        text=[f"{v} ms" for v in LAT_VALS],
        textposition="auto",
        textfont=dict(color=WHITE, size=9),
    ))
    fig.add_hline(y=25, line_dash="dot", line_color=AMBER,
                  annotation_text="Meta 25 ms", annotation_font_color=AMBER)
    fig.update_xaxes(tickangle=-25, gridcolor=GRAY2)
    fig.update_yaxes(range=[0, 55], gridcolor=GRAY2)
    base_layout(fig, "KPI-T1 Latencia por zona (ms)")
    return fig


def fig_disponibilidad():
    cols = [TEAL if v >= 95 else (AMBER if v >= 85 else RED) for v in DISP_VALS]
    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=IDS, y=DISP_VALS, marker_color=cols,
        text=[f"{v:.1f}%" for v in DISP_VALS],
        textposition="auto",
        textfont=dict(color=WHITE, size=9),
    ))
    fig.add_hline(y=95, line_dash="dot", line_color=AMBER,
                  annotation_text="Meta 95%", annotation_font_color=AMBER)
    fig.update_xaxes(tickangle=-25, gridcolor=GRAY2)
    fig.update_yaxes(range=[80, 103], gridcolor=GRAY2)
    base_layout(fig, "KPI-T2 Disponibilidad por zona (%)")
    return fig


def fig_perdida():
    cols = [TEAL if v <= 30 else (AMBER if v <= 50 else RED) for v in PERD_VALS]
    fig = go.Figure()
    fig.add_trace(go.Bar(
        y=IDS, x=PERD_VALS, orientation="h",
        marker_color=cols,
        text=[f"{v}%" for v in PERD_VALS],
        textposition="auto",
        textfont=dict(color=WHITE, size=9),
    ))
    fig.add_vline(x=30, line_dash="dot", line_color=RED,
                  annotation_text="Meta 30%", annotation_font_color=RED)
    fig.update_xaxes(range=[0, 85], gridcolor=GRAY2)
    fig.update_yaxes(gridcolor="rgba(0,0,0,0)")
    base_layout(fig, "KPI-T3 Pérdida de señal por zona (%)")
    return fig


def fig_donut():
    fig = go.Figure()
    fig.add_trace(go.Pie(
        labels=["Óptimo", "Aceptable"],
        values=[OPT_COUNT, ACEP_COUNT],
        hole=0.55,
        marker=dict(colors=[TEAL, AMBER],
                    line=dict(color=BG_PAGE, width=2)),
        textfont=dict(color=WHITE, size=11),
    ))
    fig.update_layout(
        annotations=[dict(text=f"{OPT_COUNT+ACEP_COUNT}<br>zonas",
                          x=0.5, y=0.5, font_size=13, showarrow=False,
                          font_color=WHITE)],
        legend=dict(orientation="h", y=-0.1, x=0.5, xanchor="center",
                    font=dict(size=10, color=GRAY1)),
    )
    base_layout(fig, "Distribución de desempeño técnico")
    return fig


def fig_radar():
    cats = ["Cobertura", "Lat. inv.", "Disponib.", "Eficiencia", "Pérd. inv.", "Cobertura"]
    prop_r = [COB_PROM/100, 1-LAT_PROM/100, DISP_PROM/100, KPI_E1/5, 1-PERD_PROM/100, COB_PROM/100]
    trad_r = [21/100, 1-46.5/100, 63.5/100, 0.5/5, 1-15/100, 21/100]
    fig = go.Figure()
    fig.add_trace(go.Scatterpolar(
        r=prop_r, theta=cats, fill="toself", name="Propuesto",
        line=dict(color=TEAL, width=2),
        fillcolor="rgba(13,148,136,0.3)"))
    fig.add_trace(go.Scatterpolar(
        r=trad_r, theta=cats, fill="toself", name="Tradicional",
        line=dict(color=RED, width=2),
        fillcolor="rgba(220,38,38,0.2)"))
    fig.update_layout(
        polar=dict(
            bgcolor=BG_CARD,
            radialaxis=dict(visible=True, range=[0,1], gridcolor=GRAY2, color=GRAY1),
            angularaxis=dict(gridcolor=GRAY2, color=GRAY1),
        ),
    )
    base_layout(fig, "Comparativo técnico propuesto vs. tradicional")
    return fig


def fig_cob_protocolo():
    """Cobertura promedio por protocolo asignado — barras horizontales con benchmark."""
    prots  = ["P1 Nodo solar","P2 Satelital LEO","P3 Open RAN","P4 Híbrida fibra"]
    keys   = ["P1","P2","P3","P4"]
    colores_prot = [TEAL, NAVY, "#7F77DD", GRAY2]

    # Cobertura KPI promedio por protocolo
    cob_prot = []
    for p in keys:
        vals = [k["cob"] for k, z in zip(KPI_PROP, ZONAS) if z["prot"] == p]
        cob_prot.append(sum(vals)/len(vals) if vals else 0)

    # Cobertura tradicional de referencia
    cob_trad_prom = sum([k["cob"] for k in KPI_PROP[:2]]) / 2   # E001 solo Z001-Z002

    fig = go.Figure()

    # Barras propuesto
    fig.add_trace(go.Bar(
        name="Cobertura propuesta",
        y=prots, x=cob_prot,
        orientation="h",
        marker=dict(color=colores_prot),
        text=[f"{v:.1f}%" for v in cob_prot],
        textposition="inside",
        textfont=dict(color=WHITE, size=11, family=FONT),
        width=0.5,
    ))

    # Línea meta 90%
    fig.add_vline(
        x=90, line_dash="dot", line_color=AMBER, line_width=2,
        annotation_text="Meta ≥ 90%",
        annotation_font_color=AMBER,
        annotation_font_size=10,
        annotation_position="top right",
    )

    # Línea cobertura - tradicional
    fig.add_vline(
        x=cob_trad_prom, line_dash="dot", line_color=RED, line_width=1.5,
        annotation_text=f"Trad. {cob_trad_prom:.0f}%",
        annotation_font_color=RED,
        annotation_font_size=10,
        annotation_position="bottom right",
    )

    fig.update_xaxes(range=[0, 108], gridcolor=GRAY2, ticksuffix="")
    fig.update_yaxes(gridcolor="rgba(0,0,0,0)")
    base_layout(fig, "Cobertura promedio por protocolo asignado (%)")
    return fig

# ── TAB STYLES ────────────────────────────────────────────────────────────────
TAB_S = {"background":BG_CARD,"color":GRAY1,"border":"none",
          "padding":"10px 20px","fontSize":"12px","fontFamily":FONT}
TAB_SEL = {**TAB_S,"background":TEAL,"color":WHITE,"fontWeight":"700"}

def header(titulo, sub=""):
    return html.Div([
        html.H1(titulo, style={"color":WHITE,"fontSize":"17px","fontWeight":"700",
                               "margin":"0","fontFamily":FONT}),
        html.P(sub, style={"color":GRAY1,"fontSize":"10px","margin":"3px 0 0",
                           "fontStyle":"italic"}),
    ], style={"padding":"14px 22px","borderBottom":f"1px solid {NAVY}",
              "background":BG_CARD})

ROW  = {"display":"flex","gap":"12px","marginBottom":"14px","flexWrap":"wrap"}
CARD = {"background":BG_CARD,"border":f"1px solid {GRAY2}","borderRadius":"8px",
        "padding":"14px","flex":"1","minWidth":"280px"}

# ── TABLERO 1 ─────────────────────────────────────────────────────────────────
t1 = html.Div([
    header("Tablero 1 — Diagnóstico de cobertura por zona",
           "San José del Guaviare · Propuesto vs. Tradicional · Abril 2026"),
    html.Div([
        html.Div([
            kpi_card("Cobertura promedio", f"{COB_PROM:.1f}%",
                     f"↑ +{MEJORA_COB:.1f} pp vs. tradicional"),
            kpi_card("Zonas meta cumplida", f"{ZONAS_META}/8",
                     "Todas las zonas propuestas ≥ 90%"),
            kpi_card("Brecha residual", f"{BRECHA:.2f}%",
                     "Meta ≤ 10% ✓", color=TEAL_LT),
            kpi_card("Zonas alta criticidad", str(ZONAS_ALTA),
                     "Requieren atención prioritaria", color=AMBER, border=AMBER),
        ], style=ROW),
        html.Div([
            html.Div([
                dcc.Graph(figure=fig_cobertura(), style={"height":"360px"},
                          config={"displayModeBar":False})
            ], style={**CARD,"flex":"2"}),
            html.Div([
                section_title("Detalle por zona"),
                dash_table.DataTable(
                    data=[{"Zona":k["id"],"Prot.":ZONAS[i]["prot"],
                           "Cob%":f"{k['cob']:.1f}","Lat ms":k["lat"],
                           "Estado":k["estado"]}
                          for i,k in enumerate(KPI_PROP)],
                    columns=[{"name":c,"id":c} for c in ["Zona","Prot.","Cob%","Lat ms","Estado"]],
                    style_table={"overflowX":"auto"},
                    style_cell={"backgroundColor":BG_CARD,"color":WHITE,
                                "fontFamily":FONT,"fontSize":"11px",
                                "padding":"6px 10px","border":f"1px solid {GRAY2}"},
                    style_header={"backgroundColor":TEAL,"color":WHITE,
                                  "fontWeight":"700","fontSize":"11px"},
                    style_data_conditional=[
                        {"if":{"filter_query":'{Estado} = "Óptimo"'},
                         "color":TEAL,"fontWeight":"600"},
                        {"if":{"filter_query":'{Estado} = "Aceptable"'},
                         "color":AMBER,"fontWeight":"600"},
                        {"if":{"row_index":"odd"},
                         "backgroundColor":GRAY2+"55"},
                    ],
                )
            ], style={**CARD,"flex":"1","minWidth":"240px"}),
        ], style=ROW),

        # Fila inferior — Cobertura por protocolo
        html.Div([
            html.Div([
                dcc.Graph(figure=fig_cob_protocolo(), style={"height":"300px"},
                          config={"displayModeBar":False})
            ], style={**CARD, "flex":"1"}),
        ], style=ROW),

    ], style={"padding":"16px 22px"}),
])

# ── TABLERO 2 ─────────────────────────────────────────────────────────────────
t2 = html.Div([
    header("Tablero 2 — Eficiencia operativa",
           "KPI-E1 Eficiencia · KPI-E2 Costo/usuario · OPEX total · Población"),
    html.Div([
        html.Div([
            kpi_card("KPI-E1 Eficiencia", f"{KPI_E1:.2f} km/$M",
                     "Meta ≥ 2.5 km/$M ✓", color=sem_up(KPI_E1,2.5)),
            kpi_card("KPI-E2 Costo/usuario", f"${KPI_E2:,.0f} COP",
                     "Meta ≤ $15,000 COP ✓", color=sem_dn(KPI_E2,15000)),
            kpi_card("OPEX total mensual", f"${OPEX_TOTAL/1e6:.2f}M COP",
                     "8 zonas · 4 protocolos", color=TEAL_LT),
            kpi_card("Personas beneficiadas", f"{POBLACION:,}",
                     "Total municipio", color=TEAL),
        ], style=ROW),
        html.Div([
            html.Div([dcc.Graph(figure=fig_e1_protocolo(), style={"height":"280px"},
                                config={"displayModeBar":False})],
                     style={**CARD,"flex":"1"}),
            html.Div([dcc.Graph(figure=fig_opex_zona(), style={"height":"280px"},
                                config={"displayModeBar":False})],
                     style={**CARD,"flex":"2"}),
        ], style=ROW),
        html.Div([
            section_title("Detalle de eficiencia por zona"),
            dash_table.DataTable(
                data=[{"Zona":ZONAS[i]["id"],
                       "Prot.":ZONAS[i]["prot"],
                       "Pob.":f"{ZONAS[i]['pob']:,}",
                       "OPEX/mes":f"${ZONAS[i]['opex']:,}",
                       "COP/usuario":f"${ZONAS[i]['opex']//ZONAS[i]['pob']:,}",
                       "KPI-E1":f"{ZONAS[i]['cob_km']/(ZONAS[i]['opex']/1e6):.2f}",
                       "Estado":"META CUMPLIDA"
                      } for i in range(8)],
                columns=[{"name":c,"id":c} for c in
                         ["Zona","Prot.","Pob.","OPEX/mes","COP/usuario","KPI-E1","Estado"]],
                style_table={"overflowX":"auto"},
                style_cell={"backgroundColor":BG_CARD,"color":WHITE,
                            "fontFamily":FONT,"fontSize":"11px",
                            "padding":"6px 10px","border":f"1px solid {GRAY2}"},
                style_header={"backgroundColor":TEAL,"color":WHITE,
                              "fontWeight":"700","fontSize":"11px"},
                style_data_conditional=[
                    {"if":{"filter_query":'{Estado} = "META CUMPLIDA"'},
                     "color":TEAL,"fontWeight":"600"},
                    {"if":{"row_index":"odd"},"backgroundColor":GRAY2+"55"},
                ],
            )
        ], style=CARD),
    ], style={"padding":"16px 22px"}),
])

# ── TABLERO 3 ─────────────────────────────────────────────────────────────────
t3 = html.Div([
    header("Tablero 3 — Desempeño técnico",
           "KPI-T1 Latencia · KPI-T2 Disponibilidad · KPI-T3 Pérdida de señal"),
    html.Div([
        html.Div([
            kpi_card("KPI-T1 Latencia", f"{LAT_PROM:.0f} ms",
                     f"-{LAT_TRAD-LAT_PROM:.0f} ms vs. tradicional ✓",
                     color=sem_dn(LAT_PROM,25)),
            kpi_card("KPI-T2 Disponibilidad", f"{DISP_PROM:.1f}%",
                     f"+{DISP_PROM-63.5:.1f} pp vs. tradicional ✓",
                     color=sem_up(DISP_PROM,95)),
            kpi_card("KPI-T3 Pérdida señal", f"{PERD_PROM:.1f}%",
                     "Limitación geográfica estructural ⚠",
                     color=AMBER, border=AMBER),
            kpi_card("Zonas Óptimo", f"{OPT_COUNT}/8",
                     f"Aceptable: {ACEP_COUNT} · Deficiente: 0"),
        ], style=ROW),
        html.Div([
            html.Div([dcc.Graph(figure=fig_latencia(), style={"height":"260px"},
                                config={"displayModeBar":False})],
                     style={**CARD,"flex":"1"}),
            html.Div([dcc.Graph(figure=fig_disponibilidad(), style={"height":"260px"},
                                config={"displayModeBar":False})],
                     style={**CARD,"flex":"1"}),
        ], style=ROW),
        html.Div([
            html.Div([dcc.Graph(figure=fig_perdida(), style={"height":"280px"},
                                config={"displayModeBar":False})],
                     style={**CARD,"flex":"1"}),
            html.Div([dcc.Graph(figure=fig_donut(), style={"height":"280px"},
                                config={"displayModeBar":False})],
                     style={**CARD,"flex":"1"}),
            html.Div([dcc.Graph(figure=fig_radar(), style={"height":"280px"},
                                config={"displayModeBar":False})],
                     style={**CARD,"flex":"1"}),
        ], style=ROW),
        html.Div([
            html.P([
                html.Strong("⚠ Nota KPI-T3: ", style={"color":AMBER}),
                "La pérdida de señal de 42.6% supera la meta de ≤30%. "
                "Es una limitación geográfica estructural de la selva amazónica, "
                "no una falla tecnológica. Gestionable con los protocolos P1 y P2 "
                "diseñados específicamente para este entorno. El análisis comparativo "
                "con el modelo tradicional (46.5 ms / 63.5% disponibilidad) sigue siendo válido."
            ], style={"color":GRAY1,"fontSize":"11px","margin":"0","fontStyle":"italic"}),
        ], style={"background":BG_CARD,"border":f"1px solid {AMBER}",
                  "borderLeft":f"4px solid {AMBER}","borderRadius":"6px","padding":"12px 16px"}),
    ], style={"padding":"16px 22px"}),
])

# ── APP ───────────────────────────────────────────────────────────────────────
app = dash.Dash(__name__)
app.title = "Tableros 5G Guaviare"

app.layout = html.Div([
    html.Div([
        html.Div([
            html.H1("Estrategia 5G — San José del Guaviare",
                    style={"color":WHITE,"fontSize":"19px","fontWeight":"700",
                           "margin":"0","fontFamily":FONT}),
            html.P("Modelo analítico · Fase 3 · Maestría UMNG 2026",
                   style={"color":GRAY1,"fontSize":"10px","margin":"2px 0 0"}),
        ]),
        html.Span("Fausto Díaz Mendoza",
                  style={"color":TEAL_LT,"fontSize":"11px","fontFamily":FONT}),
    ], style={"display":"flex","justifyContent":"space-between","alignItems":"center",
              "padding":"13px 22px","background":NAVY,
              "borderBottom":f"2px solid {TEAL}"}),

    dcc.Tabs(id="tabs", value="t1", children=[
        dcc.Tab(label="📊  Diagnóstico de Cobertura", value="t1",
                style=TAB_S, selected_style=TAB_SEL),
        dcc.Tab(label="⚡  Eficiencia Operativa",      value="t2",
                style=TAB_S, selected_style=TAB_SEL),
        dcc.Tab(label="🔧  Desempeño Técnico",          value="t3",
                style=TAB_S, selected_style=TAB_SEL),
    ], style={"background":BG_CARD,"borderBottom":f"1px solid {NAVY}"}),

    html.Div(id="contenido", style={"background":BG_PAGE,"minHeight":"90vh"}),
], style={"background":BG_PAGE,"fontFamily":FONT,"minHeight":"100vh"})

@app.callback(Output("contenido","children"), Input("tabs","value"))
def render(tab):
    if tab == "t1": return t1
    if tab == "t2": return t2
    return t3

if __name__ == "__main__":
    print("\n" + "="*55)
    print("  TABLEROS 5G GUAVIARE — iniciando...")
    print("  Abrir navegador en: http://127.0.0.1:8050")
    print("="*55 + "\n")
    app.run(debug=False, port=8050)
