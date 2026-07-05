#!/usr/bin/env Rscript
# bio-b: curated ML 木(1097 tips) を Sm/Lsm 型で色分けし、主要クレードの分離を評価。
# カテゴリ: Hfq(細菌) / SmAP(古細菌) / Lsm(真核) / Sm-core(真核) / Other
# 出力: 4-results/smlsm_structguided_types.{pdf,png}

suppressMessages({ library(ggtree); library(ggplot2); library(ape) })

BASE <- normalizePath(file.path(dirname(sub("--file=", "",
        commandArgs(FALSE)[grep("--file=", commandArgs(FALSE))])), "..", ".."))
if (length(BASE) == 0 || is.na(BASE)) BASE <- getwd()

tr <- read.tree(file.path(BASE, "4-results", "smlsm_tree_structguided.treefile"))
types <- read.delim(file.path(BASE, "4-results", "biob_tip_types.tsv"),
                    stringsAsFactors = FALSE)
acc2cat <- setNames(types$category, types$accession)

cat_vec <- ifelse(tr$tip.label %in% names(acc2cat), acc2cat[tr$tip.label], "Other")
tipdf <- data.frame(node = seq_along(tr$tip.label), category = cat_vec)
cat("tip カテゴリ内訳:\n"); print(sort(table(cat_vec), decreasing = TRUE))

# 色覚バリアフリー（Okabe-Ito）：Hfq=vermillion / Lsm=blue は全 CVD 型で判別可
cols <- c("Hfq" = "#D55E00", "SmAP (archaea)" = "#CC79A7",
          "Lsm (eukaryote)" = "#0072B2", "Sm-core (eukaryote)" = "#E69F00",
          "Other" = "grey55")

# fan レイアウト。タイトルは図に焼き込まず caption に置く。余白を詰める。
p <- ggtree(tr, layout = "fan", open.angle = 12, linewidth = 0.15) %<+% tipdf +
  geom_tippoint(aes(color = category), size = 0.9, na.rm = TRUE) +
  scale_color_manual(values = cols, name = "Sm/Lsm fold type", na.translate = FALSE) +
  guides(color = guide_legend(override.aes = list(size = 3))) +
  theme(legend.position = c(0.5, 0.5),
        legend.title = element_text(size = 13, face = "bold"),
        legend.text = element_text(size = 11),
        legend.background = element_rect(fill = "white", color = "grey40", linewidth = 0.4),
        plot.margin = margin(-30, -30, -30, -30))

ggsave(file.path(BASE, "4-results", "smlsm_structguided_types.pdf"), p,
       width = 9, height = 9, limitsize = FALSE)
ggsave(file.path(BASE, "4-results", "smlsm_structguided_types.png"), p,
       width = 9, height = 9, dpi = 300, limitsize = FALSE)
cat("保存: 4-results/smlsm_structguided_types.{pdf,png}\n")
