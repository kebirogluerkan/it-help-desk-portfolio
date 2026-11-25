# Power BI Dashboard Oluşturma Rehberi

Bu klasör, `data/helpdesk_tickets.csv` dosyasını Power BI Desktop ile görselleştirmek için hazırlanmıştır. `.pbix` dosyası platforma özgü olduğu için repoda doğrulanabilir DAX ölçüleri ve kurulum adımları tutulur.

## 1. Veriyi içeri aktar

1. Power BI Desktop > **Get Data > Text/CSV**
2. `data/helpdesk_tickets.csv` dosyasını seç.
3. Power Query'de veri türlerini kontrol et:
   - Tarih-saat: `opened_at`, `resolved_at`
   - Tam sayı: yanıt, çözüm ve SLA dakika alanları
   - Tam sayı: `satisfaction_score`
4. Tablo adını `Tickets` yap.

## 2. Önerilen sayfalar

### Executive Overview

- Total Tickets
- Open Backlog
- SLA Compliance %
- Average Resolution Hours
- Average CSAT
- Kategori bazında ticket hacmi
- Aylık açılan ve çözülen ticket eğilimi

### SLA & Backlog

- Önceliğe göre SLA uyumu
- Açık ticket sayısı
- Kategori ve önceliğe göre backlog matrisi
- SLA dışı kalan talepler tablosu

### Support Performance

- Ekip ve teknisyen bazında iş yükü
- Ortalama ilk yanıt süresi
- Ortalama çözüm süresi
- Tekrar açılma oranı

## 3. DAX ölçüleri

Hazır ölçüler için [measures.dax](measures.dax) dosyasını kullan.

## 4. Tasarım standardı

- Arka plan: `#F7F9FC`
- Ana renk: `#2563EB`
- Başarı: `#059669`
- Uyarı: `#D97706`
- Kritik: `#DC2626`
- Yazı: `#172033`
- Font: Segoe UI veya IBM Plex Sans

Ekran görüntülerinde kişisel veri veya yerel dosya yolu görünmemelidir.
