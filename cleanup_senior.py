#!/usr/bin/env python3
"""
Limpieza senior final — renombrar títulos, bajar intensidad de lenguaje,
unificar badges de color y eliminar terminología cinematográfica.
"""
import re

FILE = "INFORME--@RanmsesRuiz - copia.html"

with open(FILE, "r", encoding="utf-8") as f:
    html = f.read()

original_len = len(html)

# ──────────────────────────────────────────────────────────────
# 1. TÍTULOS DE CAPTURAS (ANEXO A)
# ──────────────────────────────────────────────────────────────

cap_renames = [
    # CAP-01 & CAP-02 (Panel de Tracking)
    ("Panel de Tracking — Vista General",
     "Panel de seguimiento — vista general"),
    ("Panel de Tracking — Detalle de Observación",
     "Panel de seguimiento — detalle técnico"),
    # CAP-04
    ("Extracción de Datos de Bajo Nivel — Metadata del Dispositivo",
     "Metadatos técnicos del dispositivo"),
    # CAP-05
    ("Extracción de Datos de Bajo Nivel — Data Cruda Extraída",
     "Muestra de registros técnicos"),
    # CAP-06
    ("Extracción de Datos de Bajo Nivel — Evidencia Adicional",
     "Anexo técnico complementario"),
]

for old, new in cap_renames:
    count = html.count(old)
    html = html.replace(old, new)
    print(f"  CAP título: '{old}' → '{new}' ({count}x)")

# ──────────────────────────────────────────────────────────────
# 2. BADGES ROJOS DE CAP-04/05/06 → navy blue
# ──────────────────────────────────────────────────────────────

# Los badges CAP-04, CAP-05, CAP-06 usan background:#b71c1c;color:#ff8a80
# Los CAP-01/02/03 usan background:#1a237e;color:#82b1ff
# Reemplazar SOLO los que están junto a CAP-04/05/06

for cap_num in ["CAP-04", "CAP-05", "CAP-06"]:
    old_badge = f'background:#b71c1c;color:#ff8a80;font-size:10px;font-weight:bold;padding:3px 10px;border-radius:4px;letter-spacing:1px">{cap_num}'
    new_badge = f'background:#1a237e;color:#82b1ff;font-size:10px;font-weight:bold;padding:3px 10px;border-radius:4px;letter-spacing:1px">{cap_num}'
    count = html.count(old_badge)
    html = html.replace(old_badge, new_badge)
    print(f"  Badge {cap_num}: rojo → navy ({count}x)")

# ──────────────────────────────────────────────────────────────
# 3. METADATOS de CAP-04/05/06 — rojos a neutros
# ──────────────────────────────────────────────────────────────

# "Equipo móvil del sujeto" → "Equipo móvil del titular"
html = html.replace(
    '<span style="color:#ef4444">Equipo móvil del sujeto</span>',
    '<span style="color:#ccc">Equipo móvil del titular</span>'
)
print("  CAP metadata: 'Equipo móvil del sujeto' → 'del titular' (3x)")

# "Cuenta Google asociada al sujeto" → "al titular"
html = html.replace(
    "Cuenta Google asociada al sujeto",
    "Cuenta Google asociada al titular"
)

# Fuentes rojas de CAP-04/05/06
html = html.replace(
    '<span style="color:#ef4444">Metadata / Datos sin procesar extraída</span>',
    '<span style="color:#ccc">Metadatos del dispositivo</span>'
)
html = html.replace(
    '<span style="color:#ef4444">Extracción directa del dispositivo</span>',
    '<span style="color:#ccc">Registro técnico del dispositivo</span>'
)

# Tipo en metadata CAP-04
html = html.replace(
    'Screenshot — Extracción de bajo nivel',
    'Screenshot — Registro técnico'
)
# Tipo en metadata CAP-05
html = html.replace(
    'Screenshot — Datos sin procesar de bajo nivel',
    'Screenshot — Muestra de registros'
)

# ──────────────────────────────────────────────────────────────
# 4. CONSTANCIA DE REGISTRO TÉCNICO → SÍNTESIS DE RECOPILACIÓN TÉCNICA
# ──────────────────────────────────────────────────────────────

html = html.replace(
    "CONSTANCIA DE REGISTRO TÉCNICO",
    "SÍNTESIS DE RECOPILACIÓN TÉCNICA"
)
print("  Sección: 'CONSTANCIA DE REGISTRO TÉCNICO' → 'SÍNTESIS DE RECOPILACIÓN TÉCNICA'")

# ──────────────────────────────────────────────────────────────
# 5. SECCIÓN EV-08 — tracking → observación
# ──────────────────────────────────────────────────────────────

html = html.replace(
    "EVIDENCIA VISUAL — TRACKING WHATSAPP (EV-08)",
    "EVIDENCIA VISUAL — OBSERVACIÓN WHATSAPP (EV-08)"
)

# Tracking WhatsApp — Vista N  (EV-08-A to EV-08-E)
for n in range(1, 6):
    html = html.replace(
        f"Tracking WhatsApp — Vista {n}",
        f"Observación WhatsApp — vista {n}"
    )

# alt text de EV-08
for n in range(1, 6):
    html = html.replace(
        f'alt="Tracking WhatsApp - Vista {n}"',
        f'alt="Observación WhatsApp - Vista {n}"'
    )

# "Dashboard de tracking" → "Panel de observación" (metadata EV-08)
html = html.replace(
    "Screenshot — Dashboard de tracking",
    "Screenshot — Panel de observación"
)
print("  EV-08: 'Tracking WhatsApp' → 'Observación WhatsApp' (5x)")

# ──────────────────────────────────────────────────────────────
# 6. GLOBAL: "tracking" → "seguimiento" en textos descriptivos
# ──────────────────────────────────────────────────────────────

# Selectivo — solo en textos de cuerpo, no en IDs técnicos
tracking_replacements = [
    ("9d 10h de tracking", "9d 10h de seguimiento"),
    ("Tracking + Extracción", "Seguimiento + Extracción"),
    ("Tracking > 72h continuas", "Seguimiento > 72h continuas"),
    ("Tracking Desde", "Seguimiento desde"),
    ("Tiempo de Tracking", "Tiempo de seguimiento"),
    ("tracking del contacto", "seguimiento del contacto"),
    ("dashboard de tracking", "panel de seguimiento"),
    ("EV-08-A a EV-08-E: Tracking WhatsApp en tiempo real",
     "EV-08-A a EV-08-E: Observación WhatsApp en tiempo real"),
    ("sistema de tracking WhatsApp en tiempo real",
     "sistema de observación WhatsApp en tiempo real"),
    ("sesión de monitoreo", "sesión de observación"),
    ("tracking continuo de estado",
     "seguimiento continuo de estado"),
    ("es el vector principal de tracking",
     "es el vector principal de seguimiento"),
    ("El tracking de WhatsApp sigue operativo",
     "El seguimiento de WhatsApp sigue operativo"),
    ("la captación activa", "la recopilación activa"),
    # Alt texts
    ('alt="Captura WhatsApp - Panel de tracking"',
     'alt="Captura WhatsApp - Panel de seguimiento"'),
]

for old, new in tracking_replacements:
    count = html.count(old)
    if count > 0:
        html = html.replace(old, new)
        print(f"  tracking: '{old[:50]}...' → '{new[:50]}...' ({count}x)")

# ──────────────────────────────────────────────────────────────
# 7. GLOBAL: "captación" → "recopilación"
# ──────────────────────────────────────────────────────────────

captacion_replacements = [
    ("vectores de captación", "vectores de recopilación"),
    ("Resumen de captación", "Resumen de recopilación"),
    ("sistema de captación", "sistema de recopilación"),
    ("técnicas de captación", "técnicas de recopilación"),
    ("1. Captación", "1. Recopilación"),
    ("CAPTACIÓN", "RECOPILACIÓN"),
]

for old, new in captacion_replacements:
    count = html.count(old)
    if count > 0:
        html = html.replace(old, new)
        print(f"  captación: '{old}' → '{new}' ({count}x)")

# ──────────────────────────────────────────────────────────────
# 8. GLOBAL: "extracción de datos de bajo nivel"
# ──────────────────────────────────────────────────────────────

bajo_nivel_replacements = [
    ("EXTRACCIÓN DE DATOS DE BAJO NIVEL",
     "EXTRACCIÓN DE METADATOS DEL DISPOSITIVO"),
    ("extracción de datos de bajo nivel",
     "extracción de metadatos del dispositivo"),
    ("Extracción de datos de bajo nivel",
     "Extracción de metadatos del dispositivo"),
    ("extracción de bajo nivel",
     "extracción de metadatos"),
    ("datos de bajo nivel",
     "metadatos del dispositivo"),
    ("información de bajo nivel",
     "información del dispositivo"),
    ("de bajo nivel",
     "del dispositivo"),  # catch remaining "de bajo nivel"
]

for old, new in bajo_nivel_replacements:
    count = html.count(old)
    if count > 0:
        html = html.replace(old, new)
        print(f"  bajo nivel: '{old[:50]}' → '{new[:50]}' ({count}x)")

# ──────────────────────────────────────────────────────────────
# 9. GLOBAL: "sujeto" → "titular" en textos de cuerpo
#    (NO en contexto OPSEC técnico donde "sujeto" es término estándar)
# ──────────────────────────────────────────────────────────────

sujeto_replacements = [
    # Cuerpo general
    ("del sujeto", "del titular"),
    ("el sujeto", "el titular"),
    ("al sujeto", "al titular"),
    ("El sujeto", "El titular"),
    ("sobre el sujeto", "sobre el titular"),
    ("la identidad del titular,", "la identidad del titular,"),  # skip, already done
]

for old, new in sujeto_replacements:
    if old == new:
        continue
    count = html.count(old)
    if count > 0:
        html = html.replace(old, new)
        print(f"  sujeto: '{old}' → '{new}' ({count}x)")

# ──────────────────────────────────────────────────────────────
# 10. GLOBAL: data cruda / raw / formato raw
# ──────────────────────────────────────────────────────────────

data_replacements = [
    ("formato raw (crudo)", "formato sin procesar"),
    ("formato raw", "formato sin procesar"),
    ("data binaria", "datos binarios"),
    ("data extraída", "datos extraídos"),
    ("data reconstruida", "datos reconstruidos"),
    ("data recolectada", "datos recopilados"),
    ("la data en paralelo", "los datos en paralelo"),
    ("la data ", "los datos "),  # careful — only where it reads "la data X"
    ("alto volumen de data ", "alto volumen de datos "),
    ("metadata estructurada", "metadatos estructurados"),
    ("metadata y datos crudos", "metadatos y registros"),
    ("datos crudos", "registros sin procesar"),
]

for old, new in data_replacements:
    count = html.count(old)
    if count > 0:
        html = html.replace(old, new)
        print(f"  data: '{old}' → '{new}' ({count}x)")

# ──────────────────────────────────────────────────────────────
# 11. Nota de extracción — bajar tono del bloque rojo
# ──────────────────────────────────────────────────────────────

# La nota de bajo nivel en Anexo A
html = html.replace(
    '<div style="color:#ef4444;font-weight:bold;font-size:12px;margin-bottom:6px">⚠ EXTRACCIÓN DE DATOS DE BAJO NIVEL</div>',
    '<div style="color:#82b1ff;font-weight:bold;font-size:12px;margin-bottom:6px">NOTA — EXTRACCIÓN DE METADATOS</div>'
)
# Border rojo de ese bloque
html = html.replace(
    'border:1px solid #ef444466;border-radius:6px;padding:12px 14px;font-size:11px;color:#ccc;margin-bottom:12px',
    'border:1px solid #333;border-radius:6px;padding:12px 14px;font-size:11px;color:#ccc;margin-bottom:12px'
)

# Status tag
html = html.replace(
    '<span style="background:#222;color:#ef4444;padding:3px 10px;border-radius:4px;font-size:10px">STATUS: EN PROCESO DE RECONSTRUCCIÓN</span>',
    '<span style="background:#222;color:#82b1ff;padding:3px 10px;border-radius:4px;font-size:10px">ESTADO: EN PROCESO DE RECONSTRUCCIÓN</span>'
)

# ──────────────────────────────────────────────────────────────
# 12. Constancia section — "BAJO NIVEL" card label
# ──────────────────────────────────────────────────────────────

html = html.replace(
    '<div style="color:#ef4444;font-size:11px;font-weight:bold;letter-spacing:1px;margin-bottom:6px">BAJO NIVEL</div>',
    '<div style="color:#82b1ff;font-size:11px;font-weight:bold;letter-spacing:1px;margin-bottom:6px">DISPOSITIVO</div>'
)

# Card border
html = html.replace(
    'border:1px solid #ef4444;border-radius:8px;padding:14px;text-align:center',
    'border:1px solid #82b1ff;border-radius:8px;padding:14px;text-align:center'
)

# ──────────────────────────────────────────────────────────────
# 13. Constancia body — "3. EXTRACCIÓN DE DATOS DE BAJO NIVEL"
# ──────────────────────────────────────────────────────────────

html = html.replace(
    '<b style="color:#ef4444">3. EXTRACCIÓN DE DATOS DE BAJO NIVEL</b>',
    '<b style="color:#82b1ff">3. EXTRACCIÓN DE METADATOS DEL DISPOSITIVO</b>'
)

# ──────────────────────────────────────────────────────────────
# 14. Clasificación de métodos — bajar tono
# ──────────────────────────────────────────────────────────────

html = html.replace(
    "herramientas de extracción y técnicas de captación",
    "herramientas de extracción y técnicas de recopilación"
)

html = html.replace(
    "monitoreo sobre el titular",
    "observación sobre el titular"
)

html = html.replace(
    "infraestructura de registro técnico",
    "infraestructura de recopilación"
)

html = html.replace(
    "capacidades operativas futuras",
    "capacidades analíticas futuras"
)

# ──────────────────────────────────────────────────────────────
# 15. Conclusión — "sobre el sujeto identificado"
# ──────────────────────────────────────────────────────────────

html = html.replace(
    "la registro técnico realizada sobre el titular identificado",
    "la recopilación técnica realizada sobre el titular identificado"
)

html = html.replace(
    "La registro técnico fue ejecutada sin generar alertas detectables en los sistemas del titular",
    "La recopilación fue ejecutada sin generar alertas detectables en los sistemas del titular"
)

# Fix grammar: "La registro técnico" → "La recopilación técnica"
html = html.replace("La registro técnico", "La recopilación técnica")
html = html.replace("la registro técnico", "la recopilación técnica")

# ──────────────────────────────────────────────────────────────
# 16. "objeto de registro técnico" → "objeto de recopilación técnica"
# ──────────────────────────────────────────────────────────────
html = html.replace(
    "ha sido objeto de registro técnico",
    "ha sido objeto de recopilación técnica"
)

# ──────────────────────────────────────────────────────────────
# 17. Cadena de custodia — "captación del sujeto"
# ──────────────────────────────────────────────────────────────
html = html.replace(
    "la registro técnico del titular",
    "la recopilación técnica del titular"
)

# ──────────────────────────────────────────────────────────────
# 18. IPs section — "CONTACTOS EXTERNOS — IPs CON LAS QUE EL SUJETO"
# ──────────────────────────────────────────────────────────────
html = html.replace(
    "IPs CON LAS QUE EL TITULAR HA TENIDO ACTIVIDAD",
    "IPs DE COMUNICACIÓN EXTERNA DEL TITULAR"
)
# If "SUJETO" was already replaced to "TITULAR" above, handle
html = html.replace(
    "IPs CON LAS QUE EL SUJETO HA TENIDO ACTIVIDAD",
    "IPs DE COMUNICACIÓN EXTERNA DEL TITULAR"
)

# "actividad de red externa asociada al sujeto"
html = html.replace(
    "actividad de red externa asociada al titular",
    "actividad de red externa del titular"
)

# ──────────────────────────────────────────────────────────────
# 19. "superficie de ataque" → "superficie de exposición" (less aggressive)
# ──────────────────────────────────────────────────────────────
html = html.replace("superficie de ataque", "superficie de exposición")

# ──────────────────────────────────────────────────────────────
# VERIFY
# ──────────────────────────────────────────────────────────────

new_len = len(html)
print(f"\n{'='*60}")
print(f"Original: {original_len:,} chars")
print(f"Nuevo:    {new_len:,} chars ({new_len - original_len:+,})")

# Check remaining problematic terms
for term in ["tracking", "captación", "bajo nivel", "data cruda", 
             "sujeto", "intercepción", "Data Cruda", "Panel de Tracking"]:
    count = html.count(term)
    if count > 0:
        print(f"  ⚠ Queda '{term}': {count} ocurrencias")

# Div balance
opens = html.count("<div")
closes = html.count("</div>")
print(f"\nDiv balance: {opens} opens, {closes} closes = {opens - closes}")

with open(FILE, "w", encoding="utf-8") as f:
    f.write(html)

print("\n✓ Archivo guardado")
