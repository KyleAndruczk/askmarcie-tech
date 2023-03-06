import json
from collections import Counter, defaultdict
import re
import nltk
nltk.download('stopwords')
from nltk.corpus import stopwords
from nltk.corpus import wordnet
import time


def find_common_food_phrases(file_path):
    """
    Find the most common 2 to 3 word phrases in the 'text' attribute of a JSON file that are categorically related to food.
    """
    # Define a list of food-related keywords
    food = wordnet.synset('food.n.02')

    food_keywords = ['food', 'cuisine', 'dish', 'meal', 'snack', 'ingredient', 'recipe', 'menu', 'restaurant', 'eatery', 'dining', 'gastronomy', 'cooking', 'drink', 'beverage', 'alcohol'] + list(set([w for s in food.closure(lambda s:s.hyponyms()) for w in s.lemma_names()]))
    # Expand the set of food-related words using WordNet
    food_related_words = set()
    for keyword in food_keywords:
        synsets = wordnet.synsets(keyword)
        for synset in synsets:
            # Add all lemmas of the synset to the set of food-related words
            for lemma in synset.lemmas():
                food_related_words.add(lemma.name().lower())
            # Add all hyponyms of the synset to the set of food-related words
            for hyponym in synset.hyponyms():
                for lemma in hyponym.lemmas():
                    food_related_words.add(lemma.name().lower())
            # Add all hypernyms of the synset to the set of food-related words
            for hypernym in synset.hypernyms():
                for lemma in hypernym.lemmas():
                    food_related_words.add(lemma.name().lower())
    
    # Load the JSON file
    with open(file_path) as f:
         data = [json.loads(line) for line in f]

    # data = data[:15000]

    print("data len " + str(len(data)))
    
    # Define a regular expression to remove non-alphabetic characters from the text
    pattern = re.compile('[^a-zA-Z ]')

    # Define a set of stopwords
    stop_words = set(stopwords.words('english'))

    # Define a Counter object to count the occurrences of each phrase
    phrase_counter = Counter()

    # Define a dictionary to store the review ratings associated with each phrase
    phrase_ratings = defaultdict(list)

    # Iterate over the objects in the JSON file
    for obj in data:
        # Remove non-alphabetic characters from the text
        text = pattern.sub(' ', obj['text'])
        # Tokenize the text
        tokens = text.lower().split()
        # Remove stopwords
        tokens = [token for token in tokens if token not in stop_words]
        # Find all 2 to 3 word phrases
        phrases = []
        for i in range(len(tokens)):
            if i < len(tokens) - 1:
                phrases.append(tokens[i] + ' ' + tokens[i+1])
            if i < len(tokens) - 2:
                phrases.append(tokens[i] + ' ' + tokens[i+1] + ' ' + tokens[i+2])
        # Count the occurrences of each phrase that contains at least one food-related word
        for phrase in phrases:
            if any(word in phrase for word in food_related_words):
                # Add the review rating to the list of ratings associated with the phrase
                phrase_ratings[phrase].append(obj['stars'])
                # Increment the count for the phrase
                phrase_counter[phrase] += 1

    # Calculate the average review rating for each phrase and add it to the phrase_counter
    for phrase in phrase_counter:
        if phrase in phrase_ratings:
            average_rating = sum(phrase_ratings[phrase]) / len(phrase_ratings[phrase])
            phrase_counter[phrase] = (phrase_counter[phrase], average_rating)

    # Return the 10 most common phrases
    return phrase_counter.most_common(100)

start_time = time.time()

file_path = 'only_ice_cream_reviews.json'
common_phrases = find_common_food_phrases(file_path)
print(common_phrases) 



end_time = time.time()


print("Execution time:", end_time - start_time, "seconds")

food_related_tuples = []

# Define a set of keywords related to food
food_keywords = {'fruit', 'vegetable', 'meat', 'dairy', 'grain', 'snack', 'dessert', 'beverage'}

# Define a function to check if a word is related to food
def is_food(word):
    # Check if the word is in the set of food-related keywords
    if word.lower() in food_keywords:
        return True
    # Check if the word is a synset (a group of synonyms) related to food
    synsets = wordnet.synsets(word, pos='n')
    for synset in synsets:
        if 'food' in synset.lexname():
            return True
    return False

# Iterate over each tuple and check if the first element is related to food
for t in common_phrases:
    # Tokenize the first element of the tuple into words
    words = nltk.word_tokenize(t[0])
    # Check if any of the words are related to food
    if any(is_food(w) for w in words):
        food_related_tuples.append(t)
print("_________________________________________")

print(food_related_tuples)
# open the file in write mode
with open('top_20_phrases_full.txt', 'w') as f:
    for item in food_related_tuples:
        line = str(item) + '\n'

        f.write(line)


