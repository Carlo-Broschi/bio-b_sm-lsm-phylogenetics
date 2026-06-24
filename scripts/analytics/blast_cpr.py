"""
BLAST multiple Sm/Lsm/Hfq queries against CPR (Patescibacteria) and DPANN.

Queries:
  - Hfq     : E. coli Hfq (P0A6X3)    → bacterial Sm-like, for CPR
  - SmAP1   : M. thermautotrophicus    → archaeal Sm-like, for DPANN (run separately)
  - Sm1(SmB): H. sapiens SmB (P14678)  → eukaryotic Sm, broad search
  - Lsm1    : H. sapiens Lsm1 (O15116) → eukaryotic Lsm, broad search
"""
import requests
import time
import re
from pathlib import Path

EMAIL = "vivaldi.rv484@gmail.com"
BLAST_URL = "https://blast.ncbi.nlm.nih.gov/blast/Blast.cgi"
ENTREZ_BASE = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils"
OUT_DIR = Path(__file__).parent.parent / "1-downloaded-data"
OUT_DIR.mkdir(parents=True, exist_ok=True)

QUERIES = {
    # E. coli Hfq (UniProt P0A6X3) — 102 aa
    "hfq_ecoli": (
        "MAKS NDNTSLSEQETRELEMFISSMLGTNSSKITVETPQTLKDGQIQLNEKMNFQLCTMGQNLNDHFSDLQSTLDDAKS"
        "MSRDELEALLREQQAVPADASK"
    ).replace(" ", ""),

    # H. sapiens SmB/B' (UniProt P14678) — Sm core
    "sm1_human": (
        "MANKQDNQKPPTPPKTPKKKDKNKNKDQEEPQRRLIQLKSEIKELEQVFHNLKQKYPRLDGKVKMRGMLGMPGKLDLNSG"
        "EISAIVKLDNLRDIEQFLGQPMPQNPPPPGMRGRGMPPPRGPRMPPPRGPRGMPPPRGPRGMPPPRGPRV"
    ).replace(" ", ""),

    # H. sapiens Lsm1 (UniProt O15116) — 133 aa
    "lsm1_human": (
        "MADEKKFQKPQAELAAQMQKIMSGQGLNQTHVSMILGPNGTEKLNDIRNLMKDINQLFGKPIQPNMPRGGPRGMPGRGMG"
        "RMGRGRGRGRGPGGRRGRGRGRPGGFGGGRGMDRGGRGRGRGFGGGRGMDRGGRGRGRGFG"
    ).replace(" ", ""),
}

TARGETS = {
    "cpr": (
        "Patescibacteria[Organism] OR Microgenomates[Organism] OR "
        "Parcubacteria[Organism] OR Peregrinibacteria[Organism] OR "
        "Gracilibacteria[Organism] OR Absconditabacteria[Organism] OR "
        "Saccharimonadia[Organism]"
    ),
    "dpann": (
        "Nanoarchaeota[Organism] OR Woesearchaeota[Organism] OR "
        "Pacearchaeota[Organism] OR Aenigmarchaeota[Organism] OR "
        "Diapherotrites[Organism] OR Nanohaloarchaeota[Organism] OR "
        "Nanoarchaeales[Organism]"
    ),
}


def submit_blast(query: str, entrez_org: str) -> str:
    r = requests.post(BLAST_URL, data={
        "CMD": "Put",
        "PROGRAM": "blastp",
        "DATABASE": "nr",
        "QUERY": query,
        "ENTREZ_QUERY": entrez_org,
        "EXPECT": "1e-3",
        "FORMAT_TYPE": "JSON2",
        "HITLIST_SIZE": 200,
        "EMAIL": EMAIL,
    }, timeout=30)
    m = re.search(r'RID = ([A-Z0-9]+)', r.text)
    if m:
        return m.group(1)
    raise ValueError(f"RID not found:\n{r.text[:300]}")


def wait_and_fetch(rid: str, label: str) -> bytes:
    print(f"  [{label}] RID: {rid}")
    while True:
        time.sleep(15)
        r = requests.get(BLAST_URL, params={
            "CMD": "Get", "RID": rid, "FORMAT_TYPE": "JSON2",
        }, timeout=30)
        if "Status=WAITING" in r.text:
            print(f"  [{label}] still running...")
            continue
        if "Status=FAILED" in r.text:
            raise RuntimeError(f"[{label}] BLAST failed")
        if "Status=UNKNOWN" in r.text:
            raise RuntimeError(f"[{label}] RID expired")
        return r.content  # binary to preserve ZIP integrity


def extract_accessions(zip_bytes: bytes) -> list[str]:
    import zipfile, io
    accs = []
    try:
        with zipfile.ZipFile(io.BytesIO(zip_bytes)) as zf:
            for name in zf.namelist():
                if name.endswith(".json") and not name.endswith("BlastJSON"):
                    data = json.loads(zf.read(name))
                    for entry in data.get("BlastOutput2", []):
                        hits = entry.get("report", {}).get("results", {}).get("search", {}).get("hits", [])
                        for h in hits:
                            for d in h.get("description", []):
                                if "accession" in d:
                                    accs.append(d["accession"])
    except Exception:
        # fallback: regex on raw bytes
        accs = re.findall(rb'"accession"\s*:\s*"([^"]+)"', zip_bytes)
        accs = [a.decode() for a in accs]
    return list(dict.fromkeys(accs))


def fetch_fasta(accessions: list[str], out_path: Path) -> int:
    count = 0
    with open(out_path, "w") as f:
        for i in range(0, len(accessions), 100):
            chunk = accessions[i:i + 100]
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
    # CPR × Hfq, Sm1, Lsm1
    # DPANN × Sm1, Lsm1  (SmAP1 × DPANN は blast_dpann.py で実行)
    jobs = [
        ("hfq_ecoli",  "cpr"),
        ("sm1_human",  "cpr"),
        ("lsm1_human", "cpr"),
        ("sm1_human",  "dpann"),
        ("lsm1_human", "dpann"),
    ]

    all_hits: dict[str, list[str]] = {}

    for query_name, target_name in jobs:
        label = f"{query_name}×{target_name}"
        print(f"\nSubmitting: {label}")
        try:
            rid = submit_blast(QUERIES[query_name], TARGETS[target_name])
            result = wait_and_fetch(rid, label)
            out_json = OUT_DIR / f"blast_{query_name}_{target_name}.json"
            out_json.write_bytes(result)
            accs = extract_accessions(result)
            print(f"  → {len(accs)} hits")
            all_hits[label] = accs
        except Exception as e:
            print(f"  ERROR: {e}")
            all_hits[label] = []
        time.sleep(5)  # NCBI へのマナー

    # サマリー
    print("\n=== Summary ===")
    for label, accs in all_hits.items():
        print(f"{label}: {len(accs)} hits")
        if accs:
            out_fasta = OUT_DIR / f"hits_{label.replace('×', '_')}.fasta"
            n = fetch_fasta(accs, out_fasta)
            print(f"  → saved {n} sequences to {out_fasta.name}")
