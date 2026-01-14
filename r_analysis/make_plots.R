# This file contains small helper functions for plotting DESeq2 results.
# Keeping plots here makes the main analysis script easier to read.

make_volcano_plot <- function(df, out_path) {
  png(out_path)

  plot(
    df$log2FoldChange,
    -log10(df$pvalue),
    pch = 16,
    main = "Volcano Plot",
    xlab = "Log2 Fold Change",
    ylab = "-log10(p-value)"
  )

  dev.off()
}

make_heatmap <- function(matrix_data, out_path) {
  png(out_path)

  heatmap(
    as.matrix(matrix_data),
    main = "Gene Expression Heatmap",
    scale = "row"
  )

  dev.off()
}
