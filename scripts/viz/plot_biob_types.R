#!/usr/bin/env Rscript
# bio-b: curated ML 木(1097 tips) を Sm/Lsm 型で色分けし、主要クレードの分離を評価。
# カテゴリ: Hfq(細菌) / SmAP(古細菌) / Lsm(真核) / Sm-core(真核) / Other
# 出力: 4-results/smlsm_curated_types.{pdf,png}

suppressMessages({ library(ggtree); library(ggplot2); library(ape) })

BASE <- normalizePath(file.path(dirname(sub("--file=", "",
        commandArgs(FALSE)[grep("--file=", commandArgs(FALSE))])), "..", ".."))
if (length(BASE) == 0 || is.na(BASE)) BASE <- getwd()

tr <- read.tree(file.path(BASE, "4-results", "smlsm_tree_curated_nr90.treefile"))
types <- read.delim(file.path(BASE, "4-results", "biob_tip_types.tsv"),
                    stringsAsFactors = FALSE)
acc2cat <- setNames(types$category, types$accession)

cat_vec <- ifelse(tr$tip.label %in% names(acc2cat), acc2cat[tr$tip.label], "Other")
tipdf <- data.frame(node = seq_along(tr$tip.label), category = cat_vec)
cat("tip カテゴリ内訳:\n"); print(sort(table(cat_vec), decreasing = TRUE))

cols <- c("Hfq" = "#E15759", "SmAP (archaea)" = "#4E79A7",
          "Lsm (eukaryote)" = "#59A14F", "Sm-core (eukaryote)" = "#F28E2B",
          "Other" = "grey70")

# fan レイアウトで 1097 tips をコンパクトに
p <- ggtree(tr, layout = "fan", open.angle = 12, linewidth = 0.15) %<+% tipdf +
  geom_tippoint(aes(color = category), size = 0.6, na.rm = TRUE) +
  scale_color_manual(values = cols, name = "Sm/Lsm type", na.translate = FALSE) +
  ggtitle("bio-b curated ML tree (1097 tips) colored by Sm/Lsm type") +
  theme(legend.position = "right", plot.title = element_text(size = 11),
        legend.text = element_text(size = 9))

ggsave(file.path(BASE, "4-results", "smlsm_curated_types.pdf"), p,
       width = 11, height = 11, limitsize = FALSE)
ggsave(file.path(BASE, "4-results", "smlsm_curated_types.png"), p,
       width = 11, height = 11, dpi = 150, limitsize = FALSE)
cat("保存: 4-results/smlsm_curated_types.{pdf,png}\n")
