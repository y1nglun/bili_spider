import pymysql
from pyecharts.charts import Boxplot
from pyecharts import options as opts

connection = pymysql.connect(
    host="localhost",
    user="",
    password="",
    database="computer"
)

cursor = connection.cursor()

query = "SELECT price, comment FROM computer"
cursor.execute(query)
results = cursor.fetchall()

prices = [result[0] for result in results]
evaluation_counts = [result[1] for result in results]

cursor.close()
connection.close()

boxplot = Boxplot(init_opts=opts.InitOpts(width="800px", height="400px"))
boxplot.add_xaxis(["平板电脑"])
boxplot.add_yaxis("价格与评价数量关系", [prices], tooltip_opts=opts.TooltipOpts(formatter="{b}: {c}"))
boxplot.set_global_opts(title_opts=opts.TitleOpts(title="平板电脑价格与评价数量关系箱型图"))

boxplot.render("boxplot_chart.html")
