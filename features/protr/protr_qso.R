library(protr)


# 读取FASTA文件
test_fasta <- readFASTA(fasta_file)

# 创建一个空列表来存储每次的结果
feature_list <- list()

# 创建进度条
n <- length(test_fasta)  # 获取序列的总数
pb <- txtProgressBar(min = 0, max = n, style = 3)  # 进度条初始化

# 循环遍历 test_fasta，并将每次的结果保存到 feature_list 中
for (i in seq_along(test_fasta)) {
  seq <- test_fasta[[i]]

  res <- tryCatch({
    extractQSO(seq)
  }, error = function(e) {
    # 如果出错，返回一个全 NA 的向量，列数与 extractQSO 的正常输出一致
    as.numeric(rep(NA, 100))
  })

  feature_list <- append(feature_list, list(res))
  
  # 更新进度条
  setTxtProgressBar(pb, i)
}

# 关闭进度条
close(pb)

# 将列表转换为数据框，其中每一行代表一个序列的特征结果
if (length(feature_list) == 1) {
  # 将唯一的向量转置成 1行数据框，并保留原有的列名
  res_df <- as.data.frame(t(feature_list[[1]]))
} else {
  res_df <- as.data.frame(do.call(rbind, feature_list))
}

colnames(res_df) <- c('Schneider.Xr.A', 'Schneider.Xr.R', 'Schneider.Xr.N', 'Schneider.Xr.D', 'Schneider.Xr.C', 'Schneider.Xr.E', 'Schneider.Xr.Q', 'Schneider.Xr.G', 'Schneider.Xr.H', 'Schneider.Xr.I', 'Schneider.Xr.L', 'Schneider.Xr.K', 'Schneider.Xr.M', 'Schneider.Xr.F', 'Schneider.Xr.P', 'Schneider.Xr.S', 'Schneider.Xr.T', 'Schneider.Xr.W', 'Schneider.Xr.Y', 'Schneider.Xr.V', 'Grantham.Xr.A', 'Grantham.Xr.R', 'Grantham.Xr.N', 'Grantham.Xr.D', 'Grantham.Xr.C', 'Grantham.Xr.E', 'Grantham.Xr.Q', 'Grantham.Xr.G', 'Grantham.Xr.H', 'Grantham.Xr.I', 'Grantham.Xr.L', 'Grantham.Xr.K', 'Grantham.Xr.M', 'Grantham.Xr.F', 'Grantham.Xr.P', 'Grantham.Xr.S', 'Grantham.Xr.T', 'Grantham.Xr.W', 'Grantham.Xr.Y', 'Grantham.Xr.V', 'Schneider.Xd.1', 'Schneider.Xd.2', 'Schneider.Xd.3', 'Schneider.Xd.4', 'Schneider.Xd.5', 'Schneider.Xd.6', 'Schneider.Xd.7', 'Schneider.Xd.8', 'Schneider.Xd.9', 'Schneider.Xd.10', 'Schneider.Xd.11', 'Schneider.Xd.12', 'Schneider.Xd.13', 'Schneider.Xd.14', 'Schneider.Xd.15', 'Schneider.Xd.16', 'Schneider.Xd.17', 'Schneider.Xd.18', 'Schneider.Xd.19', 'Schneider.Xd.20', 'Schneider.Xd.21', 'Schneider.Xd.22', 'Schneider.Xd.23', 'Schneider.Xd.24', 'Schneider.Xd.25', 'Schneider.Xd.26', 'Schneider.Xd.27', 'Schneider.Xd.28', 'Schneider.Xd.29', 'Schneider.Xd.30', 'Grantham.Xd.1', 'Grantham.Xd.2', 'Grantham.Xd.3', 'Grantham.Xd.4', 'Grantham.Xd.5', 'Grantham.Xd.6', 'Grantham.Xd.7', 'Grantham.Xd.8', 'Grantham.Xd.9', 'Grantham.Xd.10', 'Grantham.Xd.11', 'Grantham.Xd.12', 'Grantham.Xd.13', 'Grantham.Xd.14', 'Grantham.Xd.15', 'Grantham.Xd.16', 'Grantham.Xd.17', 'Grantham.Xd.18', 'Grantham.Xd.19', 'Grantham.Xd.20', 'Grantham.Xd.21', 'Grantham.Xd.22', 'Grantham.Xd.23', 'Grantham.Xd.24', 'Grantham.Xd.25', 'Grantham.Xd.26', 'Grantham.Xd.27', 'Grantham.Xd.28', 'Grantham.Xd.29', 'Grantham.Xd.30')

# 筛选
selected_cols <- res_df[, c("Schneider.Xd.28", "Schneider.Xd.27")]
selected_cols