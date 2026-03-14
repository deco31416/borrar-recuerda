with open(r'C:\Users\HP\Desktop\expediente-ruiz\INFORME--@RanmsesRuiz - copia.html', 'r', encoding='utf-8') as f:
    html = f.read()

import re

opens = html.count('<div')
closes = html.count('</div>')
print(f'<div> opens:  {opens}')
print(f'</div> closes: {closes}')
print(f'Balance: {opens - closes} (should be 0)')

sections = re.findall(r'class="section-header"[^>]*>(.*?)</div>', html)
print(f'\nTotal sections: {len(sections)}')
for i, s in enumerate(sections, 1):
    clean = re.sub(r'<[^>]+>', '', s).strip()[:65]
    print(f'  {i:2d}. {clean}')

section_opens = html.count('<div class="section">')
print(f'\n<div class="section"> count: {section_opens}')
print(f'Expected: {len(sections)} (should match)')
