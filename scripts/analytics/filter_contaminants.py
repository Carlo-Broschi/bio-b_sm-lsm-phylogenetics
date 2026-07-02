"""smlsm_all.fasta を Sm/Lsm 系統解析用にキュレートする。

fetch_smlsm.py の緩い [Gene Name] クエリが2種類の問題を起こしていた（2026-07-03 診断）:

  (A) コンタミ混入:
      - SmG[Gene Name]  → "Smaug" / SAM domain (SAMD4) を 302 本誤マッチ
      - SmF/SmD2/SmB    → HMG / RNA polymerase / NAC / bromodomain 等を少数誤マッチ
  (B) 古細菌 Sm ソースの完全失敗:
      - SmAP[Gene Name] → 古細菌 Sm を1本も取れず、真核 "Small Acidic Protein"(SMAP)
        136 本を誤取得（fetch_archaea_SmAP.fasta の中身は 100% 非古細菌）

対処:
  (A) 明確なコンタミ説明文をブラックリスト除外（真の Sm/Lsm の多様な命名は温存）
  (B) fetch_archaea_SmAP 由来を全除外し、Veretnik 2009 のキュレート済み古細菌 Sm
      33 本（veretnik2009_archaea.fasta）に差し替え

出力: 2-preprocessed-data/smlsm_all_curated.fasta（本番解析はこれを入力にする）
"""
import re
from pathlib import Path

BASE = Path(__file__).resolve().parents[2]
DL = BASE / "1-downloaded-data"
PP = BASE / "2-preprocessed-data"

SRC = DL / "smlsm_all.fasta"
ARCHAEA_GARBAGE = DL / "fetch_archaea_SmAP.fasta"   # 100% 非古細菌（除外源）
ARCHAEA_CURATED = DL / "veretnik2009_archaea.fasta"  # 差し替え用（33本）
OUT = PP / "smlsm_all_curated.fasta"
REMOVED = PP / "smlsm_contaminants_removed.txt"

CONTAMINANT = re.compile(
    r"smaug"
    r"|sterile alpha motif"
    r"|small acidic protein"
    r"|\bsmap\b"
    r"|kinesin.associated"
    r"|bromodomain"
    r"|hmg.domain|hmg-box|hmg box"
    r"|mannan-binding"
    r"|thymidine kinase"
    r"|no apical meristem|\bnac\b"
    r"|defensin"
    r"|rna polymerase|rna-dependent rna polymerase"
    r"|no-on-and-no-off"
    r"|open reading frame",
    re.IGNORECASE,
)


def read_fasta(path):
    header, seq = None, []
    for line in open(path):
        if line.startswith(">"):
            if header is not None:
                yield header, "".join(seq)
            header, seq = line.rstrip(), []
        else:
            seq.append(line.rstrip())
    if header is not None:
        yield header, "".join(seq)


def main():
    garbage_ids = {h[1:].split()[0] for h, _ in read_fasta(ARCHAEA_GARBAGE)}

    kept, removed_contam, dropped_archaea, seen = [], [], 0, set()
    for header, seq in read_fasta(SRC):
        acc = header[1:].split()[0]
        desc = header[1:].split(None, 1)
        desc = desc[1] if len(desc) > 1 else ""
        if CONTAMINANT.search(desc):
            removed_contam.append(header[1:])
        elif acc in garbage_ids:            # 非古細菌の SmAP ゴミ
            dropped_archaea += 1
        else:
            kept.append((header, seq)); seen.add(acc)

    added = 0
    for header, seq in read_fasta(ARCHAEA_CURATED):
        acc = header[1:].split()[0]
        if acc not in seen:
            kept.append((header, seq)); seen.add(acc); added += 1

    with open(OUT, "w") as g:
        for header, seq in kept:
            g.write(f"{header}\n{seq}\n")
    with open(REMOVED, "w") as g:
        g.write("\n".join(removed_contam) + "\n")

    print(f"入力: {sum(1 for _ in read_fasta(SRC))} 本")
    print(f"(A) コンタミ除去: {len(removed_contam)} 本")
    print(f"(B) 非古細菌SmAPゴミ除外: {dropped_archaea} 本 / Veretnik古細菌追加: +{added} 本")
    print(f"最終キュレート版: {len(kept)} 本 -> {OUT.name}")


if __name__ == "__main__":
    main()
