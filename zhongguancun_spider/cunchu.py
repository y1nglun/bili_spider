import pymysql
from pyecharts.charts import Line
from pyecharts import options as opts

# 连接数据库
connection = pymysql.connect(
    host="localhost",
    user="",
    password="",
    database="computer"
)

cursor = connection.cursor()

query = "SELECT cunchu, price FROM computer"
cursor.execute(query)
results = cursor.fetchall()

storages = [result[0] for result in results]
prices = [float(result[1]) for result in results]

cursor.close()
connection.close()

avg_prices = {}
for i in range(len(storages)):
    if storages[i] not in avg_prices:
        avg_prices[storages[i]] = [prices[i]]
    else:
        avg_prices[storages[i]].append(prices[i])

for storage in avg_prices:
    avg_prices[storage] = sum(avg_prices[storage]) / len(avg_prices[storage])


line = Line(init_opts=opts.InitOpts(width="800px", height="400px"))
line.add_xaxis(list(avg_prices.keys()))
line.add_yaxis(
    series_name="平均价格",
    y_axis=list(avg_prices.values()),
    markpoint_opts=opts.MarkPointOpts(data=[opts.MarkPointItem(type_="max"), opts.MarkPointItem(type_="min")]),
    markline_opts=opts.MarkLineOpts(data=[opts.MarkLineItem(type_="average")]),
)
line.set_global_opts(
    title_opts=opts.TitleOpts(title="平板电脑存储器容量与平均价格折线图"),
    xaxis_opts=opts.AxisOpts(name="存储器容量"),
    yaxis_opts=opts.AxisOpts(name="平均价格"),
)


line.render("line_chart_2.html")
