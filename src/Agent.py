import random

class Agent():
	def __init__(self, i, info_dict):
		self.info     = info_dict
		self.index    = i
		self.age      = 0
		self.atp      = 0
		self.div      = 0
		self.x        = int(info_dict['X'])
		self.y        = int(info_dict['Y'])
		self.type     = info_dict['Type']
		self.food_req = self.max_div = self.div_age = None

	def find_division_loc(self, x, y, n):
		r1 = random.randint(-1, 1)
		r2 = random.randint(-1, 1)
		x_new, y_new = x + r1, y + r2
		while(x_new < 0 or x_new > n - 1):
			x_new = x + random.randint(-1, 1)
		while(y_new < 0 or y_new > n - 1):
			y_new = y + random.randint(-1, 1)
		return x_new, y_new