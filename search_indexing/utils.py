from collections import defaultdict
import nltk
nltk.data.path.append('nltk_data')
from adverts.models import Advertisement
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
import re
from search_indexing.models import SearchIndex

ps = PorterStemmer()

def tokenize(text):
    return re.findall(r'\b\w+\b', text.lower())

def index_ad(advertisement: Advertisement):
    stop_words = set(stopwords.words('english'))

    #Tokenize title and description
    title_words = tokenize(advertisement.title)
    description_words = tokenize(advertisement.description)

    #Remove stop words from title and description
    title = [ps.stem(word) for word in title_words if word not in stop_words]
    description = [ps.stem(word) for word in description_words if word not in stop_words]

    #Initiate dicts for word count and word tf
    title_word_count = defaultdict(int)
    description_word_count = defaultdict(int)
    title_tf_count = defaultdict(float)
    description_tf_count = defaultdict(float)

    #Iterate over the words to get the count
    for word in set(title):
        title_word_count[word] = title.count(word)

    for word in set(description):
        description_word_count[word] = description.count(word)

    #Iterate over the word counts to get TF
    for word in title_word_count:
        tf = title_word_count[word] / sum(title_word_count.values())
        title_tf_count[word] = tf

    for word in description_word_count:
        tf = description_word_count[word] / sum(description_word_count.values())
        description_tf_count[word] = tf

    #Create objects in index table with word, advert and TF for title and description
    for word in set([k for k in title_word_count.keys()] + [k for k in description_word_count.keys()]):
        title_tf = title_tf_count.get(word, 0)
        description_tf = description_tf_count.get(word, 0)
        SearchIndex.objects.create(
            word = word,
            advert = advertisement,
            title_tf=title_tf,
            body_tf=description_tf,
        )

