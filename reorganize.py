import re

FILE = r'C:\Users\HP\Desktop\expediente-ruiz\INFORME--@RanmsesRuiz - copia.html'

with open(FILE, 'r', encoding='utf-8') as f:
    content = f.read()

def find_section_block(html, header_text):
    """Find a complete <div class="section"> block by header text."""
    header_idx = html.find(header_text)
    if header_idx == -1:
        raise ValueError(f'Header not found: {header_text}')
    
    search_area = html[:header_idx]
    section_marker = '<div class="section">'
    start_idx = search_area.rfind(section_marker)
    if start_idx == -1:
        raise ValueError(f'Section start not found for: {header_text}')
    
    depth = 0
    i = start_idx
    while i < len(html):
        if html[i:i+4] == '<div':
            depth += 1
            i += 4
        elif html[i:i+6] == '</div>':
            depth -= 1
            i += 6
            if depth == 0:
                end_idx = i
                break
        else:
            i += 1
    else:
        raise ValueError(f'Could not find end of section: {header_text}')
    
    block = html[start_idx:end_idx]
    return start_idx, end_idx, block


# Step 1: Extract all blocks we need to move
perfil_contacto_start, perfil_contacto_end, perfil_contacto_block = find_section_block(content, 'PERFIL DEL CONTACTO')
notas_start, notas_end, notas_block = find_section_block(content, 'NOTAS DE CUMPLIMIENTO Y DEFINICIONES')
opsec_start, opsec_end, opsec_block = find_section_block(content, 'PUNTAJE DE PRIVACIDAD (OPSEC)')
netmon1_start, netmon1_end, netmon1_block = find_section_block(content, 'NETWORK MONITOR — CONTACTOS EXTERNOS DETECTADOS')
netmon2_start, netmon2_end, netmon2_block = find_section_block(content, 'NETWORK MONITOR — STATISTICS')

print(f"PERFIL DEL CONTACTO: {perfil_contacto_start}-{perfil_contacto_end} ({perfil_contacto_end - perfil_contacto_start} chars)")
print(f"NOTAS CUMPLIMIENTO: {notas_start}-{notas_end} ({notas_end - notas_start} chars)")
print(f"OPSEC: {opsec_start}-{opsec_end} ({opsec_end - opsec_start} chars)")
print(f"NETMON1: {netmon1_start}-{netmon1_end} ({netmon1_end - netmon1_start} chars)")
print(f"NETMON2: {netmon2_start}-{netmon2_end} ({netmon2_end - netmon2_start} chars)")

# Step 2: Find insertion points (by their anchor sections)
# a) PERFIL DEL CONTACTO → after PERFIL DEL TITULAR
perfil_titular_start, perfil_titular_end, _ = find_section_block(content, 'PERFIL DEL TITULAR')
print(f"\nInsert PERFIL CONTACTO after PERFIL TITULAR end: {perfil_titular_end}")

# b) OPSEC → after TABLA DE EVIDENCIA (which is the last sub-section within NIVEL DE ATRIBUCIÓN area)
tabla_ev_start, tabla_ev_end, _ = find_section_block(content, 'TABLA DE EVIDENCIA')
print(f"Insert OPSEC after TABLA DE EVIDENCIA end: {tabla_ev_end}")

# c) NETWORK MONITOR (2 sections) → after ESTADÍSTICAS DE COMUNICACIÓN
est_com_start, est_com_end, _ = find_section_block(content, 'ESTADÍSTICAS DE COMUNICACIÓN — RESUMEN')
print(f"Insert NETWORK MONITOR after ESTADÍSTICAS COMUNICACIÓN end: {est_com_end}")

# d) NOTAS DE CUMPLIMIENTO → before CONCLUSIÓN
conclusion_marker = '<!-- CONCLUSIÓN Y ESTADO OPERATIVO'
conclusion_idx = content.find(conclusion_marker)
# Actually, find the <div class="section"> for CONCLUSIÓN
concl_start, concl_end, _ = find_section_block(content, 'CONCLUSIÓN Y ESTADO OPERATIVO')
print(f"Insert NOTAS CUMPLIMIENTO before CONCLUSIÓN: {concl_start}")


# Step 3: Now do the actual reorganization
# Strategy: work from end of file to beginning (so indices don't shift)
# Operations sorted by position (descending):
# 1. Remove NETWORK MONITOR 2 sections (highest position ~3267-3443)
# 2. Remove OPSEC (~2707-2870)  
# 3. Remove PERFIL DEL CONTACTO (~2686-2706)
# 4. Remove NOTAS DE CUMPLIMIENTO (~2659-2685)
# Then insert at target positions (also from end to beginning)

# But we need to be smarter. Let me collect all operations:
# Remove blocks (track the whitespace between sections too)

def get_block_with_surrounding_whitespace(html, start, end):
    """Get the block plus any trailing whitespace/newlines before next content."""
    # Include trailing whitespace up to the next non-whitespace
    trailing_end = end
    while trailing_end < len(html) and html[trailing_end] in '\n\r\t ':
        trailing_end += 1
    # Include leading whitespace
    leading_start = start
    while leading_start > 0 and html[leading_start-1] in '\n\r\t ':
        leading_start -= 1
    return leading_start, trailing_end

# Get blocks with whitespace for clean removal
pc_ws_start, pc_ws_end = get_block_with_surrounding_whitespace(content, perfil_contacto_start, perfil_contacto_end)
notas_ws_start, notas_ws_end = get_block_with_surrounding_whitespace(content, notas_start, notas_end)
opsec_ws_start, opsec_ws_end = get_block_with_surrounding_whitespace(content, opsec_start, opsec_end)
netmon1_ws_start, netmon1_ws_end = get_block_with_surrounding_whitespace(content, netmon1_start, netmon1_end)
netmon2_ws_start, netmon2_ws_end = get_block_with_surrounding_whitespace(content, netmon2_start, netmon2_end)

# Build sections to remove (as ranges) and sections to insert (with targets)
# We'll process all removals first from end to start, then insertions from end to start

# First, let's do this step by step, building the new content
# Remove all 5 blocks from their current positions
removals = sorted([
    (pc_ws_start, pc_ws_end),
    (notas_ws_start, notas_ws_end),
    (opsec_ws_start, opsec_ws_end),
    (netmon1_ws_start, netmon1_ws_end),
    (netmon2_ws_start, netmon2_ws_end),
], reverse=True)

new_content = content
for r_start, r_end in removals:
    new_content = new_content[:r_start] + '\n\n' + new_content[r_end:]

# Now find new insertion points in the cleaned content
# a) PERFIL DEL CONTACTO after PERFIL DEL TITULAR
_, pt_end, _ = find_section_block(new_content, 'PERFIL DEL TITULAR')
insert_a = pt_end

# b) OPSEC after TABLA DE EVIDENCIA  
_, te_end, _ = find_section_block(new_content, 'TABLA DE EVIDENCIA')
insert_b = te_end

# c) NETWORK MONITOR after ESTADÍSTICAS DE COMUNICACIÓN
_, ec_end, _ = find_section_block(new_content, 'ESTADÍSTICAS DE COMUNICACIÓN — RESUMEN')
insert_c = ec_end

# d) NOTAS DE CUMPLIMIENTO before CONCLUSIÓN
concl_s, _, _ = find_section_block(new_content, 'CONCLUSIÓN Y ESTADO OPERATIVO')
# Go back to find the comment block before it
comment_start = new_content.rfind('<!-- ', 0, concl_s)
if comment_start > 0 and 'CONCLUSIÓN' in new_content[comment_start:concl_s]:
    insert_d = comment_start
else:
    insert_d = concl_s

# Sort insertions by position descending so they don't shift each other
insertions = sorted([
    (insert_a, '\n\n\n' + perfil_contacto_block + '\n'),
    (insert_b, '\n\n\n' + opsec_block + '\n'),
    (insert_c, '\n\n\n' + netmon1_block + '\n\n\n' + netmon2_block + '\n'),
    (insert_d, notas_block + '\n\n\n\n'),
], key=lambda x: x[0], reverse=True)

for pos, block_text in insertions:
    new_content = new_content[:pos] + block_text + new_content[pos:]

# Verify the new order
print("\n=== NEW SECTION ORDER ===")
import re
for m in re.finditer(r'class="section-header"[^>]*>(.*?)</div>', new_content):
    header_text = re.sub(r'<[^>]+>', '', m.group(1)).strip()[:60]
    line_num = new_content[:m.start()].count('\n') + 1
    print(f"  L{line_num:4d}: {header_text}")

# Write the result
with open(FILE, 'w', encoding='utf-8') as f:
    f.write(new_content)

print("\n✅ File reorganized successfully!")
print(f"Original size: {len(content)} chars")
print(f"New size: {len(new_content)} chars")
