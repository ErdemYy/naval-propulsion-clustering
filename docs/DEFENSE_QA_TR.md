# Bitirme Savunması Sıkça Sorulan Sorular ve Kanıta Dayalı Yanıtlar (Defense Q&A)

Bu belge, bitirme projesi savunmasında jüri üyeleri ve ders sorumlusu tarafından yöneltilmesi muhtemel en az 20 kritik soruya yönelik, projede ampirik olarak doğrulanmış kanıtlara dayanan hazır yanıtları içermektedir.

---

### S1: Neden denetimli sınıflandırma (classification) yerine kümeleme (clustering) seçtiniz?
**Yanıt:**  
Gerçek deniz ve endüstriyel operasyonlarda bileşenlerin anlık aşınma katsayılarını ($kMc, kMt$) doğrudan ölçecek sensörler mevcut değildir; bu nedenle sürekli bir zemin gerçekliği etiketi akışı bulunmaz. Amacımız, etiketlerin bulunmadığı gerçekçi bir senaryoda, denetimsiz makine öğrenmesinin yalnızca telemetri sapmalarından anlamlı durum ve aşınma profilleri keşfedip keşfedemeyeceğini kanıtlamaktır. Denetimli bir model eğitmek problemi trivial bir regresyona indirgerdi.

### S2: Neden kMc ve kMt değişkenlerini model girdisi olarak kullanmadınız?
**Yanıt:**  
Bu katı kural projemizin temel invaryantıdır (Rule 1: Zero Data Leakage). $kMc$ ve $kMt$ aşınma katsayılarıdır; eğer bu değişkenleri model girdisi veya özellik mühendisliğinde kullansaydık hedef sızıntısı (target leakage) oluşur ve modelin denetimsizliği geçersiz kılınırdı. Bu değişkenler yalnızca kümeleme tamamlandıktan sonra, bulunan kümelerin fiziksel aşınma ile örtüşüp örtüşmediğini test etmek amacıyla (post-hoc benchmark) kullanılmıştır.

### S3: Gemi hızının veri setini domine ettiğini nasıl kanıtladınız?
**Yanıt:**  
İki matematiksel kanıtımız vardır:
1. Tek yönlü ANOVA testinde, gemi seyir hızı $v$ telemetri değişkenlerindeki toplam varyansın %99,33'ünü açıklamıştır ($\eta^2 \ge 0,965$).
2. PCA analizinde 1. Temel Bileşen (PC1) toplam varyansın %97,41'ini tek başına açıklamış ve 1 boyutlu kararlı durum yük çizgisini temsil etmiştir. Ham veride K-Means ($k=9$) çalıştırıldığında gemi hızı $\text{ARI} = 0,8769$ ile doğrudan kümelenmiştir.

### S4: Neden T1 ve P1 değişkenlerini elediniz?
**Yanıt:**  
Faz 1 ve Faz 2 veri kalitesi denetiminde, Kompresör Giriş Sıcaklığı $T_1$'in tüm 11.934 satırda $288,0$ K, Kompresör Giriş Basıncı $P_1$'in ise $0,998$ bar değerinde sabit kaldığı görülmüştür. Varyansı sıfır olan ($\sigma = 0$) değişkenler hiçbir bilgi taşımaz ve standartlaştırmada sıfıra bölme hatası veya mesafe matrislerinde anlamsız sabit kaymalar oluşturur. Bu nedenle çıkarılmaları zorunludur.

### S5: Neden Tp'yi elediniz ama Ts'yi tuttunuz?
**Yanıt:**  
Veri setinde sancak pervane torku ($T_s$) ile iskele pervane torku ($T_p$) arasındaki mutlak fark tüm satırlarda $0,0000$ kN·m'dir. $T_p$ ve $T_s$ matematiksel olarak birebir klondur. Birebir aynı iki değişkeni modele vermek, tork boyutunun Öklid mesafe hesabında iki kat ağırlıklandırılmasına (yapay çarpıklık) yol açar. Bilgi kaybı olmaksızın simetriyi korumak adına $T_s$ tutulmuş, $T_p$ elenmiştir.

### S6: Neden normalizasyon için StandardScaler tercih ettiniz?
**Yanıt:**  
Faz 2'de StandardScaler, RobustScaler ve MinMaxScaler karşılaştırılmıştır. Veri setimiz simülatör kaynaklı kararlı durum verisi olduğu için rastgele aykırı değer (outlier) veya sensör bozulma gürültüsü içermemektedir (Mahalanobis mesafesinde kritik bir anomali saptanmamıştır). Standart ölçekleyici, tüm sensörlerin birim varyansa getirilmesini sağlayarak devir sayısı (rpm) ve sıcaklık (°C) gibi farklı ölçeklerdeki değişkenlerin mesafeleri adil etkilemesini sağlamıştır.

### S7: Neden kümeleme öncesinde PCA ile boyut indirgemediniz?
**Yanıt:**  
PCA varyansı maksimize eden yönleri bulur. Veri setimizde varyansın %97,41'i PC1'de (hız yük çizgisi) toplanmıştır. Aşınma sinyalleri ise toplam varyansın %1'inden daha azını oluşturan küçük varyanslı alt bileşenlerde (PC3–PC6) yer almaktadır. İlk 2 veya 3 bileşene projeksiyon yapmak, aradığımız aşınma sinyalini gürültü zannedip yok etmekteydi. Bu nedenle PCA bir ön filtre olarak reddedilmiştir.

### S8: Hız İçi Koşullu Normalizasyon (Within-Speed Normalization) nedir ve neden gereklidir?
**Yanıt:**  
Hız değişkenini veriden çıkarsak bile gaz türbininin fiziksel yapısı hızı devir ve sıcaklıklara kuple eder ($\text{ARI} = 0,8440$). Within-Speed Normalization, her ayrık seyir hızı kademesi ($v \in \{3..27\}$) için sensörlerin rejim içi ortalamasını ve sapmasını hesaplayarak veriyi kendi hızı içinde z-skoruna dönüştürür ($z_{ij} = (x_{ij} - \mu_j(v_i))/\sigma_j(v_i)$). Böylece hız etkisi tamamen yok edilir ($\text{ARI} = 0,0002$), geriye yalnızca hızdan arındırılmış aşınma kalıntısı kalır.

### S9: Birincil Model olarak neden K=2 seçildi?
**Yanıt:**  
Occam'ın usturası ilkesi gereği; K=2 modeli R5 uzayında en yüksek silüet değerine ($0,2813$) sahiptir, hız bağımsızlığı mükemmeldir ($\text{ARI} = 0,0002$, hızlar arası küme oranı standart sapması yalnızca %2,22), 100 tekrarlı bootstrap kararlılığı %98,44'tür ve kompresör aşınmasında büyük bir etki büyüklüğü ($d = +0,7709, p < 10^{-100}$) sağlamaktadır. En sade ve en kararlı modeldir.

### S10: Neden K=3 modeli de ikincil model olarak saklandı?
**Yanıt:**  
K=2 modeli silüet açısından güçlü olsa da, etki büyüklüğü analizimiz $k=2$'nin türbin aşınmasına ($kMt$) karşı tamamen kör olduğunu kanıtlamıştır ($d = 0,132$, ihmal edilebilir). K=3 modeli ise kompresör aşınmasının ($d = +0,869$) yanı sıra türbin aşınmasını da bağımsız bir kümede ($d = -0,767$) başarıyla izole etmiştir. Çok bileşenli teşhis araştırmaları için K=3 vazgeçilmez bir tamamlayıcıdır.

### S11: Silüet katsayısı (Silhouette Score) burada ne ifade eder?
**Yanıt:**  
Silüet katsayısı küme içi benzerlik ile en yakın komşu kümeden uzaklığı [-1, +1] aralığında ölçer. Ham veride (R1) $k=9$'da silüetin 0,78 çıkması verinin mükemmel kümelendiğini değil, 9 farklı seyir hızının uzayda birbirinden çok uzak ayrık adalar oluşturduğunu gösterir. R5'te silüetin 0,28'e gerilemesi beklenen bir durumdur; çünkü hız adaları silinmiş, sürekli aşınma manifoldu üzerinde kümeleme yapılmıştır.

### S12: Düzeltilmiş Rand İndeksi (ARI) bu projede neyi ölçmektedir?
**Yanıt:**  
ARI iki farklı kümeleme/etiketleme bölümlemesinin şans faktöründen arındırılmış örtüşmesini [0, 1] aralığında ölçer. Projemizde iki amaçla kullanılmıştır:
1. **Dışsal Hız İyileşme İndeksi:** Modelin bulduğu kümelerin gemi hızı ile örtüşme derecesi (R1'de 0,877 iken R5'te 0,0002'ye indirilmiştir).
2. **Kararlılık İndeksi:** Farklı tohumlar ve bootstrap örneklemleri arasındaki kümeleme tutarlılığı (K=2 için %98,44).

### S13: Post-hoc doğrulamada neden yalnızca p-değerine bakmadınız? Cliff's delta nedir?
**Yanıt:**  
Veri setimizde $N=11.934$ satır vardır. Örneklem sayısı çok büyük olduğunda en önemsiz farklar bile astronomik derecede küçük p-değerleri üretir ($p < 10^{-30}$). Örneğin K=2 modelinde türbin farkı için $p = 6,69 \times 10^{-36}$ çıkmıştır; fakat parametrik olmayan Cliff's delta etki büyüklüğü $d = 0,1321$ ile ihmal edilebilir çıkmıştır. Cliff's delta, bir gruptan seçilen değerin diğerinden büyük olma olasılığını eksi küçük olma olasılığı olarak hesaplar ($d = (2U/n_1n_2)-1$). Yalnızca p-değerine bakılsaydı yanıltıcı bir zafer ilan edilmiş olurdu.

### S14: Bu çalışma bir arıza teşhisi (fault diagnosis) sistemi midir?
**Yanıt:**  
Hayır, kesinlikle değildir. Kümeleme algoritmaları yalnızca etiketsiz telemetrideki benzer veri noktalarını gruplar. Bir makinenin "arızalı" olduğunu iddia etmek alan uzmanlığı, operasyonel limit eşikleri ve kesin arıza kriterleri gerektirir. Modelimiz "arıza teşhisi" yapmaz; donanım aşınmasıyla korelasyon gösteren "durum profillerini" keşfeder.

### S15: Bu çalışma kestirimci bakım (predictive maintenance) veya RUL tahmini midir?
**Yanıt:**  
Hayır. Veri seti kararlı durum simülasyonudur ve zaman boyutu (time dimension) içermemektedir. Zamana bağlı aşınma birikimi, çevrim sayısı veya arızaya kalan süre (Remaining Useful Life - RUL) veride bulunmadığından bir kestirimci bakım veya ömür tahmini iddiası bulunmamaktadır.

### S16: Bu veriler gerçek askeri gemi telemetrisi midir?
**Yanıt:**  
Hayır. UCI #316 veri seti, bir CODAG fırkateyn tahrik sisteminin birinci prensip fiziksel denklemlerine dayanan sayısal bir simülatör çıktısıdır. Gerçek sensör verilerinde bulunan ortam sıcaklık değişimleri, deniz dalga dinamikleri, sensör kalibrasyon kaymaları ve ani gaz kolu geçişleri simülasyonda yer almamaktadır.

### S17: Bu model doğrudan gerçek bir gemiye kurulabilir mi?
**Yanıt:**  
Hayır. Gerçek bir gemide seyir hızı kararlı durumda kalmaz, deniz durumu pervaneye değişken yük bindirir ve sensör gürültüsü vardır. Gerçek bir gemiye kurulmadan önce dinamik rejim normalizasyonu, sensör gürültü filtreleme ve deniz tecrübeleri (sea trials) ile kapsamlı doğrulama gereklidir.

### S18: DBSCAN kümeleme algoritması neden elendi?
**Yanıt:**  
Faz 3'te kapsamlı bir $\epsilon$ ve $min\_samples$ taraması yapılmıştır. Veri setimiz $51 \times 26$ faktöriyel ızgaraya sahip sürekli bir uzaydır; aralarında boş yoğunluk vadileri bulunmamaktadır. DBSCAN düşük yarıçaplarda ($\epsilon \le 1,0$) veriyi onlarca mikro kümeye ve gürültüye parçalamış, $\epsilon \ge 1,5$ olduğunda ise tüm veriyi tek bir dev kümeye toplamıştır. Bu veri morfolojisine uygun değildir.

### S19: Gauss Karışım Modelleri (GMM) neden elendi?
**Yanıt:**  
GMM 11 boyutlu telemetri uzayında tam kovaryans matrisleri ile çalıştırıldığında serbest parametre sayısı çok yükselmiş ve ill-conditioned (kötü koşullanmış) kovaryans matrisleri nedeniyle Davies-Bouldin indeksi $14.785$ gibi devasa değerlere fırlamıştır. K-Means çok daha kararlı ve yorumlanabilir kalmıştır.

### S20: Elinizde gerçek gemi sensör verisi olsaydı yaklaşımınızı nasıl değiştirirdiniz?
**Yanıt:**  
Gerçek veride öncelikle zaman serisi filtrelemesi ve dinamik rejim tespiti yapardık. Sabit hız rejimlerini tespit etmek için kayar pencereli kararlı durum tespit algoritmaları (steady-state detection) kullanır, deniz dalgası gürültüsünü filtrelemek için Kalman veya bant geçiren filtreler uygular, ardından hız içi normalizasyonu bu dinamik pencereler üzerinde yürütürdük.

### S21: Projenizin yazılım mühendisliği güvenceleri nelerdir?
**Yanıt:**  
Projemiz 51 adet otomatik pytest birim ve entegrasyon testiyle %100 kapsama ile mühürlenmiştir. Model manifestosu (`model_manifest.json`) veri seti SHA-256 özetini ve hiperparametreleri denetler. Modeller yerel Windows ortamında sessiz yeniden eğitime izin vermeksizin joblib ile yüklenir ve Streamlit arayüzü tamamen çevrimdışı çalışır.
