# Veri Sözlüğü

| Alan | Tür | Açıklama |
|---|---|---|
| `ticket_id` | Metin | Benzersiz destek kaydı kimliği |
| `opened_at` | Tarih-saat | Talebin açıldığı zaman |
| `resolved_at` | Tarih-saat | Talebin çözüldüğü zaman; açık kayıtlarda boş |
| `status` | Kategori | Open, In Progress, Resolved veya Closed |
| `priority` | Kategori | Low, Medium, High veya Critical |
| `category` | Kategori | Erişim, yazılım, donanım, ağ, yazıcı veya iletişim |
| `subcategory` | Kategori | Sorunun ayrıntılı sınıfı |
| `channel` | Kategori | Portal, e-posta, telefon veya yüz yüze |
| `requester_department` | Kategori | Talebi açan sentetik departman |
| `assigned_team` | Kategori | Service Desk, Desktop Support veya Network Support |
| `assignee` | Metin | Kişisel veri içermeyen sentetik teknisyen kodu |
| `first_response_minutes` | Tam sayı | İlk yanıt için geçen dakika |
| `resolution_minutes` | Tam sayı | Çözüm için geçen dakika; açık kayıtlarda boş |
| `sla_target_minutes` | Tam sayı | Önceliğe göre hedef çözüm süresi |
| `sla_met` | Kategori | Hedef karşılandıysa Yes, aşılmışsa No |
| `reopened` | Kategori | Kayıt tekrar açıldıysa Yes |
| `satisfaction_score` | Tam sayı | Çözülen talepler için 1-5 memnuniyet puanı |
| `summary` | Metin | Kişisel veri içermeyen kısa sorun açıklaması |
| `resolution_note` | Metin | Uygulanan çözümün genel açıklaması |

## Öncelik ve SLA hedefleri

| Öncelik | Örnek etki | Hedef çözüm süresi |
|---|---|---:|
| Critical | İş birimini durduran yaygın kesinti | 240 dakika |
| High | Kritik kullanıcı veya süreç ciddi şekilde etkileniyor | 480 dakika |
| Medium | Geçici çözüm var, sınırlı kullanıcı etkileniyor | 1.440 dakika |
| Low | Bilgi talebi veya düşük etkili istek | 2.880 dakika |
