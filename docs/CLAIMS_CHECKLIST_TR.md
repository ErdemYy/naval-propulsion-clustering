# Sunumda İddia Güvenliği Kontrol Listesi (Claims Checklist)

Bu belge, bitirme projesi savunmasında ve sunumunda akademik güvenilirliği korumak, jüriden gelebilecek metodolojik itirazları önlemek ve bilimsel dürüstlük standartlarına tam uyum sağlamak için konuşmacının kullanabileceği ve kesinlikle kaçınması gereken ifadeleri kategorize eder.

---

## 🟢 1. KULLANILMASI GÜVENLİ İFADELER (SAFE TO SAY)

Bu ifadeler projenin matematiksel ve deneysel kanıtlarıyla %100 desteklenmektedir:

1. *"Simüle edilmiş veri setinde seyir hızı $v$ toplam sensör varyansının %99,33'ünü açıklamaktadır."*
2. *"Ham telemetri üzerinde çalışan naif kümeleme, donanım aşınmasını değil, geminin seyir hızını ayrıştırmaktadır (ARI = 0,8769)."*
3. *"Operasyonel hız değişkenleri çıkarılsa bile kuple termodinamik fizik nedeniyle kümeleme seyir hızını yeniden inşa etmektedir (ARI = 0,8440)."*
4. *"Geliştirdiğimiz Hız İçi Koşullu Normalizasyon (Within-Speed Normalization), kümelemenin seyir hızı ile olan korelasyonunu ARI = 0,0002 seviyesine düşürmüştür."*
5. *"Kompresör ($kMc$) ve türbin ($kMt$) bozunma katsayıları model eğitiminden tamamen yalıtılmış, sıfır hedef sızıntısı (zero data leakage) korunmuştur."*
6. *"Birincil modelimiz olan K-Means (k=2), 100 tekrarlı bootstrap testinde %98,44 ortalama Rand indeksiyle yüksek çözüm kararlılığı sergilemiştir."*
7. *"Post-hoc Mann-Whitney U ve Cliff's delta testleri, k=2 modelinin kompresör aşınmasıyla büyük bir etki büyüklüğü ile ($d = +0,7709, p < 10^{-100}$) ilişkili olduğunu doğrulamıştır."*
8. *"K=3 modeli, nominal rejim, türbin bozulması ($d = -0,7673$) ve kompresör bozulması ($d = +0,8689$) olmak üzere üç ayrı fiziksel durumu başarıyla izole etmiştir."*
9. *"Bozulma ızgarası haritasında kümeler rastgele gürültü değil, uzamsal olarak bitişik ve pürüzsüz bölgeler oluşturmaktadır."*
10. *"Tüm boru hattı 51 otomatik birim test ile mühürlenmiş olup, yerel bilgisayarda internet olmadan çalışabilmektedir."*

---

## 🟡 2. KOŞULLU / AÇIKLAMA GEREKTİREN İFADELER (REQUIRES QUALIFICATION)

Bu ifadeler söylenirken mutlaka arkasındaki metodolojik şart belirtilmelidir:

1. **"Model kompresör aşınmasını tespit etmiştir."**  
   ⚠️ *Açıklama Ekleyin:* *"Model doğrudan kompresör etiketini görmemiştir; ancak denetimsiz olarak bulduğu Küme 1 profili, kümeleme sonrasında zemin gerçekliği kompresör aşınması göstergesiyle yüksek korelasyon sergilemiştir."*
2. **"K=2 modeli türbin aşınması için p < 0.05 vermiştir."**  
   ⚠️ *Açıklama Ekleyin:* *"Örneklem hacmi 11.934 olduğu için p-değeri küçük çıkmıştır; ancak Cliff's delta etki büyüklüğü 0,132 ile ihmal edilebilir düzeydedir. Bu nedenle K=2'nin türbin aşınmasını ayrıştırdığı iddia edilemez."*
3. **"K=3 modeli daha iyi bir modeldir."**  
   ⚠️ *Açıklama Ekleyin:* *"K=3 silüet ve kararlılık açısından K=2'den daha düşüktür; ancak çok bileşenli ayrışım sunması bakımından tamamlayıcı bir teşhis modelidir."*
4. **"Telemetri sapmaları aşınmanın sonucudur."**  
   ⚠️ *Açıklama Ekleyin:* *"Bu sapmalar Brayton termodinamik çevrimiyle tutarlıdır; ancak kümeleme nedensellik değil, istatistiksel profil birlikteliği sunmaktadır."*

---

## 🔴 3. KESİNLİKLE SÖYLENMEYECEK YASAK İFADELER (DO NOT SAY)

Bu ifadeler bilimsel olarak temelsizdir, jürinin projeyi reddetmesine yol açabilir ve kesinlikle yasaktır:

1. ❌ **"Modelimiz makinenin arızalanacağını tahmin etmektedir (predicts failure)."**  
   *(Veri setinde zaman boyutu yoktur; arıza tahmini yapılamaz.)*
2. ❌ **"Sistemimiz gerçek zamanlı bir arıza teşhis (fault diagnosis) sistemidir."**  
   *(Kümeleme teşhis koymaz; benzer veri noktalarını gruplar.)*
3. ❌ **"Geliştirdiğimiz yazılım Türk Deniz Kuvvetleri veya harp gemilerinde kullanıma hazırdır."**  
   *(Çalışma bir simülasyon araştırmasıdır; gerçek gemi tecrübesi yapılmamıştır.)*
4. ❌ **"Model kalan faydalı ömrü (RUL) hesaplamaktadır."**  
   *(Veri setinde ömür veya çevrim geçmişi bulunmamaktadır.)*
5. ❌ **"Küme 1 kesinlikle arızalıdır, Küme 0 kesinlikle sağlıklıdır."**  
   *(Sağlıklı/Arızalı kesin mühendislik yargılarıdır; bunun yerine 'kompresör bozulmasıyla ilişkili profil' denmelidir.)*
6. ❌ **"K=2 modelimiz türbin aşınmasını da başarıyla yakalamıştır."**  
   *(Etki büyüklüğü analizi türbin etkisinin K=2'de ihmal edilebilir olduğunu kesinleştirmiştir.)*
7. ❌ **"Bu yöntemle tüm endüstriyel arızalar çözülmüştür."**  
   *(Yalnızca simüle edilmiş kararlı durum gaz türbini telemetrisi incelenmiştir.)*
