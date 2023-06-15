import pymysql
import pandas as pd
import matplotlib.pyplot as plt

conn = pymysql.connect(host='localhost', user='', password='', database='douban')

query = "SELECT score, COUNT(*) AS count FROM music_top250 GROUP BY score"
df = pd.read_sql(query, conn)

conn.close()

plt.style.use('seaborn')

plt.bar(df['score'], df['count'])

plt.title('Scores Distribution')
plt.xlabel('Score')
plt.ylabel('Count')

plt.show()
