import Model

def resource_production_fn(x, y, time_step):
    return 500

def resource_consumption_fnA(x, y, resource):
    s = resource[x][y]
    return s/(1+s)

def atp_production_fnA(resource_consumed):
    return 32*resource_consumed

def resource_consumption_fnB(x, y, resource):
    s = resource[x][y]
    return 100*s/(100+s)

def atp_production_fnB(resource_consumed):
    s = resource_consumed
    return 30*s/(1+s) + 200*s/(100+s)

class UserModel(Model.ScheduledModel):
	def __init__(self):
		super(UserModel, self).__init__()
		self.resource_production_fn = resource_production_fn
		#self.insert_state(name, resource_consumption_fn, atp_production_fn, division_age, min_atp_req_to_divide, no_of_div_before_death)
		self.insert_state('A', resource_consumption_fnA, atp_production_fnA, (4, 0), (224, 0), (4, 0))
		self.insert_state('B', resource_consumption_fnB, atp_production_fnB, (4, 0), (224, 0), (4, 0))
