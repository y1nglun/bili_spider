import pymysql
from collections import defaultdict

connection = pymysql.connect(
    host="localhost",
    user="",
    password="",
    database="computer"
)

cursor = connection.cursor()

cursor.execute("SHOW COLUMNS FROM computer")
columns = [column[0] for column in cursor.fetchall()]

missing_values = defaultdict(int)
for column in columns:
    cursor.execute(f"SELECT COUNT(*) FROM computer WHERE {column} IS NULL OR {column} = ''")
    count = cursor.fetchone()[0]
    missing_values[column] = count

print("缺失值统计：")
for column, count in missing_values.items():
    print(f"{column}: {count} 条缺失值")

cursor.execute("SELECT title, COUNT(*) FROM computer GROUP BY title HAVING COUNT(*) > 1")
duplicates = cursor.fetchall()
for title, count in duplicates:
    delete_query = f"DELETE FROM computer WHERE title = '{title}' LIMIT {count - 1}"
    cursor.execute(delete_query)

delete_columns = ["cao", "size", "weight"]
for column in delete_columns:
    cursor.execute(f"ALTER TABLE computer DROP COLUMN {column}")

connection.commit()
cursor.close()
connection.close()
