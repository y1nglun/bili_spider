import csv
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import datetime
import matplotlib.font_manager as fm

dates = []
indices = []
volumes = []
amounts = []

font_path = 'C:/Windows/Fonts/msyh.ttc'
prop = fm.FontProperties(fname=font_path)
plt.rcParams['font.family'] = prop.get_name()

with open('index_data.csv', 'r', encoding='utf-8') as file:
    reader = csv.DictReader(file)
    for row in reader:
        date = row['Date']
        index = float(row['Close'])
        volume = int(row['Succeed'])
        amount = float(row['Succeed Price'])

        dates.append(date)
        indices.append(index)
        volumes.append(volume)
        amounts.append(amount)

dates = [datetime.datetime.strptime(date_str, "%Y-%m-%d") for date_str in dates]

plt.figure(figsize=(18, 8))
plt.plot(dates, indices)
plt.xlabel("日期")
plt.ylabel("指数")
plt.title("指数走势图")
plt.grid(True)

ax = plt.gca()
ax.xaxis.set_major_locator(mdates.MonthLocator(bymonth=[1, 4, 7, 10]))
ax.xaxis.set_major_formatter(mdates.DateFormatter("%Y-%m"))

plt.xticks(rotation=45)
plt.savefig("index_trend.png")
plt.show()

plt.figure(figsize=(18, 8))
plt.plot(dates, volumes)
plt.xlabel("日期")
plt.ylabel("成交量")
plt.title("成交量走势图")
plt.grid(True)

ax = plt.gca()
ax.xaxis.set_major_locator(mdates.MonthLocator(bymonth=[1, 4, 7, 10]))
ax.xaxis.set_major_formatter(mdates.DateFormatter("%Y-%m"))

plt.xticks(rotation=45)
plt.savefig("volume_trend.png")
plt.show()

plt.figure(figsize=(18, 8))
plt.plot(dates, amounts)
plt.xlabel("日期")
plt.ylabel("金额")
plt.title("成交金额走势图")
plt.grid(True)

ax = plt.gca()
ax.xaxis.set_major_locator(mdates.MonthLocator(bymonth=[1, 4, 7, 10]))
ax.xaxis.set_major_formatter(mdates.DateFormatter("%Y-%m"))

plt.xticks(rotation=45)
plt.savefig("amount_trend.png")
plt.show()
