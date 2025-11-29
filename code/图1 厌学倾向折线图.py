import pandas as pd
import chardet
import matplotlib.pyplot as plt
import seaborn as sns

# 读取数据
file_path = r"D:\Study on Youth Suicide Rate\cla_schoolresult.csv"
with open(file_path, 'rb') as f:
    result = chardet.detect(f.read())

# 输出检测到的编码
print(f"检测到的文件编码: {result['encoding']}")

# 使用检测到的编码读取文件
data = pd.read_csv(file_path, encoding=result['encoding'])
print("文件读取成功！")

# 查看数据
print(data.head())

# 1. 绘制饼图：四类同学的比例
class_counts = data['Class'].value_counts().sort_index()

# 定义类别标签
class_labels = ["吃力型同学", "好学型同学", "厌学型同学", "天赋型同学"]

# 定义颜色
colors = ['#66c2a5', '#fc8d62', '#8da0cb', '#e78ac3']

# 绘制饼图
plt.rcParams['font.family'] = ['Times New Roman', 'SimHei']  # 设置字体
plt.figure(figsize=(4, 4))

# 将 len(labels) 改为 len(class_labels)
plt.pie(class_counts, labels=class_labels, autopct='%1.1f%%', startangle=140, colors=sns.color_palette("viridis", len(class_labels)))
plt.title("厌学倾向潜在剖面分析中四类同学的比例", fontsize=15)
plt.tight_layout()

# 保存饼图
plt.savefig("D:\Study on Youth Suicide Rate\class_proportion_pie.png", dpi=500)
plt.show()

# 2. 绘制折线图：四类同学在前三列指标上的表现
# 计算每类在前三列指标上的均值
class_means = data.groupby('Class')[['就学厌恶', '学习倦怠', '弃学意愿']].mean()

# 将数据转换为长格式
class_means_long = class_means.reset_index().melt(id_vars='Class', var_name='Indicator', value_name='Mean_Value')

# 定义线型
line_styles = ['solid', 'dashed', 'dotted', 'dashdot']

# 绘制折线图
plt.figure(figsize=(8, 6))
for i, class_id in enumerate(class_means.index):
    subset = class_means_long[class_means_long['Class'] == class_id]
    plt.plot(subset['Indicator'], subset['Mean_Value'], 
             label=class_labels[i], color=colors[i], linestyle=line_styles[i], linewidth=2, marker='o')

# 添加标题和标签
plt.xlabel("指标", fontsize=12)
plt.ylabel("指标得分均值", fontsize=12)
plt.xticks(fontsize=12)
plt.yticks(fontsize=12)
plt.legend(title="类别", fontsize=10)
plt.grid(True, linestyle='--', alpha=0.6)

# 保存折线图
plt.savefig("D:\Study on Youth Suicide Rate\图1四类同学在厌学指标上的表现.png", dpi=600)
plt.show()

