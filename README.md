# Fitness Takip Sistemi 🏋️‍♂️⚡

Sporcuların fiziksel aktivitelerini yönetmek için tasarlanmış, Python tabanlı ve modern bir grafik arayüze sahip kapsamlı bir projedir. Proje, geliştirme ve bakım kolaylığı sağlamak için İş Mantığı (Backend) ve Kullanıcı Arayüzü (GUI) katmanlarını birbirinden ayıracak şekilde yapılandırılmıştır.

## 🚀 Temel Özellikler

*   **Sporcu Yönetimi:** Sporcu bilgilerinin (Ad, Kilo, Boy) kaydedilmesi ve otomatik Vücut Kitle İndeksi (BMI) hesaplanması.
*   **Gelişmiş Antrenman Sistemi:** Geniş yelpazede antrenman desteği (Koşu, Yüzme, Ağırlık, Yoga, HIIT, vb.).
*   **Hassas Kalori Hesaplama:** MET (Metabolik Eşdeğer) değerlerine dayalı, tur sayısı ve süreyi hesaba katan gelişmiş hesaplama mantığı.
*   **İstatistiksel Raporlar:** Performans ve kalori tüketimini izlemek için günlük ve haftalık detaylı raporlar.
*   **Profesyonel Kullanıcı Arayüzü:** `tkinter` kütüphanesi kullanılarak tasarlanmış, modern ve fütüristik Karanlık Mod (Dark Mode) arayüzü.
*   **Çoklu Rol Desteği:** Sporcular (veri girişi) ve Antrenörler (tüm verileri inceleme) için özel çalışma modları.

## 🏗️ Proje Yapısı

Proje, en iyi yazılım pratiklerini takip etmek amacıyla iki ana dosyaya ayrılmıştır:

1.  **`akip.py` (İş Mantığı - Backend):**
    *   Temel sınıfları içerir: `Sporcu`, `Antrenman`, `TakipKaydi`.
    *   `FitnessSistemi` üzerinden tüm hesaplamaları ve veri yönetimini sağlar.
    *   Veri erişimini kolaylaştırmak için Facade tasarım desenini kullanır.

2.  **`fitness_gui.py` (Kullanıcı Arayüzü - GUI):**
    *   Pencerelerin, menülerin ve tabloların oluşturulmasından sorumludur.
    *   Verileri işlemek ve görüntülemek için Backend dosyası ile iletişim kurar.

## 🛠️ Teknik Gereksinimler

*   **Python 3.x**
*   Yerleşik Kütüphaneler: `tkinter`, `datetime`, `collections`, `uuid`.
*   Önerilen Yazı Tipleri (Opsiyonel): `Orbitron`, `Share Tech Mono` (Yüklü değilse sistem otomatik olarak alternatif yazı tiplerine geçer).




* bu proje eğitim amaclı geliştirilmiştir *
