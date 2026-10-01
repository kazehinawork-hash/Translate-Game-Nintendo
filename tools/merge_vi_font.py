"""
merge_vi_font.py — Thêm glyph tiếng Việt vào một TTF có sẵn, GIỮ NGUYÊN toàn bộ glyph gốc.

Dùng cho font vừa chứa chữ vừa chứa icon (PUA) — thay hẳn font sẽ làm mất icon,
nên phải hợp nhất: font gốc + glyph tiếng Việt lấy từ font nguồn (tự scale unitsPerEm).

Dùng:
    from merge_vi_font import merge_vn_font
    merged_bytes = merge_vn_font(ttf_goc_bytes, 'duong/dan/font_tieng_viet.ttf')

    # hoặc CLI
    python tools/merge_vi_font.py <font_goc.ttf> <font_viet.ttf> <font_ra.ttf>
"""
import io
import os
import sys
import tempfile

sys.stdout.reconfigure(encoding='utf-8')
from fontTools.merge import Merger  # noqa: E402
from fontTools.ttLib import TTFont  # noqa: E402
from fontTools.ttLib.scaleUpem import scale_upem  # noqa: E402


def merge_vn_font(base_ttf, vn_ttf_path):
    """Trả về bytes của font gốc + glyph tiếng Việt, đã đồng bộ unitsPerEm."""
    tmp = tempfile.mkdtemp(prefix='mergefont_')
    p_base = os.path.join(tmp, 'base.ttf')
    with open(p_base, 'wb') as f:
        f.write(base_ttf if isinstance(base_ttf, (bytes, bytearray)) else open(base_ttf, 'rb').read())

    base = TTFont(p_base)
    upm = base['head'].unitsPerEm

    lat = TTFont(vn_ttf_path)
    scale_upem(lat, upm)
    p_vn = os.path.join(tmp, 'vn.ttf')
    lat.save(p_vn)

    merged = Merger().merge([p_base, p_vn])
    out = io.BytesIO()
    merged.save(out)
    return out.getvalue()


if __name__ == '__main__':
    if len(sys.argv) < 4:
        print(__doc__)
        raise SystemExit(1)
    data = merge_vn_font(sys.argv[1], sys.argv[2])
    open(sys.argv[3], 'wb').write(data)
    t = TTFont(io.BytesIO(data), lazy=True)
    print(f'OK: {len(data)} bytes, {len(t.getBestCmap())} glyph -> {sys.argv[3]}')
