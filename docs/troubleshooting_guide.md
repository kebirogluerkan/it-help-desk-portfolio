# IT Destek Sorun Giderme Rehberi

Bu rehber, ilk seviye IT destek akışını göstermek için hazırlanmıştır. Kurumsal ortamlarda şirket prosedürleri, yetkilendirme ve değişiklik yönetimi kuralları önceliklidir.

## Genel yaklaşım

1. Belirtiyi ve kullanıcı etkisini netleştir.
2. Sorunun kapsamını belirle.
3. Son değişiklikleri sor.
4. En düşük riskli kontrolden başla.
5. Yapılan işlemleri ticket içine kaydet.
6. Çözüm doğrulanmazsa geri al veya eskale et.

## 1. Kullanıcı oturum açamıyor

**Kontrol:** Kullanıcı adı, klavye dili, Caps Lock, ağ bağlantısı, hata mesajı ve sorunun başka cihazda tekrarlanıp tekrarlanmadığı.

**İşlem:** Kimlik doğrulama prosedürünü uygula; hesap kilidi veya parola süresi durumunu yetkili araçtan kontrol et. Parola sıfırlama gerekiyorsa şirket politikasına göre yönlendir.

**Eskalasyon:** Birden fazla kullanıcı etkileniyorsa kimlik servisi kesintisi olarak eskale et.

## 2. Windows çok yavaş açılıyor

**Kontrol:** Görev Yöneticisi başlangıç uygulamaları, CPU/RAM/disk kullanımı, boş disk alanı ve son güncellemeler.

**Güvenli komutlar:** `taskmgr`, `msinfo32`, `systeminfo`

**İşlem:** Onaysız başlangıç uygulamalarını kapatma; desteklenen güncellemeleri kontrol etme; disk doluluğunu ve güvenlik taraması durumunu inceleme.

**Eskalasyon:** Disk sağlığı hatası, sürekli %100 kullanım veya donanım arızası belirtisi varsa masaüstü destek ekibine yönlendir.

## 3. Wi-Fi bağlı ancak internet yok

**Kontrol:** Sorun tek cihazda mı, IP adresi ve ağ geçidi alınmış mı, diğer ağ kaynaklarına erişim var mı?

**Komutlar:** `ipconfig /all`, `ping 127.0.0.1`, `ping <gateway>`, `nslookup example.com`, `tracert example.com`

**İşlem:** Adaptör durumunu ve DHCP bilgisini kontrol et; kurumsal prosedür izin veriyorsa bağlantıyı yenile ve bilinen ağı yeniden doğrula.

**Eskalasyon:** Birden fazla kullanıcı veya erişim noktası etkileniyorsa ağ ekibine kapsam ve test sonuçlarıyla eskale et.

## 4. Kablolu bağlantı çalışmıyor

**Kontrol:** Kablo, port ışığı, adaptör durumu, IP yapılandırması ve aynı noktada başka cihaz testi.

**Komutlar:** `ipconfig /all`, `ping <gateway>`, `getmac`

**İşlem:** Fiziksel bağlantıyı doğrula; adaptörü devre dışı bırakıp etkinleştirme gibi işlemleri prosedüre göre uygula.

**Eskalasyon:** Port/VLAN/switch şüphesinde port ve cihaz bilgisiyle ağ ekibine yönlendir.

## 5. Yazıcı çevrimdışı veya kuyrukta bekliyor

**Kontrol:** Güç, kablo/ağ bağlantısı, varsayılan yazıcı, kuyruk, hata ekranı ve başka kullanıcıların durumu.

**İşlem:** Sıkışmış işi kaldır; yazıcı durumunu doğrula; prosedür uygunsa Print Spooler hizmetini kontrollü yeniden başlat; test sayfası al.

**Eskalasyon:** Donanım hatası, sarf malzeme veya ağ yazıcısı erişim sorunu için ilgili ekibe yönlendir.

## 6. Uygulama açılmıyor veya çöküyor

**Kontrol:** Tam hata mesajı, uygulama sürümü, son güncelleme, kullanıcıya özel mi ve sistem kaynakları yeterli mi?

**İşlem:** Uygulamayı güvenli şekilde yeniden başlat; desteklenen güncellemeleri ve uygulama loglarını incele; onaylı onarım prosedürünü uygula.

**Eskalasyon:** Veri kaybı riski, lisans sunucusu veya arka uç hatası varsa uygulama ekibine yönlendir.

## 7. Yazılım kurulumu veya güncellemesi başarısız

**Kontrol:** Yazılım onaylı mı, işletim sistemi uyumlu mu, yeterli alan var mı, hata kodu nedir?

**İşlem:** Kurulum logunu ve hata kodunu kaydet; eski veya çakışan sürümü kontrol et; yalnızca onaylı paketi kullan.

**Eskalasyon:** Yönetici yetkisi, lisans veya merkezi dağıtım sorunu varsa yetkili ekibe aktar.

## 8. USB, klavye, fare veya harici ekran algılanmıyor

**Kontrol:** Farklı port/kablo, başka cihaz testi, Aygıt Yöneticisi durumu ve sürücü uyarısı.

**İşlem:** Fiziksel bağlantıyı doğrula; desteklenen sürücüyü kontrol et; ekran için `Win + P` ve görüntü ayarlarını incele.

**Eskalasyon:** Donanım arızası veya garanti işlemi gerekiyorsa cihaz yönetimi sürecine aktar.

## 9. Disk alanı dolu

**Kontrol:** Depolama ayarları, geçici dosyalar, kullanıcı profili ve kurumsal senkronizasyon durumu.

**İşlem:** Kullanıcı onayı olmadan dosya silme. Desteklenen temizleme aracını kullan; büyük dosyaları raporla; arşivleme politikasına göre yönlendir.

**Eskalasyon:** Profil, kota veya disk kapasitesi değişikliği gerekiyorsa sistem ekibine aktar.

## 10. Mavi ekran veya beklenmeyen yeniden başlatma

**Kontrol:** Stop code, olay zamanı, son sürücü/güncelleme, tekrar sıklığı ve donanım değişikliği.

**Araçlar:** Event Viewer, Reliability Monitor ve onaylı tanılama araçları.

**İşlem:** Stop code ve olay günlüklerini kaydet; veri kaybı riski varsa kullanıcıyı bilgilendir; gelişigüzel sürücü veya kayıt defteri değişikliği yapma.

**Eskalasyon:** Tekrarlayan hata, dump analizi veya donanım şüphesi varsa ikinci seviye desteğe aktar.

## 11. VPN bağlantısı kurulamıyor

**Kontrol:** İnternet erişimi, istemci sürümü, kullanıcı yetkisi, MFA, tarih-saat ve tam hata kodu.

**İşlem:** Onaylı VPN profili ve kimlik doğrulama adımlarını doğrula; kullanıcıya parola veya kod paylaşmamasını hatırlat.

**Eskalasyon:** Çoklu kullanıcı etkisi, sertifika veya ağ geçidi sorunu varsa ağ/güvenlik ekibine aktar.

## 12. Şüpheli e-posta veya güvenlik olayı

**Kontrol:** Kullanıcı bağlantıya tıkladı mı, dosya açtı mı, kimlik bilgisi girdi mi? E-postayı yaymadan başlık ve zaman bilgisini kaydet.

**İşlem:** Kullanıcıdan mesajı yanıtlamamasını ve bağlantıya tıklamamasını iste. Şirketin phishing bildirim kanalını kullan.

**Eskalasyon:** Kimlik bilgisi girilmişse veya dosya çalıştırılmışsa acil güvenlik olayı olarak eskale et. Delilleri silme veya cihazda izinsiz değişiklik yapma.
