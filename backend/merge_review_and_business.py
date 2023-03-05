import json
import time

start = time.time()


# Load businesses data from JSON file
print("Loading businesses data...")
with open('./extracted_files/yelp_academic_dataset_business.json') as f:
    businesses = [json.loads(line) for line in f if 'Ice Cream & Frozen Yogurt' in line]


    # businesses = businesses[:1000]
# Load reviews data from JSON file
print("Loading reviews data...")
with open('./only_ice_cream_reviews.json') as f:
    reviews = [json.loads(line) for line in f]

# Create a dictionary of reviews for each business
print("Creating a dictionary of reviews for each business...")
business_reviews = {}
for review in reviews:
    business_id = review['business_id']
    if business_id not in business_reviews:
        business_reviews[business_id] = []
    business_reviews[business_id].append(review)

# Add reviews to businesses data
print("Adding reviews to businesses data...")
for business in businesses:
    business_id = business['business_id']
    if business_id in business_reviews:
        business['reviews'] = business_reviews[business_id]

# Write combined data to new JSON file
print("Writing combined data to a new JSON file...")
with open('yelp_combined.json', 'w') as f:
    json.dump(businesses, f, indent=2)

end = time.time()
print(f"Time taken: {end - start:.2f} seconds")