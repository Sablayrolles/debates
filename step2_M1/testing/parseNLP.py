#!/usr/bin/python3

import sys
import timeit

'''
A sample code usage of the python package stanfordcorenlp to access a Stanford CoreNLP server.
Written as part of the blog post: https://www.khalidalnajjar.com/how-to-setup-and-use-stanford-corenlp-server-with-python/ 
'''

from stanfordcorenlp import StanfordCoreNLP
import logging
import json

class StanfordNLP:
	def __init__(self, host='http://localhost', port=9000):
		self.nlp = StanfordCoreNLP(host, port=port,
								   timeout=30000)  # , quiet=False, logging_level=logging.DEBUG)
		self.props = {
			'annotators': 'tokenize,ssplit,pos,lemma,ner,parse,depparse,dcoref,relation',
			'pipelineLanguage': 'en',
			'outputFormat': 'json'
		}

	def word_tokenize(self, sentence):
		return self.nlp.word_tokenize(sentence)

	def pos(self, sentence):
		return self.nlp.pos_tag(sentence)

	def ner(self, sentence):
		return self.nlp.ner(sentence)

	def parse(self, sentence):
		return self.nlp.parse(sentence)

	def dependency_parse(self, sentence):
		return self.nlp.dependency_parse(sentence)

	def annotate(self, sentence):
		return json.loads(self.nlp.annotate(sentence, properties=self.props))

	@staticmethod
	def tokens_to_dict(_tokens):
		tokens = defaultdict(dict)
		for token in _tokens:
			tokens[int(token['index'])] = {
				'word': token['word'],
				'lemma': token['lemma'],
				'pos': token['pos'],
				'ner': token['ner']
		}
		return tokens

def save_to_file(name, struct):
	f = open(name, "w")
	f.write(str(struct))
	f.close()

t = 0

def start():
	global t
	t = timeit.default_timer()

def stop():
	global t
	return timeit_default_timer() - t

if __name__ == '__main__':
	sNLP = StanfordNLP()

	if len(sys.argv) != 1:
		print("Usage : $0 \"phrase\"")
	else:
		text = sys.argv[1]
		time = {}

		save_to_file("./fics/annoted_"+sys.argv[1], sNLP.annoted(text))
		time["annotated"] = stop()

		save_to_file("./fics/pos_"+sys.argv[1], sNLP.pos(text))
		time["pos"] = stop()

		save_to_file("./fics/tokens_"+sys.argv[1], sNLP.word_tokenize(text))
		time["tokens"] = stop()

		save_to_file("./fics/ner_"+sys.argv[1], sNLP.ner(text))
		time["ner"] = stop()

		save_to_file("./fics/parse_"+sys.argv[1], sNLP.parse(text))
		time["parse"] = stop()

		save_to_file("./fics/dependancy_"+sys.argv[1], sNLP.dependency_parse(text))
		time["dependancy"] = stop()

		save_to_file("./fics/timer_"+sys.argv[1], time)
