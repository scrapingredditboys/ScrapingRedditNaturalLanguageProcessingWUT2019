from nltk.chunk import conlltags2tree, tree2conlltags
from nltk import word_tokenize, pos_tag, ne_chunk

sentence = "SpaceX on Twitter: 'Planning to send Dragon to Mars as soon as 2018. ' \
     'Red Dragons will inform overall Mars architecture, details to come"

ne_tree = ne_chunk(pos_tag(word_tokenize(sentence)))

iob_tagged = tree2conlltags(ne_tree)
print(iob_tagged)


ne_tree = conlltags2tree(iob_tagged)
print(ne_tree)
ne_tree.draw()


