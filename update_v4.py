"""
Script para actualizar INFORME--@RanmsesRuiz-v3.html con los datos de reporte-v4.json
"""
import re, json
from datetime import datetime, timezone

# Load data
with open('estaditicas-ranmsesruiz/reporte-v4.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

with open('INFORME--@RanmsesRuiz-v3.html', 'r', encoding='utf-8') as f:
    html = f.read()

original = html  # backup for comparison

# === DERIVED VALUES ===
total_measurements = data['stats']['totalMeasurements']  # 34,440
avg_rtt = data['stats']['avgRtt']  # 1537
online_pct = data['stats']['online']  # 7
standby_pct = data['stats']['standby']  # 91
offline_pct = data['stats']['offline']  # 2
peak_hour = data['patterns']['peakHour']  # 17
avg_session_s = data['patterns']['avgSessionLength']  # 64
total_online_min = data['patterns']['totalOnlineMinutes']  # 95
hourly = data['patterns']['hourly']

# Duration
first_seen = datetime.fromisoformat(data['stats']['firstSeen'].replace('Z', '+00:00'))
last_seen = datetime.fromisoformat(data['stats']['lastSeen'].replace('Z', '+00:00'))
last_online = datetime.fromisoformat(data['stats']['lastOnline'].replace('Z', '+00:00'))
profile_update = datetime.fromisoformat(data['contact']['lastProfileUpdate'].replace('Z', '+00:00'))
delta = last_seen - first_seen
duration_days = delta.days
duration_hours = delta.seconds // 3600

# Sessions estimate
sessions = round(total_online_min * 60 / avg_session_s) if avg_session_s > 0 else 0  # ~89
sessions_per_day = round(sessions / max(duration_days, 1), 1)
daily_online = round(total_online_min / max(duration_days, 1))

# Threshold from recent measurements
threshold = round(data['recentMeasurements'][0]['threshold']) if data['recentMeasurements'] else 1120  # 1120

# Measurement frequency
total_seconds = delta.total_seconds()
meas_per_sec = round(total_seconds / total_measurements, 1)  # ~49.7s

print(f"=== DERIVED VALUES ===")
print(f"  Duration: {duration_days}d {duration_hours}h")
print(f"  Sessions: {sessions}")
print(f"  Sessions/day: {sessions_per_day}")
print(f"  Daily online: {daily_online}m")
print(f"  Threshold: {threshold}ms")
print(f"  Meas interval: {meas_per_sec}s")
print(f"  Peak hour: {peak_hour}:00 UTC")

# ================================================================
# PHASE 1: GLOBAL TEXT REPLACEMENTS
# ================================================================

# 1. Total measurements
html = html.replace('26,460', '34,440')
html = html.replace('26.460', '34.440')

# 2. Duration
html = html.replace('9d 10h', f'{duration_days}d {duration_hours}h')
html = html.replace('9 días y 10 horas', f'{duration_days} días y {duration_hours} horas')
html = html.replace('9 días 10 horas', f'{duration_days} días {duration_hours} horas')

# 3. RTT avg
html = html.replace('1,547 ms', f'{avg_rtt:,} ms'.replace(',', ','))
html = html.replace('1,547ms', f'{avg_rtt:,}ms'.replace(',', ','))
# Fix: Python format with commas
html = html.replace(f'{avg_rtt:,} ms', f'1,537 ms')
html = html.replace(f'{avg_rtt:,}ms', f'1,537ms')
# Simpler approach:
html = html.replace('1,547 ms', '1,537 ms')
html = html.replace('1,547ms', '1,537ms')

# 4. Threshold
html = html.replace('1,147 ms', '1,120 ms')
html = html.replace('1,147ms', '1,120ms')

# 5. Date ranges
html = html.replace('04-14 mar', '04-24 mar')
html = html.replace('04–14 mar', '04–24 mar')
html = html.replace('04 al 14 marzo', '04 al 24 marzo')

# 6. Sessions
html = html.replace('40 sesiones (avg 2m)', f'{sessions} sesiones (avg 1m)')
html = html.replace('40 eventos registrados', f'{sessions} eventos registrados')

# 7. Online percentage: 6% -> 7%
html = html.replace('>6%<', f'>{online_pct}%<')
# Specific contexts for "6%"
html = html.replace('un 6% de tiempo', f'un {online_pct}% de tiempo')
html = html.replace('solo un 6%', f'solo un {online_pct}%')

# 8. Offline percentage: 3% -> 2%
html = html.replace('>3%<', f'>{offline_pct}%<')

# 9. Session avg duration: "2 minutos" in table
html = html.replace('<td>2 minutos</td>', f'<td>1 minuto</td>')

# 10. Profile updated date
html = html.replace(
    '14 mar 2026 — 03:23 UTC',
    f'24 mar 2026 — {profile_update.hour:02d}:{profile_update.minute:02d} UTC'
)

# 11. Último Registro in OBSERVACIONES
html = html.replace(
    '14 marzo 2026 — 03:33',
    f'24 marzo 2026 — {last_seen.hour:02d}:{last_seen.minute:02d}'
)

# 12. Último Online
html = html.replace(
    '14 marzo 2026 — 01:18:37',
    f'24 marzo 2026 — {last_online.hour:02d}:{last_online.minute:02d}:{last_online.second:02d}'
)

# 13. "Último registro" in DISPOSITIVOS
html = html.replace(
    '14 mar 03:33 UTC',
    f'24 mar {last_seen.hour:02d}:{last_seen.minute:02d} UTC'
)

# 14. Informe generado el
html = html.replace(
    '14 de marzo de 2026',
    '24 de marzo de 2026'
)

# 15. REGISTRO CRONOLÓGICO header
html = html.replace(
    f'{sessions} eventos registrados · actualizado 14 mar 03:24',
    f'{sessions} eventos registrados · actualizado 24 mar {last_seen.hour:02d}:{last_seen.minute:02d}'
)
# Also handle if the old text wasn't replaced yet
html = html.replace(
    '40 eventos registrados · actualizado 14 mar 03:24',
    f'{sessions} eventos registrados · actualizado 24 mar {last_seen.hour:02d}:{last_seen.minute:02d}'
)

# 16. Medición frequency in NOTAS
html = html.replace(
    '~1 medición cada 30.8 segundos en promedio',
    f'~1 medición cada {meas_per_sec} segundos en promedio'
)

# 17. "9 días de observación" → "20 días"
html = html.replace('9 días de observación', f'{duration_days} días de observación')

# 18. CONTACTOS header: "14 contactos · 9 días"
html = html.replace('14 contactos · 9 días', f'14 contactos · {duration_days} días')

# 19. "5 días analizados" in PROBABILIDAD
html = html.replace('5 días analizados', f'{duration_days} días analizados')

# 20. ANEXO date
html = html.replace(
    'ANEXO A — EVIDENCIA VISUAL <span style="float:right;font-weight:normal;font-size:11px;color:#888">14 mar 2026',
    'ANEXO A — EVIDENCIA VISUAL <span style="float:right;font-weight:normal;font-size:11px;color:#888">24 mar 2026'
)

# 21. Capture metadata dates (update to report date)
html = html.replace(
    '<span style="color:#ccc">14 mar 2026</span>',
    '<span style="color:#ccc">24 mar 2026</span>'
)

# ================================================================
# PHASE 2: PATRONES DE ACTIVIDAD — REBUILD SUMMARY CARDS
# ================================================================

# Peak hour card: 1am → 5pm
html = html.replace(
    '<div style="font-size:28px;font-weight:bold;color:#fff">1am</div>\n<div style="color:#888;font-size:12px">Hora Pico</div>',
    '<div style="font-size:28px;font-weight:bold;color:#fff">5pm</div>\n<div style="color:#888;font-size:12px">Hora Pico (UTC)</div>'
)

# Session avg card: 2m → 1m (in PATRONES)
html = html.replace(
    '<div style="font-size:28px;font-weight:bold;color:#fff">2m</div>\n<div style="color:#888;font-size:12px">Sesión Avg</div>',
    '<div style="font-size:28px;font-weight:bold;color:#fff">1m</div>\n<div style="color:#888;font-size:12px">Sesión Avg</div>'
)

# Total online card: 83m → 95m
html = html.replace(
    '<div style="font-size:28px;font-weight:bold;color:#fff">83m</div>\n<div style="color:#888;font-size:12px">Total Online</div>',
    f'<div style="font-size:28px;font-weight:bold;color:#fff">{total_online_min}m</div>\n<div style="color:#888;font-size:12px">Total Online</div>'
)

# ================================================================
# PHASE 3: PATRONES DE ACTIVIDAD — REBUILD SVG CHART
# ================================================================

new_chart_svg = '''<svg viewBox="0 0 800 320" style="width:100%;background:#111;border-radius:8px;border:1px solid #333;padding:10px">

<!-- Eje Y labels -->
<text x="30" y="45" fill="#888" font-size="11" text-anchor="end">3500</text>
<text x="30" y="105" fill="#888" font-size="11" text-anchor="end">2625</text>
<text x="30" y="165" fill="#888" font-size="11" text-anchor="end">1750</text>
<text x="30" y="225" fill="#888" font-size="11" text-anchor="end">875</text>
<text x="30" y="275" fill="#888" font-size="11" text-anchor="end">0</text>

<!-- Grid lines -->
<line x1="40" y1="40" x2="770" y2="40" stroke="#222" stroke-width="1"/>
<line x1="40" y1="100" x2="770" y2="100" stroke="#222" stroke-width="1"/>
<line x1="40" y1="160" x2="770" y2="160" stroke="#222" stroke-width="1"/>
<line x1="40" y1="220" x2="770" y2="220" stroke="#222" stroke-width="1"/>
<line x1="40" y1="275" x2="770" y2="275" stroke="#333" stroke-width="1"/>

'''

# Chart parameters
chart_top = 40
chart_bottom = 275
chart_height = chart_bottom - chart_top  # 235
max_total = 3500  # scale
bar_width = 10
group_width = 30  # 3 bars per group

# Hours to show (all 24)
start_x = 50
slot_width = 30  # pixels per hour slot

for h_data in hourly:
    h = h_data['hour']
    total = h_data['total']
    online = h_data['online']
    pct = h_data['pct']

    x_base = start_x + h * slot_width

    # Determine color: night (20-6) = purple, day (6-20) = green
    if h >= 20 or h < 6:
        online_color = '#7c3aed'
        pct_color = '#3b82f6'
    else:
        online_color = '#10b981'
        pct_color = '#10b981'

    # Bar heights (proportional)
    total_h = round(total / max_total * chart_height)
    online_h = round(online / max_total * chart_height)

    total_y = chart_bottom - total_h
    online_y = chart_bottom - online_h

    # Total bar (gray)
    if total > 0:
        new_chart_svg += f'<rect x="{x_base + 18}" y="{total_y}" width="{bar_width}" fill="#4b5563" height="{total_h}" rx="2"/>\n'

    # Online bar (colored)
    if online > 0:
        new_chart_svg += f'<rect x="{x_base}" y="{online_y}" width="{bar_width}" fill="{online_color}" height="{online_h}" rx="2"/>\n'

    # Peak marker
    if h == peak_hour:
        new_chart_svg += f'<text x="{x_base + 10}" y="{online_y - 5}" fill="#f59e0b" font-size="8" text-anchor="middle">★{pct}%</text>\n'

# X axis labels (every 2 hours + peak)
labels = {0: '0h', 2: '2h', 4: '4h', 6: '6h', 8: '8h', 10: '10h',
          12: '12h', 14: '14h', 16: '16h', 17: '5pm★', 18: '18h', 20: '20h', 22: '22h'}
for h, label in labels.items():
    x = start_x + h * slot_width + 14
    color = '#f59e0b' if h == peak_hour else '#888'
    new_chart_svg += f'<text x="{x}" y="295" fill="{color}" font-size="9" text-anchor="middle">{label}</text>\n'

new_chart_svg += '''
<!-- Leyenda -->
<circle cx="240" cy="315" r="5" fill="#7c3aed"/>
<text x="250" y="319" fill="#888" font-size="10">Noche (20h-6h)</text>
<circle cx="370" cy="315" r="5" fill="#10b981"/>
<text x="380" y="319" fill="#888" font-size="10">Día (6h-20h)</text>
<circle cx="480" cy="315" r="5" fill="#4b5563"/>
<text x="490" y="319" fill="#888" font-size="10">Total mediciones</text>
<circle cx="620" cy="315" r="5" fill="#f59e0b"/>
<text x="630" y="319" fill="#f59e0b" font-size="10">Hora pico: 17h UTC (12h CDMX)</text>

</svg>'''

# Replace old SVG chart
old_chart_start = '<svg viewBox="0 0 800 320" style="width:100%;background:#111;border-radius:8px;border:1px solid #333;padding:10px">'
old_chart_end = '</svg>\n\n</div>\n</div>\n\n\n\n<div class="section">\n<div class="section-header">INDICADORES DE COMPORTAMIENTO'

# Find and replace the chart
chart_start_idx = html.find(old_chart_start)
chart_end_marker = '</svg>\n\n</div>\n</div>\n\n\n\n<div class="section">\n<div class="section-header">INDICADORES DE COMPORTAMIENTO'
chart_end_idx = html.find(chart_end_marker, chart_start_idx)

if chart_start_idx > 0 and chart_end_idx > 0:
    html = html[:chart_start_idx] + new_chart_svg + html[chart_end_idx:]
    print("  ✓ PATRONES SVG chart replaced")
else:
    # Try a more flexible approach
    pattern = r'(<svg viewBox="0 0 800 320".*?</svg>)'
    match = re.search(pattern, html, re.DOTALL)
    if match:
        html = html[:match.start()] + new_chart_svg + html[match.end():]
        print("  ✓ PATRONES SVG chart replaced (regex)")
    else:
        print("  ✗ PATRONES SVG chart NOT found")

# ================================================================
# PHASE 4: INDICADORES DE COMPORTAMIENTO updates
# ================================================================

# "hora pico 1" references and "1am" in indicators
html = html.replace(
    "La hora de \"1ᵃ actividad\"",
    "La hora de \"1ᵃ actividad\""
)  # Keep this

# Update "1am" peak hour reference in behavior text
html = html.replace(
    'de los 34,440 registros de telemetría. La hora de "1ᵃ actividad"',
    'de los 34,440 registros de telemetría. La hora de "1ᵃ actividad"'
)

# Update "nocturno" to reflect new pattern with daytime peak
html = html.replace(
    'predominantemente nocturno (18:00–03:00 UTC) con solo un 7%',
    f'con actividad tanto diurna como nocturna (17:00–01:00 UTC) y un {online_pct}%'
)

# ================================================================
# PHASE 5: ESTADÍSTICAS DE SESIÓN updates
# ================================================================

# Sessions count: 40 → 89
html = html.replace(
    '<div style="font-size:28px;font-weight:bold;color:#7c3aed">40</div>\n<div style="color:#888;font-size:11px">Sesiones</div>',
    f'<div style="font-size:28px;font-weight:bold;color:#7c3aed">{sessions}</div>\n<div style="color:#888;font-size:11px">Sesiones</div>'
)

# Session avg: 2m → 1m
html = html.replace(
    '<div style="font-size:28px;font-weight:bold;color:#3b82f6">2m</div>\n<div style="color:#888;font-size:11px">Duración avg</div>',
    '<div style="font-size:28px;font-weight:bold;color:#3b82f6">1m</div>\n<div style="color:#888;font-size:11px">Duración avg</div>'
)

# Sessions/day: 10 → calculated
html = html.replace(
    '<div style="font-size:28px;font-weight:bold;color:#10b981">10</div>\n<div style="color:#888;font-size:11px">Sesiones/día</div>',
    f'<div style="font-size:28px;font-weight:bold;color:#10b981">{round(sessions_per_day)}</div>\n<div style="color:#888;font-size:11px">Sesiones/día</div>'
)

# Total online: 83m
html = html.replace(
    '<td style="color:#10b981">83m</td>',
    f'<td style="color:#10b981">{total_online_min}m</td>'
)

# Daily avg: 21m → 5m
html = html.replace(
    '<tr><td class="meta">Diario avg</td><td>21m</td></tr>',
    f'<tr><td class="meta">Diario avg</td><td>{daily_online}m</td></tr>'
)

# Intensity: 18% → adjusted
new_intensity = round(online_pct / 6 * 18)  # proportional
html = html.replace(
    'INTENSIDAD DE USO <span style="float:right;color:#10b981">18%</span>',
    f'INTENSIDAD DE USO <span style="float:right;color:#10b981">{new_intensity}%</span>'
)
html = html.replace(
    f'<div style="width:18%;height:100%',
    f'<div style="width:{new_intensity}%;height:100%'
)

# ================================================================
# PHASE 6: PROBABILIDAD DE DISPONIBILIDAD — REBUILD SVG
# ================================================================

prob_svg = '''<svg viewBox="0 0 800 200" style="width:100%;background:#0a0a0a;border-radius:8px;border:1px solid #222">

<!-- Grid lines -->
<line x1="50" y1="30" x2="750" y2="30" stroke="#1a1a1a" stroke-width="1"/>
<line x1="50" y1="150" x2="750" y2="150" stroke="#333" stroke-width="1"/>

'''

# Build bars for each hour with online > 0%
bar_chart_height = 120  # from y=30 to y=150
bar_chart_bottom = 150

hours_with_data = [(h['hour'], h['pct']) for h in hourly if h['pct'] > 0]

# Position bars evenly
if hours_with_data:
    total_bars = len(hours_with_data)
    spacing = 700 / (total_bars + 1)

    for i, (h, pct) in enumerate(hours_with_data):
        x = 50 + spacing * (i + 1) - 14
        bar_h = round(pct / 50 * bar_chart_height)  # 50% = full height
        bar_y = bar_chart_bottom - bar_h

        # Color based on percentage
        if pct >= 25:
            color = '#10b981'  # Alta
        elif pct >= 10:
            color = '#f59e0b'  # Media
        elif pct >= 5:
            color = '#7c3aed'  # Baja
        else:
            color = '#4b5563'  # Muy baja

        # Peak marker
        if h == peak_hour:
            color = '#10b981'
            prob_svg += f'<text x="{x + 14}" y="{bar_y - 8}" fill="#f59e0b" font-size="9" text-anchor="middle" font-weight="bold">★ PICO</text>\n'

        prob_svg += f'<!-- {h}h: {pct}% -->\n'
        prob_svg += f'<rect x="{x}" y="{bar_y}" width="28" fill="{color}" height="{bar_h}" rx="2"/>\n'
        prob_svg += f'<text x="{x + 14}" y="170" fill="#666" font-size="10" text-anchor="middle">{h}h</text>\n'
        prob_svg += f'<text x="{x + 14}" y="{bar_y - 2}" fill="{color}" font-size="8" text-anchor="middle">{pct}%</text>\n'

prob_svg += '''
<!-- Legend -->
<rect x="220" y="185" width="10" height="10" fill="#10b981" rx="2"/>
<text x="235" y="194" fill="#888" font-size="10">Alta (&gt;25%)</text>
<rect x="330" y="185" width="10" height="10" fill="#f59e0b" rx="2"/>
<text x="345" y="194" fill="#888" font-size="10">Media (10-25%)</text>
<rect x="460" y="185" width="10" height="10" fill="#7c3aed" rx="2"/>
<text x="475" y="194" fill="#888" font-size="10">Baja (5-10%)</text>
<rect x="580" y="185" width="10" height="10" fill="#4b5563" rx="2"/>
<text x="595" y="194" fill="#888" font-size="10">Muy baja (&lt;5%)</text>

</svg>'''

# Replace old probability SVG
old_prob_start = '<svg viewBox="0 0 800 200" style="width:100%;background:#0a0a0a;border-radius:8px;border:1px solid #222">'
prob_start_idx = html.find(old_prob_start)
if prob_start_idx > 0:
    prob_end_idx = html.find('</svg>', prob_start_idx) + len('</svg>')
    html = html[:prob_start_idx] + prob_svg + html[prob_end_idx:]
    print("  ✓ PROBABILIDAD SVG chart replaced")
else:
    print("  ✗ PROBABILIDAD SVG not found")

# Update "HORAS INACTIVAS" list
inactive_hours = [h['hour'] for h in hourly if h['pct'] == 0]
inactive_str = ', '.join(f'{h}h' for h in inactive_hours)
old_inactive = '2h, 4h, 5h, 7h, 8h, 9h, 10h, 11h, 12h, 13h, 14h, 15h, 16h, 17h, 22h'
html = html.replace(old_inactive, inactive_str)

# ================================================================
# PHASE 7: ACTIVIDAD DIARIA - update note
# ================================================================
html = html.replace(
    'Con solo un 6% de tiempo online, los datos de actividad son esporádicos',
    f'Con solo un {online_pct}% de tiempo online, los datos de actividad son esporádicos'
)

# ================================================================
# PHASE 8: HEATMAP updates
# ================================================================

# Update heatmap hour annotation
html = html.replace(
    '▲ Hora pico consistente: 14:00 UTC (09:00 CDMX)',
    '▲ Hora pico consistente: 17:00 UTC (12:00 CDMX)'
)

# ================================================================
# PHASE 9: REGISTRO CRONOLÓGICO — ADD NEW ACTIVITY
# ================================================================

# Build new timeline entries from activityHistory
activity = data['activityHistory']
state_map = {
    'Online': ('CONECTADO', '#10b981'),
    'Standby': ('EN ESPERA', '#f59e0b'),
    'Offline': ('DESCONECTADO', '#ef4444'),
    'Unknown': ('DESCONOCIDO', '#888'),
    'Calibrating...': ('CALIBRANDO', '#7c3aed'),
}

new_timeline_entries = []
for entry in reversed(activity):  # Most recent first
    ts = datetime.fromisoformat(entry['timestamp'].replace('Z', '+00:00'))
    state = entry['state']
    rtt = entry['rtt']
    label, color = state_map.get(state, (state.upper(), '#888'))

    time_str = f'{ts.hour:02d}:{ts.minute:02d}'
    date_str = f'{ts.day} mar'

    line = f'<div><b>{time_str}</b> <span style="color:#888;font-size:11px">({date_str})</span> — <span style="color:{color}">{label}</span>'
    if rtt > 0:
        line += f' — RTT: {rtt:,}ms'
        if rtt > 3000:
            line += f' <span style="color:#ef4444;font-size:10px">(pico)</span>'
    line += '</div>'
    new_timeline_entries.append(line)

new_timeline_html = '\n'.join(new_timeline_entries)

# Insert new entries before old ones
old_timeline_marker = '<div class="timeline">'
timeline_idx = html.find(old_timeline_marker)
if timeline_idx > 0:
    insert_pos = timeline_idx + len(old_timeline_marker) + 1

    separator = '\n<div style="border-left:3px solid #333;padding-left:14px;margin:8px 0;color:#666;font-size:11px">— 24 marzo 2026 — sesión activa 19:28–19:35 UTC —</div>\n\n'

    html = html[:insert_pos] + '\n' + new_timeline_html + '\n' + separator + html[insert_pos:]
    print("  ✓ Timeline entries added")
else:
    print("  ✗ Timeline marker not found")

# Update the "500 mediciones recientes" line
html = html.replace(
    '500 mediciones recientes · 34,440 totales · Device 2: OFFLINE (RTT: 10,025ms)',
    f'500 mediciones recientes · 34,440 totales · Dispositivo 2: OFFLINE (RTT: 10,021ms)'
)
# Also fix if still with old number
html = html.replace(
    '500 mediciones recientes · 26,460 totales · Device 2: OFFLINE (RTT: 10,025ms)',
    f'500 mediciones recientes · 34,440 totales · Dispositivo 2: OFFLINE (RTT: 10,021ms)'
)

# ================================================================
# PHASE 10: FIX "Device 2" → "Dispositivo 2"
# ================================================================
html = html.replace('Device 2', 'Dispositivo 2')
html = html.replace('DEVICE 2', 'DISPOSITIVO 2')

# ================================================================
# PHASE 11: FIX "Data Points" → "Registros"
# ================================================================
html = html.replace('>Data Points<', '>Registros<')

# ================================================================
# PHASE 12: SEMANA VS FIN DE SEMANA update
# ================================================================
html = html.replace(
    '<div style="font-size:20px;font-weight:bold;color:#fff">27m</div>\n<div style="color:#888;font-size:11px">Lun-Vie avg</div>',
    f'<div style="font-size:20px;font-weight:bold;color:#fff">{daily_online}m</div>\n<div style="color:#888;font-size:11px">Lun-Vie avg</div>'
)

# ================================================================
# PHASE 13: DISTRIBUCIÓN HORARIA in heatmap section
# ================================================================

# Old distribution was based on old peak at 14:00
# New: hour 17 = 5pm UTC, peak hours are 17-21 + 0-1
# Recalculate time blocks
total_online = sum(h['online'] for h in hourly)
if total_online > 0:
    madrugada = sum(h['online'] for h in hourly if 0 <= h['hour'] < 6)
    manana = sum(h['online'] for h in hourly if 6 <= h['hour'] < 12)
    tarde = sum(h['online'] for h in hourly if 12 <= h['hour'] < 18)
    noche = sum(h['online'] for h in hourly if 18 <= h['hour'] < 24)

    madr_pct = round(madrugada / total_online * 100)
    man_pct = round(manana / total_online * 100)
    tard_pct = round(tarde / total_online * 100)
    noch_pct = round(noche / total_online * 100)

    print(f"\n  Dist horaria: madrugada={madr_pct}%, mañana={man_pct}%, tarde={tard_pct}%, noche={noch_pct}%")

    # Replace old percentages
    # Madrugada
    html = html.replace(
        '00:00—06:00 (madrugada)</span><span style="color:#7c3aed;font-weight:bold">3%',
        f'00:00—06:00 (madrugada)</span><span style="color:#7c3aed;font-weight:bold">{madr_pct}%'
    )
    # Mañana
    html = html.replace(
        '06:00—12:00 (mañana)</span><span style="color:#888;font-weight:bold">0%',
        f'06:00—12:00 (mañana)</span><span style="color:#888;font-weight:bold">{man_pct}%'
    )
    # Tarde
    html = html.replace(
        '12:00—18:00 (tarde)</span><span style="color:#10b981;font-weight:bold">95%',
        f'12:00—18:00 (tarde)</span><span style="color:#10b981;font-weight:bold">{tard_pct}%'
    )
    # Noche
    html = html.replace(
        '18:00—00:00 (noche)</span><span style="color:#888;font-weight:bold">2%',
        f'18:00—00:00 (noche)</span><span style="color:#f59e0b;font-weight:bold">{noch_pct}%'
    )

# ================================================================
# PHASE 14: FIX GRAMMAR ERRORS ("la datos" → "los datos")
# ================================================================
html = html.replace('La datos recopilados', 'Los datos recopilados')
html = html.replace('la datos recopilados', 'los datos recopilados')
html = html.replace('La datos del dispositivo', 'Los datos del dispositivo')
html = html.replace('la datos del dispositivo', 'los datos del dispositivo')
html = html.replace('los datos es transferida', 'los datos son transferidos')
html = html.replace('La datos binarios', 'Los datos binarios')
html = html.replace('la datos binarios', 'los datos binarios')
html = html.replace('del dispositivo del dispositivo', 'del dispositivo')
html = html.replace('Toda la datos recopilados', 'Todos los datos recopilados')
html = html.replace('La datos reconstruidos debe ser', 'Los datos reconstruidos deben ser')
html = html.replace('la datos reconstruidos debe ser', 'los datos reconstruidos deben ser')
html = html.replace('la datos reconstruida', 'los datos reconstruidos')
html = html.replace('La datos reconstruida', 'Los datos reconstruidos')

# Fix "La datos" globally (remaining occurrences)
html = re.sub(r'\bLa datos\b', 'Los datos', html)
html = re.sub(r'\bla datos\b', 'los datos', html)

# ================================================================
# PHASE 15: "2,000 packets" → "327,954 paquetes" consistency
# ================================================================
html = html.replace('2,000 packets', '327,954 paquetes')
html = html.replace('2,000 paquetes', '327,954 paquetes')

# ================================================================
# PHASE 16: Heatmap hallazgos update
# ================================================================
html = html.replace(
    '<span style="color:#10b981;font-weight:bold">hora 14 UTC</span> (09:00 hora CDMX)',
    '<span style="color:#10b981;font-weight:bold">hora 17 UTC</span> (12:00 hora CDMX)'
)
html = html.replace(
    '<span style="color:#f59e0b">5 de 7 días</span> con actividad muestran el mismo patrón horario',
    '<span style="color:#f59e0b">Mayoría de días activos</span> muestran un patrón horario concentrado'
)

# ================================================================
# PHASE 17: Fix "10,025ms" RTT for device 2 → use actual value
# ================================================================
html = html.replace('10,025ms', '10,021ms')
html = html.replace('10,025', '10,021')

# ================================================================
# PHASE 18: Update "1ᵃ actividad" reference to 1am
# ================================================================
html = html.replace(
    "de \"1ᵃ actividad\" y \"última actividad\"",
    "de \"1ᵃ actividad\" y \"última actividad\""
)

# ================================================================
# PHASE 19: NIVEL DE ATRIBUCIÓN — update data references
# ================================================================
html = html.replace(
    'Telemetría WhatsApp (34,440 registros)',
    'Telemetría WhatsApp (34,440 registros)'
)

# ================================================================
# WRITE OUTPUT
# ================================================================
with open('INFORME--@RanmsesRuiz-v3.html', 'w', encoding='utf-8') as f:
    f.write(html)

# Summary
changes = sum(1 for a, b in zip(original, html) if a != b)
print(f"\n=== RESULTADO ===")
print(f"  Archivo actualizado: INFORME--@RanmsesRuiz-v3.html")
print(f"  Caracteres totales: {len(html):,}")
print(f"  Diferencias de caracteres: {changes:,}")

# Verify key values
for val, label in [
    ('34,440', 'total measurements'),
    (f'{duration_days}d {duration_hours}h', 'duration'),
    ('1,537', 'RTT avg'),
    ('1,120', 'threshold'),
    ('04-24 mar', 'date range'),
    (f'{sessions}', 'sessions'),
    ('5pm', 'peak hour'),
    (f'{total_online_min}m', 'total online'),
    ('24 de marzo de 2026', 'generation date'),
]:
    count = html.count(val)
    print(f"  {label}: '{val}' appears {count}x")

# Check for residual old values
for val, label in [
    ('26,460', 'old measurements'),
    ('9d 10h', 'old duration'),
    ('1,547', 'old RTT'),
    ('1,147', 'old threshold'),
    ('04-14 mar', 'old date range'),
    ('40 sesiones', 'old sessions'),
    ('1am', 'old peak'),
    ('Device 2', 'old device name'),
    ('Data Points', 'old english'),
]:
    count = html.count(val)
    if count > 0:
        print(f"  ⚠ RESIDUAL: '{val}' still appears {count}x")

# Check div balance
open_divs = html.count('<div')
close_divs = html.count('</div>')
print(f"\n  Div balance: {open_divs} open, {close_divs} close = {open_divs - close_divs}")
