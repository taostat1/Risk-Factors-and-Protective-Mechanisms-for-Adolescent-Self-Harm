import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

# 设置中文字体，确保正常显示
plt.rcParams['font.family'] = ['Times New Roman', 'SimHei']
plt.rcParams['axes.unicode_minus'] = False  # 解决负号显示问题

# 定义霸凌倾向组别名称
group_names = {
    1: "低霸凌暴露型",
    2: "言语霸凌型",
    3: "身体霸凌型",
    4: "关系霸凌型"
}

# 配色方案
colors = ['#66c2a5', '#fc8d62', '#8da0cb', '#e78ac3']


data = {
    'group': [1, 2, 3, 4],
    # 自杀想法数据
    'suicide_idea_mean': [1.8406, 2.8491, 2.6512, 3.0],  # 平均值（值越大越不认同）
    'suicide_idea_std': [1.19064, 1.32137, 1.42901, 1.77281],  # 标准偏差
    # 自杀行为数据
    'suicide_behavior_mean': [1.5266, 2.0377, 2.6977, 3.0],
    'suicide_behavior_std': [0.97822, 1.23976, 1.37208, 1.30931],
    'n': [414, 53, 43, 8]  # 个案数
}

# 自杀想法的显著差异组对
significant_pairs_idea = [
    (1, 2, 0.000),    # ***（1 vs 2）
    (1, 3, 0.001),    # ***（1 vs 3）
    (1, 4, 0.068)     # *（1 vs 4）
]

# 自杀行为的显著差异组对
significant_pairs_behavior = [
    (1, 2, 0.014),    # **（1 vs 2）
    (1, 3, 0.000),    # ***（1 vs 3）
    (1, 4, 0.001),    # ***（1 vs 4）
    (2, 3, 0.006),    # ***（2 vs 3）
    (2, 4, 0.074)     # *（2 vs 4）
]

# 绘图参数
positions = np.arange(len(data['group']))  # 组别位置
bar_width = 0.35  # 柱宽（两组数据并排显示）
hatches = ['//', '']  # 图案区分：自杀想法用斜线，自杀行为无图案

# 创建图形
plt.figure(figsize=(14, 8))

# 绘制自杀想法柱子（带斜线）
bars_idea = plt.bar(
    positions - bar_width/2, 
    data['suicide_idea_mean'], 
    bar_width,
    yerr=data['suicide_idea_std'], 
    capsize=10,
    color=colors, 
    hatch=hatches[0],
    error_kw={'ecolor': 'darkgray', 'capthick': 2},
    label='自杀意念'
)

# 绘制自杀行为柱子（无图案）
bars_behavior = plt.bar(
    positions + bar_width/2, 
    data['suicide_behavior_mean'], 
    bar_width,
    yerr=data['suicide_behavior_std'], 
    capsize=10,
    color=colors, 
    hatch=hatches[1],
    error_kw={'ecolor': 'darkgray', 'capthick': 2},
    label='自杀行为'
)

# 标题与标签
plt.xlabel('被欺凌倾向组别', fontsize=12)
plt.ylabel('自杀意念/自伤行为得分', fontsize=12)
plt.xticks(positions, [group_names[i] for i in data['group']])
plt.legend()

# 标注个案数（每组上方居中）
for i, pos in enumerate(positions):
    # 取两组数据的最大高度+误差，确保文本在上方
    max_height = max(
        data['suicide_idea_mean'][i] + data['suicide_idea_std'][i],
        data['suicide_behavior_mean'][i] + data['suicide_behavior_std'][i]
    )
    plt.text(pos, max_height + 0.2, f'n={data["n"][i]}', 
             ha='center', va='bottom', fontsize=10)

# 标注自杀想法的显著差异（顶部）
y_current_idea = max([m + s for m, s in zip(data['suicide_idea_mean'], data['suicide_idea_std'])]) + 0.3
step_idea = 0.6  # 垂直间距

for i, j, p_value in significant_pairs_idea:
    # 对应自杀想法柱子的x坐标
    x1, x2 = positions[i-1] - bar_width/4, positions[j-1] - bar_width/4
    
    # 连接线
    plt.plot([x1, x1, x2, x2], 
             [y_current_idea, y_current_idea+0.15, y_current_idea+0.15, y_current_idea], 
             'k-', linewidth=1.5)
    
    # 显著性符号（按p值定义）
    if p_value < 0.001:
        significance = '***'
    elif p_value < 0.01:
        significance = '**'
    else:  # 表20中p=0.068标注为*
        significance = '*'
    
    # 标注文本
    plt.text((x1 + x2)/2, y_current_idea + 0.2, 
             f'{significance}\np={p_value:.3f}', 
             ha='center', va='bottom', color='blue', fontweight='bold')
    y_current_idea += step_idea

# 标注自杀行为的显著差异（底部）
y_current_behavior = min([m - s for m, s in zip(data['suicide_behavior_mean'], data['suicide_behavior_std'])]) - 0.3
step_behavior = 0.6  # 垂直间距

for i, j, p_value in significant_pairs_behavior:
    # 对应自杀行为柱子的x坐标
    x1, x2 = positions[i-1] + bar_width/4, positions[j-1] + bar_width/4
    
    # 连接线（向下延伸）
    plt.plot([x1, x1, x2, x2], 
             [y_current_behavior, y_current_behavior-0.15, y_current_behavior-0.15, y_current_behavior], 
             'k-', linewidth=1.5)
    
    # 显著性符号
    if p_value < 0.001:
        significance = '***'
    elif p_value < 0.01:
        significance = '**'
    else:  # 表23中p=0.074标注为*
        significance = '*'
    
    # 标注文本
    plt.text((x1 + x2)/2, y_current_behavior - 0.2, 
             f'{significance}\np={p_value:.3f}', 
             ha='center', va='top', color='green', fontweight='bold')
    y_current_behavior -= step_behavior

# 调整y轴范围（确保底部标注完整显示）
plt.ylim(bottom=y_current_behavior - 0.5, top=y_current_idea + 0.5)

# 网格线与图例（包含显著性说明）
plt.grid(axis='y', linestyle='--', alpha=0.7)
significance_legend = [
    mpatches.Patch(color='none', label='* p < 0.1'),
    mpatches.Patch(color='none', label='** p < 0.01'),
    mpatches.Patch(color='none', label='*** p < 0.001')
]
plt.legend(handles=plt.gca().get_legend_handles_labels()[0] + significance_legend,
           loc='upper left', bbox_to_anchor=(1, 1))


# 保存与显示
plt.tight_layout()
plt.savefig(r"D:\Study on Youth Suicide Rate\图6被欺凌倾向四类同学在自我伤害指标上的表现.pdf", dpi=300, bbox_inches='tight')
plt.show()
