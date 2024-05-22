
from itemadapter import ItemAdapter

class CustomPipeline:
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