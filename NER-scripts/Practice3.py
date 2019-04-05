import nltk
from nltk.tag.stanford import StanfordNERTagger
from nltk.chunk import conlltags2tree, tree2conlltags
from sklearn.tree import DecisionTreeClassifier
from sklearn.feature_extraction import DictVectorizer
from sklearn.pipeline import Pipeline
from nltk import word_tokenize, ne_chunk, pos_tag
import pandas
from nltk.corpus import wordnet
from nltk.stem import WordNetLemmatizer
import math
import re, string, timeit
import csv

exclude = set(string.punctuation)
table = str.maketrans('', '', string.punctuation)
regex = re.compile('[%s]' % re.escape(string.punctuation))
jar = './stanford-ner.jar'
model = './finalTrainSet-EnglishReddit-Acc96.gz'

# Prepare NER tagger with english model
ner_tagger = StanfordNERTagger(model, jar, encoding='utf8')


tagged_sentences = nltk.corpus.treebank.tagged_sents()


def get_wordnet_pos(word):
    tag = nltk.pos_tag([word])[0][1][0].upper()
    tag_dict = {"J": wordnet.ADJ,
                "N": wordnet.NOUN,
                "V": wordnet.VERB,
                "R": wordnet.ADV}

    return tag_dict.get(tag, wordnet.NOUN)


def features(sentence, index):
    return {
        'word': sentence[index],
        'is_first': index == 0,
        'is_last': index == len(sentence) - 1,
        'is_capitalized': sentence[index][0].upper() == sentence[index][0],
        'is_all_caps': sentence[index].upper() == sentence[index],
        'is_all_lower': sentence[index].lower() == sentence[index],
        'prefix-1': sentence[index][0],
        'prefix-2': sentence[index][:2],
        'prefix-3': sentence[index][:3],
        'suffix-1': sentence[index][-1],
        'suffix-2': sentence[index][-2:],
        'suffix-3': sentence[index][-3:],
        'prev_word': '' if index == 0 else sentence[index - 1],
        'next_word': '' if index == len(sentence) - 1 else sentence[index + 1],
        'has_hyphen': '-' in sentence[index],
        'is_numeric': sentence[index].isdigit(),
        'capitals_inside': sentence[index][1:].lower() != sentence[index][1:]
    }


def untag(tagged_sentence):
    return [w for w, t in tagged_sentence]


# Split the dataset for training and testing
cutoff = int(.75 * len(tagged_sentences))
training_sentences = tagged_sentences[:cutoff]
test_sentences = tagged_sentences[cutoff:]

def test_trans(s):
    return s.translate(table)

def transform_to_dataset(tagged_sentences):
    X, y = [], []

    for tagged in tagged_sentences:
        for index in range(len(tagged)):
            X.append(features(untag(tagged), index))
            y.append(tagged[index][1])

    return X, y


X, y = transform_to_dataset(training_sentences)

clf = Pipeline([
    ('vectorizer', DictVectorizer(sparse=False)),
    ('classifier', DecisionTreeClassifier(criterion='entropy'))
])

clf.fit(X[:10000],
        y[:10000])  # Use only the first 10K samples if you're running it multiple times. It takes a fair bit :)


X_test, y_test = transform_to_dataset(test_sentences)

print("Accuracy:", clf.score(X_test, y_test))




lemmatizer = WordNetLemmatizer()

# submissions = pandas.read_csv("./submissions (2).csv")

# for index, row in submissions.iterrows():
#     if row['title'] is not None and not pandas.isna(row['title']):
#         words = tree2conlltags(ne_chunk(pos_tag(word_tokenize(row['title']))))
#         newState = ''
#         nerState = ''
#         for tup in words:
#             # 2. Lemmatize Single Word with the appropriate POS tag
#             currStr = test_trans(tup[0])
#             if words[len(words)-1] == tup:
#                 if currStr is not None:
#                     newState += lemmatizer.lemmatize(currStr, get_wordnet_pos(tup[0])) + "."
#                     nerState += tup[2]
#             else:
#                 if currStr is not None:
#                     newState += lemmatizer.lemmatize(currStr, get_wordnet_pos(tup[0])) + " "
#                     nerState += tup[2] + " "
#         submissions.loc[index, 'title'] = newState
#         submissions.loc[index, 'titlener'] = nerState
#     print("First: ", index, "/", submissions.size)



# for index, row in submissions.iterrows():
#     if row['selftext'] is not None and not pandas.isna(row['selftext']):
#         words = tree2conlltags(ne_chunk(pos_tag(word_tokenize(row['selftext']))))
#         newState = ''
#         nerState = ''
#         for tup in words:
#             currStr = test_trans(tup[0])
#             # 2. Lemmatize Single Word with the appropriate POS tag
#             if words[len(words) - 1] == tup:
#                 if currStr is not None:
#                     newState += lemmatizer.lemmatize(currStr, get_wordnet_pos(tup[0])) + "."
#                     nerState += tup[2]
#             else:
#                 if currStr is not None:
#                     newState += lemmatizer.lemmatize(currStr, get_wordnet_pos(tup[0])) + " "
#                     nerState += tup[2] + " "
#         submissions.loc[index, 'selftext'] = newState
#         submissions.loc[index, 'selftextner'] = nerState
#     print("Second: ", index, "/", submissions.size)

# submissions.to_csv('newSubmissions.csv', sep=',', encoding='utf-8')

comments = pandas.read_csv("./comments (1).csv", delimiter='\n', quotechar=None, quoting=2)

for index, row in comments.iterrows():
    if row['body'] is not '':
        words = tree2conlltags(ne_chunk(pos_tag(word_tokenize(row['body']))))
        newState = ''
        nerState = ''
        for tup in words:
            currStr = test_trans(tup[0])
            # 2. Lemmatize Single Word with the appropriate POS tag
            if words[len(words) - 1] == tup:
                if currStr is not None:
                    newState += lemmatizer.lemmatize(currStr, get_wordnet_pos(tup[0])) + "."
                    nerState += tup[2]
            else:
                if currStr is not None:
                    newState += lemmatizer.lemmatize(currStr, get_wordnet_pos(tup[0])) + " "
                    nerState += tup[2] + " "
        comments.loc[index, 'body'] = newState
        comments.loc[index, 'bodyner'] = nerState
    print("Third: ", index, "/", comments.size)

comments.to_csv('newComments.csv', sep=',', encoding='utf-8')
