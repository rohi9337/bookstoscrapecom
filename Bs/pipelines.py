# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter


class BsPipeline:
    
    conversion_rate = 1.25  # Sample conversion rate; adjust as needed

    def process_item(self, item, spider):
        # Convert price to dollars
        price_value = float(item['price'].replace('£', ''))
        item['price'] = f"${price_value * self.conversion_rate:.2f}"

        # Extract availability number and format as requested
        availability_text = item['availability']
        availability_number = ''.join(filter(str.isdigit, availability_text))
        item['availability'] = f"{availability_number} available"

        return item
      # Bs/pipelines.py

# from sqlalchemy.orm import sessionmaker
# from .models import Book, get_engine, create_tables

# class DatabasePipeline:
#     def __init__(self):
#         create_tables()
#         engine = get_engine()
#         self.Session = sessionmaker(bind=engine)

#     def process_item(self, item, spider):
#         session = self.Session()
#         book = Book(
#             title=item['title'],
#             price=float(item['price'].replace('$', '')),
#             availability=item['availability'],
#             rating=item['rating'],
#             image_url=item['image_url'],
#             product_page_url=item['product_page_url'],
#             upc=item['upc'],
#             product_type=item['product_type'],
#             price_excl_tax=float(item['price_excl_tax'].replace('£', '')),
#             price_incl_tax=float(item['price_incl_tax'].replace('£', '')),
#             tax=float(item['tax'].replace('£', '')),
#             number_of_reviews=int(item['number_of_reviews'])
#         )
#         try:
#             session.add(book)
#             session.commit()
#         except:
#             session.rollback()
#             raise
#         finally:
#             session.close()
#         return item
import pandas as pd

class ExcelPipeline:
    def __init__(self):
        self.items = []

    def process_item(self, item, spider):
        self.items.append(dict(item))
        return item

    def close_spider(self, spider):
        df = pd.DataFrame(self.items)
        df.to_excel('scraped_data.xlsx', index=False)