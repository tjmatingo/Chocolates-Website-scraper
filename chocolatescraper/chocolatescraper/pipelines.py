# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from scrapy.exceptions import DropItem
import mysql.connector
import psycopg2

class ChocolatescraperPipeline:
    def process_item(self, item, spider):
        return item

'''
Pipelines used to validating the data
then go to settings.py initiate pipelines
'''
class PriceToUSDPipeline:
    gbpToUsdRate = 1.2

    def process_items(self, item, spider):
        adapter = ItemAdapter(item)

        if adapter.get('price'):

            floatPrice = float(adapter['price'])

            adapter['price'] = floatPrice * self.gbpToUsdRate

            return item
        else:
            raise DropItem(f"Missing Product Price in {item}")
        

class DuplicatesPipeline:
    def __init__(self):
        self.names_seen = set()

        def process_item(self, item, spider):
            adapter = ItemAdapter(item)

            if adapter['name'] in self.names_seen:
                raise DropItem(f"Duplicate Item found: {item!r}")
            else:
                self.names_seen.add(adapter['name'])
                return item

class SavingtoMySQLPipeline(object):
    '''
    needs connector installed
    go to settings to ensure the pipeline is rendered
    '''
    def __init__(self):
        self.create_connection()
        self.id = 0

    # connection mysql db
    def create_connection(self):
        self.connection = mysql.connector.connect(
            host = 'localhost',
            user = 'root',
            password = 'root',
            database = 'chocolate_scraping',
            port = "3306"
        )
        self.curr = self.connection.cursor()

    def process_item(self, item, spider):
        self.store_db(item)
        return item

    def store_db(self, item):
        self.curr.execute(""" insert into chocolate_products (name, price, url) values (%s, %s, %s)""", (
            item["name"],
            item["price"],
            item["url"]
        ))
        self.connection.commit()
class SavingtoMyPostGresPipeline(object):

    def __init__(self):
        self.create_connection()

    # connection mysql db
    def create_connection(self):
        self.connection = psycopg2.connect(
            host = 'localhost',
            user = 'postgres',
            dbname = 'postgres',
            password = '12345678',
            database = 'chocolate_scraping',
        
        )
        self.curr = self.connection.cursor()

    def process_item(self, item, spider):
        self.store_db(item)
        return item

    def store_db(self, item):
        try: 
            self.curr.execute(""" insert into chocolate_products (namel, price, url) values (%s, %s, %s)""", (
                item["name"],
                item["price"],
                item['url']
            ))
        except BaseException as e:
            print(e)
        self.connection.commit()