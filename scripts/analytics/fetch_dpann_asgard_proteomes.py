"""
DPANN / Asgard プロテオーム取得 → HMM 検索の標的DB を作る。

設計（design_from_literature.md §3）：
- DPANN は大半が GenBank の MAG で、多くが protein.faa.gz を持たない。
- 「真の欠如」を主張するには、アノテーション欠如を交絡させない必要がある。
  → protein.faa があればそれを使い、無ければ genomic.fna を Prodigal で
     ab initio 遺伝子予測してタンパク配列を得る（meta モード）。
- こうして得たプロテオームに対し PF01423(LSM)+PF17209(Hfq) を hmmsearch する
  （検索自体は別スクリプト / コマンド）。

出力：
- 1-downloaded-data/proteomes/<accession>.faa       各ゲノムのタンパク（ヘッダに taxon/accession をタグ）
- 1-downloaded-data/dpann_asgard_manifest.tsv       taxon, species, accession, source, n_proteins
"""
import argparse
import gzip
import io
import os
import subprocess
import sys
import time
from pathlib import Path

import requests

KEY = os.environ.get("NCBI_API_KEY", "")
BASE = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils"
OUT = Path(__file__).resolve().parents[2] / "1-downloaded-data"
PROT_DIR = OUT / "proteomes"
MANIFEST = OUT / "dpann_asgard_manifest.tsv"

DPANN = [
    "Nanoarchaeota", "Woesearchaeota", "Pacearchaeota", "Aenigmarchaeota",
    "Diapherotrites", "Nanohaloarchaeota", "Micrarchaeota", "Parvarchaeota",
    "Altiarchaeota",
]
ASGARD = [
    "Asgardarchaeota", "Lokiarchaeia", "Thorarchaeia", "Heimdallarchaeia",
    "Odinarchaeia",
]


def _get(url, **params):
    params["api_key"] = KEY
    for attempt in range(4):
        try:
            r = requests.get(url, params=params, timeout=45)
            r.raise_for_status()
            return r
        except Exception as e:
            if attempt == 3:
                raise
            time.sleep(2 * (attempt + 1))


def esearch(term, retmax):
    r = _get(f"{BASE}/esearch.fcgi", db="assembly", term=term,
             retmax=retmax, retmode="json")
    time.sleep(0.15)
    return r.json()["esearchresult"]["idlist"]


def esummary(uids):
    if not uids:
        return []
    r = _get(f"{BASE}/esummary.fcgi", db="assembly", id=",".join(uids),
             retmode="json")
    time.sleep(0.15)
    res = r.json().get("result", {})
    return [res[u] for u in res.get("uids", [])]


def download_gz(url, timeout=120):
    """FTP/HTTPS の .gz を取得して bytes を返す。無ければ None。"""
    url = url.replace("ftp://ftp.ncbi.nlm.nih.gov", "https://ftp.ncbi.nlm.nih.gov")
    try:
        r = requests.get(url, timeout=timeout)
        if r.status_code != 200 or not r.content:
            return None
        return gzip.decompress(r.content)
    except Exception:
        return None


def prodigal_predict(fna_bytes, accession):
    """genomic.fna(bytes) を Prodigal meta モードでタンパク予測。faa テキストを返す。"""
    tmp_fna = PROT_DIR / f"_{accession}.fna"
    tmp_faa = PROT_DIR / f"_{accession}.prodigal.faa"
    tmp_fna.write_bytes(fna_bytes)
    try:
        subprocess.run(
            ["prodigal", "-i", str(tmp_fna), "-a", str(tmp_faa),
             "-p", "meta", "-q", "-o", os.devnull],
            check=True, capture_output=True,
        )
        return tmp_faa.read_text()
    except Exception as e:
        print(f"    ! prodigal failed for {accession}: {e}", file=sys.stderr)
        return None
    finally:
        tmp_fna.unlink(missing_ok=True)
        tmp_faa.unlink(missing_ok=True)


def tag_headers(faa_text, taxon, accession):
    """FASTA ヘッダに taxon|accession を前置き（後の型判定・集計用）。"""
    out = []
    for line in faa_text.splitlines():
        if line.startswith(">"):
            out.append(f">{taxon}|{accession}|{line[1:]}")
        else:
            out.append(line)
    return "\n".join(out) + "\n"


def process_taxon(taxon, cap, rows):
    uids = esearch(f"{taxon}[Organism] AND latest[Filter]", cap)
    print(f"[{taxon}] {len(uids)} assemblies (cap={cap})")
    for s in esummary(uids):
        acc = s.get("assemblyaccession", "")
        org = s.get("organism", "")
        ftp = s.get("ftppath_refseq") or s.get("ftppath_genbank")
        if not ftp:
            continue
        base = ftp.rstrip("/").split("/")[-1]
        out_faa = PROT_DIR / f"{acc}.faa"
        if out_faa.exists():
            n = sum(1 for _ in out_faa.open() if _.startswith(">"))
            rows.append((taxon, org, acc, "cached", n))
            continue
        # 1) アノテーション済み protein.faa.gz を優先
        prot = download_gz(f"{ftp}/{base}_protein.faa.gz")
        source = "annotated"
        if prot is None:
            # 2) 無ければ genomic.fna を Prodigal 予測
            fna = download_gz(f"{ftp}/{base}_genomic.fna.gz")
            if fna is None:
                print(f"    - {acc}: no protein & no genomic; skip")
                rows.append((taxon, org, acc, "no_data", 0))
                continue
            faa_text = prodigal_predict(fna, acc)
            if faa_text is None:
                rows.append((taxon, org, acc, "prodigal_fail", 0))
                continue
            prot = faa_text.encode()
            source = "prodigal"
        text = prot.decode("utf-8", "replace")
        tagged = tag_headers(text, taxon, acc)
        out_faa.write_text(tagged)
        n = tagged.count(">")
        print(f"    + {acc} [{source}] {n} proteins  ({org})")
        rows.append((taxon, org, acc, source, n))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--cap", type=int, default=40,
                    help="1系統あたり取得する assembly 上限")
    ap.add_argument("--groups", choices=["dpann", "asgard", "both"], default="both")
    ap.add_argument("--only", nargs="*", help="特定 taxon だけ（パイロット用）")
    args = ap.parse_args()

    PROT_DIR.mkdir(parents=True, exist_ok=True)
    taxa = []
    if args.only:
        taxa = args.only
    else:
        if args.groups in ("dpann", "both"):
            taxa += DPANN
        if args.groups in ("asgard", "both"):
            taxa += ASGARD

    rows = []
    for t in taxa:
        process_taxon(t, args.cap, rows)

    with MANIFEST.open("w") as f:
        f.write("taxon\tspecies\taccession\tsource\tn_proteins\n")
        for r in rows:
            f.write("\t".join(map(str, r)) + "\n")
    ann = sum(1 for r in rows if r[3] == "annotated")
    pro = sum(1 for r in rows if r[3] == "prodigal")
    print(f"\n=== 完了: {len(rows)} genomes "
          f"(annotated={ann}, prodigal={pro}) → {MANIFEST}")


if __name__ == "__main__":
    main()
