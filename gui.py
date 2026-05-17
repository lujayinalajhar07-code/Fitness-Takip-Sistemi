"""
╔══════════════════════════════════════════════════════════════════╗
║           FİTNESS TAKİP SİSTEMİ - Arayüz Katmanı               ║
╠══════════════════════════════════════════════════════════════════╣
║  Başlatma: python fitness_gui.py                                 ║
╚══════════════════════════════════════════════════════════════════╝
"""

import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
from app import FitnessSistemi, Sporcu, Antrenman

# ─────────────────────────────────────────────
#  GUI / KULLANICI ARAYÜZÜ KATMANI
# ─────────────────────────────────────────────

RENKLER = {
    "bg":        "#0d0f1a",
    "panel":     "#141728",
    "card":      "#1c2035",
    "border":    "#252a45",
    "accent1":   "#00e5ff",   # cyan
    "accent2":   "#ff4081",   # pembe
    "accent3":   "#69ff47",   # yeşil
    "text":      "#e8eaf6",
    "text_dim":  "#7986cb",
    "warning":   "#ffd740",
}

YAZI = {
    "baslik":  ("Orbitron", 22, "bold"),
    "panel":   ("Orbitron", 13, "bold"),
    "etiket":  ("Share Tech Mono", 11),
    "deger":   ("Share Tech Mono", 14, "bold"),
    "kucuk":   ("Share Tech Mono", 9),
    "buton":   ("Orbitron", 10, "bold"),
}

# Fallback fontlar (yüklü değilse)
YAZI_FB = {
    "baslik":  ("Courier", 18, "bold"),
    "panel":   ("Courier", 12, "bold"),
    "etiket":  ("Courier", 10),
    "deger":   ("Courier", 13, "bold"),
    "kucuk":   ("Courier", 9),
    "buton":   ("Courier", 10, "bold"),
}


def font(key):
    """Önce birincil fontu dene, hata varsa fallback kullan."""
    try:
        import tkinter.font as tkfont
        f = tkfont.Font(family=YAZI[key][0], size=YAZI[key][1],
                        weight=YAZI[key][2] if len(YAZI[key]) > 2 else "normal")
        return YAZI[key]
    except Exception:
        return YAZI_FB[key]


class GirisEkrani(tk.Toplevel):
    """Kullanıcı türü seçim ekranı."""

    def __init__(self, parent, callback):
        super().__init__(parent)
        self.callback = callback
        self.title("Fitness Takip Sistemi – Giriş")
        self.configure(bg=RENKLER["bg"])
        self.resizable(False, False)
        self.geometry("420x340")
        self.grab_set()
        self._olustur()

    def _olustur(self):
        tk.Label(self, text="FITNESS TAKİP", font=font("baslik"),
                 bg=RENKLER["bg"], fg=RENKLER["accent1"]).pack(pady=(30, 4))
        tk.Label(self, text="SİSTEMİ", font=font("panel"),
                 bg=RENKLER["bg"], fg=RENKLER["text_dim"]).pack()
        tk.Label(self, text="─" * 42, bg=RENKLER["bg"],
                 fg=RENKLER["border"]).pack(pady=10)
        tk.Label(self, text="Kullanıcı türünüzü seçin:", font=font("etiket"),
                 bg=RENKLER["bg"], fg=RENKLER["text_dim"]).pack(pady=6)

        for etiket, deger, renk in [
            ("⚡  SPORCU", "sporcu", RENKLER["accent3"]),
            ("🏋  ANTRENÖR / ADMİN", "antrenor", RENKLER["accent2"]),
        ]:
            tk.Button(
                self, text=etiket, font=font("buton"),
                bg=RENKLER["card"], fg=renk,
                activebackground=RENKLER["border"], activeforeground=renk,
                bd=0, relief="flat", padx=20, pady=10, cursor="hand2",
                command=lambda d=deger: self._secim(d)
            ).pack(fill="x", padx=50, pady=6)

    def _secim(self, tur):
        self.callback(tur)
        self.destroy()


class SporciuKayitDialog(simpledialog.Dialog):
    """Yeni sporcu kayıt diyaloğu."""

    def __init__(self, parent):
        self.sonuc = None
        super().__init__(parent, title="Yeni Sporcu Kaydı")

    def body(self, master):
        master.configure(bg=RENKLER["bg"])
        for i, (lbl, attr) in enumerate([("Ad Soyad:", "ad"),
                                         ("Kilo (kg):", "kilo"),
                                         ("Boy (cm):", "boy")]):
            tk.Label(master, text=lbl, bg=RENKLER["bg"], fg=RENKLER["text"],
                     font=font("etiket")).grid(row=i, column=0, padx=12, pady=6, sticky="e")
            entry = tk.Entry(master, bg=RENKLER["card"], fg=RENKLER["accent1"],
                             insertbackground=RENKLER["accent1"],
                             font=font("etiket"), bd=0, relief="flat", width=22)
            entry.grid(row=i, column=1, padx=8, pady=6)
            setattr(self, f"_{attr}_entry", entry)
        return self._ad_entry

    def apply(self):
        try:
            ad = self._ad_entry.get().strip()
            kilo = float(self._kilo_entry.get())
            boy = float(self._boy_entry.get())
            if not ad:
                raise ValueError("Ad boş olamaz.")
            self.sonuc = (ad, kilo, boy)
        except ValueError as e:
            messagebox.showerror("Hata", str(e))


class AntrenmanDialog(simpledialog.Dialog):
    """Antrenman ekleme diyaloğu."""

    def __init__(self, parent, sporcular):
        self.sporcular = sporcular
        self.sonuc = None
        super().__init__(parent, title="Antrenman Ekle")

    def body(self, master):
        master.configure(bg=RENKLER["bg"])
        # Sporcu seçimi
        tk.Label(master, text="Sporcu:", bg=RENKLER["bg"], fg=RENKLER["text"],
                 font=font("etiket")).grid(row=0, column=0, padx=12, pady=6, sticky="e")
        self._sporcu_var = tk.StringVar()
        sporcu_listesi = [f"{s.ad} ({s.sporcu_id})" for s in self.sporcular]
        self._sporcu_cb = ttk.Combobox(master, textvariable=self._sporcu_var,
                                       values=sporcu_listesi, state="readonly", width=24)
        self._sporcu_cb.grid(row=0, column=1, padx=8, pady=6)
        if sporcu_listesi:
            self._sporcu_cb.current(0)

        # Antrenman türü
        tk.Label(master, text="Tür:", bg=RENKLER["bg"], fg=RENKLER["text"],
                 font=font("etiket")).grid(row=1, column=0, padx=12, pady=6, sticky="e")
        self._tur_var = tk.StringVar()
        self._tur_cb = ttk.Combobox(master, textvariable=self._tur_var,
                                    values=list(Antrenman.MET_DEGERLERI.keys()),
                                    state="readonly", width=24)
        self._tur_cb.grid(row=1, column=1, padx=8, pady=6)
        self._tur_cb.current(0)

        # Tur sayısı ve süre
        for i, (lbl, attr) in enumerate([("Tur Sayısı:", "tur"), ("Süre (dk):", "sure")]):
            tk.Label(master, text=lbl, bg=RENKLER["bg"], fg=RENKLER["text"],
                     font=font("etiket")).grid(row=i + 2, column=0, padx=12, pady=6, sticky="e")
            entry = tk.Entry(master, bg=RENKLER["card"], fg=RENKLER["accent1"],
                             insertbackground=RENKLER["accent1"],
                             font=font("etiket"), bd=0, relief="flat", width=24)
            entry.grid(row=i + 2, column=1, padx=8, pady=6)
            setattr(self, f"_{attr}_entry", entry)
        return self._sporcu_cb

    def apply(self):
        try:
            secili = self._sporcu_var.get()
            sporcu_id = secili.split("(")[-1].rstrip(")")
            tur = self._tur_var.get()
            tur_sayisi = int(self._tur_entry.get())
            sure = float(self._sure_entry.get())
            self.sonuc = (sporcu_id, tur, tur_sayisi, sure)
        except ValueError as e:
            messagebox.showerror("Hata", f"Geçersiz değer: {e}")


class AnaSayfa(tk.Frame):
    """Ana uygulama çerçevesi – tüm paneller burada toplanır."""

    def __init__(self, parent, sistem: FitnessSistemi, kullanici_turu: str):
        super().__init__(parent, bg=RENKLER["bg"])
        self.sistem = sistem
        self.kullanici_turu = kullanici_turu
        self.pack(fill="both", expand=True)
        self._olustur()
        self._demo_veri_yukle()
        self._tablo_guncelle()

    def _demo_veri_yukle(self):
        """Test: 2 demo sporcu ve birkaç antrenman kaydı."""
        try:
            s1 = self.sistem.sporcu_ekle("Ahmet Yılmaz", 80, 178)
            s2 = self.sistem.sporcu_ekle("Zeynep Kaya", 62, 165)
            self.sistem.antrenman_ekle(s1.sporcu_id, "Koşu", 3, 40)
            self.sistem.antrenman_ekle(s1.sporcu_id, "Ağırlık", 4, 60)
            self.sistem.antrenman_ekle(s2.sporcu_id, "Yoga", 2, 50)
            self.sistem.antrenman_ekle(s2.sporcu_id, "HIIT", 5, 30)
        except Exception:
            pass  # demo veride hata olursa sessizce geç

    def _olustur(self):
        # ── Başlık ──────────────────────────────────────────────────
        baslik_frame = tk.Frame(self, bg=RENKLER["bg"])
        baslik_frame.pack(fill="x", padx=20, pady=(20, 0))

        tk.Label(baslik_frame, text="⚡ FITNESS TAKİP SİSTEMİ",
                 font=font("baslik"), bg=RENKLER["bg"],
                 fg=RENKLER["accent1"]).pack(side="left")

        tur_lbl = ("🏋 ANTRENÖR MODU" if self.kullanici_turu == "antrenor"
                   else "⚡ SPORCU MODU")
        tk.Label(baslik_frame, text=tur_lbl, font=font("etiket"),
                 bg=RENKLER["bg"], fg=RENKLER["accent2"]).pack(side="right", pady=8)

        tk.Label(self, text="─" * 100, bg=RENKLER["bg"],
                 fg=RENKLER["border"]).pack(fill="x", padx=20)

        # ── İçerik alanı ────────────────────────────────────────────
        icerik = tk.Frame(self, bg=RENKLER["bg"])
        icerik.pack(fill="both", expand=True, padx=20, pady=10)

        sol = tk.Frame(icerik, bg=RENKLER["bg"])
        sol.pack(side="left", fill="y", padx=(0, 12))

        sag = tk.Frame(icerik, bg=RENKLER["bg"])
        sag.pack(side="left", fill="both", expand=True)

        self._butonlar_olustur(sol)
        self._tablo_olustur(sag)
        self._durum_cubugu_olustur()

    def _butonlar_olustur(self, parent):
        butonlar = [
            ("➕ Yeni Sporcu", self._sporcu_ekle, RENKLER["accent3"]),
            ("🏃 Antrenman Ekle", self._antrenman_ekle, RENKLER["accent1"]),
            ("📊 Günlük Rapor", self._gunluk_rapor, RENKLER["warning"]),
            ("📅 Haftalık Rapor", self._haftalik_rapor, RENKLER["warning"]),
            ("🔄 Yenile", self._tablo_guncelle, RENKLER["text_dim"]),
        ]
        if self.kullanici_turu == "sporcu":
            butonlar = butonlar[:2] + butonlar[2:]

        tk.Label(parent, text="MENÜ", font=font("panel"),
                 bg=RENKLER["bg"], fg=RENKLER["text_dim"]).pack(pady=(0, 10))

        for etiket, komut, renk in butonlar:
            tk.Button(
                parent, text=etiket, font=font("buton"),
                bg=RENKLER["card"], fg=renk, bd=0, relief="flat",
                padx=14, pady=10, width=20, cursor="hand2",
                activebackground=RENKLER["border"], activeforeground=renk,
                command=komut
            ).pack(pady=4, fill="x")

    def _tablo_olustur(self, parent):
        """Sporcu listesi tablosu."""
        tk.Label(parent, text="SPORCU LİSTESİ", font=font("panel"),
                 bg=RENKLER["bg"], fg=RENKLER["text_dim"]).pack(anchor="w", pady=(0, 6))

        sutunlar = ["ID", "Ad", "Kilo", "Boy", "BMI", "Hf. Kalori", "Toplam Antr."]
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("Custom.Treeview",
                        background=RENKLER["card"],
                        foreground=RENKLER["text"],
                        rowheight=28,
                        fieldbackground=RENKLER["card"],
                        borderwidth=0,
                        font=("Courier", 10))
        style.configure("Custom.Treeview.Heading",
                        background=RENKLER["panel"],
                        foreground=RENKLER["accent1"],
                        font=("Courier", 10, "bold"),
                        relief="flat")
        style.map("Custom.Treeview",
                  background=[("selected", RENKLER["border"])],
                  foreground=[("selected", RENKLER["accent1"])])

        self.tablo = ttk.Treeview(parent, columns=sutunlar, show="headings",
                                  style="Custom.Treeview", height=14)
        genislikler = [80, 140, 70, 70, 70, 100, 110]
        for s, g in zip(sutunlar, genislikler):
            self.tablo.heading(s, text=s)
            self.tablo.column(s, width=g, anchor="center")

        sb = ttk.Scrollbar(parent, orient="vertical", command=self.tablo.yview)
        self.tablo.configure(yscrollcommand=sb.set)
        self.tablo.pack(side="left", fill="both", expand=True)
        sb.pack(side="left", fill="y")

    def _durum_cubugu_olustur(self):
        self.durum_var = tk.StringVar(value="Sistem hazır.")
        tk.Label(self, textvariable=self.durum_var, font=font("kucuk"),
                 bg=RENKLER["border"], fg=RENKLER["text_dim"],
                 anchor="w", padx=10, pady=4).pack(fill="x", side="bottom")

    # ── Eylemler ────────────────────────────────────────────────────

    def _sporcu_ekle(self):
        dlg = SporciuKayitDialog(self.winfo_toplevel())
        if dlg.sonuc:
            try:
                ad, kilo, boy = dlg.sonuc
                s = self.sistem.sporcu_ekle(ad, kilo, boy)
                self._tablo_guncelle()
                self._durum_guncelle(
                    f"✅ Sporcu eklendi: {s.ad} | ID: {s.sporcu_id}", RENKLER["accent3"])
            except ValueError as e:
                messagebox.showerror("Hata", str(e))

    def _antrenman_ekle(self):
        if not self.sistem.sporcular:
            messagebox.showwarning("Uyarı", "Önce sporcu eklemelisiniz.")
            return
        dlg = AntrenmanDialog(self.winfo_toplevel(), self.sistem.sporcular)
        if dlg.sonuc:
            try:
                sporcu_id, tur, tur_sayisi, sure = dlg.sonuc
                ozet = self.sistem.antrenman_ekle(sporcu_id, tur, tur_sayisi, sure)
                self._tablo_guncelle()
                self._durum_guncelle(
                    f"🏃 Antrenman eklendi | {tur} | {tur_sayisi} tur | "
                    f"{sure} dk | 🔥 {ozet['kalori']} kcal", RENKLER["accent1"])
            except ValueError as e:
                messagebox.showerror("Hata", str(e))

    def _gunluk_rapor(self):
        sporcu = self._secili_sporcu()
        if not sporcu:
            return
        rapor = self.sistem.gunluk_rapor(sporcu.sporcu_id)
        if not rapor:
            messagebox.showinfo("Günlük Rapor", "Henüz antrenman kaydı yok.")
            return
        mesaj = f"📊 {sporcu.ad} – Günlük Kalori Raporu\n{'─'*40}\n"
        for gun, bilgi in sorted(rapor.items(), reverse=True):
            mesaj += (f"  {gun}  →  🔥 {bilgi['toplam_kalori']:.1f} kcal  "
                      f"|  {bilgi['antrenman_sayisi']} antrenman\n")
        messagebox.showinfo("Günlük Rapor", mesaj)

    def _haftalik_rapor(self):
        sporcu = self._secili_sporcu()
        if not sporcu:
            return
        rapor = self.sistem.haftalik_rapor(sporcu.sporcu_id)
        mesaj = (f"📅 {sporcu.ad} – Haftalık Rapor (Son 7 Gün)\n{'─'*40}\n"
                 f"  Toplam Kalori  : 🔥 {rapor['toplam_kalori']} kcal\n"
                 f"  Antrenman Sayısı: {rapor['antrenman_sayisi']}\n"
                 f"  BMI            : {sporcu.bmi_hesapla()}")
        messagebox.showinfo("Haftalık Rapor", mesaj)

    def _tablo_guncelle(self):
        for row in self.tablo.get_children():
            self.tablo.delete(row)
        for ozet in self.sistem.tum_sporcular_ozet():
            self.tablo.insert("", "end", values=(
                ozet["sporcu_id"],
                ozet["ad"],
                f"{ozet['kilo']} kg",
                f"{ozet['boy']} cm",
                ozet["bmi"],
                f"{ozet['haftalik_kalori']} kcal",
                ozet["toplam_antrenman"],
            ))

    def _secili_sporcu(self) -> Sporcu | None:
        """Tabloda seçili sporcu varsa onu döner, yokسا ilk sporcuyu seçer."""
        secili = self.tablo.selection()
        if secili:
            sporcu_id = self.tablo.item(secili[0])["values"][0]
            return self.sistem.sporcu_bul(sporcu_id)
        elif self.sistem.sporcular:
            # Seçim yoksa dialog ile sor
            isimler = [f"{s.ad} ({s.sporcu_id})" for s in self.sistem.sporcular]
            secim = simpledialog.askstring(
                "Sporcu Seçin",
                "Sporcu ID veya adı:\n" + "\n".join(isimler),
                parent=self.winfo_toplevel()
            )
            if secim:
                for s in self.sistem.sporcular:
                    if secim.upper() in s.sporcu_id or secim.lower() in s.ad.lower():
                        return s
            messagebox.showwarning("Uyarı", "Sporcu bulunamadı.")
        else:
            messagebox.showwarning("Uyarı", "Sistemde sporcu yok.")
        return None

    def _durum_guncelle(self, mesaj: str, renk: str = RENKLER["text_dim"]):
        self.durum_var.set(mesaj)


# ─────────────────────────────────────────────
#  ANA GİRİŞ NOKTASI
# ─────────────────────────────────────────────

def main():
    sistem = FitnessSistemi()
    pencere = tk.Tk()
    pencere.title("Fitness Takip Sistemi")
    pencere.configure(bg=RENKLER["bg"])
    pencere.geometry("900x580")
    pencere.minsize(820, 500)

    ana_sayfa_ref = [None]

    def kullanici_secildi(tur: str):
        ana_sayfa_ref[0] = AnaSayfa(pencere, sistem, tur)

    # Giriş ekranı önce açılır
    GirisEkrani(pencere, kullanici_secildi)
    pencere.mainloop()


if __name__ == "__main__":
    main()