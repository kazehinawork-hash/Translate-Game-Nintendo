"""
build_patch_pak.py — Tạo patch pak UE4 cho mod dịch Hogwarts Legacy.

Vì file `Phoenix/Content/Localization/SWITCH/*.bin` của game nằm BÊN TRONG
pakchunk0-Switch.pak (UFS), file .bin đặt rời trong LayeredFS sẽ bị bỏ qua.
Cách đúng: đóng gói chúng thành patch pak `pakchunk0-Switch_p.pak`
(UE mount pak patch SAU pak gốc nên sẽ ghi đè).

Cách dùng (chạy từ gốc dự án):
    python tools/build_patch_pak.py

Đầu vào : output/atmosphere/contents/0100F7E00C70E000/romfs/Phoenix/Content/Localization/SWITCH/
Đầu ra  : output/atmosphere/contents/0100F7E00C70E000/romfs/Phoenix/Content/Paks/pakchunk0-Switch_p.pak

Yêu cầu: `pip install repak`
"""
import os
import sys

sys.stdout.reconfigure(encoding='utf-8')
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
import repak  # noqa: E402

TITLE = '0100F7E00C70E000'
MOD = os.path.join(ROOT, 'output', 'atmosphere', 'contents', TITLE, 'romfs')
SRC = os.path.join(MOD, 'Phoenix', 'Content', 'Localization', 'SWITCH')
OUTDIR = os.path.join(MOD, 'Phoenix', 'Content', 'Paks')

# Toàn bộ ngôn ngữ mà game Hogwarts Legacy (Switch) phát hành
LANGS = ['arAE', 'deDE', 'enUS', 'esES', 'esMX', 'frFR', 'itIT', 'jaJP',
         'koKR', 'plPL', 'ptBR', 'ruRU', 'zhCN', 'zhTW']


def main():
    main_bytes = open(os.path.join(SRC, 'MAIN-enUS.bin'), 'rb').read()
    sub_bytes = open(os.path.join(SRC, 'SUB-enUS.bin'), 'rb').read()
    print(f'MAIN={len(main_bytes)} bytes  SUB={len(sub_bytes)} bytes')

    os.makedirs(OUTDIR, exist_ok=True)
    pak_path = os.path.join(OUTDIR, 'pakchunk0-Switch_p.pak')
    builder = repak.PakBuilder().compression([repak.Compression.ZLIB])
    with builder.writer(pak_path, version=repak.Version.V11, mount_point='../../../') as w:
        for lang in LANGS:
            w.write_file(f'Phoenix/Content/Localization/SWITCH/MAIN-{lang}.bin', main_bytes)
            w.write_file(f'Phoenix/Content/Localization/SWITCH/SUB-{lang}.bin', sub_bytes)
    print(f'Da ghi: {pak_path} ({os.path.getsize(pak_path)} bytes)')

    r = repak.PakBuilder().reader(pak_path)
    ok = r.get('Phoenix/Content/Localization/SWITCH/MAIN-enUS.bin') == main_bytes
    print(f'Verify: {len(r.entries())} entry | version={r.version} | mount={r.mount_point!r} | roundtrip={"OK" if ok else "FAIL"}')


if __name__ == '__main__':
    main()
