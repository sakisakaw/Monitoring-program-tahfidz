const form = document.getElementById("form-hafalan");
const submitBtn = document.getElementById("submit-btn");
const resetBtn = document.getElementById("reset-btn");
const statusText = document.getElementById("status");
const results = document.getElementById("hasil");

form.addEventListener("submit", async (event) => {
  event.preventDefault();

  const nama = document.getElementById("nama").value.trim();
  const halaman = document.getElementById("halaman").value;

  submitBtn.disabled = true;
  submitBtn.textContent = "Menghitung...";
  statusText.textContent = "Sedang menghitung target hafalan...";

  try {
    const response = await fetch("/hitung", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ nama, halaman })
    });

    const data = await response.json();
    if (!response.ok) throw new Error(data.error || "Terjadi kesalahan.");

    document.getElementById("nama-hasil").textContent = data.nama;
    document.getElementById("halaman-hasil").textContent =
      `Halaman ${data.halaman} dari ${data.total_halaman}`;
    document.getElementById("sisa-hasil").textContent = data.sisa;
    document.getElementById("minimal-hasil").textContent = data.minimal;
    document.getElementById("target-label").textContent =
      `${data.target_pekan} pekan · ${data.tanggal_target}`;

    const tbody = document.getElementById("tabel-simulasi");
    tbody.replaceChildren();

    data.simulasi.forEach((item) => {
      const row = document.createElement("tr");
      [ `${item.kecepatan} halaman/pekan`, `${item.total_pekan} pekan`, item.waktu ]
        .forEach((value) => {
          const cell = document.createElement("td");
          cell.textContent = value;
          row.appendChild(cell);
        });
      tbody.appendChild(row);
    });

    const panel = document.getElementById("panel-motivasi");
    panel.className = `motivation ${data.motivasi.level}`;
    document.getElementById("judul-motivasi").textContent = data.motivasi.judul;
    document.getElementById("pesan-motivasi").textContent = data.motivasi.pesan;

    results.classList.remove("hidden");
    statusText.textContent = "Perhitungan selesai. Data tidak disimpan.";
    results.scrollIntoView({ behavior: "smooth", block: "start" });
  } catch (error) {
    statusText.textContent = error.message;
  } finally {
    submitBtn.disabled = false;
    submitBtn.innerHTML = 'Hitung target <span>→</span>';
  }
});

resetBtn.addEventListener("click", () => {
  form.reset();
  results.classList.add("hidden");
  statusText.textContent = "Formulir dibersihkan. Data tidak disimpan.";
  document.getElementById("nama").focus();
});
