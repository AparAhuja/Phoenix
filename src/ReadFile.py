import Agent
import re
import os.path as osp

class BaseReadFile():

	def __init__(self):
		pass

	def get_value(self,line):
	    if line.endswith('\n'):
	        line=line[:-1]
	    return line

	def FileNotFound(self, filename):
		print("ERROR: The File \'" + filename + "\' was not found!")
		exit()

class ReadConfiguration(BaseReadFile):
	def __init__(self, filename, example_path):
		self.worlds = self.time_steps = self.grid_size = self.agent_filename = self.glucose_filename = None

		try:
			f = open(filename, "r")
		except:
			self.FileNotFound("config.txt")

		self.grid_size = (int)(self.get_value_config(f.readline()))
		self.worlds = (int)(self.get_value_config(f.readline()))
		self.time_steps = (int)(self.get_value_config(f.readline()))
		self.agent_filename = self.get_value_config(f.readline())
		self.glucose_filename = self.get_value_config(f.readline())
		self.example_path = example_path

		f.close()

	def get_value_config(self, line):
	    l = re.findall("\<.*?\>", line)
	    if len(l) != 1:
	        print("Error! Invalid Entry in config.txt")
	        exit()
	    return l[0][1:][:-1]

class ReadAgents(BaseReadFile):
	def __init__(self,config_obj):
		super().__init__()
		filename = config_obj.agent_filename
		try:
			f = open(osp.join(config_obj.example_path, filename),'r')
		except:
			self.FileNotFound(self.filename)
		agent_info_keys = self.get_value(f.readline())
		self.parameter_keys = [key.strip().lstrip() for key in agent_info_keys.split(':')]
		self.agents   = {}
		self.agentsAt = {}
		index = 0
		for line in f:
			info_dict = self.create_info_dict(self.get_value(line).split(':'), index + 3)
			agent = Agent.Agent(index, info_dict)
			Time_Step = int(info_dict['Time Step'])
			if Time_Step == 0:
				self.agents[agent.index] = agent
			else:
				self.agentsAt[Time_Step] = self.agentsAt.get(Time_Step, []) + [agent]
			index += 1
		f.close()
		if not all(x in agent_info_keys for x in ['Time Step', 'Type', 'X', 'Y']):
			print("ERROR: Agents Key Error. \'Time Step\' or \'Type\' or \'X\' or \'Y\' is missing. Please check your agents file!")
			exit()

	def create_info_dict(self,info_list, line_number):
		info_dict = {}
		last_line = 0, "EMPTY_LINE"
		try:
			for i,key in enumerate(self.parameter_keys):
				info_dict[key] = info_list[i].strip().lstrip()
				last_line = ':'.join(info_list)
		except:
			print("ERROR: Missing parameters in agents file at line number " + str(line_number) + ": \'" + last_line + "\' !")
			exit()
		return info_dict

class ReadResource(BaseReadFile):
	def __init__(self, config_obj):
		super().__init__()
		filename = config_obj.glucose_filename
		n = config_obj.grid_size
		self.resource_grid = [[0 for i in range(n)] for j in range(n)]
		if(filename != ''):
			try:
				f = open(osp.join(config_obj.example_path, filename), 'r')
			except:
				self.FileNotFound(filename)
			for i in range(n):
				row_i = [int(x) for x in self.get_value(f.readline()).split()]
				self.resource_grid[i] = row_i
				if(len(row_i) != n):
					print("ERROR: Resource initilization error. Please check your resource file!")
					exit()
			f.close()
