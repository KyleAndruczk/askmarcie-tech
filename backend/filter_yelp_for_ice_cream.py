import pandas as pd
import json
import time

# Load businesses data
start = time.time()
businesses = pd.read_json('./extracted_files/yelp_academic_dataset_business.json', lines=True)
businesses = businesses[~businesses['categories'].isna()]  # Filter out null values
businesses = businesses[businesses['categories'].str.contains("Ice Cream & Frozen Yogurt")]
print(f'There are {len(businesses)} Ice Cream shops')
# businesses = businesses.head(1000)
business_ids = businesses['business_id'].tolist()
print(f'Loaded {len(businesses)} businesses in {time.time()-start:.2f} seconds.')

# Search for reviews of those businesses
start = time.time()
with open('./extracted_files/yelp_academic_dataset_review.json', 'r') as f:
    with open('./only_ice_cream_reviews.json', 'w') as merged_file:
        for line in f:
            data = json.loads(line)
            if data['business_id'] in business_ids:
                # print(line)
                business = businesses[businesses['business_id'] == data['business_id']].iloc[0]
                merged = {
                    'business_id': data['business_id'],
                    'name': business['name'],
                    'address': business['address'],
                    'city': business['city'],
                    'state': business['state'],
                    'postal_code': business['postal_code'],
                    'latitude': business['latitude'],
                    'longitude': business['longitude'],
                    'stars': int(business['stars']),
                    'review_count': int(business['review_count']),
                    'categories': business['categories'],
                    'date': data['date'],
                    'text': data['text'],
                    'useful': int(data['useful']),
                    'funny': int(data['funny']),
                    'cool': int(data['cool'])
                }
                merged_file.write(json.dumps(merged) + '\n')
print(f'Searched for reviews in {time.time()-start:.2f} seconds.')