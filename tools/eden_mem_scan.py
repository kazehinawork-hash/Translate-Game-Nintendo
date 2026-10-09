"""Quet bo nho tien trinh Eden tim chuoi tieng Viet (UTF-16LE).

Cach nay chung minh duoc game CO nap ban dich hay khong, khong can nhin man hinh.
Chay: python tools/eden_mem_scan.py
"""
import ctypes
import ctypes.wintypes as wt
import sys
import unicodedata

sys.stdout.reconfigure(encoding='utf-8')

# chuoi dac trung chi co trong ban dich tieng Viet
NEEDLES = ['Trực tuyến', 'Ghi công', 'Chơi', 'Trợ giúp']
# va mot chuoi tieng Anh goc de doi chieu
ENGLISH = ['Online', 'Credits', 'Help And Options']


def needles_bytes(lst):
    out = []
    for s in lst:
        out.append((s, s.encode('utf-16-le')))
    return out


k32 = ctypes.windll.kernel32
PROCESS_QUERY_INFORMATION = 0x0400
PROCESS_VM_READ = 0x0010
MEM_COMMIT = 0x1000


class MBI(ctypes.Structure):
    _fields_ = [('BaseAddress', ctypes.c_void_p), ('AllocationBase', ctypes.c_void_p),
                ('AllocationProtect', wt.DWORD), ('RegionSize', ctypes.c_size_t),
                ('State', wt.DWORD), ('Protect', wt.DWORD), ('Type', wt.DWORD)]


def find_pid():
    import subprocess
    out = subprocess.run(['tasklist', '/FI', 'IMAGENAME eq eden.exe', '/FO', 'CSV'],
                         capture_output=True, text=True).stdout
    for line in out.splitlines():
        parts = [p.strip('"') for p in line.split('","')]
        if len(parts) >= 2 and parts[0].lower().startswith('eden'):
            return int(parts[1])
    return None


def add_bytes(blob, dst):
    """Cong tung byte (nhan 0-255) vao list 'dst' theo cap 65536 de tron tranh 256."""
    step = 65536
    for i in range(0, len(blob), step):
        for b in blob[i:i + step]:
            dst[b] += 1


def main():
    pid = find_pid()
    if not pid:
        print('  KHONG thay eden.exe dang chay')
        return
    print(f'  eden PID = {pid}')
    h = k32.OpenProcess(PROCESS_QUERY_INFORMATION | PROCESS_VM_READ, False, pid)
    if not h:
        print('  khong mo duoc tien trinh (can quyen):', k32.GetLastError())
        return
    print('  da mo tien trinh, bat dau quet...')

    vi_hits = {s: 0 for s, _ in needles_bytes(NEEDLES)}
    en_hits = {s: 0 for s, _ in needles_bytes(ENGLISH)}
    total = scanned = 0
    addr = 0
    mbi = MBI()
    while k32.VirtualQueryEx(h, ctypes.c_void_p(addr), ctypes.byref(mbi), ctypes.sizeof(mbi)):
        base = mbi.BaseAddress or 0
        size = mbi.RegionSize
        if mbi.State == MEM_COMMIT and size > 0:
            read = min(size, 8 << 20)
            buf = ctypes.create_string_buffer(read)
            got = ctypes.c_size_t(0)
            if k32.ReadProcessMemory(h, ctypes.c_void_p(base), buf, read, ctypes.byref(got)) and got.value > 0:
                data = buf.raw[:got.value]
                scanned += got.value
                for s, nb in needles_bytes(NEEDLES):
                    if nb in data:
                        vi_hits[s] += data.count(nb)
                for s, nb in needles_bytes(ENGLISH):
                    if nb in data:
                        en_hits[s] += data.count(nb)
        nxt = base + size
        if nxt <= addr:
            break
        addr = nxt
        total += 1
        if scanned > (12 << 30):
            break

    k32.CloseHandle(h)
    print(f'  da quet {scanned/1e9:.2f} GB ({total} vung)')
    print('\n  --- chuoi TIENG VIET tim thay ---')
    anyvi = False
    for s, n in vi_hits.items():
        if n:
            anyvi = True
        print(f'    {s!r:<16} x{n}')
    print('  --- chuoi TIENG ANH (goc) ---')
    for s, n in en_hits.items():
        print(f'    {s!r:<22} x{n}')
    print('\n  KET LUAN:', 'GAME CO NAP BAN DICH TIENG VIET' if anyvi else 'khong tim thay chuoi tieng Viet trong bo nho')


main()
