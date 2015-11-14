#Import relevant packages
from __future__ import division
from math import pi, sin, cos, tan

class calc:
	def __init__(self, name):
		self.name = name

	def add(self, one, two):
		return one + two

	def subtract(self, one, two):
		return one - two

	def multiply(self, one, two):
		return one * two

	def divide(self, one, two):
		return one / two

def main():
	a = 44.2
	b = 53.4
	mycalc = "lev's calc"
	c = calc(mycalc)
	print(a)
	print(b)
	print(c.add(a,b))
	print(c.subtract(a,b))
	print(c.multiply(a,b))
	print(c.divide(a,b))
	print(c.name)

main()