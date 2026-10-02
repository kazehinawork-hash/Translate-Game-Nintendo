"""
unity_bitmapfont.py — Giải mã & phân tích **BitmapFont** của Moon Studios (Ori and the Blind Forest).

ĐỊNH DẠNG ĐÃ GIẢI MÃ (kiểm chứng bằng ảnh cắt từ atlas: A a i x g j W ~ m b đều đúng):

    MonoScript class "BitmapFont" -> các MonoBehaviour font (candara, msPGothic, nyala, ...)
    Raw của font:
        [0..12]   12 byte 0
        [12]      int32 (1)         (không rõ)
        [16]      int32 (1)
        [20]      int64  m_Script PPtr (trỏ MonoScript BitmapFont)
        [28]      int32  nameLen
        [32]      name (utf-8)
        [align 4] BLOCK 1: int32 count, rồi `count` entry 48 byte
        ...       BLOCK 2, 3, ... cùng dạng
        [cuối]    vài float metric (line height / ascent / descent...)

    Mỗi ENTRY 48 byte = [int32 mã ký tự] + [11 float]:
        f[0], f[1] = u0, u1   (toạ độ ngang, normalized 0..1)
        f[2], f[3] = v0, v1   (toạ độ dọc, GỐC DƯỚI — phải lật: y_px = (1 - v) * height)
        f[4]       = độ lệch ngang (bearing), âm = nhô trái
        f[5..8]    = "quad" lấy mẫu SDF (chưa chốt công thức — sẽ đối chiếu thêm)
        f[9], f[10]= 0

    ATLAS = Texture2D tên `<tên font>_0 distance map`, định dạng Alpha8 (fmt=1);
            giá trị nằm ở KÊNH ALPHA (khi decode ra RGBA thì Alpha mới là dữ liệu).
            Bảng mã + atlas được engine ghép theo TÊN lúc chạy (Material font có _MainTex = null).

KIỂM CHỨNG: `python tools/unity_bitmapfont.py <bundle> candara <thư_mục_ra>` sẽ cắt thử
vài glyph ra ảnh để mắt thường đối chiếu.
"""
import os
import struct
import sys

sys.stdout.reconfigure(encoding='utf-8')
u32 = lambda b, i: int.from_bytes(b[i:i+4], 'little')
u64 = lambda b, i: int.from_bytes(b[i:i+8], 'little')
f32 = lambda b, i: struct.unpack_from('<f', b, i)[0]


def find_fonts(bundle_path):
    """Trả [(path_id, tên font, raw)] của mọi MonoBehaviour thuộc class BitmapFont."""
    import UnityPy
    env = UnityPy.load(bundle_path)
    bid = None
    for o in env.objects:
        if o.type.name == 'MonoScript':
            try:
                if (getattr(o.read(), 'm_ClassName', '') or '') == 'BitmapFont':
                    bid = o.path_id
            except Exception:
                pass
    out = []
    for o in env.objects:
        if o.type.name != 'MonoBehaviour':
            continue
        raw = o.get_raw_data()
        if len(raw) < 60 or u64(raw, 20) != bid:
            continue
        nlen = u32(raw, 28)
        out.append((o.path_id, raw[32:32 + nlen].decode('utf-8', 'replace'), raw))
    return out, env


def parse_glyphs(raw):
    """Trả {mã ký tự: 11 float} + danh sách block."""
    glyphs, blocks = {}, []
    pos = 40
    while pos + 4 <= len(raw):
        if pos == 40 + 4:
            pass
        cnt = u32(raw, pos)
        if not (0 < cnt < 5000) or pos + 4 + cnt * 48 > len(raw) + 4:
            break
        blocks.append((pos, cnt))
        for k in range(cnt):
            off = pos + 4 + k * 48
            c = u32(raw, off)
            glyphs[c] = [f32(raw, off + 4 + j * 4) for j in range(11)]
        pos += 4 + cnt * 48
    return glyphs, blocks


def rect_px(f, width, height):
    """Đổi 4 float đầu thành hình chữ nhật pixel (đã lật trục dọc)."""
    xa, xb = int(f[0] * width), int(f[1] * width)
    ya, yb = int((1 - f[3]) * height), int((1 - f[2]) * height)
    return xa, xb, ya, yb


def decode_atlas(env, font_name):
    """Trả (mảng numpy Alpha8, width, height, đối tượng Texture2D)."""
    import numpy as np
    want = f'{font_name}_0 distance map'
    for o in env.objects:
        if o.type.name != 'Texture2D':
            continue
        d = o.read()
        if str(getattr(d, 'm_Name', '')) == want:
            arr = np.array(d.image)
            alpha = arr[:, :, 3] if arr.ndim == 3 else arr
            return alpha, d.m_Width, d.m_Height, o
    raise LookupError(f'không thấy atlas {want!r}')


def main():
    if len(sys.argv) < 4:
        print(__doc__)
        return 1
    bundle, font, outdir = sys.argv[1], sys.argv[2], sys.argv[3]
    os.makedirs(outdir, exist_ok=True)
    fonts, env = find_fonts(bundle)
    print('Font trong bundle:', [(p, n) for p, n, _ in fonts])
    raw = next(r for p, n, r in fonts if n == font)
    glyphs, blocks = parse_glyphs(raw)
    print(f'{font}: {len(glyphs)} glyph | block: {blocks}')

    from PIL import Image
    A, W, H, tex = decode_atlas(env, font)
    print(f'atlas {W}x{H} | pixel có mực: {(A > 8).sum()}')

    VN = 'ẠạẢảẤấẦầẨẩẫẬậẮắằẳẵẶặẻẼẽẾếỀềỂểỄễỆệỉịỌọỎỏỐốỒồỔổỗỘộỚớỜờỞởỡỢợỤụỦủỨứỪừỬửữỰựỳỷỸỹ'
    miss = [c for c in VN if ord(c) not in glyphs]
    print(f'ký tự tiếng Việt còn thiếu: {len(miss)} -> {"".join(miss[:40])}')

    # cắt vài glyph ra ảnh để kiểm chứng
    strip = []
    for ch in 'AaixgjW~mb':
        if ord(ch) not in glyphs:
            continue
        xa, xb, ya, yb = rect_px(glyphs[ord(ch)], W, H)
        crop = A[ya:yb, xa:xb]
        if crop.size == 0:
            continue
        im = Image.fromarray(crop)
        im = im.resize((im.width * 3 + 1, im.height * 3 + 1), Image.NEAREST)
        strip.append(im)
    if strip:
        Hh = max(i.height for i in strip) + 8
        canvas = Image.new('L', (sum(i.width + 12 for i in strip), Hh), 0)
        x = 0
        for im in strip:
            canvas.paste(im, (x, 4))
            x += im.width + 12
        p = os.path.join(outdir, f'STRIP_{font}.png')
        canvas.save(p)
        print('đã lưu ảnh kiểm chứng:', p)
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
