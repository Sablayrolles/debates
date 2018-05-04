import spacy

nlp = spacy.load('en_core_web_sm')

text = ("Secretary Clinton and others, politicians, should have been doing this for years, not right now, because of the fact that we've created a movement. They should have been doing this for years. What's happened to our jobs and our country and our economy generally is -- look, we owe $20 trillion. We cannot do it any longer, Lester.")

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
		
	def outputDependancy(self):
		print("graph (open with localhost:port on a navigator")
		spacy.displacy.serve(self.doc,style="dep")