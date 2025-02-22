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
  res_list <- append(res_list, list(extractAAC(seq)))
  setTxtProgressBar(pb, i)
}
close(pb)

if (length(res_list) == 1) {
  # 将唯一的向量转置成 1行数据框，并保留原有的列名
  res_df <- as.data.frame(t(res_list[[1]]))
} else {
  res_df <- as.data.frame(do.call(rbind, res_list))
}

selected_cols <- res_df[, c("C", "Q")]  # 筛选
selected_cols
