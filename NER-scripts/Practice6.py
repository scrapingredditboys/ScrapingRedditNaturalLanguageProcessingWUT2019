import nltk
import pprint
from sklearn.tree import DecisionTreeClassifier
from sklearn.feature_extraction import DictVectorizer
from sklearn.pipeline import Pipeline
from nltk.chunk import conlltags2tree, tree2conlltags
from nltk import word_tokenize, pos_tag, ne_chunk
import os
import collections
import string
from nltk.stem.snowball import SnowballStemmer
import pickle
from collections.abc import Iterable
from nltk.tag import ClassifierBasedTagger
from nltk.chunk import ChunkParserI
from nltk import pos_tag, word_tokenize
import re
from nltk.stem.snowball import SnowballStemmer
import itertools
from nltk import tree2conlltags
from nltk.chunk import ChunkParserI
from sklearn.linear_model import Perceptron
from sklearn.feature_extraction import DictVectorizer
from sklearn.pipeline import Pipeline
from joblib import dump, load
import pandas


doc = "SpaceX on Twitter: 'Planning to send Dragon to Mars as soon as 2018. ' \
     'Red Dragons will inform overall Mars architecture, details to come"

tagged_sentences = nltk.corpus.treebank.tagged_sents()

# print(tagged_sentences[0])
# print("Tagged sentences: ", len(tagged_sentences))
# print("Tagged words:", len(nltk.corpus.treebank.tagged_words()))
# [('I', 'PRP'), ("'m", 'VBP'), ('learning', 'VBG'), ('NLP', 'NNP')]


def features(sentence, index):
    """ sentence: [w1, w2, ...], index: the index of the word """
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


# pprint.pprint(features(['This', 'is', 'a', 'sentence'], 2))


def untag(tagged_sentence):
    return [w for w, t in tagged_sentence]


# Split the dataset for training and testing
cutoff = int(.75 * len(tagged_sentences))
training_sentences = tagged_sentences[:cutoff]
test_sentences = tagged_sentences[cutoff:]

# print(len(training_sentences))  # 2935
# print(len(test_sentences)) # 979


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

# print('Training completed')

X_test, y_test = transform_to_dataset(test_sentences)

print("Accuracy:", clf.score(X_test, y_test))


def pos_tag(sentence):
    tags = clf.predict([features(sentence, index) for index in range(len(sentence))])
    tagged_sentence = list(map(list, zip(sentence, tags)))
    return tagged_sentence



ne_tree2 = pos_tag(word_tokenize(doc))
ne_tree = ne_chunk(pos_tag(word_tokenize(doc)))

iob_tagged = tree2conlltags(ne_tree)
iob_tagged2 = tree2conlltags(ne_tree2)
# print(iob_tagged)
# print(iob_tagged2)

"""
[('Mark', 'NNP', u'B-PERSON'), ('and', 'CC', u'O'), ('John', 'NNP', u'B-PERSON'), ('are', 'VBP', u'O'), ('working', 'VBG', u'O'), ('at', 'IN', u'O'), ('Google', 'NNP', u'B-ORGANIZATION'), ('.', '.', u'O')]
"""

ne_tree = conlltags2tree(iob_tagged)
# print(ne_tree)
# ne_tree.draw()
"""
(S
  (PERSON Mark/NNP)
  and/CC
  (PERSON John/NNP)
  are/VBP
  working/VBG
  at/IN
  (ORGANIZATION Google/NNP)
  ./.)
"""
corpus_root = "./gmb-2.2.0"   # Make sure you set the proper path to the unzipped corpus

ner_tags = collections.Counter()

for root, dirs, files in os.walk(corpus_root):
    for filename in files:
        if filename.endswith(".tags"):
            with open(os.path.join(root, filename), 'rb') as file_handle:
                file_content = file_handle.read().decode('utf-8').strip()
                annotated_sentences = file_content.split('\n\n')  # Split sentences
                for annotated_sentence in annotated_sentences:
                    annotated_tokens = [seq for seq in annotated_sentence.split('\n') if seq]  # Split words

                    standard_form_tokens = []

                    for idx, annotated_token in enumerate(annotated_tokens):
                        annotations = annotated_token.split('\t')  # Split annotation
                        word, tag, ner = annotations[0], annotations[1], annotations[3]

                        # Get only the primary category
                        if ner != 'O':
                            ner = ner.split('-')[0]

                        ner_tags[ner] += 1

print(ner_tags)
# Counter({u'O': 1146068, u'geo': 58388, u'org': 48094, u'per': 44254, u'tim': 34789, u'gpe': 20680, u'art': 867, u'eve': 709, u'nat': 300})

print("Words=", sum(ner_tags.values()))
# Words= 1354149


def featured(tokens, index, history):
    """
    `tokens`  = a POS-tagged sentence [(w1, t1), ...]
    `index`   = the index of the token we want to extract features for
    `history` = the previous predicted IOB tags
    """

    # init the stemmer
    stemmer = SnowballStemmer('english')

    # Pad the sequence with placeholders
    tokens = [('[START2]', '[START2]'), ('[START1]', '[START1]')] + list(tokens) + [('[END1]', '[END1]'),
                                                                                    ('[END2]', '[END2]')]
    history = ['[START2]', '[START1]'] + list(history)

    # shift the index with 2, to accommodate the padding
    index += 2

    word, pos = tokens[index]
    prevword, prevpos = tokens[index - 1]
    prevprevword, prevprevpos = tokens[index - 2]
    nextword, nextpos = tokens[index + 1]
    nextnextword, nextnextpos = tokens[index + 2]
    previob = history[index - 1]
    contains_dash = '-' in word
    contains_dot = '.' in word
    allascii = all([True for c in word if c in string.ascii_lowercase])

    allcaps = word == word.capitalize()
    capitalized = word[0] in string.ascii_uppercase

    prevallcaps = prevword == prevword.capitalize()
    prevcapitalized = prevword[0] in string.ascii_uppercase

    nextallcaps = prevword == prevword.capitalize()
    nextcapitalized = prevword[0] in string.ascii_uppercase
    return {
        'word': word,
        'lemma': stemmer.stem(word),
        'pos': pos,
        'all-ascii': allascii,

        'next-word': nextword,
        'next-lemma': stemmer.stem(nextword),
        'next-pos': nextpos,

        'next-next-word': nextnextword,
        'nextnextpos': nextnextpos,

        'prev-word': prevword,
        'prev-lemma': stemmer.stem(prevword),
        'prev-pos': prevpos,

        'prev-prev-word': prevprevword,
        'prev-prev-pos': prevprevpos,

        'prev-iob': previob,

        'contains-dash': contains_dash,
        'contains-dot': contains_dot,

        'all-caps': allcaps,
        'capitalized': capitalized,

        'prev-all-caps': prevallcaps,
        'prev-capitalized': prevcapitalized,

        'next-all-caps': nextallcaps,
        'next-capitalized': nextcapitalized,
    }


def to_conll_iob(annotated_sentence):
    """
    `annotated_sentence` = list of triplets [(w1, t1, iob1), ...]
    Transform a pseudo-IOB notation: O, PERSON, PERSON, O, O, LOCATION, O
    to proper IOB notation: O, B-PERSON, I-PERSON, O, O, B-LOCATION, O
    """
    proper_iob_tokens = []
    for idx, annotated_token in enumerate(annotated_sentence):
        tag, word, ner = annotated_token

        if ner != 'O':
            if idx == 0:
                ner = "B-" + ner
            elif annotated_sentence[idx - 1][2] == ner:
                ner = "I-" + ner
            else:
                ner = "B-" + ner
        proper_iob_tokens.append((tag, word, ner))
    return proper_iob_tokens


def read_gmb(corpus_root):
    for root, dirs, files in os.walk(corpus_root):
        for filename in files:
            if filename.endswith(".tags"):
                with open(os.path.join(root, filename), 'rb') as file_handle:
                    file_content = file_handle.read().decode('utf-8').strip()
                    annotated_sentences = file_content.split('\n\n')
                    for annotated_sentence in annotated_sentences:
                        annotated_tokens = [seq for seq in annotated_sentence.split('\n') if seq]

                        standard_form_tokens = []

                        for idx, annotated_token in enumerate(annotated_tokens):
                            annotations = annotated_token.split('\t')
                            word, tag, ner = annotations[0], annotations[1], annotations[3]

                            if ner != 'O':
                                ner = ner.split('-')[0]

                            if tag in ('LQU', 'RQU'):  # Make it NLTK compatible
                                tag = "``"

                            standard_form_tokens.append((word, tag, ner))

                        conll_tokens = to_conll_iob(standard_form_tokens)

                        # Make it NLTK Classifier compatible - [(w1, t1, iob1), ...] to [((w1, t1), iob1), ...]
                        # Because the classfier expects a tuple as input, first item input, second the class
                        yield [((w, t), iob) for w, t, iob in conll_tokens]


reader = read_gmb(corpus_root)
# print(reader.next())
# print('------------')
"""
[((u'Thousands', u'NNS'), u'O'), ((u'of', u'IN'), u'O'), ((u'demonstrators', u'NNS'), u'O'), ((u'have', u'VBP'), u'O'), ((u'marched', u'VBN'), u'O'), ((u'through', u'IN'), u'O'), ((u'London', u'NNP'), u'B-geo'), ((u'to', u'TO'), u'O'), ((u'protest', u'VB'), u'O'), ((u'the', u'DT'), u'O'), ((u'war', u'NN'), u'O'), ((u'in', u'IN'), u'O'), ((u'Iraq', u'NNP'), u'B-geo'), ((u'and', u'CC'), u'O'), ((u'demand', u'VB'), u'O'), ((u'the', u'DT'), u'O'), ((u'withdrawal', u'NN'), u'O'), ((u'of', u'IN'), u'O'), ((u'British', u'JJ'), u'B-gpe'), ((u'troops', u'NNS'), u'O'), ((u'from', u'IN'), u'O'), ((u'that', u'DT'), u'O'), ((u'country', u'NN'), u'O'), ((u'.', u'.'), u'O')]
------------
"""

# print(reader.next())
# print('------------')
"""
[((u'Families', u'NNS'), u'O'), ((u'of', u'IN'), u'O'), ((u'soldiers', u'NNS'), u'O'), ((u'killed', u'VBN'), u'O'), ((u'in', u'IN'), u'O'), ((u'the', u'DT'), u'O'), ((u'conflict', u'NN'), u'O'), ((u'joined', u'VBD'), u'O'), ((u'the', u'DT'), u'O'), ((u'protesters', u'NNS'), u'O'), ((u'who', u'WP'), u'O'), ((u'carried', u'VBD'), u'O'), ((u'banners', u'NNS'), u'O'), ((u'with', u'IN'), u'O'), ((u'such', u'JJ'), u'O'), ((u'slogans', u'NNS'), u'O'), ((u'as', u'IN'), u'O'), ((u'"', '``'), u'O'), ((u'Bush', u'NNP'), u'B-per'), ((u'Number', u'NN'), u'O'), ((u'One', u'CD'), u'O'), ((u'Terrorist', u'NN'), u'O'), ((u'"', '``'), u'O'), ((u'and', u'CC'), u'O'), ((u'"', '``'), u'O'), ((u'Stop', u'VB'), u'O'), ((u'the', u'DT'), u'O'), ((u'Bombings', u'NNS'), u'O'), ((u'.', u'.'), u'O'), ((u'"', '``'), u'O')]
------------
"""

# print(reader.next())
# print('------------')
"""
[((u'They', u'PRP'), u'O'), ((u'marched', u'VBD'), u'O'), ((u'from', u'IN'), u'O'), ((u'the', u'DT'), u'O'), ((u'Houses', u'NNS'), u'O'), ((u'of', u'IN'), u'O'), ((u'Parliament', u'NN'), u'O'), ((u'to', u'TO'), u'O'), ((u'a', u'DT'), u'O'), ((u'rally', u'NN'), u'O'), ((u'in', u'IN'), u'O'), ((u'Hyde', u'NNP'), u'B-geo'), ((u'Park', u'NNP'), u'I-geo'), ((u'.', u'.'), u'O')]
------------
"""


class NamedEntityChunker(ChunkParserI):
    def __init__(self, train_sents, **kwargs):
        assert isinstance(train_sents, Iterable)

        self.feature_detector = featured
        self.tagger = ClassifierBasedTagger(
            train=train_sents,
            feature_detector=featured,
            **kwargs)

    def parse(self, tagged_sent):
        chunks = self.tagger.tag(tagged_sent)

        # Transform the result from [((w1, t1), iob1), ...]
        # to the preferred list of triplets format [(w1, t1, iob1), ...]
        iob_triplets = [(w, t, c) for ((w, t), c) in chunks]

        # Transform the list of triplets to nltk.Tree format
        return conlltags2tree(iob_triplets)


reader = read_gmb(corpus_root)
data = list(reader)
training_samples = data[:int(len(data) * 0.9)]
test_samples = data[int(len(data) * 0.9):]

print("#training samples = %s" % len(training_samples)) # training samples = 55809
print("#test samples = %s" % len(test_samples)) # test samples = 6201

chunker = NamedEntityChunker(training_samples[:2000])
print(chunker.parse(pos_tag(word_tokenize(doc))))
score = chunker.evaluate([conlltags2tree([(w, t, iob) for (w, t), iob in iobs]) for iobs in test_samples[:500]])
print(score.accuracy())


def to_conll_iob(annotated_sentence):
    """
    `annotated_sentence` = list of triplets [(w1, t1, iob1), ...]
    Transform a pseudo-IOB notation: O, PERSON, PERSON, O, O, LOCATION, O
    to proper IOB notation: O, B-PERSON, I-PERSON, O, O, B-LOCATION, O
    """
    proper_iob_tokens = []
    for idx, annotated_token in enumerate(annotated_sentence):
        tag, word, ner = annotated_token

        if ner != 'O':
            if idx == 0:
                ner = "B-" + ner
            elif annotated_sentence[idx - 1][2] == ner:
                ner = "I-" + ner
            else:
                ner = "B-" + ner
        proper_iob_tokens.append((tag, word, ner))
    return proper_iob_tokens


def read_gmb_ner(corpus_root):
    for root, dirs, files in os.walk(corpus_root):
        for filename in files:
            if filename.endswith(".tags"):
                with open(os.path.join(root, filename), 'rb') as file_handle:
                    file_content = file_handle.read().decode('utf-8').strip()
                    annotated_sentences = file_content.split('\n\n')
                    for annotated_sentence in annotated_sentences:
                        annotated_tokens = [seq for seq in annotated_sentence.split('\n') if seq]

                        standard_form_tokens = []

                        for idx, annotated_token in enumerate(annotated_tokens):
                            annotations = annotated_token.split('\t')
                            word, tag, ner = annotations[0], annotations[1], annotations[3]

                            if ner != 'O':
                                ner = ner.split('-')[0]

                            standard_form_tokens.append((word, tag, ner))

                        conll_tokens = to_conll_iob(standard_form_tokens)
                        yield conlltags2tree(conll_tokens)


def shape(word):
    word_shape = 'other'
    if re.match('[0-9]+(\.[0-9]*)?|[0-9]*\.[0-9]+$', word):
        word_shape = 'number'
    elif re.match('\W+$', word):
        word_shape = 'punct'
    elif re.match('[A-Z][a-z]+$', word):
        word_shape = 'capitalized'
    elif re.match('[A-Z]+$', word):
        word_shape = 'uppercase'
    elif re.match('[a-z]+$', word):
        word_shape = 'lowercase'
    elif re.match('[A-Z][a-z]+[A-Z][a-z]+[A-Za-z]*$', word):
        word_shape = 'camelcase'
    elif re.match('[A-Za-z]+$', word):
        word_shape = 'mixedcase'
    elif re.match('__.+__$', word):
        word_shape = 'wildcard'
    elif re.match('[A-Za-z0-9]+\.$', word):
        word_shape = 'ending-dot'
    elif re.match('[A-Za-z0-9]+\.[A-Za-z0-9\.]+\.$', word):
        word_shape = 'abbreviation'
    elif re.match('[A-Za-z0-9]+\-[A-Za-z0-9\-]+.*$', word):
        word_shape = 'contains-hyphen'

    return word_shape


stemmer = SnowballStemmer('english')


def ner_features(tokens, index, history):
    """
    `tokens`  = a POS-tagged sentence [(w1, t1), ...]
    `index`   = the index of the token we want to extract features for
    `history` = the previous predicted IOB tags
    """

    # Pad the sequence with placeholders
    tokens = [('__START2__', '__START2__'), ('__START1__', '__START1__')] + list(tokens) + [('__END1__', '__END1__'),
                                                                                            ('__END2__', '__END2__')]
    history = ['__START2__', '__START1__'] + list(history)

    # shift the index with 2, to accommodate the padding
    index += 2

    word, pos = tokens[index]
    prevword, prevpos = tokens[index - 1]
    prevprevword, prevprevpos = tokens[index - 2]
    nextword, nextpos = tokens[index + 1]
    nextnextword, nextnextpos = tokens[index + 2]
    previob = history[-1]
    prevpreviob = history[-2]
    # print(word)

    feat_dict = {
        'word': word,
        'lemma': stemmer.stem(word),
        'pos': pos,
        'shape': shape(word),

        'next-word': nextword,
        'next-pos': nextpos,
        'next-lemma': stemmer.stem(nextword),
        'next-shape': shape(nextword),

        'next-next-word': nextnextword,
        'next-next-pos': nextnextpos,
        'next-next-lemma': stemmer.stem(nextnextword),
        'next-next-shape': shape(nextnextword),

        'prev-word': prevword,
        'prev-pos': prevpos,
        'prev-lemma': stemmer.stem(prevword),
        'prev-iob': previob,
        'prev-shape': shape(prevword),

        'prev-prev-word': prevprevword,
        'prev-prev-pos': prevprevpos,
        'prev-prev-lemma': stemmer.stem(prevprevword),
        'prev-prev-iob': prevpreviob,
        'prev-prev-shape': shape(prevprevword),
    }

    return feat_dict


class ScikitLearnChunker(ChunkParserI):

    @classmethod
    def to_dataset(cls, parsed_sentences, feature_detector):
        """
        Transform a list of tagged sentences into a scikit-learn compatible POS dataset
        :param parsed_sentences:
        :param feature_detector:
        :return:
        """
        X, y = [], []
        for parsed in parsed_sentences:
            iob_tagged = tree2conlltags(parsed)
            words, tags, iob_tags = zip(*iob_tagged)

            tagged = list(zip(words, tags))

            for index in range(len(iob_tagged)):
                X.append(feature_detector(tagged, index, history=iob_tags[:index]))
                y.append(iob_tags[index])

        return X, y

    @classmethod
    def get_minibatch(cls, parsed_sentences, feature_detector, batch_size=500):
        batch = list(itertools.islice(parsed_sentences, batch_size))
        X, y = cls.to_dataset(batch, feature_detector)
        return X, y

    @classmethod
    def train(cls, parsed_sentences, feature_detector, all_classes, **kwargs):
        X, y = cls.get_minibatch(parsed_sentences, feature_detector, kwargs.get('batch_size', 500))
        vectorizer = DictVectorizer(sparse=False)
        vectorizer.fit(X)

        clf = Perceptron(verbose=10, n_jobs=-1, n_iter=kwargs.get('n_iter', 5))

        while len(X):
            X = vectorizer.transform(X)
            clf.partial_fit(X, y, all_classes)
            X, y = cls.get_minibatch(parsed_sentences, feature_detector, kwargs.get('batch_size', 500))

        clf = Pipeline([
            ('vectorizer', vectorizer),
            ('classifier', clf)
        ])
        # dump(clf, 'firstModel.joblib')
        clf = load('firstModel.joblib')

        return cls(clf, feature_detector)

    def __init__(self, classifier, feature_detector):
        self._classifier = classifier
        self._feature_detector = feature_detector

    def parse(self, tokens):
        """
        Chunk a tagged sentence
        :param tokens: List of words [(w1, t1), (w2, t2), ...]
        :return: chunked sentence: nltk.Tree
        """
        history = []
        iob_tagged_tokens = []
        for index, (word, tag) in enumerate(tokens):
            iob_tag = self._classifier.predict([self._feature_detector(tokens, index, history)])[0]
            history.append(iob_tag)
            iob_tagged_tokens.append((word, tag, iob_tag))

        return conlltags2tree(iob_tagged_tokens)

    def score(self, parsed_sentences):
        """
        Compute the accuracy of the tagger for a list of test sentences
        :param parsed_sentences: List of parsed sentences: nltk.Tree
        :return: float 0.0 - 1.0
        """
        X_test, y_test = self.__class__.to_dataset(parsed_sentences, self._feature_detector)
        return self._classifier.score(X_test, y_test)


def train_perceptron(doc):
    reader = read_gmb_ner("./gmb-2.2.0")

    all_classes = ['O', 'B-per', 'I-per', 'B-gpe', 'I-gpe',
                   'B-geo', 'I-geo', 'B-org', 'I-org', 'B-tim', 'I-tim',
                   'B-art', 'I-art', 'B-eve', 'I-eve', 'B-nat', 'I-nat']

    # pa_ner = ScikitLearnChunker.train(itertools.islice(reader, 50000), feature_detector=ner_features,
    #                                   all_classes=all_classes, batch_size=500, n_iter=5)
    # dump(pa_ner, 'finalModel.joblib')
    pa_ner = load('finalModel.joblib')
    print(pa_ner.parse(pos_tag(word_tokenize(doc))))
    # accuracy = pa_ner.score(itertools.islice(reader, 5000))
    #
    # print("Accuracy:", accuracy) # 0.970327096314


submissions = pandas.read_csv("./submissions.csv")
modifiedData = []
for index, row in submissions.iterrows():
    modifiedData.append(train_perceptron(row['title']))

# doc = "I love Paris"
# train_perceptron(doc)