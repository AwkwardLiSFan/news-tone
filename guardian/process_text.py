# this program pre-processes the text in order to prepare it for analysis

# import the necessary packages
import csv
import re
import json
import string
import nltk
from nltk.tokenize import word_tokenize
from nltk.stem import PorterStemmer
from nltk.stem import WordNetLemmatizer
from nltk.corpus import stopwords
from nltk.corpus import wordnet
from nltk.corpus import sentiwordnet as swn
from appos import appos_list

# getting the stopwords from the nltk corpus for future use
stop_words = stopwords.words('english')
# define punctuation
punctuations = '''!()-[]{};:'"\,<>./?@#$%^&*_~'''
# creating an object of class PorterStemmer
porter = PorterStemmer()
# creating an object of class WordNetLemmatizer
lemmatizer = WordNetLemmatizer()

# function to clean-up heading
def clean_text(text):
    # making heading lowercase
    text = text.lower()
    text = text.lstrip('\n')
    if (text[0] == text[-1]) and text.startswith(("'", '"')):
        text = text[1:-1]
    # split each heading into words
    words = text.split()
    # edit apostrophe words: can't, don't, won't
    for word in words:
        if word in appos_list:
            word = appos_list[word]
            word = " ".join(word)
    return text

# function to remove punctuation
def remove_punctuation(text):
    text = ''.join([c for c in text if c not in string.punctuation])
    return text

# function to remove special characters
def remove_special_characters(text):
    # define the pattern to keep
    pat = r'[^a-zA-z0-9.,!?/:;\"\'\s]'
    return re.sub(pat, '', text)

# function to lemmatize the sentence
def lemmatize_text(text):
    tag = nltk.pos_tag([text])[0][1][0].upper()
    if tag.startswith('J'):
        return wordnet.ADJ
    elif tag.startswith('V'):
        return wordnet.VERB
    elif tag.startswith('N'):
        return wordnet.NOUN
    elif tag.startswith('R'):
        return wordnet.ADV
    elif tag.startswith('S'):
        return wordnet.ADJ_SAT
    else:
        return ''

# loading the articles from .json file
with open('articleData_Guardian.json', encoding='utf-8') as json_data:
    jsonData = json.load(json_data)

# list of all lemmas to compare against in order to filter out the words that
# don't exist in WordNet, for e.g. names like Boris Johnson
wn_lemmas = set(wordnet.all_lemma_names())

# array that stores all the articles for analysis later
data_to_write = []

#
def sent_analysis(text):
    # call all the functions in order to clean up the text
    heading = clean_text(text)
    heading = remove_special_characters(heading)
    heading = remove_punctuation(heading)

    # get a list of all tokens in the heading
    tokens = word_tokenize(heading)

    # removing stopwords
    tokens_cleaned = []
    for j in tokens:
        if j not in stop_words:
            tokens_cleaned.append(j)

    # creating an array of lemmatized tokens
    lemmatized_tokens = [lemmatizer.lemmatize(w, lemmatize_text(w)) for w in tokens_cleaned if lemmatize_text(w) != '']

    # assigning a sentiment score of 0.0 plus creating array to store scores
    # of all the words in a sentence
    sentiment = 0.0
    sentiments = []
    for i in lemmatized_tokens:
            pos = 0.0
            neg = 0.0
            if i in wn_lemmas and lemmatize_text(i) != '':
                swn_synset_1 = list(swn.senti_synsets(i, lemmatize_text(i)))
                if swn_synset_1:
                    swn_synset = swn_synset_1[0]
                    pos += swn_synset.pos_score()
                    neg += swn_synset.neg_score()
                else:
                    break
            sentiment = pos-neg
            sentiments.append(sentiment)

#    sentiment = sum(sentiments)/len(lemmatized_tokens)
    sentiment = sum(sentiments)
    s = ""
#    if sentiment >= 0.01:
    if sentiment > 0:
        s = "Positive"
        print(text)
        print("Lemmatized: ", lemmatized_tokens)
        print("net sentiment: ", sum(sentiments))
        print("Predicted sentiment: Positive\n")
#    elif sentiment <= -0.01:
    elif sentiment < 0:
        s = "Negative"
        print(text)
        print("Lemmatized: ", lemmatized_tokens)
        print("net sentiment: ", sum(sentiments))
        print("Predicted sentiment: Negative\n")
    else:
        s = "Neutral"
        print(text)
        print("Lemmatized: ", lemmatized_tokens)
        print("net sentiment: ", sum(sentiments))
        print("Predicted sentiment: Neutral\n")

    writeObject = {
        'article': text,
        's_score': sentiment,
        'sent': s
    }

    data_to_write.append(writeObject)

# calculating the sentiment scores for all 572 headings
for i in range(572):
    # simply change 'body' to 'head' and the headings will be processed instead
    sent_analysis(jsonData[i]['head'])

# copying heading data 
h_data_to_write = data_to_write 

# make data_to_write empty again to store article data
data_to_write = []

# calculating the sentiment scores for all 572 articles
for i in range(572):
    # simply change 'body' to 'head' and the headings will be processed instead
    sent_analysis(jsonData[i]['body'])

# writing the outcome to a .csv file
with open('guardian/guardian_articles.csv', 'w', newline='', encoding='utf-8') as file:
    fieldnames = ['head','head_sentiment','head_sntmnt','body','sentiment_score','sntmnt']
    writer = csv.DictWriter(file, fieldnames=  fieldnames)
    writer.writeheader()
    for i in range(572):
        writer.writerow({'head': h_data_to_write[i]['article'], 'head_sentiment': h_data_to_write[i]['s_score'], 'head_sntmnt': h_data_to_write[i]['sent'], 'body': data_to_write[i]['article'], 'sentiment_score': data_to_write[i]['s_score'], 'sntmnt': data_to_write[i]['sent']})
