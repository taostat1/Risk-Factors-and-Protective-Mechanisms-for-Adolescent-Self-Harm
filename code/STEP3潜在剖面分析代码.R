rm(list = ls()) # clear everything
renv::install("MplusAutomation")
library(MplusAutomation)
renv::install("mclust")
library(mclust)
renv::install("tidyLPA")
library(tidyLPA)
library(dplyr)
load("output/清洗所得数据.RData")
#########################################################
# 1. 厌学倾向
#########################################################
school_select <- select(df_common, '我不喜欢上学', '我觉得学习很累很烦', '我希望可以不用学习')
# 转为数值型变量
school_select <- school_select %>%
  mutate(across(everything(), as.numeric))
# 使用estimate_profiles进行聚类分析，范围是1到6个聚类
school_cluster <- estimate_profiles(school_select, 1:6)

plot_profiles(school_cluster, rawdata = F, sd = F, ci = F, add_line = T) +
  theme(axis.text.x = element_text(angle = 45, hjust = 0.4, vjust = 0.5))

fit_schoolresult <- get_fit(school_cluster)
cla_schoolresult <- school_cluster$model_1_class_4$dff

################将分类信息加到df_common中#################
# 将cla_schoolresult的Class列添加到df_common
df_common$Class <- cla_schoolresult$Class

# 计算每个Class的三个厌学变量均值并排序
class_厌学均值 <- cla_schoolresult %>%
  group_by(Class) %>%
  summarise(
    不喜欢上学均值 = mean(`我不喜欢上学`, na.rm = TRUE),
    学习很累均值 = mean(`我觉得学习很累很烦`, na.rm = TRUE),
    希望不用学习均值 = mean(`我希望可以不用学习`, na.rm = TRUE),
    综合厌学均值 = mean(c(`我不喜欢上学`, `我觉得学习很累很烦`, `我希望可以不用学习`), na.rm = TRUE),
    .groups = "drop"
  ) %>%
  arrange(综合厌学均值) %>%  # 按均值从小到大排序
  mutate(school_class = row_number())  # 生成1-4的排序类别

# 将school_class匹配到df_common
df_common <- df_common %>%
  left_join(class_厌学均值 %>% select(Class, school_class), by = "Class") %>%
  select(-Class) #（删除映射）


#########################打印出分类的BIC等信息####################
class_counts <- table(school_cluster$model_1_class_4$model$classification)
total_samples <- sum(class_counts)
class_proportions <- class_counts/total_samples
print(class_proportions)

school_result <- cbind(school_select, school_cluster$model_1_class_5$model$classification)
fit_temp <- get_fit(school_cluster)
print(colnames(fit_temp))

fit_df <- get_fit(school_cluster) %>%
  rename(
    Classes = Classes,  # 类别数量列名直接是Classes
    AIC = AIC,
    BIC = BIC,
    aBIC = SABIC,      # 校正BIC对应列名是SABIC
    Entropy = Entropy,
    "BLRT(p)" = BLRT_p  # BLRT检验p值对应列名是BLRT_p
  )

# 计算每个类别数的潜在类别比例
prop_list <- lapply(1:6, function(k) {
  model_name <- paste0("model_1_class_", k)
  # 提取该模型的分类结果
  classifications <- school_cluster[[model_name]]$model$classification
  # 计算类别数量和比例
  class_counts <- table(classifications)
  class_props <- round(class_counts / sum(class_counts), 2)
  # 格式化为"0.12:0.15:0.70"形式
  paste(class_props, collapse = ": ")
})

# 输出表格
fit_table <- fit_df %>%
  mutate(
    "潜在类别比例" = unlist(prop_list)
  ) %>%
  select(Classes, AIC, BIC, aBIC, Entropy, "BLRT(p)", "潜在类别比例")

print(fit_table, row.names = FALSE)
write.csv(fit_table, "output/厌学倾向潜在类别分析结果表格.csv", row.names = FALSE, fileEncoding = "UTF-8")



# 网络依赖
internet_select <- select(df_common, "我只要有一段时间没有上网、看手机，就会莫名地情绪低落", 
                          "长时间网游，使我的身体健康状况越来越不如以前了", 
                          "由于上网使我与周围其他人的关系没以前好了，但我无法减少上网时间")
# 转为数值型变量
internet_select <- internet_select %>%
  mutate(across(everything(), as.numeric))
# 使用estimate_profiles进行聚类分析，范围是1到6个聚类
internet_cluster <- estimate_profiles(internet_select, 1:6)

plot_profiles(internet_cluster, rawdata = F, sd = F, ci = F, add_line = T) +
  theme(axis.text.x = element_text(angle = 45, hjust = 0.4, vjust = 0.5))
internet_schoolresult <- get_fit(internet_cluster)

fit_internetresult <- get_fit(internet_cluster)
cla_internetresult <- internet_cluster$model_1_class_4$dff
write.csv(fit_internetresult, "fit_internetresult.csv")
write.csv(cla_internetresult, "cla_internetresult.csv")

fit_temp <- get_fit(internet_cluster)
print(colnames(fit_temp))

fit_df <- get_fit(internet_cluster) %>%
  rename(
    Classes = Classes,  # 类别数量列名直接是Classes，无需修改
    AIC = AIC,
    BIC = BIC,
    aBIC = SABIC,      # 校正BIC对应列名是SABIC
    Entropy = Entropy,
    "BLRT(p)" = BLRT_p  # BLRT检验p值对应列名是BLRT_p
  )

# 计算每个类别数的潜在类别比例
prop_list <- lapply(1:6, function(k) {
  # 构建模型在internet_cluster中的名称（如"model_1_class_1"、"model_1_class_2"）
  model_name <- paste0("model_1_class_", k)
  
  # 检查该模型是否存在
  if (!model_name %in% names(internet_cluster)) {
    return(NA)  # 若模型不存在，返回NA
  }
  
  # 提取该模型的分类结果
  classifications <- internet_cluster[[model_name]]$model$classification
  
  # 计算类别数量和比例
  class_counts <- table(classifications)
  class_props <- round(class_counts / sum(class_counts), 2)
  
  # 格式化为"0.12:0.15:0.70"形式
  paste(class_props, collapse = ": ")
})

# 后续代码保持不变，继续合并并输出表格
fit_table <- fit_df %>%
  mutate(
    "潜在类别比例" = unlist(prop_list)
  ) %>%
  select(Classes, AIC, BIC, aBIC, Entropy, "BLRT(p)", "潜在类别比例")

print(fit_table, row.names = FALSE)
write.csv(fit_table, "网络依赖潜在类别分析结果表格.csv", row.names = FALSE, fileEncoding = "UTF-8")


# 创伤事件
injury_select <- select(df_common, "别人给我起难听的外号，骂我，或取笑、讽刺我", 
                        "别人强迫向我要钱，或者拿走、损坏我的东西", 
                        "某些同学采用打、踢、推、撞等方式欺负我")
# 转为数值型变量
injury_select <- injury_select %>%
  mutate(across(everything(), as.numeric))
# 使用estimate_profiles进行聚类分析，范围是1到6个聚类
injury_cluster <- estimate_profiles(injury_select, 1:6)

plot_profiles(injury_cluster, rawdata = F, sd = F, ci = F, add_line = T) +
  theme(axis.text.x = element_text(angle = 45, hjust = 0.4, vjust = 0.5))
fit_injuryresult <- get_fit(injury_cluster)

fit_injuryresult <- get_fit(injury_cluster)
cla_injuryresult <- injury_cluster$model_1_class_4$dff
write.csv(fit_injuryresult, "fit_injuryresult.csv")
write.csv(cla_injuryresult, "cla_injuryresult.csv")

fit_temp <- get_fit(injury_cluster)
print(colnames(fit_temp))

fit_df <- get_fit(injury_cluster) %>%
  rename(
    Classes = Classes,  # 类别数量列名直接是Classes
    AIC = AIC,
    BIC = BIC,
    aBIC = SABIC,      # 校正BIC对应列名是SABIC
    Entropy = Entropy,
    "BLRT(p)" = BLRT_p  # BLRT检验p值对应列名是BLRT_p
  )

# 计算每个类别数的潜在类别比例
prop_list <- lapply(1:6, function(k) {
  # 构建模型在injury_cluster中的名称（如"model_1_class_1"、"model_1_class_2"）
  model_name <- paste0("model_1_class_", k)
  
  # 检查该模型是否存在
  if (!model_name %in% names(injury_cluster)) {
    return(NA)  # 若模型不存在，返回NA
  }
  
  # 提取该模型的分类结果
  classifications <- injury_cluster[[model_name]]$model$classification
  
  # 计算类别数量和比例
  class_counts <- table(classifications)
  class_props <- round(class_counts / sum(class_counts), 2)
  
  # 格式化为"0.12:0.15:0.70"形式
  paste(class_props, collapse = ": ")
})

# 输出表格
fit_table <- fit_df %>%
  mutate(
    "潜在类别比例" = unlist(prop_list)
  ) %>%
  select(Classes, AIC, BIC, aBIC, Entropy, "BLRT(p)", "潜在类别比例")

print(fit_table, row.names = FALSE)
write.csv(fit_table, "网络依赖潜在类别分析结果表格.csv", row.names = FALSE, fileEncoding = "UTF-8")