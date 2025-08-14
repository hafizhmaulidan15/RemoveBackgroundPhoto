# remove_bg_batch.py — CPU only, fresh output, no-emoji prints

import os, sys, subprocess, importlib.util, shutil
from pathlib import Path

# ====== KONFIGURASI ======
INPUT_DIR  = r"....\Folder gambar" #Masukan alamat folder yang berisikan foto yang ingin di hapus backgoundnya, copy aja folder path
OUTPUT_DIR = r"....\Folder gambar\hasil_remove_bg" #Ini folder untuk outputnya
ALLOWED_EXT = {".jpg", ".jpeg", ".png", ".bmp", ".JPG", ".JPEG", ".PNG", ".BMP"}
MAX_SIDE = 3000  # kecilkan (mis. 2048) kalau mau lebih cepat/hemat RAM

def ensure(pkg, pipname=None):
    pipname = pipname or pkg
    if importlib.util.find_spec(pkg) is None:
        print(f"Installing {pipname} ...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", pipname])

# Dependensi CPU
ensure("PIL", "pillow")
ensure("onnxruntime")
ensure("rembg")

from PIL import Image, ImageOps
from rembg import remove

inp = Path(INPUT_DIR)
outp = Path(OUTPUT_DIR)

if not inp.exists():
    raise FileNotFoundError(f"Folder input tidak ditemukan: {inp}")

# Bersihkan output -> hanya hasil baru
if outp.exists():
    shutil.rmtree(outp)
outp.mkdir(parents=True, exist_ok=True)

files = [p for p in inp.iterdir() if p.is_file() and p.suffix in ALLOWED_EXT]
if not files:
    print("Tidak ada file gambar cocok di folder input.")
    sys.exit(1)

print(f"Memproses {len(files)} file")
print(f"Input : {inp}")
print(f"Output: {outp}\n")

ok = fail = 0
for f in files:
    try:
        with Image.open(f) as im:
            im = ImageOps.exif_transpose(im)
            if max(im.size) > MAX_SIDE:
                im.thumbnail((MAX_SIDE, MAX_SIDE))
            out = remove(im)
            out_path = outp / (f.stem + "_nobg.png")
            out.save(out_path)
        ok += 1
        print(f"OK  - {f.name} -> {out_path.name}")
    except Exception as e:
        fail += 1
        print(f"FAIL- {f.name}: {e}")

print(f"\nSelesai. Berhasil: {ok} | Gagal: {fail}")
print(f"Hasil di: {outp}")
