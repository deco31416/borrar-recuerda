import json

with open(r'estaditicas-ranmsesruiz\reporte-v4.json', 'r', encoding='utf-8') as f:
    d = json.load(f)

print('=== TOP KEYS ===')
for k in d.keys():
    print(f'  {k}: {type(d[k]).__name__}')

print('\n=== STATS ===')
for k, v in d['stats'].items():
    print(f'  {k}: {v}')

p = d['patterns']
print(f'\n=== PATTERNS ===')
print(f'  peakHour: {p["peakHour"]}')
print(f'  avgSessionLength: {p["avgSessionLength"]}s')
print(f'  totalOnlineMinutes: {p["totalOnlineMinutes"]}')
print(f'  hourly entries: {len(p["hourly"])}')
for h in p['hourly']:
    if h['online'] > 0:
        print(f'    hora {h["hour"]}: total={h["total"]}, online={h["online"]}, pct={h["pct"]}%')

print(f'\n=== ACTIVITY HISTORY ===')
print(f'  entries: {len(d["activityHistory"])}')
if d['activityHistory']:
    print(f'  first: {d["activityHistory"][0]}')
    print(f'  last: {d["activityHistory"][-1]}')

print(f'\n=== RECENT MEASUREMENTS ===')
print(f'  entries: {len(d["recentMeasurements"])}')

if 'sessions' in d:
    print(f'\n=== SESSIONS ===')
    print(f'  entries: {len(d["sessions"])}')
    for s in d['sessions'][:5]:
        print(f'  {s}')

if 'dailyActivity' in d:
    print(f'\n=== DAILY ACTIVITY ===')
    for day in d['dailyActivity']:
        print(f'  {day}')

# First and last seen calc
from datetime import datetime
first = datetime.fromisoformat(d['stats']['firstSeen'].replace('Z', '+00:00'))
last = datetime.fromisoformat(d['stats']['lastSeen'].replace('Z', '+00:00'))
delta = last - first
print(f'\n=== DURATION ===')
print(f'  First seen: {first}')
print(f'  Last seen: {last}')
print(f'  Duration: {delta.days}d {delta.seconds // 3600}h')

for k in d.keys():
    if k not in ['generatedAt', 'contact', 'stats', 'patterns', 'activityHistory', 'recentMeasurements', 'sessions', 'dailyActivity']:
        val = d[k]
        if isinstance(val, list):
            print(f'\n=== {k.upper()} === ({len(val)} entries)')
            if val:
                print(f'  sample: {val[0]}')
        elif isinstance(val, dict):
            print(f'\n=== {k.upper()} ===')
            for sk, sv in val.items():
                if isinstance(sv, (str, int, float, bool)):
                    print(f'  {sk}: {sv}')
                else:
                    print(f'  {sk}: {type(sv).__name__}')
        else:
            print(f'  {k}: {val}')
