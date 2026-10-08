"""zs_util.py — nen .zs KHOP tham so frame cua file goc (Nintendo).

Quan trong: file .zs goc cua Nintendo dung windowLog co dinh (vd 21 = 2 MB).
Neu nen lai bang tham so mac dinh (windowLog 22+), decoder cua game co the TU CHOI
frame -> game crash / bao loi software.

Dung:
    from zs_util import compress_like, frame_params
    out = compress_like(orig_zs_bytes, new_raw_bytes)
"""
import struct
import sys

import zstandard


def frame_params(zs_bytes: bytes) -> dict:
    """Doc tham so frame zstd tu file .zs goc."""
    if zs_bytes[:4] != b'\x28\xb5\x2f\xfd':
        raise ValueError('khong phai frame zstd')
    fhd = zs_bytes[4]
    dict_id_flag = fhd & 3
    checksum = bool((fhd >> 2) & 1)
    single_seg = bool((fhd >> 5) & 1)
    pos = 5
    if not single_seg:
        wd = zs_bytes[pos]
        pos += 1
        window_log = 10 + (wd >> 3)
        window_base = 1 << (10 + (wd >> 3))
        mantissa = window_base + (window_base // 8) * (wd & 7)
    else:
        window_log = None
        mantissa = None
    # FCS
    fcs_size = 0
    fcs = (fhd >> 6) & 1
    if fcs:
        if single_seg:
            fcs_size = 1
        elif window_log is not None:
            fcs_size = 1 if (wd & 7) == 0 else 2
        else:
            fcs_size = 1
    pos += fcs_size
    if dict_id_flag == 1:
        pos += 1
    elif dict_id_flag == 2:
        pos += 2
    elif dict_id_flag == 3:
        pos += 4
    return dict(window_log=window_log, window_mantissa=mantissa, single_seg=single_seg,
                checksum=checksum, header_len=pos, fhd=fhd)


def compress_like(orig_zs: bytes, new_raw: bytes, level: int = None) -> bytes:
    """Nen new_raw bang tham so CUA FILE GOC (window_log, checksum...)."""
    p = frame_params(orig_zs)
    wl = p['window_log'] or 21
    write_checksum = p['checksum']
    lvl = level if level is not None else 15
    params = zstandard.ZstdCompressionParameters.from_level(
        lvl, window_log=wl, write_checksum=int(write_checksum),
        write_content_size=1, format=zstandard.FORMAT_ZSTD1)
    return zstandard.ZstdCompressor(compression_params=params).compress(new_raw)


if __name__ == '__main__':
    sys.stdout.reconfigure(encoding='utf-8')
    for p in sys.argv[1:]:
        b = open(p, 'rb').read()
        print(p, frame_params(b))
