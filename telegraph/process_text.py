# this program pre-processes the text in order to prepare for analysis

# import the necessary packages
import csv
import json
import string
import nltk
import re 
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

# function to remove special characters
def remove_special_characters(text):
    # define the pattern to keep
    pat = r'[^a-zA-z0-9.,!?/:;\"\'\s]'
    return re.sub(pat, '', text)

# function to stem the sentence
def stem_text(text):
    stem_heading = []
    for word in text:
        stem_heading.append(porter.stem(word))
    return stem_heading

# function to lemmatize the sentence
def lemmatize_text(text):
#    pos_tags = []
#    pos_tags.append(nltk.pos_tag(text))
#    print(pos_tags)
    if (text == 'reclaims' or text == 'reclaim'):
        return wordnet.VERB
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
with open('telegraph/articleData_telegraph.json', encoding='utf-8') as json_data:
    jsonData = json.load(json_data)
# list of all lemmas to compare against in order to filter out the words that
# don't exist in WordNet, for e.g. names
wn_lemmas = set(wordnet.all_lemma_names())

# final array of all news articles to write to the .csv file
data_to_write = []

# function to handle the sentiment analysis of text provided as an argument
def sent_analysis(text):
    heading = clean_text(text)
    heading = remove_special_characters(heading)
    # get a list of all tokens in the heading
    tokens = word_tokenize(heading)
    # removing stopwords
    tokens_cleaned = []
    for j in tokens:
        if j not in stop_words:
            if j not in punctuations:
                tokens_cleaned.append(j)

    lemmatized_tokens = [lemmatizer.lemmatize(w, lemmatize_text(w)) for w in tokens_cleaned if lemmatize_text(w) != '']

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

    sentiment = sum(sentiments)
    s = ""
    if sentiment > 0:
        s = "Positive"
        print(text)
        print("Lemmatized: ", lemmatized_tokens)
        print("net sentiment: ", sum(sentiments))
        print("Predicted sentiment: Positive\n")
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

# run sentiment analysis over headings
for i in range(779):
    sent_analysis(jsonData[i]['head'])

# copy heading data
h_data_to_write = data_to_write

# make data_to_write empty again for the article body
data_to_write = []

# run sentiment analysis over articles
for i in range(779):
    sent_analysis(jsonData[i]['body'])

# write the outcome to a .csv file
with open('telegraph/telegraph_articles.csv', 'w', newline='', encoding='utf-8') as file:
    fieldnames = ['head','head_sentiment','head_snmnt','body','sentiment_score','sntmnt']
    writer = csv.DictWriter(file, fieldnames=  fieldnames)
    writer.writeheader()
    for i in range(779):
        writer.writerow({'head': h_data_to_write[i]['article'], 'head_sentiment': h_data_to_write[i]['s_score'], 'head_snmnt': h_data_to_write[i]['sent'], 'body': data_to_write[i]['article'], 'sentiment_score': data_to_write[i]['s_score'], 'sntmnt': data_to_write[i]['sent']})
