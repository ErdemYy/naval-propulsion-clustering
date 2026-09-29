# Final Publication Figure Catalog & Defense Presentation Guide

**Project:** Naval Propulsion Clustering  
**Scope:** Definitive registry of all publication-grade figures, their scientific interpretation, report location, and recommended live defense speaking points.

---

## Prioritized Figure Registry

### 1. Operating Speed Dominance across Telemetry Channels
- **File:** [`reports/figures/phase2/variance_by_operating_regime.png`](file:///reports/figures/phase2/variance_by_operating_regime.png)
- **Phase:** Phase 2 (Preprocessing & Operating Regime Diagnostics)
- **Purpose:** Quantify the variance explained ($\eta^2$) by commanded ship speed ($v$) across all sensor channels.
- **What it Demonstrates:** Commanded speed explains **99.33% of total sensor variance** ($\eta^2 \ge 0.965$ across all telemetry channels). Sensor variance is overwhelmed by operating point rather than component health.
- **Report Location:** Section 11 (*Çalışma Rejimi Probleminin İspatı*).
- **Defense Explanation:** *"Bu grafik, ham sensör verisindeki değişimin %99'dan fazlasının gemi hızından kaynaklandığını kanıtlamaktadır. Hız kontrol altına alınmadan yapılacak her kümeleme kaçınılmaz olarak gemi hızını kümeleyecektir."*

---

### 2. Operating Speed Recovery across Feature Representations
- **File:** [`reports/figures/phase3/k_vs_speed_recovery_ari.png`](file:///reports/figures/phase3/k_vs_speed_recovery_ari.png)
- **Phase:** Phase 3 (Controlled Clustering Experiments)
- **Purpose:** Compare Adjusted Rand Index against operating speed ($\text{ARI vs Speed}$) across representations R1 through R5 for $k=2 \dots 12$.
- **What it Demonstrates:** In R1 and R2, clustering achieves $\text{ARI} \approx 0.88$ and $0.84$ with ship speed. In R5 (Within-Speed Normalized), the speed association drops to $\text{ARI} \approx 0.0002$.
- **Report Location:** Section 11 & Section 12 (*Within-Speed Normalization*).
- **Defense Explanation:** *"Görüldüğü üzere, hız değişkenlerini veri setinden çıkarmak (R2) hızı unutturmaya yetmemektedir (ARI = 0.844). Yalnızca hız içi koşullu normalizasyon (R5) hız bağımlılığını sıfırlamaktadır (ARI = 0.0002)."*

---

### 3. Silhouette Score Trajectory Across Candidate Representations
- **File:** [`reports/figures/phase3/k_vs_silhouette_all_representations.png`](file:///reports/figures/phase3/k_vs_silhouette_all_representations.png)
- **Phase:** Phase 3 (Controlled Clustering Experiments)
- **Purpose:** Contrast intrinsic geometric separation curves across candidate representations.
- **What it Demonstrates:** R1–R4 exhibit high silhouette scores peaking at $k=9$ ($s \approx 0.78$) because they separate distinct speed clusters. R5 exhibits lower silhouette ($s = 0.2813$ at $k=2$) because the massive speed separation is removed, revealing the subtle continuous degradation manifold.
- **Report Location:** Section 13 (*Kümeleme Yöntemleri*).
- **Defense Explanation:** *"R1-R4'te $k=9$'da görülen yüksek silüet (0.78), modelin 9 hızı mükemmel ayırdığının göstergesidir. R5'te silüetin 0.28'e inmesi bir zayıflık değil; hız artefaktının temizlenip sürekli aşınma uzayına ulaşıldığının kanıtıdır."*

---

### 4. Post-Hoc Compressor Decay ($kMc$) Distribution by Cluster
- **File:** [`reports/figures/phase3/kmc_distribution_by_cluster.png`](file:///reports/figures/phase3/kmc_distribution_by_cluster.png)
- **Phase:** Phase 3 & Phase 4 (Post-Hoc Validation)
- **Purpose:** Boxplot and violin distribution of quarantined compressor decay coefficient $kMc$ across clusters.
- **What it Demonstrates:** Cluster 0 is concentrated around nominal compressor health ($M = 0.9860$), while Cluster 1 captures degraded compressor states ($M = 0.9640$).
- **Report Location:** Section 16 & Section 17 (*Birincil Model*).
- **Defense Explanation:** *"Model eğitiminde $kMc$ etiketini hiç görmediği halde, kümeleme sonrası dağılım incelendiğinde Küme 0'ın yüksek sağlık, Küme 1'in ise belirgin kompresör aşınması ile örtüştüğü görülmektedir."*

---

### 5. Post-Hoc Turbine Decay ($kMt$) Distribution by Cluster
- **File:** [`reports/figures/phase3/kmt_distribution_by_cluster.png`](file:///reports/figures/phase3/kmt_distribution_by_cluster.png)
- **Phase:** Phase 3 & Phase 4 (Post-Hoc Validation)
- **Purpose:** Distribution of quarantined turbine decay coefficient $kMt$ across clusters.
- **What it Demonstrates:** For $k=2$, $kMt$ distributions are nearly identical between clusters. For $k=3$, Cluster 0 captures degraded turbine states ($M = 0.9810$), while Cluster 1 captures nominal turbine states ($M = 0.9930$).
- **Report Location:** Section 16 & Section 18 (*İkincil Model*).
- **Defense Explanation:** *"Bu grafik $k=2$'nin türbin aşınmasına duyarsız olduğunu, ancak $k=3$'ün türbin aşınmasını başarıyla bağımsız bir kümede izole ettiğini kanıtlamaktadır."*

---

### 6. Factorial Degradation Grid Map (Candidate A: K=2)
- **File:** [`reports/figures/phase4/degradation_grid_k2.png`](file:///reports/figures/phase4/degradation_grid_k2.png)
- **Phase:** Phase 4 (Scientific Validation)
- **Purpose:** 2D spatial mapping of majority cluster assignments across the $51 \times 26$ ($1,326$ cells) $kMc \times kMt$ plane.
- **What it Demonstrates:** Clusters form a clean, spatially contiguous boundary along $kMc \approx 0.975$ with $86.24\%$ consistency across all 9 operating speeds.
- **Report Location:** Section 15 & Section 17.
- **Defense Explanation:** *"1.326 hücrelik aşınma ızgarasında kümeler rastgele gürültü değil, uzamsal olarak bitişik ve fiziksel sınırları olan pürüzsüz bölgeler oluşturmaktadır."*

---

### 7. Factorial Degradation Grid Map (Candidate B: K=3)
- **File:** [`reports/figures/phase4/degradation_grid_k3.png`](file:///reports/figures/phase4/degradation_grid_k3.png)
- **Phase:** Phase 4 (Scientific Validation)
- **Purpose:** 2D spatial mapping for the tripartite model across $kMc \times kMt$.
- **What it Demonstrates:** Three contiguous geometric zones: low $kMc$ (Cluster 2), high $kMc$ + low $kMt$ (Cluster 0), and high $kMc$ + high $kMt$ (Cluster 1) with $82.17\%$ speed consistency.
- **Report Location:** Section 15 & Section 18.
- **Defense Explanation:** *"Bu harita $K=3$ modelinin iki boyutlu aşınma uzayını üç fiziksel alt bölgeye başarıyla ayırdığını görsel olarak teyit etmektedir."*

---

### 8. Standardized Telemetry Deviation Profiles with 95% Bootstrap CIs
- **File:** [`reports/figures/phase4/telemetry_profiles_comparison.png`](file:///reports/figures/phase4/telemetry_profiles_comparison.png)
- **Phase:** Phase 4 (Scientific Validation)
- **Purpose:** Bar chart showing normalized z-score deviations of all 11 sensor channels with 95% bootstrap confidence intervals for cluster means ($B=500$).
- **What it Demonstrates:** In Cluster 1 (degraded compressor), temperatures ($T_2, T_{48}$) and fuel flow ($m_f$) are significantly elevated above baseline, consistent with Brayton cycle thermodynamics. All 95% CIs exclude zero.
- **Report Location:** Section 19 (*Mühendislik ve Termodinamik Yorumu*).
- **Defense Explanation:** *"Kompresör bozulduğunda verim düşer ve şaft gücünü korumak için yakıt debisi ($m_f$) ile egzoz sıcaklıkları ($T_2, T_{48}$) artar. Modelimizin bulduğu profil fiziksel gaz türbini dinamikleriyle birebir örtüşmektedir."*

---

### 9. Speed Invariance of Cluster Proportions
- **File:** [`reports/figures/phase4/cluster_distribution_by_speed_k2.png`](file:///reports/figures/phase4/cluster_distribution_by_speed_k2.png)
- **Phase:** Phase 4 (Scientific Validation)
- **Purpose:** Grouped bar chart showing cluster 0 and cluster 1 proportions across the 9 discrete ship speeds.
- **What it Demonstrates:** Proportions remain strictly balanced between $46.9\%$ and $53.1\%$ across all speeds (mean $49.77\% \pm 2.22\%$, Cramér's $V = 0.0418$).
- **Report Location:** Section 17 (*Birincil Model*).
- **Defense Explanation:** *"Küme oranlarının 3 knot'tan 27 knot'a kadar her hızda yaklaşık %50-%50 sabit kalması, bulunan profilin hız kaynaklı bir yan etki olmadığını kesinleştirmektedir."*

---

### 10. Bootstrap Resampling Stability Distribution ($B=100$)
- **File:** [`reports/figures/phase4/bootstrap_stability_distribution.png`](file:///reports/figures/phase4/bootstrap_stability_distribution.png)
- **Phase:** Phase 4 (Scientific Validation)
- **Purpose:** Kernel Density Estimate (KDE) comparing empirical Adjusted Rand Index distributions under bootstrap resampling with replacement for Candidate A vs Candidate B.
- **What it Demonstrates:** Candidate A exhibits exceptional determinism with Mean ARI $= 0.9844$ ($95\%$ CI: $[0.970, 0.998]$). Candidate B exhibits solid stability with Mean ARI $= 0.9434$.
- **Report Location:** Section 15 (*Deneysel Sonuçlar*).
- **Defense Explanation:** *"Veri seti 100 kez yerine koyarak rastgele yeniden örneklendiğinde bile K=2 modelinin %98,4 uyum göstermesi, küme yapısının örneklem dalgalanmalarına karşı son derece dayanıklı olduğunu kanıtlar."*
