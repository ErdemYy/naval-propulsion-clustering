# Research & Prototyping Notebooks

This directory contains Jupyter notebooks used for initial exploratory data analysis (EDA), interactive visualization, and hypothesis testing.

## Notebook Conventions
1. **Numbered Sequence:** Name notebooks sequentially by lifecycle phase:
   - `01_exploratory_data_analysis.ipynb`
   - `02_feature_distributions_and_correlations.ipynb`
   - `03_clustering_prototypes.ipynb`
   - `04_degradation_posthoc_analysis.ipynb`
2. **Read-Only / Import Principle:** Notebooks should import logic, pipelines, and functions directly from `src/naval_propulsion` rather than defining massive redundant script blocks.
3. **No Target Leakage in Notebooks:** Exploratory analyses must observe the same strict separation: $kMc$ and $kMt$ must never be provided to unsupervised methods.
4. **Clean State Before Commit:** Restart and run all cells sequentially before committing, or clear output cells to keep version control clean.
