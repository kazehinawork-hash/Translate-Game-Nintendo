"""Kiem tra font Hades II: (1) giu du glyph goc, (2) phu het ky tu dung trong ban dich."""
import os
import re
import struct
import sys

sys.stdout.reconfigure(encoding='utf-8')
ROOT = r'E:\OneDrive\3.家 Jiā Home\99. 其他 Qítā Other\96.Translate Game'
G = os.path.join(ROOT, 'games', '0100A00019DE0000_Hades2', 'source', 'orig_font')
M = os.path.join(ROOT, 'output', 'atmosphere', 'contents', '0100A00019DE0000', 'romfs', 'Fonts')
TR = os.path.join(ROOT, 'games', '0100A00019DE0000_Hades2', 'translations')


def read_7bit(buf, off):
    val = shift = 0
    while True:
        b = buf[off]
        off += 1
        val |= (b & 0x7F) << shift
        if not (b & 0x80):
            break
        shift += 7
    return val, off


def xnb_chars(path):
    data = open(path, 'rb').read()
    data_len, = struct.unpack_from('<I', data, 10 + 16)  # fmt,width,height,mip,dataLen -> offset 26
    # doc lai cho chac: header XNB: 'XNB'+plat+ver(2)+flags+fileSize(4) = 10; texture header 20 byte
    _, w, h, mip, dlen = struct.unpack_from('<IIIII', data, 10)
    pos = 10 + 20 + dlen
    num_glyphs, pos = read_7bit(data, pos)
    pos += num_glyphs * 16
    num_crop, pos = read_7bit(data, pos)
    pos += num_crop * 16
    num_chars, pos = read_7bit(data, pos)
    chars = []
    for _ in range(num_chars):
        b0 = data[pos]
        cl = 1 if b0 < 0x80 else 2 if (b0 & 0xE0) == 0xC0 else 3 if (b0 & 0xF0) == 0xE0 else 4
        chars.append(data[pos:pos + cl].decode('utf-8'))
        pos += cl
    return num_glyphs, num_crop, chars


def text_chars():
    used = set()
    for r, _, fs in os.walk(TR):
        for f in fs:
            if f.endswith(('.sjson', '.json', '.txt')):
                try:
                    s = open(os.path.join(r, f), encoding='utf-8').read()
                except Exception:
                    continue
                used |= set(s)
    return used


print('=== DOC BAN DICH ===')
used = text_chars()
vn = {c for c in used if ord(c) > 0x7F and c.isprintable()}
print(f'  ky tu khac ASCII dung trong ban dich: {len(vn)}')
print(f'  {"".join(sorted(vn))[:160]}')

print('\n=== SO SANH FONT (bin/en) ===')
od = os.path.join(G, 'bin', 'en')
md = os.path.join(M, 'bin', 'en')
ok = True
for fn in sorted(os.listdir(md)):
    op = os.path.join(od, fn)
    mp = os.path.join(md, fn)
    if not os.path.exists(op):
        print(f'  {fn}: (khong co font goc)')
        continue
    ng_o, nc_o, co = xnb_chars(op)
    ng_m, nc_m, cm = xnb_chars(mp)
    so, sm = set(co), set(cm)
    lost = so - sm
    new = sm - so
    missing_used = {c for c in vn if c not in sm and c not in ('\t', '\n', '\r')}
    status = 'OK' if not lost and not missing_used else 'LOI'
    if status == 'LOI':
        ok = False
    print(f'  {fn:<46} glyph {ng_o:>4}->{ng_m:<4} | ky tu {nc_o:>4}->{nc_m:<4} | mat {len(lost):>3} | thieu(chu dich) {len(missing_used):>2} [{status}]')
    if lost:
        print(f'      MAT: {"".join(sorted(lost))[:80]}')
    if missing_used:
        print(f'      THIEU: {"".join(sorted(missing_used))[:80]}')

print('\n=== SO SANH FONT (bin/720p/en) ===')
od = os.path.join(G, 'bin', '720p', 'en')
md = os.path.join(M, 'bin', '720p', 'en')
if os.path.isdir(md):
    for fn in sorted(os.listdir(md)):
        op, mp = os.path.join(od, fn), os.path.join(md, fn)
        if not os.path.exists(op):
            continue
        ng_o, nc_o, co = xnb_chars(op)
        ng_m, nc_m, cm = xnb_chars(mp)
        lost = set(co) - set(cm)
        mu = {c for c in vn if c not in set(cm) and c not in ('\t', '\n', '\r')}
        if lost or mu:
            ok = False
        print(f'  {fn:<46} glyph {ng_o:>4}->{ng_m:<4} | ky tu {nc_o:>4}->{nc_m:<4} | mat {len(lost)} | thieu {len(mu)} [{"OK" if not lost and not mu else "LOI"}]')

print('\nKET QUA FONT:', 'PASS' if ok else 'CO LOI')
