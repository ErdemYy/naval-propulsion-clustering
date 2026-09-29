# Canlı Uygulama Gösterim Kılavuzu (5–7 Dakika)

**Uygulama:** Streamlit Yerel Karar Destek Paneli (`app/main.py`)  
**Ortam:** Yerel Windows Bilgisayar (Çevrimdışı / İnternetsiz)  
**Komut:** `streamlit run app/main.py`  
**Adres:** `http://localhost:8501`  

---

## 1. Gösterim Öncesi Hazırlık Kontrol Listesi
- [ ] Terminalde `streamlit run app/main.py` çalıştırılmış olmalı.
- [ ] Tarayıcı `http://localhost:8501` adresinde tam ekran açılmış olmalı.
- [ ] Sol menüden **"1. Overview"** seçili olmalı.
- [ ] Yedek Plan: İnternet veya yazılım çökmesi durumunda `reports/figures/` altındaki yüksek çözünürlüklü görseller sunum klasöründe hazır bulundurulmalıdır.

---

## 2. Adım Adım Canlı Gösterim Akışı

### Adım 1: Uygulama Başlangıcı ve Genel Bakış (0:00 – 1:00)
- **Ekran / Sayfa:** `1. Overview`
- **Tıklanacak Eleman:** Sayfayı yukarıdan aşağıya yavaşça kaydırın.
- **Ekranda Görünen:** 4 adet metrik kartı (11.934 Satır, 18 Ham Sensör, 11 Kümeleme Özelliği, 9 Hız Rejimi) ve Birincil / İkincil model özet kutuları.
- **Konuşmacının Söyleyecekleri:**  
  *"Değerli hocalarım, şu anda sistemimizde tamamen yerel olarak çalışan Streamlit karar destek panelimizi görüyorsunuz. Veri setimiz 11.934 satırdan oluşmakta ve tüm boru hattı sıfır hedef sızıntısı ilkesiyle çalışmaktadır. Sayfanın alt kısmında metodoloji akış şemamızı ve model mühürlerimizi görebilirsiniz."*

---

### Adım 2: Hız Baskınlığı ve Normalizasyonun Gösterimi (1:00 – 2:00)
- **Ekran / Sayfa:** Sol menüden `2. Operating Regime Analysis` seçin.
- **Tıklanacak Eleman:** Sayfadaki karşılaştırma kartlarını gösterin.
- **Ekranda Görünen:** 
  - R1: ARI = 0.8769
  - R2: ARI = 0.8440
  - R5: ARI = 0.0002
  - Alt tarafta `variance_by_operating_regime.png` ve `k_vs_speed_recovery_ari.png` grafikleri.
- **Konuşmacının Söyleyecekleri:**  
  *"Bu sayfada araştırmamızın temel metodolojik çıkış noktasını görüyoruz. Sol kartta göreceğiniz üzere, ham telemetride yapılan kümeleme doğrudan gemi hızını bulmaktadır (ARI = 0.876). Hız sütununu çıkardığımızda (R2), fiziksel kuplaj nedeniyle model yine hızı kümelemektedir (ARI = 0.844). Sağdaki kartta ise geliştirdiğimiz Hız İçi Normalizasyon (R5) ile bu bağımlılığın 0.0002'ye indirilerek hız etkisinin tamamen yok edildiği görülmektedir."*

---

### Adım 3: Birincil Model (K=2) Kompresör Ayrışımı (2:00 – 3:15)
- **Ekran / Sayfa:** Sol menüden `3. Primary Degradation Profile (K=2)` seçin.
- **Tıklanacak Eleman:** Sayfadaki Küme 0 ve Küme 1 kartlarını ve altındaki telemetri profil grafiğini işaret edin.
- **Ekranda Görünen:**
  - Silüet: 0.2813
  - Hız ARI: 0.0002
  - kMc Cliff's delta: +0.771 (Büyük Etki)
  - Küme 0 (n=5.939, %49,8) ve Küme 1 (n=5.995, %50,2) kartları.
  - Altta hızlara göre küme oranları grafiği (%46,9 - %53,1 dengeli).
- **Konuşmacının Söyleyecekleri:**  
  *"Birincil modelimiz olan K=2 çözümünü incelediğimizde, modelin veriyi %50-%50 dengeli iki kümeye ayırdığını görüyoruz. Kümeleme sonrasında zemin gerçekliği aşınma değerleriyle karşılaştırdığımızda; Küme 0'ın yüksek kompresör sağlığı, Küme 1'in ise kompresör aşınması ile örtüştüğünü ve Cliff's delta etki büyüklüğünün +0,771 ile istatistiksel olarak devasa bir ayrışım sunduğunu doğrulamış bulunuyoruz."*

---

### Adım 4: İkincil Model (K=3) Çok Bileşenli Ayrışım (3:15 – 4:15)
- **Ekran / Sayfa:** Sol menüden `4. Multi-Component Profile (K=3)` seçin.
- **Tıklanacak Eleman:** 3 küme kartını (Nominal, Türbin Bozulması, Kompresör Bozulması) gösterin.
- **Ekranda Görünen:**
  - Küme 1: Nominal Referans ($kMc \approx 0,983, kMt \approx 0,992$)
  - Küme 0: Türbin Bozulması ($kMt \approx 0,982$, Cliff's $d = -0,767$)
  - Küme 2: Kompresör Bozulması ($kMc \approx 0,961$, Cliff's $d = +0,869$)
- **Konuşmacının Söyleyecekleri:**  
  *"K=2 modeli türbin aşınmasına duyarsız kaldığı için, K=3 modelini ikincil çok bileşenli model olarak sakladık. Burada göreceğiniz üzere Küme 0 türbin aşınmasını tek başına izole etmekte, Küme 2 kompresör aşınmasını temsil etmekte, Küme 1 ise her iki bileşenin de sağlıklı olduğu referans rejimini yakalamaktadır."*

---

### Adım 5: 2B Bozulma Izgarası Haritası (4:15 – 5:00)
- **Ekran / Sayfa:** Sol menüden `5. Degradation Map` seçin.
- **Tıklanacak Eleman:** Radyo butonundan önce `Candidate A (K=2)`, ardından `Candidate B (K=3)` seçin.
- **Ekranda Görünen:** 2B $kMc \times kMt$ düzleminde renklendirilmiş ızgara haritası.
- **Konuşmacının Söyleyecekleri:**  
  *"Bu interaktif haritada, modelin 1.326 farklı aşınma durumunda nasıl küme atadığını görüyoruz. Dikkat ederseniz kümeler rastgele dağılmamış; K=2'de düşey bir hat boyunca, K=3'te ise 3 farklı geometrik bölge olarak pürüzsüz biçimde yerleşmiştir. 9 hız arasındaki atama tutarlılığı %82'nin üzerindedir."*

---

### Adım 6: Yeni Gözlem Analizi ve Canlı Test (5:00 – 6:15)
- **Ekran / Sayfa:** Sol menüden `6. New Observation Analysis` seçin.
- **Tıklanacak Eleman:** 
  1. Üstteki butonlardan **"Load Case 2: Compressor Decay"** butonuna basın. (Başarı mesajı belirecektir).
  2. Aşağı kaydırıp mavi renkli **"🚀 Analyze Observation & Assign Profile"** butonuna tıklayın.
- **Ekranda Görünen:**
  - Atanan Küme: `Cluster 1 (Compressor Degradation Association)`
  - Merkez Mesafesi (L2 normu)
  - Post-Hoc Benchmark: True kMc = 0.950 (Aşınmış kompresör), True kMt = 1.000.
  - Altta z-skor sapma grafiği.
- **Konuşmacının Söyleyecekleri:**  
  *"Şimdi canlı bir çıkarım denemesi yapalım. Panelimizdeki 'Case 2: Compressor Decay' butonuna basarak 18 knot seyir hızındaki bir test telemetrisini yüklüyorum. Model bu aşamada aşınma etiketini kesinlikle bilmiyor. 'Analyze Observation' dediğimizde; model bu telemetriyi hız içi normalizasyondan geçirip merkez mesafelerini hesaplıyor ve anında **Küme 1 (Kompresör Bozulması)** profiline atıyor. Alt taraftaki doğrulama kutusunda göreceğiniz üzere, bu gözlemin gerçek zemin değeri $kMc = 0,950$'dir; yani model denetimsiz olarak doğru aşınma durumunu teşhis etmiştir."*

---

### Adım 7: Kapanış ve Sınırlılıklar (6:15 – 7:00)
- **Ekran / Sayfa:** Sol menüden `8. Methodology & Limitations` seçin.
- **Konuşmacının Söyleyecekleri:**  
  *"Son olarak vurgulamak isteriz ki bu sistem simülasyon temelli kararlı durum verisiyle geliştirilmiştir ve canlı bir savaş gemisinde doğrudan operasyonel arıza tahmini iddiası taşımaz. Ancak denetimsiz makine öğrenmesinin doğru normalizasyonla aşınma rejimlerini yakalayabileceğini matematiksel ve deneysel olarak kanıtlamıştır. Dinlediğiniz için teşekkür ederim."*

---

## 3. Yedek Plan (Fail-Safe Scenario)
Eğer sunum bilgisayarında Streamlit port çakışması veya beklenmeyen bir aksaklık yaşanırsa:
1. `reports/figures/phase4/` klasörünü açın.
2. Sırasıyla `degradation_grid_k2.png`, `degradation_grid_k3.png` ve `telemetry_profiles_comparison.png` dosyalarını slaytlardan veya doğrudan resim görüntüleyiciden göstererek yukarıdaki senaryoyu slaytlar üzerinden kesintisiz sürdürün.
