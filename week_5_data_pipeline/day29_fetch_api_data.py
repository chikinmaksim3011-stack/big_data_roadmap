# Fetch public data from dummyjson.com API
# Saves to CSV and JSON with metadata logging

import requests
from datetime import datetime
import pandas as pd
import json


def fetch_posts():
    url = "https://dummyjson.com/posts"
    response = requests.get(url)

    if response.status_code != 200:
        print(f"{response.status_code}: {response.text}")
        return

    posts = response.json()['posts']

    fetched_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"Fetched at: {fetched_at}")
    print(f"Status: {response.status_code}")
    print(f"Records: {len(posts)}")
    df = pd.DataFrame(posts)
    df.to_csv('posts.csv')
    with open('posts.json', 'w', encoding='utf-8') as f:
        json.dump(posts, f, ensure_ascii=False, indent=2)

if __name__ == '__main__':
    fetch_posts()