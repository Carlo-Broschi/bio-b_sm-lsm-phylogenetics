"""
bio-b Fig: 縮小ゲノム2放散の Sm フォールド分布の対照＋構造検証。
- Panel A: 系統別の Sm/Lsm 保有率（archaea 保持 vs CPR 喪失）
- Panel B: foldseek TM-score 分布（archaea ヒットが本物の Sm fold である証拠）
出力: 4-results/fig_distribution_verification.{pdf,png}
"""
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

BASE = Path(__file__).resolve().parents[2]
ARCH = BASE / "3-analysis" / "hmm" / "census_lineage.tsv"
CPR = BASE / "3-analysis" / "hmm" / "census_lineage_cpr.tsv"
VERIF = BASE / "4-results" / "smfold_foldseek_verification.tsv"
OUT = BASE / "4-results" / "fig_distribution_verification"


def load_lineage(p):
    rows = []
    with p.open() as f:
        next(f)
        for line in f:
            c = line.rstrip("\n").split("\t")
            rows.append((c[0], int(c[1]), int(c[3])))  # taxon, n_genomes, genomes_with_SmLsm
    return rows


arch = load_lineage(ARCH)
cpr = load_lineage(CPR)
tms = [float(l.split("\t")[3]) for l in VERIF.read_text().splitlines()[1:]]

fig, (axA, axB) = plt.subplots(1, 2, figsize=(11, 5.2), gridspec_kw={"width_ratios": [1.5, 1]})

# --- Panel A: 保有率 ---
labels, fracs, colors, counts = [], [], [], []
for tax, ng, nsm in sorted(arch, key=lambda x: -x[2] / x[1]):
    labels.append(f"{tax}"); fracs.append(nsm / ng * 100); colors.append("#2166AC")
    counts.append(f"{nsm}/{ng}")
# separator
labels.append(""); fracs.append(0); colors.append("white"); counts.append("")
for tax, ng, nsm in sorted(cpr, key=lambda x: -x[1]):
    short = tax.replace("Candidatus ", "")
    labels.append(short); fracs.append(nsm / ng * 100); colors.append("#B2182B")
    counts.append(f"{nsm}/{ng}")

y = range(len(labels))
axA.barh(list(y), fracs, color=colors, height=0.7)
axA.set_yticks(list(y)); axA.set_yticklabels(labels, fontsize=9)
axA.invert_yaxis()
axA.set_xlim(0, 108)
axA.set_xlabel("genomes with Sm/Lsm (%)", fontsize=10)
for yi, (fr, ct) in enumerate(zip(fracs, counts)):
    if ct:
        axA.text(fr + 2, yi, ct, va="center", fontsize=8, color="#333")
axA.set_title("A  Sm-fold distribution across reduced-genome radiations",
              fontsize=11, loc="left", weight="bold")
axA.text(54, -0.7, "Archaea (DPANN/Asgard): RETAINED", color="#2166AC",
         fontsize=9, ha="center", weight="bold")
axA.text(54, len(arch) + 0.5, "Bacteria (CPR): LOST", color="#B2182B",
         fontsize=9, ha="center", weight="bold")
for sp in ("top", "right"):
    axA.spines[sp].set_visible(False)

# --- Panel B: TM-score 分布 ---
axB.hist(tms, bins=[0.90, 0.925, 0.95, 0.975, 1.0], color="#2166AC",
         edgecolor="white", rwidth=0.95)
axB.axvline(0.5, color="grey", ls="--", lw=1)
axB.set_xlim(0.88, 1.01)
axB.set_xlabel("Foldseek TM-score to Sm-fold anchor", fontsize=10)
axB.set_ylabel("archaeal hits (n=55)", fontsize=10)
axB.set_title("B  Structural verification of archaeal hits",
              fontsize=11, loc="left", weight="bold")
axB.text(0.945, axB.get_ylim()[1] * 0.9,
         "all 55 hits ≥0.92\n(median 0.96)\n→ genuine Sm fold",
         fontsize=9, ha="center", color="#333")
for sp in ("top", "right"):
    axB.spines[sp].set_visible(False)

fig.tight_layout()
fig.savefig(f"{OUT}.pdf", bbox_inches="tight")
fig.savefig(f"{OUT}.png", dpi=150, bbox_inches="tight")
print(f"保存: {OUT}.{{pdf,png}}")
