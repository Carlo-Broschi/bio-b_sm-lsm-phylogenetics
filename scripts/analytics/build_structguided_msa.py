"""
bio-b: 構造ガイド MSA パイプライン（design memo §2）。再現用にワークフローを集約。

前提ツール: foldseek/foldmason（GitHub 静的バイナリ）、cd-hit、mafft。
入力: 確定アンカー19 PDB（3-analysis/structures/*.pdb）、curated nr90（2-preprocessed-data/smlsm_curated_nr90.fasta）。

手順:
 1. foldmason easy-msa で 19 PDB の構造 MSA（全鎖）を生成
 2. ユニーク鎖抽出 → CD-HIT 0.95 で distinct タンパク代表に縮約（構造 seed）
 3. mafft --seed で curated 配列を構造 seed にガイド整列
 4. 占有率トリム（列>=10%, 行>=30%）→ 解析用アライメント

このスクリプトは 2/4 の Python 部分（縮約・トリム）を担う。1（foldmason）と
3（mafft）はシェルで実行（末尾のコメント参照）。
"""
import subprocess
import sys
from pathlib import Path

BASE = Path(__file__).resolve().parents[2]
STRUCT_MSA = BASE / "3-analysis" / "structure_anchor_msa_aa.fa"
SEED = BASE / "3-analysis" / "structure_anchor_seed.fa"
GUIDED = BASE / "3-analysis" / "smlsm_curated_structguided.fasta"
TRIM = BASE / "3-analysis" / "smlsm_structguided_trim.fasta"


def read_fasta(p):
    recs = []; h = None; s = []
    for line in open(p):
        line = line.rstrip("\n")
        if line.startswith(">"):
            if h:
                recs.append((h, "".join(s)))
            h = line[1:]; s = []
        else:
            s.append(line)
    if h:
        recs.append((h, "".join(s)))
    return recs


def drop_allgap_cols(recs):
    L = len(recs[0][1])
    cols = [i for i in range(L) if any(a[i] not in "-." for _, a in recs)]
    return [(h, "".join(a[i] for i in cols)) for h, a in recs]


def build_seed():
    """構造 MSA の全鎖 → ユニーク鎖 → CD-HIT 0.95 代表 → 構造 seed（整列保持）。"""
    recs = read_fasta(STRUCT_MSA)
    seen = {}; uniq = []
    for h, aln in recs:
        ung = aln.replace("-", "").replace(".", "")
        if len(ung) < 40 or ung in seen:      # 断片/RNA鎖・重複を除外
            continue
        seen[ung] = h; uniq.append((h, aln))
    uniq = drop_allgap_cols(uniq)

    tmp_ung = Path("/tmp/seed_ungapped.fa")
    tmp_ung.write_text("".join(f">{h}\n{a.replace('-','').replace('.','')}\n" for h, a in uniq))
    subprocess.run(["cd-hit", "-i", str(tmp_ung), "-o", "/tmp/seed_rep.fa",
                    "-c", "0.95", "-n", "5", "-T", "4", "-M", "2000"],
                   check=True, capture_output=True)
    reps = {l[1:].strip() for l in open("/tmp/seed_rep.fa") if l.startswith(">")}
    keep = drop_allgap_cols([(h, a) for h, a in uniq if h in reps])
    SEED.write_text("".join(f">{h}\n{a}\n" for h, a in keep))
    print(f"構造 seed: {len(keep)} 配列 x {len(keep[0][1])} 列 → {SEED}")


def trim_guided(col_occ=0.10, row_occ=0.30):
    """mafft --seed 出力を占有率トリムし、seed 行を除いて解析用に。"""
    recs = read_fasta(GUIDED)
    n = len(recs); L = len(recs[0][1])
    occ = [0] * L
    for _, s in recs:
        for i, c in enumerate(s):
            if c not in "-.":
                occ[i] += 1
    keepcols = [i for i in range(L) if occ[i] / n >= col_occ]
    kc = len(keepcols)
    final = []
    for h, s in recs:
        if "_seed_" in h:                      # 構造 seed は解析から除外
            continue
        t = "".join(s[i] for i in keepcols)
        if sum(1 for c in t if c not in "-.") / kc >= row_occ:
            final.append((h, t))
    TRIM.write_text("".join(f">{h}\n{s}\n" for h, s in final))
    print(f"解析用トリム: {len(final)} 配列 x {kc} 列 → {TRIM}")


if __name__ == "__main__":
    step = sys.argv[1] if len(sys.argv) > 1 else "all"
    if step in ("seed", "all"):
        build_seed()
    if step in ("trim", "all"):
        trim_guided()

# --- シェル手順（このスクリプト外で実行）---
# 1) 構造 MSA:
#    foldmason easy-msa 3-analysis/structures/*.pdb \
#        3-analysis/structure_anchor_msa 3-analysis/structures/tmp
#    python build_structguided_msa.py seed
# 2) 構造ガイド整列:
#    mafft --seed 3-analysis/structure_anchor_seed.fa --anysymbol --thread 4 --reorder \
#        2-preprocessed-data/smlsm_curated_nr90.fasta > 3-analysis/smlsm_curated_structguided.fasta
#    python build_structguided_msa.py trim
