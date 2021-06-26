import Agent
import random

class Simulate():
	def __init__(self, config_obj, model, agents_obj, resource_obj, stats, world_number):
		self.agents_obj   = agents_obj
		self.resource_obj = resource_obj
		self.model        = model
		self.config_obj   = config_obj
		self.stats        = stats
		self.world_number = world_number
		self.current_time_step = 0

	def onStartSimulation(self):

		# Intitialize state list
		self.state_list    = {}
		self.state_history = {}
		for state in self.model.individual_state_types:
			self.state_list[state]    = []
			self.state_history[state] = []

		# Initialize states
		self.model.initialize_states(self.agents_obj.agents)

		# Update State list
		for agent in self.agents_obj.agents.values():
			self.state_list[agent.type].append(agent.index)

		# Store state list with start = True for stats
		self.store_state(True)

	def onStartTimeStep(self, current_time_step):
		self.current_time_step = current_time_step
		r_obj                  = self.resource_obj
		model                  = self.model
		new_agents             = dict([(agent.index, agent) for agent in self.agents_obj.agentsAt.get(current_time_step+1, [])])
		dead_agents            = []
		free_index             = len(self.agents_obj.agents)

		agents_list = list(self.agents_obj.agents.values())
		random.shuffle(agents_list)

		# add resource
		for x in range(self.config_obj.grid_size):
			for y in range(self.config_obj.grid_size):
				r_obj.resource_grid[x][y] += model.resource_production_fn(x, y, current_time_step)

		for agent in agents_list:
			# increase age by 1
			agent.age += 1

			# consume food
			x = agent.x; y = agent.y; atype = agent.type
			resource_consumed          = min(r_obj.resource_grid[x][y], model.consumption_fn[atype](x, y, r_obj.resource_grid))
			agent.atp                 += model.production_fn[atype](resource_consumed)
			r_obj.resource_grid[x][y] -= resource_consumed

			# divide if divage crossed
			if agent.age % agent.div_age == 0 and agent.atp >= agent.food_req:
				new_x, new_y  = agent.find_division_loc(x, y, self.config_obj.grid_size)
				new_info_dict = {'X': new_x, 'Y': new_y, 'Type': agent.type}
				new_agents[free_index] = Agent.Agent(free_index, new_info_dict)
				free_index += 1
				agent.div  += 1
				agent.atp   = 0

			# die if max_no_of_div crossed
			if agent.div >= agent.max_div:
				dead_agents.append(agent.index)

		model.initialize_states(new_agents)
		for key in dead_agents:
			self.agents_obj.agents.pop(key)
		self.agents_obj.agents.update(new_agents)

	def handleTimeStepForAllAgents(self):
		#Too ensure concurrency we update agent.next_state in method handleTimeStepAsAgent
		#After every agent has updated next_state we update states of all agents in method handleTimeStep()
		for state in self.state_list:
			self.state_list[state] = []
		for agent in self.agents_obj.agents.values():
			self.state_list[agent.type].append(agent.index)

	def endTimeStep(self):
		self.store_state()

	def endSimulation(self):
		return self.state_history

	def store_state(self, start = False):
		if(self.stats):
			statFile = open(self.config_obj.example_path + '/Statistics.txt', 'a')
			if start:
				if self.world_number == 0:
					statFile.write('\nInitial Microbe Distribution\n')
					for state in self.state_list:
						statFile.write('\t' + state + ': ' + str(self.state_list[state]) + '\n')
			else:
				statFile.write('\nTime Step: ' + str(self.current_time_step + 1) + '\n')
				for state in self.state_list:
					statFile.write('\t' + state + ': ' + str(self.state_list[state]) + '\n')
			statFile.close()
		for state in self.state_history.keys():
			self.state_history[state].append(len(self.state_list[state]))
