import re

class Sentences():
	cur_ligne = -1
	def __init__(self, fichier, entete_to_split, type="Sentences"):
		fic = open(fichier,"r")
		f = fic.readlines()
		fic.close()
		
		self.f = []
		n = 0
		for l in f:
			if l.strip() != "":
				n += 1
				m = re.search(entete_to_split, l)
				
				if type == "EDU":
					for edu in re.sub(entete_to_split, '', l).split("&"):
						emmiter = m.group(0)
						d = {"num":n, "emmiter": emmiter, "edu": edu}
						if edu != '\n':
							self.f.append(d)
				else:
					emmiter = m.group(0)
					d = {"num":n, "emmiter": emmiter, "sentences": re.sub(entete_to_split, '', l).replace("&", "").replace("\n", "")}
					self.f.append(d)
					
	def __iter__(self):
		
		return self
	
	def next(self):
		self.cur_ligne += 1
		
		if self.cur_ligne > len(self.f):
			raise StopIteration
		
		return self.f[self.cur_ligne]
		
	def __next__(self):
		return self.next()

class It():
	cur = 0
	def __init__(self, stop):
		self.stop = stop
	def __iter__(self):
		return self
	def next(self):
		self.cur += 1 
		if self.cur > self.stop:
			raise StopIteration
		return self.cur
	def __next__(self):
		return self.next()
		
if __name__ == "__main__":

	for i in It(3):
		print(i)

	file = "C:\\Users\\louis\\Documents\\GitHub\\debates\\step2_M1\\dataset\\usa\\2016\\1\\hand-segmented\\2.txt"
	
	for s in Sentences(file, "(^[A-Z]+: )"):
		print(s)
		a = input()