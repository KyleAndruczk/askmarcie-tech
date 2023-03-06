# import json
# from collections import Counter
# import re
# import nltk
# nltk.download('stopwords')
# from nltk.corpus import stopwords
# from nltk.corpus import wordnet

# def find_common_phrases(file_path):
#     """
#     Find the most common 2 to 3 word phrases in the 'text' attribute of a JSON file after eliminating stopwords.
#     """
#     with open(file_path, 'r') as f:
#         data = [json.loads(line) for line in f]

#     data = data[:500]
#     # Concatenate the text attribute of all JSON objects
#     text = ' '.join([d['text'] for d in data])
#     # Remove punctuation and convert to lowercase
#     text = re.sub(r'[^\w\s]', '', text).lower()
#     # Split the text into words
#     words = text.split()
#     # Eliminate stopwords
#     words = [word for word in words if word not in stopwords.words('english')]
#     # Join the words back into a string
#     text = ' '.join(words)
#     # Find all 2 to 3 word phrases
#     phrases = re.findall(r'\b\w+\s\w+\b|\b\w+\s\w+\s\w+\b', text)
#     # Keep only phrases that are categorically related to food
#     food_phrases = []
#     for phrase in phrases:
#         # Check if any word in the phrase is categorically related to food
#         is_food_related = any(wordnet.synsets(word, pos='n') and wordnet.synsets(word, pos='n')[0].hypernyms() and 'food' in wordnet.synsets(word, pos='n')[0].hypernyms()[0].name() for word in phrase.split())
#         if is_food_related:
#             food_phrases.append(phrase)
#     # Count the occurrence of each food-related phrase
#     phrase_counts = Counter(food_phrases)
#     # Return the 10 most common food-related phrases
#     return phrase_counts.most_common(100)

# # Example usage
# file_path = 'only_ice_cream_reviews.json'
# common_phrases = find_common_phrases(file_path)
# print(common_phrases) # Output: [('new york', 4), ('central park', 3), ('york city', 3), ('metropolitan museum', 2), ('american museum', 2), ('museum natural', 2), ('natural history', 2), ('empire state', 2), ('state building', 2), ('statue liberty', 2)]


# ---------------------------------------------------
# !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

# import json
# from collections import Counter
# import re
# import nltk
# nltk.download('stopwords')
# from nltk.corpus import stopwords
# from nltk.corpus import wordnet

# def find_common_food_phrases(file_path):
#     """
#     Find the most common 2 to 3 word phrases in the 'text' attribute of a JSON file that are categorically related to food.
#     """
#     # Define a list of food-related keywords
#     food = wordnet.synset('food.n.02')

#     food_keywords = ['food', 'cuisine', 'dish', 'meal', 'snack', 'ingredient', 'recipe', 'menu', 'restaurant', 'eatery', 'dining', 'gastronomy', 'cooking', 'drink', 'beverage', 'alcohol'] + list(set([w for s in food.closure(lambda s:s.hyponyms()) for w in s.lemma_names()]))
#     # Expand the set of food-related words using WordNet
#     food_related_words = set()
#     for keyword in food_keywords:
#         synsets = wordnet.synsets(keyword)
#         for synset in synsets:
#             # Add all lemmas of the synset to the set of food-related words
#             for lemma in synset.lemmas():
#                 food_related_words.add(lemma.name().lower())
#             # Add all hyponyms of the synset to the set of food-related words
#             for hyponym in synset.hyponyms():
#                 for lemma in hyponym.lemmas():
#                     food_related_words.add(lemma.name().lower())
#             # Add all hypernyms of the synset to the set of food-related words
#             for hypernym in synset.hypernyms():
#                 for lemma in hypernym.lemmas():
#                     food_related_words.add(lemma.name().lower())
    
#     # Load the JSON file
#     with open(file_path) as f:
#          data = [json.loads(line) for line in f]

#     data = data[:500]
    
#     # Define a regular expression to remove non-alphabetic characters from the text
#     pattern = re.compile('[^a-zA-Z ]')
    
#     # Define a set of stopwords
#     stop_words = set(stopwords.words('english'))
    
#     # Define a Counter object to count the occurrences of each phrase
#     phrase_counter = Counter()
    
#     # Iterate over the objects in the JSON file
#     for obj in data:
#         # Remove non-alphabetic characters from the text
#         text = pattern.sub(' ', obj['text'])
#         # Tokenize the text
#         tokens = text.lower().split()
#         # Remove stopwords
#         tokens = [token for token in tokens if token not in stop_words]
#         # Find all 2 to 3 word phrases
#         phrases = []
#         for i in range(len(tokens)):
#             if i < len(tokens) - 1:
#                 phrases.append(tokens[i] + ' ' + tokens[i+1])
#             if i < len(tokens) - 2:
#                 phrases.append(tokens[i] + ' ' + tokens[i+1] + ' ' + tokens[i+2])
#         # Count the occurrences of each phrase that contains at least one food-related word
#         for phrase in phrases:
#             if any(word in phrase for word in food_related_words):
#                 phrase_counter[phrase] += 1
    
#     # Return the 10 most common phrases
#     return phrase_counter.most_common(100)

# file_path = 'only_ice_cream_reviews.json'
# common_phrases = find_common_food_phrases(file_path)
# print(common_phrases) # Output: [('new york', 4), ('central park', 3), ('york city', 3), ('metropolitan museum', 2), ('american museum', 2), ('museum natural', 2), ('natural history', 2), ('empire state', 2), ('state building', 2), ('statue liberty', 2)]

# -----------------------------------------------------

# import json
# from collections import Counter
# import re
# import nltk
# nltk.download('stopwords')
# from nltk.corpus import stopwords
# from nltk.corpus import wordnet

# def find_common_food_phrases(file_path):
#     """
#     Find the most common 2 to 3 word phrases in the 'text' attribute of a JSON file that are categorically related to food.
#     """
#     # Define a list of food-related keywords
#     food_keywords = ['food', 'cuisine', 'dish', 'meal', 'snack', 'ingredient', 'recipe', 'menu', 'restaurant', 'eatery', 'dining', 'gastronomy', 'cooking', 'drink', 'beverage', 'alcohol']
#     # Expand the set of food-related words using WordNet
#     food_related_words = set()
#     for keyword in food_keywords:
#         synsets = wordnet.synsets(keyword)
#         for synset in synsets:
#             # Add all lemmas of the synset to the set of food-related words
#             for lemma in synset.lemmas():
#                 food_related_words.add(lemma.name().lower())
#             # Add all hyponyms of the synset to the set of food-related words
#             for hyponym in synset.hyponyms():
#                 for lemma in hyponym.lemmas():
#                     food_related_words.add(lemma.name().lower())
#             # Add all hypernyms of the synset to the set of food-related words
#             for hypernym in synset.hypernyms():
#                 for lemma in hypernym.lemmas():
#                     food_related_words.add(lemma.name().lower())
    
#     # Define a regular expression to remove non-alphabetic characters from the text
#     pattern = re.compile('[^a-zA-Z ]')
    
#     # Define a set of stopwords
#     stop_words = set(stopwords.words('english'))
    
#     # Define a set of food-related nouns
#     food_nouns = set(['food', 'cuisine', 'dish', 'meal', 'snack', 'ingredient', 'recipe', 'menu', 'restaurant', 'eatery', 'dining', 'gastronomy'])
    
#     # Define a Counter object to count the occurrences of each phrase
#     phrase_counter = Counter()
    
#     # Iterate over the objects in the JSON file
#     with open(file_path) as f:
#         data = [json.loads(line) for line in f]

#     data = data[:500]
    
    
#     for obj in data:
#         # Remove non-alphabetic characters from the text
#         text = pattern.sub(' ', obj['text'])
#         # Tokenize the text
#         tokens = text.lower().split()
#         # Remove stopwords
#         tokens = [token for token in tokens if token not in stop_words]
#         # Find all 2 to 3 word phrases
#         phrases = []
#         for i in range(len(tokens)):
#             if i < len(tokens) - 1:
#                 phrases.append(tokens[i] + ' ' + tokens[i+1])
#             if i < len(tokens) - 2:
#                 phrases.append(tokens[i] + ' ' + tokens[i+1] + ' ' + tokens[i+2])
#         # Count the occurrences of each phrase that contains at least one food-related word
#         for phrase in phrases:
#              # Use regular expressions to match only phrases that contain certain food-related nouns
#             if re.search(r'\b(' + '|'.join(food_nouns) + r')\b', phrase):
#                 # Count the phrase if it contains at least one food-related word
#                 if any(word in food_related_words for word in phrase.split()):
#                     phrase_counter[phrase] += 1

#     # Return the most common phrases
#     return phrase_counter.most_common(10)

# file_path = 'only_ice_cream_reviews.json'
# common_phrases = find_common_food_phrases(file_path)
# print(common_phrases) # Output: [('new york', 4), ('central park', 3), ('york city', 3), ('metropolitan museum', 2), ('american museum', 2), ('museum natural', 2), ('natural history', 2), ('empire state', 2), ('state building', 2), ('statue liberty', 2)]

# -------------------------------------------------


# import json
# import re
# from collections import Counter
# from nltk.corpus import stopwords
# from nltk.tokenize import word_tokenize, sent_tokenize
# from nltk.tag import pos_tag

# def get_common_phrases(file_path):
#     # Load the JSON file
#     with open(file_path) as f:
#         data = [json.loads(line) for line in f]

#     data = data[:100]

#     # Define the stop word list
#     stop_words = set(stopwords.words('english'))

#     # Define the food-related words and nouns
#     food_related_words = set(['food', 'restaurant', 'menu', 'dish', 'cuisine'])
#     food_nouns = set(['food', 'dish', 'cuisine', 'restaurant', 'menu', 'ingredient', 'flavor', 'taste'])

#     # Initialize a counter for the phrases
#     phrase_counter = Counter()

#     # Loop through the sentences in the JSON data
#     for review in data:
#         sentences = sent_tokenize(review['text'])
#         for sentence in sentences:
#             # Tokenize the sentence and tag the parts of speech
#             words = word_tokenize(sentence.lower())
#             tagged_words = pos_tag(words)

#             # Extract only the noun phrases
#             noun_phrases = []
#             for i in range(len(tagged_words)):
#                 if tagged_words[i][1].startswith('N'):
#                     phrase = tagged_words[i][0]
#                     for j in range(i+1, len(tagged_words)):
#                         if tagged_words[j][1].startswith('N'):
#                             phrase += ' ' + tagged_words[j][0]
#                         else:
#                             break
#                     noun_phrases.append(phrase)

#             # Filter out stop words and phrases that do not contain food-related nouns
#             for phrase in noun_phrases:
#                 if not any(word in food_related_words for word in phrase.split()):
#                     continue
#                 if any(word in stop_words for word in phrase.split()):
#                     continue
#                 if re.search(r'\b(' + '|'.join(food_nouns) + r')\b', phrase):
#                     phrase_counter[phrase] += 1
    
#     # Return the most common phrases
#     return phrase_counter.most_common(10)

# file_path = 'only_ice_cream_reviews.json'
# common_phrases = get_common_phrases(file_path)
# print(common_phrases) # Output: [('new york', 4), ('central park', 3), ('york city', 3), ('metropolitan museum', 2), ('american museum', 2), ('museum natural', 2), ('natural history', 2), ('empire state', 2), ('state building', 2), ('statue liberty', 2)]

#____________________________________________________________

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
print(common_phrases) # Output: [('new york', 4), ('central park', 3), ('york city', 3), ('metropolitan museum', 2), ('american museum', 2), ('museum natural', 2), ('natural history', 2), ('empire state', 2), ('state building', 2), ('statue liberty', 2)]

# list_of_tuples = [('apple', 2), ('banana', 3), ('car', 4), ('cheese', 5), ('milk', 6)]

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


