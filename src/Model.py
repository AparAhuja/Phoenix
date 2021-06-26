import random

class ScheduledModel():
	def __init__(self):
		self.name = 'Scheduled Model'
		self.individual_state_types= []
		self.consumption_fn        = {}
		self.production_fn         = {}
		self.enzyme_production_fn  = {}
		self.enzyme_consumption_fn = {}
		self.state_food_mean       = {}
		self.state_food_vary       = {}
		self.state_divideAge_mean  = {}
		self.state_divideAge_vary  = {}
		self.state_noOfDiv_mean    = {}
		self.state_noOfDiv_vary    = {}

	def insert_state(self, state, resource_consumption_fn, atp_production_fn, enzyme_production_fn, enzyme_consumption_fn, division_age, min_food_req_to_divide, no_of_div_before_death):
		self.individual_state_types.append(state)
		self.consumption_fn[state]        = resource_consumption_fn
		self.production_fn[state]         = atp_production_fn
		self.enzyme_production_fn[state]  = enzyme_production_fn
		self.enzyme_consumption_fn[state] = enzyme_consumption_fn
		self.state_food_mean[state]       = min_food_req_to_divide[0]
		self.state_food_vary[state]       = min_food_req_to_divide[1]
		self.state_divideAge_mean[state]  = division_age[0]
		self.state_divideAge_vary[state]  = division_age[1]
		self.state_noOfDiv_mean[state]    = no_of_div_before_death[0]
		self.state_noOfDiv_vary[state]    = no_of_div_before_death[1]

	def initialize_states(self, agents):
		for agent_index in agents:
			agent = agents[agent_index]
			state = agent.type

			mean = self.state_food_mean[state]; vary = self.state_food_vary[state];
			agent.food_req = random.randint(mean - vary, mean + vary)

			mean = self.state_noOfDiv_mean[state]; vary = self.state_noOfDiv_vary[state]
			agent.max_div  = random.randint(mean - vary, mean + vary)

			mean = self.state_divideAge_mean[state]; vary = self.state_divideAge_vary[state]
			agent.div_age  = random.randint(mean - vary, mean + vary)
