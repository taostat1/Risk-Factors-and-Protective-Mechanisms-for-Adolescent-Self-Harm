import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

# 设置中文字体，保持一致性
plt.rcParams['font.family'] = ['Times New Roman', 'SimHei']
plt.rcParams['axes.unicode_minus'] = False  # 解决负号显示问题

# 定义组别名称
group_names = {
    1: "好学型",
    2: "吃力型",
    3: "天赋型",
    4: "厌学型"
}

# 使用指定的颜色
colors = ['#66c2a5', '#fc8d62', '#8da0cb', '#e78ac3']

# 从表格获取数据：自杀倾向和自杀行为的平均值、标准偏差
data = {
    'group': [1, 2, 3, 4],
    # 自杀倾向数据
    'suicide_tendency_mean': [1.9121, 2.2773, 1.2474, 2.3261],
    'suicide_tendency_std': [1.23512, 1.29213, 0.75043, 1.43817],
    # 自杀行为数据
    'suicide_behavior_mean': [1.6484, 1.9202, 1.1031, 1.8043],
    'suicide_behavior_std': [1.06847, 1.20387, 0.44452, 1.18821],
    # 个案数
    'n': [91, 238, 97, 92]
}

# 提取自杀倾向的显著差异组对
significant_pairs_tendency = [
    (4, 1, 0.072),   # *
    (2, 3, 0.057),   # *
    (3, 2, 0.057),   # *
    (3, 4, 0.01),    # **
    (4, 3, 0.01)     # **
]

# 提取自杀行为的显著差异组对 
significant_pairs_behavior = [
    (2, 3, 0.002),   # ***
    (3, 2, 0.002),   # ***
    (3, 4, 0.019),   # **
    (4, 3, 0.019)    # **
]

# 准备绘图数据
positions = np.arange(len(data['group']))  # 组别的位置
bar_width = 0.35  # 条形宽度

# 创建图形和轴
plt.figure(figsize=(6, 4))  # 增加高度以容纳底部标注

# 定义纹理样式，用于区分自杀倾向和自杀行为
hatches = ['//', '']  # 自杀倾向使用斜线纹理，自杀行为无纹理

# 绘制自杀倾向条形图
bars1 = plt.bar(positions - bar_width/2, data['suicide_tendency_mean'], bar_width,
                yerr=data['suicide_tendency_std'], capsize=10,
                color=colors, hatch=hatches[0],
                error_kw={'ecolor': 'darkgray', 'capthick': 2},
                label='自杀意念')

# 绘制自杀行为条形图
bars2 = plt.bar(positions + bar_width/2, data['suicide_behavior_mean'], bar_width,
                yerr=data['suicide_behavior_std'], capsize=10,
                color=colors, hatch=hatches[1],
                error_kw={'ecolor': 'darkgray', 'capthick': 2},
                label='自伤行为')

# 添加标题和标签

plt.xlabel('厌学倾向组别', fontsize=12)
plt.ylabel('自杀意念/自伤行为得分', fontsize=12)
plt.xticks(positions, [group_names[i] for i in data['group']])

# 添加图例
plt.legend()

# 在每个组别上方添加个案数
for i, pos in enumerate(positions):
    max_height = max(data['suicide_tendency_mean'][i] + data['suicide_tendency_std'][i],
                    data['suicide_behavior_mean'][i] + data['suicide_behavior_std'][i])
    plt.text(pos, max_height + 0.15,
             f'n={data["n"][i]}', ha='center', va='bottom', fontsize=10)

# 标注自杀倾向的显著差异（保持在顶部）
unique_pairs_tendency = {(4, 1), (2, 3), (3, 4)}
y_max_tendency = max([m + s for m, s in zip(data['suicide_tendency_mean'], data['suicide_tendency_std'])]) + 0.5

for i, j in unique_pairs_tendency:
    p_value = next(p[2] for p in significant_pairs_tendency if (p[0]==i and p[1]==j))
    x1, x2 = positions[i-1] - bar_width/4, positions[j-1] - bar_width/4  # 稍微向左偏移，对应自杀倾向柱子
    
    # 绘制连接线
    plt.plot([x1, x1, x2, x2], [y_max_tendency, y_max_tendency+0.15, y_max_tendency+0.15, y_max_tendency], 
             'k-', linewidth=1.5, alpha=0.7)
    
    # 标注显著性水平
    if p_value < 0.001:
        significance = f'***\np={p_value:.3f}'
    elif p_value < 0.01:
        significance = f'**\np={p_value:.3f}'
    elif p_value < 0.05:
        significance = f'*\np={p_value:.3f}'
    else:  # p < 0.1
        significance = f'+\np={p_value:.3f}'
    
    plt.text((x1 + x2) / 2, y_max_tendency + 0.2, significance, 
             ha='center', va='bottom', color='blue', fontweight='bold')
    y_max_tendency += 0.5

# 标注自杀行为的显著差异（放在x轴下方）
unique_pairs_behavior = {(2, 3), (3, 4)}
y_min_behavior = min([m - s for m, s in zip(data['suicide_behavior_mean'], data['suicide_behavior_std'])]) - 0.5
current_y = y_min_behavior  # 从最低处开始向下标注

for i, j in unique_pairs_behavior:
    p_value = next(p[2] for p in significant_pairs_behavior if (p[0]==i and p[1]==j))
    x1, x2 = positions[i-1] + bar_width/4, positions[j-1] + bar_width/4  # 稍微向右偏移，对应自杀行为柱子
    
    # 绘制连接线（向下延伸）
    plt.plot([x1, x1, x2, x2], [current_y, current_y-0.15, current_y-0.15, current_y], 
             'k-', linewidth=1.5, alpha=0.7)
    
    # 标注显著性水平
    if p_value < 0.001:
        significance = f'***\np={p_value:.3f}'
    elif p_value < 0.01:
        significance = f'**\np={p_value:.3f}'
    elif p_value < 0.05:
        significance = f'*\np={p_value:.3f}'
    else:  # p < 0.1
        significance = f'+\np={p_value:.3f}'
    
    plt.text((x1 + x2) / 2, current_y - 0.2, significance, 
             ha='center', va='top', color='green', fontweight='bold')
    current_y -= 0.5  # 为下一个标注腾出空间

# 添加网格线
plt.grid(axis='y', linestyle='--', alpha=0.7)

# 调整y轴范围，确保底部标注可见
plt.ylim(bottom=current_y - 0.5)

# 添加图例说明显著性符号
significance_legend = [
    mpatches.Patch(color='none', label='+ p < 0.1'),
    mpatches.Patch(color='none', label='* p < 0.05'),
    mpatches.Patch(color='none', label='** p < 0.01'),
    mpatches.Patch(color='none', label='*** p < 0.001')
]
plt.legend(handles=plt.gca().get_legend_handles_labels()[0] + significance_legend, 
           loc='upper left', bbox_to_anchor=(1, 1))

# 紧凑布局
plt.tight_layout()

# 保存图片
plt.savefig(r"D:\Study on Youth Suicide Rate\图2厌学倾向四类同学在自我伤害指标上的表现.png", dpi=600, bbox_inches='tight')
plt.show()