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

## 💻 Çalıştırma

Uygulamayı başlatmak için GUI dosyasını çalıştırmanız yeterlidir:

```bash
python fitness_gui.py
```

## 📈 المنطق الحسابي

*   **BMI:** يتم حسابه بتقسيم الوزن على مربع الطول بالمتر.
*   **السعرات الحرارية:** `MET * الوزن (كجم) * الوقت (ساعة) * معامل الجولات`.
    *   *ملاحظة: كل جولة إضافية بعد الجولة الأولى تزيد من كفاءة حرق السعرات بنسبة 10%.*

---
**ملاحظة:** تم تصميم هذا النظام كنموذج تعليمي واحترافي يجمع بين تقنيات البرمجة كائنية التوجه (OOP) وتصميم واجهات المستخدم.

تم التطوير بواسطة نظام 