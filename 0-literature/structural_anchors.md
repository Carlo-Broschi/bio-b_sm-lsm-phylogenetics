# 構造アンカー論文 ↔ PDB ID 対応表

**作成 2026-07-04／一次精読で確定・訂正。** bio-b §2「構造アンカー較正アライメント」用。

## A. 確定（PDB ID を一次精読 or RCSB/PDBe で確認済み）

| # | 論文 | DOI | PDB | 生物 / 状態 | 確認手段 |
|---|---|---|---|---|---|
| A1 | Kambach et al. 1999 (Cell) | 10.1016/s0092-8674(00)80550-4 | **1D3B / 1B34** | ヒト Sm D3B / D1D2（Sm fold 基準） | 本文精読 |
| A2 | Weber & Wahl 2010 (EMBO J) | 10.1038/emboj.2010.295 | **3PGW** | ヒト U1 snRNP + snRNA, 4.4 Å | PDBe（本文精読で 4.4 Å・7 Sm 蛋白は一次確認、ID は末尾脚注のため PDBe 据置） |
| A3 | Mura & Eisenberg 2001 (PNAS) | 10.1073/pnas.091102298 | **1I8F** | *P. aerophilum* SmAP1 7量体, 1.75 Å | **本文精読（脚注 "PDB ID code 1I8F"）** |
| A4 | **Törő et al. 2001 (EMBO J)** | 10.1093/emboj/20.9.2293 | **1I5L**（apo）/ **1I4K**（+U5 RNA） | *A. fulgidus* AF-Sm1 7量体 | **本文精読（p.2301）** |
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
| B6 | Nikulin 2020 (Biochimie) | 10.1016/j.biochi.2020.05.001 | Sso vs Mvann Lsm U結合比較 | **PDF 入手待ち**（ユーザーが朝に ResearchGate 再アクセス） |
| B7 | Nikulin 2021 (Biochem Moscow) | 10.1134/s000629792107004x | *H. salinarum* Lsm | **PDF 入手待ち**（同上） |

## C. 設計に効く重要ニュアンス（一次精読で判明）

1. **【重要】Hfq型 vs Sm型の分布は「細菌/古細菌」で綺麗に割れない**（Nielsen 2007）。*M. jannaschii*（古細菌）は Sm型を持たず **Hfq型（ヘキサマー、径54Å）** を持ち、*E. coli* Hfq と機能互換（sRNA結合・相補）。→ bio-a（Hfq）の taxon に**古細菌 Hfq様も含まれうる**。rooting と相互外群設計で「細菌=Hfq／古細菌=Sm」を単純前提にできない。
2. **SmAP パラログは遺伝子重複起源**（Mura 2003）：SmAP2/SmAP3 は SmAP1 の重複で生じた（水平伝播でない）。→ §3 opening③（Crenarchaeal SmAP1/2 重複史）と §1 の重複ベース rooting を支持。
3. **古細菌 Sm ⇔ RNase P RNA**（Törő 2001）：AF-Sm1/Sm2 は in vivo で RNase P RNA と会合＝tRNA プロセシング関与。真核 Lsm と機能的に平行（Reichelt 2023 の RNA homeostasis network と整合）。
4. **archaeal Sm = 真核 Sm core の "primitive form"**（Törő 2001 結論）：古細菌 Sm を真核 Sm/Lsm の祖先型外群に置く §1 の根拠を補強。

## 相互確認（重畳表による独立クロスチェック）

一次精読で、**2本の論文の構造重畳表がアンカーPDB群を独立に確認**した。取り違えリスクは実質消滅：
- **Thore & Suck 2003 本文 Cα 重畳**：AF-Sm1 `1I4K`／AF-Sm2 `1LJO`／M. thermo Sm1 **`1I81`**（＝Collins A11 の孫引き推定が正しいと裏取り）／P. aerophilum `1I8F`／ヒト SmB/D3 `1D3B`・SmD1/D2 `1B34`。
- **Sauter 2003 Table 2（RMSD）**：`1KQ1`/`1KQ2`（S. aureus Hfq）・`1I4K`/`1I5L`（AF-Sm1）・`1LJO`・`1I8F`・`1M8V`・`1I81`・`1D3B`/`1B34` を同一表で照合。加えて M. jannaschii に Sm/Lsm 遺伝子を欠くまま Hfq様ホモログを同定（YKHAI モチーフ）＝§C-1（Nielsen 2007）を独立補強。

→ A1・A3・A4・A5・A6・A9・A11 は複数一次ソースで確定。**A2（3PGW）のみ ID が末尾脚注依存で PDBe 据置**、A4 論文本体は権限で未入手だが 1I4K/1I5L は他2論文の表で確定。

## 確定作業メモ
- B群の未抽出 PDB ID（B2 Nielsen, B3 Someya）は各論文の Data deposition / Methods 節に記載。§2 実装時に該当ページ精読 or RCSB で確定。
- §2 実装：A群10構造の PDB 座標を RCSB REST から取得 → PROMALS3D/Expresso で構造ガイド MSA。3ドメイン・apo/RNA・ヘプタ(7)/ヘキサ(6)を網羅済み。
