import customtkinter as ctk

# --- Konfigurasi Awal & Skema Warna ---
# Palet warna akan disesuaikan oleh mode Terang/Gelap
# jadi kita tidak mendefinisikannya secara statis lagi.

class AplikasiKonversiSuhu(ctk.CTk):
    def __init__(self):
        super().__init__()

        # --- Konfigurasi Utama Jendela ---
        self.title("Kalkulator Suhu ")
        self.geometry("420x640")
        self.resizable(False, False)
        
        # Menyimpan riwayat konversi
        self.riwayat = []

        # Atur tema awal dari sistem
        ctk.set_appearance_mode("System") 

        # --- Font Kustom ---
        self.font_judul = ctk.CTkFont(family="Roboto", size=28, weight="bold")
        self.font_label = ctk.CTkFont(family="Roboto", size=14)
        self.font_tombol = ctk.CTkFont(family="Roboto", size=16, weight="bold")
        self.font_hasil = ctk.CTkFont(family="Roboto", size=26, weight="bold")
        self.font_riwayat = ctk.CTkFont(family="Courier New", size=12)

        self._buat_widget()

    def _buat_widget(self):
        """Membuat dan menata semua widget di jendela utama."""
        
        # --- Frame Header (Judul & Tombol Tema) ---
        frame_header = ctk.CTkFrame(self, fg_color="transparent")
        frame_header.pack(pady=(10, 20), padx=20, fill="x")

        label_judul = ctk.CTkLabel(frame_header, text="Kalkulator Suhu", font=self.font_judul)
        label_judul.pack(side="left")

        self.saklar_tema = ctk.CTkSwitch(
            frame_header, text="Mode Gelap", command=self._ganti_tema,
            font=self.font_label, progress_color="#FFC300"
        )
        self.saklar_tema.pack(side="right", pady=5)


        # --- Frame Input & Pilihan ---
        frame_input = ctk.CTkFrame(self, corner_radius=10)
        frame_input.pack(pady=10, padx=20, fill="x", ipady=15)

        ctk.CTkLabel(frame_input, text="Masukkan Nilai Suhu", font=self.font_label).pack(pady=(5,5))
        self.entry_suhu = ctk.CTkEntry(
            frame_input, placeholder_text="misal: 37.5", font=self.font_label, width=200, height=40,
            corner_radius=8, border_width=2
        )
        self.entry_suhu.pack()

        ctk.CTkLabel(frame_input, text="Pilih Jenis Konversi", font=self.font_label).pack(pady=(15,5))
        # --- OPSI KONVERSI DIPERBARUI ---
        opsi_konversi = [
            "Celcius → Fahrenheit (°C → °F)", "Celcius → Kelvin (°C → K)", "Celcius → Réaumur (°C → °R)",
            "Fahrenheit → Celcius (°F → °C)", "Fahrenheit → Kelvin (°F → K)", "Fahrenheit → Réaumur (°F → °R)",
            "Kelvin → Celcius (K → °C)", "Kelvin → Fahrenheit (K → °F)", "Kelvin → Réaumur (K → °R)",
            "Réaumur → Celcius (°R → °C)", "Réaumur → Fahrenheit (°R → °F)", "Réaumur → Kelvin (°R → K)",
        ]
        self.pilihan_konversi = ctk.CTkComboBox(
            frame_input, values=opsi_konversi, font=self.font_label, height=40, width=280, corner_radius=8
        )
        self.pilihan_konversi.set(opsi_konversi[0])
        self.pilihan_konversi.pack()

        # --- Frame Tombol Aksi ---
        frame_aksi = ctk.CTkFrame(self, fg_color="transparent")
        frame_aksi.pack(pady=10, padx=20, fill="x")
        frame_aksi.grid_columnconfigure((0, 1), weight=1)

        tombol_reset = ctk.CTkButton(
            frame_aksi, text="Reset", font=self.font_tombol, command=self._reset_form,
            height=50, corner_radius=10, fg_color="gray50", hover_color="gray30"
        )
        tombol_reset.grid(row=0, column=0, padx=(0, 5), sticky="ew")

        tombol_konversi = ctk.CTkButton(
            frame_aksi, text="Konversi", font=self.font_tombol, command=self._lakukan_konversi,
            height=50, corner_radius=10, fg_color="#FFC300", hover_color="#FFAA00"
        )
        tombol_konversi.grid(row=0, column=1, padx=(5, 0), sticky="ew")

        # --- Frame Hasil & Salin ---
        frame_hasil = ctk.CTkFrame(self, corner_radius=10)
        frame_hasil.pack(pady=10, padx=20, fill="x", ipady=10)
        frame_hasil.grid_columnconfigure(0, weight=1)

        self.label_hasil = ctk.CTkLabel(frame_hasil, text="Hasil: -", font=self.font_hasil)
        self.label_hasil.grid(row=0, column=0, pady=10, padx=10, sticky="w")
        
        self.tombol_salin = ctk.CTkButton(
            frame_hasil, text="Salin", font=self.font_label, width=80, command=self._salin_hasil
        )
        self.tombol_salin.grid(row=0, column=1, padx=10, sticky="e")
        
        # --- Frame Riwayat ---
        frame_riwayat = ctk.CTkFrame(self, corner_radius=10)
        frame_riwayat.pack(pady=(10,20), padx=20, fill="both", expand=True)
        ctk.CTkLabel(frame_riwayat, text="Riwayat Konversi", font=self.font_label).pack(pady=(10,5))
        
        self.box_riwayat = ctk.CTkTextbox(
            frame_riwayat, font=self.font_riwayat, corner_radius=8, border_width=1
        )
        self.box_riwayat.pack(pady=5, padx=10, fill="both", expand=True)
        self.box_riwayat.configure(state="disabled") # Hanya untuk dibaca

    def _lakukan_konversi(self):
        try:
            nilai_input = float(self.entry_suhu.get())
            jenis_konversi = self.pilihan_konversi.get()
            hasil, unit, input_unit_str = 0, "", ""

            # Logika konversi dengan unit yang lebih jelas
            pilihan = jenis_konversi.split(" ")
            input_unit = pilihan[0]
            
            # Menentukan unit input string
            if input_unit == "Celcius": input_unit_str = "°C"
            elif input_unit == "Fahrenheit": input_unit_str = "°F"
            elif input_unit == "Kelvin": input_unit_str = "K"
            elif input_unit == "Réaumur": input_unit_str = "°R"

            # --- LOGIKA KONVERSI DIPERBARUI ---
            # Celcius ke ...
            if jenis_konversi == "Celcius → Fahrenheit (°C → °F)":
                hasil, unit = (nilai_input * 9/5) + 32, "°F"
            elif jenis_konversi == "Celcius → Kelvin (°C → K)":
                hasil, unit = nilai_input + 273.15, "K"
            elif jenis_konversi == "Celcius → Réaumur (°C → °R)":
                hasil, unit = nilai_input * 4/5, "°R"
            # Fahrenheit ke ...
            elif jenis_konversi == "Fahrenheit → Celcius (°F → °C)":
                hasil, unit = (nilai_input - 32) * 5/9, "°C"
            elif jenis_konversi == "Fahrenheit → Kelvin (°F → K)":
                hasil, unit = (nilai_input - 32) * 5/9 + 273.15, "K"
            elif jenis_konversi == "Fahrenheit → Réaumur (°F → °R)":
                hasil, unit = (nilai_input - 32) * 4/9, "°R"
            # Kelvin ke ...
            elif jenis_konversi == "Kelvin → Celcius (K → °C)":
                hasil, unit = nilai_input - 273.15, "°C"
            elif jenis_konversi == "Kelvin → Fahrenheit (K → °F)":
                hasil, unit = (nilai_input - 273.15) * 9/5 + 32, "°F"
            elif jenis_konversi == "Kelvin → Réaumur (K → °R)":
                hasil, unit = (nilai_input - 273.15) * 4/5, "°R"
            # Réaumur ke ...
            elif jenis_konversi == "Réaumur → Celcius (°R → °C)":
                hasil, unit = nilai_input * 5/4, "°C"
            elif jenis_konversi == "Réaumur → Fahrenheit (°R → °F)":
                hasil, unit = (nilai_input * 9/4) + 32, "°F"
            elif jenis_konversi == "Réaumur → Kelvin (°R → K)":
                hasil, unit = (nilai_input * 5/4) + 273.15, "K"
            
            hasil_string = f"{hasil:.2f} {unit}"
            self.label_hasil.configure(text=hasil_string)
            
            # Tambahkan ke riwayat
            riwayat_entry = f"{nilai_input:.1f} {input_unit_str} → {hasil_string}"
            self.riwayat.insert(0, riwayat_entry) # Masukkan ke paling atas
            if len(self.riwayat) > 10: self.riwayat.pop() # Batasi 10 entri
            self._update_riwayat_box()
            
        except (ValueError, IndexError):
            self.label_hasil.configure(text="Input Salah!")
        except Exception as e:
            self.label_hasil.configure(text="Error!")
            print(f"Terjadi error: {e}")

    def _update_riwayat_box(self):
        self.box_riwayat.configure(state="normal") # Aktifkan untuk menulis
        self.box_riwayat.delete("1.0", "end")
        self.box_riwayat.insert("1.0", "\n".join(self.riwayat))
        self.box_riwayat.configure(state="disabled") # Nonaktifkan lagi

    def _salin_hasil(self):
        hasil_teks = self.label_hasil.cget("text")
        if "Hasil:" not in hasil_teks and "Input" not in hasil_teks and "Error" not in hasil_teks:
            self.clipboard_clear()
            self.clipboard_append(hasil_teks)
            self.tombol_salin.configure(text="Tersalin!")
            self.after(1500, lambda: self.tombol_salin.configure(text="Salin")) # Kembalikan teks tombol
            
    def _reset_form(self):
        self.entry_suhu.delete(0, "end")
        self.label_hasil.configure(text="Hasil: -")
        self.pilihan_konversi.set(self.pilihan_konversi.cget("values")[0])

    def _ganti_tema(self):
        if self.saklar_tema.get() == 1:
            ctk.set_appearance_mode("Dark")
        else:
            ctk.set_appearance_mode("Light")

# --- Menjalankan Aplikasi ---
if __name__ == "__main__":
    app = AplikasiKonversiSuhu()
    app.mainloop()
