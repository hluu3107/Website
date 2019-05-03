import numpy as np
class Gradient:	
	def __init__(self,a,b,d1,d2,w):
		self.a = a
		self.b = b
		self.d1 = d1
		self.d2 = d2
		self.w = w
	
	def shape(self):
		result = 0
    	#1 straight line, 2 linear line, 3 has both head and tail, 
    	#4 has head, 5 has tail, 0 illegal shape
		if self.a==self.b:
			result = 1
		elif self.d1==self.d2 or (self.d1!=0 and self.d2!=self.w):
			result = 3
		elif self.d1==0 and self.d2==self.w:
			result = 2
		elif self.d1!=0 and self.d2==self.w:
			result = 4
		elif self.d1==0 and self.d2!=self.w:
			result = 5
		return result

	def slope(self):
		return (self.a-self.b)/(self.d1-self.d2)

	def calculateArea(self):
		result = self.d1*self.a + (self.a+self.b)*(self.d2-self.d1)/2 + (self.w - self.d2)*self.b;
		return result
	
	def equalArea(self,newGrad):
		if abs(self.calculateArea()-newGrad.calculateArea())<1e-9:
			return True
		else:
			return False
	
	def getConcentration(self,mid):
		result = 0
		if self.a==self.b:
			result = self.b
		elif mid <= self.d1:
			result = self.a
		elif mid >= self.d2:
			result = self.b
		else: 
			result = getY(mid,self.d1,self.d2,self.a,self.b)
		return result

	def calculateConcentration(self):
		if self.a==0:
			return 0
		area = self.calculateArea()
		return area/self.w

	def __str__(self):
		return (f'a is {self.a:.2f} b is {self.b:.2f} d1 is {self.d1:.6f} d2 is {self.d2:.6f} w is {self.w:.1f}')

def getY(x,x1,x2,y1,y2):
	slope = (y2-y1)/(x2-x1)
	c = y1 - slope*x1
	return c + slope*x

class Point:
	def __init__(self,x,y):
		self.x = x
		self.y = y

	def __eq__(self,other):
		return np.all((abs(self.x-other.x)<1e-9)) and np.all((abs(self.y-other.y)<1e-9))

	def __ne__(self,other):
		return self.x != other.x or self.y != other.y

	def __lt__(self,other):
		return isinstance(other, self.__class__) and self.x < other.x 

	def __gt__(self,other):
		return isinstance(other, self.__class__) and self.x > other.x 

	def __str__(self):
		return (f'x is {self.x:.4f} y is {self.y:.4f}')