# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from scrapy.exceptions import DropItem

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
