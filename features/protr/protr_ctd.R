# 加载所需的包
library(protr)

# 读取FASTA文件
test_fasta <- readFASTA(fasta_file)

# 创建一个空列表来存储每次的结果
feature_list_c <- list()
feature_list_t <- list()
feature_list_d <- list()

# 创建进度条
n <- length(test_fasta)  # 获取序列的总数
pb <- txtProgressBar(min = 0, max = n, style = 3)  # 进度条初始化

# 循环遍历 test_fasta，并将每次的结果保存到 feature_list 中
for (i in seq_along(test_fasta)) {
  seq <- test_fasta[[i]]
  feature_list_c <- append(feature_list_c, list(extractCTDC(seq)))
  feature_list_t <- append(feature_list_t, list(extractCTDT(seq)))
  feature_list_d <- append(feature_list_d, list(extractCTDD(seq)))
  
  # 更新进度条
  setTxtProgressBar(pb, i)
}

# 关闭进度条
close(pb)

# 将每个特征列表转换为数据框
if (length(feature_list_c) == 1) {
  df_c <- as.data.frame(t(feature_list_c[[1]]))
  df_t <- as.data.frame(t(feature_list_t[[1]]))
  df_d <- as.data.frame(t(feature_list_d[[1]]))
} else {
  df_c <- as.data.frame(do.call(rbind, feature_list_c))
  df_t <- as.data.frame(do.call(rbind, feature_list_t))
  df_d <- as.data.frame(do.call(rbind, feature_list_d))
}

# 按列拼接数据框
df_combined <- cbind(df_c, df_t, df_d)

# 筛选
selected_cols <- df_combined[, c("prop2.G2.residue25", "prop1.G3.residue0", "prop7.G3.residue0", "prop7.G1.residue25", "prop5.G2.residue0", "prop1.G3.residue25", "prop5.G2.residue25", "prop6.G1.residue75", "prop5.G3.residue0", "prop6.G1.residue50", "prop5.G1.residue0", "prop2.G2.residue50", "prop2.G3.residue0", "prop1.G2.residue0", "prop6.G1.residue0", "prop2.G2.residue75", "prop2.G1.residue25", "secondarystruct.Group2", "prop6.G3.residue25", "prop7.G1.residue50", "prop7.G3.residue100", "prop7.G1.residue0", "prop5.G3.residue100", "prop1.G1.residue25", "prop6.G3.residue0", "prop5.G3.residue75", "prop1.G3.residue50", "secondarystruct.Group1", "prop2.G2.residue0")]

selected_cols

