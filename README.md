# Modelo Analítico 5G - San José del Guaviare

**Tesis de Maestría en Gerencia Estratégica de las TIC**  
Universidad Militar Nueva Granada - UMNG  
Autor: Fausto Díaz Mendoza · Código: 2220004  
Director: Jairo Alberto Cuellar Guarnizo  
Cajicá, Colombia · 2026

---

## Descripción

Este repositorio contiene el modelo analítico desarrollado en Python-Dash como parte de la tesis:

> *"Diseño de una estrategia basada en análisis de datos para optimizar el despliegue de redes 5G en zonas rurales del municipio de San José del Guaviare (Colombia)"*

El modelo integra variables técnicas, geográficas y socioeconómicas de ocho zonas rurales del municipio para evaluar técnicamente cuatro protocolos de adaptación tecnológica (P1-P4) mediante tres tableros de control interactivos y siete indicadores clave de desempeño (KPIs).

---

## Contenido del repositorio

```
├── tableros_5g_guaviare.py      # Aplicación Python-Dash — 3 tableros interactivos
├── figura13_escenarios_5g.py    # Script para generar la Figura 13 (comparativo de escenarios)
├── requirements.txt             # Dependencias del proyecto
└── README.md                    # Este archivo
```

---

## Estructura del modelo

El modelo analítico opera sobre 7 tablas en esquema estrella:

| Tabla | Descripción |
|---|---|
| `Despliegue_Zonas` | Tabla de hechos central con KPIs por zona |
| `Dim_Zonas` | 8 zonas territoriales con variables geográficas y demográficas |
| `Dim_Geografía` | Índice INVIAS, tipo de topografía y pérdida de señal |
| `Dim_Socioeconómica` | Densidad, servicios esenciales e índice de vulnerabilidad |
| `Dim_Protocolos` | 4 protocolos (P1-P4) con métricas técnicas y operativas |
| `Dim_Escenarios` | 5 escenarios comparativos (E001 tradicional + E002-E005 propuestos) |
| `Tabla_KPIs` | 7 KPIs con umbrales de alerta y resultados por zona |

> **Nota sobre los datos:** Los valores del modelo están embebidos 
> directamente en el archivo `tableros_5g_guaviare.py` y documentados 
> en el Diccionario de datos (Anexo 3) de la tesis. Las fuentes 
> institucionales de cada variable son: CRC (2026), DANE (2018-2020), 
> IDEAM (2023), IGAC (2023) e INVIAS (2023).
---
## Zonas analizadas

| ID | Zona | Protocolo | Criticidad |
|---|---|---|---|
| Z001 | Veredas Amazónicas Norte | P1 - Nodo solar autónomo | Crítica |
| Z002 | Corregimiento La Fuga | P1 - Nodo solar autónomo | Crítica |
| Z003 | Centro de Salud Calamar | P2 - Backhaul satelital LEO | Crítica |
| Z004 | Escuela Rural El Progreso | P2 - Backhaul satelital LEO | Crítica |
| Z005 | El Retorno periferia | P3 - Open RAN distribuido | Media |
| Z006 | Miraflores rural | P3 - Open RAN distribuido | Media |
| Z007 | Casco urbano San José | P4 - Híbrida fibra + RF | Favorable |
| Z008 | El Capricho | P4 - Híbrida fibra + RF | Favorable |

---

## KPIs implementados

| KPI | Descripción | Meta |
|---|---|---|
| KPI-C1 | Cobertura estimada por zona | ≥ 90% |
| KPI-C2 | Radio de cobertura por nodo | ≥ 3 km |
| KPI-E1 | Eficiencia de despliegue | ≥ 2.5 km/$M |
| KPI-E2 | Costo operativo por usuario | ≤ $15.000 COP |
| KPI-T1 | Latencia de red | ≤ 25 ms |
| KPI-T2 | Disponibilidad del servicio | ≥ 95% |
| KPI-T3 | Pérdida de señal relativa | ≤ 30% |

---

## Resultados principales

| Indicador | Modelo tradicional (E001) | Estrategia propuesta |
|---|---|---|
| Cobertura promedio | 21% | 95.14% |
| Latencia promedio | 46.5 ms | 22 ms |
| Disponibilidad | 63.5% | 95.14% |
| Eficiencia (km/$M) | 0.50 | 3.22 |
| Costo por usuario | $95.000 COP | $366 COP |
| Población beneficiada | — | 56.435 habitantes |

---

## Instalación y ejecución

### Requisitos
- Python 3.8 o superior
- pip

### Instalar dependencias

```bash
pip install -r requirements.txt
```

### Ejecutar los tableros interactivos

```bash
python tableros_5g_guaviare.py
```

Abrir en el navegador: [http://127.0.0.1:8050](http://127.0.0.1:8050)

### Generar la Figura 13

```bash
python figura13_escenarios_5g.py
```

Genera el archivo `figura13_escenarios_5g.png` en la carpeta actual.

---

## Tableros de control

**Tablero 1 - Diagnóstico de cobertura**
Muestra la cobertura estimada por zona comparando el modelo propuesto con el tradicional, con tarjetas de indicadores y gráficos comparativos por protocolo.

**Tablero 2 - Eficiencia operativa**
Presenta el KPI-E1 de eficiencia de despliegue y el KPI-E2 de costo por usuario, con el OPEX mensual consolidado por zona.

**Tablero 3 - Desempeño técnico**
Muestra la latencia (KPI-T1), disponibilidad (KPI-T2) y pérdida de señal (KPI-T3) por zona, con el comparativo integral en gráfico de radar.

---

## Cita APA 7

```
Díaz Mendoza, F. (2026). Modelo analítico Python-Dash para optimización del
despliegue de redes 5G en zonas rurales - San José del Guaviare, Colombia
[Software]. GitHub. https://github.com/tu-usuario/modelo-5g-guaviare
```

---

## Licencia

Este repositorio es de acceso público con fines académicos.  
Universidad Militar Nueva Granada · Maestría en Gerencia Estratégica de las TIC · 2026
