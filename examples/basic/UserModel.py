import Model

def resource_production_fn(x, y, time_step):
    return 1

def resource_consumption_fn1(x, y, resource):
    return 1

def ATP_production_fn1(resource_consumed):
    return 1

def resource_consumption_fn2(x, y, resource):
    return 1

def ATP_production_fn2(resource_consumed):
    return 1

class UserModel(Model.ScheduledModel):
	def __init__(self):
		super(UserModel, self).__init__()
		self.set_resource_production_fn = resource_production_fn
		#self.insert_state(name, resource_consumption_fn, division_age, min_food_req_to_divide, no_of_div_before_death)
		self.insert_state('A', resource_consumption_fn1, ATP_production_fn1, (2, 0), (4, 0), (4, 0))
		self.insert_state('B', resource_consumption_fn2, ATP_production_fn2, (2, 0), (2, 0), (4, 0))
