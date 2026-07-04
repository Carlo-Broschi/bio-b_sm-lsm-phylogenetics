"""
bio-b: curated 木の tip を Sm/Lsm 型で色分けするための accession -> カテゴリ マップ。
記述(protein name)と生物名(archaea 判定)から分類する。
カテゴリ: Hfq(細菌) / SmAP(古細菌 Sm) / Lsm(真核) / Sm-core(真核 SmB/D/E/F/G) / Other
出力: 4-results/biob_tip_types.tsv （accession, category, organism, description）
"""
import re
from pathlib import Path

BASE = Path(__file__).resolve().parents[1].parent  # scripts/analytics -> project? adjust below
BASE = Path(__file__).resolve().parents[2]
ALN = BASE / "3-analysis" / "smlsm_curated_aln_nr90_trim.fasta"
OUT = BASE / "4-results" / "biob_tip_types.tsv"

ARCHAEA = re.compile(
    r"sulfolob|nanoarch|archaeoglob|methano|pyrobaculum|pyrococc|thermoproteus|"
    r"halo(bacter|ferax|arcula|coccus)|thermoplasma|ferroplasma|acidianus|"
    r"saccharolobus|aeropyrum|ignicoccus|thermococc|archaeon|haloarch|"
    r"picrophilus|thermofilum|caldivirga|vulcanisaeta|metallosphaera|"
    r"candidatus.*archae", re.I)


def classify(desc, org):
    d = desc.lower()
    if "hfq" in d:
        return "Hfq"
    if ARCHAEA.search(org) or "archaeal" in d or "smap" in d:
        return "SmAP (archaea)"
    if re.search(r"lsm|u6 snrna|u6-snrna|u6_snrna", d):
        return "Lsm (eukaryote)"
    if re.search(r"\bsm[- ]?[bdefg]\b|smd[123]|sm-d|core protein|ruxe|ruxf|ruxg|"
                 r"snrnp|small nuclear|ribonucleoprotein|splicing|sm protein|"
                 r"sm-like|like-sm|snorp|small nucleolar rnp", d):
        return "Sm-core (eukaryote)"
    return "Other"


def main():
    rows = []
    cat_count = {}
    for line in ALN.open():
        if not line.startswith(">"):
            continue
        acc = line[1:].split()[0]
        m = re.match(r">?\S+\s+(.*?)(?:\s+\[(.+?)\])?\s*$", line.rstrip("\n"))
        desc = m.group(1) if m else ""
        org = m.group(2) if m and m.group(2) else ""
        cat = classify(desc, org)
        cat_count[cat] = cat_count.get(cat, 0) + 1
        rows.append((acc, cat, org, desc))

    OUT.write_text("accession\tcategory\torganism\tdescription\n"
                   + "".join(f"{a}\t{c}\t{o}\t{d}\n" for a, c, o, d in rows))
    print(f"{len(rows)} tips -> {OUT}")
    for c, n in sorted(cat_count.items(), key=lambda x: -x[1]):
        print(f"  {c}: {n}")


if __name__ == "__main__":
    main()
