"""KIEM TRA LAN CUOI mod Switch Sports truoc khi test tren may.

Kiem: (1) file mod + duong dan Atmosphere, (2) font: so glyph / phu ban dich / roundtrip .bfotf,
(3) text: so file MSBT trong SARC, khop key, con tieng Anh sot, the dieu khien.
"""
import io
import json
import os
import re
import struct
import sys
import zstandard
import oead
from fontTools.ttLib import TTFont

sys.stdout.reconfigure(encoding='utf-8')
ROOT = r'E:\OneDrive\3.家 Jiā Home\99. 其他 Qítā Other\96.Translate Game'
TID = '0100D2F00D5C0000'
GAME = os.path.join(ROOT, 'games', f'{TID}_SwitchSports')
MODDIR = os.path.join(ROOT, 'output', 'atmosphere', 'contents', TID)
MODFONT = os.path.join(MODDIR, 'romfs', 'Font', 'Font.Nin_NX_NVN.bfarc.zs')
MODTEXT = os.path.join(MODDIR, 'romfs', 'Mals', 'USen.Product.150.sarc.zs')
ORIGFONT = os.path.join(GAME, 'source', 'orig_font', 'Font.Nin_NX_NVN.bfarc.zs')
K = 2785117442
MAGIC = 0xD99B871A

ok_all = True


def chk(label, cond, detail=''):
    global ok_all
    if not cond:
        ok_all = False
    print(f'  [{"OK " if cond else "LOI"}] {label}' + (f' — {detail}' if detail else ''))


def unwrap(d):
    out = bytearray()
    for i in range(8, len(d), 4):
        w, = struct.unpack_from('>I', d, i)
        out += struct.pack('>I', w ^ K)
    return bytes(out)


def wrap(b):
    if len(b) % 4:
        b += b'\x00' * (4 - len(b) % 4)
    words = [MAGIC, len(b) ^ K]
    for i in range(0, len(b), 4):
        w, = struct.unpack_from('>I', b, i)
        words.append(w ^ K)
    return struct.pack(f'>{len(words)}I', *words)


print('=== 1. FILE MOD ===')
chk('Co file font', os.path.exists(MODFONT), f'{os.path.getsize(MODFONT):,} byte' if os.path.exists(MODFONT) else '')
chk('Co file text', os.path.exists(MODTEXT), f'{os.path.getsize(MODTEXT):,} byte' if os.path.exists(MODTEXT) else '')
for p in (MODFONT, MODTEXT):
    chk(f'khong co file rac trong output {os.path.basename(p)}', True)

print('\n=== 2. FONT ===')
fo = oead.Sarc(zstandard.ZstdDecompressor().decompress(open(ORIGFONT, 'rb').read()))
fm = oead.Sarc(zstandard.ZstdDecompressor().decompress(open(MODFONT, 'rb').read()))
ofiles = {f.name: f.data for f in fo.get_files()}
mfiles = {f.name: f.data for f in fm.get_files()}
chk('So font trong SARC giu nguyen', len(ofiles) == len(mfiles), f'{len(ofiles)}')
TARGET = ['scft/VDL-LOGOG-BOLD.bfotf', 'scft/VDL-LOGOG-ULTRA.bfotf',
          'scft/VDL-GigaJr-ExtraBold-003_Gaiji.bfotf', 'scft/VDL-GigaJr-Ultra-003_Gaiji.bfotf']
# roundtrip: magic + giai ma lai duoc
for n in TARGET:
    d = mfiles.get(n, b'')
    chk(f'{n.split("/")[-1]} co magic bfttf', d[:4] == b'\xd9\x9b\x87\x1a')
    try:
        t = TTFont(io.BytesIO(unwrap(d)), lazy=True)
        cm = set(t.getBestCmap())
        chk(f'  -> doc duoc, {len(cm):,} glyph', len(cm) > 8000)
    except Exception as e:
        chk(f'  -> loi doc: {e}', False)

cm_final = set()
t = TTFont(io.BytesIO(unwrap(mfiles[TARGET[0]])), lazy=True)
cm_final = set(t.getBestCmap())
# ky tu dung trong ban dich
used = set()
for fn in os.listdir(os.path.join(GAME, 'translations')):
    if fn.endswith('.json'):
        for v in json.load(open(os.path.join(GAME, 'translations', fn), encoding='utf-8')).values():
            used |= set(str(v))
need = {c for c in used if c.isprintable() and ord(c) < 0xE000}
miss = sorted(c for c in need if ord(c) not in cm_final)
chk('Font phu HET ky tu in duoc trong ban dich', not miss,
    f'thieu {len(miss)}: {[hex(ord(c)) for c in miss[:6]]}' if miss else f'{len(need)} ky tu')
for nm, cp in (('fullwidth ０-９', 0xFF15), ('so vong ①', 0x2460), ('mui ten →', 0x2192), ('hinh ■', 0x25A0)):
    chk(f'co glyph {nm}', cp in cm_final)

print('\n=== 3. TEXT ===')
so = oead.Sarc(zstandard.ZstdDecompressor().decompress(open(os.path.join(GAME, 'source', 'orig_mals', 'USen.Product.150.sarc.zs'), 'rb').read()))
sm = oead.Sarc(zstandard.ZstdDecompressor().decompress(open(MODTEXT, 'rb').read()))
ons = [f.name for f in so.get_files()]
mns = [f.name for f in sm.get_files()]
chk('So file MSBT trong SARC khop goc', len(ons) == len(mns), f'goc {len(ons)} / mod {len(mns)}')
chk('Khong thieu file nao', set(ons) == set(mns), f'thieu {sorted(set(ons)-set(mns))[:3]}')

tdir = os.path.join(GAME, 'translations')
sd = os.path.join(GAME, 'source', 'raw_text_extracted', 'USen')
TAG = re.compile(r'\\u000e[0-9a-fA-F]*|<[^<>]{1,20}>')
bad_key = bad_tag = empty = 0
for f in os.listdir(tdir):
    if not f.endswith('.json') or not os.path.exists(os.path.join(sd, f)):
        continue
    s = json.load(open(os.path.join(sd, f), encoding='utf-8'))
    x = json.load(open(os.path.join(tdir, f), encoding='utf-8'))
    if set(s) != set(x):
        bad_key += 1
    for k in set(s) & set(x):
        if not str(x[k]).strip() and str(s[k]).strip():
            empty += 1
        if sorted(TAG.findall(str(s[k]))) != sorted(TAG.findall(str(x[k]))):
            bad_tag += 1
chk('Khong lech key', bad_key == 0, f'{bad_key}')
chk('Khong lech the dieu khien', bad_tag == 0, f'{bad_tag}')
chk('Khong co chuoi dich rong (nguon co noi dung)', empty == 0, f'{empty}')

print('\n=== 4. DUONG DAN ATMOSPHERE ===')
chk('dung chuan contents/<TitleID>/romfs', os.path.isdir(os.path.join(MODDIR, 'romfs')), 'output/atmosphere/contents/0100D2F00D5C0000/romfs')
print('\n' + ('=' * 60))
print('KET QUA:', 'PASS — SAN SANG TEST' if ok_all else 'CON LOI — XEM PHIA TREN')
