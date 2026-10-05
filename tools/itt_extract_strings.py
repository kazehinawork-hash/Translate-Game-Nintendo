"""Boc toan bo chuoi It Takes Two (StringTable + TextProperty trong asset phu de)."""
import json
import os
import sys

sys.stdout.reconfigure(encoding='utf-8')
J = r'E:\ITT_work\json'
OUT = r'E:\ITT_work\strings.json'

items = []


def add(asset, jpath, text):
    if isinstance(text, str) and text.strip():
        items.append({'asset': asset, 'path': jpath, 'en': text})


# 1. StringTable
st_dir = os.path.join(J, 'Nuts', 'Content', 'Untold', 'StringTables')
for f in sorted(os.listdir(st_dir)) if os.path.isdir(st_dir) else []:
    if not f.endswith('.json'):
        continue
    p = os.path.join(st_dir, f)
    d = json.load(open(p, encoding='utf-8'))
    for ei, ex in enumerate(d.get('Exports') or []):
        tab = ex.get('Table')
        if not isinstance(tab, dict) or not isinstance(tab.get('Value'), list):
            continue
        for i, row in enumerate(tab['Value']):
            if isinstance(row, list) and len(row) >= 2:
                add(os.path.relpath(p, J), f'Exports[{ei}].Table.Value[{i}][1]', row[1])

# 2. Moi TextPropertyData.CultureInvariantString trong asset phu de (duyet de quy)
def walk(o, asset, path):
    if isinstance(o, dict):
        t = str(o.get('$type', ''))
        if 'TextPropertyData' in t:
            v = o.get('CultureInvariantString')
            if isinstance(v, str) and v.strip():
                add(asset, path + '.CultureInvariantString', v)
            return
        for k, v in o.items():
            walk(v, asset, f'{path}.{k}' if path else k)
    elif isinstance(o, list):
        for i, v in enumerate(o):
            walk(v, asset, f'{path}[{i}]')


sub_dir = os.path.join(J, 'Nuts', 'Content', 'Cinematics', 'Subtitles', 'Generated')
n_sub_files = 0
for f in sorted(os.listdir(sub_dir)) if os.path.isdir(sub_dir) else []:
    if not f.endswith('.json'):
        continue
    n_sub_files += 1
    p = os.path.join(sub_dir, f)
    d = json.load(open(p, encoding='utf-8'))
    walk(d.get('Exports') or [], os.path.relpath(p, J), 'Exports')

json.dump(items, open(OUT, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
print(f'BOC DUOC {len(items):,} chuoi tu {n_sub_files} file phu de + 2 StringTable')
print(f'  -> {OUT}')

assets = {i['asset'] for i in items}
print(f'  {len(assets)} asset co chuoi')
uniq = {i['en'] for i in items}
print(f'  {len(uniq):,} chuoi duy nhat')
lens = sorted(len(i['en']) for i in items)
print(f'  do dai: min {lens[0]} | trung vi {lens[len(lens)//2]} | max {lens[-1]:,}')
print('\nvi du:')
for i in items[:4]:
    print(f'  {i["en"][:85]!r}')
for i in items[-3:]:
    print(f'  {i["en"][:85]!r}')
