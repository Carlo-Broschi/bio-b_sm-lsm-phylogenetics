# [Title TBD] — Manuscript Draft

**Project:** bio-b — Sm/Lsm Phylogenetics
**Author:** Sui Nakai
**Target journal:** Genome Biology and Evolution / Molecular Biology and Evolution
**Status:** Pre-draft

---

## Title candidates

-

---

## Abstract

---

## 1. Introduction

### Background

The Sm/Lsm protein family is one of the most ancient and conserved families in the history of life. In eukaryotes, seven Sm proteins (SmB, SmD1, SmD2, SmD3, SmE, SmF, SmG) and eight Lsm proteins (Lsm1–Lsm8) form heptameric rings that associate with snRNAs to constitute the spliceosome and mRNA decay machinery. Archaeal homologs (SmAP) form similar homomeric rings involved in RNA binding, and the bacterial counterpart Hfq shares the same Sm fold despite low sequence identity. The evolutionary relationship among these proteins across the three domains of life has been proposed to reflect the early evolution of the spliceosome (Veretnik et al. 2009).

### Gap

The most comprehensive phylogenetic study of the Sm/Lsm family to date (Veretnik et al. 2009, PLoS Comput Biol) analyzed 335 sequences from 80 species using ClustalW alignment and the PhyML maximum likelihood method with the JTT substitution model. In the intervening ~17 years, the number of available sequences has increased by more than an order of magnitude, and phylogenetic methods have advanced substantially — notably ModelFinder for automatic substitution model selection, ultrafast bootstrap approximation (UFBoot), and Bayesian inference with improved convergence diagnostics. Additionally, reduced-genome organisms such as DPANN archaea and CPR bacteria (Patescibacteria), whose genomes were largely unsequenced in 2009, are now represented in public databases.

### Aims

1. To reconstruct the phylogeny of the Sm/Lsm family across all three domains of life using current best-practice methods (IQ-TREE3 + MrBayes), providing an updated view of Sm/Lsm evolution.
2. To determine whether DPANN archaea and CPR bacteria, organisms with drastically reduced genomes, encode Sm/Lsm or Hfq homologs, testing whether the loss of RNA processing factors is a general feature of genome reduction.

---

## 2. Materials and Methods

### 2.1 Sequence retrieval

Sm and Lsm protein sequences were retrieved from the NCBI RefSeq database using the NCBI E-utilities API. For each of the seven eukaryotic Sm subtypes (SmB, SmD1, SmD2, SmD3, SmE, SmF, SmG) and eight Lsm subtypes (Lsm1–Lsm8), up to 500 sequences were fetched using gene name queries (e.g., `SmB[Gene Name] AND eukaryota[Organism] AND refseq[Filter]`). Archaeal Sm proteins were retrieved using `SmAP[Gene Name]` (136 sequences). Bacterial Hfq sequences were retrieved using `hfq[Gene Name] AND bacteria[Organism] AND refseq[Filter]` (500 of 19,778 total). A total of 6,103 sequences were collected across all categories.

To search for Sm/Lsm homologs in reduced-genome organisms, BLASTP searches were performed against the NCBI nr database restricted to DPANN archaea and CPR bacteria (Patescibacteria) using four query sequences: SmAP1 (*Methanothermobacter thermautotrophicus*, PDB:1JRI), SmAP2 (*Archaeoglobus fulgidus*, UniProt O28751), *E. coli* Hfq (UniProt P0A6X3), human SmB (UniProt P14678), and human Lsm1 (UniProt O15116). An E-value threshold of 1e-3 was applied.

### 2.2 Sequence filtering and redundancy reduction

Sequences were clustered at 70% amino acid identity using CD-HIT v4.8.1 with parameters `-c 0.7 -n 5`, reducing the dataset from 6,103 to 541 representative sequences. A 70% threshold was chosen to retain sufficient sequence diversity across divergent taxa while keeping the dataset computationally tractable for initial analysis; a subsequent analysis at 90% identity (1,453 sequences) is planned.

### 2.3 Multiple sequence alignment

Multiple sequence alignment was performed with MAFFT v7 using the `--auto` option. The resulting alignment of 541 sequences was used as input for phylogenetic inference.

### 2.4 Phylogenetic analysis

Maximum likelihood phylogenetic inference was performed using IQ-TREE3 v3.1.3. The best-fit substitution model was selected by ModelFinder under the Bayesian Information Criterion (BIC). Node support was assessed by ultrafast bootstrap approximation (UFBoot) with 1,000 replicates. Bayesian inference will be performed using MrBayes v3.2 following completion of the maximum likelihood analysis.

<!-- TODO: モデル・結果は完了後に追記 -->

---

## 3. Results

---

## 4. Discussion

---

## 5. Conclusion

---

## References

<!-- Zotero から出力 -->

---

## Figures

| Figure | Caption | Status |
|--------|---------|--------|
| Fig. 1 | | |
| Fig. 2 | | |

## Tables

| Table | Caption | Status |
|-------|---------|--------|
| Table 1 | | |
