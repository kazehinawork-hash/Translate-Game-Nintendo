"""
Bo tao glyph Tieng Viet tu chinh font goc (Native Synthesis) cho It Takes Two.
Triet tieu 100% hien tuong lech font (khac kieu dang/do dam giua chu thuong va chu co dau).
Ap dung cho toan bo cac bo font UI cua ITT:
- MarkW1G (Heavy, Medium, MediumItalic)
- Poppins (Medium, ExtraBold, Italic)
"""
import sys, os, unicodedata
sys.stdout.reconfigure(encoding='utf-8')
from fontTools.ttLib import TTFont
from fontTools.ttLib.tables._g_l_y_f import Glyph, GlyphComponent, GlyphCoordinates, ttProgram

VI_CHARS = (
    'àáảãạăằắẳẵặâầấẩẫậèéẻẽẹêềếểễệìíỉĩịòóỏõọôồốổỗộơờớởỡợùúủũụưừứửữựỳýỷỹỵđ'
    'ÀÁẢÃẠĂẰẮẲẴẶÂẦẤẨẪẬÈÉẺẼẸÊỀẾỂỄỆÌÍỈĨỊÒÓỎÕỌÔỒỐỔỖỘƠỜỚỞỠỢÙÚỦŨỤƯỪỨỬỮỰỲÝỶỸỴĐ'
)

def make_composite(glyf, base_name, mark_list):
    g = Glyph()
    g.numberOfContours = -1
    components = []
    
    # base glyph
    comp_base = GlyphComponent()
    comp_base.glyphName = base_name
    comp_base.x = 0
    comp_base.y = 0
    comp_base.flags = 0x0204 # ARGS_ARE_XY_VALUES | ROUND_XY_TO_GRID
    components.append(comp_base)
    
    # mark components
    for mark_name, ox, oy in mark_list:
        comp_m = GlyphComponent()
        comp_m.glyphName = mark_name
        comp_m.x = int(round(ox))
        comp_m.y = int(round(oy))
        comp_m.flags = 0x0204
        components.append(comp_m)
        
    g.components = components
    g.recalcBounds(glyf)
    return g

def patch_mark_font(font_path, out_path):
    print(f"=== Patching MarkW1G native: {font_path} ===")
    font = TTFont(font_path)
    glyf = font['glyf']
    hmtx = font['hmtx']
    cmap = font.getBestCmap()
    upem = font['head'].unitsPerEm # 2000
    
    # 1. Tao hookabovecomb tu contour 0 cua dau cham hoi 'question'
    g_q = glyf['question']
    coords, endPts, flags = g_q.getCoordinates(glyf)
    c0_coords = coords[:endPts[0]+1]
    c0_flags = flags[:endPts[0]+1]
    min_x, max_x = min(x for x,y in c0_coords), max(x for x,y in c0_coords)
    min_y, max_y = min(y for x,y in c0_coords), max(y for x,y in c0_coords)
    cx = (min_x + max_x) / 2.0
    
    # Hook thuong (dat tam tai x=0, y nam ngay tren x-height)
    hook_scale = 0.35
    hook_coords = [
        (int(round((x - cx) * hook_scale)), int(round((y - min_y) * hook_scale + 1070)))
        for x, y in c0_coords
    ]
    hg = Glyph()
    hg.numberOfContours = 1
    hg.endPtsOfContours = [len(hook_coords) - 1]
    hg.flags = c0_flags
    hg.coordinates = GlyphCoordinates(hook_coords)
    hg.program = ttProgram.Program()
    hg.recalcBounds(glyf)
    glyf['hookabovecomb'] = hg
    hmtx['hookabovecomb'] = (0, hg.xMin)
    
    # Hook hoa (case)
    hook_case_coords = [
        (int(round((x - cx) * hook_scale)), int(round((y - min_y) * hook_scale + 1460)))
        for x, y in c0_coords
    ]
    hgc = Glyph()
    hgc.numberOfContours = 1
    hgc.endPtsOfContours = [len(hook_case_coords) - 1]
    hgc.flags = c0_flags
    hgc.coordinates = GlyphCoordinates(hook_case_coords)
    hgc.program = ttProgram.Program()
    hgc.recalcBounds(glyf)
    glyf['hookabovecomb.case'] = hgc
    hmtx['hookabovecomb.case'] = (0, hgc.xMin)
    
    # 2. Tao horncomb (dau moc cho o, u) lay tu Nunito va phong to len 2000 upem
    nunito = TTFont('tools/Nunito-Bold.ttf')
    n_horn = nunito['glyf']['uni031B']
    n_coords, n_endPts, n_flags = n_horn.getCoordinates(nunito['glyf'])
    horn_coords = [
        (int(round(x * 1.6)), int(round((y - 418) * 1.6 + 940)))
        for x, y in n_coords
    ]
    horng = Glyph()
    horng.numberOfContours = len(n_endPts)
    horng.endPtsOfContours = list(n_endPts)
    horng.flags = n_flags
    horng.coordinates = GlyphCoordinates(horn_coords)
    horng.program = ttProgram.Program()
    horng.recalcBounds(glyf)
    glyf['horncomb'] = horng
    hmtx['horncomb'] = (0, horng.xMin)
    
    horn_case_coords = [
        (int(round(x * 1.8)), int(round((y - 418) * 1.8 + 1340)))
        for x, y in n_coords
    ]
    horngc = Glyph()
    horngc.numberOfContours = len(n_endPts)
    horngc.endPtsOfContours = list(n_endPts)
    horngc.flags = n_flags
    horngc.coordinates = GlyphCoordinates(horn_case_coords)
    horngc.program = ttProgram.Program()
    horngc.recalcBounds(glyf)
    glyf['horncomb.case'] = horngc
    hmtx['horncomb.case'] = (0, horngc.xMin)
    
    # Dinh vi toa do trung tam cua cac nguyen am
    # Trong MarkW1G, cac mark comb co tam X = -591 (thuong) va -807 (hoa)
    mark_cx = -591.0
    case_mark_cx = -807.5
    
    def get_vowel_cx(v_name):
        g = glyf[v_name]
        return (g.xMin + g.xMax) / 2.0
    
    # Map nguyen am co ban
    v_map = {
        'a': ('a', False), 'e': ('e', False), 'i': ('dotlessi', False), 'o': ('o', False), 'u': ('u', False), 'y': ('y', False),
        'A': ('A', True),  'E': ('E', True),  'I': ('I', True),  'O': ('O', True),  'U': ('U', True),  'Y': ('Y', True),
    }
    
    # Ten cac dau
    # Dấu đơn:
    # 0x0300: grave, 0x0301: acute, 0x0303: tilde, 0x0309: hook, 0x0323: dotbelow
    # 0x0306: breve, 0x0302: circumflex, 0x031B: horn
    
    accent_map_lower = {
        0x0300: 'gravecomb',
        0x0301: 'acutecomb',
        0x0303: 'tildecomb',
        0x0309: 'hookabovecomb',
        0x0323: 'dotbelowcomb',
        0x0306: 'brevecomb',
        0x0302: 'circumflexcomb',
        0x031B: 'horncomb',
    }
    accent_map_upper = {
        0x0300: 'gravecomb.case',
        0x0301: 'acutecomb.case',
        0x0303: 'tildecomb.case',
        0x0309: 'hookabovecomb.case',
        0x0323: 'dotbelowcomb.case',
        0x0306: 'uni0306.case',
        0x0302: 'uni0302.case',
        0x031B: 'horncomb.case',
    }
    
    added_count = 0
    for ch in VI_CHARS:
        cp = ord(ch)
        if cp in cmap:
            continue
            
        nfd = unicodedata.normalize('NFD', ch)
        base_char = nfd[0]
        marks = [ord(m) for m in nfd[1:]]
        
        base_glyph, is_upper = v_map[base_char]
        base_cx = get_vowel_cx(base_glyph)
        base_w = hmtx[base_glyph][0]
        
        comp_list = []
        
        # Truong hop 1 dau
        if len(marks) == 1:
            m = marks[0]
            if is_upper:
                m_name = accent_map_upper[m]
                ox = base_cx - case_mark_cx
            else:
                m_name = accent_map_lower[m]
                ox = base_cx - mark_cx
            
            # Neu la dau moc (horn) tren o/u
            if m == 0x031B:
                # Can le phai cua chu
                g_base = glyf[base_glyph]
                if is_upper:
                    ox = g_base.xMax - 180
                else:
                    ox = g_base.xMax - 140
            comp_list.append((m_name, ox, 0))
            
        # Truong hop 2 dau (vi du: ơ/ư + dau thanh, hoac a/e/o mu + dau thanh)
        elif len(marks) == 2:
            # marks co the gom (mu/moc/trang) va (dau thanh)
            # Sap xep: mu/moc truoc, dau thanh sau (hoac nguoc lai)
            hat = next((m for m in marks if m in (0x0302, 0x0306, 0x031B)), None)
            tone = next((m for m in marks if m in (0x0300, 0x0301, 0x0303, 0x0309, 0x0323)), None)
            
            # 1. Hat / horn
            if hat == 0x031B: # Horn (ơ, ư)
                g_base = glyf[base_glyph]
                if is_upper:
                    comp_list.append((accent_map_upper[hat], g_base.xMax - 180, 0))
                else:
                    comp_list.append((accent_map_lower[hat], g_base.xMax - 140, 0))
            elif hat in (0x0302, 0x0306): # Circumflex hoặc Breve
                if is_upper:
                    comp_list.append((accent_map_upper[hat], base_cx - case_mark_cx, 0))
                else:
                    comp_list.append((accent_map_lower[hat], base_cx - mark_cx, 0))
                    
            # 2. Tone
            if tone == 0x0323: # Dấu nặng: nằm dưới đáy, giữ nguyên Y
                if is_upper:
                    comp_list.append((accent_map_upper[tone], base_cx - case_mark_cx, 0))
                else:
                    comp_list.append((accent_map_lower[tone], base_cx - mark_cx, 0))
            elif tone is not None:
                # Neu la tren mu circumflex/breve, day dau thanh len cao hon (+320 y)
                if hat in (0x0302, 0x0306):
                    shift_y = 330 if not is_upper else 340
                    shift_x = 70 if tone == 0x0301 else (-70 if tone == 0x0300 else 0)
                    if is_upper:
                        comp_list.append((accent_map_upper[tone], base_cx - case_mark_cx + shift_x, shift_y))
                    else:
                        comp_list.append((accent_map_lower[tone], base_cx - mark_cx + shift_x, shift_y))
                else:
                    # Tren ơ, ư: dấu thanh nằm ở giữa thân chữ bình thường
                    if is_upper:
                        comp_list.append((accent_map_upper[tone], base_cx - case_mark_cx, 0))
                    else:
                        comp_list.append((accent_map_lower[tone], base_cx - mark_cx, 0))
                        
        # Tao glyph moi
        g_name = f"uni{cp:04X}"
        new_g = make_composite(glyf, base_glyph, comp_list)
        glyf[g_name] = new_g
        hmtx[g_name] = (base_w, new_g.xMin)
        
        # Them vao cmap
        for table in font['cmap'].tables:
            table.cmap[cp] = g_name
        added_count += 1
        
    print(f"-> Added {added_count} native Vietnamese glyphs to {font_path}")
    font.save(out_path)
    print(f"Saved: {out_path}")

print("MarkW1G native patcher loaded.")
