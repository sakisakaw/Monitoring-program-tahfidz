# Monitoring Hafalan — Web App

Web kalkulator responsif berbasis Flask. Tidak menggunakan database dan tidak menyimpan data santri.

## Menjalankan di komputer sendiri

1. Install Python.
2. Buka terminal di folder proyek.
3. Buat virtual environment (opsional):
   `python -m venv .venv`
4. Aktifkan environment:
   - Windows PowerShell: `.venv\\Scripts\\Activate.ps1`
   - macOS/Linux: `source .venv/bin/activate`
5. Install kebutuhan:
   `pip install -r requirements.txt`
6. Jalankan:
   `python app.py`
7. Buka `http://127.0.0.1:5000` di browser.

## Hosting gratis di Render

1. Upload folder proyek ini ke repository GitHub.
2. Buat akun Render dan pilih **New > Web Service**.
3. Hubungkan repository GitHub.
4. Build Command: `pip install -r requirements.txt`
5. Start Command: `gunicorn app:app`
6. Deploy. Render akan memberikan URL publik.

## Privasi

- Tidak ada database atau fitur penyimpanan.
- Nama dan halaman dikirim melalui request POST untuk dihitung saat itu saja.
- Aplikasi tidak menuliskan data input ke file.
- Penyedia hosting tetap dapat memproses metadata akses sesuai kebijakan mereka. Jangan masukkan informasi pribadi yang tidak diperlukan.

## Catatan

Konversi tahun, bulan, dan pekan masih menggunakan pendekatan 52 pekan per tahun seperti program awal.
