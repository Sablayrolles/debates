import spacy

class Spacy:
	def __init__(self):
		self.nlp = spacy.load('en_core_web_sm')
		self.doc = {}
	
	def analyse(self, text):
		self.doc = self.nlp(text)
	
	def getEntities(self):
		if self.doc != {}:
			t = {}
			for entity in self.doc.ents:
				t[entity.text] = entity.label_
				
			return t
		else:
			return {}

	def tokens(self):
		if self.doc != {}:
			t = {}
			for token in self.doc:
				t[token.text] = token
			return t
		else:
			return {}
		
	def outputDependancy(self):
		print("graph (open with localhost:port on a navigator")
		spacy.displacy.serve(self.doc,style="dep")
		
	def getSentiment(self):
		return self.doc.sentiment
