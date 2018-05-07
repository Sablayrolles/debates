#!/usr/bin/python3
# -*- coding: utf-8 -*-

# Module Timer
# Author : SABLAYROLLES Louis
# Date : 07 / 05 / 17

# Mesure time of any bloc code with a simple class

import timeit

"""
	Module Timer
	============
	
	This module can be use to mesure the user time of any bloc code with a simple class.
	
"""
class Timer:
	"""
		Class Timer
		===========
		
		Use it to define a timer for a bloc of code.
		
		def __init__(self) : instanciation of timer object
		def start(self) : start or restart the timer 
		def pause(self) : pause the timer
		def getTime(self) : return the actual elapse time without stopping the timer
		def stop(self) : stop the timer and return the elapse time
	"""
		
	def __init__(self):
		"""
			def __init__(self)
			------------------
			
			instanciation of timer object
			
			:return: None
			:rtype: NoneType
		"""
		self.t = 0
	def start(self):
		"""
			def start(self)
			---------------
			
			start or restart the timer 
			
			:return: None
			:rtype: NoneType
		"""
		self.time = timeit.default_timer()
	def pause(self):
		"""
			def pause(self)
			---------------
			
			pause the timer
			
			:return: None
			:rtype: NoneType
		"""
		self.t = timeit.default_timer() - self.time
	def getTime(self):
		"""
			def pause(self)
			---------------
			
			return the actual elapse time without stopping the timer
			
			:return: Elapse Time
			:rtype: Float
		"""
		return self.t + (timeit.default_timer() - self.time)
	def stop(self):
		"""
			def stop(self)
			--------------
		
			stop the timer and return the elapse time
			
			:return: Elapse Time
			:rtype: Float
		"""
		t = self.t + (timeit.default_timer() - self.time)
		self.t = 0
		return t
