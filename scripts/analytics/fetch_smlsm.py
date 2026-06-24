"""
Fetch Sm/Lsm/Hfq sequences from NCBI RefSeq for bio-b phylogenetic analysis.

Dataset structure:
  - Eukaryotic Sm:  SmB, SmD1, SmD2, SmD3, SmE, SmF, SmG  (7 subtypes)
  - Eukaryotic Lsm: Lsm1–Lsm8                               (8 subtypes)
  - Archaeal Sm:    sm-like archaeal protein (SmAP)
  - Bacterial Hfq:  hfq gene, bacteria, RefSeq
"""
import requests
import time
from pathlib import Path

EMAIL = "vivaldi.rv484@gmail.com"
APIKEY = "8a180c138a0e39293e410fe625beb73e4d08"
BASE = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils"
OUT_DIR = Path(__file__).parent.parent / "1-downloaded-data"
OUT_DIR.mkdir(parents=True, exist_ok=True)

RETMAX = 500  # 各クエリの上限

QUERIES = {
    # 真核生物 Sm サブタイプ
    "sm_SmB":  'SmB[Gene Name] AND eukaryota[Organism] AND refseq[Filter]',
    "sm_SmD1": 'SmD1[Gene Name] AND eukaryota[Organism] AND refseq[Filter]',
    "sm_SmD2": 'SmD2[Gene Name] AND eukaryota[Organism] AND refseq[Filter]',
    "sm_SmD3": 'SmD3[Gene Name] AND eukaryota[Organism] AND refseq[Filter]',
    "sm_SmE":  'SmE[Gene Name] AND eukaryota[Organism] AND refseq[Filter]',
    "sm_SmF":  'SmF[Gene Name] AND eukaryota[Organism] AND refseq[Filter]',
    "sm_SmG":  'SmG[Gene Name] AND eukaryota[Organism] AND refseq[Filter]',
    # 真核生物 Lsm サブタイプ
    "lsm_Lsm1": 'Lsm1[Gene Name] AND eukaryota[Organism] AND refseq[Filter]',
    "lsm_Lsm2": 'Lsm2[Gene Name] AND eukaryota[Organism] AND refseq[Filter]',
    "lsm_Lsm3": 'Lsm3[Gene Name] AND eukaryota[Organism] AND refseq[Filter]',
    "lsm_Lsm4": 'Lsm4[Gene Name] AND eukaryota[Organism] AND refseq[Filter]',
    "lsm_Lsm5": 'Lsm5[Gene Name] AND eukaryota[Organism] AND refseq[Filter]',
    "lsm_Lsm6": 'Lsm6[Gene Name] AND eukaryota[Organism] AND refseq[Filter]',
    "lsm_Lsm7": 'Lsm7[Gene Name] AND eukaryota[Organism] AND refseq[Filter]',
    "lsm_Lsm8": 'Lsm8[Gene Name] AND eukaryota[Organism] AND refseq[Filter]',
    # 古細菌 Sm
    "archaea_SmAP": 'sm-like archaeal protein[Protein Name] AND archaea[Organism]',
    # 細菌 Hfq
    "bacteria_Hfq": 'hfq[Gene Name] AND bacteria[Organism] AND refseq[Filter]',
}


def esearch(term: str, retmax: int) -> list[str]:
    r = requests.get(f"{BASE}/esearch.fcgi", params={
        "db": "protein", "term": term, "retmax": retmax,
        "retmode": "json", "api_key": APIKEY,
    }, timeout=30)
    result = r.json()["esearchresult"]
    return result["idlist"], int(result["count"])


def efetch_fasta(ids: list[str]) -> str:
    chunks = []
    for i in range(0, len(ids), 200):
        chunk = ids[i:i + 200]
        r = requests.post(f"{BASE}/efetch.fcgi", data={
            "db": "protein", "id": ",".join(chunk),
            "rettype": "fasta", "retmode": "text",
            "api_key": APIKEY, "email": EMAIL,
        }, timeout=60)
        r.raise_for_status()
        chunks.append(r.text)
        time.sleep(0.15)
    return "".join(chunks)


def count_seqs(fasta: str) -> int:
    return fasta.count(">")


if __name__ == "__main__":
    summary = []

    for label, term in QUERIES.items():
        print(f"\n[{label}]")
        ids, total = esearch(term, RETMAX)
        print(f"  total hits: {total}, fetching: {len(ids)}")

        if not ids:
            print("  → 0 sequences, skipping")
            summary.append((label, 0, total))
            continue

        fasta = efetch_fasta(ids)
        n = count_seqs(fasta)
        out = OUT_DIR / f"fetch_{label}.fasta"
        out.write_text(fasta)
        print(f"  → {n} sequences saved to {out.name}")
        summary.append((label, n, total))
        time.sleep(0.5)

    print("\n=== Summary ===")
    total_seqs = 0
    for label, n, total in summary:
        print(f"  {label}: {n} fetched / {total} total")
        total_seqs += n
    print(f"\nTotal sequences fetched: {total_seqs}")
    print("Next: cat all fetch_*.fasta > smlsm_all.fasta → CD-HIT → MAFFT → IQ-TREE3")
