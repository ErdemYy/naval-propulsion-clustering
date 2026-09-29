# Deniz Gaz Türbini Tahrik Sistemlerinde Çalışma ve Performans Bozulma Profillerinin Denetimsiz Öğrenme ile Keşfi

**Akademik Proje Bitirme ve Araştırma Raporu**  
**Tarih:** 29 Eylül 2026  
**Alan:** Makine Öğrenmesi, Denetimsiz Öğrenme (Unsupervised Learning) & Kümeleme  
**Veri Seti:** UCI Machine Learning Repository #316 (Naval Propulsion Plants)  
**Yazılım Mimarisi & Kod Deposu:** `naval-propulsion-clustering`  

---

## 1. Kapak Bilgileri

- **Proje Başlığı:** Unsupervised Discovery of Operating and Performance Degradation Profiles in Naval Gas Turbine Propulsion Systems (Deniz Gaz Türbini Tahrik Sistemlerinde Çalışma ve Performans Bozulma Profillerinin Denetimsiz Öğrenme ile Keşfi)
- **Ders / Kapsam:** Makine Öğrenmesine Giriş / Akademik Dönem Bitirme Projesi
- **Öğrenci / Araştırmacı:** Erdem Y.
- **Tarih:** Eylül 2026
- **Kod ve Model Deposu:** [GitHub - ErdemYy/naval-propulsion-clustering](https://github.com/ErdemYy/naval-propulsion-clustering)

---

## 2. Özet

Bu araştırma projesinde, simüle edilmiş bir hücumbot/fırkateyn tipi kombine dizel ve gaz türbini (CODAG) tahrik sistemine ait çok değişkenli telemetri verileri üzerinde denetimsiz öğrenme (kümeleme) algoritmaları uygulanarak çalışma rejimleri ve bileşen performans bozulmalarına (kompresör ve türbin aşınması) ilişkin anlamlı profillerin keşfi incelenmiştir. Literatürde sıkça karşılaşılan operasyonel yük baskınlığı problemi doğrultusunda, gemi seyir hızının ($v$) telemetri değişkenlerindeki toplam varyansın %99,33'ünü açıkladığı saptanmıştır. Ham veya yalnızca ölçeklenmiş veriler üzerinde çalışan saf kümeleme algoritmalarının, donanım aşınmasını değil, doğrudan geminin seyir hızını (Düzeltilmiş Rand İndeksi - $\text{ARI} = 0,8769$) kümelediği gösterilmiştir. Bu metodolojik engeli aşmak amacıyla "hız içi koşullu normalizasyon" (Within-Speed Normalization, $R5$) geliştirilmiş ve seyir hızının kümeleme üzerindeki baskısı $\text{ARI} = 0,0002$'ye düşürülerek izole edilmiştir.

Katı veri sızıntısı önleme protokolü (Rule 1: Zero Data Leakage) kapsamında, kompresör ($kMc$) ve türbin ($kMt$) bozunma katsayıları model eğitiminden tamamen soyutlanmış, yalnızca kümeleme sonrası istatistiksel doğrulama amacıyla kullanılmıştır. $R5$ uzayında eğitilen K-Means ($k=2$) **Birincil Bilimsel Model** olarak seçilmiştir; silüet katsayısı $0,2813$, çoklu başlangıç tohumu kararlılığı $\text{ARI} = 0,9994$ ve 100 tekrarlı bootstrap kararlılığı $\text{ARI} = 0,9844$ olarak ölçülmüştür. Kümeleme sonrası yapılan Mann-Whitney $U$ ve Cliff's delta analizleri, $k=2$ modelinin kompresör aşınmasını büyük bir etki büyüklüğü ile ($d = +0,7709, \eta^2 = 0,4459, p < 10^{-100}$) başarıyla ayrıştırdığını kanıtlamıştır. Türbin aşınmasının da eş zamanlı ayrıştırılmasını inceleyen K-Means ($k=3$) ise **İkincil Çok Bileşenli Teşhis Modeli** olarak korunmuş; kompresör ($d = +0,8689$) ve türbin ($d = -0,7673$) bozulmalarını üç ayrı termodinamik rejimde başarıyla ayrıştırmıştır. Çalışma, doğrulanmış modelleri içeren yerel ve çevrimdışı bir Streamlit arayüzü ile desteklenmiştir.

---

## 3. Anahtar Kelimeler

Denetimsiz Öğrenme, K-Means Kümelemesi, Deniz Gaz Türbinleri, Veri Sızıntısı İnvaryantı, Çalışma Rejimi Normalizasyonu, Cliff's Delta, Bootstrap Kararlılığı.

---

## 4. Giriş

Karmaşık mühendislik sistemlerinde durum izleme ve tahmine dayalı bakım çalışmaları çoğunlukla etiketli arıza verilerine dayanan denetimli öğrenme yöntemleriyle yürütülmektedir. Ancak askeri gemi tahrik sistemleri ve endüstriyel gaz türbinlerinde gerçek arıza veya aşınma etiketlerinin seyir esnasında elde edilmesi maliyetli, tehlikeli ve çoğu zaman imkânsızdır. Sensör ölçümleri çoğunlukla etiketsiz olarak akmaktadır.

Bu çalışma, denetimsiz makine öğrenmesi yaklaşımlarının, tahrik sistemi telemetrisinden etiketsiz olarak fiziksel ve termodinamik açıdan tutarlı aşınma profilleri çıkarıp çıkaramayacağını araştırmaktadır. Çalışmanın temel odağı, denetimli bir sınıflandırma problemi kurmak değil; tamamen etiketsiz veriden yapı keşfetmek ve bulunan kümeleri bağımsız zemin gerçekliği göstergeleriyle istatistiksel olarak doğrulamaktır.

---

## 5. Problem Tanımı

Endüstriyel gaz türbini telemetrisi incelenirken karşılaşılan iki temel metodolojik zorluk bulunmaktadır:
1. **Operasyonel Yük Baskınlığı (Operational Regime Dominance):** Bir geminin seyir hızı veya yük talebi değiştikçe yakıt akışı, devir sayıları ve sıcaklıklar dramatik biçimde değişir. Bu operasyonel değişim, aşınma kaynaklı termodinamik sapmalardan katbekat büyüktür. Naif kümeleme yapıldığında algoritma yalnızca geminin hızlı mı yavaş mı gittiğini kümelemekte, aşınmayı görememektedir.
2. **Veri Sızıntısı Riski (Data Leakage):** Literatürdeki birçok çalışmada, aşınma etiketleri normalizasyon, özellik seçimi veya küme sayısı belirleme adımlarında örtük olarak kullanılmakta ve bu durum modelin denetimsiz niteliğini geçersiz kılmaktadır.

---

## 6. Araştırma Sorusu

> **Temel Bilimsel Araştırma Sorusu:**  
> *Simüle edilmiş bir deniz gaz türbini tahrik sisteminde, baskın operasyonel seyir hızı koşulu kontrol altına alındığında; denetimsiz makine öğrenmesi algoritmaları, model eğitimine hiçbir aşınma etiketi verilmeksizin, kompresör ve türbin performans bozulmasıyla ilişkili anlamlı durum profillerini keşfedebilir mi?*

---

## 7. Veri Seti

Araştırmada İtalya Cenova Üniversitesi araştırmacıları (Coraddu ve ark.) tarafından geliştirilen ve UCI Machine Learning Repository bünyesinde 316 kimlik numarasıyla arşivlenen **Condition Based Maintenance of Naval Propulsion Plants** veri seti kullanılmıştır.
- **Gözlem Sayısı ($N$):** 11.934 satır (kararlı durum simülasyonu).
- **Orijinal Değişken Sayısı:** 18 adet sürekli numerik sütun.
- **Faktöriyel Izgara Yapısı:** Veri seti rastgele değil, tam faktöriyel bir deney tasarımıyla üretilmiştir:
  - 9 farklı seyir hızı ($v \in \{3, 6, 9, 12, 15, 18, 21, 24, 27\}$ knot),
  - 51 farklı kompresör bozunma durumu ($kMc \in [0,950, 1,000]$),
  - 26 farklı gaz türbini bozunma durumu ($kMt \in [0,975, 1,000]$).
  - $9 \times 51 \times 26 = 11.934$ gözlem.
- **Veri Bütünlüğü:** Ham dosya SHA-256 özeti `de0ea69da1efaab8b9655ffed828547d10dd68c1fb8c6e0163e6a988def393a6` olarak mühürlenmiştir.

---

## 8. Veri Sözlüğü ve Değişkenler

Veri setindeki 18 değişken üç işlevsel kategoriye ayrılmıştır:

| No | Sembol | Değişken Adı | Birim | Rolü |
| :--- | :--- | :--- | :--- | :--- |
| 1 | `lp` | Kol Pozisyonu (Lever Position) | [katsayı] | Operasyonel Kontrol Girdisi (Hız ile korelasyon $r=1,0$) |
| 2 | `v` | Gemi Seyir Hızı (Ship Speed) | [knot] | Operasyonel Rejim Değişkeni ($3 \dots 27$) |
| 3 | `GTT` | Gaz Türbini Şaft Torku | [kN·m] | Telemetri Sensörü |
| 4 | `GTn` | Gaz Türbini Devir Sayısı | [rpm] | Telemetri Sensörü |
| 5 | `GGn` | Gaz Jeneratörü Devir Sayısı | [rpm] | Telemetri Sensörü |
| 6 | `Ts` | Sancak Pervane Torku | [kN·m] | Telemetri Sensörü |
| 7 | `Tp` | İskele Pervane Torku | [kN·m] | Sabit Çift ($T_p \equiv T_s$, elendi) |
| 8 | `T48` | Yüksek Basınç Türbin Çıkış Sıcaklığı | [°C] | Telemetri Sensörü |
| 9 | `T1` | Kompresör Giriş Sıcaklığı | [K] | Sabit Değişken ($288,0$ K, $\sigma=0$, elendi) |
| 10 | `T2` | Kompresör Çıkış Sıcaklığı | [°C] | Telemetri Sensörü |
| 11 | `P48` | Yüksek Basınç Türbin Çıkış Basıncı | [bar] | Telemetri Sensörü |
| 12 | `P1` | Kompresör Giriş Basıncı | [bar] | Sabit Değişken ($0,998$ bar, $\sigma=0$, elendi) |
| 13 | `P2` | Kompresör Çıkış Basıncı | [bar] | Telemetri Sensörü |
| 14 | `Pexh` | Egzoz Gazı Basıncı | [bar] | Telemetri Sensörü |
| 15 | `TIC` | Türbin Giriş Sıcaklığı Kontrol Sinyali | [%] | Telemetri Sensörü |
| 16 | `mf` | Yakıt Kütlesel Debisi | [kg/s] | Telemetri Sensörü |
| 17 | `kMc` | Kompresör Bozunma Katsayısı | [katsayı] | **Karantinaya Alınan Hedef (Hedef Sızıntısı Yok)** |
| 18 | `kMt` | Türbin Bozunma Katsayısı | [katsayı] | **Karantinaya Alınan Hedef (Hedef Sızıntısı Yok)** |

---

## 9. Veri Kalitesi Analizi

Faz 1 kapsamında yürütülen veri kalitesi denetiminde:
- Eksik değer (missing/NaN) sayısı: **0**.
- Mükerrer satır (duplicate row) sayısı: **0**.
- Tüm satırlarda numerik tipler ve aralıklar doğrulanmıştır.
- $kMc$ ve $kMt$ değişkenleri `DatasetContainer.targets` nesnesine aktarılarak kümeleme boru hattından fiziksel olarak yalıtılmıştır.

---

## 10. Ön İşleme ve Özellik Eleme

Faz 2 analizlerinde üç kritik eleme kararı alınmıştır:
1. **Sıfır Varyans Elemesi:** $T_1 = 288,0$ K ve $P_1 = 0,998$ bar simülatörde sabit tutulduğundan varyansları sıfırdır. Mesafe hesaplamalarını bozmamaları için çıkarılmıştır.
2. **Mükerrer Sütun Elemesi:** Sancak torku ($T_s$) ve iskele torku ($T_p$) arasındaki fark tüm satırlarda $0,0000$ kN·m'dir. Çift saymayı engellemek adına $T_p$ elenmiş, $T_s$ korunmuştur.
3. **Kümeleme Uzayı:** Geriye kalan 11 telemetri kanalı kümelemeye uygun özellik kümesi olarak tescillenmiştir.

---

## 11. Çalışma Rejimi Probleminin İspatı

Tek yönlü varyans analizi (ANOVA), gemi hızının ($v$) telemetri değişkenlerindeki toplam varyansın **%99,33'ünü** açıkladığını ortaya koymuştur. Temel Bileşenler Analizinde (PCA) ise **PC1 tek başına toplam varyansın %97,41'ini** oluşturmakta ve gaz türbininin 1 boyutlu kararlı durum yük eğrisini temsil etmektedir.

Kümeleme deneyleri bu durumu açıkça kanıtlamıştır:
- **Temsil R1 (Tüm Sensörler, Standart Ölçekli):** $k=9$ K-Means kümelemesi, gemi seyir hızını **$\text{ARI} = 0,8769$** ve $\text{NMI} = 0,9315$ doğrulukla doğrudan kümelemiştir.
- **Temsil R2 (Hız ve Kol Pozisyonu Çıkarılmış):** Hız girdisi çıkarılmasına rağmen, kuple termodinamik bağıntılar nedeniyle model seyir hızını yine **$\text{ARI} = 0,8440$** ile dolaylı olarak yeniden inşa etmiştir.

*Sonuç:* Operasyonel hız değişkenlerini veri setinden atmak hız etkisini gidermemektedir.

---

## 12. Hız İçi Koşullu Normalizasyon (Within-Speed Normalization - R5)

Bu problemin çözümü için Faz 2'de **R5 Temsili** geliştirilmiştir. Her ayrık seyir hızı $v \in \{3, \dots, 27\}$ knot için telemetri sensörlerinin rejim içi ortalaması ($\mu_j(v)$) ve standart sapması ($\sigma_j(v)$) hesaplanmış ve z-skor dönüşümü hız içinde yapılmıştır:

$$z_{ij} = \frac{x_{ij} - \mu_j(v_i)}{\sigma_j(v_i)}$$

Bu dönüşüm sonucunda:
- Hız etkisi tamamen sıfırlanmış, K-Means ($k=2$) için hız iyileşme indeksi **$\text{ARI} = 0,0002$** seviyesine inmiştir.
- Geriye kalan sinyal, operasyonel yükten bağımsız termodinamik bileşen bozulmalarını temsil eden saf varyasyon olmuştur.
- Dönüşümde $kMc$ ve $kMt$ hiçbir şekilde kullanılmamış, sıfır sızıntı korunmuştur.

---

## 13. Kümeleme Yöntemleri ve Karşılaştırması

Faz 3 kapsamında R5 temsili üzerinde dört farklı kümeleme algoritması ailesi test edilmiştir:
1. **K-Means:** Farklı $k$ ($2 \dots 12$) değerlerinde taranmıştır. En yüksek silüet ($0,2813$) $k=2$ seviyesinde elde edilmiştir.
2. **Hiyerarşik Kümeleme (Ward & Average):** Ward bağlantısı, K-Means $k=2$ çözümü ile **$\text{ARI} = 0,9620$** uyum sağlayarak bağımsız bir algoritma ailesi olarak K-Means küme yapısını doğrulamıştır. Average bağlantısı ise zincirleme etkisi nedeniyle başarısız olmuştur (11.932'ye 2 örnek ayrımı).
3. **DBSCAN:** Faktöriyel sürekli ızgara yapısında boş yoğunluk vadileri bulunmadığından; düşük $\epsilon \le 1,0$ değerlerinde aşırı parçalanma, yüksek $\epsilon \ge 1,5$ değerlerinde ise tüm veriyi tek kümeye toplama eğilimi göstermiş, bu veri yapısına uygun bulunmamıştır.
4. **Gauss Karışım Modelleri (GMM):** 11 boyutlu uzayda kovaryans matrislerinin aşırı parametrizasyonu nedeniyle kararsızlık yaşamıştır ($DB = 14.785$).

---

## 14. Deney Tasarımı ve Değerlendirme Kriterleri

Aday modeller Faz 4 kapsamında 10 kriter üzerinden sınanmıştır:
1. Geometrik Küme Ayrışımı (Silhouette, Davies-Bouldin, Calinski-Harabasz)
2. Hız Bağımsızlığı (ARI vs Speed, Cramér's V)
3. Çözüm Kararlılığı (10 tohumlu ARI, 100 tekrarlı Bootstrap ARI)
4. Kompresör Bozunma İlişkisi ($kMc$ ANOVA $\eta^2$, Mann-Whitney $U$, Cliff's delta)
5. Türbin Bozunma İlişkisi ($kMt$ ANOVA $\eta^2$, Mann-Whitney $U$, Cliff's delta)
6. İkili Ayrışım ve FDR Düzeltmesi (Benjamini-Hochberg düzeltmeli $p$ değerleri)
7. Bozulma Izgarası Tutarlılığı ($kMc \times kMt$ ızgarasında uzamsal süreklilik)
8. Hızlar Arası Dağılım Değişmezliği (9 hızdaki küme yüzdelerinin standart sapması)
9. Yorumlanabilirlik (Fiziksel termodinamik tutarlılık)
10. Sadelik ve Aşırı Öğrenme Riski (Occam'ın Usturası)

---

## 15. Deneysel Sonuçlar

R5 uzayında yürütülen deney sonuçları aşağıda özetlenmiştir:

| Model | $k$ | Silüet | Davies-Bouldin | Hız ARI | Bootstrap ARI | $kMc$ $\eta^2$ | $kMt$ $\eta^2$ |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **Aday A (K=2)** | 2 | **0,2813** | 1,3917 | **0,0002** | **0,9844** | 0,4459 | 0,0131 |
| **Aday B (K=3)** | 3 | 0,2593 | **1,2918** | 0,0064 | 0,9434 | **0,5109** | **0,3007** |

---

## 16. İstatistiksel Doğrulama ve Etki Büyüklüğü Analizi

$N=11.934$ gibi yüksek örneklem hacimlerinde standart hipotez testleri çok küçük önemsiz farklarda bile $p < 0,05$ üretmektedir. Bu nedenle Benjamini-Hochberg FDR düzeltmesi uygulanmış ve etki büyüklüğü parametrik olmayan **Cliff's delta ($d$)** ile ölçülmüştür ($|d| < 0,147$ ihmal edilebilir, $\ge 0,474$ büyük etki).

### İkili Karşılaştırma Sonuçları Tablosu:

| Model | Hedef | Kümeler | Ham $p$ | Düzeltilmiş $p$ (FDR) | Cliff's Delta ($d$) | Sözel Yorum | Medyan Farkı (%95 GA) |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **K=2** | $kMc$ | 0 vs 1 | $0,0$ | $0,0$ | **+0,7709** | **Büyük Etki** | $+0,022$ $[+0,022, +0,023]$ |
| **K=2** | $kMt$ | 0 vs 1 | $6,69 \times 10^{-36}$ | $6,69 \times 10^{-36}$ | **+0,1321** | **İhmal Edilebilir** | $+0,003$ $[+0,002, +0,003]$ |
| **K=3** | $kMc$ | 0 vs 1 | $2,18 \times 10^{-4}$ | $2,18 \times 10^{-4}$ | **+0,0495** | **İhmal Edilebilir** | $+0,001$ $[0,000, +0,002]$ |
| **K=3** | $kMc$ | 0 vs 2 | $0,0$ | $0,0$ | **+0,8689** | **Büyük Etki** | $+0,025$ $[+0,024, +0,025]$ |
| **K=3** | $kMc$ | 1 vs 2 | $0,0$ | $0,0$ | **+0,8406** | **Büyük Etki** | $+0,024$ $[+0,022, +0,024]$ |
| **K=3** | $kMt$ | 0 vs 1 | $0,0$ | $0,0$ | **-0,7673** | **Büyük Etki** | $-0,012$ $[-0,013, -0,012]$ |
| **K=3** | $kMt$ | 0 vs 2 | $0,0$ | $0,0$ | **-0,5020** | **Büyük Etki** | $-0,007$ $[-0,008, -0,007]$ |
| **K=3** | $kMt$ | 1 vs 2 | $4,86 \times 10^{-179}$| $4,86 \times 10^{-179}$| **+0,3561** | **Orta Etki** | $+0,005$ $[+0,005, +0,005]$ |

*Kritik Bilimsel Çıkarım:*  
Aday A'da türbin bozunumu için $p = 6,69 \times 10^{-36}$ çıkmasına rağmen Cliff's delta $0,1321$ (ihmal edilebilir) bulunmuştur. Bu bulgu, $K=2$ modelinin türbin aşınmasını tespit edemediğini kesinleştirmiştir. Aday B'de ise Küme 0 ile 1 arasında kompresör farkı ihmal edilebilirken ($d = 0,0495$), türbin aşınması **büyük etki ($d = -0,7673$)** ile ayrışmıştır.

---

## 17. Birincil Bilimsel Model (K=2)

- **Seçim Gerekçesi:** En yüksek silüet değeri ($0,2813$), seyir hızından neredeyse tam yalıtım ($\text{ARI} = 0,0002$), 100 bootstrap tekrarında %98,44 ortalama kararlılık ve kompresör aşınmasında belirgin ayrım ($d = 0,7709$).
- **Küme 0 ($n = 5.939$, %49,77):** Nominal kompresör sağlığı ($kMc$ medyan: $0,9860$).
- **Küme 1 ($n = 5.995$, %50,23):** Bozulmuş kompresör profili ($kMc$ medyan: $0,9640$).
- **Hız Değişmezliği:** 9 seyir hızının tamamında küme oranları %46,9 ile %53,1 arasında sabit kalmaktadır (standart sapma: %2,22).

---

## 18. İkincil Çok Bileşenli Teşhis Modeli (K=3)

- **Seçim Gerekçesi:** İki bileşenli eşzamanlı aşınma ayrışımını incelemek isteyen durumlar için korunmuştur.
- **Küme 1 ($n = 4.125$, %34,57):** Nominal Referans Durumu ($kMc \approx 0,983, kMt \approx 0,992$).
- **Küme 0 ($n = 3.379$, %28,31):** Türbin Bozulması ile İlişkili Profil ($kMc \approx 0,984, kMt \approx 0,982$).
- **Küme 2 ($n = 4.430$, %37,12):** Kompresör Bozulması ile İlişkili Profil ($kMc \approx 0,961, kMt \approx 0,988$).
- **Kararlılık:** Bootstrap ortalama $\text{ARI} = 0,9434$ ile oldukça kararlıdır.

---

## 19. Mühendislik ve Termodinamik Yorumu

Bulunan küme profilleri gaz türbini Brayton çevrimi fiziği ile tam uyumludur:
1. **Kompresör Bozulması Belirtileri (Küme 1 / Küme 2):** Kompresör kanatçık kirlenmesi veya aşınması akışkan dinamik verimini düşürür. Kompresör aynı basıncı üretmek için daha fazla iş talep eder; kompresör çıkış sıcaklığı ($T_2$) yükselir. İstenen şaft torkunu korumak için yakıt debisi ($m_f$) artar ve bu durum türbin giriş/çıkış sıcaklıklarını ($T_{48}$) belirgin şekilde yukarı çeker. Tüm %95 güven aralıkları pozitif sapmayı doğrulamaktadır.
2. **Türbin Bozulması Belirtileri (K=3, Küme 0):** Türbin kanatçık erozyonu genleşme verimini düşürür. Yüksek basınç türbin çıkış basıncı ($P_{48}$) ve kompresör basıncı ($P_2$) artar, şaft devirleri ($GT_n, GG_n$) geriler.

---

## 20. Streamlit Uygulaması ve Yerel Gösterim

Faz 5 kapsamında geliştirilen web tabanlı yerel arayüz (`app/main.py`), internet bağlantısına ve harici bulut servislerine ihtiyaç duymadan tamamen yerel Windows ortamında çalışmaktadır.

Uygulama 8 ana modülden oluşur:
1. **Genel Bakış (Overview):** Temel göstergeler ve metodoloji akışı.
2. **Çalışma Rejimi Analizi (Operating Regime):** Hız baskınlığının ampirik kanıtı.
3. **Birincil Profil (K=2):** Kompresör ayrışımı ve güven aralıkları.
4. **Çok Bileşenli Profil (K=3):** Türbin ve kompresör ortak ayrışımı.
5. **Bozulma Haritası (Degradation Map):** 2B $kMc \times kMt$ ızgara sürekliliği.
6. **Yeni Gözlem Analizi (Observation Analysis):** Yeni bir telemetri vektörünü en yakın kümeye atayan etkileşimli teşhis aracı.
7. **Model Karşılaştırması (Model Comparison):** 11 kriterli resmi karşılaştırma tablosu.
8. **Metodoloji ve Sınırlılıklar:** Bilimsel sınırlar ve etik kurallar.

---

## 21. Sınırlılıklar

Araştırmanın akademik dürüstlük çerçevesinde kabul edilen temel sınırları şunlardır:
1. **Simülasyon Temelli Veri:** Veriler CODAG simülatöründen elde edilmiştir; gerçek deniz ortamındaki sensör gürültüsü, dalgalanma ve veri kaybı simülasyonda yer almamaktadır.
2. **Kararlı Durum Kısıtı:** Tüm gözlemler sabit hız ve aşınmadaki statik dengedir. Manevra, ivmelenme ve dinamik geçişler kapsanmamıştır.
3. **Faktöriyel Izgara:** Aşınma gerçekte kademeli zaman serisi olarak ilerler; veri setindeki ayrık ızgara zaman boyutu içermemektedir.
4. **Korelasyon $\neq$ Nedensellik:** Kümeleme bir nedensellik kanıtlamaz; çok boyutlu artık uzayındaki geometrik birliktelikleri gösterir.
5. **Askeri/Operasyonel Dağıtım İddiası Yoktur:** Gerçek bir harp gemisinde canlı kontrole hazır değildir.
6. **Gelecek Arıza Tahmini Değildir:** Kalan faydalı ömür (RUL) veya arıza tahmini yapılmamaktadır.

---

## 22. Gelecek Çalışmalar

- Gerçek gemi seyir kayıtlarından elde edilen dinamik zaman serisi telemetrisi üzerinde rejim normalizasyonunun test edilmesi.
- Akışkanlar mekaniği geçişkenliklerini modellemek amacıyla yarı denetimli (semi-supervised) veya fizik kurallı (physics-informed) kümeleme mimarilerinin incelenmesi.
- Dengesiz aşınma ızgaralarında yoğunluk tabanlı kümeleme için uyarlamalı manifold öğrenme tekniklerinin araştırılması.

---

## 23. Sonuç

Bu bitirme çalışması, deniz gaz türbini tahrik sistemlerinde denetimsiz makine öğrenmesi uygulamalarının önündeki en büyük engelin operasyonel hız baskınlığı (%99,33 varyans) olduğunu deneysel olarak kanıtlamıştır. Geliştirilen "hız içi koşullu normalizasyon" tekniği sayesinde, model eğitimine hiçbir aşınma etiketi verilmeksizin, kompresör ($d = 0,7709$) ve türbin ($d = -0,7673$) aşınma profillerinin denetimsiz olarak keşfedilebildiği %98,4'lük bootstrap kararlılığı ve 51/51 başarılı birim test ile doğrulanmıştır.

---

## 24. Kaynakça

1. Coraddu, A., Oneto, L., Ghio, A., Savio, S., Anguita, D., & Figari, M. (2016). *Machine learning for ship propulsion plants: dynamic condition based maintenance from sensor data.* IEEE Transactions on Reliability, 65(4), 1644-1656.
2. UCI Machine Learning Repository. (2014). *Condition Based Maintenance of Naval Propulsion Plants.* Dataset ID: 316.
3. MacQueen, J. (1967). *Some methods for classification and analysis of multivariate observations.* Proc. 5th Berkeley Symp. Math. Statist. Prob., 1, 281-297.
4. Rousseeuw, P. J. (1987). *Silhouettes: a graphical aid to the interpretation and validation of cluster analysis.* Journal of Computational and Applied Mathematics, 20, 53-65.
5. Hubert, L., & Arabie, P. (1985). *Comparing partitions.* Journal of Classification, 2(1), 193-218.
6. Benjamini, Y., & Hochberg, Y. (1995). *Controlling the false discovery rate: a practical and powerful approach to multiple testing.* Journal of the Royal Statistical Society: Series B, 57(1), 289-300.
7. Romano, J., Kromrey, J. D., Coraggio, J., & Skowronek, J. (2006). *Appropriate statistics for ordinal level data: Should we really be using t-test and Cohen's d for evaluating group differences on the NSSE and other surveys?* Florida Association for Institutional Research.
