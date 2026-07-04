# [Title TBD] — Manuscript Draft

**Project:** bio-b — Sm/Lsm Phylogenetics
**Author:** Sui Nakai
**Target journal:** Genome Biology and Evolution / Molecular Biology and Evolution
**Status:** Pre-draft (updated 2026-07-04 to reflect scenario pivot: absence → retention)

---

## Title candidates

- Sm/Lsm proteins are retained across the reduced-genome DPANN and Asgard archaea: a structure-informed phylogenomic reassessment
- (alt) Widespread retention of the ancestral Sm fold in DPANN and Asgard archaea

---

## Abstract

<!-- 後で。骨子：Sm/Lsm 超科の3ドメイン系統を現代手法＋構造ガイドで更新。従来「縮小ゲノム
（DPANN/CPR）は Sm/Lsm を欠く」とされたが、completeness フィルタ＋高感度 HMM＋ab initio 遺伝子
予測で再検証すると DPANN/Asgard は Sm/Lsm を保持（N. equitans・Lokiarchaeia 含む）。ESMFold+
foldseek で 55/55 が Sm fold と構造検証。これらは祖先型 Lsm に近く、真核 Sm 起源に一次データを与える。 -->

---

## 1. Introduction

### Background

The Sm/Lsm protein family is one of the most ancient and conserved families in the history of life. In eukaryotes, seven Sm proteins (SmB, SmD1, SmD2, SmD3, SmE, SmF, SmG) and eight Lsm proteins (Lsm1–Lsm8) form heptameric rings that associate with snRNAs to constitute the spliceosome and mRNA-decay machinery. Archaeal homologs (Sm-like archaeal proteins, SmAP) form similar homomeric rings involved in RNA binding, and the bacterial counterpart Hfq shares the same Sm fold — an N-terminal α-helix over a strongly bent five-stranded antiparallel β-sheet (Sm1 motif, β1–β3; Sm2 motif, β4–β5) — despite low sequence identity. The evolutionary relationships among these proteins across the three domains of life bear on the early evolution of the spliceosome (Veretnik et al. 2009) and on eukaryogenesis, since the eukaryotic Sm/Lsm machinery is thought to derive from an archaeal ancestor.

### Gap

The most comprehensive phylogenetic study of the Sm/Lsm family to date (Veretnik et al. 2009, PLoS Comput Biol) analyzed 335 sequences from 80 species using ClustalW alignment and PhyML with the JTT model. In the intervening ~17 years, the number of available sequences has grown by more than an order of magnitude, phylogenetic methods have advanced (ModelFinder, ultrafast bootstrap, Bayesian inference with convergence diagnostics), and — critically — the reduced-genome archaeal superphyla **DPANN** and the eukaryote-related **Asgard** archaea, essentially unsampled in 2009, are now represented by hundreds of (largely metagenome-assembled) genomes. Whether these deeply-branching, reduced-genome lineages encode Sm/Lsm proteins has been treated as an open question, and low-sensitivity BLAST searches have suggested their absence. However, BLAST cannot distinguish true gene loss from failure to detect divergent sequences, and metagenome-assembled genomes (MAGs) confound absence with incomplete assembly and annotation.

### Aims

1. To reconstruct the phylogeny of the Sm/Lsm family across the three domains of life using current best-practice methods (structure-guided alignment, IQ-TREE3 + MrBayes), updating Veretnik et al. (2009).
2. To rigorously test whether the reduced-genome DPANN and Asgard archaea encode Sm/Lsm proteins, controlling for genome completeness and annotation gaps, and to verify any detected homologs at the structural level.

> **Note on scenario (2026-07-04):** an early framing of this project was to *demonstrate the absence* of Sm/Lsm in reduced-genome organisms (following an initial BLAST result of zero hits). Re-analysis with a completeness-filtered, dual-HMM, ab initio gene-prediction pipeline overturned this: DPANN and Asgard archaea in fact **retain** Sm/Lsm. The manuscript is framed around this retention finding.

---

## 2. Materials and Methods

### 2.1 Reference sequence set (Sm/Lsm/Hfq)

Sm, Lsm, SmAP and Hfq protein sequences were retrieved from NCBI RefSeq via the E-utilities API (eukaryotic Sm subtypes SmB/D1/D2/D3/E/F/G and Lsm1–Lsm8, up to 500 each; bacterial Hfq; archaeal SmAP). An initial gene-name–based retrieval (6,103 sequences) was found to contain substantial contamination from symbol-similar but unrelated proteins (e.g., "Smaug"/SAM-domain proteins matched by `SmG[Gene Name]`, and eukaryotic "Small Acidic Protein" matched by `SmAP[Gene Name]`, which returned no genuine archaeal Sm). Contaminants were removed with a curated description blacklist, and the archaeal Sm set was replaced with the manually curated 33 archaeal Sm sequences of Veretnik et al. (2009), yielding a clean reference set of **5,665 sequences** (`smlsm_all_curated.fasta`).

### 2.2 Redundancy reduction and length filtering

Curated sequences were length-filtered to 50–150 aa (retaining the ~76-aa Sm core domain while excluding full-length fusion proteins in which the Sm fold is a subdomain) and clustered at 90% identity with CD-HIT (5,665 → 5,133 → 1,107 representatives).

### 2.3 Structure-guided multiple sequence alignment

Because Sm/Lsm/Hfq proteins are short and highly divergent across domains, plain sequence alignment is unreliable at deep nodes (a straightforward MAFFT alignment expanded to ~92% gaps). A structural reference was therefore built from 19 experimentally determined Sm-fold structures spanning all three domains (eukaryotic Sm/U1 snRNP, archaeal SmAP, bacterial Hfq; PDB accessions listed in Table S1). These were structurally aligned with FoldMason (Gilchrist et al. 2024) and dereplicated (CD-HIT 95%) into a 25-sequence structural seed, which was used to guide alignment of the full sequence set with MAFFT (`--seed`). After occupancy trimming, the analysis alignment comprised 1,101 sequences × 184 columns, with a structurally-defined core of ~76 columns corresponding to the Sm fold.

### 2.4 Phylogenetic analysis

Maximum-likelihood inference used IQ-TREE3 v3.1.3 with ModelFinder (BIC) and ultrafast bootstrap (1,000 replicates); Bayesian inference used MrBayes v3.2. Rooting follows the reciprocal-outgroup design shared with the companion Hfq study (bacterial Hfq and archaeal SmAP as mutual outgroups).

### 2.5 Distribution survey in DPANN, Asgard (and CPR)

Genomes of DPANN (nine lineages) and Asgard (five classes) archaea were retrieved via the NCBI Datasets v2 API. To avoid confounding true absence with incomplete assembly, genomes were filtered by CheckM completeness ≥ 50% and contamination ≤ 10% (MIMAG medium-quality), and GCA/GCF duplicates were removed. For genomes lacking an annotated proteome, genes were predicted ab initio with Prodigal (meta mode), removing annotation-gap artifacts. The resulting proteomes were scanned with two profile HMMs — the Sm/Lsm domain (Pfam **PF01423**) and the Hfq domain (Pfam **PF17209**) — under the trusted (`--cut_ga`) cutoff; each hit was typed as Sm/Lsm or Hfq by its higher-scoring model. The same pipeline was applied to CPR/Patescibacteria bacteria. Hit counts were aggregated at genome and species level, and lineages with no completeness-passing genome were reported as data-insufficient rather than as absences.

### 2.6 Structural verification of homologs

To confirm that HMM hits represent genuine Sm folds, each hit sequence was structurally modeled with ESMFold (ESM Atlas API) and the predicted structures were compared against the experimental Sm-fold anchors with Foldseek; a TM-score ≥ 0.5 to a Sm-fold anchor was taken as structural confirmation.

---

## 3. Results

### 3.1 A curated, contamination-controlled Sm/Lsm dataset

<!-- コンタミ診断（15%）と除去、curated 5,665、型配色木で Hfq/Sm/Lsm/SmAP が分離しコンタミ大ブロックが消えたことを提示（Fig. curated types）。 -->

### 3.2 Structure-guided phylogeny of the Sm/Lsm family

<!-- 構造ガイド MSA による3ドメイン系統。生配列版との比較（深部支持の改善）。IQ-TREE 完了後に数値。 -->

### 3.3 DPANN and Asgard archaea retain Sm/Lsm proteins

Applying the completeness-filtered dual-HMM pipeline to 50 quality genomes across DPANN and Asgard, we detected Sm/Lsm proteins in all six lineages with sufficient genome quality (Nanoarchaeota, Asgardarchaeota, Lokiarchaeia, Parvarchaeota, Micrarchaeota, Nanohaloarchaeota); all 70 hits were typed as Sm/Lsm and none as Hfq. Notably, the DPANN type species *Nanoarchaeum equitans* — for which an early BLAST search returned no hit — encodes a Sm/Lsm protein, and all sampled Lokiarchaeia (Asgard) genomes, including the cultured *Promethearchaeum syntrophicum*, retain the fold. Eight lineages (e.g., Woesearchaeota, Thorarchaeia) had no completeness-passing genome and are reported as data-insufficient. Thus the earlier apparent absence reflected BLAST sensitivity limits, not gene loss.

### 3.4 Structural verification

All 55 hit sequences that yielded confident ESMFold models (mean pLDDT ≥ 0.7) matched an experimental Sm-fold anchor by Foldseek with high structural similarity (TM-score 0.92–1.00; median 0.97), and 49/55 were closest to an archaeal Sm anchor. The Sm/Lsm presence in DPANN/Asgard is therefore supported by both sequence (HMM) and structure (ESMFold + Foldseek).

### 3.5 CPR bacteria

<!-- CPR census 完了後に追記。焦点：Saccharibacteria が Hfq を持つか。他 CPR は data-insufficient。 -->

---

## 4. Discussion

- The headline result overturns the intuitive expectation that genome reduction eliminates the Sm/Lsm machinery: DPANN and Asgard archaea retain the fold, detectable only once completeness filtering, high-sensitivity HMMs and ab initio gene prediction remove the artifacts that make BLAST report absence.
- The retained proteins are archaeal Sm/SmAP-type (structurally closest to archaeal anchors), consistent with the view that the eukaryotic Sm/Lsm system derives from an archaeal ancestor; the presence in Asgard (Lokiarchaeia) provides primary data relevant to eukaryogenesis.
- <!-- 構造ガイド系統の位置づけ（Veretnik Fig1 との比較、SmAP の系統的位置）。 -->
- <!-- SmAP1/SmAP2 パラログ史（Nikulin 2020：Sm1 第3位 His vs Thr が SmAP1/2 を分ける残基指標）。 -->
- Limitations: DPANN/Asgard genome quality caps the survey at a minority of lineages; CPR remains only partially assessed (Saccharibacteria); the structure-guided alignment still leaves the deepest backbone data-limited.

---

## 5. Conclusion

---

## References

<!-- Zotero から出力 -->

---

## Figures

| Figure | Caption | Status |
|--------|---------|--------|
| Fig. 1 | Structure-guided Sm/Lsm phylogeny across three domains, tips colored by type (Hfq / SmAP / Lsm / Sm-core). | Curated-tree version rendered (`4-results/smlsm_curated_types.pdf`); structure-guided tree pending |
| Fig. 2 | Distribution of Sm/Lsm and Hfq across DPANN/Asgard (and CPR) lineages by HMM, with completeness-based assessability. | Data ready (`3-analysis/hmm/census_lineage.tsv`); figure TBD |
| Fig. 3 | Structural verification of DPANN/Asgard hits: ESMFold models vs Sm-fold anchors (Foldseek TM-score). | Data ready (`4-results/smfold_foldseek_verification.tsv`); figure TBD |

## Tables

| Table | Caption | Status |
|-------|---------|--------|
| Table 1 | Sm/Lsm and Hfq counts per DPANN/Asgard/CPR lineage (genome- and species-level), with completeness. | Data ready |
| Table S1 | Sm-fold structural anchors (PDB accessions, organism, domain) used for structure-guided alignment. | Ready (`0-literature/structural_anchors.md`) |
