import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

# 设置中文字体，保持风格统一
plt.rcParams['font.family'] = ['Times New Roman', 'SimHei']
plt.rcParams['axes.unicode_minus'] = False  # 解决负号显示问题

# 定义网络依赖组别名称
group_names = {
    1: "网络自律型",
    2: "中度依赖型",
    3: "网络依赖型",
    4: "网络成瘾型"
}

# 配色方案
colors = ['#66c2a5', '#fc8d62', '#8da0cb', '#e78ac3']

# 数据整理：网络依赖与自杀倾向、自伤行为的描述性数据
data = {
    'group': [1, 2, 3, 4],
    # 自杀倾向数据
    'suicide_tendency_mean': [1.8552, 2.1, 2.5714, 2.6552],
    'suicide_tendency_std': [1.22029, 1.25719, 1.46742, 1.47057],
    # 自伤行为数据
    'self_harm_mean': [1.65, 1.88, 2.32, 2.45],
    'self_harm_std': [1.10, 1.18, 1.35, 1.40],
    # 个案数
    'n': [297, 150, 42, 29]
}

# 网络依赖与自杀倾向的显著差异组对
significant_pairs_tendency = [
    (1, 4, 0.028), 
    (4, 1, 0.028)   
]

# 网络依赖与自伤行为的显著差异组对
significant_pairs_self_harm = [
    (1, 3, 0.045),  
    (1, 4, 0.012),  
    (2, 4, 0.038)   
]

# 绘图参数
positions = np.arange(len(data['group']))  # 组别位置
bar_width = 0.35  # 柱宽
hatches = ['//', '']  # 图纹：自杀倾向用斜线，自伤行为无图纹

# 创建图形
plt.figure(figsize=(12, 7))

# 绘制自杀倾向柱子（带斜线）
bars1 = plt.bar(
    positions - bar_width/2, 
    data['suicide_tendency_mean'], 
    bar_width,
    yerr=data['suicide_tendency_std'], 
    capsize=10,
    color=colors, 
    hatch=hatches[0],
    error_kw={'ecolor': 'darkgray', 'capthick': 2},
    label='自杀倾向'
)

# 绘制自伤行为柱子（无图纹）
bars2 = plt.bar(
    positions + bar_width/2, 
    data['self_harm_mean'], 
    bar_width,
    yerr=data['self_harm_std'], 
    capsize=10,
    color=colors, 
    hatch=hatches[1],
    error_kw={'ecolor': 'darkgray', 'capthick': 2},
    label='自伤行为'
)

# 标题与标签
plt.xlabel('网络依赖组别', fontsize=12)
plt.ylabel('自杀意念/自伤行为得分', fontsize=12)
plt.xticks(positions, [group_names[i] for i in data['group']])
plt.legend()

# 标注个案数
for i, pos in enumerate(positions):
    max_height = max(
        data['suicide_tendency_mean'][i] + data['suicide_tendency_std'][i],
        data['self_harm_mean'][i] + data['self_harm_std'][i]
    )
    plt.text(pos, max_height + 0.15, f'n={data["n"][i]}', 
             ha='center', va='bottom', fontsize=10)

# 标注自杀倾向的显著差异（顶部）
unique_pairs_tendency = {(1, 4)}
y_max_tendency = max([m + s for m, s in zip(data['suicide_tendency_mean'], data['suicide_tendency_std'])]) + 0.5

for i, j in unique_pairs_tendency:
    p_value = next(p[2] for p in significant_pairs_tendency if (p[0]==i and p[1]==j))
    x1, x2 = positions[i-1] - bar_width/4, positions[j-1] - bar_width/4  # 对应自杀倾向柱子位置
    
    # 连接线
    plt.plot([x1, x1, x2, x2], 
             [y_max_tendency, y_max_tendency+0.15, y_max_tendency+0.15, y_max_tendency], 
             'k-', linewidth=1.5)
    
    # 显著性标注
    significance = '**' if p_value < 0.05 else '*'
    plt.text((x1 + x2)/2, y_max_tendency + 0.2, 
             f'{significance}\np={p_value:.3f}', 
             ha='center', va='bottom', color='blue', fontweight='bold')
    y_max_tendency += 0.4

# 标注自伤行为的显著差异
unique_pairs_self_harm = {(1, 3), (1, 4), (2, 4)}
y_min_harm = min([m - s for m, s in zip(data['self_harm_mean'], data['self_harm_std'])]) - 0.5
current_y = y_min_harm

for i, j in unique_pairs_self_harm:
    p_value = next(p[2] for p in significant_pairs_self_harm if (p[0]==i and p[1]==j))
    x1, x2 = positions[i-1] + bar_width/4, positions[j-1] + bar_width/4  # 对应自伤行为柱子位置
    
    # 连接线（向下）
    plt.plot([x1, x1, x2, x2], 
             [current_y, current_y-0.15, current_y-0.15, current_y], 
             'k-', linewidth=1.5)
    
    # 显著性标注
    if p_value < 0.01:
        significance = '**'
    elif p_value < 0.05:
        significance = '*'
    plt.text((x1 + x2)/2, current_y - 0.2, 
             f'{significance}\np={p_value:.3f}', 
             ha='center', va='top', color='green', fontweight='bold')
    current_y -= 0.4

# 调整y轴范围
plt.ylim(bottom=current_y - 0.3)

# 网格线与图例
plt.grid(axis='y', linestyle='--', alpha=0.7)
significance_legend = [
    mpatches.Patch(color='none', label='* p < 0.05'),
    mpatches.Patch(color='none', label='** p < 0.01')
]
plt.legend(handles=plt.gca().get_legend_handles_labels()[0] + significance_legend,
           loc='upper left', bbox_to_anchor=(1, 1))

# 保存与显示
plt.tight_layout()
plt.savefig(r"D:\Study on Youth Suicide Rate\图4网络依赖四类同学在自我伤害指标上的表现.pdf", dpi=300, bbox_inches='tight')
plt.show()