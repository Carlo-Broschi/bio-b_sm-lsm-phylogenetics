# bio-b — QC ハンドオフ（Claude Science バックグラウンド・レビュアー用）

**目的**：`draft.md` の (a) 引用、(b) 数値、(c) 図とコードの整合 を Claude Science のレビュアーに検証させる。本ファイルは「数値→出所」の追跡可能性対応表と、レビュアーに読み込ませるべきファイル一覧。

## Claude Science に読み込ませるもの
1. `draft.md`（原稿）
2. データ（数値の出所）：`3-analysis/hmm/census_lineage*.tsv`, `census_species*.tsv`, `1-downloaded-data/*manifest.tsv`, `4-results/smfold_foldseek_verification.tsv`, `4-results/biob_tip_types.tsv`
3. 図生成コード＋図：`scripts/viz/plot_distribution_figure.py`＋`4-results/fig_distribution_verification.pdf`；`scripts/viz/plot_biob_types.R`＋`4-results/smlsm_curated_types.pdf`
4. 手法コード：`scripts/analytics/{fetch_dpann_asgard_proteomes,hmm_type_census,predict_smfold_hits,verify_smfold_foldseek,build_structguided_msa}.py`
5. 引用の一次ソース：`0-literature/structural_anchors.md`, `0-literature/cpr_hfq_references.csv`

## 数値→出所 対応表（自己 QC 済み 2026-07-05）
| draft の主張 | 値 | 出所ファイル | 照合 |
|---|---|---|---|
| 初期取得→curated | 6,103→5,665 | filter_contaminants.py 実行ログ / smlsm_all_curated.fasta | ✅ |
| 長さフィルタ→nr90 | 5,665→5,133→1,107 | 2-preprocessed-data/*.fasta | ✅ |
| コンタミ ~15% | ~15% | 旧 nr70 色分け（notes 06-24） | ✅ |
| 型内訳 | Hfq231/SmAP27/Lsm499/Sm-core335/Other5 | biob_tip_types.tsv | ✅ |
| 構造アンカー数 | 19 PDB→seed 25×219 | structural_anchors.md / structure_anchor_seed.fa | ✅ |
| 構造ガイド trim | 1,101×184（コア~76） | smlsm_structguided_trim.fasta | ✅ |
| DPANN/Asgard census | 50 genome・70 hit・6系統 | census_lineage.tsv / hits_all.tsv | ✅ |
| 構造検証 | 55/55、TM 0.918–0.999、**中央値0.967(≈0.97)** | smfold_foldseek_verification.tsv | ✅（0.96→0.97 に修正済） |
| 最良アンカー古細菌Sm | 49/55 | verification tsv（1I5L14+1I4K11+1M5Q9+1I8F8+1M8V4+1H64 3） | ✅ |
| CPR census | 0/397（Saccha 393）、リボソーム注釈843 | census_lineage_cpr.tsv / proteomes_cpr | ✅ |
| Payá&Bonete 比較 | 109種・163 Lsm | Payá&Bonete 2023 原著（精読済） | ✅ |
| §3.2 構造ガイド木 | 1101×184、Q.INSECT+G4、logL −81864、UFBoot≥95 470/1092(43%)、非収束 | smlsm_tree_structguided.iqtree/.contree | ✅ |
| §3.2 生配列版対照 | 196 sites、UFBoot≥95 519/1087(48%)、非収束（構造ガイドで改善せず） | smlsm_tree_curated_nr90.contree | ✅ |
| Fig.1 型内訳（構造ガイド木） | Hfq231/SmAP27/Lsm498/Sm335/Other10(~1%) | smlsm_structguided_types + biob_tip_types.tsv | ✅ |

## 自己 QC で見つけて修正した不整合（レビュアーへの申し送り）
- **TM-score 中央値**：図・caption が「0.96」、本文§3.4 が「0.97」で不整合。正確な中央値＝0.967(≈0.97)。→ 図(`plot_distribution_figure.py`)と Fig.2 caption を **0.97 に統一済み**（2026-07-05）。

## 引用の要注意（レビュアーに重点確認させる）
- **Reichelt et al. 2018**：新規性の位置づけの要（「発見でなく定量」）。引用が正しく効いているか。
- **[to verify] 事項**：Moran & Bennett 2014 の「縮小ゲノムで Hfq 喪失」、genome サイズ値（~140kb/~1Mb）は原著未照合。Discussion で使う際は要確認。
- DOI 検証：CPR 9本は CrossRef で 9/9 確認済み（cpr_hfq_references.csv）。
