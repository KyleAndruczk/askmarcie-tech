# import json
# from collections import Counter
# from nltk import pos_tag, word_tokenize, WordNetLemmatizer
# import time
# from nltk.corpus import wordnet as wn
# from nltk.corpus import stopwords
# # Load Yelp JSON file
# with open("only_ice_cream_reviews.json", "r") as f:
#     data = [json.loads(line) for line in f]

# # Define a list of ice cream shop keywords
# food = wn.synset('food.n.02')
# shop_keywords = list(set([w for s in food.closure(lambda s:s.hyponyms()) for w in s.lemma_names()]))

# lemmatizer = WordNetLemmatizer()

# # Extract the first 100 reviews from ice cream shops
# reviews = [rev["text"] for rev in data[:1000]]

# # Define a function to clean and preprocess the text
# def preprocess(text):
#     # Convert text to lowercase
#     text = text.lower()
#     # Remove punctuation and newlines
#     text = "".join(char for char in text if char.isalnum() or char.isspace())
#     # Lemmatize words
#     lemmatizer = WordNetLemmatizer()
#     text = " ".join(lemmatizer.lemmatize(word) for word in word_tokenize(text))
#     return text

# # Clean and preprocess the text of each review
# start_time = time.time()
# preprocessed_reviews = [preprocess(review) for review in reviews]
# elapsed_time = time.time() - start_time
# print(f"Preprocessed {len(reviews)} reviews in {elapsed_time:.2f} seconds")

# # Define a function to extract ingredient and product mentions
# def extract_mentions(text):
#     mentions = []
#     # Tokenize the text and tag each token with its part of speech
#     tagged_tokens = pos_tag(word_tokenize(text))
#     # Define a list of part-of-speech tags that can indicate an ingredient or product
#     pos_tags = ["NN", "NNS", "JJ", "VB", "VBD", "VBG", "VBN", "VBP", "VBZ"]
#     # Extract all noun chunks and lemmatized tokens with relevant POS tags
#     for i in range(len(tagged_tokens)):
#         word, pos = tagged_tokens[i]
#         if pos in pos_tags:
#             if pos.startswith("VB"):
#                 lemma = lemmatizer.lemmatize(word, pos="v")
#             else:
#                 lemma = lemmatizer.lemmatize(word)
#             if pos.startswith("NN"):
#                 mentions.append(lemma)
#             elif pos.startswith("JJ"):
#                 if i > 0:
#                     prev_word, prev_pos = tagged_tokens[i-1]
#                     if prev_pos.startswith("NN"):
#                         mentions.append(f"{prev_word} {lemma}")
#                             # Filter out stop words
#     mentions = [word for word in mentions if word not in stopwords.words("english")]
#     return mentions

# # Extract ingredient and product mentions from each preprocessed review
# start_time = time.time()
# mentions = []
# for i, review in enumerate(preprocessed_reviews):
#     mentions.extend(extract_mentions(review))
#     if (i+1) % 10 == 0:
#         elapsed_time = time.time() - start_time
#         print(f"Extracted mentions from {i+1} reviews in {elapsed_time:.2f} seconds")
#         start_time = time.time()
# elapsed_time = time.time() - start_time
# print(f"Extracted mentions from {len(preprocessed_reviews)} reviews in {elapsed_time:.2f} seconds")

# # Count the frequency of each mention
# mention_counts = Counter(mentions)

# # Get the 20 most common mentions
# top_mentions = mention_counts.most_common(20)

# print("Top 20 mentions:")
# for mention, count in top_mentions:
#     print(f"{mention}: {count}")


# --------------------------------------------------
# API_KEY = "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"

import json
from collections import Counter
from nltk import pos_tag, word_tokenize, WordNetLemmatizer
import time
from nltk.corpus import wordnet as wn
from nltk.chunk import RegexpParser

# Load Yelp JSON file
with open("only_ice_cream_reviews.json", "r") as f:
    data = [json.loads(line) for line in f]

# Define a list of ice cream shop keywords
food = wn.synset('food.n.02')
shop_keywords = list(set([w for s in food.closure(lambda s:s.hyponyms()) for w in s.lemma_names()]))

print(shop_keywords)

lemmatizer = WordNetLemmatizer()

# Extract the first 100 reviews from ice cream shops
reviews = [rev["text"] for rev in data[:1000]]

# Define a function to clean and preprocess the text
def preprocess(text):
    # Convert text to lowercase
    text = text.lower()
    # Remove punctuation and newlines
    text = "".join(char for char in text if char.isalnum() or char.isspace())
    # Lemmatize words
    lemmatizer = WordNetLemmatizer()
    text = " ".join(lemmatizer.lemmatize(word) for word in word_tokenize(text))
    return text

# Clean and preprocess the text of each review
start_time = time.time()
preprocessed_reviews = [preprocess(review) for review in reviews]
elapsed_time = time.time() - start_time
print(f"Preprocessed {len(reviews)} reviews in {elapsed_time:.2f} seconds")

# Define a function to extract ingredient and product mentions
# def extract_mentions(text):
#     mentions = []
#     # Tokenize the text and tag each token with its part of speech
#     tagged_tokens = pos_tag(word_tokenize(text))
#     # Define a list of part-of-speech tags that can indicate an ingredient or product
#     pos_tags = ["NN", "NNS", "JJ", "VB", "VBD", "VBG", "VBN", "VBP", "VBZ"]
#     # Extract all noun chunks and lemmatized tokens with relevant POS tags
#     for i in range(len(tagged_tokens)):
#         word, pos = tagged_tokens[i]
#         if pos in pos_tags:
#             if pos.startswith("VB"):
#                 lemma = lemmatizer.lemmatize(word, pos="v")
#             else:
#                 lemma = lemmatizer.lemmatize(word)
#             if pos.startswith("NN"):
#                 mentions.append(lemma)
#             elif pos.startswith("JJ"):
#                 if i > 0:
#                     prev_word, prev_pos = tagged_tokens[i-1]
#                     if prev_pos.startswith("NN"):
#                         mentions.append(f"{prev_word} {lemma}")
#     return mentions

def extract_mentions(text):
    mentions = []
    # Tokenize the text and tag each token with its part of speech
    tagged_tokens = pos_tag(word_tokenize(text))
    # Define a list of part-of-speech tags that can indicate an ingredient or product
    pos_tags = ["NN", "NNS", "JJ", "VB", "VBD", "VBG", "VBN", "VBP", "VBZ"]
    # Extract all noun chunks and lemmatized tokens with relevant POS tags
    chunk_parser = RegexpParser('''
        NP: {<DT>?<JJ>*<NN.*>+}
    ''')
    tree = chunk_parser.parse(tagged_tokens)
    for subtree in tree.subtrees(filter=lambda t: t.label() == 'NP'):
        phrase = ' '.join([word for word, pos in subtree.leaves()])
        if any(keyword in phrase.lower() for keyword in shop_keywords):
            mentions.append(phrase)
        else:
            for i in range(len(subtree)):
                word, pos = subtree[i]
                if pos in pos_tags:
                    if pos.startswith("VB"):
                        lemma = lemmatizer.lemmatize(word, pos="v")
                    else:
                        lemma = lemmatizer.lemmatize(word)
                    if pos.startswith("NN"):
                        mentions.append(lemma)
                    elif pos.startswith("JJ"):
                        if i > 0:
                            prev_word, prev_pos = subtree[i-1]
                            if prev_pos.startswith("NN"):
                                mentions.append(f"{prev_word} {lemma}")
    return mentions

# Extract ingredient and product mentions from each preprocessed review
start_time = time.time()
mentions = []
for i, review in enumerate(preprocessed_reviews):
    mentions.extend(extract_mentions(review))
    if (i+1) % 10 == 0:
        elapsed_time = time.time() - start_time
        print(f"Extracted mentions from {i+1} reviews in {elapsed_time:.2f} seconds")
        start_time = time.time()
elapsed_time = time.time() - start_time
print(f"Extracted mentions from {len(preprocessed_reviews)} reviews in {elapsed_time:.2f} seconds")

# Count the frequency of each mention
mention_counts = Counter(mentions)

# Get the set of businesses
businesses = set([rev["business_id"] for rev in data[:1000]])


# Get the total number of businesses
num_businesses = len(businesses)

# Define a threshold for common mentions
common_threshold = 0.5

# Filter out common mentions
mentions_filtered = {m: c for m, c in mention_counts.items() if c/num_businesses < common_threshold}

# Count the frequency of each mention
mention_counts = Counter(mentions_filtered)

# Get the 20 most common mentions
top_mentions = mention_counts.most_common(200)

print("Top 20 mentions:")
for mention, count in top_mentions:
    print(f"{mention}: {count}")

# -------------------------------------------------

