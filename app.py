"""
╔══════════════════════════════════════════════════════════════════╗
║           FİTNESS TAKİP SİSTEMİ - Sistem Kullanım Kılavuzu     ║
╠══════════════════════════════════════════════════════════════════╣
║  Kullanıcı Türleri:                                              ║
║    • Sporcu  : Antrenman ve fiziksel verilerini girer            ║
║    • Antrenör: Tüm sporcuların genel verilerini inceler          ║
║                                                                  ║
║  Temel İşlevler:                                                 ║
║    1. Yeni sporcu kaydı oluşturma                                ║
║    2. Antrenman ekleme (tur + süre)                              ║
║    3. Kalori hesaplama ve takibi                                 ║
║    4. Günlük/Haftalık rapor görüntüleme                          ║
║                                                                  ║
║  Backend Mantığı Katmanı                                         ║
╚══════════════════════════════════════════════════════════════════╝
"""

from datetime import datetime, timedelta
from collections import defaultdict
import uuid


# ─────────────────────────────────────────────
#  BACKEND / İŞ MANTIĞI KATMANI
# ─────────────────────────────────────────────

class Sporcu:
    """
    Sporcu sınıfı: Bir sporcunun kişisel bilgilerini ve
    ilerleme geçmişini kapsüller (Encapsulation).
    """

    def __init__(self, ad: str, kilo: float, boy: float):
        self.__sporcu_id = str(uuid.uuid4())[:8].upper()
        self.__ad = ad
        self.__kilo = kilo          # kg
        self.__boy = boy            # cm
        self.__ilerleme_gecmisi = []  # [{"tarih", "kilo", "boy", "bmi"}]

    # --- Getter'lar ---
    @property
    def sporcu_id(self): return self.__sporcu_id

    @property
    def ad(self): return self.__ad

    @property
    def kilo(self): return self.__kilo

    @property
    def boy(self): return self.__boy

    @property
    def ilerleme_gecmisi(self): return list(self.__ilerleme_gecmisi)

    def bmi_hesapla(self) -> float:
        """Mevcut kilo ve boya göre Vücut Kitle İndeksi (BMI) hesaplar."""
        boy_m = self.__boy / 100
        return round(self.__kilo / (boy_m ** 2), 2)

    def ilerleme_kaydet(self, yeni_kilo: float, yeni_boy: float):
        """Kilo ve boy değişimini tarihlendirerek kaydeder."""
        if yeni_kilo <= 0 or yeni_boy <= 0:
            raise ValueError("Kilo ve boy sıfırdan büyük olmalıdır.")
        self.__kilo = yeni_kilo
        self.__boy = yeni_boy
        kayit = {
            "tarih": datetime.now().strftime("%Y-%m-%d %H:%M"),
            "kilo": yeni_kilo,
            "boy": yeni_boy,
            "bmi": self.bmi_hesapla()
        }
        self.__ilerleme_gecmisi.append(kayit)
        return kayit

    def __repr__(self):
        return (f"Sporcu(id={self.__sporcu_id}, ad={self.__ad}, "
                f"kilo={self.__kilo}kg, boy={self.__boy}cm, BMI={self.bmi_hesapla()})")


class Antrenman:
    """
    Antrenman sınıfı: Bir antrenman seansının detaylarını ve
    kalori hesaplama mantığını barındırır.
    """

    # MET (Metabolik Eşdeğer) değerleri – antrenman türüne göre
    MET_DEGERLERI = {
        "Koşu":         9.8,
        "Yüzme":        7.0,
        "Bisiklet":     6.8,
        "Ağırlık":      5.0,
        "Yoga":         2.5,
        "HIIT":        10.0,
        "Yürüyüş":      3.5,
        "Pilates":      3.0,
    }

    def __init__(self, antrenman_turu: str, tur: int, sure: float):
        """
        :param antrenman_turu: Antrenman kategorisi (MET_DEGERLERI anahtarı)
        :param tur: Tamamlanan tur sayısı
        :param sure: Süre (dakika)
        """
        if tur <= 0 or sure <= 0:
            raise ValueError("Tur ve süre sıfırdan büyük olmalıdır.")
        if antrenman_turu not in self.MET_DEGERLERI:
            raise ValueError(f"Geçersiz antrenman türü: {antrenman_turu}")

        self.__antrenman_id = str(uuid.uuid4())[:8].upper()
        self.__antrenman_turu = antrenman_turu
        self.__tur = tur
        self.__sure = sure  # dakika
        self.__tarih = datetime.now()

    # --- Getter'lar ---
    @property
    def antrenman_id(self): return self.__antrenman_id

    @property
    def antrenman_turu(self): return self.__antrenman_turu

    @property
    def tur(self): return self.__tur

    @property
    def sure(self): return self.__sure

    @property
    def tarih(self): return self.__tarih

    def kalori_hesapla(self, sporcu_kilo: float) -> float:
        """
        Kalori = MET × kilo(kg) × süre(saat) × tur_çarpanı
        Tur çarpanı: her tur %10 verimlilik artışı sağlar.
        """
        met = self.MET_DEGERLERI[self.__antrenman_turu]
        sure_saat = self.__sure / 60
        tur_carpani = 1 + (self.__tur - 1) * 0.10
        kalori = met * sporcu_kilo * sure_saat * tur_carpani
        return round(kalori, 1)

    def performans_ozeti(self, sporcu_kilo: float) -> dict:
        """Antrenman performans özetini sözlük olarak döndürür."""
        return {
            "antrenman_id": self.__antrenman_id,
            "tur": self.__antrenman_turu,
            "tur_sayisi": self.__tur,
            "sure_dk": self.__sure,
            "kalori": self.kalori_hesapla(sporcu_kilo),
            "tarih": self.__tarih.strftime("%Y-%m-%d %H:%M")
        }

    def __repr__(self):
        return (f"Antrenman(id={self.__antrenman_id}, tür={self.__antrenman_turu}, "
                f"tur={self.__tur}, süre={self.__sure}dk)")


class TakipKaydi:
    """
    Takip sınıfı: Belirli bir tarihe ait kalori bilgisini
    ve günlük/haftalık istatistik hesaplamalarını yönetir (Composition).
    """

    def __init__(self, tarih: datetime, kalori: float, antrenman_id: str):
        self.__tarih = tarih
        self.__kalori = kalori
        self.__antrenman_id = antrenman_id

    @property
    def tarih(self): return self.__tarih

    @property
    def kalori(self): return self.__kalori

    @property
    def antrenman_id(self): return self.__antrenman_id

    @staticmethod
    def gunluk_istatistik(kayitlar: list) -> dict:
        """
        Verilen kayıt listesinden tarih bazlı istatistik üretir.
        :return: {"YYYY-MM-DD": {"toplam_kalori": float, "antrenman_sayisi": int}}
        """
        gunler = defaultdict(lambda: {"toplam_kalori": 0.0, "antrenman_sayisi": 0})
        for k in kayitlar:
            gun = k.tarih.strftime("%Y-%m-%d")
            gunler[gun]["toplam_kalori"] += k.kalori
            gunler[gun]["antrenman_sayisi"] += 1
        return dict(gunler)

    @staticmethod
    def haftalik_istatistik(kayitlar: list) -> dict:
        """Son 7 günün toplam kalori ve antrenman sayısını döndürür."""
        simdi = datetime.now()
        yedi_gun_once = simdi - timedelta(days=7)
        haftalik = [k for k in kayitlar if k.tarih >= yedi_gun_once]
        toplam_kalori = sum(k.kalori for k in haftalik)
        return {
            "toplam_kalori": round(toplam_kalori, 1),
            "antrenman_sayisi": len(haftalik),
            "gun_sayisi": 7
        }


class FitnessSistemi:
    """
    Ana sistem sınıfı: Tüm veri yapılarını ve iş mantığını
    tek noktadan yönetir (Facade Pattern).

    Veri Yapıları:
      • self.sporcular (list)     : Tüm Sporcu nesneleri
      • self.antrenman_gecmisi (dict): {sporcu_id: [Antrenman, ...]}
      • self.takip_kayitlari (dict) : {sporcu_id: [TakipKaydi, ...]}
    """

    def __init__(self):
        self.sporcular: list[Sporcu] = []
        self.antrenman_gecmisi: dict[str, list[Antrenman]] = defaultdict(list)
        self.takip_kayitlari: dict[str, list[TakipKaydi]] = defaultdict(list)

    # ── SPORCU İŞLEMLERİ ──────────────────────────────────────────

    def sporcu_ekle(self, ad: str, kilo: float, boy: float) -> Sporcu:
        """Yeni sporcu oluşturur ve sisteme kaydeder."""
        sporcu = Sporcu(ad, kilo, boy)
        self.sporcular.append(sporcu)
        return sporcu

    def sporcu_bul(self, sporcu_id: str) -> Sporcu | None:
        """ID'ye göre sporcu arar; bulamazsa None döner."""
        return next((s for s in self.sporcular if s.sporcu_id == sporcu_id), None)

    # ── ANTRENMAN İŞLEMLERİ ───────────────────────────────────────

    def antrenman_ekle(self, sporcu_id: str, tur: str, tur_sayisi: int, sure: float) -> dict:
        """
        Sporcuya yeni antrenman ekler; kaloriyi hesaplayıp takip kaydına yazar.
        :return: Performans özeti sözlüğü
        """
        sporcu = self.sporcu_bul(sporcu_id)
        if not sporcu:
            raise ValueError(f"Sporcu bulunamadı: {sporcu_id}")

        antrenman = Antrenman(tur, tur_sayisi, sure)
        kalori = antrenman.kalori_hesapla(sporcu.kilo)
        ozet = antrenman.performans_ozeti(sporcu.kilo)

        self.antrenman_gecmisi[sporcu_id].append(antrenman)

        takip = TakipKaydi(antrenman.tarih, kalori, antrenman.antrenman_id)
        self.takip_kayitlari[sporcu_id].append(takip)

        return ozet

    # ── RAPOR İŞLEMLERİ ───────────────────────────────────────────

    def gunluk_rapor(self, sporcu_id: str) -> dict:
        kayitlar = self.takip_kayitlari.get(sporcu_id, [])
        return TakipKaydi.gunluk_istatistik(kayitlar)

    def haftalik_rapor(self, sporcu_id: str) -> dict:
        kayitlar = self.takip_kayitlari.get(sporcu_id, [])
        return TakipKaydi.haftalik_istatistik(kayitlar)

    def tum_sporcular_ozet(self) -> list[dict]:
        """Antrenör görünümü: tüm sporcuların özet bilgisi."""
        sonuc = []
        for s in self.sporcular:
            kayitlar = self.takip_kayitlari.get(s.sporcu_id, [])
            haftalik = TakipKaydi.haftalik_istatistik(kayitlar)
            sonuc.append({
                "sporcu_id": s.sporcu_id,
                "ad": s.ad,
                "kilo": s.kilo,
                "boy": s.boy,
                "bmi": s.bmi_hesapla(),
                "haftalik_kalori": haftalik["toplam_kalori"],
                "toplam_antrenman": len(self.antrenman_gecmisi.get(s.sporcu_id, []))
            })
        return sonuc
