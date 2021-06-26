import Model

def resource_production_fn(x, y, time_step):
    return 1

def resource_consumption_fnA(resource_avalible, enzyme_avalible):
    return 1

def resource_consumption_fnB(resource_avalible, enzyme_avalible):
    return 1

def atp_production_fnA(resource_consumed):
    return 1

def atp_production_fnB(resource_consumed):
    return 1

class UserModel(Model.ScheduledModel):
	def __init__(self):
		super(UserModel, self).__init__()
		self.resource_production_fn = resource_production_fn
		#self.insert_state(name, resource_consumption_fn, atp_production_fn, division_age, min_atp_req_to_divide, no_of_div_before_death)
		self.insert_state('A', resource_consumption_fnA, atp_production_fnA, lambda x: 0, lambda x: 0, (2, 0), (4, 0), (4, 0))
		self.insert_state('B', resource_consumption_fnB, atp_production_fnB, lambda x: 0, lambda x: 0, (2, 0), (2, 0), (4, 0))
