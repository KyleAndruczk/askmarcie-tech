from flask import Flask, jsonify, request
import json
import sqlite3
from flask_cors import CORS, cross_origin
import sys
import openai
# import requests
import threading
from secrets import openAIKey

# Set OpenAI API key
openai.api_key = openAIKey

# Define weights for local and global markets
local_weight = 2
global_weight = 1

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

# Load businesses data from Yelp businesses JSON file
with open('./extracted_files/yelp_academic_dataset_business.json', 'r') as f:
    businesses_data = [json.loads(line) for line in f]

# Load reviews data from Yelp reviews JSON file
with open('./ice_cream_shops_reviews.json', 'r') as f:
    reviews_data = [json.loads(line) for line in f]

# Connect to SQLite database
conn = sqlite3.connect('yelp.db', check_same_thread=False)
c = conn.cursor()

# Create businesses table in SQLite database
c.execute('CREATE TABLE IF NOT EXISTS businesses (business_id TEXT PRIMARY KEY, name TEXT, address TEXT, city TEXT, state TEXT, postal_code TEXT, latitude REAL, longitude REAL, stars REAL, review_count INTEGER, is_open INTEGER, categories TEXT, hours TEXT)')

# # Insert businesses data into SQLite database
# for business in businesses_data:
#     c.execute('INSERT INTO businesses (business_id, name, address, city, state, postal_code, latitude, longitude, stars, review_count, is_open, categories, hours) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)',
#               (business['business_id'], str(business['name']), str(business['address']), str(business['city']), str(business['state']), str(business['postal_code']), business['latitude'], business['longitude'], business['stars'], business['review_count'], business['is_open'], str(business['categories']), str(business['hours'])))

    

# # # Create reviews table in SQLite database
# c.execute('CREATE TABLE IF NOT EXISTS reviews (business_id TEXT PRIMARY KEY, name TEXT, address TEXT, city TEXT, state TEXT, postal_code TEXT, latitude REAL, longitude REAL, stars REAL, review_count INTEGER, categories TEXT, date TEXT, text TEXT, useful INTEGER, funny INTEGER, cool INTEGER)')

# # Insert reviews data into SQLite database
# for review in reviews_data:
#     c.execute('INSERT INTO reviews (business_id, name, address, city, state, postal_code, latitude, longitude, stars, review_count, categories, date, text, useful, funny, cool) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)',
#               (review['business_id'], review['name'], review['address'], review['city'], review['state'], review['postal_code'], review['latitude'], review['longitude'], review['stars'], review['review_count'], review['categories'], review['date'], review['text'], review['useful'], review['funny'], review['cool']))


# # Commit changes to database
# conn.commit()
# conn.close()

# Define a route for getting all businesses data
@app.route('/businesses')
def get_businesses():
    conn = sqlite3.connect('yelp.db')
    c = conn.cursor()
    c.execute('SELECT * FROM businesses WHERE categories LIKE "%%Ice Cream & Frozen Yogurt%%"')
    businesses = c.fetchall()
    conn.close()
    return jsonify(businesses)

# Define a route for getting all reviews data
@app.route('/reviews')
def get_reviews():
    conn = sqlite3.connect('yelp.db')
    c = conn.cursor()
    c.execute('SELECT * FROM reviews')
    reviews = c.fetchall()
    conn.close()
    return jsonify(reviews)

# Define a function to generate summaries for a business
def generate_summary(business_id, name, address, city, state, postal_code, latitude, longitude, review_count, score, ingredient, summaries):
    prompt = f"Generate a brief description of why {name} is a good match for {ingredient}."
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=prompt,
        max_tokens=50,
        n=1,
        stop=None,
        temperature=0.5
    )
    summary = response['choices'][0]['text'].strip()
    if summary:
        summaries.append({
            'business_id': business_id,
            'name': name,
            'address': address,
            'city': city,
            'state': state,
            'postal_code': postal_code,
            'latitude': latitude,
            'longitude': longitude,
            'review_count': review_count,
            'score': score,
            'summary': summary
        })
    else:
        summaries.append({
            'business_id': business_id,
            'name': name,
            'address': address,
            'city': city,
            'state': state,
            'postal_code': postal_code,
            'latitude': latitude,
            'longitude': longitude,
            'review_count': review_count,
            'score': score,
            'summary': 'Summary not available'
        })

@app.route('/ice_cream_shops', methods=['GET'])
@cross_origin()
def ice_cream_shops():
    # Get ingredient/product name from request parameters
    ingredient = request.args.get('ingredient')

    # Query database for businesses that use the ingredient/product
    c.execute("SELECT business_id, name, address, city, state, postal_code, latitude, longitude, review_count FROM businesses WHERE categories LIKE '%Ice Cream & Frozen Yogurt%'")
    rows = c.fetchall()

    # Initialize counts for local and global markets
    local_count = 0
    global_count = 0

    # Calculate counts for local and global markets
    for row in rows:
        if row[3] == 'Phoenix':
            local_count += 1
        else:
            global_count += 1

    # Calculate weights for local and global markets
    local_weighted = local_weight * local_count
    global_weighted = global_weight * global_count

    # Query reviews for the ingredient/product
    c.execute("SELECT business_id, COUNT(*) FROM reviews WHERE text LIKE ? GROUP BY business_id", ('%' + ingredient + '%',))
    review_counts = dict(c.fetchall())

    # Calculate scores for each business
    scores = []
    for row in rows:
        business_id = row[0]
        name = row[1]
        address = row[2]
        city = row[3]
        state = row[4]
        postal_code = row[5]
        latitude = row[6]
        longitude = row[7]
        review_count = row[8]

        # Get review count for the business
        count = review_counts.get(business_id, 0)

        # Calculate weight for business based on location
        if city == 'Phoenix':
            weight = local_weighted
        else:
            weight = global_weighted

        # Calculate score for business
        score = weight * count / review_count

        # Add business to scores list
        scores.append((business_id, name, address, city, state, postal_code, latitude, longitude, review_count, score))

    # Sort scores in descending order
    sorted_scores = sorted(scores, key=lambda x: x[9], reverse=True)

    # Generate summaries for the top 5 businesses
    summaries = []
    threads = []
    for i in range(min(len(sorted_scores), 10)):
        if sorted_scores:
            business_id = sorted_scores[i][0]
            name = sorted_scores[i][1]
            address = sorted_scores[i][2]
            city = sorted_scores[i][3]
            state = sorted_scores[i][4]
            postal_code = sorted_scores[i][5]
            latitude = sorted_scores[i][6]
            longitude = sorted_scores[i][7]
            review_count = sorted_scores[i][8]
            score = sorted_scores[i][9]
            thread = threading.Thread(target=generate_summary, args=(business_id, name, address, city, state, postal_code, latitude, longitude, review_count, score, ingredient, summaries))
            threads.append(thread)
            thread.start()

    # Wait for all threads to complete
    for thread in threads:
        thread.join()

    # Return summaries as JSON response
    return jsonify(summaries)
if __name__ == '__main__':
    app.run()