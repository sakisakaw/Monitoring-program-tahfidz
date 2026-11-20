from flask import Flask, render_template, request, jsonify
import math

app = Flask(__name__)

TOTAL_HALAMAN = 581
TARGET_PEKAN = 32
TANGGAL_TARGET = "4 Juli 2027"


def konversi_waktu(total_pekan):
    tahun = total_pekan // 52
    sisa = total_pekan % 52
    bulan = int(sisa * 12 / 52)
    pekan = round(sisa - (bulan * 52 / 12))
    return tahun, bulan, pekan


def pesan_motivasi(minimal):
    if minimal <= 0:
        return {
            "judul": "Hafalan telah selesai!",
            "pesan": "Anda sudah menyelesaikan hafalan Al-Qur'an 30 juz. Jangan lupa untuk senantiasa memuraja'ahnya.",
            "level": "success"
        }
    if minimal <= 5:
        return {
            "judul": "Sedikit lagi!",
            "pesan": f"Paling lambat minimal menyetorkan {minimal} halaman setiap pekan. Walau tinggal sedikit lagi, jangan kasih kendor!",
            "level": "success"
        }
    if minimal <= 10:
        return {
            "judul": "Tetap semangat!",
            "pesan": f"Paling lambat minimal menyetorkan {minimal} halaman setiap pekan. Tetap semangat, kamu pasti bisa segera khatam sugra!",
            "level": "info"
        }
    if minimal <= 15:
        return {
            "judul": "Tingkatkan kesungguhan!",
            "pesan": f"Harus istiqomah menghafal {minimal} halaman setiap pekan. Lebih serius lagi, maksimalkan waktumu untuk mengejar target!",
            "level": "warning"
        }
    return {
        "judul": "Saatnya berbenah!",
        "pesan": f"Harus istiqomah menghafal {minimal} halaman setiap pekan. Jangan biarkan waktu terus berlalu tanpa perubahan. Tinggalkan alasan, bangun disiplin, dan buktikan kesungguhanmu melalui setoran nyata!",
        "level": "danger"
    }


@app.get("/")
def index():
    return render_template(
        "index.html",
        total_halaman=TOTAL_HALAMAN,
        target_pekan=TARGET_PEKAN,
        tanggal_target=TANGGAL_TARGET
    )


@app.post("/hitung")
def hitung():
    data = request.get_json(silent=True) or {}
    nama = str(data.get("nama", "")).strip()

    try:
        halaman = int(data.get("halaman"))
    except (TypeError, ValueError):
        return jsonify({"error": "Halaman terakhir harus berupa angka bulat."}), 400

    if not nama:
        return jsonify({"error": "Silakan masukkan nama santri."}), 400

    if halaman < 0 or halaman > TOTAL_HALAMAN:
        return jsonify({
            "error": f"Halaman terakhir harus berada di antara 0 sampai {TOTAL_HALAMAN}."
        }), 400

    sisa = TOTAL_HALAMAN - halaman
    minimal = math.ceil(sisa / TARGET_PEKAN)

    if minimal <= 10:
        batas_simulasi = 10
    else:
        batas_simulasi = math.ceil(minimal / 5) * 5

    simulasi = []
    for kecepatan in range(1, batas_simulasi + 1):
        total_pekan = math.ceil(sisa / kecepatan) if sisa > 0 else 0
        tahun, bulan, pekan = konversi_waktu(total_pekan)
        simulasi.append({
            "kecepatan": kecepatan,
            "total_pekan": total_pekan,
            "waktu": f"{tahun} tahun, {bulan} bulan, {pekan} pekan"
        })

    return jsonify({
        "nama": nama,
        "halaman": halaman,
        "total_halaman": TOTAL_HALAMAN,
        "sisa": sisa,
        "minimal": minimal,
        "target_pekan": TARGET_PEKAN,
        "tanggal_target": TANGGAL_TARGET,
        "simulasi": simulasi,
        "motivasi": pesan_motivasi(minimal)
    })


if __name__ == "__main__":
    app.run(debug=True)
