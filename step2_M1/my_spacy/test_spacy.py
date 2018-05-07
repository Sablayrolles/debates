import spacy_mod

sp = spacy_mod.Spacy()

text = (u"Secretary Clinton and others, politicians, should have been doing this for years, not right now, because of the fact that we've created a movement. They should have been doing this for years. What's happened to our jobs and our country and our economy generally is -- look, we owe $20 trillion. We cannot do it any longer, Lester.")

sp.analyse(text)
print("Entities:")
print(sp.getEntities())
print("\nTokens:")
print(sp.tokens())
print("\nDependancy:")
sp.outputDependancy()
print("\nSentiment:")
sp.getSentiment()
