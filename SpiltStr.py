import nltk
sents = nltk.corpus.treebank_raw.sents()
tokens = []
boundaries = set()
offset = 0
for sent in nltk.corpus.treebank_raw.sents():
	tokens.extend(sent)
	offset += len(sent)
	boundaries.add(offset-1)
def punct_features(token ,i ):
	return {'next-word-capitalized': tokens[i+1][0].isupper(),
			'prevword': tokens[i-1].lower(),
			'punct':tokens[i],
			'prev-word-is-one-char':len(tokens[i-1] ) == 1}
