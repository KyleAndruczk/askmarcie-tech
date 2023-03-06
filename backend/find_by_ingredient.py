import openai
import json
import time
from collections import Counter
from secrets import openAIKey

# Set OpenAI API key
openai.api_key = openAIKey

def generate_description(business, ingredient):
    prompt = f"Generate a brief description of why {business['name']} is a good match for {ingredient}."
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=prompt,
        max_tokens=50,
        n=1,
        stop=None,
        temperature=0.5
    )
    description = response.choices[0].text.strip()
    return (business, description)

def find_top_10_ice_cream_shops(ingredient):
    start = time.time()

    # Load combined data from JSON file
    with open('yelp_combined.json') as f:
        businesses = json.load(f)

    # Separate businesses in Phoenix from businesses in other markets
    phoenix_businesses = []
    global_businesses = []
    for business in businesses:
        if business['city'] == 'Phoenix' and 'Ice Cream & Frozen Yogurt' in business['categories']:
            phoenix_businesses.append(business)
        elif 'Ice Cream & Frozen Yogurt' in business['categories']:
            global_businesses.append(business)

    # Tokenize reviews to count the number of times the ingredient is mentioned
    for business in phoenix_businesses + global_businesses:
        business['mentions'] = Counter(token.lower() for review in business['reviews'] for token in review['text'].split())
    
    # Filter out businesses that do not have any reviews that mention the ingredient
    phoenix_businesses = [business for business in phoenix_businesses if business['mentions'][ingredient.lower()] > 0]
    global_businesses = [business for business in global_businesses if business['mentions'][ingredient.lower()] > 0]

    # Sort ice cream shops by the number of times the ingredient is mentioned in their reviews
    ice_cream_shops = []
    for business in phoenix_businesses + global_businesses:
        count = business['mentions'][ingredient.lower()]
        ice_cream_shops.append((business, count))
    ice_cream_shops.sort(key=lambda x: x[1], reverse=True)

    # Generate a brief description for each of the top 10 ice cream shops using GPT
    print(f"Top 10 ice cream shops that use {ingredient}:")
    descriptions = []
    for i in range(min(10, len(ice_cream_shops))):
        business = ice_cream_shops[i][0]
        description = generate_description(business, ingredient)
        descriptions.append((business, description))
    for i, (business, description) in enumerate(descriptions):
        print(business['name'] + f" ({'Local' if business in phoenix_businesses else 'Global'}) - {description[1]}\n")

    end = time.time()
    print(f"Execution time: {end - start:.2f} seconds.")


top_10 = find_top_10_ice_cream_shops("chocolate")

