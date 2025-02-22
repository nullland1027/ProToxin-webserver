library(protr)

# 读取FASTA文件
test_fasta <- readFASTA(fasta_file)

# 创建一个空列表来存储每次的结果
res_list <- list()

# 创建进度条
n <- length(test_fasta)  # 获取序列的总数
pb <- txtProgressBar(min = 0, max = n, style = 3)  # 进度条初始化

# 循环遍历 test_fasta，并将每次的结果保存到 res_list 中
for (i in seq_along(test_fasta)) {
  seq <- test_fasta[[i]]
  res <- tryCatch({
    extractAPAAC(seq)
  }, error = function(e) {
    # 如果出错，返回一个全 NA 的向量，列数与 extractAPAAC 的正常输出一致
    as.numeric(rep(NA, 80))
  })

  res_list <- append(res_list, list(res))
  setTxtProgressBar(pb, i)
}
close(pb)

if (length(res_list) == 1) {
  # 将唯一的向量转置成 1行数据框，并保留原有的列名
  res_df <- as.data.frame(t(res_list[[1]]))
} else {
  res_df <- as.data.frame(do.call(rbind, res_list))
}

colnames(res_df) <- c('Pc1.A', 'Pc1.R', 'Pc1.N', 'Pc1.D', 'Pc1.C', 'Pc1.E', 'Pc1.Q', 'Pc1.G', 'Pc1.H', 'Pc1.I', 'Pc1.L', 'Pc1.K', 'Pc1.M', 'Pc1.F', 'Pc1.P', 'Pc1.S', 'Pc1.T', 'Pc1.W', 'Pc1.Y', 'Pc1.V', 'Pc2.Hydrophobicity.1', 'Pc2.Hydrophilicity.1', 'Pc2.Hydrophobicity.2', 'Pc2.Hydrophilicity.2', 'Pc2.Hydrophobicity.3', 'Pc2.Hydrophilicity.3', 'Pc2.Hydrophobicity.4', 'Pc2.Hydrophilicity.4', 'Pc2.Hydrophobicity.5', 'Pc2.Hydrophilicity.5', 'Pc2.Hydrophobicity.6', 'Pc2.Hydrophilicity.6', 'Pc2.Hydrophobicity.7', 'Pc2.Hydrophilicity.7', 'Pc2.Hydrophobicity.8', 'Pc2.Hydrophilicity.8', 'Pc2.Hydrophobicity.9', 'Pc2.Hydrophilicity.9', 'Pc2.Hydrophobicity.10', 'Pc2.Hydrophilicity.10', 'Pc2.Hydrophobicity.11', 'Pc2.Hydrophilicity.11', 'Pc2.Hydrophobicity.12', 'Pc2.Hydrophilicity.12', 'Pc2.Hydrophobicity.13', 'Pc2.Hydrophilicity.13', 'Pc2.Hydrophobicity.14', 'Pc2.Hydrophilicity.14', 'Pc2.Hydrophobicity.15', 'Pc2.Hydrophilicity.15', 'Pc2.Hydrophobicity.16', 'Pc2.Hydrophilicity.16', 'Pc2.Hydrophobicity.17', 'Pc2.Hydrophilicity.17', 'Pc2.Hydrophobicity.18', 'Pc2.Hydrophilicity.18', 'Pc2.Hydrophobicity.19', 'Pc2.Hydrophilicity.19', 'Pc2.Hydrophobicity.20', 'Pc2.Hydrophilicity.20', 'Pc2.Hydrophobicity.21', 'Pc2.Hydrophilicity.21', 'Pc2.Hydrophobicity.22', 'Pc2.Hydrophilicity.22', 'Pc2.Hydrophobicity.23', 'Pc2.Hydrophilicity.23', 'Pc2.Hydrophobicity.24', 'Pc2.Hydrophilicity.24', 'Pc2.Hydrophobicity.25', 'Pc2.Hydrophilicity.25', 'Pc2.Hydrophobicity.26', 'Pc2.Hydrophilicity.26', 'Pc2.Hydrophobicity.27', 'Pc2.Hydrophilicity.27', 'Pc2.Hydrophobicity.28', 'Pc2.Hydrophilicity.28', 'Pc2.Hydrophobicity.29', 'Pc2.Hydrophilicity.29', 'Pc2.Hydrophobicity.30', 'Pc2.Hydrophilicity.30')

selected_cols <- res_df[, c("Pc1.N", "Pc1.A", "Pc1.C")]  # 筛选
selected_cols
