"""
Windows Calculator Automation Test Launcher
GUI Test Runner menggunakan Python Tkinter untuk eksekusi Automation Testing calc.exe
"""

import sys
import threading
import datetime
import tkinter as tk
from tkinter import messagebox, scrolledtext

from calculator_engine import CalculatorAutomationEngine


class StyledButton(tk.Button):
    """Custom Button dengan efek hover & bevel 3D yang elegan."""

    def __init__(self, master, is_primary=False, is_util=False, **kwargs):
        self.is_primary = is_primary
        self.is_util = is_util

        if is_primary:
            # Primary Emerald Green
            self.normal_bg = "#2e7d32"
            self.hover_bg = "#388e3c"
            self.active_bg = "#1b5e20"
            self.fg_color = "#ffffff"
        elif is_util:
            # Slate Dark Utility
            self.normal_bg = "#374151"
            self.hover_bg = "#4b5563"
            self.active_bg = "#1f2937"
            self.fg_color = "#e5e7eb"
        else:
            # Classic Gray Stone Button
            self.normal_bg = "#4b5563"
            self.hover_bg = "#6b7280"
            self.active_bg = "#374151"
            self.fg_color = "#ffffff"

        super().__init__(
            master,
            bg=self.normal_bg,
            fg=self.fg_color,
            activebackground=self.active_bg,
            activeforeground="#ffffff",
            disabledforeground="#9ca3af",
            relief="raised",
            bd=3,
            cursor="hand2",
            highlightthickness=1,
            highlightbackground="#1f2937",
            **kwargs
        )

        self.bind("<Enter>", self._on_enter)
        self.bind("<Leave>", self._on_leave)

    def _on_enter(self, event):
        if self["state"] != "disabled":
            self.configure(bg=self.hover_bg)

    def _on_leave(self, event):
        if self["state"] != "disabled":
            self.configure(bg=self.normal_bg)


class CalculatorTestRunnerGUI:
    """Aplikasi GUI Tkinter untuk otomatisasi Windows Calculator."""

    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title("Windows Calculator Automation Test Launcher")
        self.root.geometry("920x760")
        self.root.minsize(860, 700)

        # Inisialisasi engine pywinauto
        self.engine = CalculatorAutomationEngine(timeout=10)
        self.is_running = False

        # Palette Warna Dark Theme
        self.colors = {
            "bg_main": "#1e2430",        # Background Utama
            "bg_card": "#283040",        # Card/Panel Container
            "bg_dark": "#111827",        # Log background
            "border": "#3b485d",         # Border kontainer
            "accent_title": "#facc15",   # Aksen Kuning Title
            "accent_cyan": "#38bdf8",    # Aksen Cyan
            "accent_green": "#4ade80",   # Aksen Hijau
            "accent_red": "#f87171",     # Aksen Merah
            "text_white": "#ffffff",
            "text_gray": "#94a3b8"
        }

        self.root.configure(bg=self.colors["bg_main"])

        # Bangun komponen UI
        self._build_header()
        self._build_feature_buttons()
        self._build_status_bar()
        self._build_log_console()

        self.log_message("SYSTEM", "Aplikasi siap. Silakan pilih fitur untuk memulai pengujian.")

    def _build_header(self) -> None:
        """Membuat bagian header aplikasi."""
        header_frame = tk.Frame(
            self.root,
            bg=self.colors["bg_card"],
            padx=20,
            pady=12,
            relief="raised",
            bd=3,
            highlightbackground="#181f2a",
            highlightthickness=1
        )
        header_frame.pack(fill="x", side="top", padx=14, pady=(12, 6))

        # 1. Judul Utama
        title_label = tk.Label(
            header_frame,
            text="Windows Calculator Automation Test Launcher",
            font=("Consolas", 15, "bold"),
            fg=self.colors["accent_title"],
            bg=self.colors["bg_card"]
        )
        title_label.pack(anchor="w")

        # 2. Subtitle Engine Info
        subtitle_label = tk.Label(
            header_frame,
            text="Engine: pywinauto (UIA Backend)  •  Target: calc.exe  •  UI Automation Driven",
            font=("Consolas", 9),
            fg=self.colors["accent_cyan"],
            bg=self.colors["bg_card"]
        )
        subtitle_label.pack(anchor="w", pady=(2, 4))

        # 3. Baris Informasi Pembuat (By) tepat di bawah Engine (Disusun vertikal agar tidak terpotong)
        by_frame = tk.Frame(header_frame, bg=self.colors["bg_card"])
        by_frame.pack(anchor="w", pady=(4, 0))

        lbl_by = tk.Label(
            by_frame,
            text="By:",
            font=("Segoe UI", 9, "bold"),
            fg=self.colors["accent_green"],
            bg=self.colors["bg_card"]
        )
        lbl_by.pack(anchor="w")

        authors = [
            "Aloys Gamaliel Barus (2802520463)",
            "El Husamy Ahmad (2802558304)",
            "Keizha Tanuwijaya Sumbaymider (2802512184)"
        ]

        for author in authors:
            lbl_item = tk.Label(
                by_frame,
                text=f"  • {author}",
                font=("Segoe UI", 9),
                fg=self.colors["text_white"],
                bg=self.colors["bg_card"]
            )
            lbl_item.pack(anchor="w")

    def _build_feature_buttons(self) -> None:
        """Membuat 5 tombol fitur utama dan 1 tombol jalankan semua."""
        container = tk.LabelFrame(
            self.root,
            text=" [ ⚙️ MODUL & FITUR PENGUJIAN ] ",
            font=("Consolas", 10, "bold"),
            bg=self.colors["bg_card"],
            fg=self.colors["accent_title"],
            padx=12,
            pady=8,
            relief="raised",
            bd=3,
            highlightbackground="#181f2a",
            highlightthickness=1
        )
        container.pack(fill="x", padx=14, pady=(6, 6))

        # Definisi 5 Fitur Utama sesuai spesifikasi
        self.features = [
            {
                "id": 1,
                "title": "Fitur 1: Basic Arithmetic",
                "desc": "7 + 5 = 12 (Validasi CalculatorResults)",
                "method": self.engine.test_basic_arithmetic,
            },
            {
                "id": 2,
                "title": "Fitur 2: Clear Function",
                "desc": "Input 9 -> Tekan C -> Validasi Layar = 0",
                "method": self.engine.test_clear_function,
            },
            {
                "id": 3,
                "title": "Fitur 3: Decimal Ops",
                "desc": "0.5 + 1.5 = 2 (Validasi Nilai Desimal)",
                "method": self.engine.test_decimal_ops,
            },
            {
                "id": 4,
                "title": "Fitur 4: Negation",
                "desc": "Input 5 -> Tekan ± -> Validasi Layar = -5",
                "method": self.engine.test_negation,
            },
            {
                "id": 5,
                "title": "Fitur 5: Error Handling",
                "desc": "9 / 0 -> Validasi Divide by Zero Error",
                "method": self.engine.test_error_handling,
            },
        ]

        self.buttons = []

        # Grid tombol (2 kolom)
        for idx, feat in enumerate(self.features):
            row = idx // 2
            col = idx % 2

            btn_frame = tk.Frame(container, bg=self.colors["bg_card"], padx=4, pady=3)
            btn_frame.grid(row=row, column=col, sticky="nsew")
            container.grid_columnconfigure(col, weight=1)

            btn = StyledButton(
                btn_frame,
                text=f"{feat['title']}\n[{feat['desc']}]",
                font=("Consolas", 9, "bold"),
                command=lambda f=feat: self.run_single_test_threaded(f)
            )
            btn.pack(fill="both", expand=True)
            self.buttons.append(btn)

        # Baris aksi: Tombol Primary
        action_frame = tk.Frame(container, bg=self.colors["bg_card"], pady=4)
        action_frame.grid(row=3, column=0, columnspan=2, sticky="ew", padx=4, pady=(6, 2))

        self.btn_run_all = StyledButton(
            action_frame,
            is_primary=True,
            text="🚀 JALANKAN SEMUA PENGUJIAN SEKALIGUS (FITUR 1 s.d. 5) 🚀",
            font=("Consolas", 10, "bold"),
            command=self.run_all_tests_threaded
        )
        self.btn_run_all.pack(fill="x", expand=True)

    def _build_status_bar(self) -> None:
        """Membuat status bar informasi."""
        self.status_frame = tk.Frame(
            self.root,
            bg="#111827",
            padx=16,
            pady=6,
            relief="sunken",
            bd=2
        )
        self.status_frame.pack(fill="x", padx=14, pady=(0, 6))

        self.lbl_status = tk.Label(
            self.status_frame,
            text="STATUS: [ READY ]",
            font=("Consolas", 9, "bold"),
            fg=self.colors["accent_green"],
            bg="#111827"
        )
        self.lbl_status.pack(side="left")

        self.lbl_active_test = tk.Label(
            self.status_frame,
            text="Menunggu tindakan pengujian...",
            font=("Consolas", 9),
            fg=self.colors["text_gray"],
            bg="#111827"
        )
        self.lbl_active_test.pack(side="right")

    def _build_log_console(self) -> None:
        """Membuat konsol log eksekusi."""
        console_frame = tk.LabelFrame(
            self.root,
            text=" [ 📝 LOG OUTPUT AKTIVITAS & EKSEKUSI ] ",
            font=("Consolas", 10, "bold"),
            bg=self.colors["bg_card"],
            fg=self.colors["accent_title"],
            padx=12,
            pady=6,
            relief="raised",
            bd=3,
            highlightbackground="#181f2a",
            highlightthickness=1
        )
        console_frame.pack(fill="both", expand=True, padx=14, pady=(0, 12))

        # Toolbar di atas log
        toolbar = tk.Frame(console_frame, bg=self.colors["bg_card"])
        toolbar.pack(fill="x", pady=(0, 4))

        btn_clear = StyledButton(
            toolbar,
            is_util=True,
            text="🧹 Bersihkan Log",
            font=("Consolas", 8, "bold"),
            command=self.clear_log
        )
        btn_clear.pack(side="right", padx=(4, 0))

        btn_copy = StyledButton(
            toolbar,
            is_util=True,
            text="📋 Salin Semua Log",
            font=("Consolas", 8, "bold"),
            command=self.copy_log
        )
        btn_copy.pack(side="right")

        lbl_log_hint = tk.Label(
            toolbar,
            text="Log real-time pywinauto UIA engine:",
            font=("Consolas", 8),
            fg=self.colors["text_gray"],
            bg=self.colors["bg_card"]
        )
        lbl_log_hint.pack(side="left")

        # ScrolledText
        self.log_text = scrolledtext.ScrolledText(
            console_frame,
            wrap=tk.WORD,
            font=("Consolas", 9),
            height=13,
            bg=self.colors["bg_dark"],
            fg=self.colors["text_white"],
            insertbackground="#ffffff",
            relief="sunken",
            bd=3,
            padx=8,
            pady=8
        )
        self.log_text.pack(fill="both", expand=True)

        # Warna Tag Log
        self.log_text.tag_config("PASS", foreground=self.colors["accent_green"], font=("Consolas", 9, "bold"))
        self.log_text.tag_config("FAIL", foreground=self.colors["accent_red"], font=("Consolas", 9, "bold"))
        self.log_text.tag_config("ERROR", foreground="#fb7185", font=("Consolas", 9, "bold"))
        self.log_text.tag_config("INFO", foreground=self.colors["accent_cyan"])
        self.log_text.tag_config("SYSTEM", foreground=self.colors["accent_title"], font=("Consolas", 9, "bold"))
        self.log_text.tag_config("TIMESTAMP", foreground=self.colors["text_gray"])

    # =========================================================================
    # Thread-Safe UI Helpers
    # =========================================================================

    def log_message(self, tag: str, message: str) -> None:
        """Thread-safe logging ke antarmuka GUI."""
        if threading.current_thread() is not threading.main_thread():
            self.root.after(0, lambda: self._append_log(tag, message))
        else:
            self._append_log(tag, message)

    def _append_log(self, tag: str, message: str) -> None:
        """Menulis teks ke widget ScrolledText dan auto-scroll ke akhir."""
        timestamp = datetime.datetime.now().strftime("[%H:%M:%S] ")
        self.log_text.insert(tk.END, timestamp, "TIMESTAMP")
        self.log_text.insert(tk.END, f"[{tag}] ", tag)
        self.log_text.insert(tk.END, f"{message}\n", tag)
        self.log_text.see(tk.END)

    def clear_log(self) -> None:
        """Membersihkan layar log."""
        self.log_text.delete("1.0", tk.END)
        self.log_message("SYSTEM", "Konsol log telah dibersihkan.")

    def copy_log(self) -> None:
        """Menyalin teks log ke clipboard Windows."""
        content = self.log_text.get("1.0", tk.END)
        self.root.clipboard_clear()
        self.root.clipboard_append(content)
        messagebox.showinfo("Clipboard", "Seluruh teks log berhasil disalin ke clipboard.")

    def set_ui_busy(self, is_busy: bool, current_task: str = "") -> None:
        """Thread-safe kontrol status tombol saat proses pengujian berjalan."""
        if threading.current_thread() is not threading.main_thread():
            self.root.after(0, lambda: self._apply_ui_busy(is_busy, current_task))
        else:
            self._apply_ui_busy(is_busy, current_task)

    def _apply_ui_busy(self, is_busy: bool, current_task: str) -> None:
        self.is_running = is_busy
        state = "disabled" if is_busy else "normal"

        for btn in self.buttons:
            btn.configure(state=state)
        self.btn_run_all.configure(state=state)

        if is_busy:
            self.lbl_status.configure(
                text="STATUS: [ ⏳ SEDANG BERJALAN... ]",
                fg=self.colors["accent_title"]
            )
            self.lbl_active_test.configure(
                text=f"Sedang menguji: {current_task}",
                fg=self.colors["accent_cyan"]
            )
        else:
            self.lbl_status.configure(
                text="STATUS: [ SELESAI / READY ]",
                fg=self.colors["accent_green"]
            )
            self.lbl_active_test.configure(
                text="Siap untuk pengujian berikutnya.",
                fg=self.colors["text_gray"]
            )

    # =========================================================================
    # Test Runners (Threaded)
    # =========================================================================

    def run_single_test_threaded(self, feature: dict) -> None:
        """Menjalankan satu fitur pengujian di thread terpisah."""
        if self.is_running:
            return

        thread = threading.Thread(
            target=self._execute_single_test,
            args=(feature,),
            daemon=True
        )
        thread.start()

    def _execute_single_test(self, feature: dict) -> None:
        """Eksekusi skenario uji di latar belakang."""
        title = feature["title"]
        self.set_ui_busy(True, title)
        self.log_message("INFO", f"Memulai pengujian {title}...")

        success, detail = feature["method"]()

        # Update UI di main thread
        self.root.after(0, lambda: self._handle_single_test_result(title, success, detail))

    def _handle_single_test_result(self, title: str, success: bool, detail: str) -> None:
        """Handler hasil uji tunggal dan menampilkan pop-up messagebox."""
        self.set_ui_busy(False)

        if success:
            self.log_message("PASS", detail)
            messagebox.showinfo(
                title=f"Test Selesai - PASS ({title})",
                message=f"Status: PASS\n\nDetail:\n{detail}"
            )
        else:
            self.log_message("FAIL", detail)
            messagebox.showerror(
                title=f"Test Selesai - FAIL ({title})",
                message=f"Status: FAIL\n\nDetail:\n{detail}"
            )

    def run_all_tests_threaded(self) -> None:
        """Menjalankan seluruh 5 pengujian secara berurutan."""
        if self.is_running:
            return

        thread = threading.Thread(
            target=self._execute_all_tests,
            daemon=True
        )
        thread.start()

    def _execute_all_tests(self) -> None:
        """Loop eksekusi kelima fitur uji."""
        self.set_ui_busy(True, "Seluruh Fitur (1 s.d. 5)")
        self.log_message("SYSTEM", "==========================================================")
        self.log_message("SYSTEM", "MEMULAI BATCH TEST (SEMUA 5 FITUR KALKULATOR)")
        self.log_message("SYSTEM", "==========================================================")

        results = []
        for feature in self.features:
            title = feature["title"]
            self.set_ui_busy(True, title)
            self.log_message("INFO", f"Mengeksekusi {title}...")

            success, detail = feature["method"]()
            results.append((title, success, detail))

            tag = "PASS" if success else "FAIL"
            self.log_message(tag, f"[{title}] -> {detail}")

        self.root.after(0, lambda: self._handle_all_tests_result(results))

    def _handle_all_tests_result(self, results: list) -> None:
        """Handler hasil batch test."""
        self.set_ui_busy(False)

        total = len(results)
        passed = sum(1 for _, ok, _ in results if ok)
        failed = total - passed

        summary_msg = f"Ringkasan Pengujian:\nTotal: {total}\nPASS: {passed}\nFAIL: {failed}\n\n"
        for title, ok, detail in results:
            status_text = "PASS" if ok else "FAIL"
            summary_msg += f"• [{status_text}] {title}\n"

        self.log_message("SYSTEM", "==========================================================")
        self.log_message("SYSTEM", f"HASIL AKHIR BATCH TEST: {passed}/{total} PASS ({failed} GAGAL)")
        self.log_message("SYSTEM", "==========================================================")

        if failed == 0:
            messagebox.showinfo(
                title="Batch Test Selesai - ALL PASS",
                message=summary_msg
            )
        else:
            messagebox.showwarning(
                title=f"Batch Test Selesai - {failed} GAGAL",
                message=summary_msg
            )


def main():
    root = tk.Tk()
    app = CalculatorTestRunnerGUI(root)

    def on_closing():
        try:
            app.engine.kill_calculator()
        except Exception:
            pass
        root.destroy()
        sys.exit(0)

    root.protocol("WM_DELETE_WINDOW", on_closing)
    root.mainloop()


if __name__ == "__main__":
    main()
