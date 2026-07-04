# The Sm fold diverges in fate between reduced-genome archaea and bacteria: a structure-informed phylogenomic census — Manuscript Draft

**Project:** bio-b — Sm/Lsm Phylogenetics
**Author:** Minoru Nakai
**Target journal:** Genome Biology and Evolution / Molecular Biology and Evolution
**Status:** Submission preparation (2026-07); integrated framing (framework + finding) finalized, science QC-locked, GBE format assembly in `../_gbe_submission/`

---

## Title candidates

- The Sm fold diverges in fate between reduced-genome archaea and bacteria: a structure-informed phylogenomic census
- (alt) Reduced-genome archaea retain, but CPR bacteria have lost, the Sm/Lsm fold
- (alt) A structure-guided phylogeny and reduced-genome distribution of the Sm/Lsm/Hfq superfamily

---

## Abstract

The Sm/Lsm/Hfq superfamily builds the RNA-associated toroidal rings that underlie processes from eukaryotic pre-mRNA splicing to bacterial small-RNA regulation, and its distribution across the three domains bears on the archaeal ancestry of the eukaryotic spliceosome. Using structures from all three domains, we built a structure-guided alignment and an updated phylogenetic framework for the superfamily, and on that scaffold we asked how the Sm fold has fared in the two prokaryotic reduced-genome radiations. A completeness-controlled census — using dual profile-HMMs (Sm/Lsm PF01423 and Hfq PF17209), ab initio gene prediction to remove annotation gaps, and structural verification of hits by ESMFold and Foldseek — shows that the radiations diverge. Reduced-genome archaea (DPANN and Asgard, including *Nanoarchaeum equitans* and cultured Lokiarchaeia) retain the Sm fold in every quality-genome lineage examined, with all 55 confidently modelled hits matching an experimental Sm-fold anchor (TM-score ≥ 0.92); this retention, indicated qualitatively by earlier work, is quantified and structurally verified here. In contrast, the bacterial CPR/Patescibacteria radiation has lost the fold entirely: no Hfq or Sm/Lsm protein was found in 397 quality genomes (including 393 Saccharibacteria with otherwise complete ribosomal machinery), a clean negative that also serves as an internal control on the method. The Sm fold thus shows a domain-level asymmetry in its fate under genome reduction — retained in archaea, lost in the bacterial CPR — establishing rigorously a contrast not previously drawn.

---

## Significance statement

The Sm/Lsm/Hfq fold builds the RNA-associated rings that underlie machinery across all cellular life, and its fate in reduced-genome lineages informs the archaeal origin of the eukaryotic spliceosome. Using a completeness-controlled, ab-initio-annotated and structurally-verified census, we show that the two prokaryotic reduced-genome radiations diverge: archaea (DPANN, Asgard) retain the Sm fold whereas the bacterial CPR radiation has lost it entirely. This domain-level asymmetry — drawn rigorously here — distinguishes genuine gene loss from the detection and assembly artifacts that confound reduced-genome surveys.

---

## 1. Introduction

### Background

The Sm/Lsm protein family is one of the most ancient and conserved families in the history of life. In eukaryotes, seven Sm proteins (SmB, SmD1, SmD2, SmD3, SmE, SmF, SmG) and eight Lsm proteins (Lsm1–Lsm8) form heptameric rings that associate with snRNAs to constitute the spliceosome and mRNA-decay machinery. Archaeal homologs (Sm-like archaeal proteins, SmAP) form similar homomeric rings involved in RNA binding, and the bacterial counterpart Hfq shares the same Sm fold — an N-terminal α-helix over a strongly bent five-stranded antiparallel β-sheet (Sm1 motif, β1–β3; Sm2 motif, β4–β5) — despite low sequence identity. The evolutionary relationships among these proteins across the three domains of life bear on the early evolution of the spliceosome (Veretnik et al. 2009) and on eukaryogenesis, since the eukaryotic Sm/Lsm machinery is thought to derive from an archaeal ancestor.

### Gap

The most comprehensive phylogenetic study of the Sm/Lsm family to date (Veretnik et al. 2009, PLoS Comput Biol) analyzed 335 sequences from 80 species using ClustalW alignment and PhyML with the JTT model. In the intervening ~17 years, the number of available sequences has grown by more than an order of magnitude, phylogenetic methods have advanced (ModelFinder, ultrafast bootstrap, Bayesian inference with convergence diagnostics), and — critically — the reduced-genome archaeal superphyla **DPANN** and the eukaryote-related **Asgard** archaea, essentially unsampled in 2009, are now represented by hundreds of (largely metagenome-assembled) genomes. Whether these deeply-branching, reduced-genome lineages encode Sm/Lsm proteins has been treated as an open question, and low-sensitivity BLAST searches have suggested their absence. However, BLAST cannot distinguish true gene loss from failure to detect divergent sequences, and metagenome-assembled genomes (MAGs) confound absence with incomplete assembly and annotation.

### Aims

This study is organized as a phylogenetic *framework* plus a comparative-distribution *finding*.

1. **Framework** — to place the Sm/Lsm/Hfq superfamily in an updated, structure-guided three-domain phylogeny (IQ-TREE3 + MrBayes; reciprocal archaeal-SmAP / bacterial-Hfq outgroups shared with the companion Hfq study), providing the evolutionary scaffold for the distribution analysis.
2. **Finding** — to test, with a completeness-controlled, ab-initio-annotated, structurally-verified census, how the Sm fold has fared in the two prokaryotic reduced-genome radiations, and to show that they diverge: reduced-genome **archaea (DPANN, Asgard) retain** the fold whereas the reduced-genome **bacterial radiation (CPR/Patescibacteria) has lost** it.

> **Framing note (updated 2026-07-05).** The project began as an attempt to *demonstrate absence* of Sm/Lsm in reduced-genome organisms (after an initial zero-hit BLAST). Two corrections followed. First, completeness-filtered HMM + ab-initio prediction showed DPANN/Asgard in fact retain the fold. Second — and importantly — a prior EFI-based survey (Reichelt et al. 2018) had already reported Sm-like proteins in representative DPANN/Asgard organisms, so this retention is *confirmed and quantified here, not discovered*. The manuscript's novel core is therefore the **rigorous, structurally-verified distribution and the archaea-vs-bacteria asymmetry**, set within the phylogenetic framework — not a claim of first detection. The deep phylogenetic backbone is data-limited (Section 3.2) and is used as scaffold rather than as the primary result.

---

## 2. Materials and Methods

### 2.1 Reference sequence set (Sm/Lsm/Hfq)

Sm, Lsm, SmAP and Hfq protein sequences were retrieved from NCBI RefSeq via the E-utilities API (eukaryotic Sm subtypes SmB/D1/D2/D3/E/F/G and Lsm1–Lsm8, up to 500 each; bacterial Hfq; archaeal SmAP). An initial gene-name–based retrieval (6,103 sequences) was found to contain substantial contamination from symbol-similar but unrelated proteins (e.g., "Smaug"/SAM-domain proteins matched by `SmG[Gene Name]`, and eukaryotic "Small Acidic Protein" matched by `SmAP[Gene Name]`, which returned no genuine archaeal Sm). Contaminants were removed with a curated description blacklist, and the archaeal Sm set was replaced with the manually curated 33 archaeal Sm sequences of Veretnik et al. (2009), yielding a clean reference set of **5,665 sequences** (`smlsm_all_curated.fasta`).

### 2.2 Redundancy reduction and length filtering

Curated sequences were length-filtered to 50–150 aa (retaining the ~76-aa Sm core domain while excluding full-length fusion proteins in which the Sm fold is a subdomain) and clustered at 90% identity with CD-HIT (5,665 → 5,133 → 1,107 representatives).

### 2.3 Structure-guided multiple sequence alignment

Because Sm/Lsm/Hfq proteins are short and highly divergent across domains, plain sequence alignment is unreliable at deep nodes (a straightforward MAFFT alignment expanded to ~92% gaps). A structural reference was therefore built from 19 experimentally determined Sm-fold structures spanning all three domains (eukaryotic Sm/U1 snRNP, archaeal SmAP, bacterial Hfq; PDB accessions listed in Table S1). These were structurally aligned with FoldMason (Gilchrist et al. 2026) and dereplicated (CD-HIT 95%) into a 25-sequence structural seed, which was used to guide alignment of the full sequence set with MAFFT (`--seed`). After occupancy trimming, the analysis alignment comprised 1,101 sequences × 184 columns, with a structurally-defined core of ~76 columns corresponding to the Sm fold.

### 2.4 Phylogenetic analysis

Maximum-likelihood inference used IQ-TREE3 v3.1.3 (Wong et al. 2026; note: the IQ-TREE **3** paper, not the IQ-TREE 2 paper Minh et al. 2020) with ModelFinder (BIC) and ultrafast bootstrap (1,000 replicates); Bayesian inference used MrBayes v3.2. Rooting follows the reciprocal-outgroup design shared with the companion Hfq study (bacterial Hfq and archaeal SmAP as mutual outgroups).

### 2.5 Distribution survey in DPANN, Asgard (and CPR)

Genomes of DPANN (nine lineages) and Asgard (five classes) archaea were retrieved via the NCBI Datasets v2 API. To avoid confounding true absence with incomplete assembly, genomes were filtered by CheckM completeness ≥ 50% and contamination ≤ 10% (MIMAG medium-quality), and GCA/GCF duplicates were removed. For genomes lacking an annotated proteome, genes were predicted ab initio with Prodigal (meta mode), removing annotation-gap artifacts. The resulting proteomes were scanned with two profile HMMs — the Sm/Lsm domain (Pfam **PF01423**) and the Hfq domain (Pfam **PF17209**) — under the trusted (`--cut_ga`) cutoff; each hit was typed as Sm/Lsm or Hfq by its higher-scoring model. The same pipeline was applied to CPR/Patescibacteria bacteria. Hit counts were aggregated at genome and species level, and lineages with no completeness-passing genome were reported as data-insufficient rather than as absences.

### 2.6 Structural verification of homologs

To confirm that HMM hits represent genuine Sm folds, each hit sequence was structurally modeled with ESMFold (ESM Atlas API) and the predicted structures were compared against the experimental Sm-fold anchors with Foldseek; a TM-score ≥ 0.5 to a Sm-fold anchor was taken as structural confirmation.

---

## 3. Results

### 3.1 A curated, contamination-controlled reference dataset

Gene-name–based retrieval of 6,103 sequences proved substantially contaminated: colour-coding an initial tree showed ~15% of tips to be unrelated proteins recruited by symbol-similar names — for example, `SmG[Gene Name]` matched hundreds of "Smaug"/SAM-domain proteins, and `SmAP[Gene Name]` returned eukaryotic "Small Acidic Protein" entries and no genuine archaeal Sm at all. After removing these with a curated description filter and substituting a manually curated set of archaeal Sm sequences, 5,665 clean sequences remained; length-filtering (50–150 aa) and 90% clustering reduced this to 1,107 representatives for alignment.

To confirm the curation, we mapped protein type onto the framework tree (Fig. 1): the four expected assemblages — bacterial Hfq (231 tips), archaeal SmAP (27), eukaryotic Lsm (498) and eukaryotic Sm-core (335) — separate cleanly, with the paralogue-specific subclades expected for each. Only ten tips (~1%) remained unclassifiable, and no large block of misplaced contaminants persisted, in contrast to the ~15% seen before curation. Consistent with the reciprocal-outgroup design, the bacterial Hfq clade is distinct while the archaeal SmAP sequences fall among the eukaryotic Sm/Lsm assemblages rather than with Hfq, as expected if archaeal Sm is ancestral to the eukaryotic system.

### 3.2 A structure-guided phylogenetic framework

We used 19 experimentally determined Sm-fold structures spanning the three domains to build a structure-guided alignment (Section 2.3) and inferred a maximum-likelihood tree (1,101 sequences, 184 sites; Q.INSECT+G4; log-likelihood −81,864) as the evolutionary framework for the distribution analysis that follows. The terminal and mid-depth clades — corresponding to the recognized eukaryotic Sm and Lsm paralogues, archaeal SmAP, and bacterial Hfq — are recovered (Fig. 1), but the deep backbone is poorly resolved: only 43% of internal branches reach UFBoot ≥ 95 and the bootstrap did not converge.

Critically, this is not a shortcoming of the sequence alignment. A control tree from a plain-sequence (MAFFT) alignment of the same taxa, trimmed comparably (196 sites), gave essentially the same picture — 48% of branches at UFBoot ≥ 95, again non-convergent — so structural guidance produced a principled, structurally-calibrated core but did not improve deep-node resolution. As in the companion Hfq study, the limit is set by the short length of these proteins rather than by the alignment method. We therefore use the tree as a scaffold that assigns each sequence to a fold type and domain, and interpret the distribution results (Sections 3.3–3.6) within it, rather than reading the deepest splits as resolved.

### 3.3 DPANN and Asgard archaea retain Sm/Lsm proteins

Applying the completeness-filtered dual-HMM pipeline to 50 quality genomes across DPANN and Asgard, we detected Sm/Lsm proteins in all six lineages with sufficient genome quality (Nanoarchaeota, Asgardarchaeota, Lokiarchaeia, Parvarchaeota, Micrarchaeota, Nanohaloarchaeota); all 70 hits were typed as Sm/Lsm and none as Hfq. All sampled Lokiarchaeia (Asgard) genomes, including the cultured *Promethearchaeum syntrophicum*, retain the fold, as does the DPANN type species *Nanoarchaeum equitans*. Eight lineages (e.g., Woesearchaeota, Thorarchaeia) had no completeness-passing genome and are reported as data-insufficient.

*Relation to prior work.* That some DPANN and Asgard archaea encode Sm-like proteins is not itself new: an EFI-based analysis of ~1,000 archaeal Lsm-domain proteins already placed SmAP genes in representative DPANN (including *N. equitans* and a Woesearchaeota) and Asgard organisms (Reichelt et al. 2018). Our contribution is to convert that qualitative observation into a systematic, completeness-controlled, ab-initio-annotated census across many metagenome-assembled genomes per lineage; to verify the hits structurally (Section 3.4); and — most importantly — to contrast archaeal retention with the bacterial CPR radiation (Section 3.5/3.6), which has lost the fold. We do not claim the discovery of Sm/Lsm in DPANN/Asgard; we establish its distribution rigorously and set it against the bacterial reduced-genome case.

### 3.4 Structural verification

All 55 hit sequences that yielded confident ESMFold models (mean pLDDT ≥ 0.7) matched an experimental Sm-fold anchor by Foldseek with high structural similarity (TM-score 0.92–1.00; median 0.97), and 49/55 were closest to an archaeal Sm anchor. The Sm/Lsm presence in DPANN/Asgard is therefore supported by both sequence (HMM) and structure (ESMFold + Foldseek).

### 3.5 CPR/Patescibacteria bacteria lack Hfq and Sm/Lsm

Applying the identical completeness-filtered dual-HMM pipeline to the bacterial reduced-genome radiation (CPR/Patescibacteria) gave the opposite result. Across 397 completeness-passing genomes (290,425 predicted proteins; mean 731 per genome), including 393 Saccharibacteria genomes spanning 15 species with cultured oral isolates, **no Hfq and no Sm/Lsm protein was detected** — neither PF17209 nor PF01423 returned any hit under the trusted cutoff, and ab initio gene prediction ruled out annotation artifacts. That the same pipeline recovered 70 archaeal hits, and that these CPR proteomes carry the expected universal machinery (e.g., 843 ribosomal-protein annotations), confirm the absence is biological rather than technical. The other CPR lineages (Parcubacteria, Microgenomates, Gracilibacteria, Dojkabacteria) had no completeness-passing genome and are data-insufficient. No prior study has examined Hfq or Sm-like proteins in any CPR lineage (literature survey), so this is the first assessment, and it is a rigorous true absence.

> **Comparison to the existing archaeal census.** Payá & Bonete (2023) manually surveyed 109 cultured archaeal species and found every genome to encode one to three Lsm proteins (their Fig. 1A: Nanoarchaeota single-copy in the species they sampled; Euryarchaeota mostly one, 74%; Crenarchaeota often two, 65%). Our result extends that picture to the reduced-genome, MAG-dominated DPANN and Asgard lineages they did not sample — which likewise retain Sm/Lsm — and contrasts it against the bacterial CPR radiation, which has lost the fold. The two censuses agree where they overlap (single-copy retention in the sampled Nanoarchaeota).

### 3.6 Reduced-genome archaea and bacteria diverge in Sm-fold fate

The two prokaryotic reduced-genome radiations went opposite ways: reduced-genome archaea (DPANN, Asgard) retain the Sm/Lsm fold, whereas the reduced-genome bacterial radiation (CPR) has lost the Hfq/Sm fold entirely. This contrast is consistent with the differing dispensability of the fold in the two domains — Hfq is frequently lost under bacterial genome reduction (as in several endosymbionts), whereas the archaeal Sm/Lsm system, ancestral to the eukaryotic spliceosomal machinery, is retained.

---

- **Central result — a domain-level asymmetry in Sm-fold fate under genome reduction.** Using one rigorous, completeness-controlled, ab-initio-annotated and structurally-verified pipeline, we find that the two prokaryotic reduced-genome radiations diverge: reduced-genome archaea (DPANN, Asgard) retain the Sm fold, whereas the reduced-genome bacterial radiation (CPR/Patescibacteria) has lost it entirely (0/397, including 393 Saccharibacteria genomes with full ribosomal machinery). The negative CPR result is also an internal control: the pipeline reports true absence when the gene is genuinely gone, so the archaeal retention is not an artifact of a method that "finds hits everywhere."
- **On novelty and prior work.** That DPANN/Asgard archaea encode Sm-like proteins was already indicated qualitatively (Reichelt et al. 2018); our contribution is the systematic, completeness-controlled, structurally-verified quantification and — the genuinely new element — the contrast with the bacterial CPR loss. We deliberately avoid claiming first detection.
- **Evolutionary interpretation.** The retained archaeal proteins are Sm/SmAP-type (structurally closest to archaeal anchors), consistent with the eukaryotic Sm/Lsm system deriving from an archaeal ancestor (Collins & Mabbutt 2001; Törő et al. 2001); retention in Asgard (Lokiarchaeia) provides primary data relevant to eukaryogenesis. The bacterial loss fits a broader pattern: Hfq is present in only about half of bacteria and its distribution reflects gene loss rather than lateral transfer, with the protein specifically absent from reduced-genome parasites and endosymbionts (e.g. *Buchnera*, *Rickettsia*; Sun, Zhulin & Wartell 2002) — itself part of the pervasive gene loss that accompanies bacterial genome reduction (Moran & Bennett 2014). The radiation-wide absence of Hfq across the CPR is thus an extreme case of this trend.
- <!-- SmAP1/SmAP2 パラログ史（Collins 2001 の Lsmα普遍/Lsmβγ可変、Nikulin 2020 の Sm1 第3位 His vs Thr）を系統的形質として。lsmα-L37e オペロン(Collins 2001/Payá 2023)をシンテニー形質に。 -->
- **Limitations.** Genome quality caps the assessable archaeal lineages to six and the assessable CPR to essentially Saccharibacteria; the structure-guided alignment leaves the deepest backbone data-limited (hence the phylogeny is used as a framework, not a resolved deep tree). The CPR side of the contrast rests chiefly on one well-sampled lineage, which we treat as the decisive test rather than a domain-wide claim.

---

## 5. Conclusion

Within an updated, structure-guided phylogenetic framework for the Sm/Lsm/Hfq superfamily, a completeness-controlled and structurally-verified census reveals that the two prokaryotic reduced-genome radiations have taken opposite paths: archaea (DPANN, Asgard) retain the Sm fold, whereas the CPR/Patescibacteria bacteria have lost it. This domain-level asymmetry — quantified rigorously here rather than discovered — is the study's central contribution, with the archaeal retention bearing on the archaeal ancestry of the eukaryotic Sm/Lsm machinery.

---

## Data Availability

Reference sequences were retrieved from NCBI RefSeq; DPANN/Asgard/CPR genomes via the NCBI Datasets API (accessions in the manifests). The curated sequence set, structure-guided alignment, tree files, HMM profiles (PF01423, PF17209), the census output tables, ESMFold-predicted structures and Foldseek verification, the structural-anchor PDB list, and all analysis and figure-generating scripts are available in the project repository (https://github.com/Carlo-Broschi/bio-b_sm-lsm-phylogenetics). Bulk downloaded proteomes and predicted structures are regenerable from accession numbers via the provided scripts. <!-- 投稿時：private→public 化、または Zenodo deposit で DOI 付与。 -->

---

## References

<!-- Zotero から出力 -->

---

## Figures

| Figure | Caption | Status |
|--------|---------|--------|
| Fig. 1 | Structure-guided Sm/Lsm phylogeny across three domains, tips colored by type (Hfq / SmAP / Lsm / Sm-core). | **Rendered** (`4-results/smlsm_structguided_types.pdf`, structure-guided framework tree) |
| Fig. 2 | (A) Sm-fold distribution across reduced-genome radiations: DPANN/Asgard archaea retain Sm/Lsm (high per-lineage fraction) while CPR bacteria have lost it (0/393 Saccharibacteria etc.); (B) structural verification — all 55 archaeal ESMFold hits match a Sm-fold anchor by Foldseek (TM-score ≥ 0.92, median 0.97). | **Rendered** (`4-results/fig_distribution_verification.pdf`) |

## Tables

| Table | Caption | Status |
|-------|---------|--------|
| Table 1 | Sm/Lsm and Hfq counts per DPANN/Asgard/CPR lineage (genome- and species-level), with completeness. | **Rendered** (below) |
| Table S1 | Sm-fold structural anchors (PDB accessions, organism, domain) used for structure-guided alignment. | Ready (`0-literature/structural_anchors.md`) |

**Table 1.** Sm/Lsm and Hfq incidence across the sampled reduced-genome radiations. Genome and species counts are after CheckM completeness filtering (≥50% complete, ≤10% contaminated); "genomes with Sm/Lsm" and "genomes with Hfq" count genomes carrying at least one PF01423 (Sm/Lsm) or PF17209 (Hfq) hit, respectively; "Sm/Lsm hits" and "Hfq hits" are total domain hits summed over genomes; mean completeness is the CheckM mean over each lineage's genomes. Every archaeal lineage retains the Sm fold in nearly all assessable genomes, whereas the bacterial CPR radiation carries neither Sm/Lsm nor Hfq in any of 397 genomes despite comparable assembly completeness — excluding low completeness as an explanation for the bacterial absence.

| Domain (radiation) | Lineage | Genomes | Species | Genomes w/ Sm/Lsm | Genomes w/ Hfq | Sm/Lsm hits | Hfq hits | Mean completeness (%) |
|---|---|--:|--:|--:|--:|--:|--:|--:|
| Archaea (DPANN/Asgard) | *Nanoarchaeota* | 16 | 4 | 14 | 0 | 14 | 0 | 67.9 |
| Archaea (DPANN/Asgard) | *Asgardarchaeota* | 11 | 6 | 10 | 0 | 24 | 0 | 82.9 |
| Archaea (DPANN/Asgard) | *Lokiarchaeia* | 8 | 4 | 8 | 0 | 20 | 0 | 78.5 |
| Archaea (DPANN/Asgard) | *Parvarchaeota* | 7 | 2 | 4 | 0 | 4 | 0 | 66.9 |
| Archaea (DPANN/Asgard) | *Micrarchaeota* | 4 | 4 | 4 | 0 | 4 | 0 | 86.2 |
| Archaea (DPANN/Asgard) | *Nanohaloarchaeota* | 4 | 3 | 4 | 0 | 4 | 0 | 85.4 |
| **Archaea — subtotal** | | **50** | **23** | **44** | **0** | **70** | **0** | **75.6** |
| Bacteria (CPR/Patescibacteria) | *Saccharibacteria* | 393 | 15 | 0 | 0 | 0 | 0 | 82.0 |
| Bacteria (CPR/Patescibacteria) | *Candidatus* Absconditabacteria | 3 | 3 | 0 | 0 | 0 | 0 | 81.5 |
| Bacteria (CPR/Patescibacteria) | *Patescibacteria* (unclassified) | 1 | 1 | 0 | 0 | 0 | 0 | 80.7 |
| **Bacteria — subtotal** | | **397** | **19** | **0** | **0** | **0** | **0** | **82.0** |
