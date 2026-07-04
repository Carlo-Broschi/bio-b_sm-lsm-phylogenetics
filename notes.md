# bio-b Research Notes — Sm/Lsm Phylogenetics

**Author:** Minoru Nakai
**Started:** 2026-06-22

---

## 研究概要

Sm および Lsm タンパク質の系統解析。DPANN アーキアにおける分布と、
真核生物の spliceosomal Sm タンパク質への進化的連続性を検討する。
bio-a（Hfq）と並行して進め、Sm/Lsm スーパーファミリー全体の進化を俯瞰する。

**中心的な問い：**
- DPANN アーキアの Sm 様タンパク質は細菌 Hfq と真核 Sm のどちらに近いか
- Sm/Lsm の機能分化（RNA 結合特異性）はいつ生じたか
- 共通祖先の Sm 様タンパク質はどのような特徴を持っていたか

---

## 解析ログ

<!-- 時系列（上ほど古い／下ほど新しい）で記録する -->

### 2026-06-22 — Veretnik 2009 ベースライン配列取得

**目的：** Veretnik et al. (2009) のデータセットを再現し、本研究のベースラインとする

**背景・判断：**
bio-b は Veretnik 2009（PLoS Comput Biol）の更新を骨格とする。
同論文の Supplementary Methods に GI 番号リストが掲載されており、これを使って
NCBI から配列を再取得した。GI 番号は古い識別子で廃番や再マップが起きているため、
取得数は論文記載値と一致しない可能性があった。

**スクリプト：** `scripts/analytics/fetch_veretnik2009.py`
- ライブラリ：`requests`（NCBI E-utilities 直接呼び出し）
- GI番号リストをカテゴリ（細菌・古細菌・真核生物）別に分類してから efetch

```bash
cd ~/Workspace/Research/Biology/bio-b_sm-lsm-phylogenetics
/Users/carlobroschi_imac/Workspace/Research/shared/venv-bio/bin/python scripts/analytics/fetch_veretnik2009.py
```

**結果：**

| ファイル | 配列数 | 論文記載 | 差分の理由 |
|---|---|---|---|
| `veretnik2009_bacteria.fasta` | 64 | 64 | 一致 |
| `veretnik2009_archaea.fasta` | 33 | 33 | 一致 |
| `veretnik2009_eukaryotes.fasta` | 250 | 262 | GI 廃番 12 件 |
| `veretnik2009_all.fasta` | **347** | 335 | 一部 GI が複数配列にマップ |

- MD5（all）：`6777b3fc05352077f7ae606b1c1af081`
- 古細菌33件のうち DPANN は *Nanoarchaeum equitans* 1種のみ含む

---

### 2026-06-22 — DPANN・CPR への Sm/Lsm 相同体 BLAST 検索

**目的：** DPANN アーキアと CPR 細菌に Sm/Lsm・Hfq 相同体が存在するかを確認する

**背景・判断：**
DPANN と CPR はいずれも極端に縮小したゲノムを持つ超寄生性の生物群で、
RNA プロセシング因子を多数失っている可能性がある。
これを確認するために複数クエリ・複数ターゲットで BLAST を実施した。

クエリ選択の根拠：
- **SmAP1**（*M. thermautotrophicus*、PDB:1JRI）：古細菌 Sm の代表。DPANN 検索に適切
- ***E. coli* Hfq**（UniProt P0A6X3）：細菌 Sm 様タンパク質の代表。CPR（細菌）検索に適切
- **ヒト SmB**（P14678）：真核 Sm コアの代表。広域検索に使用
- **ヒト Lsm1**（O15116）：真核 Lsm の代表。広域検索に使用

当初 SmAP1 クエリのみ CPR に使用したが、CPR は細菌であり古細菌クエリでは
検出感度が低いと気づき、Hfq クエリを追加した。

**スクリプト：** `scripts/analytics/blast_dpann.py`（SmAP1 × DPANN）、`scripts/analytics/blast_cpr.py`（複数クエリ × CPR・DPANN）
- NCBI BLAST Web API（リモート blastp、`nr` データベース）
- `ENTREZ_QUERY` で生物を絞り込み
- E値閾値：1e-3
- ヒット上限：200件

```bash
# SmAP1 × DPANN
/Users/carlobroschi_imac/Workspace/Research/shared/venv-bio/bin/python scripts/analytics/blast_dpann.py

# Hfq・Sm1・Lsm1 × CPR および DPANN
/Users/carlobroschi_imac/Workspace/Research/shared/venv-bio/bin/python scripts/analytics/blast_cpr.py
```

**トラブルと対処：**
NCBI BLAST API の JSON2 フォーマットは ZIP 圧縮バイナリで返される。
当初 `response.text`（文字列）で保存したため ZIP が破損し、ヒット抽出に失敗した。
`response.content`（バイナリ）で保存するよう修正し、`zipfile` モジュールで解凍してパースするよう変更した。
破損ファイルは削除し、修正後のスクリプトで再実行した。

**結果（2026-06-22 確定）：**

| クエリ | 対象 | ヒット |
|---|---|---|
| SmAP1（*M. thermautotrophicus*） | DPANN | **0** |
| Hfq (*E. coli*) | CPR | **0** |
| SmB (ヒト) | CPR | **0** |
| Lsm1 (ヒト) | CPR | **0** |
| SmB (ヒト) | DPANN | **0** |
| Lsm1 (ヒト) | DPANN | **0** |

全クエリ・全ターゲットで E 値 1e-3 以下のヒットなし。

> ⚠️ **後日（2026-07-04）補足：BLAST 0ヒットは感度限界と区別できないため、HMM（PF01423/PF17209）による高感度再検証に発展。下記 07-04 の HMM 検索を参照。実際、completeness フィルタ＋HMM では DPANN 複数系統で Sm/Lsm を検出しており、この BLAST 0ヒットは「感度不足」だったと判明。**

**次のステップ：**
- ヒットあり → FASTA 取得 → Veretnik データセットに追加
- ヒットなし → 「縮小ゲノム生物は Sm/Lsm ファミリーを欠く」として考察に記載

---

### 2026-06-22 — BLAST 結果確定・スクリプト修正

**トラブルの詳細：**
最初の実行（`blast_dpann.py`）で BLAST 結果ファイルが 32KB で保存されたが、JSON としてパースできなかった。
調査したところ NCBI BLAST API の JSON2 フォーマットは ZIP 圧縮バイナリで返されることが判明した。
`response.text`（文字列）で保存していたため、バイナリが破損していた。

**修正内容（`blast_dpann.py`・`blast_cpr.py` 共通）：**
- `response.text` → `response.content`（バイナリ保存）
- `out.write_text()` → `out.write_bytes()`
- `extract_accessions()` を regex → `zipfile` モジュールで ZIP を解凍してパースするよう書き直し

**再実行後の確定結果（2026-06-22）：**

| クエリ | 対象 | ヒット |
|---|---|---|
| SmAP1（*M. thermautotrophicus*） | DPANN | **0** |
| Hfq (*E. coli*) | CPR | **0** |
| SmB (ヒト) | CPR | **0** |
| Lsm1 (ヒト) | CPR | **0** |
| SmB (ヒト) | DPANN | **0** |
| Lsm1 (ヒト) | DPANN | **0** |

全クエリ・全ターゲットで E 値 1e-3 以下のヒットなし。

**解釈（当時）：**
DPANN アーキアおよび CPR 細菌には Sm/Lsm・Hfq のいずれの相同体も検出されなかった。
複数の独立したクエリ（古細菌型・細菌型・真核型）すべてでヒットゼロだったため、
これらの生物群が Sm/Lsm ファミリーを持たないという結論は信頼性が高い（と当時は判断）。
また Saito et al. (2019) でも *Nanoarchaeum equitans* の Clp1 ファミリーが 0 件と記録されており、
複数の RNA 処理因子の欠落として整合的な結果である。
※ この解釈は 07-04 の HMM 検索で更新（BLAST の感度限界だった）。

---

### 2026-06-22 — SmAP2 × DPANN・CPR BLAST 追加検索

**目的：** SmAP1 でゼロだった古細菌クエリが1種のみだったため、SmAP2（*Archaeoglobus fulgidus*、UniProt O28751）で補完する

**スクリプト：** `scripts/analytics/blast_smAP2.py`

```bash
/Users/carlobroschi_imac/Workspace/Research/shared/venv-bio/bin/python scripts/analytics/blast_smAP2.py
```

**結果：**

| クエリ | 対象 | ヒット |
|---|---|---|
| SmAP2（*A. fulgidus*） | DPANN | **0** |
| SmAP2（*A. fulgidus*） | CPR | **0** |

SmAP1・SmAP2 の両方でゼロを確認。古細菌クエリ1種のみのバイアスを排除できた。

---

### 2026-06-22 — 本番データセット取得（fetch_smlsm.py）

**目的：** Veretnik 2009（335配列）から約20年分のデータを加えた本番データセットを構築する

**スクリプト：** `scripts/analytics/fetch_smlsm.py`

- 真核 Sm：SmB/D1/D2/D3/E/F/G（各 RefSeq 上限500件）
- 真核 Lsm：Lsm1〜Lsm8（各 RefSeq 上限500件）
- 古細菌 Sm：SmAP[Gene Name]（136件全件）
- 細菌 Hfq：hfq[Gene Name] × bacteria × RefSeq（上限500件）

**注意：** `sm-like archaeal protein[Protein Name]` では 0 件。`SmAP[Gene Name]` に変更して 136 件取得。

**結果（2026-06-22）：**

| カテゴリ | 取得数 / 総件数 |
|---|---|
| SmB | 155 / 155 |
| SmD1 | 232 / 232 |
| SmD2 | 273 / 273 |
| SmD3 | 253 / 253 |
| SmE | 87 / 87 |
| SmF | 151 / 151 |
| SmG | 316 / 316 |
| Lsm1 | 500 / 1,235 |
| Lsm2 | 500 / 622 |
| Lsm3 | 500 / 1,177 |
| Lsm4 | 500 / 1,261 |
| Lsm5 | 500 / 1,239 |
| Lsm6 | 500 / 1,824 |
| Lsm7 | 500 / 1,326 |
| Lsm8 | 500 / 1,039 |
| SmAP（古細菌） | 136 / 136 |
| Hfq（細菌） | 500 / 19,778 |
| **合計** | **6,103** | |

出力：`1-downloaded-data/fetch_*.fasta`、`1-downloaded-data/smlsm_all.fasta`

> ⚠️ **後日判明（2026-07-03）：この取得データには重大なコンタミ・古細菌ソース失敗がある。下記「データセットキュレーション」参照。上表の SmG 316 / SmAP 136 はほぼ全てが誤取得だった。**

---

### 2026-06-22 — CD-HIT・MAFFT・IQ-TREE3（本番データセット）— コンタミ入り（後に破棄）

**目的：** 6,103配列から冗長除去し、系統推定を行う

**CD-HIT：**

```bash
# 90% → 1,453件
cd-hit -i 1-downloaded-data/smlsm_all.fasta -o 2-preprocessed-data/smlsm_full_nr90.fasta -c 0.9 -n 5 -T 4 -M 4000

# 70% → 541件（本番第一弾として採用）
cd-hit -i 1-downloaded-data/smlsm_all.fasta -o 2-preprocessed-data/smlsm_full_nr70.fasta -c 0.7 -n 5 -T 4 -M 4000
```

70% を採用した理由：Veretnik 2009（335配列）に近い規模で最初のトポロジーを確認してから、90%（1,453件）に移行する方針。

**MAFFT：**

```bash
mafft --auto --quiet 2-preprocessed-data/smlsm_full_nr70.fasta > 3-analysis/smlsm_aln_full_nr70.fasta
# → 541配列
```

**IQ-TREE3：**

```bash
nohup iqtree3 -s 3-analysis/smlsm_aln_full_nr70.fasta \
              -m TEST -B 1000 -T AUTO \
              --prefix 4-results/smlsm_tree_full_nr70 \
              > /tmp/iqtree3_biob_full.log 2>&1 &
# PID: 31317
```

> ⚠️ この nr70 樹で色分けした結果、約15%がコンタミと判明（07-03 参照）。**このデータセットは破棄し curated 版で再解析。**

---

### 2026-06-22 — Veretnik データセットのパイプライン（動作確認用）

**目的：** 347配列で CD-HIT → MAFFT → IQ-TREE3 が動くことを確認する（本番前の動作確認）

```bash
# CD-HIT: 347 → 292配列
cd-hit -i 1-downloaded-data/veretnik2009_all.fasta -o 2-preprocessed-data/smlsm_nr90.fasta -c 0.9 -n 5 -T 4 -M 4000

# MAFFT
mafft --auto --quiet 2-preprocessed-data/smlsm_nr90.fasta > 3-analysis/smlsm_aln_nr90.fasta

# IQ-TREE3（PID: 13061）
nohup iqtree3 -s 3-analysis/smlsm_aln_nr90.fasta -m TEST -B 1000 -T AUTO \
              --prefix 4-results/smlsm_tree_nr90 > /tmp/iqtree3_biob.log 2>&1 &
```

**結果（2026-06-24 完了）：**
- BIC 最適モデル：**Q.PFAM+G4**
- 700 iterations で収束・完了
- 出力：`4-results/smlsm_tree_nr90.*`（.treefile / .contree 等）

---

### 2026-06-22 — DPANN ゲノムサーベイ

**目的：** DPANN に分類される生物のゲノム登録数と、Sm/Lsm/Hfq アノテーションの有無を網羅的に確認する

**スクリプト：** `scripts/analytics/survey_dpann.py`
- NCBI Assembly DB から各 DPANN タクソンのゲノム登録数を取得
- NCBI Protein DB でキーワード（sm protein / lsm protein / sm-like / hfq / RNA chaperone / SmAP）× DPANN タクソンを全組み合わせ検索

**ゲノム登録数（2026-06-22 時点）：**

| タクソン | アセンブリ数 |
|---|---|
| Woesearchaeota | 1,957 |
| Aenigmarchaeota | 685 |
| Pacearchaeota | 438 |
| Parvarchaeota | 241 |
| Diapherotrites | 216 |
| Nanohaloarchaeota | 4 |
| Nanoarchaeota | 3 |
| Nanoarchaeales | 2 |
| Micrarchaeota | 2 |

種リスト：`1-downloaded-data/dpann_species_list.txt`

**Sm/Lsm/Hfq アノテーション検索結果：** 全タクソン × 全キーワードで **0 件**。

これは NCBI タンパク質 DB のアノテーション自体に Sm/Lsm/Hfq が登録されていないことを示す。
※ ただしアノテーション欠如＝遺伝子欠如ではない（07-04 の Prodigal + HMM でこの交絡を除去し、実際に検出）。

---

### 2026-06-22 — ディレクトリ移行（Kryukov方式）

bio-a と同時に移行スクリプトで実施。

```bash
bash ~/Workspace/Research/Biology/migrate_to_kryukov.sh
```

**移行後の構造：**
- `1-downloaded-data/`：Veretnik 2009 FASTA・BLAST JSON
- `2-preprocessed-data/`：（今後：CD-HIT・長さフィルタ後）
- `3-analysis/`：（今後：アラインメント）
- `4-results/`：（今後：系統樹）

---

### 2026-06-24 — Veretnik nr90 系統樹のラベル付与・可視化

**目的：** contree のアクセッション番号を `accession|protein_name|organism` 形式に変換し、FigTree と Python で閲覧する

**ラベル付与：**
- `4-results/smlsm_tree_nr90.contree` → `4-results/smlsm_tree_nr90_annotated.contree`
- `accession|protein_name|organism` 形式で重複排除（accession を先頭に付けることで unique 保証）

**FigTree 起動（Java 26 対応）：**
FigTree v1.4.4 の `.app` バンドルは Java 26 を認識しない。以下のコマンドで起動：

```bash
java -jar /Applications/FigTree.app/Contents/Resources/Java/figtree.jar \
     4-results/smlsm_tree_nr90_annotated.contree &
```

ラッパースクリプト `/opt/homebrew/bin/figtree` でも同様に起動可能。

**Python カラー可視化：**
FigTree のハイライト機能が無根ツリー表示では動作しなかったため、dendropy + matplotlib で PNG を生成。

```bash
/Users/carlobroschi_imac/Workspace/Research/shared/venv-bio/bin/python \
    scripts/analytics/viz_tree_colored.py
```

- 出力：`4-results/smlsm_tree_nr90_colored.png`（1200×~2200px、dpi=150）
- 色分け：SmD1/D2/D3 / SmB/E/F/G / Lsm1-7 / Lsm8 / SmAP / Hfq / Sm-Lsm(unspecified) の 11 カテゴリ
- スクリプト保存先：`scripts/analytics/viz_tree_colored.py`
- **この可視化で nr70 に約15%のコンタミを発見 → 07-03 のキュレーションへ。**

---

### 2026-07-03 — データセットキュレーション（コンタミ除去・古細菌ソース修復）

**発端：** nr70 の色分け系統樹で約15%（79/541）が Sm/Lsm と無関係のコンタミと判明。全データ（6,103本）の混入源を診断した。

**診断結果：** `fetch_smlsm.py` の緩い `[Gene Name]` クエリが2種類の失敗を起こしていた。

| 問題 | 内容 |
|---|---|
| (A) コンタミ混入 | `SmG[Gene Name]` → "**Smaug**"/SAM domain (SAMD4) を **302本**誤マッチ。SmF/SmD2/SmB も HMG・RNA polymerase・NAC・bromodomain 等を少数誤マッチ |
| (B) 古細菌ソース完全失敗 | `SmAP[Gene Name]` → 古細菌 Sm を**1本も取れず**、真核 "**Small Acidic Protein**"(SMAP) 136本を誤取得。`fetch_archaea_SmAP.fasta` の中身は **100% 非古細菌**（Symbiodinium・Homo・ペンギン等） |

問題(B)が特に致命的：本論文の核心は3ドメインの Sm/Lsm 進化であり、古細菌 Sm がゼロでは成立しない。

**対処スクリプト：** `scripts/analytics/filter_contaminants.py`
- (A) 明確なコンタミ説明文をブラックリスト除外（真の Sm/Lsm の多様な命名は温存）
- (B) `fetch_archaea_SmAP` 由来を全除外 → Veretnik 2009 のキュレート済み古細菌 Sm 33本（`veretnik2009_archaea.fasta`、Euryarchaeota/Crenarchaeota/Nanoarchaeota/Thermoplasmata 網羅）に差し替え

```bash
/Users/carlobroschi_imac/Workspace/Research/shared/venv-bio/bin/python \
    scripts/analytics/filter_contaminants.py
# 6103 → コンタミ458除去 → 非古細菌SmAPゴミ13除外 → Veretnik古細菌+33 = 5665本
```

**結果：** `2-preprocessed-data/smlsm_all_curated.fasta`（**5,665本**、残コンタミ0）。除去記録は `smlsm_contaminants_removed.txt`。

**検証：**
- 残存ファイルにコンタミ語（smaug/small acidic/bromodomain/HMG）**0件**
- 除去リストに真の Sm/Lsm（ribonucleoprotein/snRNP/lsm/hfq）**0件**（誤除去なし）
- 古細菌 Sm が 0 → 33 に修復

**次のステップ：** 本番の CD-HIT → MAFFT → IQ-TREE は curated を入力にやり直す（旧 nr70/nr90 はコンタミ入りのため破棄）。

---

### 2026-07-04 — curated 再解析（CD-HIT → MAFFT → trim → IQ-TREE3）

bio-a の MrBayes 停止で CPU が空いたため、curated データで本番パイプラインを再実行。

**長さフィルタ（50-150 aa）：** curated 5,665 → **5,133**。除外した >150 aa は残コンタミではなく**本物の真核 Sm/Lsm 全長タンパク**（LSm7 全長〜548 aa 等、Sm ドメインは ~76 aa の部分ドメイン）。生投入すると整列が崩れるため bio-a と同じ長さ基準に統一。厳密なドメイン抽出は後段の PF01423/構造ガイド工程（design memo §2/§3）に委ねる。

```bash
# 50-150 フィルタ → CD-HIT nr90
cd-hit -i 2-preprocessed-data/smlsm_curated_len50-150.fasta \
       -o 2-preprocessed-data/smlsm_curated_nr90.fasta -c 0.9 -n 5 -T 4 -M 4000
# 5133 → 1107 配列
mafft --auto --quiet 2-preprocessed-data/smlsm_curated_nr90.fasta \
      > 3-analysis/smlsm_curated_aln_nr90.fasta   # 1107 x 1371 列
```

**アライメント品質問題と対処：** MAFFT --auto（FFT-NS-2）は 1107 本の短鎖・高乖離配列を **1371 列（~92% gap）** に過剰展開。保存コアは占有率≥10% の **196 列**、≥20% で 136 列に集中（＝私的挿入ノイズに埋もれた真のコア）。design memo §2 が構造ガイドを要求する理由の実例。初回 ML（コンタミ除去効果とグロス樹形の確認）目的なので、Python で trimAl 相当のトリミングを実施：
- 列：占有率 ≥10%（trimAl gap-threshold 0.9 相当）→ 196 列保持
- 行：トリム後占有 <30% の行を除去 → 10 本除去 → **1097 seqs × 196 cols**
- 出力：`3-analysis/smlsm_curated_aln_nr90_trim.fasta`

```bash
iqtree3 -s 3-analysis/smlsm_curated_aln_nr90_trim.fasta \
        -m TEST -B 1000 -T AUTO --seqtype AA \
        --prefix 4-results/smlsm_tree_curated_nr90   # 無根 ML
```

選択モデル `Q.INSECT+G4`（BIC）。

**方針：** 有根化は後段の構造アンカー工程（古細菌 SmAP / 細菌 Hfq 相互外群、design memo §1）で実施。この初回 ML は無根で樹形の健全性（コンタミ除去でクレードが整理されたか）を確認する位置づけ。**次段階の "本番" アライメントは PROMALS3D/Expresso による構造ガイド MSA に置換予定**（trim 版は暫定）。

**IQ-TREE 完了（2026-07-04）：** Q.INSECT+G4、logL −81688、1090 taxa、7h45m。UFBoot 相関 0.982（目標0.99にわずか未達だが実用範囲）。強支持枝 519/1087（48%）。

**クレード評価（型配色）：** `scripts/analytics/build_biob_types.py`（記述＋生物名から型分類）→ `4-results/biob_tip_types.tsv`、`scripts/viz/plot_biob_types.R`（fan レイアウト）→ `4-results/smlsm_curated_types.{pdf,png}`。
- 型内訳：Lsm 499・Sm-core 335・Hfq 231・SmAP(古細菌) 27・**Other 5**。
- **①コンタミ除去の確証**：Other は5 tip のみ（旧 nr70 の15%汚染から激減）。誤配置の大ブロックなし。
- **②主要型の分離が明瞭**：**Hfq（細菌）が凝集した独立クラスタ**、Sm-core・Lsm は各々パラログ特異的クラスタを形成（各オーソログが単系統的）。
- **③古細菌 SmAP は真核 Sm/Lsm 領域に散在し Hfq とは離れる**＝「古細菌 Sm が真核 Lsm/Sm の祖先、Hfq は別系統」という相互外群設計（design memo §1）を支持。
- → curated データセットが健全と確認。構造ガイド MSA（"本番"）へ進める状態。

---

### 2026-07-04 — PF01423/PF17209 HMM 検索パイプライン構築（DPANN/Asgard 分布）

design memo §3 の実装。HMMER 3.4 導入。

**二重 HMM 設計（カバレッジ検証で確定）：** PF01423(LSM) 単独では Hfq を検出できない（bio-a Hfq 229本中 GA 通過1本のみ）。Hfq 型リングを持つ古細菌系統を「偽の欠如」と誤判定するリスク（Nielsen 2007＝§C-1）。→ **PF17209(Hfq) を併用**（Hfq 全数通過、Sm/Lsm も 404 交差検出）。両 HMM の和集合で Sm フォールド全体を捕捉し、best-HMM で **Sm/Lsm型 vs Hfq型を型判定**。取得済み：`3-analysis/hmm/PF01423.hmm`・`PF17209.hmm`。

| HMM | LENG / GA | vs Hfq(229) | vs Sm/Lsm(5133) |
|---|---|---|---|
| PF01423 (LSM) | 66 / 23.4 | 1 | 4691 |
| PF17209 (Hfq) | 64 / 27 | 229 | 404 |

**取得スクリプト：** `scripts/analytics/fetch_dpann_asgard_proteomes.py`
- DPANN 9系統＋Asgard 5系統（クラスを門より先に列挙し帰属の二重化を回避）を **NCBI Datasets v2 API** で取得。
- **completeness フィルタ（重要）：** DPANN/Asgard は大半が不完全 MAG。CheckM completeness≥50 & contamination≤10（MIMAG medium-quality 相当）で選別。cap なし（≥50 では各系統 数〜十数本しか残らず冗長・volume 問題が発生しないため）。GCA/GCF 重複は `paired_accession` で除去（RefSeq 優先）。
- **アノテーション交絡の除去：** protein.faa があればそれ、**無ければ genomic.fna を Prodigal（meta モード）で ab initio 予測**。→「真の欠如」がアノテーション欠如の artifact でないことを担保。
- 出力：`1-downloaded-data/proteomes/<acc>.faa`（ヘッダに `taxon|accession|` タグ）＋ `dpann_asgard_manifest.tsv`（taxon/species/accession/completeness/contamination/source/n_proteins）。

**completeness 閾値の検討経緯（実測ベース）：** 当初 cap=40 で走らせたが、cap は一度も binding せず、完全性閾値の方が支配的と判明。
- ≥80% では全14系統で通過が**合計18 genome**のみ。Woesearchaeota(1983)・Thorarchaeia(444) 等は**0**（主要系統が消え、欠如を論じられない）。
- ≥50% でも Woesearchaeota・Pacearchaeota・Thorarchaeia 等は**0 genome**＝「数千 genome」の正体はほぼ全て <50% の不完全 MAG。**評価可能な系統は限られる**という配列決定の現実。
- 結論：**存在（presence）は completeness 非依存で主張可、欠如（absence）だけが completeness を要求**。評価可能系統／データ不足系統を分けて報告する。

**パイロット（Nanohaloarchaeota, 8 genome）：** PF01423=6ヒット（6/8 が単一コピー LSM）、PF17209=0。うち1件は **Prodigal 予測ゲノムから回収**＝アノテーションでは見逃す本物を捕捉、手法の核心的価値を実証。

---

### 2026-07-04 — DPANN/Asgard 分布センサス（中規模本番）— 結果確定

**集計スクリプト：** `scripts/analytics/hmm_type_census.py`（両 HMM を全プロテオームに hmmsearch --cut_ga → best-domain スコアで型判定 → genome/種/系統の3粒度集計）。取得は completeness≥50 & contam≤10、cap なし、accession 重複除去（クラス→門の順で最具体タグを優先）。**50 genome（annotated 39・prodigal 11）取得**。

**系統別サマリ（`3-analysis/hmm/census_lineage.tsv`）：**

| taxon | n_genomes | n_species | Sm/Lsm保有 genome | Hfq保有 | 評価可否 |
|---|---|---|---|---|---|
| Nanoarchaeota | 16 | 4 | 14 | 0 | yes |
| Asgardarchaeota | 11 | 6 | 10 | 0 | yes |
| Lokiarchaeia | 8 | 4 | **8（全数）** | 0 | yes |
| Parvarchaeota | 7 | 2 | 4 | 0 | yes |
| Micrarchaeota | 4 | 4 | **4（全数）** | 0 | yes |
| Nanohaloarchaeota | 4 | 3 | **4（全数）** | 0 | yes |
| Woese/Pace/Aenigma/Diaphero/Altiarch/Thor/Heimdall/Odin | 0 | – | – | – | **no_data** |

**主要な発見：**
1. **全70ヒットが Sm/Lsm 型、Hfq 型ゼロ**。DPANN/Asgard は（Nielsen 2007 の Euryarchaeota *M. jannaschii* 型 Hfq とは異なり）Sm/Lsm 型フォールドを持つ。
2. ***Nanoarchaeum equitans*（DPANN 基準種）が Sm/Lsm を保持**（1ヒット）。我々の 06-22 BLAST 0ヒットは感度限界だった。**※ただし Willkomm/Reichelt 2018（Fig3）が既に *N. equitans*・一部 DPANN/Asgard の SmAP 保有を提示済み**＝「保持自体」は新発見でない。我々の貢献は completeness 制御の系統的センサス＋構造検証＋CPR 対照（過剰主張回避、2026-07-05 修正）。
3. **Lokiarchaeia（真核起源に直結）は全 8 genome・4 種が保有**。培養株 *Promethearchaeum syntrophicum*／*Ca. Lokiarchaeum ossiferum* を含む。→ 真核 Sm の起源議論に一次データを提供。
4. **種レベルでも presence は堅牢**（over-sequencing 中和後も評価可能系統でほぼ普遍）。唯一 *Ca. Flexarchaeum multiprotrusionis*（Asgard, 1 genome）が 0 ヒット＝欠如候補だが単一 genome で弱い。
5. **評価可能は6系統のみ**。Woesearchaeota 等8系統は completeness≥50 の genome が皆無＝配列決定の現実的限界。**presence は主張可・absence はデータ不足**として正直に報告する。

**成果物：** `hits_all.tsv`（全ヒット・型・スコア）、`census_genome/species/lineage.tsv`、`smfold_hits.faa`（ヒット配列＝§2 構造ガイド MSA・§1 有根ツリー投入用）。

**次段階：** smfold_hits.faa を §2 構造ガイド MSA に統合 → §1 有根ツリー。Payá&Bonete 2023 の 109古細菌コピー数マトリックス（Euryarchaeota baseline）と DPANN/Asgard 分布を比較。

---

### 2026-07-04 — 構造ガイド MSA（design memo §2）— "本番"アライメント準備

ツール選定：PROMALS3D(Web)／T-Coffee Expresso／FoldMason を比較し **FoldMason** を採用。判断基準＝(1) Sm/Lsm は近縁 PDB をほぼ持たず T-Coffee の「配列ごとテンプレ割当」の強みが効かない→構造シグナルは実質同じ19アンカー、(2) FoldMason は単一バイナリで完全ローカル・再現的（Bioconda 回避方針と合致）、(3) T-Coffee Expresso は外部サーバ依存で再現性リスク。

**ツール導入：** FoldMason（Steinegger lab、mmseqs.com の macOS universal バイナリ、`~/tools/foldmason` → `/opt/homebrew/bin/foldmason`。foldseek と同じ導入モデル）。

**手順（`scripts/analytics/build_structguided_msa.py` に集約）：**
1. **確定アンカー19 PDB** を RCSB から取得（`3-analysis/structures/*.pdb`）。
2. `foldmason easy-msa` で構造 MSA（全243鎖×224列）→ ユニーク鎖 → CD-HIT 0.95 で **構造 seed 25配列×219列**（3ドメイン網羅：真核 Sm パラログ[3PGW/1D3B]・古細菌 SmAP[1I8F/1I81/1TH7/1LJO/1M5Q/1M8V/1I5L]・細菌 Hfq[1HK9/1KQ1/1U1S/2QTX/3AHU]・Caulobacter[6GWK]）。
3. `mafft --seed structure_anchor_seed.fa` で curated nr90（1107）を構造ガイド整列 → `smlsm_curated_structguided.fasta`（1132×1480）。
4. 占有率トリム（列≥10%・行≥30%、seed 除外）→ `smlsm_structguided_trim.fasta`（**1101×184**）。構造 seed の≥50%充填列＝**76列**＝Sm fold ~70残基と一致＝構造座標に較正されたコア。

**位置づけ：** design memo §2 の実体。生配列 MAFFT の trim（1097×196）を置換する "本番" アライメント。次段は IQ-TREE3（+ MrBayes）を `smlsm_structguided_trim.fasta` で実行し、生配列版と樹形・深部支持を比較。

**IQ-TREE3 実行中（2026-07-04 起動、PID 64151）：** `-s smlsm_structguided_trim.fasta -m TEST -B 1000 -T AUTO`、prefix `4-results/smlsm_tree_structguided`。~7時間見込み。完了後の確認事項：
- 生配列版（Q.INSECT+G4、UFBoot 48%≥95）との**深部支持の比較**（構造ガイドで改善するか＝§2 の狙い）。
- 型配色（`plot_biob_types.R` を構造ガイド木に適用）で主要型クレードの分離が向上するか。

---

### 2026-07-04 — CPR/Patescibacteria 再検証（シナリオ転換の残タスク）— 決定的な対照結果

DPANN/Asgard と同じ completeness＋二重HMM＋Prodigal パイプラインを CPR に適用（`fetch ... --groups cpr --tag cpr` → `hmm_type_census.py --tag cpr`、出力 `census_*_cpr.tsv`）。

**結果：397 genome（Prodigal 379＋注釈18、計29万タンパク・平均731/genome）で Hfq 0・Sm/Lsm 0。**
| 系統 | genome | 種 | Sm/Lsm | Hfq |
|---|---|---|---|---|
| Saccharibacteria | 393 | 15 | 0 | 0 |
| Absconditabacteria | 3 | 3 | 0 | 0 |
| Patescibacteria(未分類) | 1 | 1 | 0 | 0 |
| 他（Parcubacteria/Microgenomates/Gracilibacteria/Dojkabacteria） | 0 | – | data不足 | – |

**「0」の妥当性（サニティチェック合格）：** (1) プロテオームは健全（リボソームタンパク注釈843件）、(2) 陽性対照＝同 HMM が DPANN/Asgard で 70 ヒット、(3) Prodigal で ab initio 予測済＝アノテーション交絡除去、(4) Saccharibacteria は培養株含む393 genome＝**どの DPANN 系統より高品質サンプリング**で欠如がより強固。→ 技術的でなく**生物学的な真の欠如**。

**物語上の意義（対照）：** **DPANN/Asgard（古細菌）＝Sm/Lsm 保持、CPR（細菌）＝Hfq/Sm 完全喪失。** 縮小ゲノム2放散が正反対に進化。CPR の喪失は「縮小ゲノム細菌で Hfq が失われがち（endosymbiont 既知）」と整合。**CPR の負例が「パイプラインは遺伝子が真に無ければ0を返す」ことを実証**＝DPANN/Asgard の保持が方法のバイアスでないことの内部対照にもなる。draft §3.5/3.6/Discussion に反映。

**文献（Claude Science CPR サーベイ、2026-07-04）：** CPR で Hfq/Sm を扱った論文は**ゼロ**（377レコード横断で co-mention 0）＝our 実測の完璧な補完（文献 gap＋実測欠如）。今回の Claude Science 出力は信頼性要件（[read]/[inferred]/[to verify] マーカー・DOI・推論と事実の区別）が効き前回より格段に良好。※成果物 `cpr_hfq_survey.md`/`cpr_hfq_references.csv`/`cpr_hfq_gap.png` は Claude Science 内生成のまま＝**0-literature/ へローカル保存推奨**（archaeal deepdive と同様）。

---

### 2026-07-04 — DPANN/Asgard ヒットの構造予測検証（査読対策①）

**目的：** HMM（配列プロファイル）で見つけた DPANN/Asgard の Sm/Lsm ヒットが**本物の Sm fold か**を、配列に依存しない構造で独立検証。査読の最大の攻撃点「HMM ヒット＝本物とは限らない」を先に潰す。design memo §3 の Foldseek 活用の実装。

**構造アライメント（済）とは別物**：§2 は実験構造で配列を並べた。ここは**実験構造の無いヒット配列の3D形を予測**して検証する。

**手順：**
1. `scripts/analytics/predict_smfold_hits.py`：`smfold_hits.faa` の 70件（Asgard 24・Loki 20・Nanoarch 14・Micrarch/Nanohalo/Parvarch 各4、長さ46–142）を **ESMFold（ESMAtlas API、ローカル不要）** で構造予測 → `3-analysis/predicted/*.pdb`、pLDDT 記録。動作確認：Nanoarchaeota ヒットが **mean pLDDT 0.8（高信頼）で Sm fold**。
2. `scripts/analytics/verify_smfold_foldseek.py`：予測構造を **foldseek** で確定アンカー（1I8F 等 Sm 系）と照合 → TM-score≥0.5 かつ Sm アンカー命中で「Sm fold 確認」。出力 `4-results/smfold_foldseek_verification.tsv`。

**状態：** ESMFold 予測 実行中（PID 64698、API が遅く ~30分超）。完了後に foldseek 照合。予測構造は gitignore（API 再生成可）、スクリプトとサマリのみ追跡。

**期待成果：** *Nanoarchaeum equitans*・Lokiarchaeia 等のヒットが構造でも Sm fold と確定すれば、目玉（DPANN/Asgard にも Sm/Lsm）が**配列（HMM）＋構造（ESMFold+foldseek）の二重証拠**になる。

**結果（2026-07-04、確定）：** ESMFold 予測 55/70 成功（**全て pLDDT≥0.7 の高信頼**、15件は API タイムアウト＝リトライ中）。foldseek 照合で **55/55 すべて Sm fold と確認**（`4-results/smfold_foldseek_verification.tsv`）:
- **TM-score min=0.92・median=0.97・max=1.00**（極めて高い構造一致）。
- 6系統すべて確認（Asgard 21・Loki 13・Nanoarch 9・Micrarch/Nanohalo/Parvarch 各4）。
- 最良アンカーの型：**古細菌 Sm 49／真核 Sm 4／細菌 Hfq 2**＝DPANN/Asgard ヒットは構造的に古細菌 Sm に最も近い（期待どおり）。
- → **査読の最大の攻撃点「HMM ヒット≠本物」を完全に無力化**。DPANN/Asgard の Sm/Lsm 保持が配列＋構造の二重証拠に。目玉が盤石化。

### 2026-07-05 — 投稿直前フェーズ：フレーミング確定・GBE パッケージ・Table 1

- **フレーミング最終確定（統合型）**：「系統樹＝frame、古細菌保持／CPR喪失の非対称＝finding」。構造ガイド IQ-TREE 完了（1101×184・Q.INSECT+G4・logL −81864.0368・UFBoot≥95=470/1092=43%）は素の版（519/1087=48%）より**深部解像を改善せず** → 系統樹を"足場"、census/構造検証の非対称を主張、が正当と実測で裏付け。
- **保持は既出・我々の貢献の再定義**：DPANN/Asgard の Sm/Lsm 保持自体は Willkomm/Reichelt 2018（Fig3）が既出。genuine な貢献は ① completeness 制御の系統的 MAG センサス ② 構造検証 ESMFold+foldseek（55/55、TM 中央値 0.967≈0.97、49/55 古細菌アンカー最良）③ **CPR 対照** ④ Prodigal 交絡除去。「DPANN で発見」と過剰主張しない。
- **CPR 再検証＝決定的対照（確定）**：同 HMM+completeness で **0/397（393 Saccharibacteria 等、Sm/Lsm・Hfq とも 0）**。陽性対照 OK（古細菌側 70 ヒット、CPR 側 290,425 タンパク・843 リボソームタンパク注釈あり＝検出系は機能）。completeness は CPR の方が高い(82.0 vs 古細菌 75.6%)→「低品質だから」の反論封じ。
- **Hfq 喪失一次文献**：Sun, Zhulin & Wartell 2002（NAR 30:3662）を Discussion に追加。
- **Table 1 レンダリング**：`census_lineage{,_cpr}.tsv` から lineage 別カウント＋completeness の実表を draft に埋込（display items 2→3）。Fig.1 の in-plot タイトルを "Structure-guided ... framework tree" に修正・CMYK TIFF 再変換。
- **GBE 投稿パッケージ**（`Biology/_gbe_submission/`）：submission.md・参考文献リスト（DOI 全検証・GBE 著者年式）・CMYK 300dpi TIFF・compliance（全上限クリア：abstract 223w/title 114字/本文 2440w/refs 9）。Significance statement・Data Availability 追加済。参考文献は `REFS_zotero_doi.txt`（21件、全 DOI 検証）で Zotero 一括投入可能。
- **残る手作業**：repo public化 or Zenodo DOI／Zotero 整形／FoldMason 引用の出版版差替。

---

## 配列リスト

| Accession | Organism | タンパク質 | 備考 |
|-----------|----------|-----------|------|
| | | | |

---

## 未解決の問い

- [x] DPANN・CPR の BLAST 結果を最終確認 → 全クエリ・全ターゲットで 0 ヒット（後に HMM で感度限界と判明）
- [x] DPANN/CPR がヒットゼロの場合、文献でも裏付けがあるか → Saito et al. (2019) で *N. equitans* の Clp1 欠落として傍証あり
- [ ] 真核生物 Sm タンパク質（U1-A 等）を外群として使うか内群として扱うか
- [ ] bio-a との解析パイプラインをどこまで共通化するか
- [ ] 論文の主張を「Veretnik update」から「縮小ゲノム生物における Sm/Lsm 分布」にシフトするか検討
- [x] Veretnik データセットで CD-HIT → MAFFT → IQ-TREE3 パイプラインを実行する（完了、Q.PFAM+G4、700 iterations）
- [x] 本番データセット取得（6,103配列、fetch_smlsm.py）→ コンタミ判明 → curated 5,665 に修復
- [x] curated 再解析（1097×196、Q.INSECT+G4、無根 ML）
- [x] DPANN/Asgard HMM 分布センサス（completeness≥50、二重 HMM、型判定）
- [ ] 構造ガイドアライメント（PROMALS3D/Expresso）で "本番" MSA に置換
- [ ] 有根化（古細菌 SmAP / 細菌 Hfq 相互外群）
- [ ] HMM ヒット配列を §2 構造ガイド MSA 経由で §1 有根ツリーへ投入

---

## 環境・方針メモ（bio-a/bio-b 共通）

### ツール構成
- Python: venv-bio（`~/Workspace/Research/shared/venv-bio/`）、uv 管理
  - 主要パッケージ: requests / dendropy（系統樹比較）
- R: 4.6.0、**可視化専用**（ggtree による論文品質の系統樹作図のみ）
  - パッケージ: ggtree / ggplot2 / treeio
  - 分析スクリプトは Python → `scripts/analytics/`、R は `scripts/viz/` に配置
- MAFFT、CD-HIT、IQ-TREE3 v3.1.3（ARM マルチスレッド）、MrBayes（ソースビルド）、Jalview
- **HMMER 3.4**（`hmmsearch`、2026-07-04 導入）、**Prodigal V2.6.3**（MAG 遺伝子予測、2026-07-04 導入）
- FigTree v1.4.4（Java 26 + ラッパースクリプト `/opt/homebrew/bin/figtree`）
- Foldseek（構造類似性検索、`/opt/homebrew/bin/foldseek`）
- PyMOL Incentive 版（構造可視化、ライセンス登録済み）
- NCBI API Key: `~/.zshenv` に設定済み

### ディレクトリ方針
- Kryukov 方式に移行済み（2026-06-22）
- 移行スクリプト: `~/Workspace/Research/Biology/migrate_to_kryukov.sh`

### 外群設定方針
- bio-a（Hfq）の外群 → bio-b の解析対象（Sm/Lsm）
- bio-b（Sm/Lsm）の外群 → bio-a の解析対象（細菌 Hfq）
- 両プロジェクトは互いの外群になる

### 系統推定方針
- 最尤法：IQ-TREE3（UFBoot 1000回）
- ベイズ法：MrBayes（IQ-TREE3 完了後に並行実行）
- モデル選択：IQ-TREE3 の `-m TEST`（BIC 基準）で自動選択

### 論文方針（bio-b）
- 先行研究：Veretnik et al. (2009, PLoS Comput Biol)、PhyML による最尤法
- 方法論的改善：IQ-TREE3 + MrBayes、新モデル、最新データ、構造ガイド MSA、HMM 分布センサス
- **⚡シナリオ転換（2026-07-04）：当初の顔は「DPANN/CPR での Sm/Lsm 欠落の実証」だった（BLAST 0ヒット）。だが completeness フィルタ＋二重HMM＋Prodigal で再探索したところ DPANN/Asgard は Sm/Lsm を保持していた（*N. equitans* 含む・Lokiarchaeia 全数、ESMFold+foldseek で 55/55 が Sm fold と構造検証済）。旧「欠落」は BLAST の感度限界。→ 顔を「欠落の実証」から「予想外の保持＝祖先型 Lsm・真核 Sm 起源への一次データ」へ転換。**
- **新規性の核心（最終確定 2026-07-05、統合フレーミング）**：系統樹＝frame、「古細菌は Sm フォールド保持／縮小ゲノム細菌 CPR は喪失」の非対称＝finding。保持自体は Willkomm 2018 が既出→我々の貢献は (1) completeness 制御の系統的 MAG センサス (2) 構造検証 ESMFold+foldseek（55/55）(3) **CPR 対照＝0/397 で喪失を実証（再検証完了・陽性対照 real）** (4) Prodigal 交絡除去。eukaryogenesis 含意（Lokiarchaeia）は有効。「DPANN で発見」とは主張しない。

## 参考文献メモ

### Veretnik et al. (2009) PLoS Comput Biol
- 80種335配列（細菌Hfq・古細菌SmAP・真核Sm/Lsm）
- PhyML（最尤法）で系統推定
- 限界：DPANN・CPR なし、AlphaFold2 なし、旧ツール

### Saito et al. (2019) Genome Biol Evol
- Clp1 ファミリー（RNA キナーゼ）の3ドメイン大規模解析
- *Nanoarchaeum equitans*（DPANN）で Clp1 ファミリーが0件と記録
- bio-b の「DPANN は RNA 処理因子を欠く」という主張の傍証として使える
