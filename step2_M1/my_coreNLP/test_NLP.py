import parseNLP

import sys
import ..timer.timer as timer
import random

def save_to_file(name, struct):
	f = open(name, "w")
	f.write(str(struct))
	f.close()
	
def test(sNLP, text):
	text = sys.argv[1]
	time = {}
	chars = "".join([random.choice(list("ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxytz0123456789")) for i in range(15)])

	t = timer.Timer().start()
	print("\tannotate")
	save_to_file("./fics/annotate_"+chars, sNLP.annotate(text))
	time["annotate"] = t.stop()

	t.start()
	print("\tpos")
	save_to_file("./fics/pos_"+chars, sNLP.pos(text))
	time["pos"] = t.stop()

	t.start()
	print("\ttokens")
	save_to_file("./fics/tokens_"+chars, sNLP.word_tokenize(text))
	time["tokens"] = t.stop()

	t.start()
	print("\tner")
	save_to_file("./fics/ner_"+chars, sNLP.ner(text))
	time["ner"] = t.stop()

	t.start()
	print("\tparse")
	save_to_file("./fics/parse_"+chars, sNLP.parse(text))
	time["parse"] = t.stop()

	t.start()
	print("\tdependancy")
	save_to_file("./fics/dependancy_"+chars, sNLP.dependency_parse(text))
	time["dependancy"] = t.stop()

	print("\ttimer")
	save_to_file("./fics/timer_"+chars, time)
	
	f = open("./fics/corespond_random_chain", "a+")
	f.write(chars+" : "+text+"\n")
	f.close()

if __name__ == '__main__':
	sNLP = parseNLP.StanfordNLP()

	if len(sys.argv) != 2:
		print("Usage : $0 \"phrase\"")
	else:
		test(sNLP, sys.argv[1])