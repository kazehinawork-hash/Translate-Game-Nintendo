"""
Bộ công cụ patch font XNB Version 7 HOÀN HẢO cho Hades II (Nintendo Switch).
TÍNH NĂNG ĐỘT PHÁ V7:
1. ĐỒNG BỘ 100% TOÀN BỘ KÝ TỰ TIẾNG VIỆT (OVERWRITE TẤT CẢ GLYPHS TIẾNG VIỆT):
   Ghi đè cả các ký tự 1 dấu có sẵn của game (á, à, ã, é, è, ó, ò, ú, ù, đ...)
   lẫn các ký tự 2 dấu và dấu nặng (ấ, ầ, ể, ệ, ố, ồ, ớ, ợ, ứ, ự, ạ, ẹ, ị, ọ, ụ)
   vào cùng một bộ glyphs mới render từ Lato-Bold / TTF đồng nhất.
   -> Triệt tiêu 100% hiện tượng "lạc quẻ / cọc cạch / 2 font khác nhau".
2. BÙ TRỪ HORIZONTAL BEARING (CROP_X) VÀ BASELINE GỐC (BASE STEM ALIGNMENT):
   - Crop.X bù trừ đúng độ nhô dấu sang trái (ch_bb[0] - base_bb[0]), triệt tiêu hiện tượng đè chữ (như ầ đè vào r).
   - Crop.Y căn chỉnh theo đúng chân thân chữ cơ sở của game (base_orig_bottom), đảm bảo chữ có dấu nặng (. dưới chân)
     hoặc dấu mũ trên đầu vẫn giữ nguyên độ cao thân chữ thẳng hàng tăm tắp với các chữ cái không dấu xung quanh.
3. KẾ THỪA KERNING & ADVANCE CHUẨN XÁC TỪ KÝ TỰ GỐC:
   Giữ nguyên độ giãn cách chữ tự nhiên của font gốc trong Hades 2.
"""
import os
import sys
import struct
import unicodedata
from PIL import Image, ImageFont, ImageDraw

if sys.stdout.encoding.lower() != 'utf-8':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

VIETNAMESE_LOWER = (
    "áàảãạăắằẳẵặâấầẩẫậ"
    "éèẻẽẹêếềểễệ"
    "íìỉĩị"
    "óòỏõọôốồổỗộơớờởỡợ"
    "úùủũụưứừửữự"
    "ýỳỷỹỵ"
    "đ"
)

VIETNAMESE_UPPER = (
    "ÁÀẢÃẠĂẮẰẲẴẶÂẤẦẨẪẬ"
    "ÉÈẺẼẸÊẾỀỂỄỆ"
    "ÍÌỈĨỊ"
    "ÓÒỎÕỌÔỐỒỔỖỘƠỚỜỞỠỢ"
    "ÚÙỦŨỤƯỨỪỬỮỰ"
    "ÝỲỶỸỴ"
    "Đ"
)

VIETNAMESE_ALL = VIETNAMESE_LOWER + VIETNAMESE_UPPER

# Bộ ký tự chuẩn đồng bộ 100%: Bao gồm toàn bộ chữ Latin cơ bản và tiếng Việt
# Nhờ vậy, chữ không dấu lẫn chữ có dấu đều render từ cùng 1 font Be Vietnam Pro
ALL_SYNC_CHARS = (
    "abcdefghijklmnopqrstuvwxyz"
    "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    + VIETNAMESE_ALL
)

def get_base_char(ch: str) -> str:
    if ch in "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ":
        return ch
    if ch == 'đ': return 'd'
    if ch == 'Đ': return 'D'
    d = unicodedata.decomposition(ch)
    if d:
        base = chr(int(d.split()[0], 16))
        d2 = unicodedata.decomposition(base)
        if d2:
            base = chr(int(d2.split()[0], 16))
        return base
    return ch

def encode_7bit(val: int) -> bytes:
    res = bytearray()
    while True:
        b = val & 0x7F
        val >>= 7
        if val > 0:
            res.append(b | 0x80)
        else:
            res.append(b)
            break
    return bytes(res)

def read_7bit(buf, offset):
    res = 0
    shift = 0
    while True:
        b = buf[offset]
        offset += 1
        res |= (b & 0x7F) << shift
        if (b & 0x80) == 0:
            break
        shift += 7
    return res, offset

def calibrate_font_size(ttf_path: str, target_h: int, test_char: str) -> int:
    """Tìm font size TTF sao cho chiều cao glyph thực tế khớp chính xác target_h."""
    best_sz = 10
    best_diff = 999
    for sz in range(10, 160):
        f = ImageFont.truetype(ttf_path, sz)
        b = f.getbbox(test_char)
        h = b[3] - b[1]
        diff = abs(h - target_h)
        if diff < best_diff:
            best_diff = diff
            best_sz = sz
        if diff == 0:
            break
    return best_sz

def patch_xnb_font(orig_xnb_path: str, ttf_font_path: str, out_xnb_path: str, stroke_width: int = 0):
    font_name = os.path.basename(orig_xnb_path)
    is_smallcaps = "SC" in font_name
    print(f"\n>>> Đang xử lý font: {font_name} (SmallCaps={is_smallcaps}, stroke_width={stroke_width})")

    with open(orig_xnb_path, 'rb') as f:
        data = f.read()

    orig_file_size, = struct.unpack_from('<I', data, 6)
    fmt, width, height, mipmaps, data_len = struct.unpack_from('<IIIII', data, 10)
    pixel_data = data[30 : 30 + data_len]
    pos = 30 + data_len

    num_glyphs, pos = read_7bit(data, pos)
    glyphs_boxes = [struct.unpack_from('<iiii', data, pos + i*16) for i in range(num_glyphs)]
    pos += num_glyphs * 16

    num_crop, pos = read_7bit(data, pos)
    crops = [struct.unpack_from('<iiii', data, pos + i*16) for i in range(num_crop)]
    pos += num_crop * 16

    std_crop_h = crops[0][3]

    num_chars, pos = read_7bit(data, pos)
    chars = []
    for _ in range(num_chars):
        b0 = data[pos]
        if b0 < 0x80: c_len = 1
        elif (b0 & 0xE0) == 0xC0: c_len = 2
        elif (b0 & 0xF0) == 0xE0: c_len = 3
        else: c_len = 4
        c = data[pos : pos + c_len].decode('utf-8')
        pos += c_len
        chars.append(c)

    other_data = data[pos : pos + 12]
    line_spacing, = struct.unpack_from('<i', other_data, 0)
    spacing, = struct.unpack_from('<f', other_data, 4)
    font_size, = struct.unpack_from('<i', other_data, 8)
    pos += 12

    num_kern, pos = read_7bit(data, pos)
    kerns = [struct.unpack_from('<fff', data, pos + i*12) for i in range(num_kern)]
    pos += num_kern * 12

    default_char_bytes = data[pos:]

    # 1. Đo chiều cao tham chiếu từ các glyph gốc của game
    c_idx = chars.index('C') if 'C' in chars else (chars.index('A') if 'A' in chars else 0)
    ref_cap_h = glyphs_boxes[c_idx][3]

    o_idx = chars.index('o') if 'o' in chars else None
    ref_lower_h = glyphs_boxes[o_idx][3] if o_idx is not None else ref_cap_h

    # 2. Hiệu chuẩn font size cho TTF
    upper_sz = calibrate_font_size(ttf_font_path, ref_cap_h, 'C')
    lower_sz = calibrate_font_size(ttf_font_path, ref_lower_h, 'C' if is_smallcaps else 'o')

    ttf_font_upper = ImageFont.truetype(ttf_font_path, upper_sz)
    ttf_font_lower = ImageFont.truetype(ttf_font_path, lower_sz)

    print(f" - std_crop_h={std_crop_h}")
    print(f" - Hiệu chuẩn font size: Upper={upper_sz} (target_h={ref_cap_h}), Lower={lower_sz} (target_h={ref_lower_h})")

    # Mở rộng canvas texture bên dưới để vẽ toàn bộ ký tự Latin & tiếng Việt mới đồng bộ
    # Cần diện tích cho khoảng 228 ký tự x 35px chiều cao = ~7-9 dòng
    extra_height = (max(upper_sz, lower_sz) + 25) * 12
    new_height = height + extra_height
    orig_img = Image.frombytes('L', (width, height), pixel_data)
    new_img = Image.new('L', (width, new_height), 0)
    new_img.paste(orig_img, (0, 0))

    draw = ImageDraw.Draw(new_img)

    cur_x = 2
    cur_y = height + 2
    row_height = max(upper_sz, lower_sz) + 20

    new_glyphs_boxes = list(glyphs_boxes)
    new_crops = list(crops)
    new_chars = list(chars)
    new_kerns = list(kerns)

    # Toàn bộ danh sách ký tự Latin & tiếng Việt cần render đồng nhất từ font Be Vietnam Pro
    chars_to_render = list(ALL_SYNC_CHARS)

    for ch in chars_to_render:
        is_upper = ch in VIETNAMESE_UPPER or (ch.isupper() and ch.isalpha())

        # Chọn font và ký tự vẽ:
        if is_smallcaps and not is_upper:
            draw_char = ch.upper()
            curr_font = ttf_font_lower
        elif is_upper:
            draw_char = ch
            curr_font = ttf_font_upper
        else:
            draw_char = ch
            curr_font = ttf_font_lower

        curr_stroke = stroke_width
        ch_bb = curr_font.getbbox(draw_char, stroke_width=curr_stroke)
        char_w = ch_bb[2] - ch_bb[0]
        char_h = ch_bb[3] - ch_bb[1]

        if char_w <= 0: char_w = upper_sz // 3
        if char_h <= 0: char_h = upper_sz

        glyph_w = char_w + 2
        glyph_h = char_h + 2

        if cur_x + glyph_w >= width - 2:
            cur_x = 2
            cur_y += row_height

        # Vẽ ký tự sát lề vào texture
        draw.text((cur_x - ch_bb[0] + 1, cur_y - ch_bb[1] + 1), draw_char, fill=255, font=curr_font, stroke_width=curr_stroke, stroke_fill=255)

        # 1. Glyphs Box (x, y, w, h trong texture)
        glyph_box = (cur_x, cur_y, glyph_w, glyph_h)

        # 2. Tìm ký tự cơ sở trong font gốc
        base_c = get_base_char(ch)
        if is_smallcaps and not is_upper:
            base_cand = base_c.lower() if base_c.lower() in chars else (base_c.upper() if base_c.upper() in chars else None)
        else:
            base_cand = base_c if base_c in chars else (base_c.lower() if base_c.lower() in chars else None)

        base_idx = chars.index(base_cand) if base_cand is not None else None

        # 3. Tính toán Crop chuẩn xác:
        # Lấy bbox ký tự cơ sở trong TTF để căn chân thân chữ (baseline stem)
        base_draw_char = base_c.upper() if (is_smallcaps or is_upper) else base_c
        base_bb = curr_font.getbbox(base_draw_char, stroke_width=curr_stroke)

        if base_idx is not None:
            base_orig_bottom = crops[base_idx][1] + glyphs_boxes[base_idx][3]
            base_crop_w = crops[base_idx][2]
            base_kern = kerns[base_idx]
        else:
            base_orig_bottom = crops[0][1] + glyphs_boxes[0][3]
            base_crop_w = max(1, glyph_w - 1)
            base_kern = (1.5, float(char_w), 1.5)

        # Crop X: Bù trừ chính xác độ nhô của dấu sang trái (ví dụ dấu huyền trong 'ầ')
        # Thân chữ bắt đầu ở 1 + (base_bb[0] - ch_bb[0]) trong ô glyph. Để thân chữ bắt đầu tại pos.X:
        crop_x = (ch_bb[0] - base_bb[0]) - 1

        # Crop Y: Căn chân thân chữ của ký tự có dấu khớp 100% với chân thân chữ gốc của game!
        # Thân chữ (base stem) ở vị trí base_bb[3]. Đáy glyph có dấu là ch_bb[3].
        # Khi vẽ vào game: glyph_top = baseline + crop_y.
        # Với 1px padding trên, thân chữ tiếp đất ở: glyph_top + 1 + (base_bb[3] - ch_bb[1]).
        # Để thân chữ tiếp đất chính xác tại base_orig_bottom:
        # crop_y = base_orig_bottom - (base_bb[3] - ch_bb[1]) - 1
        crop_y = base_orig_bottom - (base_bb[3] - ch_bb[1]) - 1

        crop_rect = (crop_x, crop_y, base_crop_w, std_crop_h)

        # 4. Kerning: Giữ nguyên kerning chuẩn từ ký tự cơ sở của game
        # Để đảm bảo khoảng cách dòng chảy giữa các chữ cái hoàn hảo
        glyph_kern = base_kern

        # Nếu ký tự đã có trong mảng chars gốc (như á, à, é...), ta GHI ĐÈ
        # Nếu chưa có, ta APPEND
        if ch in chars:
            idx = chars.index(ch)
            new_glyphs_boxes[idx] = glyph_box
            new_crops[idx] = crop_rect
            new_kerns[idx] = glyph_kern
        else:
            new_glyphs_boxes.append(glyph_box)
            new_crops.append(crop_rect)
            new_chars.append(ch)
            new_kerns.append(glyph_kern)

        cur_x += glyph_w + 3

    # Ghép lại XNB Version 6
    new_pixel_bytes = new_img.tobytes()
    new_data_len = len(new_pixel_bytes)
    total_glyphs = len(new_chars)
    glyphs_num_encoded = encode_7bit(total_glyphs)

    out_body = bytearray()
    out_body.extend(struct.pack('<IIIII', fmt, width, new_height, mipmaps, new_data_len))
    out_body.extend(new_pixel_bytes)

    out_body.extend(glyphs_num_encoded)
    for b in new_glyphs_boxes: out_body.extend(struct.pack('<iiii', *b))

    out_body.extend(glyphs_num_encoded)
    for c in new_crops: out_body.extend(struct.pack('<iiii', *c))

    out_body.extend(glyphs_num_encoded)
    for c in new_chars: out_body.extend(c.encode('utf-8'))

    out_body.extend(other_data)

    out_body.extend(glyphs_num_encoded)
    for k in new_kerns: out_body.extend(struct.pack('<fff', *k))

    out_body.extend(default_char_bytes)

    total_file_size = 10 + len(out_body)
    header = bytearray(b'XNBw\x06\x00')
    header.extend(struct.pack('<I', total_file_size))

    full_output = header + out_body

    os.makedirs(os.path.dirname(out_xnb_path), exist_ok=True)
    with open(out_xnb_path, 'wb') as f:
        f.write(full_output)

    print(f"✅ Hoàn tất font {font_name} (Tổng {total_glyphs} glyphs đồng bộ)")

if __name__ == '__main__':
    orig_base = "games/0100A00019DE0000_Hades2/source/orig_font/bin"
    out_base = "output/atmosphere/contents/0100A00019DE0000/romfs/Fonts/bin"

    # Bộ Font Thuần Việt Cao Cấp: Be Vietnam Pro (Được thiết kế chuẩn mực 100% cho tiếng Việt)
    font_bold_ttf = "tools/fonts_hades2/vietnam/BeVietnamPro-Bold.ttf"
    font_semi_ttf = "tools/fonts_hades2/vietnam/BeVietnamPro-SemiBold.ttf"
    font_med_ttf = "tools/fonts_hades2/vietnam/BeVietnamPro-Medium.ttf"
    font_reg_ttf = "tools/fonts_hades2/vietnam/BeVietnamPro-Regular.ttf"
    font_italic_ttf = "tools/fonts_hades2/vietnam/BeVietnamPro-Italic.ttf"
    font_bold_italic_ttf = "tools/fonts_hades2/vietnam/BeVietnamPro-BoldItalic.ttf"
    font_semi_italic_ttf = "tools/fonts_hades2/vietnam/BeVietnamPro-SemiBoldItalic.ttf"

    font_caesar_ttf = "tools/fonts_hades2/CaesarDressing-Regular.ttf"
    font_spectral_reg_ttf = "tools/fonts_hades2/Spectral-Regular.ttf"
    font_spectral_med_ttf = "tools/fonts_hades2/Spectral-Medium.ttf"
    font_spectral_semi_ttf = "tools/fonts_hades2/Spectral-SemiBold.ttf"
    font_p22_ttf = "tools/Nunito-Black.ttf"

    tasks = [
        # P22 Underground (Menu chính & Profiles - Dùng Nunito chuẩn)
        ("en/P22UndergroundSCHeavy.xnb", font_p22_ttf, 0),
        ("720p/en/P22UndergroundSCHeavy.xnb", font_p22_ttf, 0),
        ("en/P22UndergroundSCMedium.xnb", font_p22_ttf, 0),
        ("720p/en/P22UndergroundSCMedium.xnb", font_p22_ttf, 0),

        # Lato Regular & Bold (Đối thoại nhân vật & UI - Dùng Be Vietnam Pro đồng bộ tuyệt đối)
        ("en/LatoBold.xnb", font_bold_ttf, 0),
        ("720p/en/LatoBold.xnb", font_bold_ttf, 0),
        ("en/LatoMedium.xnb", font_med_ttf, 0),
        ("720p/en/LatoMedium.xnb", font_med_ttf, 0),
        ("en/LatoSemibold.xnb", font_semi_ttf, 0),
        ("720p/en/LatoSemibold.xnb", font_semi_ttf, 0),
        ("en/LatoBold64.xnb", font_bold_ttf, 0),
        ("720p/en/LatoBold64.xnb", font_bold_ttf, 0),

        # Lato Italic & BoldItalic
        ("en/LatoBoldItalic.xnb", font_bold_italic_ttf, 0),
        ("720p/en/LatoBoldItalic.xnb", font_bold_italic_ttf, 0),
        ("en/LatoSemiboldItalic.xnb", font_semi_italic_ttf, 0),
        ("720p/en/LatoSemiboldItalic.xnb", font_semi_italic_ttf, 0),
        ("en/LatoItalic.xnb", font_italic_ttf, 0),
        ("720p/en/LatoItalic.xnb", font_italic_ttf, 0),

        # Caesar Dressing (Tên người nói / Tiêu đề)
        ("en/CaesarDressing.xnb", font_caesar_ttf, 0),
        ("720p/en/CaesarDressing.xnb", font_caesar_ttf, 0),

        # Spectral (Dẫn chuyện / Subtitle banner)
        ("en/SpectralSCMedium.xnb", font_spectral_semi_ttf, 0),
        ("720p/en/SpectralSCMedium.xnb", font_spectral_semi_ttf, 0),
        ("en/SpectralSCLight.xnb", font_spectral_med_ttf, 0),
        ("720p/en/SpectralSCLight.xnb", font_spectral_med_ttf, 0),
        ("en/SpectralSCExtraLight.xnb", font_spectral_reg_ttf, 0),
        ("720p/en/SpectralSCExtraLight.xnb", font_spectral_reg_ttf, 0),

        # P22 Light
        ("en/P22UndergroundSCLight.xnb", font_p22_ttf, 0),
        ("720p/en/P22UndergroundSCLight.xnb", font_p22_ttf, 0),

        # Noto Sans / Monospace
        ("en/NotoSansMedium.xnb", font_med_ttf, 0),
        ("720p/en/NotoSansMedium.xnb", font_med_ttf, 0),
        ("en/MonospaceTypewriterBold.xnb", font_bold_ttf, 0),
        ("720p/en/MonospaceTypewriterBold.xnb", font_bold_ttf, 0),
        ("en/MonospaceNumericP22UndergroundSCMedium.xnb", font_p22_ttf, 0),
        ("720p/en/MonospaceNumericP22UndergroundSCMedium.xnb", font_p22_ttf, 0),
    ]

    for item in tasks:
        rel_path = item[0]
        ttf = item[1]
        stroke = item[2] if len(item) > 2 else 0
        in_p = os.path.join(orig_base, rel_path)
        out_p = os.path.join(out_base, rel_path)
        if os.path.exists(in_p):
            patch_xnb_font(in_p, ttf, out_p, stroke_width=stroke)
