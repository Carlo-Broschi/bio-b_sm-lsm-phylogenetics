import re, sys
import dendropy
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

with open("/Users/carlobroschi_imac/Workspace/Research/Biology/bio-b_sm-lsm-phylogenetics/4-results/smlsm_tree_nr90_annotated.contree") as f:
    content = f.read()

tree_match = re.search(r'tree tree_1 = \[&R\] (.+);', content)
newick_str = re.sub(r'\[&[^\]]*\]', '', tree_match.group(1)).strip() + ";"

color_rules = [
    ('SmD1',    r'\|.*[Ss][Mm][Dd]1|\|.*SMD1|\|.*Sm-D1|\|.*KIAA0851|\|.*small_nuclear_riboprotein_Sm-D|\|.*Sm-D\b', '#457B9D'),
    ('SmD2',    r'\|.*[Ss][Mm][Dd]2|\|.*SMD2|\|.*Sm-D2|\|.*SMD2_',                '#7B2D8B'),
    ('SmD3',    r'\|.*[Ss][Mm][Dd]3|\|.*SMD3|\|.*Sm-D3|\|.*SMD3_|\|.*mRNA_splicing_protein_SMD3|\|.*pre-mRNA_splicing_factor|\|.*pre-mRNA_splicing_factor_puta', '#E040FB'),
    ('SmB',     r'\|.*[Ss]m[Bb]\b|\|.*RSMB|\|.*[Ss]mb1|\|.*Sm-B|\|.*RSMB_|\|.*Probable_small_nuclear_ribonuc.*elegans|\|.*small_nuclear_ribonucleoprotein_p.*7', '#1D3D8F'),
    ('SmE',     r'\|.*[Ss]m[Ee]\b|\|.*Sm-E|\|.*SME\b|\|.*Sme1|\|.*RUXE|\|.*snRNP.*[Xx]5|\|.*SMX5|\|.*snRNP_core.*[Xx]5', '#2D6A4F'),
    ('SmF',     r'\|.*[Ss]m[Ff]\b|\|.*Sm-F|\|.*SMF\b|\|.*RUXF|\|.*small_ribonucleoprotein_partic', '#74C69D'),
    ('SmG',     r'\|.*[Ss]m[Gg]\b|\|.*Sm-G|\|.*SMG\b|\|.*RUXG|\|.*putative_small_nuclear_ribonuc.*SmG', '#F9C74F'),
    ('Lsm8',    r'\|.*[Ll]sm8\b|\|.*LSM8\b|\|.*similar_to_U6_snRNA.*Lsm8|\|.*PREDICTED_similar_to_U6_snRNA',  '#6D4C41'),
    ('Lsm1-7',  r'\|.*[Ll]sm[1-7]\b|\|.*LSM[1-7]\b|\|.*[Ss]mx|\|.*SMX[0-9]'
                r'|\|.*LSM4_homolog|\|.*similar_to_Lsm4|\|.*PREDICTED_similar_to_Lsm4'
                r'|\|.*similar_to_LSM5|\|.*PREDICTED_similar_to_LSM5'
                r'|\|.*U6_snRNA_binding_protein'
                r'|\|.*snRNP_core.*[Oo][94]'
                r'|\|.*LSM_complex_subu'
                r'|\|.*U6-snRNA_ASSOCIATED'
                r'|\|.*U6_snRNA-ASSOCIATED'
                r'|\|.*SMALL_NUCLEAR_RIBONUCLEOPROTEI'  # Encephalitozoon Lsm
                r'|\|.*probable_U6_SNRNA'
                r'|\|.*u6_snRNA-associated_sm-like'
                r'|\|.*U6_snRNA_associated_Sm-like'
                r'|\|.*putative_snRNA_associated'
                r'|\|.*glycine_rich_protein_putative.*Crypto'  # Lsm4 in Crypto
                r'|\|.*small_nuclear_ribonuclear'
                r'|\|.*AAM29642|AAM29479|AAM29470|EAA00211|EAA00327'  # Drosophila/Anopheles Lsm
                r'|\|.*XP_394397|XP_625205|XP_484457|AAH81512|XP_312222'  # Sm metazoans
                r'|\|.*XP_416157|XP_919276|XP_418849|XP_917671|XP_418245|XP_624908|XP_318746|NP_001027236',  '#F4845F'),
    ('SmAP',    r'\|.*[Ss]n[Rr][Nn][Pp]|\|.*SmAP|\|.*[Ss]m.like|\|.*Sm_protein'
                r'|\|.*[Ss]mall_nuclear_ribonucleoprotei'
                r'|\|.*small_nucleolar_RNP'
                r'|\|.*[Ss]m_snRNP'
                r'|\|.*Like-Sm|\|.*like-Sm'
                r'|\|.*LSM_domain'
                r'|\|.*Lsm2-8'
                r'|\|.*NFRA_protein'
                r'|\|.*Small_nuclear_riboprotein_prot'  # Sulfolobus
                r'|\|.*90aa_long_hypothetical_small_n'  # Sulfolobus tokodaii
                r'|\|.*homolog_of_small_nuclear_ribon'  # Aeropyrum
                r'|\|.*ribonucleoprotein_putativ',                                 '#F4A261'),
    ('Hfq',     r'\|.*[Hh]fq|\|.*host.factor|\|.*[Nn]fr[Aa]|\|.*HF-I'
                r'|\|.*[Hh]ost_factor|\|.*COG1923'
                r'|\|.*putative_hfq|\|.*hfq_protein'
                r'|\|.*hypothetical_protein_lpl'
                r'|\|.*hypothetical_protein_TTE'
                r'|\|.*hypothetical_protein_ELI'
                r'|\|.*[Hh]ost_factor_I-like'
                r'|\|.*RNA-binding_protein_Hfq'
                r'|\|.*putative_RNA-binding_reg',                                  '#E63946'),
    # 残りの真核生物 hypothetical → Sm/Lsm unspecified
    ('Sm/Lsm\n(unspecified)', r'\|.*hypothetical_protein|\|.*unnamed_protein|\|.*conserved_hypothetical'
                r'|\|.*probable_small_nuclear|\|.*putative_small_nuclear'
                r'|\|.*[Ss]m-LIKE_PROTEIN'
                r'|\|.*Zgc103688|\|.*RH73529p|\|.*RE43665p|\|.*RE39820p'
                r'|\|.*DEHA2|\|.*ENSANGP|\|.*LD14049|\|.*AAC63620|\|.*AAW4'
                r'|\|.*EAA6|\|.*EAA0|\|.*CAC28|\|.*CAG8|\|.*CAG9|\|.*CAD2'
                r'|\|.*mRNA_processing|\|.*NrfA|\|.*AAB85915|\|.*NP_113',          '#AAAAAA'),
]

def get_color_label(name):
    for label, pattern, color in color_rules:
        if re.search(pattern, name):
            return color, label
    return '#888888', 'unknown'

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
    _, label = get_color_label(leaf.taxon.label)
    group_counts[label] = group_counts.get(label, 0) + 1

print("グループ数:")
for k, v in sorted(group_counts.items()):
    print(f"  {k}: {v}")
print(f"合計: {sum(group_counts.values())}")

fig, ax = plt.subplots(figsize=(12, n_tips * 0.075 + 2))
ax.set_axis_off()

def draw_node(node):
    x = get_dist(node) / max_dist if max_dist > 0 else 0
    y = get_y(node)
    if node.is_leaf():
        color, _ = get_color_label(node.taxon.label)
        ax.plot(x, y, 'o', color=color, markersize=4, zorder=3)
    for child in node.child_nodes():
        cx = get_dist(child) / max_dist
        cy = get_y(child)
        ax.plot([x, x], [y, cy], 'k-', lw=0.3, zorder=1)
        ax.plot([x, cx], [cy, cy], 'k-', lw=0.3, zorder=1)
        draw_node(child)

sys.setrecursionlimit(5000)
draw_node(tree.seed_node)

ordered = ['Hfq','SmAP','SmB','SmD1','SmD2','SmD3','SmE','SmF','SmG','Lsm1-7','Lsm8','Sm/Lsm\n(unspecified)','unknown']
legend_patches = []
color_map = {label: color for label, _, color in color_rules}
color_map['unknown'] = '#888888'
for lbl in ordered:
    n = group_counts.get(lbl, 0)
    if n > 0:
        legend_patches.append(mpatches.Patch(color=color_map[lbl], label=f"{lbl.replace(chr(10),' ')} (n={n})"))

ax.legend(handles=legend_patches, loc='lower right', fontsize=8, framealpha=0.9)
ax.set_title("Sm/Lsm superfamily — ML consensus tree (nr90, Q.PFAM+G4)", fontsize=11)

out = "/Users/carlobroschi_imac/Workspace/Research/Biology/bio-b_sm-lsm-phylogenetics/4-results/smlsm_tree_nr90_colored.png"
plt.savefig(out, dpi=150, bbox_inches='tight')
print(f"出力: {out}")
