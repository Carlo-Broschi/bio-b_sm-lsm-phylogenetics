# bio-b: Sm/Lsm系統解析 データログ

## ファイル一覧

### raw/veretnik2009_bacteria.fasta
- Source: NCBI Protein（Veretnik et al. 2009 補足データのGI番号から取得）
- Date: 2026-06-22
- Sequences: 64
- Note: 細菌 Hfq 配列

### raw/veretnik2009_archaea.fasta
- Source: NCBI Protein（同上）
- Date: 2026-06-22
- Sequences: 33
- Note: 古細菌 SmAP 配列（DPANN は Nanoarchaeum equitans のみ含む）

### raw/veretnik2009_eukaryotes.fasta
- Source: NCBI Protein（同上）
- Date: 2026-06-22
- Sequences: 250
- Note: 論文記載262件より12件少ない（GI廃番分）

### raw/veretnik2009_all.fasta
- Source: 上記3ファイルを結合
- Date: 2026-06-22
- Sequences: 347
- MD5: 6777b3fc05352077f7ae606b1c1af081
- Note: 論文記載335件より多いのは一部GIが複数配列にマップされたため

---

## Command Log

### Veretnik 2009 ベースライン配列取得
```bash
# scripts/fetch_veretnik2009.py を使用
# GI番号リストは Veretnik et al. (2009, PLoS Comput Biol) Supplementary Methods より
cd bio-b_sm-lsm-phylogenetics
/path/to/shared/venv-bio/bin/python scripts/fetch_veretnik2009.py
# → data/raw/veretnik2009_{bacteria,archaea,eukaryotes,all}.fasta
```

### DPANN Sm/Lsm 検索（NCBI BLAST、結果取得失敗）
```bash
# scripts/blast_dpann.py を使用
# クエリ: SmAP1 (Methanothermobacter thermautotrophicus, PDB:1JRI)
# 対象: DPANN[Organism] を ENTREZ_QUERY に指定
# RID: 3GJMWGZY014
# 結果: 0ヒット or ファイル破損のため再取得が必要
```

---

## 先行研究

- Veretnik S, Bourne PE, Alexandrov NN, Shindyalov IN (2009).
  "Sm/Lsm Genes Provide a Glimpse into the Early Evolution of the Spliceosome."
  *PLoS Comput Biol* 5(3): e1000314.
  - データ：80種335配列
  - 手法：PhyML最尤法
  - 限界：DPANNなし・AlphaFold2なし・旧式ツール

---

## TODO
- [ ] DPANN Sm/Lsm 配列の取得（NCBI BLAST 再試行 or 文献から）
- [ ] 長さフィルタ適用
- [ ] CD-HIT による冗長配列除去
- [ ] MAFFT アラインメント
- [ ] IQ-TREE3 + MrBayes による系統推定
- [ ] 外群設定（細菌 Hfq を外群に）
