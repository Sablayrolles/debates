#!/usr/bin/python3

import sys
import timeit
import random

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
	return timeit.default_timer() - t

def test(sNLP, text):
	text = sys.argv[1]
	time = {}
	chars = "".join([random.choice(string.letters+sting.digits) for i in xrange(15)])

	save_to_file("./fics/annotate_"+chars, sNLP.annotate(text))
	time["annotate"] = stop()

	save_to_file("./fics/pos_"+chars, sNLP.pos(text))
	time["pos"] = stop()

	save_to_file("./fics/tokens_"+chars, sNLP.word_tokenize(text))
	time["tokens"] = stop()

	save_to_file("./fics/ner_"+chars, sNLP.ner(text))
	time["ner"] = stop()

	save_to_file("./fics/parse_"+chars, sNLP.parse(text))
	time["parse"] = stop()

	save_to_file("./fics/dependancy_"+chars, sNLP.dependency_parse(text))
	time["dependancy"] = stop()

	save_to_file("./fics/timer_"+chars, time)
	
	f = open("corespond_random_chain", "w")
	f.write(chars+" : "+text)
	f.close()


if __name__ == '__main__':
	sNLP = StanfordNLP()

	if len(sys.argv) != 2:
		print("Usage : $0 \"phrase\"")
	else:
		test(sNLP, sys.argv[1])
