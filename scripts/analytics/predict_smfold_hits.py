"""
bio-b: DPANN/Asgard の HMM ヒット(smfold_hits.faa)を ESMFold(ESMAtlas API) で
構造予測し、Sm fold か検証する（design memo §3 / 査読対策）。

- 各配列を ESMAtlas fold API で予測 → 3-analysis/predicted/<id>.pdb
- pLDDT(B-factor, 0-1 スケール)の平均を記録
- 出力サマリ: 4-results/smfold_prediction_summary.tsv
後段で foldseek により確定アンカー(1I8F 等)と構造照合する。
"""
import re
import time
import warnings
from pathlib import Path

import requests

warnings.filterwarnings("ignore")  # InsecureRequestWarning 抑制

BASE = Path(__file__).resolve().parents[2]
HITS = BASE / "3-analysis" / "hmm" / "smfold_hits.faa"
OUTDIR = BASE / "3-analysis" / "predicted"
SUMMARY = BASE / "4-results" / "smfold_prediction_summary.tsv"
API = "https://api.esmatlas.com/foldSequence/v1/pdb/"


def read_fasta(p):
    recs = []; h = None; s = []
    for line in p.open():
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


def safe_id(header):
    # "Loki|GCA_..|contig_n type=.." -> "Loki__GCA___contig_n"
    core = header.split(" ")[0]
    return re.sub(r"[^A-Za-z0-9]+", "_", core)


def predict(seq):
    for attempt in range(3):
        try:
            r = requests.post(API, data=seq, timeout=180, verify=False)
            if r.status_code == 200 and r.text.lstrip().startswith(("HEADER", "ATOM", "MODEL")):
                return r.text
            time.sleep(3)
        except Exception:
            time.sleep(5)
    return None


def mean_plddt(pdb_text):
    vals = []
    for l in pdb_text.splitlines():
        if l.startswith("ATOM") and l[12:16].strip() == "CA":
            try:
                vals.append(float(l[60:66]))
            except ValueError:
                pass
    return round(sum(vals) / len(vals), 3) if vals else None


def main():
    OUTDIR.mkdir(parents=True, exist_ok=True)
    recs = read_fasta(HITS)
    rows = []
    for i, (h, seq) in enumerate(recs, 1):
        sid = safe_id(h)
        taxon = h.split("|")[0]
        out = OUTDIR / f"{sid}.pdb"
        if out.exists():
            pl = mean_plddt(out.read_text())
            rows.append((sid, taxon, len(seq), pl, "cached"))
            continue
        pdb = predict(seq)
        if pdb is None:
            rows.append((sid, taxon, len(seq), None, "fail"))
            print(f"[{i}/{len(recs)}] {sid} FAIL")
        else:
            out.write_text(pdb)
            pl = mean_plddt(pdb)
            rows.append((sid, taxon, len(seq), pl, "ok"))
            print(f"[{i}/{len(recs)}] {sid} pLDDT={pl} len={len(seq)}")
        time.sleep(1.0)  # API 礼儀

    with SUMMARY.open("w") as f:
        f.write("id\ttaxon\tlength\tmean_plddt\tstatus\n")
        for r in rows:
            f.write("\t".join("" if v is None else str(v) for v in r) + "\n")
    ok = [r for r in rows if r[4] in ("ok", "cached")]
    conf = [r for r in ok if r[3] and r[3] >= 0.7]
    print(f"\n=== 予測 {len(ok)}/{len(recs)} 成功、うち pLDDT>=0.7(高信頼): {len(conf)} ===")
    print(f"→ {SUMMARY}, 構造 {OUTDIR}/")


if __name__ == "__main__":
    main()
