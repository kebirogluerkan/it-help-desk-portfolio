# Projeyi Mülakatta Anlatma Rehberi

## 30 saniyelik anlatım

"IT Help Desk süreçlerini uygulamalı göstermek için 420 sentetik talepten oluşan bir portföy projesi hazırladım. Talepleri kategori, öncelik, durum ve SLA bilgileriyle modelledim; veriyi SQLite'a aktardım ve SQL sorgularıyla backlog, çözüm süresi, SLA ve memnuniyet analizleri yaptım. Ayrıca yaygın Windows, donanım ve ağ sorunları için standart sorun giderme ve eskalasyon dokümanı oluşturdum. Veri kalitesini otomatik testlerle kontrol ettim ve sonuçları dashboard üzerinde raporladım."

## Muhtemel sorular

### Neden sentetik veri kullandın?

Gerçek destek kayıtları kişisel ve kurumsal hassas bilgiler içerebilir. Bu nedenle gerçekçi dağılıma sahip ancak kimseye ait olmayan, tekrar üretilebilir bir veri seti oluşturdum.

### Ticket önceliğini nasıl belirledin?

Etki ve aciliyet yaklaşımını kullandım. Çok sayıda kullanıcıyı veya kritik iş sürecini durduran olayları Critical; sınırlı etkili ve geçici çözümü olan olayları Medium veya Low olarak sınıflandırdım.

### SLA nedir?

Hizmet seviyesini ölçmek için belirlenen hedef süredir. Projede öncelik seviyesine göre çözüm hedefleri kullandım ve çözülen kayıtların hedef içinde kalıp kalmadığını hesapladım.

### Sorunu çözemediğinde ne yaparsın?

Belirtiyi, kapsamı, hata mesajını, uyguladığım adımları ve sonuçlarını ticket içine yazarım. Yetki, güvenlik, sunucu, ağ veya veri kaybı riski varsa doğru ekibe eksiksiz bilgiyle eskale ederim.

### En önemli KPI hangisi?

Tek bir KPI yeterli değildir. SLA uyumu hız hakkında bilgi verirken tekrar açılma ve memnuniyet kaliteyi gösterir. Backlog ise ekibin mevcut iş yükünü anlamaya yardımcı olur.

### Veri kalitesini nasıl kontrol ettin?

Benzersiz ticket kimliği, izin verilen durum/öncelik değerleri, çözülmüş kayıtların zorunlu alanları, SLA hesaplama tutarlılığı ve kişisel veri benzeri desenler için otomatik kontroller yazdım.

### SQL'i nerede kullandın?

KPI özeti, kategori dağılımı, açık backlog, aylık hacim, SLA performansı, tekrar açılma oranı ve ekip performansı için sorgular oluşturdum.

### Projeyi geliştirsen ne eklersin?

Active Directory laboratuvarı, gerçek bir açık kaynak ticket sistemi entegrasyonu, bilgi bankası araması ve rol bazlı web arayüzü eklerdim.

## Dürüstlük sınırı

Bu proje bir portföy laboratuvarıdır; gerçek şirket üretim ortamı deneyimi değildir. Mülakatta "uygulamalı portföy projesi" olarak anlatılmalıdır.
