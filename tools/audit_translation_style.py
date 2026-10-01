import re
import sys
from pathlib import Path

if sys.stdout.encoding and sys.stdout.encoding.lower() != 'utf-8':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / 'tools'))
from hades2_sjson_helper import parse_sjson_entries

TR = ROOT / 'translations/0100A00019DE0000_Hades2/Game/Text/en'
SRC = ROOT / 'working/0100A00019DE0000_Hades2/raw_text/en'

# 1. Các mẫu dịch máy thô, giữ nguyên ngữ pháp bị động tiếng Anh (word-by-word)
MACHINE_PATTERNS = [
    (re.compile(r'bị\s+([^\.,;!\?]+?)\s+bởi\b', re.IGNORECASE), "Cấu trúc bị động cứng nhắc 'bị ... bởi'"),
    (re.compile(r'được\s+([^\.,;!\?]+?)\s+bởi\b', re.IGNORECASE), "Cấu trúc bị động cứng nhắc 'được ... bởi'"),
    (re.compile(r'\bbạn\s+đã\s+bị\b', re.IGNORECASE), "Xưng hô 'bạn' cứng nhắc trong game thần thoại Hy Lạp"),
    (re.compile(r'\bcủa\s+bạn\b', re.IGNORECASE), "Dùng 'của bạn' thừa thãi (your...)"),
    (re.compile(r'\bcho\s+phép\s+bạn\b', re.IGNORECASE), "Dịch thô 'allows you to' thành 'cho phép bạn'"),
    (re.compile(r'\blàm\s+cho\s+bạn\b', re.IGNORECASE), "Dịch thô 'makes you'"),
]

# 2. Kiểm tra hallucination / bịa đặt:
# - Độ lệch chiều dài bất thường: câu tiếng Anh ngắn mà tiếng Việt dài gấp 3.5 lần trở lên mà không phải do giải thích thuật ngữ UI.
# - Câu nguồn là tiếng kêu/thán từ (e.g. "...", "Ugh", "Ah") nhưng câu dịch bịa ra cả câu văn dài.

passive_hits = []
hallucination_hits = []

for tr_file in sorted(TR.glob('*.sjson')):
    src_file = SRC / tr_file.name
    if not src_file.exists():
        continue
        
    raw_tr = tr_file.read_text(encoding='utf-8-sig')
    raw_src = src_file.read_text(encoding='utf-8-sig')
    
    try:
        tr_entries = parse_sjson_entries(raw_tr)
        src_entries = parse_sjson_entries(raw_src)
    except Exception:
        continue
        
    for eid, tr_val in tr_entries.items():
        src_val = src_entries.get(eid)
        if not src_val:
            continue
            
        for field in ('DisplayName', 'Description'):
            tr_t = tr_val.get(field) or ''
            src_t = src_val.get(field) or ''
            
            if not tr_t or not src_t or tr_t == src_t:
                continue
                
            # Kiểm tra passive / dịch máy thô
            for pat, desc in MACHINE_PATTERNS:
                m = pat.findall(tr_t)
                if m:
                    passive_hits.append((tr_file.name, eid, field, desc, tr_t))
                    
            # Kiểm tra hallucination
            # Trường hợp 1: Source là thán từ ngắn (dưới 10 ký tự, dấu chấm...) nhưng dịch thành câu văn dài > 40 ký tự
            clean_src = re.sub(r'\{[^{}]*\}', '', src_t).strip()
            clean_tr = re.sub(r'\{[^{}]*\}', '', tr_t).strip()
            
            if len(clean_src) <= 8 and clean_src in ('...', 'Ah.', 'Oh.', 'Ugh.', 'Hmm.', 'Ha!', 'Hey.', 'Well.') and len(clean_tr) > 25:
                hallucination_hits.append((tr_file.name, eid, field, f"Nguồn ngắn '{clean_src}' nhưng dịch quá dài: '{clean_tr}'"))
                
            # Trường hợp 2: Tỉ lệ độ dài bất thường (> 4x với văn bản dài > 20 ký tự)
            if len(clean_src) >= 20 and len(clean_tr) > 4 * len(clean_src):
                hallucination_hits.append((tr_file.name, eid, field, f"Độ dài tăng bất thường {len(clean_src)} -> {len(clean_tr)}: '{clean_tr[:80]}...'"))

print(f"=== KẾT QUẢ RÀ SOÁT VĂN PHONG & CHẤT LƯỢNG BẢN DỊCH ===")
print(f"1. Số điểm nghi vấn cấu trúc dịch máy / bị động thô: {len(passive_hits)}")
for f, eid, field, desc, text in passive_hits[:15]:
    print(f"   [{f}:{eid}] ({desc}):\n      -> \"{text[:100]}\"")

print(f"\n2. Số điểm nghi vấn 'bịa đặt' (Hallucination) / lệch nội dung: {len(hallucination_hits)}")
for f, eid, field, detail in hallucination_hits[:15]:
    print(f"   [{f}:{eid}]: {detail}")

