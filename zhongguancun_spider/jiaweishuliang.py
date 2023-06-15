import pymysql
from pyecharts.charts import Bar
from pyecharts import options as opts


connection = pymysql.connect(
    host="localhost",
    user="",
    password="",
    database="computer"
)


cursor = connection.cursor()


query = "SELECT price, COUNT(*) AS count FROM computer GROUP BY price ORDER BY price"
cursor.execute(query)
results = cursor.fetchall()


price_ranges = [result[0] for result in results]
counts = [result[1] for result in results]


cursor.close()
connection.close()


bar = Bar()
bar.add_xaxis(price_ranges)
bar.add_yaxis("数量", counts)
bar.set_global_opts(title_opts=opts.TitleOpts(title="平板电脑各个价位的数量柱状图"))

bar.render("bar_chart.html")
