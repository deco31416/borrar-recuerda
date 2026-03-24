import re

h = open('INFORME--@RanmsesRuiz-v3.html', 'r', encoding='utf-8').read()
lines = h.split('\n')

patterns = [
    ('26,460', r'26[,.]460'),
    ('1,547', r'1[,.]547'),
    ('1,147', r'1[,.]147'),
    ('9d 10h', r'9d\s*10h'),
    ('40 sesion', r'40 sesion'),
    ('83m', r'83m|83 min'),
    ('04-14 mar', r'04.14\s*mar'),
    ('14 mar', r'14 mar|14 de marzo'),
    ('03:24', r'03:24'),
    ('2m avg', r'2m\b'),
    ('hora pico 1', r'hora\s+pico.*1|1am|01:00'),
    ('peakHour', r'hora\s+1\b|1:00.*pico|pico.*1:00'),
]

for label, pat in patterns:
    found = False
    for i, line in enumerate(lines, 1):
        if re.search(pat, line, re.IGNORECASE):
            snippet = line.strip()[:140]
            print(f'L{i:4d}: [{label}] {snippet}')
            found = True
    if not found:
        print(f'      [{label}] -- NOT FOUND --')
    print()
