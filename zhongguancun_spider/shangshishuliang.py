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

query = "SELECT year, COUNT(*) AS count FROM computer GROUP BY year ORDER BY year"
cursor.execute(query)
results = cursor.fetchall()


years = [result[0] for result in results]
counts = [result[1] for result in results]


cursor.close()
connection.close()


line = Line(init_opts=opts.InitOpts(width="800px", height="400px"))
line.add_xaxis(years)


line.add_yaxis("数量", counts, markpoint_opts=opts.MarkPointOpts(
    data=[opts.MarkPointItem(type_="max"), opts.MarkPointItem(type_="min")]),
               markline_opts=opts.MarkLineOpts(data=[opts.MarkLineItem(type_="average")]))

line.set_global_opts(title_opts=opts.TitleOpts(title="平板电脑每年上市数量折线图"))


line.render("line_chart.html")
