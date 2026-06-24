"""
Fetch Sm/LSm protein sequences from NCBI for phylogenetic analysis.
Usage: uv run --python ../../shared/venv-bio/bin/python fetch_sm_lsm.py
"""
from Bio import Entrez, SeqIO
from pathlib import Path

Entrez.email = "vivaldi.rv484@gmail.com"

OUT_DIR = Path(__file__).parent.parent / "data" / "raw"
OUT_DIR.mkdir(parents=True, exist_ok=True)

QUERIES = {
    "sm": "Sm protein[Protein Name] AND refseq[filter]",
    "lsm": "(LSm[Protein Name] OR \"like Sm\"[Protein Name]) AND refseq[filter]",
}
MAX_RECORDS = 300


def fetch_by_query(label: str, query: str) -> None:
    handle = Entrez.esearch(db="protein", term=query, retmax=MAX_RECORDS)
    record = Entrez.read(handle)
    handle.close()
    ids = record["IdList"]
    print(f"[{label}] Found {record['Count']}, fetching {len(ids)}")
    if not ids:
        return
    handle = Entrez.efetch(db="protein", id=",".join(ids), rettype="fasta", retmode="text")
    out = OUT_DIR / f"{label}_refseq.fasta"
    with open(out, "w") as f:
        f.write(handle.read())
    handle.close()
    n = len(list(SeqIO.parse(out, "fasta")))
    print(f"  Saved {n} sequences → {out}")


if __name__ == "__main__":
    for label, query in QUERIES.items():
        fetch_by_query(label, query)
