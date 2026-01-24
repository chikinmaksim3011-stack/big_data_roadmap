import requests
import json
from datetime import datetime
import pandas as pd


def extract():
    url = "https://dummyjson.com/products"
    response = requests.get(url)

    if response.status_code != 200:
        print(f"Error: {response.status_code}")
        return

    new_data = response.json()['products']

    fetched_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"Fetched at: {fetched_at}")
    print(f"Status: {response.status_code}")
    print(f"Records: {len(new_data)}")

    df = pd.DataFrame(new_data)
    unique_category = df['category'].nunique()
    print(f"Unique category: {unique_category}")
    df.to_csv('products.csv')
    with open('products.json', 'w', encoding='utf-8') as f:
        json.dump(new_data, f, ensure_ascii=False, indent=2)

if __name__ == "__main__":
    extract()