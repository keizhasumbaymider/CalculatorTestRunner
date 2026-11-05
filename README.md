# Windows Calculator Automation Test Launcher

Aplikasi Desktop GUI (Test Runner) berbasis Python dan Tkinter untuk melakukan Automation Testing pada aplikasi Windows Calculator (`calc.exe`) menggunakan backend `pywinauto` (UIA).

### 👥 Tim Pengembang (By):
- **Aloys Gamaliel Barus** (2802520463)
- **El Husamy Ahmad** (2802558304)
- **Keizha Tanuwijaya Sumbaymider** (2802512184)

---

## 📋 Fitur & Test Case yang Diuji

1. **Fitur 1 (Basic Arithmetic)**:
   - Skenario: `7 + 5 = 12`
   - Validasi: Nilai `12` pada elemen hasil `CalculatorResults`.
2. **Fitur 2 (Clear Function)**:
   - Skenario: Input angka `9` -> Tekan tombol Clear (`clearButton` / `C`).
   - Validasi: Layar kembali ke `0`.
3. **Fitur 3 (Decimal Ops)**:
   - Skenario: `0.5 + 1.5 = 2`
   - Validasi: Hasil desimal mengandung `2`.
4. **Fitur 4 (Negation)**:
   - Skenario: Input `5` -> Tekan tombol Negate (`negateButton` / `±`).
   - Validasi: Hasil berubah menjadi `-5`.
5. **Fitur 5 (Error Handling)**:
   - Skenario: `9 / 0` (Divide by Zero).
   - Validasi: Menangkap pesan error pembagian dengan nol (*Cannot divide by zero* / *Tidak dapat dibagi dengan nol*).

---

## 🛠️ Persyaratan Sistem & Instalasi

- **Sistem Operasi**: Windows 10 atau Windows 11
- **Python**: 3.8+ (Sudah teruji di Python 3.14)
- **Library**: `pywinauto`, `pywin32`, `comtypes`

Instal dependensi melalui terminal / Command Prompt:
```bash
pip install -r requirements.txt
```

---

## 🚀 Cara Menjalankan Aplikasi

Jalankan perintah berikut di terminal:
```bash
python calculator_test_runner.py
```

### Panduan Penggunaan GUI:
1. Setelah jendela **Windows Calculator Automation Test Launcher** terbuka, pilih salah satu tombol fitur pengujian (atau tombol **Jalankan Semua Pengujian**).
2. Sistem akan membuka `calc.exe`, melakukan penekanan tombol secara otomatis, memvalidasi hasil, dan menutup kalkulator (`app.kill()`).
3. Seluruh proses pengujian berjalan di latar belakang (multithreading) sehingga antarmuka GUI tetap responsif tanpa *lag* / *freeze*.
4. Pop-up dialog (`tkinter.messagebox`) akan muncul menampilkan status **PASS** atau **FAIL** beserta detail hasil uji, dan catatan lengkap tersimpan di konsol log aplikasi.
