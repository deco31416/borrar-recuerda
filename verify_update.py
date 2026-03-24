h = open('INFORME--@RanmsesRuiz-v3.html','r',encoding='utf-8').read()

residuals = {
    '26,460': h.count('26,460'),
    '26.460': h.count('26.460'),
    '9d 10h': h.count('9d 10h'),
    '1,547': h.count('1,547'),
    '1,147': h.count('1,147'),
    '04-14 mar': h.count('04-14 mar'),
    '40 sesiones': h.count('40 sesiones'),
    'Device 2': h.count('Device 2'),
    'Data Points': h.count('Data Points'),
    'La datos': h.count('La datos'),
    'la datos': h.count('la datos'),
    '14 de marzo': h.count('14 de marzo'),
    '2,000 packets': h.count('2,000 packets'),
}
print('=== RESIDUOS ===')
for k, v in residuals.items():
    status = 'OK (0)' if v == 0 else f'RESIDUAL ({v})'
    print(f'  {k}: {status}')

print()
print('=== NUEVOS VALORES ===')
news = {
    '34,440': h.count('34,440'),
    '19d 20h': h.count('19d 20h'),
    '1,537': h.count('1,537'),
    '1,120': h.count('1,120'),
    '04-24 mar': h.count('04-24 mar'),
    '89 sesiones': h.count('89 sesiones'),
    '89 eventos': h.count('89 eventos'),
    '5pm': h.count('5pm'),
    '95m': h.count('95m'),
    '24 de marzo': h.count('24 de marzo'),
    'Dispositivo 2': h.count('Dispositivo 2'),
    '17:00 UTC': h.count('17:00 UTC'),
    '7%': h.count('>7%<'),
    '2%_offline': h.count('>2%<'),
}
for k, v in news.items():
    print(f'  {k}: {v}x')

# Check div balance
print(f'\nDiv balance: {h.count("<div")} open, {h.count("</div>")} close = {h.count("<div") - h.count("</div>")}')
print(f'Total chars: {len(h):,}')
print(f'Total lines: {h.count(chr(10)) + 1}')
