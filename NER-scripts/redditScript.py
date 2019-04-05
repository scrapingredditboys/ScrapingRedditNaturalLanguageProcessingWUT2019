from nltk.corpus import stopwords
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import re, string, timeit
import nltk
from nltk.corpus import state_union
from nltk.tokenize import PunktSentenceTokenizer
from nltk.stem import WordNetLemmatizer

lemmatizer = WordNetLemmatizer()

train_text = state_union.raw("2005-GWBush.txt")
sample_text = state_union.raw("2006-GWBush.txt")
custom_sent_tokenizer = PunktSentenceTokenizer(train_text)
tokenized = custom_sent_tokenizer.tokenize(sample_text)


def process_content():
    try:
        for i in tokenized[5:]:
            words = nltk.word_tokenize(i)
            tagged = nltk.pos_tag(words)
            namedEnt = nltk.ne_chunk(tagged, binary=False)
            print(lemmatizer.lemmatize(namedEnt))
    except Exception as e:
        print(str(e))


process_content()

# exclude = set(string.punctuation)
# table = str.maketrans("","")
# regex = re.compile('[%s]' % re.escape(string.punctuation))
#
#
# def test_trans(s):
#     return s.translate(table, string.punctuation)
#
#
# example_sent = "This might be a sample sentence, [showing] off the stop words mouse."
#
# stop_words = set(stopwords.words('english'))
#
# word_tokens = word_tokenize(example_sent)
#
# filtered_sentence = [w for w in word_tokens if not w in stop_words]
#
# filtered_sentence = []
#
# for w in word_tokens:
#     if w not in stop_words:
#         w = w.translate(str.maketrans('','',string.punctuation))
#         if w is not '':
#             filtered_sentence.append(w)
#
# print(word_tokens)
# print(filtered_sentence)