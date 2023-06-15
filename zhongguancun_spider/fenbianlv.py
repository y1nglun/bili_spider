import pymysql
from pyecharts.charts import Pie
from pyecharts import options as opts

connection = pymysql.connect(
    host="localhost",
    user="",
    password="",
    database="computer"
)

cursor = connection.cursor()

query = "SELECT fenbian, price FROM computer"
cursor.execute(query)
results = cursor.fetchall()

resolutions = [result[0] for result in results]
prices = [float(result[1]) for result in results]

cursor.close()
connection.close()

avg_prices = {}
for i in range(len(resolutions)):
    if resolutions[i] not in avg_prices:
        avg_prices[resolutions[i]] = [prices[i]]
    else:
        avg_prices[resolutions[i]].append(prices[i])

for resolution in avg_prices:
    avg_prices[resolution] = sum(avg_prices[resolution]) / len(avg_prices[resolution])

pie = Pie(init_opts=opts.InitOpts(width="800px", height="400px"))
pie.add(
    series_name="平板电脑价格分布",
    data_pair=list(avg_prices.items()),
    radius=["30%", "75%"],
    center=["50%", "50%"],
    label_opts=opts.LabelOpts(formatter="{b}: {c}元", position="outside", font_size=12),
)

pie.set_global_opts(
    title_opts=opts.TitleOpts(title="平板电脑屏幕分辨率与价格饼状图"),
    legend_opts=opts.LegendOpts(orient="vertical", pos_top="15%", pos_right="2%"),
)

pie.render("pie_chart.html")
