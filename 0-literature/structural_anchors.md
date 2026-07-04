# 構造アンカー論文 ↔ PDB ID 対応表

**作成 2026-07-04／一次精読で確定・訂正。** bio-b §2「構造アンカー較正アライメント」用。

## A. 確定（PDB ID を一次精読 or RCSB/PDBe で確認済み）

| # | 論文 | DOI | PDB | 生物 / 状態 | 確認手段 |
|---|---|---|---|---|---|
| A1 | Kambach et al. 1999 (Cell) | 10.1016/s0092-8674(00)80550-4 | **1D3B / 1B34** | ヒト Sm D3B / D1D2（Sm fold 基準） | 本文精読 |
| A2 | Weber & Wahl 2010 (EMBO J) | 10.1038/emboj.2010.295 | **3PGW** | ヒト U1 snRNP + snRNA, 4.4 Å | PDBe（本文精読で 4.4 Å・7 Sm 蛋白は一次確認、ID は末尾脚注のため PDBe 据置） |
| A3 | Mura & Eisenberg 2001 (PNAS) | 10.1073/pnas.091102298 | **1I8F** | *P. aerophilum* SmAP1 7量体, 1.75 Å | **本文精読（脚注 "PDB ID code 1I8F"）** |
| A4 | **Törő et al. 2001 (EMBO J)** | 10.1093/emboj/20.9.2293 | **1I5L**（apo）/ **1I4K**（+U5 RNA） | *A. fulgidus* AF-Sm1 7量体（径65Å・厚30Å・中央孔13Å）| **✅原著精読済（2026-07-05、PDF入手）** |
| A5 | Törő & Suck 2002 (JMB) | 10.1016/s0022-2836(02)00406-0 | **1LJO**（AF-Sm2, 6量体） | *A. fulgidus* Sm2 ヘキサマー, 1.95 Å | RCSB。AF-Sm1 7量体は B4 |
| A6 | Thore & Suck 2003 (JBC) | 10.1074/jbc.m207685200 | **1H64**（apo）/ **1M8V**（+U7 RNA） | *P. abyssi* PA-Sm1 7量体（±ウリジン） | **本文精読（脚注 "1H64 and 1M8V"）。1H64=apo は新規追加** |
| A7 | **Mura & Eisenberg 2003 (PNAS)** | 10.1073/pnas.0538042100 | **1M5Q** | *P. aerophilum* **SmAP3 14量体**（Sm+CTD, Cd²⁺依存） | **本文精読** |
| A8 | **Kilic & Suck 2005 (Proteins)** | 10.1002/prot.20637 | **1TH7** | *S. solfataricus* SS-Sm1 7量体, 1.68 Å | **本文精読** |
| A9 | Sauter (Basquin) 2003 (NAR) | 10.1093/nar/gkg480 | **1HK9** | *E. coli* Hfq 6量体, 2.15 Å（結晶形A=全長/B=short） | **本文精読（構造決定節末尾 "...Protein Data Bank (1HK9)"）** |
| A10 | Santiago-Frangos 2019 (PNAS) | 10.1073/pnas.1814428116 | **6GWK** | *C. crescentus* Hfq 6量体, 2.15 Å | 本文精読 |
| A11 | **Collins & Mabbutt 2001 (JMB)** | 10.1006/jmbi.2001.4693 | **1I81** | *M. thermoautotrophicum* Lsmα 7量体, 2.0 Å | **孫引き→RCSB照合**（旧B1） |
| A12 | **Nielsen & Valentin-Hansen 2007 (RNA)** | 10.1261/rna.689007 | **2QTX** | *M. jannaschii* **Hfq様6量体**, 2.5 Å | **本文精読（Table1/p.2221）**（旧B2） |
| A13 | **Someya et al. 2011 (NAR)** | 10.1093/nar/gkr892 | **3AHU / 3HSB** | *B. subtilis* Hfq(YmaH) + AGr RNA, 2.2 Å | **本文精読＋RCSB**（旧B3） |

**細菌 Hfq 追加アンカー**（Someya Fig6C 凡例より、参照構造として確定）：*S. aureus* Hfq **1KQ1**／SaHfq-AU₅G **1KQ2**／*E. coli* Hfq-poly(A) **3GIB**／*P. aeruginosa* Hfq **1U1S**。

**RNA接触残基（一次確認、アライメントの機能アンカー）**：
- 古細菌 Sm ウリジンポケット＝**His37・Asn39・Arg63**（loop L3/L5、AF-Sm1番号）。Asn39 が O4/N3 と水素結合、His37 と Arg63 で uracil をサンドイッチ、隣接サブユニットの Met38（Törő 2001, 1I4K）。
- Sm1(β1-3)/Sm2(β4-5) が Cα rmsd ~0.6-1.1 Å で古細菌↔ヒト重畳（Törő/Kilic）→ **整列固定点**。
- 細菌 Hfq：proximal 面 Y55/K56/H57（AU₅G）、distal 面 Y25/I30（poly(A)）、BsHfq は R32 が distal で AG 認識（Someya 2011）。

## B. 未確定（残り。§2 実装時に確定）

| # | 論文 | DOI | 生物 / 内容 | 状態 |
|---|---|---|---|---|
| B4 | Törő & Suck 2002 の **AF-Sm1 7量体** | 10.1016/s0022-2836(02)00406-0 | *A. fulgidus* Sm1（A5=AF-Sm2 1LJO と同論文の別鎖） | ID 未確定（AF-Sm1 apo 7量体） |
| B5 | Mura & Eisenberg 2003b (Protein Sci) | 10.1110/ps.0224703 | SmAP オリゴマー化・リガンド結合（溶液生物物理） | **未読**（構造アンカー価値低） |
| ~~B6~~ | Nikulin 2020 (Biochimie 175:1) | 10.1016/j.biochi.2020.05.001 | Sac SmAP2 vs Mva SmAP1 の U結合様式比較 | **✅確定（本文精読 2026-07-04）：5MKI（*M. vannielii* SmAP1 apo, 2.05Å, 2ヘプタマー）／5MKL（*S. acidocaldarius* SmAP2 apo, 2.09Å, P1, 4ヘプタマー）／5MKN（*M. vannielii* SmAP1・**UMP複合体**, 2.55Å, 7 UMP/中央孔）** ※MR model：MvaSmAP1←1I4K、SacSmAP2←4XQ3 |
| ~~B7~~ | Nikulin 2021 (Biochem Moscow 86:833) | 10.1134/s000629792107004x | *H. salinarum* Lsm（L4 loop 効果） | **✅確定（本文精読）：6TFL（*H. salinarum* HsaSmAP60・**UMP複合体**, 2.40Å, P4₁2₁2, 14 UMP）** ※MR model←1LJO（AF-Sm2） |

**上記5構造は §2 のアンカー拡張候補**（Sac/Mva/Hsa ＝現19に無い古細菌 SmAP 系統。特に UMP 複合体 5MKN・6TFL は RNA接触残基の較正に有用）。関連：8XAP/8XAQ/8XAO（S. acidocaldarius Lsm の 2024年新規構造、別論文）も RCSB ヒット。
- **ウリジンポケット残基（精読で確認、両論文横断）**：MvaSmAP1（5MKN）＝**His39/Asn41/Arg63/Asp65**＋Leu38 主鎖。HsaSmAP（6TFL）＝**His37/Arg51/Asn39/Asp53**＋Gln36* 隣接。共通して Arg が uracil にスタック（H結合せず）、Asn が N3/O4 と、His が O2′ とリボース識別（Hfq の His57 相当）。His＝Hfq の Phe42 相当位置、Asn＝Hfq の Gln41 相当（Lsm 最保存残基＝PF01423）。
- **【重要・新規 PDB】1LOJ＝*M. thermolithotrophicus* SmAP1・UMP**（Nikulin 2020 Fig6 で確定、`1LJO`＝AF-Sm2 とは別物・混同注意）。他の U複合体アンカー一覧（Fig6）：4MML（Pae Hfq+UMP）・1I5L（AF-Sm1+U3 RNA）・1M8V（Pab-Sm1+U7 RNA）。

## C. 設計に効く重要ニュアンス（一次精読で判明）

1. **【重要】Hfq型 vs Sm型の分布は「細菌/古細菌」で綺麗に割れない**（Nielsen 2007）。*M. jannaschii*（古細菌）は Sm型を持たず **Hfq型（ヘキサマー、径54Å）** を持ち、*E. coli* Hfq と機能互換（sRNA結合・相補）。→ bio-a（Hfq）の taxon に**古細菌 Hfq様も含まれうる**。rooting と相互外群設計で「細菌=Hfq／古細菌=Sm」を単純前提にできない。
2. **SmAP パラログは遺伝子重複起源**（Mura 2003）：SmAP2/SmAP3 は SmAP1 の重複で生じた（水平伝播でない）。→ §3 opening③（Crenarchaeal SmAP1/2 重複史）と §1 の重複ベース rooting を支持。
3. **古細菌 Sm ⇔ RNase P RNA**（Törő 2001）：AF-Sm1/Sm2 は in vivo で RNase P RNA と会合＝tRNA プロセシング関与。真核 Lsm と機能的に平行（Reichelt 2023 の RNA homeostasis network と整合）。
4. **archaeal Sm = 真核 Sm core の "primitive form"**（Törő 2001 結論）：古細菌 Sm を真核 Sm/Lsm の祖先型外群に置く §1 の根拠を補強。
5. **【新規・設計形質①】SmAP1 vs SmAP2 の分子指標＝Sm1 モチーフ第3位の His vs Thr**（Nikulin 2020 精読）：SmAP1 は His（uracil にスタック、強い U結合）、SmAP2（Sso/Sac）は Thr40 → U18 RNA 親和性が **≥100倍低下**。T40H 置換でも cRBM 結合は回復せず。→ **クレナーキオータ SmAP1/2 パラログの機能分化を残基1つで説明**でき、design memo §3 の「SmAP1/2 重複史」の形質軸に直結。系統形質としてマップ可能。
6. **【新規・設計形質②】U結合様式が Sm型 vs Hfq型で構造的に別**（Nikulin 2020/2021 精読）：**SmAP＝"baseball glove"（同一モノマーの His＋Arg 2残基）**／**Hfq＝"Frisbee trap"（隣接2モノマーの芳香族 Phe/Tyr）**。かつ SmAP は**ウリジン単一サイトのみ**（Hfq のアデニン/distal サイトを欠く＝L4 loop で遮蔽）。UMP は SmAP で Hfq より **~90°回転**。→ Hfq型/Sm型の型判定（§1 rooting・bio-a↔bio-b 相互外群）を**構造・残基レベルで裏付ける形質**。
7. **【重要・仮説の反証】L4 loop 長は4次構造（ヘキサ/ヘプタ）を決めない**（Nikulin 2021 精読）：*H. salinarum* SmAP は L4 が**短い（3残基、細菌 Hfq 並み）のにヘプタマー**を形成。→ 「L4 短い＝ヘキサマー」という旧仮説を反証。オリゴマー状態を L4 長で予測する設計は不可。単量体構造はむしろ細菌 Hfq に近い（短 L4 が L2 loop 配向に影響）が、それでもヘプタ。※細胞内で実際に発現するのは HsaSmAP69（N末+電荷で RNA 結合↑）で、結晶化したのは HsaSmAP60。

## 相互確認（重畳表による独立クロスチェック）

一次精読で、**2本の論文の構造重畳表がアンカーPDB群を独立に確認**した。取り違えリスクは実質消滅：
- **Thore & Suck 2003 本文 Cα 重畳**：AF-Sm1 `1I4K`／AF-Sm2 `1LJO`／M. thermo Sm1 **`1I81`**（＝Collins A11 の孫引き推定が正しいと裏取り）／P. aerophilum `1I8F`／ヒト SmB/D3 `1D3B`・SmD1/D2 `1B34`。
- **Sauter 2003 Table 2（RMSD）**：`1KQ1`/`1KQ2`（S. aureus Hfq）・`1I4K`/`1I5L`（AF-Sm1）・`1LJO`・`1I8F`・`1M8V`・`1I81`・`1D3B`/`1B34` を同一表で照合。加えて M. jannaschii に Sm/Lsm 遺伝子を欠くまま Hfq様ホモログを同定（YKHAI モチーフ）＝§C-1（Nielsen 2007）を独立補強。

→ A1・A3・A4・A5・A6・A9・A11 は複数一次ソースで確定。**A2（3PGW）のみ ID が末尾脚注依存で PDBe 据置**、A4 論文本体は権限で未入手だが 1I4K/1I5L は他2論文の表で確定。

## 精読ログ追補（2026-07-05、Claude Science 言及の追加文献）

- **Payá & Bonete 2023（Microorganisms 11:1196）＝我々の census の比較基準（原著精読）**：UniProt 手動収集で **109古細菌種・163 Lsm タンパク**。**全ゲノムが 1〜3 Lsm を保有**（欠如ゼロ）。コピー数分布：**Nanoarchaeota 100%が単一 Lsm**／Euryarchaeota 74%が1・23%が2／**Crenarchaeota は多パラログ（65%が2、23%が3）**。2つのMW群（54-105残基 vs 139-164残基、後者はほぼ Crenarchaeota 限定）。遺伝子環境：Lrp/AsnC・MarR 転写因子、PUA ドメイン RNA結合タンパク、**リボソーム L37e（rpl37e）**隣接（Halobacteria では lsm と rpl37e が重複・共転写）。RNA結合残基（P. abyssi）＝**His37/Asn39/Arg63**（内部ポケット）、Lys22/Asp35/Asn39/Arg63 が>90%保存。→ **我々の census（MAG ベースで DPANN/Asgard へ拡張）と相補**：Payá は培養古細菌で「全て 1-3 Lsm」、我々は未培養 DPANN/Asgard でも保持を確認し、さらに CPR(細菌)で喪失を対比。**Nanoarchaeota が Payá で 100%単一 Lsm ＝我々の Nanoarchaeota 14/16 と整合**。
- **Törő 2001（A4）原著精読**：ウリジンポケット **His37・Asn39・Arg63**（loop3/5）。uracil を His37/Arg63 でサンドイッチ、Asn39（普遍保存）が O4/N3 と水素結合（Asp35 と Gly64 主鎖が Asn39 の向きを固定＝U特異性）、隣接サブユニットの Met38。**Sm fold ＋ Sm core 構築 ＋ RNA結合様式が古細菌↔真核で保存**（Cα rmsd ~0.6Å vs ヒト D3）＝古細菌 Sm を真核 Sm core のモデルにする根拠の原典。C2'-endo リボース必須。AF-Sm1/Sm2 は in vivo で RNase P RNA と会合。→ **ウリジンポケット His/Asn/Arg は Törő2001・Thore2003・Payá2023・Nikulin2020/21 の4論文で確定**。
- **Mura 2013（RNA Biol 総説、原著精読）framing**：Sm/Lsm/SmAP/Hfq は2002年に統一。**用語指針＝「Sm1/Sm2 motif は構造・進化的に区別する証拠がない」ので proximal(L3面)/distal(L4面) で呼ぶ**（本論文執筆時の用語に採用推奨）。Sm core ~60-70残基、N末αヘリックスは「inessential・多くの Sm 配列で欠く」＝定義的特徴でない。SmAP はオリゴマー可塑性（単環ヘキサ/ヘプタ・多環・高次集合）。L4=distal 面＝Hfq の A-rich RNA 部位。**「古細菌は Sm 生物学の missing link かつ opportunity」**＝bio-b の Introduction/Discussion の framing に使える。Sm fold はウイルスにも（Herpesvirus saimiri・cyanophage Sm・Brome mosaic virus が host Lsm1-7 を利用）＝Kim 2025 ファージ fold の先行文脈。
- **その他（要旨/既知レベルで把握、フル精読は優先度低）**：Fischer/Marchfelder 2010（初の古細菌 Lsm-sRNA 結合実証、*Hfx. volcanii*）、Vogel/Luisi 総説（細菌 sRNA と Hfq）、Bläsi 2017（Sso SmAP2 の 3'UTR mRNA 安定性）、Payá 2024/2021（*Hfx. mediterranei* Lsm 機能・ストレス応答）、Sabater-Muñoz 2017（endosymbiont ゲノム進化、CPR baseline）。
- **⚠ 対象外の混入**：`Structural basis for stop codon recognition in eukaryotes`（eRF1/eRF3 の終止コドン認識）は **Sm/Lsm と無関係**。誤 DL か Claude Science の誤言及の可能性 → 使わない。

## 確定作業メモ
- B群の未抽出 PDB ID（B2 Nielsen, B3 Someya）は各論文の Data deposition / Methods 節に記載。§2 実装時に該当ページ精読 or RCSB で確定。
- §2 実装：A群10構造の PDB 座標を RCSB REST から取得 → PROMALS3D/Expresso で構造ガイド MSA。3ドメイン・apo/RNA・ヘプタ(7)/ヘキサ(6)を網羅済み。
