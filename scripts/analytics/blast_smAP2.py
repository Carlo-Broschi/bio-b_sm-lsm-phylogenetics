"""
BLAST SmAP2 (Archaeoglobus fulgidus, UniProt O28751) against DPANN and CPR.
SmAP2 is a distinct archaeal Sm protein; using it alongside SmAP1 covers
broader archaeal Sm sequence diversity.
"""
import requests
import time
import re
import json
import zipfile
import io
from pathlib import Path

EMAIL = "vivaldi.rv484@gmail.com"
BLAST_URL = "https://blast.ncbi.nlm.nih.gov/blast/Blast.cgi"
ENTREZ_BASE = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils"
OUT_DIR = Path(__file__).parent.parent / "1-downloaded-data"
OUT_DIR.mkdir(parents=True, exist_ok=True)

# SmAP2 (Archaeoglobus fulgidus, UniProt O28751) — 75 aa
QUERY_SMAP2 = "MKVLVLKGDKEVRGMLRSFELHMELVLKDAEELEAGETKRLGTVLIRGDRIVYIEPAAEE"

TARGETS = {
    "dpann": (
        "Nanoarchaeota[Organism] OR Woesearchaeota[Organism] OR "
        "Pacearchaeota[Organism] OR Aenigmarchaeota[Organism] OR "
        "Diapherotrites[Organism] OR Nanohaloarchaeota[Organism] OR "
        "Nanoarchaeales[Organism]"
    ),
    "cpr": (
        "Patescibacteria[Organism] OR Microgenomates[Organism] OR "
        "Parcubacteria[Organism] OR Peregrinibacteria[Organism] OR "
        "Gracilibacteria[Organism] OR Absconditabacteria[Organism] OR "
        "Saccharimonadia[Organism]"
    ),
}


def submit_blast(query: str, entrez_org: str) -> str:
    r = requests.post(BLAST_URL, data={
        "CMD": "Put", "PROGRAM": "blastp", "DATABASE": "nr",
        "QUERY": query, "ENTREZ_QUERY": entrez_org,
        "EXPECT": "1e-3", "FORMAT_TYPE": "JSON2", "HITLIST_SIZE": 200,
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
        return r.content


def extract_accessions(zip_bytes: bytes) -> list[str]:
    accs = []
    try:
        with zipfile.ZipFile(io.BytesIO(zip_bytes)) as zf:
            for name in zf.namelist():
                if name.endswith(".json"):
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


if __name__ == "__main__":
    jobs = [("smAP2", "dpann"), ("smAP2", "cpr")]

    for query_name, target_name in jobs:
        label = f"{query_name}×{target_name}"
        print(f"\nSubmitting: {label}")
        try:
            rid = submit_blast(QUERY_SMAP2, TARGETS[target_name])
            result = wait_and_fetch(rid, label)
            out_json = OUT_DIR / f"blast_{query_name}_{target_name}.json"
            out_json.write_bytes(result)
            accs = extract_accessions(result)
            print(f"  → {len(accs)} hits")
            if accs:
                print(f"  accessions: {accs[:5]}")
        except Exception as e:
            print(f"  ERROR: {e}")
        time.sleep(5)

    print("\nDone.")
