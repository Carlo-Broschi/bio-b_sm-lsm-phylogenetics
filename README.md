# Sm/Lsm Phylogenetics (bio-b)

**Project ID:** bio-b
**Status:** Archived component of the integrated study **bio-c** (2026-07)
**Target journal:** Genome Biology and Evolution / Molecular Biology and Evolution
**Timeline:** 2026–2029

> **Note (2026-07):** This analysis has been consolidated into the integrated paper **bio-c** (https://github.com/Carlo-Broschi/bio-c_sm-fold-genome-reduction), which merges the Hfq and Sm/Lsm studies into one manuscript. Integrated study archived at Zenodo doi:10.5281/zenodo.21202213. This repository is retained as the archived component providing the Sm/Lsm three-domain tree and the DPANN/Asgard/CPR census; it is not submitted independently.

## Overview

A structure-informed phylogenomic census of the Sm/Lsm/Hfq superfamily across the
three domains of life, and a comparative analysis of how the Sm fold has fared in
the two prokaryotic reduced-genome radiations. The study is organised as a
phylogenetic *framework* (a structure-guided three-domain tree, IQ-TREE3 + MrBayes,
updating Veretnik et al. 2009) plus a comparative-distribution *finding*: a
completeness-controlled, ab-initio-annotated, structurally-verified census of
DPANN/Asgard archaea versus the bacterial CPR/Patescibacteria radiation.
Companion project to bio-a (Hfq), with reciprocal outgroups.

## Key results

- Reduced-genome **archaea (DPANN, Asgard) retain** the Sm fold in every
  quality-genome lineage examined (50 genomes, 70 hits); all 55 confidently
  modelled hits match an experimental Sm-fold anchor by Foldseek (TM-score ≥ 0.92,
  median 0.97).
- The bacterial **CPR/Patescibacteria radiation has lost** the fold entirely:
  0 hits in 397 quality genomes (incl. 393 Saccharibacteria with otherwise complete
  ribosomal machinery) — a clean negative that also controls the method.
- Retention in DPANN/Asgard was indicated qualitatively by earlier work
  (Reichelt et al. 2018); it is quantified and structurally verified here. The novel
  core is the rigorous distribution and the archaea-vs-bacteria asymmetry. The deep
  phylogenetic backbone is data-limited and used as scaffold, not primary result.

## Methods (distinctive)

Dual profile-HMMs (Sm/Lsm PF01423 + Hfq PF17209), NCBI Datasets retrieval with
CheckM completeness filtering, Prodigal ab initio gene prediction to remove
annotation gaps, FoldMason structure-guided MSA seeded from 19 experimental
Sm-fold PDB structures, and ESMFold + Foldseek structural verification of hits.

## Structure

| Path | Contents |
|------|----------|
| `0-literature/` | Structural anchors and literature-derived design notes |
| `0-original-data/` | Immutable source data |
| `1-downloaded-data/` | Sequences and proteomes (NCBI RefSeq / Datasets) |
| `2-preprocessed-data/` | Curated / filtered / aligned sequences |
| `3-analysis/` | IQ-TREE3, MrBayes, HMM census (`hmm/`) outputs |
| `4-results/` | Final trees, figures, census tables |
| `scripts/analytics/` | Python analysis scripts (fetch, HMM census, verify) |
| `scripts/viz/` | R / Python visualisation scripts |
| `refs/` | Bibliography and PDFs (managed via Zotero) |
| `reading/` | Reading notes per source |
| `design_from_literature.md` | Alignment/outgroup design derived from primary reading |
| `notes.md` | Analysis log and argument development |
| `draft.md` | Manuscript draft |
| `REFS_zotero_doi.txt` | Verified DOI list for Zotero import |

## Data and code availability

All analysis code and derived data are in this repository. Genome and sequence
accessions are listed in the manuscript's supplementary material. Archived at Zenodo:
doi:10.5281/zenodo.21197824 (this study) and doi:10.5281/zenodo.21197822 (companion Hfq study).

## Author

Minoru Nakai — Independent researcher
Email: vivaldi.rv484@gmail.com
