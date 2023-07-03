# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import mysql.connector


class JyksPipeline:
    def __init__(self, mysql_host, mysql_port, mysql_database, mysql_user, mysql_password):
        self.mysql_host = mysql_host
        self.mysql_port = mysql_port
        self.mysql_database = mysql_database
        self.mysql_user = mysql_user
        self.mysql_password = mysql_password

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            mysql_host=crawler.settings.get('MYSQL_HOST'),
            mysql_port=crawler.settings.get('MYSQL_PORT'),
            mysql_database=crawler.settings.get('MYSQL_DATABASE'),
            mysql_user=crawler.settings.get('MYSQL_USER'),
            mysql_password=crawler.settings.get('MYSQL_PASSWORD'),
        )

    def open_spider(self, spider):
        self.connection = mysql.connector.connect(
            host=self.mysql_host,
            port=self.mysql_port,
            database=self.mysql_database,
            user=self.mysql_user,
            password=self.mysql_password,
        )
        self.cursor = self.connection.cursor()

    def close_spider(self, spider):
        self.connection.close()

    def process_item(self, item, spider):
        table_name = 'book'
        if not self.table_exists(table_name):
            self.create_table(table_name)

        sql = "INSERT INTO book (title, author, price, wordCount) VALUES (%s, %s, %s, %s)"
        values = (item['name'], item['author'], item['price'], item['wordCount'])
        self.cursor.execute(sql, values)
        self.connection.commit()
        return item

    def table_exists(self, table_name):
        sql = "SHOW TABLES LIKE %s"
        self.cursor.execute(sql, (table_name,))
        result = self.cursor.fetchone()
        return result is not None

    def create_table(self, table_name):
        sql = """
            CREATE TABLE IF NOT EXISTS book (
                id INT AUTO_INCREMENT PRIMARY KEY,
                title VARCHAR(255),
                author VARCHAR(255),
                price DECIMAL(10, 2),
                wordCount INT
            )
        """
        self.cursor.execute(sql)
        self.connection.commit()

