"""
Windows Calculator Automation Engine
Menggunakan pywinauto dengan backend UIA untuk mengotomasi aplikasi calc.exe.
Dilengkapi mekanisme multi-window detection dan error handling yang robust.
"""

import time
import subprocess
from typing import Tuple
from pywinauto import Application, Desktop


class CalculatorAutomationEngine:
    """Backend engine untuk mengontrol dan menguji Windows Calculator."""

    def __init__(self, timeout: int = 10):
        self.timeout = timeout
        self.app = None
        self.window = None

    def start_calculator(self) -> None:
        """
        Menjalankan calc.exe dan menyambungkan session pywinauto (UIA).
        Mencegah ElementAmbiguousError dengan memfilter window aktif/valid.
        """
        # Bersihkan instans kalkulator lama terlebih dahulu
        self.kill_calculator()
        time.sleep(0.6)

        # Jalankan calc.exe via subprocess agar tidak terhambat launcher stub
        subprocess.Popen("calc.exe", shell=True)

        start_time = time.time()
        desktop = Desktop(backend="uia")
        found_window = None

        # Loop mencari window kalkulator yang benar-benar siap dan memiliki elemen kalkulator
        while time.time() - start_time < self.timeout:
            try:
                # Cari semua window kalkulator yang tampak (visible)
                candidates = desktop.windows(
                    title_re=r"(?i).*(calculator|kalkulator).*",
                    visible_only=True
                )

                for cand in candidates:
                    try:
                        # Pastikan window memiliki elemen inti kalkulator (CalculatorResults atau clearButton)
                        if (cand.child_window(auto_id="CalculatorResults").exists(timeout=0.3) or
                                cand.child_window(auto_id="clearButton").exists(timeout=0.3) or
                                cand.child_window(auto_id="num7Button").exists(timeout=0.3)):
                            found_window = cand
                            break
                    except Exception:
                        continue

                if found_window:
                    break
            except Exception:
                pass

            time.sleep(0.4)

        # Fallback jika pencarian spesifik belum menemukan
        if not found_window:
            try:
                found_window = desktop.window(
                    title_re=r"(?i).*(calculator|kalkulator).*",
                    visible_only=True,
                    found_index=0
                )
                found_window.wait("visible", timeout=2)
            except Exception as ex:
                raise RuntimeError(
                    f"Gagal menemukan window Windows Calculator setelah {self.timeout} detik: {ex}"
                )

        self.window = found_window

        # Fokuskan window ke depan
        try:
            self.window.set_focus()
        except Exception:
            pass

    def click_button(self, auto_id: str) -> None:
        """Mengeklik tombol berdasarkan automation_id dengan fallback aman."""
        if not self.window:
            raise RuntimeError("Aplikasi Calculator belum berjalan.")

        btn = self.window.child_window(auto_id=auto_id)
        btn.wait("visible", timeout=self.timeout)

        # Coba invoke UIA terlebih dahulu (cepat dan tidak mengganggu mouse), lalu fallback click_input
        try:
            btn.invoke()
        except Exception:
            try:
                btn.click_input()
            except Exception:
                btn.click()

        time.sleep(0.3)

    def clear(self) -> None:
        """Menekan tombol Clear (C) untuk mereset kalkulator ke kondisi awal."""
        try:
            self.click_button("clearButton")
        except Exception:
            try:
                self.click_button("clearEntryButton")
            except Exception:
                pass
        time.sleep(0.2)

    def get_result_text(self) -> str:
        """
        Mengambil teks hasil perhitungan dari elemen CalculatorResults.
        Mendukung parsing teks UIA di berbagai versi Windows 10/11.
        """
        if not self.window:
            raise RuntimeError("Aplikasi Calculator belum berjalan.")

        result_elem = self.window.child_window(auto_id="CalculatorResults")
        result_elem.wait("visible", timeout=self.timeout)

        # Coba ambil melalui window_text
        text = ""
        try:
            text = result_elem.window_text().strip()
        except Exception:
            pass

        # Fallback melalui name element info jika window_text kosong
        if not text:
            try:
                text = (result_elem.element_info.name or "").strip()
            except Exception:
                pass

        # Fallback melalui list texts()
        if not text:
            try:
                items = result_elem.texts()
                text = " ".join([i for i in items if i]).strip()
            except Exception:
                pass

        return text

    def kill_calculator(self) -> None:
        """Menutup calc.exe dan membersihkan sisa proses terkait."""
        if self.app:
            try:
                self.app.kill()
            except Exception:
                pass
            self.app = None

        self.window = None

        # Membersihkan proses CalculatorApp dan calc via taskkill
        try:
            subprocess.run(
                "taskkill /F /IM CalculatorApp.exe",
                shell=True,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL
            )
            subprocess.run(
                "taskkill /F /IM calc.exe",
                shell=True,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL
            )
        except Exception:
            pass

    # =========================================================================
    # Test Cases (5 Fitur Utama)
    # =========================================================================

    def test_basic_arithmetic(self) -> Tuple[bool, str]:
        """
        Fitur 1 (Basic Arithmetic):
        Skenario: 7 + 5 = 12
        Validasi: Nilai 12 pada CalculatorResults
        """
        try:
            self.start_calculator()
            self.clear()

            self.click_button("num7Button")
            self.click_button("plusButton")
            self.click_button("num5Button")
            self.click_button("equalButton")

            result = self.get_result_text()
            expected = "12"

            if expected in result:
                return True, f"PASS: Perhitungan 7 + 5 menghasilkan '{result}' (Mengandung nilai {expected})"
            else:
                return False, f"FAIL: Ekspektasi mengandung '{expected}', namun didapatkan '{result}'"
        except Exception as e:
            return False, f"ERROR: Terjadi exception: {str(e)}"
        finally:
            self.kill_calculator()

    def test_clear_function(self) -> Tuple[bool, str]:
        """
        Fitur 2 (Clear Function):
        Skenario: Input 9, lalu tekan tombol Clear (C)
        Validasi: Layar kembali ke 0
        """
        try:
            self.start_calculator()
            self.clear()

            self.click_button("num9Button")
            self.click_button("clearButton")

            result = self.get_result_text()
            # Validasi layar menampilkan 0
            is_zero = result.strip().endswith("0") or " 0" in result or result == "0"

            if is_zero:
                return True, f"PASS: Tombol Clear berhasil mereset tampilan ke '{result}'"
            else:
                return False, f"FAIL: Ekspektasi tampilan kembali ke 0, namun didapatkan '{result}'"
        except Exception as e:
            return False, f"ERROR: Terjadi exception: {str(e)}"
        finally:
            self.kill_calculator()

    def test_decimal_ops(self) -> Tuple[bool, str]:
        """
        Fitur 3 (Decimal Ops):
        Skenario: 0.5 + 1.5 = 2
        Validasi: Hasil desimal menunjukkan 2
        """
        try:
            self.start_calculator()
            self.clear()

            # Input 0.5
            self.click_button("num0Button")
            self.click_button("decimalSeparatorButton")
            self.click_button("num5Button")

            # Operasi +
            self.click_button("plusButton")

            # Input 1.5
            self.click_button("num1Button")
            self.click_button("decimalSeparatorButton")
            self.click_button("num5Button")

            # Sama dengan (=)
            self.click_button("equalButton")

            result = self.get_result_text()
            if "2" in result:
                return True, f"PASS: Perhitungan desimal 0.5 + 1.5 menghasilkan '{result}' (Mengandung 2)"
            else:
                return False, f"FAIL: Ekspektasi hasil mengandung '2', namun didapatkan '{result}'"
        except Exception as e:
            return False, f"ERROR: Terjadi exception: {str(e)}"
        finally:
            self.kill_calculator()

    def test_negation(self) -> Tuple[bool, str]:
        """
        Fitur 4 (Negation):
        Skenario: Input 5, tekan tombol Negate (±)
        Validasi: Hasil menjadi -5
        """
        try:
            self.start_calculator()
            self.clear()

            self.click_button("num5Button")
            self.click_button("negateButton")

            result = self.get_result_text()
            if "-5" in result or "- 5" in result:
                return True, f"PASS: Tombol Negate berhasil mengubah 5 menjadi '{result}'"
            else:
                return False, f"FAIL: Ekspektasi hasil mengandung '-5', namun didapatkan '{result}'"
        except Exception as e:
            return False, f"ERROR: Terjadi exception: {str(e)}"
        finally:
            self.kill_calculator()

    def test_error_handling(self) -> Tuple[bool, str]:
        """
        Fitur 5 (Error Handling):
        Skenario: 9 / 0 (Divide by Zero)
        Validasi: Pesan error 'Cannot divide by zero' / 'Tidak dapat dibagi dengan nol'
        """
        try:
            self.start_calculator()
            self.clear()

            self.click_button("num9Button")
            self.click_button("divideButton")
            self.click_button("num0Button")
            self.click_button("equalButton")

            result = self.get_result_text()
            result_lower = result.lower()

            error_keywords = [
                "cannot divide by zero",
                "tidak dapat dibagi dengan nol",
                "tidak dapat membagi dengan nol",
                "divide by zero",
                "tidak terdefinisi",
                "hasilnya tidak dapat ditentukan",
                "error"
            ]

            is_error = any(keyword in result_lower for keyword in error_keywords)

            if is_error:
                return True, f"PASS: Pesan error divide by zero terdeteksi dengan tepat: '{result}'"
            else:
                return False, f"FAIL: Pesan divide by zero tidak ditemukan pada: '{result}'"
        except Exception as e:
            return False, f"ERROR: Terjadi exception: {str(e)}"
        finally:
            self.kill_calculator()
