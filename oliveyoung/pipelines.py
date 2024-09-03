# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
# from itemadapter import ItemAdapter
# import pymongo
# from pymongo import MongoClient
# from scrapy.exceptions import DropItem
# from scrapy import Request
# from scrapy.utils.project import get_project_settings


class OliveyoungPipeline:
    # def __init__(self,):
    #     self.product_ids = set()
    #     settings = get_project_settings()
    #     mongo_url = settings.get("MONGO_URI")
    #     self.client = MongoClient(mongo_url)
    #     self.db = self.client[settings.get("MONGO_DATABASE")]

    # def open_spider(self, spider):
    #     collection = self.db["product_urls"]
    #     cursor = collection.find()
    #     for doc in cursor:
    #         spider.start_urls.append(doc["url"])

    # def close_spider(self, spider):
    #     self.client.close()

    # def process_item(self, item, spider):
    #     self.db["products"].update_one({"_id": item["_id"]}, {"$set": dict(item)}, True)
    #     return item
    pass
