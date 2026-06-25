import re, sys
import dendropy
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

BIO_B = "/Users/carlobroschi_imac/Workspace/Research/Biology/bio-b_sm-lsm-phylogenetics"

# smlsm_all.fasta から acc → description (lowercase)
acc2desc = {}
with open(f"{BIO_B}/1-downloaded-data/smlsm_all.fasta") as f:
    for line in f:
        if line.startswith(">"):
            parts = line[1:].rstrip().split(None, 1)
            acc2desc[parts[0]] = parts[1].lower() if len(parts) > 1 else ""

def get_category(acc):
    desc = acc2desc.get(acc.replace(" ", "_"), "")
    if re.search(r'\bhfq\b|rna chaperone hfq|host factor for|hf-i', desc):
        return 'Hfq', '#E63946'
    if re.search(r"\bsmd1\b|sm-d1\b|snrnpd1\b|small nuclear.*sm-d\b|mrna splicing protein smd1", desc):
        return 'SmD1', '#457B9D'
    if re.search(r"\bsmd2\b|sm-d2\b|snrnpd2\b|mrna splicing protein smd2", desc):
        return 'SmD2', '#7B2D8B'
    if re.search(r"\bsmd3\b|sm-d3\b|snrnpd3\b|mrna splicing protein smd3", desc):
        return 'SmD3', '#E040FB'
    if re.search(r'\bsmb\b|sm-b\b|snrnpb\b|\brsmb\b', desc):
        return 'SmB', '#1D3D8F'
    if re.search(r'\bsme\b|sm-e\b|snrnpe\b|\bsmx5\b|snrnp.*x5\b', desc):
        return 'SmE', '#2D6A4F'
    if re.search(r'\bsmf\b|sm-f\b|snrnpf\b|\bruxf\b', desc):
        return 'SmF', '#74C69D'
    if re.search(r'\bsmg\b|sm-g\b|snrnpg\b|\bruxg\b', desc):
        return 'SmG', '#F9C74F'
    if re.search(r'\blsm8\b', desc):
        return 'Lsm8', '#6D4C41'
    if re.search(r'\blsm[1-7]\b|u6 snrna.assoc|u6-snrna|lsm complex|u6 snrnp', desc):
        return 'Lsm1-7', '#F4845F'
    if re.search(r'mrna splicing protein', desc): return 'SmD1', '#457B9D'
    if re.search(r'snrnp|sm.like|sm protein\b|small nuclear ribonucleoprot|like-sm|lsm domain'
                 r'|small nuclear riboprotein|archaeal sm|smap\b', desc):
        return 'SmAP', '#F4A261'
    if re.search(r'small acidic protein|bromodomain|kinesin.assoc|kap-3|sterile alpha motif|smaug|hmg.domain|hmg-box|stromal membrane|thymidine kinase|nac .no apical|defensin|rna polymerase|mannan-binding|no-on-and-no-off|uncharacterized protein.*dmel|uncharacterized protein.*aco1|uncharacterized protein.*fob|uncharacterized protein.*kq6', desc):
        return 'contaminant', '#CCCCCC'
    return 'unknown', '#888888'

sys.setrecursionlimit(10000)

with open(f"{BIO_B}/4-results/smlsm_tree_full_nr70.contree") as f:
    newick_str = f.read().strip()
if not newick_str.endswith(";"):
    newick_str += ";"

tree = dendropy.Tree.get(data=newick_str, schema="newick")
leaves = list(tree.leaf_node_iter())
y_map = {n: i for i, n in enumerate(leaves)}
n_tips = len(leaves)

def get_dist(node):
    d, n = 0.0, node
    while n.parent_node is not None:
        d += n.edge.length or 0.0
        n = n.parent_node
    return d

max_dist = max(get_dist(n) for n in leaves)

def get_y(node):
    if node.is_leaf():
        return y_map[node]
    ys = [get_y(c) for c in node.child_nodes()]
    return sum(ys) / len(ys)

group_counts = {}
for leaf in leaves:
    cat, _ = get_category(leaf.taxon.label)
    group_counts[cat] = group_counts.get(cat, 0) + 1

print("グループ数:")
for k, v in sorted(group_counts.items(), key=lambda x: -x[1]):
    print(f"  {k}: {v}")
print(f"合計: {sum(group_counts.values())}")

fig, ax = plt.subplots(figsize=(12, n_tips * 0.075 + 2))
ax.set_axis_off()

def draw_node(node):
    x = get_dist(node) / max_dist if max_dist > 0 else 0
    y = get_y(node)
    if node.is_leaf():
        _, color = get_category(node.taxon.label)
        ax.plot(x, y, 'o', color=color, markersize=4, zorder=3)
    for child in node.child_nodes():
        cx = get_dist(child) / max_dist
        cy = get_y(child)
        ax.plot([x, x], [y, cy], 'k-', lw=0.3, zorder=1)
        ax.plot([x, cx], [cy, cy], 'k-', lw=0.3, zorder=1)
        draw_node(child)

draw_node(tree.seed_node)

ordered = [
    ('Hfq', '#E63946'), ('SmAP', '#F4A261'), ('SmB', '#1D3D8F'),
    ('SmD1', '#457B9D'), ('SmD2', '#7B2D8B'), ('SmD3', '#E040FB'),
    ('SmE', '#2D6A4F'), ('SmF', '#74C69D'), ('SmG', '#F9C74F'),
    ('Lsm1-7', '#F4845F'), ('Lsm8', '#6D4C41'),
    ('contaminant', '#CCCCCC'), ('unknown', '#888888'),
]
legend_patches = [
    mpatches.Patch(color=c, label=f"{lbl} (n={group_counts.get(lbl,0)})")
    for lbl, c in ordered if group_counts.get(lbl, 0) > 0
]
ax.legend(handles=legend_patches, loc='lower right', fontsize=8, framealpha=0.9)
ax.set_title("Sm/Lsm superfamily — ML consensus tree (nr70, VT+G4, 541 taxa)", fontsize=11)

out = f"{BIO_B}/4-results/smlsm_tree_full_nr70_colored.png"
plt.savefig(out, dpi=150, bbox_inches='tight')
print(f"出力: {out}")
