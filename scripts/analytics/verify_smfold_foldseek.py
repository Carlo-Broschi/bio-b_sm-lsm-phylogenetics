"""
bio-b: ESMFold 予測構造(3-analysis/predicted/*.pdb)を foldseek で確定アンカー
(3-analysis/structures/*.pdb, 特に古細菌 Sm)と照合し、Sm fold か検証する。

各予測構造について、最良ヒットのアンカー・TM-score・prob を記録。
高 TM-score(>0.5) かつ Sm 系アンカーに当たれば「本物の Sm fold」と判定。
出力: 4-results/smfold_foldseek_verification.tsv
"""
import subprocess
from pathlib import Path

BASE = Path(__file__).resolve().parents[2]
PRED = BASE / "3-analysis" / "predicted"
ANCHOR = BASE / "3-analysis" / "structures"
TMP = BASE / "3-analysis" / "foldseek_tmp"
OUTM8 = BASE / "3-analysis" / "foldseek_pred_vs_anchor.m8"
SUMMARY = BASE / "4-results" / "smfold_foldseek_verification.tsv"

# Sm フォールドのアンカー（古細菌 Sm＋真核 Sm＋細菌 Hfq、全て同 fold）
SM_ANCHORS = {"1I8F", "1I81", "1TH7", "1LJO", "1M5Q", "1M8V", "1I5L", "1I4K",
              "1H64", "1D3B", "3PGW", "1HK9", "1KQ1", "1U1S", "2QTX", "3AHU", "6GWK"}


def main():
    preds = list(PRED.glob("*.pdb"))
    if not preds:
        raise SystemExit("予測構造がありません。predict_smfold_hits.py を先に。")
    TMP.mkdir(exist_ok=True)
    # foldseek easy-search: 予測構造(query) vs アンカー(target)
    subprocess.run([
        "foldseek", "easy-search", str(PRED), str(ANCHOR), str(OUTM8), str(TMP),
        "--format-output", "query,target,alntmscore,evalue,prob,lddt",
        "-e", "10", "--exhaustive-search", "1",
    ], check=True, capture_output=True)

    # query ごとの最良ヒット（alntmscore 最大）
    best = {}
    for line in OUTM8.read_text().splitlines():
        c = line.split("\t")
        if len(c) < 6:
            continue
        q, t = c[0], c[1]
        tm = float(c[2]); ev = float(c[3]); prob = float(c[4]); lddt = float(c[5])
        anchor = Path(t).stem.split("_")[0].upper()[:4]
        if q not in best or tm > best[q][1]:
            best[q] = (anchor, tm, ev, prob, lddt)

    with SUMMARY.open("w") as f:
        f.write("prediction\ttaxon\tbest_anchor\ttm_score\tevalue\tprob\tlddt\tis_sm_fold\n")
        n_sm = 0
        for q in sorted(best):
            anchor, tm, ev, prob, lddt = best[q]
            taxon = q.split("_")[0]
            is_sm = "YES" if (anchor in SM_ANCHORS and tm >= 0.5) else "weak"
            if is_sm == "YES":
                n_sm += 1
            f.write(f"{q}\t{taxon}\t{anchor}\t{tm:.3f}\t{ev:.1e}\t{prob:.3f}\t{lddt:.3f}\t{is_sm}\n")
    print(f"照合 {len(best)} 予測構造、Sm fold 確認(TM>=0.5 & Sm アンカー): {n_sm}")
    print(f"→ {SUMMARY}")


if __name__ == "__main__":
    main()
