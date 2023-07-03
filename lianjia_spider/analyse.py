import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm

font_path = 'C:/Windows/Fonts/STHUPO.TTF'
prop = fm.FontProperties(fname=font_path)
plt.rcParams['font.family'] = prop.get_name()
# 读取数据文件，假设数据保存在名为data.xlsx的 Excel 文件中，包含标题、房屋详细信息、总价和单价字段


data = pd.read_excel('data.xlsx')

# 数据分析和可视化

# 房屋总价分布分析（直方图）
plt.figure(figsize=(10, 6))
plt.hist(data['总价'], bins=10, edgecolor='black')
plt.xlabel('房屋总价')
plt.ylabel('数量')
plt.title('房屋总价分布')
plt.grid(True)
plt.show()

# 单价与总价的关系分析（散点图）
plt.figure(figsize=(10, 6))
prices = data['单价'].str.replace(',', '').str.extract(r'(\d+)').astype(int)  # 提取单价中的数字，并转换为整数类型
plt.scatter(prices, data['总价'], alpha=0.5)
plt.xlabel('单价')
plt.ylabel('总价')
plt.title('单价与总价关系')
plt.grid(True)
plt.show()
