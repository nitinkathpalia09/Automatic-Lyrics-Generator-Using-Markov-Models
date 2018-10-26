from __future__ import print_function
from nltk.tokenize import word_tokenize

with open ('lavigne_verse.txt') as fin, open('lyrics_tokenize.txt') as fout:
	for line in fin:
		tokens = word_tokenize(line)
		print(' '.join(tokens), end='\n', file=fout)
        
