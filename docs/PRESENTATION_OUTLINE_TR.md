# Bitirme Tezi ve Proje Savunması Sunum Planı (12–15 Dakika)

**Proje Başlığı:** Deniz Gaz Türbini Tahrik Sistemlerinde Çalışma ve Performans Bozulma Profillerinin Denetimsiz Öğrenme ile Keşfi  
**Hedef Süre:** 12 – 15 Dakika (17 Slayt)  
**Sunum Formatı:** Akademik Mühendislik Sunumu  

---

### Slayt 1: Kapak ve Giriş (0:00 – 0:45)
- **Başlık:** Deniz Gaz Türbini Tahrik Sistemlerinde Çalışma ve Performans Bozulma Profillerinin Denetimsiz Öğrenme ile Keşfi
- **Alt Başlık:** Makine Öğrenmesi Dersi Akademik Araştırma Projesi
- **Öğrenci:** Erdem Y.
- **Amaç:** Projenin akademik bağlamını ve araştırmacı kimliğini tanıtmak.
- **Konuşulacaklar:** *"Sayın jüri üyeleri ve hocalarım, bugün deniz gaz türbini tahrik sistemlerinde çok değişkenli telemetri verilerinden denetimsiz öğrenme yoluyla aşınma profillerinin keşfini ele aldığımız araştırma projemizi sunacağım."*
- **Geçiş Cümlesi:** *"Öncelikle bu araştırmayı tetikleyen temel endüstriyel problemle başlayalım."*

---

### Slayt 2: Problem Tanımı (0:45 – 1:30)
- **Başlık:** Endüstriyel Durum İzlemede Etiket Kıtlığı ve Yük Baskısı
- **Amaç:** Gerçek deniz operasyonlarında arıza etiketlerinin bulunmadığını vurgulamak.
- **Görsel/Vurgu:** Şematik gaz türbini akış diyagramı ve etiketsiz sensör akışı.
- **Konuşulacaklar:** *"Deniz platformlarında ve enerji santrallerinde bileşenlerin gerçek aşınma katsayılarını seyir esnasında doğrudan ölçmek mümkün değildir. Sensörler sürekli veri üretir ancak bu veriler etiketsizdir. Ayrıca operasyonel yük değişimleri, donanım aşınmasından çok daha büyük dalgalanmalara yol açar."*
- **Geçiş Cümlesi:** *"Bu durum bizi doğrudan denetimsiz öğrenme metodolojisine yönlendirmektedir."*

---

### Slayt 3: Neden Kümeleme (Denetimsiz Öğrenme)? (1:30 – 2:15)
- **Başlık:** Denetimsiz Profil Keşfi ve Sızıntısız Tasarım (Rule 1)
- **Amaç:** Projenin neden denetimli sınıflandırma değil, saf kümeleme olduğunu açıklamak.
- **Görsel/Vurgu:** Karantinaya alınan hedefler şeması ($kMc, kMt \rightarrow$ Zemin Gerçekliği).
- **Konuşulacaklar:** *"Çalışmamız bir arıza tahmin veya regresyon projesi değildir. Temel prensibimiz 'Zero-Leakage' yani sıfır veri sızıntısıdır. Kompresör ve türbin aşınma katsayıları model eğitiminden tamamen yalıtılmış, modeller yalnızca etiketsiz telemetri üzerinde eğitilmiştir."*
- **Geçiş Cümlesi:** *"Araştırmamızda kullanılan veri setinin yapısına göz atalım."*

---

### Slayt 4: Veri Seti ve Faktöriyel Tasarım (2:15 – 3:00)
- **Başlık:** UCI Veri Seti #316: Deniz Tahrik Sistemi Kararlı Durum Verisi
- **Amaç:** Veri setinin güvenilirliğini, mühürlü SHA-256 özetini ve faktöriyel ızgarayı sunmak.
- **Görsel/Vurgu:** 11.934 satır $\times$ 18 değişken, $9 \times 51 \times 26$ faktöriyel matris tablosu.
- **Konuşulacaklar:** *"Cenova Üniversitesi tarafından CODAG tahrik simülatöründen üretilen UCI #316 veri setini kullandık. Veri seti 11.934 kararlı durum satırından ve 18 değişkenden oluşmaktadır. Eksik veya mükerrer satır içermemektedir. Sabit sıcaklık/basınç kanalları ve çift tork sensörü elenerek 11 telemetri kanalı seçilmiştir."*
- **Geçiş Cümlesi:** *"Fakat bu veriyi doğrudan kümelemeye çalıştığımızda büyük bir metodolojik engelle karşılaştık."*

---

### Slayt 5: Gizli Metodolojik Engel: Hız Baskınlığı (3:00 – 4:00)
- **Başlık:** Operasyonel Rejim Baskınlığı (%99,33 Varyans)
- **Amaç:** Hız değişkeninin telemetri üzerindeki ezici baskısını ampirik olarak göstermek.
- **Görsel/Vurgu:** [`reports/figures/phase2/variance_by_operating_regime.png`](file:///reports/figures/phase2/variance_by_operating_regime.png)
- **Konuşulacaklar:** *"Tek yönlü varyans analizi (ANOVA) gerçekleştirdiğimizde, gemi hızının ($v$) telemetri değişkenlerindeki varyansın %99,33'ünü açıkladığını keşfettik. PCA analizinde ise PC1 tek başına varyansın %97,41'ini oluşturmaktadır. Yani sensörlerdeki sinyalin neredeyse tamamı makinenin aşınmasını değil, geminin hızını yansıtmaktadır."*
- **Geçiş Cümlesi:** *"Peki bu veriyle naif bir kümeleme yaparsak ne olur?"*

---

### Slayt 6: Naif Kümeleme ve Fiziksel Kuplaj (4:00 – 5:00)
- **Başlık:** Naif Kümeleme Hızı Ayrıştırır, Aşınmayı Göremez
- **Amaç:** R1 ve R2 temsillerinde kümelemenin başarısızlığını (hız kümelemesini) kanıtlamak.
- **Görsel/Vurgu:** [`reports/figures/phase3/k_vs_speed_recovery_ari.png`](file:///reports/figures/phase3/k_vs_speed_recovery_ari.png)
- **Konuşulacaklar:** *"Ham veride (R1) K-Means ($k=9$) çalıştırdığımızda gemi hızını 0,8769 Rand indeksiyle kümelediğini gördük. Daha çarpıcı olanı, hız ve kol pozisyonu değişkenlerini veri setinden tamamen çıkardığımızda (R2), termodinamik kuplaj nedeniyle modelin gemi hızını yine 0,8440 doğrulukla yeniden inşa etmesidir."*
- **Geçiş Cümlesi:** *"Bu problemi çözmek için özgün normalizasyon yaklaşımımızı geliştirdik."*

---

### Slayt 7: Çözüm: Hız İçi Koşullu Normalizasyon (R5) (5:00 – 6:00)
- **Başlık:** Within-Speed Normalization ($R5$ Temsili)
- **Amaç:** Rejim içi normalizasyonun matematiksel mantığını ve hız etkisini nasıl sıfırladığını açıklamak.
- **Görsel/Vurgu:** Formül: $z_{ij} = (x_{ij} - \mu_j(v_i)) / \sigma_j(v_i)$ ve R5 hız ARI grafiği.
- **Konuşulacaklar:** *"Çözüm olarak her hız kademesi için sensörlerin kendi ortalama ve sapmasını hesaplayarak hız içi z-skor dönüşümü yaptık. Bu işlem sonucunda hızın kümeleme ile olan korelasyonu 0,0002 seviyesine inmiştir. Artık geriye kalan varyans saf bileşen sapmalarını temsil etmektedir."*
- **Geçiş Cümlesi:** *"Şimdi bu temizlenmiş uzayda geliştirdiğimiz Birincil Modele bakalım."*

---

### Slayt 8: Birincil Bilimsel Model (K-Means, K=2) (6:00 – 7:15)
- **Başlık:** Birincil Model: Sade ve Güçlü Kompresör Ayrışımı
- **Amaç:** Aday A modelinin metriklerini ve küme özelliklerini sunmak.
- **Görsel/Vurgu:** Silüet: 0,2813, Hız ARI: 0,0002, Dağılım: %49,8 - %50,2.
- **Konuşulacaklar:** *"R5 uzayında en yüksek silüet değerini (0,2813) veren K-Means ($k=2$) modelini Birincil Model olarak seçtik. Model veriyi neredeyse mükemmel bir %50-%50 dengede iki kümeye ayırmaktadır. 9 hız rejiminin tamamında küme oranları %46,9 ile %52,2 arasında sabit kalarak hızdan bağımsızlığını kanıtlamıştır."*
- **Geçiş Cümlesi:** *"Peki bu iki küme fiziksel olarak ne anlama gelmektedir?"*

---

### Slayt 9: K=2 İstatistiksel Doğrulama ve Etki Büyüklüğü (7:15 – 8:30)
- **Başlık:** Post-Hoc Doğrulama: Kompresör Aşınmasında Büyük Etki ($d = +0,771$)
- **Amaç:** Mann-Whitney U, Cliff's delta ve Benjamini-Hochberg sonuçlarını paylaşmak.
- **Görsel/Vurgu:** İkili karşılaştırma tablosu ve [`reports/figures/phase3/kmc_distribution_by_cluster.png`](file:///reports/figures/phase3/kmc_distribution_by_cluster.png).
- **Konuşulacaklar:** *"Kümeleme bittikten sonra karantinadaki $kMc$ değerlerini incelediğimizde; Küme 0'ın yüksek kompresör sağlığıyla (medyan 0,986), Küme 1'in ise kompresör aşınmasıyla (medyan 0,964) örtüştüğünü gördük. Cliff's delta etki büyüklüğü +0,7709 ile 'Büyük Etki' kategorisindedir. Ancak türbin aşınmasında ($kMt$) etki büyüklüğü ihmal edilebilir düzeydedir ($d=0,132$)."*
- **Geçiş Cümlesi:** *"Türbin aşınmasını da yakalamak mümkün müdür? İşte bu soru bizi İkincil Modele götürdü."*

---

### Slayt 10: İkincil Model: Çok Bileşenli Ayrışım (K=3) (8:30 – 9:45)
- **Başlık:** İkincil Teşhis Modeli: Kompresör ve Türbinin Ortak Keşfi
- **Amaç:** K=3 modelinin türbin bozulmasını nasıl izole ettiğini açıklamak.
- **Görsel/Vurgu:** 3 küme profili kartları ve Cliff's delta ($d = -0,7673$).
- **Konuşulacaklar:** *"K=3 modelini incelediğimizde sistemin üç ayrı rejime ayrıldığını gördük: Küme 1 nominal referans durumu ($kMc \approx 0,983, kMt \approx 0,992$), Küme 0 türbin aşınması ($kMt \approx 0,982$, Cliff's delta = -0,767), Küme 2 ise kompresör aşınması ($kMc \approx 0,961$, Cliff's delta = +0,869). Böylece denetimsiz model iki farklı bileşenin aşınmasını bağımsız olarak ayrıştırmayı başarmıştır."*
- **Geçiş Cümlesi:** *"Bu ayrışımın uzamsal tutarlılığını 2 boyutlu ızgarada test ettik."*

---

### Slayt 11: 2B Faktöriyel Bozulma Izgarası Haritası (9:45 – 10:45)
- **Başlık:** Faktöriyel Aşınma Düzleminde Uzamsal Süreklilik
- **Amaç:** Kümelerin aşınma düzleminde rastgele değil pürüzsüz bölgeler oluşturduğunu göstermek.
- **Görsel/Vurgu:** [`reports/figures/phase4/degradation_grid_k2.png`](file:///reports/figures/phase4/degradation_grid_k2.png) ve `k3.png`.
- **Konuşulacaklar:** *"1.326 hücrelik $kMc \times kMt$ düzlemine baktığımızda kümelerin pürüzsüz ve bitişik geometrik bölgeler oluşturduğunu görüyoruz. 9 farklı seyir hızındaki atama tutarlılığı %82 ile %86 arasındadır. Bu bulgu, modelin rastgele gürültüye değil, kararlı bir manifold yapısına tutunduğunun kanıtıdır."*
- **Geçiş Cümlesi:** *"Sonuçlarımızın rastlantısal olmadığını kanıtlamak için yeniden örnekleme kararlılığını test ettik."*

---

### Slayt 12: Bootstrap ve Kararlılık Analizi (10:45 – 11:30)
- **Başlık:** Yeniden Örnekleme Kararlılığı (B=100 Bootstrap)
- **Amaç:** Modelin rastgele tohumlara ve veri dalgalanmalarına direncini göstermek.
- **Görsel/Vurgu:** [`reports/figures/phase4/bootstrap_stability_distribution.png`](file:///reports/figures/phase4/bootstrap_stability_distribution.png)
- **Konuşulacaklar:** *"Veri setini yerine koyarak 100 kez rastgele yeniden örneklediğimizde K=2 modeli 0,9844 ortalama Rand indeksiyle olağanüstü bir determinizm sergilemiştir (%95 güven aralığı: 0,970 - 0,998). Çoklu başlangıç tohumlarında ise kararlılık %99,94'tür."*
- **Geçiş Cümlesi:** *"Geliştirdiğimiz modelleri interaktif olarak deneyimlemek için yerel bir kontrol paneli inşa ettik."*

---

### Slayt 13: Yerel Streamlit Karar Destek Paneli (11:30 – 12:30)
- **Başlık:** Canlı Akademik Arayüz: Streamlit Dashboard
- **Amaç:** Uygulamanın mimarisini, çevrimdışı çalışabilirliğini ve özelliklerini tanıtmak.
- **Görsel/Vurgu:** Streamlit arayüz ekran görüntüsü veya mimari şeması.
- **Konuşulacaklar:** *"Faz 5'te geliştirdiğimiz Streamlit uygulaması 8 modülden oluşmaktadır. Kesinlikle sessiz yeniden eğitim yapmaz; önceden mühürlenmiş modelleri doğrular. Kullanıcı yeni bir telemetri vektörü girdiğinde hız içi normalizasyonu uygulayıp en yakın küme merkezine olan Öklid mesafesini hesaplar ve fiziksel durum profilini sunar."*
- **Geçiş Cümlesi:** *"Sunumumuzu tamamlarken çalışmamızın sınırlarını açıkça ifade etmek istiyoruz."*

---

### Slayt 14: Akademik Sınırlılıklar ve Kapsam Sınırları (12:30 – 13:30)
- **Başlık:** Bilimsel Dürüstlük: Metodolojik Sınırlılıklar
- **Amaç:** İddia edilmeyen ve sınırları çizilen noktaları dürüstçe vurgulamak.
- **Görsel/Vurgu:** Sınırlılıklar uyarı kutusu (6 temel madde).
- **Konuşulacaklar:** *"Akademik ilkelerimiz gereği altını çiziyoruz: Bu çalışma bir simülasyon veri setidir ve kararlı durum gözlemlerini içerir. Dinamik manevralar ve deniz dalgalanmaları kapsanmamıştır. Bu sistem doğrudan askeri bir gemiye entegre edilemez, gerçek arıza teşhisi veya kalan faydalı ömür tahmini iddiası taşımaz. Yalnızca denetimsiz kümelemenin fiziksel aşınma profilleriyle güçlü birliktelikler keşfettiğini kanıtlar."*
- **Geçiş Cümlesi:** *"Genel bir özetle sunumumu tamamlıyorum."*

---

### Slayt 15: Sonuç ve Katkılar (13:30 – 14:15)
- **Başlık:** Temel Bilimsel Çıkarımlar
- **Amaç:** Projenin 3 ana başarısını özetlemek.
- **Madde Başlıkları:**
  1. Operasyonel hız baskınlığı deneysel olarak gösterilmiş ve aşılmıştır.
  2. Denetimsiz K-Means ($k=2$), sıfır sızıntı ile kompresör aşınmasını başarıyla ayrıştırmıştır ($d = 0,771$).
  3. K-Means ($k=3$), türbin aşınmasını ek bir boyutta başarıyla izole etmiştir ($d = -0,767$).
  4. Tüm pipeline 51 otomatik test ile mühürlenmiş ve yerel yazılımla hayata geçirilmiştir.
- **Geçiş Cümlesi:** *"Dinlediğiniz için teşekkür ederim, sorularınızı yanıtlamaktan memnuniyet duyarım."*

---

### Slayt 16: Teşekkür & Soru - Cevap (14:15 – 15:00)
- **Görsel:** GitHub depo karekodu / linki, iletişim bilgileri.
