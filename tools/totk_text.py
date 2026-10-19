# -*- coding: utf-8 -*-
"""
totk_text.py — Bộ tách / che (mask) mã điều khiển MSBT của Zelda: Tears of the Kingdom.

Mục đích: mọi chuỗi văn bản TotK đều bắt đầu bằng các "thẻ điều khiển" nhiều byte
(\x0e...). Để subagent dịch mà KHÔNG thể phá thẻ, ta:
    1. tách chuỗi thành các đoạn [TAG] và [TEXT]
    2. thay mỗi TAG bằng token [[n]]
    3. gửi chuỗi đã che cho subagent dịch
    4. khôi phục token về đúng byte gốc

Nhờ vậy mã điều khiển được bảo toàn 100% (không phụ thuộc khả năng của model).

Các họ thẻ đã nhận diện từ dữ liệu thật:
  \x0e\x03\x00\x02 + 1          (đổi tông/màu)
  \x0e\x04\x00 + 2 + TÊN        (biểu cảm — TÊN lấy từ NAME_BASES)
  \x0e\x05 + 2                  (ngắt/nhịp)
  \x0e\x00\x03\x02 + 1          (mở/đóng đánh dấu thuật ngữ)
  \x0e\x00\x04\x00              (phân đoạn)
  \x0e\x00\x02\x02 + 1          (ngoặc đặc biệt)
  \x0e\x02 + 3 + TÊN + (\uffff + 1)   (thẻ biến số/đếm)
  \x0eÉ...                      (thẻ số nhiều point/points)
  \x0e\x01 + ...                (thẻ icon/bảng hiệu)
  \x0e + TÊN                    (dạng cũ)
"""
import re
import sys

# 105 base tên biểu cảm (lấy tự động từ kho text gốc; sắp theo độ dài giảm dần để khớp dài nhất)
NAME_BASES = [
    "Joy", "Cry", "Sad", "Run", "Savo", "Sigh", "Ease", "Talk", "Sava", "Work",
    "Chat", "Pass", "Care", "Tired", "Scare", "Angry", "Think", "Guess", "Sleep", "Taunt",
    "Happy", "Notice", "Custom", "AngryL", "Beware", "LaughM", "Rocket", "Eating", "Wakeup", "LaughS",
    "LaughL", "Humming", "Goodbye", "CallFar", "Puzzled", "Trouble", "Tension", "Painful", "Runaway", "Arrogant",
    "TuliHowl", "Surprise", "LaughBad", "TalkDeny", "Pointing", "Greeting", "Discovery", "WorkHeavy", "Shitauchi", "SurpriseM",
    "Nostalgia", "SurpriseS", "ShoutTalk", "SickThink", "Convinced", "Encourage", "TuliAngry", "SurpriseL", "SickCough", "Admiration",
    "Groundwork", "Irritation", "TuliNotice", "Understand", "SakuradaCM", "TuliSpirit", "Hysterical", "CustomHappy", "HiddenKorok", "Unconscious",
    "Observation", "Embarrassed", "ShidoSpirit", "Description", "Regrettable", "SagonoCheck", "ShidoClench", "Inspiration", "CustomVasaaq", "SickGreeting",
    "WeaponSwingS", "WeaponSwingM", "TuliPositive", "ShidoAizuchi", "CustomSavaaq", "TalkPositive", "ShidoInspire", "PurahGreeting", "YunBoArrogant", "YunBoGreeting",
    "ZeldaSurprise", "TuliDepressed", "CustomSavotta", "Determination", "QuestionAngry", "CustomSavsaaba", "QuestionNormal", "ShidoImpressed", "ArrogantLaughS", "SageSkillStart",
    "QuestionSurprise", "PurahTalkSerious", "ZeldaTalkPositive", "MiloyanTactPlayEnd", "ZeldaQuestionNormal",
]
NAME_BASES.sort(key=len, reverse=True)
_NN_RE = re.compile(r'_\d\d')
_ALNUM = re.compile(r'[A-Za-z0-9_]')

# Ký tự điều khiển / PUA / fullwidth-terminator (không tính \n \r \t)
CTRL = re.compile(r'[\u0000-\u0008\u000b\u000c\u000e-\u001f\ue000-\uf8ff\uffff]')
# Lưới an toàn: mọi ký tự điều khiển còn sót trong đoạn văn cũng bị che riêng
STRAY = CTRL


def match_name(s, i):
    """Nếu tại vị trí i có TÊN biểu cảm, trả về chỉ số kết thúc, ngược lại None."""
    for b in NAME_BASES:
        if s.startswith(b, i):
            j = i + len(b)
            m = _NN_RE.match(s, j)
            if m:
                j = m.end()
            return j
    return None


def tag_end(s, i):
    """Cho s[i] == '\\x0e', trả về chỉ số kết thúc thẻ."""
    n = len(s)
    j = i + 1
    if j >= n:
        return n
    c = s[j]

    if c == '\x03':
        return min(i + 5, n)

    if c == '\x04':
        k = i + 5
        m = match_name(s, k)
        if m is not None:
            return m
        # lui lại nếu trong 2 byte đệm có '\x0e'
        for p in range(i + 3, min(i + 5, n)):
            if s[p] == '\x0e':
                return p
        return min(k, n)

    if c == '\x05':
        return min(i + 4, n)

    if c == '\x00':
        c3 = s[j + 1] if j + 1 < n else ''
        c4 = s[j + 2] if j + 2 < n else ''
        if c3 == '\x03' and c4 == '\x02':
            return min(i + 5, n)
        if c3 == '\x04':
            return min(i + 4, n)
        if c3 == '\x02' and c4 == '\x02':
            return min(i + 5, n)
        return min(i + 2, n)

    if c == '\x02':
        k = i + 2
        cnt = 0
        esc = None
        while k < n and cnt < 3:
            if s[k] == '\x0e':
                if esc is None:
                    esc = k
                k += 1
                cnt += 1
            elif ord(s[k]) >= 0x80 or ord(s[k]) < 0x20 or not s[k].isalnum():
                k += 1
                cnt += 1
            else:
                k += 1
                cnt += 1
        k2 = k
        while k2 < n and _ALNUM.match(s[k2]):
            k2 += 1
        if k2 > k:
            k = k2
            if k < n and s[k] == '\uffff':
                k += 1
                if k < n:
                    k += 1
            return k
        if esc is not None:
            return esc
        return k

    if c == '\xc9':                      # 'É' — thẻ số nhiều (point/points)
        k = i + 2
        if k < n and s[k] == '\x04':
            return min(k + 2, n)
        # tiêu thụ tới ký tự \x00 kết thúc (trong cửa sổ hợp lý), nếu không tới '\x0e' kế
        lim = min(n, i + 48)
        p = i + 2
        while p < lim:
            if s[p] == '\x00':
                return p + 1
            p += 1
        return min(i + 2, n)

    if c == '\x01':
        k = i + 2
        cnt = 0
        while k < n and cnt < 4:
            ch = s[k]
            o = ord(ch)
            if ch == '\x0e':
                break
            if o < 0x20 or o >= 0x80:
                k += 1
                cnt += 1
            else:
                break
        if cnt == 2 and k < n and s[k] != '\x0e' and 0x20 <= ord(s[k]) < 0x80:
            k += 1
            cnt += 1
            if k < n and s[k] == '\x00':
                k += 1
        return k

    if c == '\x0c':
        m = match_name(s, i + 2)
        return m if m is not None else min(i + 2, n)

    m = match_name(s, i + 1)
    if m is not None:
        return m
    return min(i + 2, n)


def split_parts(s):
    """Trả về danh sách ('tag', str) / ('text', str)."""
    out = []
    n = len(s)
    i = 0
    start = 0
    while i < n:
        if s[i] == '\x0e':
            if i > start:
                out.append(('text', s[start:i]))
            e = tag_end(s, i)
            out.append(('tag', s[i:e]))
            i = e
            start = i
        else:
            i += 1
    if start < n:
        out.append(('text', s[start:n]))

    # Lưới an toàn: tách tiếp mọi ký tự điều khiển còn sót trong đoạn văn thành token riêng
    safe = []
    for kind, t in out:
        if kind == 'tag' or not STRAY.search(t):
            safe.append((kind, t))
            continue
        pos = 0
        for m in STRAY.finditer(t):
            if m.start() > pos:
                safe.append(('text', t[pos:m.start()]))
            safe.append(('tag', m.group(0)))
            pos = m.end()
        if pos < len(t):
            safe.append(('text', t[pos:]))
    return safe


def mask(s):
    """Che thẻ bằng token [[n]]. Trả về (chuỗi_đã_che, danh_sách_thẻ)."""
    parts = split_parts(s)
    tags = []
    buf = []
    for kind, t in parts:
        if kind == 'tag':
            idx = len(tags)
            tags.append(t)
            buf.append(f'[[{idx}]]')
        else:
            buf.append(t)
    return ''.join(buf), tags


TOKEN_RE = re.compile(r'\[\[(\d+)\]\]')


def unmask(masked, tags):
    """Khôi phục token về thẻ gốc."""
    def rep(m):
        i = int(m.group(1))
        if i >= len(tags):
            raise ValueError(f'token [[{i}]] vượt phạm vi {len(tags)}')
        return tags[i]
    return TOKEN_RE.sub(rep, masked)


def text_segments(s):
    return [t for k, t in split_parts(s) if k == 'text']


if __name__ == '__main__':
    import os, json, glob, collections
    sys.stdout.reconfigure(encoding='utf-8')
    ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    RAW = os.path.join(ROOT, 'games', '0100F2C0115B6000_ZeldaTotK', 'source', 'raw_text')
    mode = sys.argv[1] if len(sys.argv) > 1 else 'check'

    if mode == 'check':
        bad_leftover = []
        n_str = n_tag = n_tok = 0
        for f in sorted(glob.glob(os.path.join(RAW, '*.json'))):
            d = json.load(open(f, encoding='utf-8'))
            for k, v in d.items():
                if not isinstance(v, str):
                    continue
                n_str += 1
                parts = split_parts(v)
                n_tag += sum(1 for x, _ in parts if x == 'tag')
                for kind, t in parts:
                    if kind == 'text' and CTRL.search(t):
                        bad_leftover.append((os.path.basename(f), k, repr(t[:60])))
                m, tags = mask(v)
                if unmask(m, tags) != v:
                    print('ROUNDTRIP FAIL', k)
                    break
        print(f'strings={n_str} tags={n_tag} leftover_ctrl_in_text={len(bad_leftover)}')
        for x in bad_leftover[:20]:
            print('   ', x)
