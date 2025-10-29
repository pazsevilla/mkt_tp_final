import pandas as pd
from pathlib import Path

RAW_PATH = Path("raw")

FILES = {
    "address": "address.csv",
    "channel": "channel.csv",
    "customer": "customer.csv",
    "nps_response": "nps_response.csv",
    "payment": "payment.csv",
    "product": "product.csv",
    "product_category": "product_category.csv",
    "province": "province.csv",
    "sales_order": "sales_order.csv",
    "sales_order_item": "sales_order_item.csv",
    "shipment": "shipment.csv",
    "store": "store.csv",
    "web_session": "web_session.csv",
}

def load_raw():
    data = {}
    for key, file in FILES.items():
        path = RAW_PATH / file
        df = pd.read_csv(path)
        data[key] = df
    return data
