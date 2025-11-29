rm(list = ls()) # clear everything

renv::install(c("dplyr", "flextable", "stats", "janitor"))
library(dplyr)
library(flextable)
library(stats)
library(janitor)

load("output/清洗所得数据.RData")
# 数据预处理
df_common <- df_common %>%
  # 自杀意念：原变量“我从没有过自杀的想法和准备”，反向编码（>2=有，<=2=无）
  mutate(
    自杀意念 = ifelse(`我从没有过自杀的想法和准备` > 2, "有", "无"),
  # 自伤行为：原变量“我从没做过故意弄伤自己的行为”，反向编码（>2=有，<=2=无）
    自伤行为 = ifelse(`我从没做过故意弄伤自己的行为` > 2, "有", "无"),
  # 身体素质：scorelevel>2 =好，<2=差
    身体素质 = ifelse(scorelevel >= 3, "好", "差"),
  # 性别标签化（1=男，0=女）
    性别 = factor(sex, levels = c(1,0), labels = c("男", "女"))
  ) %>%
  # 保留分析变量
  select(性别, 身体素质, 自杀意念, 自伤行为)
print(names(df_common)) 

# 计算人数(%) + 卡方检验
get_stats <- function(group_var, outcome_var) {
  # 生成交叉表
  tab <- df_common %>%
    tabyl({{group_var}}, {{outcome_var}}) %>%
    adorn_totals(where = "row") %>%
    adorn_percentages(denominator = "row") %>%
    adorn_pct_formatting(digits = 2) %>%
    adorn_ns(position = "front")
  
  count_pct_res <- tab[-nrow(tab), "有"]
  
  # 卡方检验
  chisq_test <- chisq.test(table(df_common[[deparse(substitute(group_var))]], 
                                 df_common[[deparse(substitute(outcome_var))]]),correct=FALSE)
  chisq_val <- round(chisq_test$statistic, 3)
  p_val <- chisq_test$p.value
  sig_mark <- ifelse(p_val < 0.01, "**", ifelse(p_val < 0.05, "*", ""))
  chisq_res <- paste0("χ²=", chisq_val, sig_mark)
  
  return(list(
    count_pct = count_pct_res,
    chisq = chisq_res
  ))
}

# 计算各组统计量
sex_suicide <- get_stats(性别, 自杀意念)
sex_selfharm <- get_stats(性别, 自伤行为)
physical_suicide <- get_stats(身体素质, 自杀意念)
physical_selfharm <- get_stats(身体素质, 自伤行为)

# 整理表格数据
table_result <- data.frame(
  变量 = c("性别", "男", "女", "", "身体素质", "好", "差", ""),
  自杀意念 = c("", 
           sex_suicide$count_pct[1], 
           sex_suicide$count_pct[2], 
           sex_suicide$chisq,
           "", 
           physical_suicide$count_pct[2], 
           physical_suicide$count_pct[1], 
           physical_suicide$chisq),
  自伤行为 = c("", 
           sex_selfharm$count_pct[1], 
           sex_selfharm$count_pct[2], 
           sex_selfharm$chisq,
           "", 
           physical_selfharm$count_pct[2], 
           physical_selfharm$count_pct[1], 
           physical_selfharm$chisq)
)

# 写入CSV文件
write.csv(table_result, 
          file = "output/中学生自伤行为和自杀意念的人口统计学差异.csv", 
          row.names = FALSE,  
          fileEncoding = "UTF-8") 

