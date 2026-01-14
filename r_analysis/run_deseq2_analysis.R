# This R script is called by Python.
# For now, it makes a DESeq2-like output file so the pipeline works end-to-end.
# Later, I am gonna replace this with real DESeq2 analysis.

args <- commandArgs(trailingOnly = TRUE)

getArg <- function(flag) {
  idx <- which(args == flag)
  if (length(idx) == 0) stop(paste("Missing flag:", flag))
  args[idx + 1]
}

counts_path <- getArg("--counts")
meta_path   <- getArg("--meta")
out_dir     <- getArg("--out")

dir.create(out_dir, recursive = TRUE, showWarnings = FALSE)

counts <- read.csv(counts_path, check.names = FALSE)
meta   <- read.csv(meta_path, check.names = FALSE)

# Basic setup
gene_ids <- counts$gene_id
sample_cols <- setdiff(colnames(counts), "gene_id")

# Find which samples belong to each condition
conditions <- unique(meta$condition)
control_samples <- meta$sample_id[meta$condition == conditions[1]]
disease_samples <- meta$sample_id[meta$condition == conditions[2]]

# Make sure samples exist in counts
control_samples <- intersect(control_samples, sample_cols)
disease_samples <- intersect(disease_samples, sample_cols)

# Simple “difference” logic just for wiring (NOT real DESeq2)
control_means <- rowMeans(counts[, control_samples, drop=FALSE])
disease_means <- rowMeans(counts[, disease_samples, drop=FALSE])

log2fc <- log2((disease_means + 1) / (control_means + 1))

# Fake p-values for now
pvalue <- rep(0.5, length(gene_ids))
padj <- rep(0.5, length(gene_ids))

results <- data.frame(
  gene_id = gene_ids,
  log2FoldChange = log2fc,
  pvalue = pvalue,
  padj = padj
)

# Sort so the “top genes” are the largest changes
results <- results[order(abs(results$log2FoldChange), decreasing = TRUE), ]

write.csv(results, file.path(out_dir, "deseq2_results.csv"), row.names = FALSE)

# Make placeholder images
png(file.path(out_dir, "volcano_plot.png"))
plot(1, 1, main="Placeholder Volcano Plot")
dev.off()

png(file.path(out_dir, "heatmap.png"))
plot(1, 1, main="Placeholder Heatmap")
dev.off()

# Session info
sink(file.path(out_dir, "r_session_info.txt"))
sessionInfo()
sink()
