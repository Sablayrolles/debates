import sys
sys.path.insert(0,'..')

import my_spacy.spacy_mod as spacy_mod

PUNCT_FACTOR = 0.7
WORD_FACTOR = 0.7
ENTITY_FACTOR = 0.2
SENTENCE_FACTOR = 0.4

def getPunct():
	return [[","], ["."], [";"], ["..."], ["!"], ["?"], ["(",")"], ["--"]]
	
def getPunctEndSentences():
	return [["."], ["..."], ["!"], ["?"]]
	
def getPunctAgressivity():
	return {",": 0, "." : -0.1, ";": 0, "...": -1, "!": 3, "?": 2, "()": 2, "--": 1}
	
def getWordsToAnalyse():
	return ["I", "You", "i", "you", "Clinton", "Trump", "his", "her", "she", "he", "him"]

class EDUFeelings:
	def __init__(self, spacy, EDU):
		self.EDU = EDU
		self.analyse = False
		self.spacy = spacy
	
	def analysis(self):
		if not self.analyse:
			self.analyse = True
			self.size = len(self.EDU)

			self.spacy.analyse(self.EDU)
			self.nbWords = len(self.spacy.tokens())
			
			#---------------------------------------------------------------------------------------
			#analyse de la ponctuation
			self.punct = {}
			for p in getPunct():
				self.punct["n"+"".join(p)] = 0
				for symb in p:
					self.punct["n"+"".join(p)] += list(self.spacy.tokens().keys()).count(symb)
			
			self.nbPhrases = 0
			for p in getPunctEndSentences():
				self.nbPhrases += self.punct["n"+"".join(p)]
				
			#ratio sur le nombre de phrases
			for p in getPunct():
				self.punct["r"+"".join(p)] = self.punct["n"+"".join(p)] / self.nbPhrases			 
			#--------------------------------------------------------------------------------------
			
			#--------------------------------------------------------------------------------------
			#analyse sur les mots
			self.moy_words_length = 0
			
			for t in self.spacy.tokens():
				self.moy_words_length += len(t)
			self.moy_words_length /= self.nbWords
			
			self.words = {}
			for w in getWordsToAnalyse():
				self.words["nb"+w] = list(self.spacy.tokens().keys()).count('w')
				self.words["r"+w] = self.words["nb"+w] / self.nbPhrases
			#--------------------------------------------------------------------------------------
			
			#--------------------------------------------------------------------------------------
			#analyse sur le contenu des tokens
			self.nbEntities = len(self.spacy.getEntities().keys())
			self.rEntities = self.nbEntities / self.nbPhrases
			#--------------------------------------------------------------------------------------
			
	def agressivity(self):
		if not self.analyse:
			return -1
		else:
			pagressivity = 0
			for p in getPunct():
				pagressivity += getPunctAgressivity()["".join(p)] * self.punct["r"+"".join(p)] 	
			
			wagressivity = 0
			for w in getWordsToAnalyse():
				wagressivity += self.words["r"+w]
			
			agressivity = wagressivity * WORD_FACTOR + pagressivity * PUNCT_FACTOR + self.rEntities * ENTITY_FACTOR + SENTENCE_FACTOR * (1.0 / self.moy_words_length)
			return agressivity
			
if __name__ == "__main__":
	spacy = spacy_mod.Spacy()
	
	texts = [u"In the last couple of weeks, you acknowledged what most Americans have accepted for years: The president was born in the United States. Can you tell us what took you so long?", u"Secretary Clinton and others, politicians, should have been doing this for years, not right now, because of the fact that we've created a movement. They should have been doing this for years. What's happened to our jobs and our country and our economy generally is -- look, we owe $20 trillion. We cannot do it any longer, Lester.", u"Well, nobody was pressing it, nobody was caring much about it. But I was the one that got him to produce the birth certificate. And I think I did a good job.", u"Well, just listen to what you heard. But it can't be dismissed that easily. He has really started his political activity based on this racist lie that our first black president was not an American citizen. But, remember, Donald started his career back in 1973 being sued by the Justice Department for racial discrimination because he would not rent apartments in one of his developments to African-Americans, and he made sure that the people who worked for him understood that was the policy. And the birther lie was a very hurtful one. You know, Barack Obama is a man of great dignity. And I could tell how much it bothered him and annoyed him that this was being touted and used against him. But I like to remember what Michelle Obama said in her amazing speech at our Democratic National Convention: When they go low, we go high. And Barack Obama went high, despite Donald Trump's best efforts to bring him down."]
	
	for t in texts:
		f=EDUFeelings(spacy, t)
		f.analysis()
		print("\n"+t)
		print("Agressivity : ", f.agressivity())