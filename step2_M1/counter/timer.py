import timeit
	
class Timer:
	def __init__(self):
		self.t = 0
	def start(self):
		self.time = timeit.default_timer()
	def pause(self):
		self.t = timeit.default_timer() - self.time
	def stop(self):
		t = self.t + (timeit.default_timer() - self.time)
		self.t = 0
		return t
