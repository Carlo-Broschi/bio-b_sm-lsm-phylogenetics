"""
Survey DPANN archaea in NCBI:
1. List species with RefSeq genomes
2. Check if each species has Sm/Lsm/Hfq annotations
"""
import requests
import time
from pathlib import Path

APIKEY = "8a180c138a0e39293e410fe625beb73e4d08"
BASE = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils"
OUT_DIR = Path(__file__).parent.parent / "1-downloaded-data"

DPANN_TAXA = [
    "Nanoarchaeota", "Woesearchaeota", "Pacearchaeota",
    "Aenigmarchaeota", "Diapherotrites", "Nanohaloarchaeota",
    "Nanoarchaeales", "Micrarchaeota", "Parvarchaeota",
]

SM_KEYWORDS = [
    "sm protein", "lsm protein", "sm-like", "hfq",
    "RNA chaperone", "sm archaeal", "SmAP",
]


def esearch(db: str, term: str, retmax: int = 500) -> tuple[list[str], int]:
    r = requests.get(f"{BASE}/esearch.fcgi", params={
        "db": db, "term": term, "retmax": retmax,
        "retmode": "json", "api_key": APIKEY,
    }, timeout=30)
    res = r.json()["esearchresult"]
    return res["idlist"], int(res["count"])


def esummary(db: str, ids: list[str]) -> list[dict]:
    if not ids:
        return []
    r = requests.post(f"{BASE}/esummary.fcgi", data={
        "db": db, "id": ",".join(ids),
        "retmode": "json", "api_key": APIKEY,
    }, timeout=60)
    result = r.json().get("result", {})
    return [result[uid] for uid in result.get("uids", [])]


if __name__ == "__main__":
    print("=== DPANN Species Survey ===\n")

    all_species = {}  # species_name -> {taxon, genome_count, sm_hits}

    # 1. DPANN 各タクソンのゲノム登録種を取得
    for taxon in DPANN_TAXA:
        ids, total = esearch("assembly", f"{taxon}[Organism] AND latest_refseq[Filter]")
        if not ids:
            # RefSeq がなければ GenBank も試す
            ids, total = esearch("assembly", f"{taxon}[Organism] AND latest[Filter]")
        print(f"{taxon}: {total} assemblies")
        if ids:
            summaries = esummary("assembly", ids[:20])
            for s in summaries:
                name = s.get("speciesname", s.get("organism", "?"))
                all_species[name] = {"taxon": taxon, "genome_count": total, "sm_hits": []}
        time.sleep(0.2)

    print(f"\nTotal unique species (sample): {len(all_species)}")

    # 2. 各タクソンで Sm/Lsm キーワードを protein DB で検索
    print("\n=== Sm/Lsm/Hfq keyword search in DPANN ===\n")
    results = []
    for taxon in DPANN_TAXA:
        for kw in SM_KEYWORDS:
            term = f'{kw}[Protein Name] AND {taxon}[Organism]'
            ids, count = esearch("protein", term, retmax=10)
            if count > 0:
                summaries = esummary("protein", ids[:5])
                hits = [(s.get("accessionversion", "?"), s.get("organism", "?"), s.get("title", "?")[:60])
                        for s in summaries]
                results.append((taxon, kw, count, hits))
                print(f"[HIT] {taxon} × {kw}: {count} hits")
                for acc, org, title in hits[:3]:
                    print(f"       {acc} | {org} | {title}")
            time.sleep(0.15)

    if not results:
        print("No Sm/Lsm/Hfq annotations found in any DPANN taxon.")

    # 3. DPANN 全種リストを保存
    out = OUT_DIR / "dpann_species_list.txt"
    with open(out, "w") as f:
        f.write("taxon\tspecies\tassemblies\n")
        for sp, info in sorted(all_species.items()):
            f.write(f"{info['taxon']}\t{sp}\t{info['genome_count']}\n")
    print(f"\nSpecies list saved → {out.name}")
    print("\nDone.")
