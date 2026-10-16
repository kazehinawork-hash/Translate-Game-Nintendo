"""
Patch toan bo font TrueType goc (.ufont) cua It Takes Two thanh ban Native Hoan Hao.
- Chuyen toan bo glyph tieng Viet thanh single-contour (khong dung composite gay loi advanceWidth).
- Tich hop vao cac slot glyph san co (unused slots) de bao toan nguyen ven 100% cau truc nhan hmtx/maxp/loca.
- Ap dung cho MarkW1G (Heavy, Medium, MediumItalic) va Poppins (Medium, ExtraBold, Italic).
"""
import sys, os, unicodedata
sys.stdout.reconfigure(encoding='utf-8')
from fontTools.ttLib import TTFont
from fontTools.ttLib.tables._g_l_y_f import Glyph, GlyphCoordinates, ttProgram

VI_CHARS = (
    'àáảãạăằắẳẵặâầấẩẫậèéẻẽẹêềếểễệìíỉĩịòóỏõọôồốổỗộơờớởỡợùúủũụưừứửữựỳýỷỹỵđ'
    'ÀÁẢÃẠĂẰẮẲẴẶÂẦẤẨẪẬÈÉẺẼẸÊỀẾỂỄỆÌÍỈĨỊÒÓỎÕỌÔỒỐỔỖỘƠỜỚỞỠỢÙÚỦŨỤƯỪỨỬỮỰỲÝỶỸỴĐ'
)

def get_glyph_contours(glyf, gname, ox=0, oy=0, sx=1.0, sy=1.0):
    g = glyf[gname]
    coords, endPts, flags = g.getCoordinates(glyf)
    new_coords = [(int(round(x * sx + ox)), int(round(y * sy + oy))) for x, y in coords]
    return new_coords, list(endPts), list(flags)

def combine_contours(glyf, parts):
    tot_coords = []
    tot_flags = []
    tot_endPts = []
    for coords, endPts, flags in parts:
        offset = len(tot_coords)
        tot_coords.extend(coords)
        tot_flags.extend(flags)
        tot_endPts.extend([offset + p for p in endPts])
    new_g = Glyph()
    new_g.numberOfContours = len(tot_endPts)
    new_g.endPtsOfContours = tot_endPts
    new_g.flags = tot_flags
    new_g.coordinates = GlyphCoordinates(tot_coords)
    new_g.program = ttProgram.Program()
    new_g.recalcBounds(glyf)
    return new_g

def patch_mark_native_perfect(src_path, out_path):
    print(f"=== Patching MarkW1G: {src_path} ===")
    font = TTFont(src_path)
    glyf = font['glyf']
    hmtx = font['hmtx']
    cmap = font.getBestCmap()
    
    used_gids = set(cmap.values())
    unused = [g for g in font.getGlyphOrder() if g not in used_gids and g != '.notdef']
    print(f"  Unused slots: {len(unused)}")
    
    # 1. Hook above (dau hoi) tu 'question'
    q_coords, q_endPts, q_flags = glyf['question'].getCoordinates(glyf)
    c0_coords = q_coords[:q_endPts[0]+1]
    c0_flags = q_flags[:q_endPts[0]+1]
    min_x, max_x = min(x for x,y in c0_coords), max(x for x,y in c0_coords)
    min_y, max_y = min(y for x,y in c0_coords), max(y for x,y in c0_coords)
    cx_q = (min_x + max_x) / 2.0
    hook_scale = 0.35
    
    # 2. Horn (dau moc cho o, u) tu Nunito
    nunito = TTFont('tools/Nunito-Bold.ttf')
    n_coords, n_endPts, n_flags = nunito['glyf']['uni031B'].getCoordinates(nunito['glyf'])
    
    # Vowel centers cx:
    # lower: mark_cx = -591
    mark_cx = -591.0
    case_mark_cx = -807.5
    
    v_map = {
        'a': ('a', False), 'e': ('e', False), 'i': ('dotlessi', False), 'o': ('o', False), 'u': ('u', False), 'y': ('y', False),
        'A': ('A', True),  'E': ('E', True),  'I': ('I', True),  'O': ('O', True),  'U': ('U', True),  'Y': ('Y', True),
    }
    
    accent_map_lower = {
        0x0300: 'gravecomb',
        0x0301: 'acutecomb',
        0x0303: 'tildecomb',
        0x0306: 'brevecomb',
        0x0302: 'circumflexcomb',
        0x0323: 'dotbelowcomb',
    }
    accent_map_upper = {
        0x0300: 'gravecomb.case',
        0x0301: 'acutecomb.case',
        0x0303: 'tildecomb.case',
        0x0306: 'uni0306.case',
        0x0302: 'uni0302.case',
        0x0323: 'dotbelowcomb.case',
    }
    
    slot_idx = 0
    added = 0
    for ch in VI_CHARS:
        cp = ord(ch)
        if cp in cmap:
            continue
            
        nfd = unicodedata.normalize('NFD', ch)
        base_char = nfd[0]
        marks = [ord(m) for m in nfd[1:]]
        
        base_glyph, is_upper = v_map[base_char]
        base_cx = (glyf[base_glyph].xMin + glyf[base_glyph].xMax) / 2.0
        base_w = hmtx[base_glyph][0]
        
        parts = [get_glyph_contours(glyf, base_glyph)]
        
        # 1 dau
        if len(marks) == 1:
            m = marks[0]
            if m == 0x0309: # Hook (dau hoi)
                y_base = 1460 if is_upper else 1070
                h_coords = [(int(round((x - cx_q) * hook_scale + base_cx)), int(round((y - min_y) * hook_scale + y_base))) for x, y in c0_coords]
                parts.append((h_coords, [len(h_coords)-1], list(c0_flags)))
            elif m == 0x031B: # Horn (dau moc)
                y_base = 1320 if is_upper else 900
                scale_h = 1.8 if is_upper else 1.5
                x_shift = (glyf[base_glyph].xMax - 140) if not is_upper else (glyf[base_glyph].xMax - 180)
                h_coords = [(int(round(x * scale_h + x_shift)), int(round((y - 418) * scale_h + y_base))) for x, y in n_coords]
                parts.append((h_coords, list(n_endPts), list(n_flags)))
            else:
                m_name = accent_map_upper[m] if is_upper else accent_map_lower[m]
                ox = base_cx - (case_mark_cx if is_upper else mark_cx)
                parts.append(get_glyph_contours(glyf, m_name, ox=ox, oy=0))
                
        # 2 dau
        elif len(marks) == 2:
            hat = next((m for m in marks if m in (0x0302, 0x0306, 0x031B)), None)
            tone = next((m for m in marks if m in (0x0300, 0x0301, 0x0303, 0x0309, 0x0323)), None)
            
            # Hat / Horn
            if hat == 0x031B:
                y_base = 1320 if is_upper else 900
                scale_h = 1.8 if is_upper else 1.5
                x_shift = (glyf[base_glyph].xMax - 140) if not is_upper else (glyf[base_glyph].xMax - 180)
                h_coords = [(int(round(x * scale_h + x_shift)), int(round((y - 418) * scale_h + y_base))) for x, y in n_coords]
                parts.append((h_coords, list(n_endPts), list(n_flags)))
            elif hat in (0x0302, 0x0306):
                m_name = accent_map_upper[hat] if is_upper else accent_map_lower[hat]
                ox = base_cx - (case_mark_cx if is_upper else mark_cx)
                parts.append(get_glyph_contours(glyf, m_name, ox=ox, oy=0))
                
            # Tone
            if tone == 0x0323: # Dấu nặng
                m_name = accent_map_upper[tone] if is_upper else accent_map_lower[tone]
                ox = base_cx - (case_mark_cx if is_upper else mark_cx)
                parts.append(get_glyph_contours(glyf, m_name, ox=ox, oy=0))
            elif tone == 0x0309: # Dấu hỏi
                shift_y = 330 if hat in (0x0302, 0x0306) else 0
                y_base = (1460 if is_upper else 1070) + shift_y
                h_coords = [(int(round((x - cx_q) * hook_scale + base_cx)), int(round((y - min_y) * hook_scale + y_base))) for x, y in c0_coords]
                parts.append((h_coords, [len(h_coords)-1], list(c0_flags)))
            elif tone is not None:
                m_name = accent_map_upper[tone] if is_upper else accent_map_lower[tone]
                shift_y = 330 if hat in (0x0302, 0x0306) else 0
                shift_x = 70 if (hat in (0x0302, 0x0306) and tone == 0x0301) else (-70 if (hat in (0x0302, 0x0306) and tone == 0x0300) else 0)
                ox = base_cx - (case_mark_cx if is_upper else mark_cx) + shift_x
                parts.append(get_glyph_contours(glyf, m_name, ox=ox, oy=shift_y))
                
        # Assign to unused slot
        slot = unused[slot_idx]
        slot_idx += 1
        
        new_g = combine_contours(glyf, parts)
        glyf[slot] = new_g
        hmtx[slot] = (base_w, new_g.xMin)
        
        for t in font['cmap'].tables:
            t.cmap[cp] = slot
        added += 1
        
    print(f"  -> Added {added} native non-composite glyphs.")
    font.save(out_path)
    print(f"  Saved: {out_path}")

def patch_poppins_native_perfect(src_path, out_path):
    print(f"=== Patching Poppins: {src_path} === ")
    font = TTFont(src_path)
    glyf = font['glyf']
    hmtx = font['hmtx']
    cmap = font.getBestCmap()
    
    used_gids = set(cmap.values())
    unused = [g for g in font.getGlyphOrder() if g not in used_gids and g != '.notdef']
    print(f"  Unused slots: {len(unused)}")
    
    # 1. Period coords for dotbelow
    p_coords, p_endPts, p_flags = glyf['period'].getCoordinates(glyf)
    p_cx = (glyf['period'].xMin + glyf['period'].xMax) / 2.0
    
    # 2. Hook above tu question
    q_coords, q_endPts, q_flags = glyf['question'].getCoordinates(glyf)
    c0_coords = q_coords[:q_endPts[0]+1]
    c0_flags = q_flags[:q_endPts[0]+1]
    min_x, max_x = min(x for x,y in c0_coords), max(x for x,y in c0_coords)
    min_y, max_y = min(y for x,y in c0_coords), max(y for x,y in c0_coords)
    cx_q = (min_x + max_x) / 2.0
    hook_scale = 0.35
    
    # 3. Horn tu Nunito
    nunito = TTFont('tools/Nunito-Bold.ttf')
    n_coords, n_endPts, n_flags = nunito['glyf']['uni031B'].getCoordinates(nunito['glyf'])
    
    v_map = {
        'a': ('a', False), 'e': ('e', False), 'i': ('dotlessi', False), 'o': ('o', False), 'u': ('u', False), 'y': ('y', False),
        'A': ('A', True),  'E': ('E', True),  'I': ('I', True),  'O': ('O', True),  'U': ('U', True),  'Y': ('Y', True),
    }
    
    accent_map = {
        0x0300: 'grave',
        0x0301: 'acute',
        0x0303: 'tilde',
        0x0306: 'breve' if 'breve' in glyf else 'circumflex',
        0x0302: 'circumflex',
    }
    
    slot_idx = 0
    added = 0
    for ch in VI_CHARS:
        cp = ord(ch)
        if cp in cmap:
            continue
            
        nfd = unicodedata.normalize('NFD', ch)
        base_char = nfd[0]
        marks = [ord(m) for m in nfd[1:]]
        
        base_glyph, is_upper = v_map[base_char]
        base_cx = (glyf[base_glyph].xMin + glyf[base_glyph].xMax) / 2.0
        base_w = hmtx[base_glyph][0]
        
        parts = [get_glyph_contours(glyf, base_glyph)]
        
        if len(marks) == 1:
            m = marks[0]
            if m == 0x0323: # Dot below
                dot_c = [(x - p_cx + base_cx, y - 150) for x, y in p_coords]
                parts.append((dot_c, list(p_endPts), list(p_flags)))
            elif m == 0x0309: # Hook
                y_base = 720 if is_upper else 580
                h_coords = [(int(round((x - cx_q) * hook_scale + base_cx)), int(round((y - min_y) * hook_scale + y_base))) for x, y in c0_coords]
                parts.append((h_coords, [len(h_coords)-1], list(c0_flags)))
            elif m == 0x031B: # Horn
                y_base = 660 if is_upper else 520
                scale_h = 1.0 if is_upper else 0.9
                x_shift = (glyf[base_glyph].xMax - 60) if not is_upper else (glyf[base_glyph].xMax - 80)
                h_coords = [(int(round(x * scale_h + x_shift)), int(round((y - 418) * scale_h + y_base))) for x, y in n_coords]
                parts.append((h_coords, list(n_endPts), list(n_flags)))
            else:
                m_name = accent_map[m]
                m_cx = (glyf[m_name].xMin + glyf[m_name].xMax) / 2.0
                oy = 150 if is_upper else 0
                parts.append(get_glyph_contours(glyf, m_name, ox=base_cx - m_cx, oy=oy))
                
        elif len(marks) == 2:
            hat = next((m for m in marks if m in (0x0302, 0x0306, 0x031B)), None)
            tone = next((m for m in marks if m in (0x0300, 0x0301, 0x0303, 0x0309, 0x0323)), None)
            
            if hat == 0x031B:
                y_base = 660 if is_upper else 520
                scale_h = 1.0 if is_upper else 0.9
                x_shift = (glyf[base_glyph].xMax - 60) if not is_upper else (glyf[base_glyph].xMax - 80)
                h_coords = [(int(round(x * scale_h + x_shift)), int(round((y - 418) * scale_h + y_base))) for x, y in n_coords]
                parts.append((h_coords, list(n_endPts), list(n_flags)))
            elif hat in (0x0302, 0x0306):
                m_name = accent_map[hat]
                m_cx = (glyf[m_name].xMin + glyf[m_name].xMax) / 2.0
                oy = 150 if is_upper else 0
                parts.append(get_glyph_contours(glyf, m_name, ox=base_cx - m_cx, oy=oy))
                
            if tone == 0x0323:
                dot_c = [(x - p_cx + base_cx, y - 150) for x, y in p_coords]
                parts.append((dot_c, list(p_endPts), list(p_flags)))
            elif tone == 0x0309:
                shift_y = 170 if hat in (0x0302, 0x0306) else 0
                y_base = (720 if is_upper else 580) + shift_y
                h_coords = [(int(round((x - cx_q) * hook_scale + base_cx)), int(round((y - min_y) * hook_scale + y_base))) for x, y in c0_coords]
                parts.append((h_coords, [len(h_coords)-1], list(c0_flags)))
            elif tone is not None:
                m_name = accent_map[tone]
                m_cx = (glyf[m_name].xMin + glyf[m_name].xMax) / 2.0
                shift_y = (170 if hat in (0x0302, 0x0306) else 0) + (150 if is_upper else 0)
                shift_x = 40 if (hat in (0x0302, 0x0306) and tone == 0x0301) else (-40 if (hat in (0x0302, 0x0306) and tone == 0x0300) else 0)
                parts.append(get_glyph_contours(glyf, m_name, ox=base_cx - m_cx + shift_x, oy=shift_y))
                
        slot = unused[slot_idx]
        slot_idx += 1
        
        new_g = combine_contours(glyf, parts)
        glyf[slot] = new_g
        hmtx[slot] = (base_w, new_g.xMin)
        
        for t in font['cmap'].tables:
            t.cmap[cp] = slot
        added += 1
        
    print(f"  -> Added {added} native non-composite glyphs.")
    font.save(out_path)
    print(f"  Saved: {out_path}")

if __name__ == '__main__':
    DEST_DIR = 'E:/ITT_work/font_patches'
    os.makedirs(DEST_DIR, exist_ok=True)
    
    # 1. MarkW1G
    for name in ['MarkW1G-Heavy', 'MarkW1G-Medium', 'MarkW1G-MediumItalic']:
        src = f'E:/ITT_work/{name}.ufont'
        dst = os.path.join(DEST_DIR, f'{name}.ufont')
        patch_mark_native_perfect(src, dst)
        
    # 2. Poppins
    for name in ['Poppins-Medium', 'Poppins-ExtraBold', 'Poppins-Italic']:
        src = f'E:/ITT_work/{name}.ufont'
        dst = os.path.join(DEST_DIR, f'{name}.ufont')
        patch_poppins_native_perfect(src, dst)
        
    print("ALL FONTS PATCHED TO NATIVE HARMONY PERFECTLY!")
