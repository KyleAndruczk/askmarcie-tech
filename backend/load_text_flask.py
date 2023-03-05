from flask import Flask, jsonify
import json
import sqlite3

# app = Flask(__name__)

# Load businesses data from Yelp businesses JSON file
with open('./extracted_files/yelp_academic_dataset_business.json', 'r') as f:
    businesses_data = [json.loads(line) for line in f]

# Load reviews data from Yelp reviews JSON file
with open('./only_ice_cream_reviews.json', 'r') as f:
    reviews_data = [json.loads(line) for line in f]

# Connect to SQLite database
conn = sqlite3.connect('yelp.db')
c = conn.cursor()

# Create businesses table in SQLite database
c.execute('CREATE TABLE IF NOT EXISTS businesses (business_id TEXT PRIMARY KEY, name TEXT, address TEXT, city TEXT, state TEXT, postal_code TEXT, latitude REAL, longitude REAL, stars REAL, review_count INTEGER, is_open INTEGER, categories TEXT, hours TEXT)')

# # Insert businesses data into SQLite database
for business in businesses_data:
    c.execute('INSERT INTO businesses (business_id, name, address, city, state, postal_code, latitude, longitude, stars, review_count, is_open, categories, hours) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)',
              (business['business_id'], str(business['name']), str(business['address']), str(business['city']), str(business['state']), str(business['postal_code']), business['latitude'], business['longitude'], business['stars'], business['review_count'], business['is_open'], str(business['categories']), str(business['hours'])))

# Create reviews table in SQLite database
c.execute('CREATE TABLE IF NOT EXISTS reviews (id INTEGER PRIMARY KEY AUTOINCREMENT, business_id TEXT, name TEXT, address TEXT, city TEXT, state TEXT, postal_code TEXT, latitude REAL, longitude REAL, stars REAL, review_count INTEGER, categories TEXT, date TEXT, text TEXT, useful INTEGER, funny INTEGER, cool INTEGER)')

# Insert reviews data into SQLite database
for review in reviews_data:
    c.execute('INSERT INTO reviews (business_id, name, address, city, state, postal_code, latitude, longitude, stars, review_count, categories, date, text, useful, funny, cool) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)',
              (str(review['business_id']), str(review['name']), str(review['address']), str(review['city']), str(review['state']), str(review['postal_code']), float(review['latitude']), float(review['longitude']), float(review['stars']), int(review['review_count']), str(review['categories']), str(review['date']), str(review['text']), int(review['useful']), int(review['funny']), int(review['cool'])))


# Commit changes to database
conn.commit()
conn.close()