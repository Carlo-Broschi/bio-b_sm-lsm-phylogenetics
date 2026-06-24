"""
BLAST SmAP1 (1JRI) against DPANN archaeal genomes to find Sm/Lsm homologs.
Uses NCBI BLAST API (remote).
"""
import requests
import time
from pathlib import Path

EMAIL = "vivaldi.rv484@gmail.com"
BLAST_URL = "https://blast.ncbi.nlm.nih.gov/blast/Blast.cgi"
ENTREZ_BASE = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils"
OUT_DIR = Path(__file__).parent.parent / "1-downloaded-data"
OUT_DIR.mkdir(parents=True, exist_ok=True)

# SmAP1 query (Methanothermobacter thermautotrophicus, PDB:1JRI)
QUERY = "MIDVSSQRVNVQRPLDALGNSLNSPVIIKLKGDREFRGVLKSFDLHMNLVLNDAEELEDGEVTRRLGTVLIRGDNIVYISP"

# DPANN taxa IDs
DPANN_ENTREZ_ORG = (
    "Nanoarchaeota[Organism] OR Woesearchaeota[Organism] OR "
    "Pacearchaeota[Organism] OR Aenigmarchaeota[Organism] OR "
    "Diapherotrites[Organism] OR Nanohaloarchaeota[Organism] OR "
    "Nanoarchaeales[Organism]"
)


def submit_blast(query: str) -> str:
    r = requests.post(BLAST_URL, data={
        "CMD": "Put",
        "PROGRAM": "blastp",
        "DATABASE": "nr",
        "QUERY": query,
        "ENTREZ_QUERY": DPANN_ENTREZ_ORG,
        "EXPECT": "1e-3",
        "FORMAT_TYPE": "JSON2",
        "HITLIST_SIZE": 200,
        "EMAIL": EMAIL,
    }, timeout=30)
    import re
    m = re.search(r'RID = ([A-Z0-9]+)', r.text)
    if m:
        return m.group(1)
    raise ValueError(f"RID not found in response:\n{r.text[:500]}")


def wait_and_fetch(rid: str) -> bytes:
    print(f"RID: {rid}, waiting for results...")
    while True:
        time.sleep(15)
        r = requests.get(BLAST_URL, params={
            "CMD": "Get", "RID": rid, "FORMAT_TYPE": "JSON2",
        }, timeout=30)
        if "Status=WAITING" in r.text:
            print("  still running...")
            continue
        if "Status=FAILED" in r.text:
            raise RuntimeError("BLAST job failed")
        if "Status=UNKNOWN" in r.text:
            raise RuntimeError("RID expired or unknown")
        return r.content  # binary to preserve ZIP integrity


def extract_accessions(zip_bytes: bytes) -> list[str]:
    import json, zipfile, io, re
    accs = []
    try:
        with zipfile.ZipFile(io.BytesIO(zip_bytes)) as zf:
            for name in zf.namelist():
                if "_1.json" in name:
                    data = json.loads(zf.read(name))
                    for entry in data.get("BlastOutput2", []):
                        hits = entry.get("report", {}).get("results", {}).get("search", {}).get("hits", [])
                        for h in hits:
                            for d in h.get("description", []):
                                if "accession" in d:
                                    accs.append(d["accession"])
    except Exception:
        accs = re.findall(rb'"accession"\s*:\s*"([^"]+)"', zip_bytes)
        accs = [a.decode() for a in accs]
    return list(dict.fromkeys(accs))


def fetch_fasta(accessions: list[str], out_path: Path) -> int:
    chunk_size = 100
    count = 0
    with open(out_path, "w") as f:
        for i in range(0, len(accessions), chunk_size):
            chunk = accessions[i:i + chunk_size]
            r = requests.post(f"{ENTREZ_BASE}/efetch.fcgi", data={
                "db": "protein", "id": ",".join(chunk),
                "rettype": "fasta", "retmode": "text", "email": EMAIL,
            }, timeout=60)
            r.raise_for_status()
            f.write(r.text)
            count += r.text.count(">")
            time.sleep(0.4)
    return count


if __name__ == "__main__":
    print("Submitting BLAST job...")
    rid = submit_blast(QUERY)
    result = wait_and_fetch(rid)

    out_json = OUT_DIR / "blast_dpann_result.json"
    out_json.write_bytes(result)
    print(f"Raw result saved → {out_json}")

    accessions = extract_accessions(result)
    print(f"Found {len(accessions)} hits: {accessions[:5]}...")

    if accessions:
        out_fasta = OUT_DIR / "dpann_sm_hits.fasta"
        n = fetch_fasta(accessions, out_fasta)
        print(f"Saved {n} sequences → {out_fasta}")
