import pymysql
from pyecharts.charts import Bar
from pyecharts import options as opts

# 连接数据库
connection = pymysql.connect(
    host="localhost",
    user="",
    password="",
    database="computer"
)

cursor = connection.cursor()


query = "SELECT pval_name, COUNT(*) AS count FROM computer GROUP BY pval_name"
cursor.execute(query)
results = cursor.fetchall()


companies = [result[0] for result in results]
counts = [result[1] for result in results]


cursor.close()
connection.close()


bar = Bar(init_opts=opts.InitOpts(width="800px", height="400px"))
bar.add_xaxis(companies)
bar.add_yaxis("平板电脑数量", counts)


bar.set_global_opts(
    title_opts=opts.TitleOpts(title="各公司平板电脑数量规模对比柱状图"),
    xaxis_opts=opts.AxisOpts(axislabel_opts=opts.LabelOpts(rotate=-45)),
    yaxis_opts=opts.AxisOpts(name="数量"),
)


bar.render("bar_chart_2.html")
