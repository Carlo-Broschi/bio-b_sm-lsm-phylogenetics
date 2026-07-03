"""
DPANN/Asgard プロテオームに PF01423(LSM)+PF17209(Hfq) を hmmsearch し、
Sm フォールドの分布を「型判定つき」で集計する（design_from_literature.md §3）。

型判定：各ヒット配列について PF01423 と PF17209 のビットスコアを比較し、
高い方を型とする（Sm/Lsm型 vs Hfq型）。→ Nielsen 2007 の「古細菌に Hfq型が
混在するか」を genome ごとに判定。

集計は2粒度：
- genome-level：genome あたりのコピー数・型
- species-level：over-sequencing バイアス中和のため organism_name で畳む

出力：
- 3-analysis/hmm/hits_all.tsv          全ヒット（taxon,accession,species,protein,best_model,score_lsm,score_hfq,type)
- 3-analysis/hmm/census_genome.tsv     genome 別 集計
- 3-analysis/hmm/census_species.tsv    種 別 集計
- 3-analysis/hmm/census_lineage.tsv    系統別サマリ（評価可能/データ不足の別）
- 3-analysis/hmm/smfold_hits.faa       ヒット配列（§2 構造ガイド MSA / §1 ツリー投入用）
"""
import subprocess
import sys
from collections import defaultdict
from pathlib import Path

BASE = Path(__file__).resolve().parents[2]
PROT_DIR = BASE / "1-downloaded-data" / "proteomes"
MANIFEST = BASE / "1-downloaded-data" / "dpann_asgard_manifest.tsv"
HMM_DIR = BASE / "3-analysis" / "hmm"
LSM = HMM_DIR / "PF01423.hmm"
HFQ = HMM_DIR / "PF17209.hmm"


def load_manifest():
    """accession -> (taxon, species, completeness, contamination)"""
    m = {}
    if not MANIFEST.exists():
        return m
    with MANIFEST.open() as f:
        next(f)
        for line in f:
            p = line.rstrip("\n").split("\t")
            if len(p) >= 7:
                m[p[2]] = {"taxon": p[0], "species": p[1],
                           "completeness": p[3], "contamination": p[4],
                           "source": p[5], "n_proteins": p[6]}
    return m


def run_hmm(hmm, target):
    """hmmsearch --cut_ga、domtbl から best-domain スコアを protein -> score で返す。"""
    tbl = HMM_DIR / f"_tmp_{hmm.stem}.domtbl"
    subprocess.run(["hmmsearch", "--cut_ga", "--domtblout", str(tbl),
                    "-o", "/dev/null", str(hmm), str(target)], check=True)
    scores = {}
    with tbl.open() as f:
        for line in f:
            if line.startswith("#"):
                continue
            c = line.split()
            name = c[0]                 # target name（taxon|acc|protein...）
            dom_score = float(c[13])    # domain bit score
            scores[name] = max(scores.get(name, -1e9), dom_score)
    tbl.unlink(missing_ok=True)
    return scores


def read_seqs(target):
    seqs = {}
    h = None
    buf = []
    for line in target.open():
        if line.startswith(">"):
            if h:
                seqs[h] = "".join(buf)
            h = line[1:].split()[0]
            buf = []
        else:
            buf.append(line.strip())
    if h:
        seqs[h] = "".join(buf)
    return seqs


def main():
    man = load_manifest()
    faas = sorted(PROT_DIR.glob("*.faa"))
    if not faas:
        sys.exit("proteomes/*.faa がありません。先に取得スクリプトを実行してください。")

    # 全プロテオームを1本に結合（ヘッダは taxon|acc|protein... 形式）
    combined = HMM_DIR / "_all_proteomes.faa"
    with combined.open("w") as out:
        for fa in faas:
            out.write(fa.read_text())

    lsm_sc = run_hmm(LSM, combined)
    hfq_sc = run_hmm(HFQ, combined)
    seqs = read_seqs(combined)
    hit_names = set(lsm_sc) | set(hfq_sc)

    hits = []
    for name in hit_names:
        parts = name.split("|")
        taxon = parts[0] if len(parts) > 0 else ""
        acc = parts[1] if len(parts) > 1 else ""
        sl = lsm_sc.get(name, 0.0)
        sh = hfq_sc.get(name, 0.0)
        typ = "Sm/Lsm" if sl >= sh else "Hfq"
        species = man.get(acc, {}).get("species", "")
        hits.append({"taxon": taxon, "acc": acc, "species": species,
                     "protein": name, "score_lsm": sl, "score_hfq": sh,
                     "type": typ})

    HMM_DIR.mkdir(exist_ok=True)
    with (HMM_DIR / "hits_all.tsv").open("w") as f:
        f.write("taxon\taccession\tspecies\tprotein\tbest_model\tscore_lsm\tscore_hfq\ttype\n")
        for h in sorted(hits, key=lambda d: (d["taxon"], d["acc"])):
            best = "PF01423" if h["type"] == "Sm/Lsm" else "PF17209"
            f.write(f"{h['taxon']}\t{h['acc']}\t{h['species']}\t{h['protein']}\t"
                    f"{best}\t{h['score_lsm']:.1f}\t{h['score_hfq']:.1f}\t{h['type']}\n")

    # genome 別集計
    g_sm = defaultdict(int)
    g_hfq = defaultdict(int)
    for h in hits:
        (g_sm if h["type"] == "Sm/Lsm" else g_hfq)[h["acc"]] += 1
    with (HMM_DIR / "census_genome.tsv").open("w") as f:
        f.write("accession\ttaxon\tspecies\tcompleteness\tn_SmLsm\tn_Hfq\n")
        for acc, meta in sorted(man.items(), key=lambda kv: (kv[1]["taxon"], kv[0])):
            f.write(f"{acc}\t{meta['taxon']}\t{meta['species']}\t"
                    f"{meta['completeness']}\t{g_sm.get(acc,0)}\t{g_hfq.get(acc,0)}\n")

    # species 別集計（over-sequencing 中和：型の有無を種単位で）
    sp_tax = {}
    sp_sm = defaultdict(int)
    sp_hfq = defaultdict(int)
    sp_ng = defaultdict(set)
    for acc, meta in man.items():
        sp = meta["species"]
        sp_tax[sp] = meta["taxon"]
        sp_ng[sp].add(acc)
    for h in hits:
        sp = h["species"]
        (sp_sm if h["type"] == "Sm/Lsm" else sp_hfq)[sp] += 1
    with (HMM_DIR / "census_species.tsv").open("w") as f:
        f.write("species\ttaxon\tn_genomes\thas_SmLsm\thas_Hfq\ttotal_SmLsm_hits\ttotal_Hfq_hits\n")
        for sp in sorted(sp_tax, key=lambda s: (sp_tax[s], s)):
            if not sp:
                continue
            f.write(f"{sp}\t{sp_tax[sp]}\t{len(sp_ng[sp])}\t"
                    f"{'Y' if sp_sm.get(sp) else 'N'}\t{'Y' if sp_hfq.get(sp) else 'N'}\t"
                    f"{sp_sm.get(sp,0)}\t{sp_hfq.get(sp,0)}\n")

    # 系統別サマリ（評価可能性つき）
    lin_g = defaultdict(set)
    lin_sp = defaultdict(set)
    lin_sm_g = defaultdict(set)
    lin_hfq_g = defaultdict(set)
    for acc, meta in man.items():
        lin_g[meta["taxon"]].add(acc)
        if meta["species"]:
            lin_sp[meta["taxon"]].add(meta["species"])
    for h in hits:
        (lin_sm_g if h["type"] == "Sm/Lsm" else lin_hfq_g)[h["taxon"]].add(h["acc"])
    with (HMM_DIR / "census_lineage.tsv").open("w") as f:
        f.write("taxon\tn_genomes\tn_species\tgenomes_with_SmLsm\tgenomes_with_Hfq\tassessable\n")
        for tax in sorted(lin_g):
            ng = len(lin_g[tax])
            assess = "yes" if ng >= 1 else "no_data"
            f.write(f"{tax}\t{ng}\t{len(lin_sp[tax])}\t"
                    f"{len(lin_sm_g[tax])}\t{len(lin_hfq_g[tax])}\t{assess}\n")

    # ヒット配列を書き出し（§2/§1 用）
    with (HMM_DIR / "smfold_hits.faa").open("w") as f:
        for h in sorted(hits, key=lambda d: d["protein"]):
            f.write(f">{h['protein']} type={h['type']}\n{seqs.get(h['protein'],'')}\n")

    combined.unlink(missing_ok=True)
    print(f"総ヒット {len(hits)}  (Sm/Lsm {sum(1 for h in hits if h['type']=='Sm/Lsm')}, "
          f"Hfq {sum(1 for h in hits if h['type']=='Hfq')})")
    print(f"→ {HMM_DIR}/hits_all.tsv, census_genome/species/lineage.tsv, smfold_hits.faa")


if __name__ == "__main__":
    main()
