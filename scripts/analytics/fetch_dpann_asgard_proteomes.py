"""
DPANN / Asgard プロテオーム取得 → HMM 検索の標的DB を作る（completeness フィルタ版）。

設計（design_from_literature.md §3）：
- DPANN/Asgard は大半が MAG。数千 assembly は冗長・不完全 MAG が多く、raw count を
  増やしても存在/欠如シグナルは改善せず、むしろ偽陰性ノイズが増える。
  → NCBI Datasets v2 API の CheckM completeness/contamination でフィルタし、
    系統ごとに completeness 上位を cap 件だけ取得する「中規模・層別」設計。
- GCA/GCF 重複は paired_accession で除去（RefSeq=GCF を優先）。
- アノテーション交絡の除去：protein.faa があればそれ、無ければ genomic.fna を
  Prodigal(meta) で ab initio 予測。→「真の欠如」がアノテーション欠如でないことを担保。
- 得たプロテオームに PF01423(LSM)+PF17209(Hfq) を hmmsearch（別工程）。

出力：
- 1-downloaded-data/proteomes/<accession>.faa           taxon|accession タグ付き
- 1-downloaded-data/dpann_asgard_manifest.tsv           taxon,species,accession,completeness,contamination,source,n_proteins
"""
import argparse
import gzip
import os
import subprocess
import sys
import time
from pathlib import Path

import requests

KEY = os.environ.get("NCBI_API_KEY", "")
HDR = {"api-key": KEY} if KEY else {}
DATASETS = "https://api.ncbi.nlm.nih.gov/datasets/v2/genome"
FTP = "https://ftp.ncbi.nlm.nih.gov/genomes/all"
OUT = Path(__file__).resolve().parents[2] / "1-downloaded-data"
PROT_DIR = OUT / "proteomes"
MANIFEST = OUT / "dpann_asgard_manifest.tsv"

DPANN = [
    "Nanoarchaeota", "Woesearchaeota", "Pacearchaeota", "Aenigmarchaeota",
    "Diapherotrites", "Nanohaloarchaeota", "Micrarchaeota", "Parvarchaeota",
    "Altiarchaeota",
]
# クラスを門より先に列挙：クラス所属 genome をクラスタグで取得し、
# 門クエリ(Asgardarchaeota)は「未分類 Asgard」だけを拾うようにする（帰属の二重化回避）
ASGARD = [
    "Lokiarchaeia", "Thorarchaeia", "Heimdallarchaeia", "Odinarchaeia",
    "Asgardarchaeota",
]


def _req(method, url, **kw):
    for attempt in range(4):
        try:
            r = requests.request(method, url, timeout=90, **kw)
            r.raise_for_status()
            return r
        except Exception:
            if attempt == 3:
                return None
            time.sleep(2 * (attempt + 1))


def gather_candidates(taxon, min_compl, max_contam, cap):
    """datasets v2 report をページングし、completeness フィルタ済み候補を返す。"""
    cands = {}          # numeric_core -> record（GCA/GCF 重複を潰す）
    token = None
    while True:
        params = {"page_size": 500}
        if token:
            params["page_token"] = token
        r = _req("GET", f"{DATASETS}/taxon/{taxon}/dataset_report",
                 headers=HDR, params=params)
        if r is None:
            break
        j = r.json()
        for rep in j.get("reports", []):
            acc = rep.get("accession", "")
            name = rep.get("assembly_info", {}).get("assembly_name", "")
            cm = rep.get("checkm_info", {})
            compl = cm.get("completeness")
            contam = cm.get("contamination")
            if compl is None or compl < min_compl:
                continue
            if contam is not None and contam > max_contam:
                continue
            annotated = bool(rep.get("annotation_info"))
            org = rep.get("organism", {}).get("organism_name", "")
            core = acc.split("_")[1].split(".")[0]      # GCA/GCF 共通の数値部
            rec = {"acc": acc, "name": name, "compl": compl,
                   "contam": contam if contam is not None else "",
                   "annotated": annotated, "org": org}
            prev = cands.get(core)
            # RefSeq(GCF) を優先、同格なら completeness 高い方
            if prev is None:
                cands[core] = rec
            else:
                better_src = acc.startswith("GCF") and prev["acc"].startswith("GCA")
                if better_src or (prev["acc"][:3] == acc[:3] and compl > prev["compl"]):
                    cands[core] = rec
        token = j.get("next_page_token")
        if not token:
            break
        time.sleep(0.2)
    ranked = sorted(cands.values(), key=lambda d: d["compl"], reverse=True)
    return ranked[:cap], len(cands)


def ftp_base(acc, name):
    pre, num = acc.split("_")
    num = num.split(".")[0]
    parts = "/".join([num[0:3], num[3:6], num[6:9]])
    return f"{FTP}/{pre}/{parts}/{acc}_{name}"


def download_gz(url):
    r = _req("GET", url)
    if r is None or r.status_code != 200 or not r.content:
        return None
    try:
        return gzip.decompress(r.content)
    except Exception:
        return None


def prodigal_predict(fna_bytes, acc):
    tmp_fna = PROT_DIR / f"_{acc}.fna"
    tmp_faa = PROT_DIR / f"_{acc}.prodigal.faa"
    tmp_fna.write_bytes(fna_bytes)
    try:
        subprocess.run(["prodigal", "-i", str(tmp_fna), "-a", str(tmp_faa),
                        "-p", "meta", "-q", "-o", os.devnull],
                       check=True, capture_output=True)
        return tmp_faa.read_text()
    except Exception as e:
        print(f"    ! prodigal failed {acc}: {e}", file=sys.stderr)
        return None
    finally:
        tmp_fna.unlink(missing_ok=True)
        tmp_faa.unlink(missing_ok=True)


def tag_headers(text, taxon, acc):
    out = []
    for line in text.splitlines():
        out.append(f">{taxon}|{acc}|{line[1:]}" if line.startswith(">") else line)
    return "\n".join(out) + "\n"


def fetch_proteome(taxon, c, rows, seen):
    acc, name = c["acc"], c["name"]
    # 上位分類（門）と下位（綱）の重複回避：既に別 taxon で取得済なら skip。
    # クラスを門より先に列挙しているため、より具体的な系統タグが優先される。
    if acc in seen:
        return
    seen.add(acc)
    out_faa = PROT_DIR / f"{acc}.faa"
    if out_faa.exists():
        n = sum(1 for _ in out_faa.open() if _.startswith(">"))
        rows.append((taxon, c["org"], acc, c["compl"], c["contam"], "cached", n))
        return
    base = ftp_base(acc, name)
    source = "annotated"
    prot = download_gz(f"{base}/{acc}_{name}_protein.faa.gz") if c["annotated"] else None
    if prot is None:
        fna = download_gz(f"{base}/{acc}_{name}_genomic.fna.gz")
        if fna is None:
            print(f"    - {acc}: no data; skip")
            rows.append((taxon, c["org"], acc, c["compl"], c["contam"], "no_data", 0))
            return
        txt = prodigal_predict(fna, acc)
        if txt is None:
            rows.append((taxon, c["org"], acc, c["compl"], c["contam"], "prodigal_fail", 0))
            return
        prot = txt.encode()
        source = "prodigal"
    tagged = tag_headers(prot.decode("utf-8", "replace"), taxon, acc)
    out_faa.write_text(tagged)
    n = tagged.count(">")
    print(f"    + {acc} [{source}] compl={c['compl']} contam={c['contam']} "
          f"{n} prot  ({c['org']})")
    rows.append((taxon, c["org"], acc, c["compl"], c["contam"], source, n))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--cap", type=int, default=40, help="1系統あたり取得上限（completeness 上位）")
    ap.add_argument("--min-completeness", type=float, default=80.0)
    ap.add_argument("--max-contamination", type=float, default=5.0)
    ap.add_argument("--groups", choices=["dpann", "asgard", "both"], default="both")
    ap.add_argument("--only", nargs="*")
    args = ap.parse_args()

    PROT_DIR.mkdir(parents=True, exist_ok=True)
    taxa = args.only or ((DPANN if args.groups in ("dpann", "both") else [])
                         + (ASGARD if args.groups in ("asgard", "both") else []))

    rows = []
    seen = set()
    for t in taxa:
        picks, npass = gather_candidates(t, args.min_completeness,
                                         args.max_contamination, args.cap)
        print(f"[{t}] completeness>={args.min_completeness} & contam<="
              f"{args.max_contamination}: {npass} genomes 通過 → 上位 {len(picks)} 取得")
        for c in picks:
            fetch_proteome(t, c, rows, seen)

    with MANIFEST.open("w") as f:
        f.write("taxon\tspecies\taccession\tcompleteness\tcontamination\tsource\tn_proteins\n")
        for r in rows:
            f.write("\t".join(map(str, r)) + "\n")
    ann = sum(1 for r in rows if r[5] == "annotated")
    pro = sum(1 for r in rows if r[5] == "prodigal")
    print(f"\n=== 完了: {len(rows)} genomes (annotated={ann}, prodigal={pro}) → {MANIFEST}")


if __name__ == "__main__":
    main()
