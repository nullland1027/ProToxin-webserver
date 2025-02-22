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
  feature_list <- append(feature_list, list(extractGeary(seq)))
  
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

# 筛选
selected_cols <- res_df[, c("CIDH920105.lag1")]
selected_cols