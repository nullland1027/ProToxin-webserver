# 加载所需的包
library(protr)

# 定义你的变量和路径
file_path <- "/Users/zhanghaohan/code/Group_protein_toxin/mine/data/sequences/final_TRAIN/v4/neg_train_all.fasta"

# 读取FASTA文件
test_fasta <- readFASTA(file_path)

# 创建一个空列表来存储每次的结果
feature_list <- list()

# 创建进度条
n <- length(test_fasta)  # 获取序列的总数
pb <- txtProgressBar(min = 0, max = n, style = 3)  # 进度条初始化

# 循环遍历 test_fasta，并将每次的结果保存到 feature_list 中
for (i in seq_along(test_fasta)) {
  seq <- test_fasta[[i]]
  feature_list <- append(feature_list, list(extractAPAAC(seq)))
  
  # 更新进度条
  setTxtProgressBar(pb, i)
}

# 关闭进度条
close(pb)

# 将列表转换为数据框，其中每一行代表一个序列的特征结果
df <- do.call(rbind, feature_list)

# 筛选
selected_cols <- df[, c("Pc1.N", "Pc1.A", "Pc1.C")]

# 将数据框写入CSV文件
result_filename <- "neg_apaac_3_all.csv"
write.csv(selected_cols, result_filename, row.names = FALSE)

# 提示保存完成
cat(sprintf("AAC results have been saved to '%s'.", result_filename))