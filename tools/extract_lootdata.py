import os, json, sys
sys.path.insert(0, 'tools')
from hades2_sjson_helper import parse_sjson_entries

raw_dir = 'games/0100A00019DE0000_Hades2/source/raw_text/en'
files = [f for f in sorted(os.listdir(raw_dir)) if f.startswith('_LootData_') and f.endswith('.sjson')]

for f in files:
    in_path = os.path.join(raw_dir, f)
    with open(in_path, 'r', encoding='utf-8') as fl:
        text = fl.read()
    
    entries = parse_sjson_entries(text)
    export_list = []
    for entry_id, data in entries.items():
        if 'DisplayName' in data and data['DisplayName'].strip():
            item = {
                'Id': entry_id,
                'Source': data['DisplayName'],
                'Speaker': data.get('Speaker', '')
            }
            if 'Description' in data and data['Description'].strip():
                item['SourceDesc'] = data['Description']
            export_list.append(item)
            
    out_json = f'games/0100A00019DE0000_Hades2/source/_export_{f}.json'
    with open(out_json, 'w', encoding='utf-8') as out_f:
        json.dump(export_list, out_f, ensure_ascii=False, indent=2)
    print(f'Đã trích xuất {len(export_list):3} entry từ {f} -> {out_json}')
