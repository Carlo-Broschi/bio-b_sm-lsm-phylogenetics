# bio-b 設計メモ：文献知見の統合（rooting・構造アンカー・DPANN HMM）

**作成：2026-07-04**
**根拠：** 精読5本（Reichelt/Grohmann 2023, Kambach 1999, Santiago-Frangos 2019, Kim/Tevenvirinae 2025, Zhang 2025）＋ Claude Science archaeal deep-dive（Payá & Bonete 2023 ほか構造アンカー系譜）

このメモは「読んだ文献をどう bio-b の設計判断に落とすか」だけを書く。文献の要約自体は各ノート/memory を参照。

---

## 0. 一枚要約：進化の骨格（設計の前提）

文献群が一致して支持する方向性：

```
細菌 Hfq(ヘキサマー)  ←機能アナログ・別系統→  古細菌 SmAP(ヘプタ/ヘキサマー)
   [bio-a]                                        │ 祖先的 Lsm 様
                                                   ▼
                              真核 Lsm型リング(祖先状態) ──→ 真核 Sm型リング(派生状態)
                                                              [Zhang 2025 が実験的に確定]
```

- **Lsm型=祖先、Sm型=派生**は Zhang 2025 が実験（リング相互変換）で確定 → これが rooting の最重要根拠。
- 古細菌 SmAP は真核 Lsm に近い（Reichelt 2023：PfuSmAP1 は真核型 RNA homeostasis network に入り、細菌 Hfq の sRNA matchmaker とは役割が違う）。
- 細菌 Hfq は同じ Sm フォールドの**機能アナログだが独立系統** → bio-a↔bio-b の相互外群設計の生化学的裏付け。

---

## 1. Rooting（有根化）の設計

### 採用する根拠の階層
> ⚠️ **2026-07-04 訂正**：本節の Zhang 由来記述は当初セッション要約に依拠しており、原著（Mu et al. 2025, NAR gkaf451）の一次精読で誤りを修正した。以下は精読後の正しい記述。

1. **主根拠（実験）**: Mu et al. 2025（"Zhang 2025"）の4段階モデル（Fig 6）。真核内部では Lsm2-8(祖先, Ring1) → Sm core(派生, Ring2)。変換スイッチは **SC1-SC3 接触（= Interface C = SmB-SmD1 ⇔ Lsm8-Lsm2）の親和性**。Sm→Lsm は「Step I: SC1-SC3 強化」、Lsm→Sm は「Step I: SC1-SC3 弱化 + Step II: RNA結合残基の最適化」。
   - 親和性順位（PISA計算値）：Sm core **I-A(−9.4) > I-B(−6.8) > I-C(−2.9)**／Lsm2-8 **I-C(−9.4) > I-A(−5.9) > I-B(−3.9)**。※ I-C の逆転が要。
2. **ドメイン間の根**: 古細菌 SmAP を真核 Sm/Lsm の外群に、細菌 Hfq を全体の最外群に置く（相互外群）。Reichelt 2023 が「archaeal SmAP ≈ 祖先 Lsm 型」を機能面から支持。
3. **残基レベルの検証軸（molecular character、ただし格に注意）**: Mu et al. 2025 が挙げた残基。
   - **【検証済み】Lsm→Sm 変換に効いた RNA 結合残基変異**：**F46Y/N75K（Lsm5, loop3/5）・L43F（Lsm7, loop3）＋ loop2 置換**（Lsm3/5/6 を SmD2/E/F 型に）。これらは実験で変換を達成した実残基 → 系統形質として使える。
   - **【未検証・構造推論】Interface C の側鎖**：Lsm 側 **Val69(Lsm8 β5)/Phe61(Lsm2 β4)** ↔ Sm 側 **Ser79(SmB β5)/Ser59(SmD1 β4)**。**原著が "await experimental confirmation" と明記**（Supplementary Fig S3 からの推論）。系統形質に使う場合は「未検証の構造推論」と明示必須。断定的な synapomorphy 扱いは不可。
   - 残基番号はすべて**ヒト (L)Sm タンパク質**の座標。bio-b への写像には各ヒト参照配列のアライメントが必要（§Q3運用）。

### 既知のリスクと対策
- **Veretnik 2009 Comment #3**：古細菌 SmAP を外群にすると木が崩れた。短鎖・高乖離が原因 → **§2 の構造アンカーで緩和**してから rooting する。
- bio-a 側で観測した ASDSF プラトー（短鎖ゆえの深部枝の解像不能）は bio-b でも起こりうる前提で設計する。
- **【一次精読で判明・重要】「細菌=Hfq／古細菌=Sm」は綺麗に割れない**（Nielsen 2007, *M. jannaschii*）。ある古細菌は Sm型でなく **Hfq型（ヘキサマー）** を持ち *E. coli* Hfq と機能互換。→ 単純な相互外群前提は危険。**rooting 前に、古細菌側に Hfq様が混在しないか（PF01423/構造で）確認**し、Hfq clade と Sm clade の帰属を taxon ごとに検証する。これは §3 の HMM 検索とも連動（古細菌ゲノムで Hfq型/Sm型どちらを持つかを判定）。

### 具体的手順
1. §2 の構造ガイドアライメントを入力にする。
2. IQ-TREE3 で unrooted ML → 古細菌 SmAP / 細菌 Hfq を outgroup 指定して有根化。
3. Zhang の残基極性（Val/Phe vs Ser/Ser、Loop2/3/5）を末端形質としてマップし、Lsm→Sm 極性と樹形が一致するか確認。矛盾すれば long-branch/rogue を疑う（bio-a と同じ RogueNaRok 手順）。

---

## 2. 構造アンカー較正アライメント

### なぜ必要か
Hfq/Sm/Lsm は**短鎖かつ配列乖離が大きい**。生配列 MSA は深部ノードで信頼できない（＝ bio-a の収束難・Veretnik Comment #3 の崩壊と同根の問題）。Kambach 1999 は Sm1/Sm2 モチーフの Cα が **<0.9 Å で重畳**することを示した＝**配列では見えない相同性が構造では保存**。よって構造で整列を拘束する。

### 使う構造アンカー（PDB ID を一次精読で確定、2026-07-04）

**【確定＝アンカー論文の一次精読で照合済み】** 3ドメイン・apo/RNA複合体・ヘプタ/ヘキサを網羅。詳細・確認手段は [`0-literature/structural_anchors.md`](0-literature/structural_anchors.md) を参照（本表はその抜粋）：

| ドメイン | 構造 | PDB | 生物 / 状態 | 出典・確認 |
|---|---|---|---|---|
| 真核 | Sm core D3B / D1D2 | **1D3B / 1B34** | ヒト / ヘテロ二量体（Sm fold 基準） | Kambach 1999（一次精読） |
| 真核 | U1 snRNP の Sm core | **3PGW** | ヒト / 7量体+snRNA、4.4 Å | Weber/Wahl 2010（本文で 4.4Å・7Sm 蛋白は一次確認、ID は PDBe 据置） |
| 古細菌 | SmAP1 ヘプタマー | **1I8F** | *P. aerophilum* / 7量体, 1.75 Å | Mura/Eisenberg 2001（一次精読・脚注） |
| 古細菌 | Sm2 **ヘキサマー** | **1LJO** | *A. fulgidus* / 6量体, 1.95 Å | Törő/Suck 2002（Thore/Sauter 重畳表で相互確認） |
| 古細菌 | AF-Sm1 **7量体**（±U5 RNA） | **1I5L（apo）/ 1I4K（+RNA）** | *A. fulgidus* / 7量体 | Törő 2001（本体未入手、Thore/Sauter 表で確定） |
| 古細菌 | **PA-Sm1 ± U7 RNA** | **1H64（apo）/ 1M8V（+RNA）** | *P. abyssi* / 7量体（ウリジンポケット His37/Asn39/Arg63） | Thore/Suck 2003（一次精読・脚注）← **RNA接触残基の要** |
| 古細菌 | Lsmα ヘプタマー | **1I81** | *M. thermoautotrophicum* / 7量体, 2.0 Å | Collins 2001（Thore/Sauter 表で相互確認） |
| 細菌 | Hfq ヘキサマー | **1HK9** | *E. coli* / 6量体, 2.15 Å | Sauter 2003（一次精読・構造決定節末尾） |
| 細菌 | Hfq + CTD 自己阻害 | **6GWK** | *C. crescentus* / 6量体, 2.15 Å | Santiago-Frangos 2019（一次精読） |

**構造から読める整列アンカー（一次確認）**：
- Sm1(β1-3)/Sm2(β4-5) モチーフが Cα <0.9 Å で重畳（Kambach）。**ここを整列固定点**に。
- ウリジン結合ポケット＝リング内側の**保存3残基**＋ N末αヘリックス＋β2 の保存芳香族残基（Thore 1M8V）。→ RNA接触ループ（L3/L5）を第二アンカーに。
- Mura 1I8F：ヘプタマー＋陽イオン性中央孔。3PGW：各サブユニットが Sm1/Sm2 で snRNA 1ヌクレオチドを認識。

**【未確認＝ID 要確定】**（§2 実装時に RCSB で確定）：Törő 2002 AF-Sm1 ヘプタマー（AF-Sm2=1LJO は確定）／Mura 2003 augmented SmAP3 14-mer（*Pyrobaculum*, PNAS 100:4539）／Nielsen 2007 *M. jannaschii* Hfq様（PMC2080587）／Collins 2001 *Methanobacterium*（1I5L or 1IS1）／crenarchaeal SmAP1/2（Bläsi 2015 は機能論文、新規PDB無しの可能性）。

### 方法
- PROMALS3D / T-Coffee Expresso / mTM-align 等で上記 PDB をテンプレートに構造ガイド MSA を作る。
- Foldseek は「遠縁ホモログの探索＋引用可能な構造相同性の定量」に使う（DPANN 反論対策にも流用、§3）。
- 較正の要点：Sm1(β1-3)/Sm2(β4-5) モチーフをアンカー、可変な N末 helix・Loop L4 は緩く。

---

## 3. PF01423 HMM 検索（DPANN/Asgard 分布）

### 位置づけ
deep-dive の opening #1。**文献上 DPANN/Asgard の Sm/Lsm を扱った論文はゼロ**（陰性証拠）。bio-b は既に BLAST で DPANN 0ヒットを確認済みだが、BLAST は感度が低い。

### なぜ HMM か（査読対策の核心）
- **BLAST 0ヒット**では「本当に無い」のか「配列が乖離して当たらない」のか区別できない。
- **Pfam の hmmsearch は高感度** → 「遺伝子の真の欠如」と「アノテーション/配列乖離の欠如」を切り分けられる。
- これは査読者の想定反論「短鎖で乖離しているだけでは？」への**決定的な備え**。どちらの結果でも publishable：
  - ヒットあり → 新規分布データ、ツリーに追加
  - 真に欠如 → 「縮小ゲノムでの喪失」主張を BLAST 以上に強化

### 【2026-07-04 実証】二重 HMM 設計（カバレッジ検証で確定）
HMMER 3.4 導入、PF01423 と PF17209 を InterPro から取得し、既知配列でカバレッジを検証した結果、**PF01423 単独では不十分**と判明：

| HMM | DESC / LENG / GA | vs Hfq (bio-a, n=229) | vs Sm/Lsm (curated, n=5133) |
|---|---|---|---|
| **PF01423** (LSM) | LSM domain / 66 / 23.4 | **1（❌ ほぼ欠測）** | 4691（✅ 91%） |
| **PF17209** (Hfq) | Hfq protein / 64 / 27 | **229（✅ 全数）** | 404（交差検出） |

- **含意①（偽陰性回避）**：PF01423 だけで DPANN/Asgard を探索すると、**Hfq型リングを持つ系統を「偽の欠如」と誤判定**する（Nielsen 2007＝§C-1 の *M. jannaschii* Hfq型リスクが現実の検出漏れとして顕在化）。「真の欠如」を厳密主張する本研究では致命的。→ **両 HMM の和集合で探索**する。
- **含意②（型判定という副産物）**：各ヒットを **PF01423 vs PF17209 のどちらで高スコアか**で分類 → genome ごとに「Sm/Lsm型 or Hfq型」を型付けできる。§1 の「古細菌に Hfq様が混在しないか」の検証軸に直結。当初の懸念が新しい形質軸に転化。
- 取得済み：`3-analysis/hmm/PF01423.hmm`（PF01423.29）、`3-analysis/hmm/PF17209.hmm`（PF17209.10）。判定は `--cut_ga`（信頼カットオフ）を基準に、境界域は E値と併記。

### 手順
1. RefSeq から DPANN 代表（Nanoarchaeota・Woesearchaeota・Pacearchaeota・ARMAN 等）＋ Asgard ゲノムのプロテオームを取得。
2. `hmmsearch --cut_ga`（**PF01423 と PF17209 の両方**）でスキャン → 和集合をヒット、best-HMM で Sm/Lsm型 vs Hfq型に分類、コピー数・ドメイン構造を集計。
3. **陽性対照ベンチマーク**：Payá & Bonete 2023 の既知 Euryarchaeota（1-3 Lsm パラログ）で先にパイプラインを回し、既知コピー数を再現できることを確認してから DPANN/Asgard へ適用。
4. **Payá & Bonete 2023 の 109古細菌コピー数マトリックス**（Euryarchaeota baseline、シンテニー Lrp/AsnC・MarR・L37e）と比較。
5. ヒット配列は §2 の構造ガイドアライメントに追加 → §1 の有根ツリーへ。
6. 補助軸：Kim et al. 2025（Tevenvirinae）の GoF/MotB.1/Frd.2 → フォールドがファージゲノムまで及ぶ＝分布/水平伝播の別軸。**ただし精読で判明した強い制約**：(i) 配列相同性がなく BLAST では検出不可（PSI-BLAST 5ラウンドでようやく 210 配列、AlphaFold3 で初めてフォールド同定）、(ii) **リング/オリゴマー形成は未実証**（AlphaFold の homomultimer モデルが ipTM<0.4 で失敗）。→ これらは**配列 ML ツリーには入れられない**（整列不能）。**構造フォールドレベルの相同として、Foldseek/構造ツリーで別扱い**が妥当。系統本体の taxon にはしない。

### 【2026-07-04 実行済】中規模センサス結果（completeness フィルタ版）
`fetch_dpann_asgard_proteomes.py`（Datasets v2 + CheckM completeness≥50 & contam≤10 + Prodigal フォールバック + accession 重複除去）→ `hmm_type_census.py`。**50 genome 取得、70 ヒット全て Sm/Lsm 型・Hfq 型ゼロ**。

- **評価可能6系統**：Nanoarchaeota(16g/14 保有)・Asgardarchaeota(11g/10)・Lokiarchaeia(8g/**全数**)・Parvarchaeota(7g/4)・Micrarchaeota(4g/**全数**)・Nanohaloarchaeota(4g/**全数**)。
- **データ不足8系統**：Woese/Pace/Aenigma/Diaphero/Altiarch/Thor/Heimdall/Odin は completeness≥50 の genome ゼロ。
- **重要**：*Nanoarchaeum equitans*（DPANN 基準種）が Sm/Lsm 保持 → **初期 BLAST 0ヒット（感度限界）を覆す**。Lokiarchaeia 全数保有（培養株 *Promethearchaeum* 含む）→ 真核 Sm 起源に一次データ。
- **閾値の教訓**：≥80% では18 genome・主要系統消失。≥50% で6系統確保。**presence は completeness 非依存で主張可、absence だけが要 completeness**。→ 論文では「評価可能系統の presence」を主軸に、absence は「データ不足」と明記して過剰主張を避ける。
- 実データ詳細は bio-b `notes.md`（2026-07-04 センサスエントリ）と `3-analysis/hmm/census_*.tsv`。

**手順3の陽性対照ベンチ（Payá&Bonete Euryarchaeota 再現）と手順4の 109古細菌比較は未実施**（次段階）。

### 【2026-07-04 実行中】HMM ヒットの構造予測検証（査読対策）
HMM は配列プロファイルなので「ヒット＝本物の Sm fold」を保証しない。→ ヒット70件を **ESMFold（ESMAtlas API）で構造予測 → foldseek で確定アンカーと照合**（`predict_smfold_hits.py`／`verify_smfold_foldseek.py`）。TM-score≥0.5 & Sm アンカー命中で fold 確認。*N. equitans*・Lokiarchaeia 等が構造でも Sm fold と出れば、**配列（HMM）＋構造（ESMFold+foldseek）の二重証拠**で目玉を盤石化。動作確認：Nanoarchaeota ヒット mean pLDDT 0.8。この Foldseek 活用は §3 冒頭で想定していた「DPANN 反論対策」の実装。

---

## 4. bio-a への波及（一次精読済み 2026-07-04）

**Santiago-Frangos et al. 2019（PNAS、PDB 6GWK、2.15 Å）** ※要約の記述を一次確認 → 正確だった。
- 機構：*C. crescentus* Hfq の **CTD 酸性チップ −DADD（残基78-82）** が近位面の**正電荷 rim（R18/K19/K21）**に結合し、RNA と競合して非特異的 annealing を自己阻害。具体接触：Asp81/82→Lys19/Arg18、Asp79→隣接プロトマーの Arg49、Glu75→Arg49/Ser39。
- **Cc CTD は短い（15 aa、tip −DADD）**、*E. coli* は長い（38 aa、tip −DSEETE）。短い方が**局所濃度が高く自己阻害が強い**。
- CTD は **sRNA 結合の選択性を上げる**。in vivo：Cc Hfq は Ec の RybB/ompF・DsrA/hns 制御を相補できるが、**RydC/cfa は相補不可**（Cc Hfq の RydC 結合が弱い）。
- **bio-a への含意（原著 Discussion が明言）**：「**Hfq CTD は新規 sRNA の獲得に合わせて急速に多様化しうる**」。CTD は core より速く（非保存置換＋indel）進化し、rim との相互作用は静電支配で配列非依存＝modular。
- **設計上の運用注意（私の判断）**：CTD は**速進化・indel 多で core アライメントに入れられない**（bio-a が既に 50-150 aa で長さフィルタしているのと同根）。よって「phylogenetic signal」として使うなら、**CTD をアライメントに入れるのではなく、CTD長・酸性チップ motif型（−DADD / −DSEETE 等）を離散/連続形質として core ベースのツリーにマップ**（祖先状態推定）する形が正しい。

**Reichelt 2023** の「Hfq は転写に関与、SmAP は RNAP 活性に非影響」は bio-a/bio-b の機能分離の根拠。

---

## 5. 未処理・要確認（正直な棚卸し）

- Claude Science 成果物 `archaeal_sm_lsm_deepdive.md` / `archaeal_sm_lsm_papers.csv` / `archaeal_sm_coverage.png` は**ローカル未保存**（Claude Science 内生成のまま）。回収推奨。
- 構造アンカーの**主要12論文は一次精読で PDB ID 確定済み**（Kambach/Weber-Wahl/Mura2001/Törő2001-2002/Thore/Mura2003/Kilic/Sauter/Santiago-Frangos/Collins/Nielsen/Someya、[structural_anchors.md](0-literature/structural_anchors.md)）。Thore 2003 と Sauter 2003 の重畳表がアンカー群を独立にクロスチェック（取り違えリスク消滅）。**残り未精読**：Nikulin 2020/2021（PDF入手待ち）、Mura 2003b（Protein Sci、構造価値低）、Weichenrieder 2014 レビュー。
- PF01423 が Sm フォールド全体を十分カバーするか（Hfq/Lsm も拾うか）は hmmsearch 前に Pfam の HMM 定義を確認。
- **Zhang(Mu et al. 2025) は 2026-07-04 に一次精読済み**。残基→アライメント写像は前提(a)Zhang=クリア、前提(b)キュレート版アライメント=未（bio-a CPU 待ち）。アライメント完成後に：検証済み残基（F46Y/N75K・L43F・loop2）を優先、未検証の Interface-C 側鎖（Val69/Phe61 vs Ser79/Ser59）は「構造推論」注記付きで写像。残基番号はヒト座標。
- **要修正の痕跡**：当初の Zhang 記述には要約由来の誤り（Lsm2-8 親和性順位の A/B 逆転、Lsm8-Lsm4→Lsm8-Lsm2、未検証残基の断定扱い）があり §1 で訂正済み。memory/notes への波及なしを確認済み。

### 精読検証ステータス（2026-07-04）
5本すべて**私が一次精読済み**：
- **Zhang (Mu et al. 2025)** — 要約に誤り3件 → 訂正済み（§1）。
- **Reichelt/Grohmann 2023**、**Kambach 1999** — 一次精読、memory 記録済み。
- **Santiago-Frangos 2019**、**Kim et al. 2025** — 本日一次精読。**要約は正確だった**（Zhang と異なり誤りなし）。§4/§3 に一次確認済み詳細を反映。
- 構造アンカーの **PDB ID は主要12論文を一次精読して確定**（1D3B/1B34/3PGW/1I8F/1I5L/1I4K/1LJO/1H64/1M8V/1M5Q/1TH7/1HK9/6GWK/1I81/2QTX/3AHU/3HSB）。3ドメイン・apo/RNA・ヘプタ/ヘキサを網羅。→ §2 の構造ガイドアライメントは PDB 座標を RCSB から回収すれば実装可能。
- Thore 2003（1H64 apo を新規追加）・Sauter 2003 の重畳表で相互確認済み。**3PGW のみ ID が末尾脚注依存で PDBe 据置**、Törő 2001 本体（1I5L/1I4K）は権限で未入手だが他2論文の表で確定。
- 残 PDF：Nikulin 2020/2021（B6/B7、ResearchGate 復帰待ち）、Mura 2003b（B5、優先度低）。
