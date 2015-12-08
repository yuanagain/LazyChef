

#boolean defining type of ingredient
basic = True;
compound = False;

'''
class Ingredient

fields : name (string)
		 type (boolean)
		 operator (object)
		 operands (list of objects)

initializer : name_in (string describing task)
			  operator_in (object) (optional)
			  operands_in (list of objects) (optional)

notes : operands_in will ALWAYS be in the order that they
		are input

'''

class Ingredient:
	def __init__(self, name_in, operator_in, \
				  operands_in):
		self.name = name_in
		#Overload 
		if (operator_in is None or operands_in is None):
			self.type = basic
		else:
			self.type = compound
			self.operator = operator_in
			self.operands = operands_in

'''
class Operator

fields : name (string)
		 type (boolean)
		 operator (object)
		 operands (list of objects)

initializer : name_in (string)
			  front_end_name (string)
			  operator_in (object) (optional)
			  operands_in (list of objects) (optional)

notes : operands_in will ALWAYS be in the order that they
		are input

'''

class Operator:
	def __init__(self, name_in):
		self.name = name_in


