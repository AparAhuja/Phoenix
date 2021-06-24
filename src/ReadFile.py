import Agent
import re
import os.path as osp

class ReadConfiguration():
	def __init__(self,filename,example_path):
		self.worlds = self.time_steps = self.grid_size = self.agent_filename = self.glucose_filename = None

		f = open(filename,"r")

		self.grid_size        = (int)(self.get_value_config(f.readline()))
		self.worlds           = (int)(self.get_value_config(f.readline()))
		self.time_steps       = (int)(self.get_value_config(f.readline()))
		self.agent_filename   = self.get_value_config(f.readline())
		self.glucose_filename = self.get_value_config(f.readline())
		self.example_path     = example_path

		f.close()

	def get_value_config(self, line):
	    l = re.findall("\<.*?\>", line)
	    if len(l)!=1:
	        print("Error! Invalid entry in config.txt")
	        return None
	    return l[0][1:][:-1]

class BaseReadFile():

	def __init__(self):
		pass

	def get_value(self,line):
	    if line.endswith('\n'):
	        line=line[:-1]
	    return line

class ReadAgents(BaseReadFile):
	def __init__(self,config_obj):
		super().__init__()
		filename = config_obj.agent_filename
		f = open(osp.join(config_obj.example_path, filename),'r')
		self.n = int(self.get_value(f.readline()))
		agent_info_keys = self.get_value(f.readline())

		self.parameter_keys=agent_info_keys.split(':')
		self.agents = {}

		for i in range(self.n):
			info_dict = self.create_info_dict(self.get_value(f.readline()).split(':'))
			agent = Agent.Agent(i, info_dict)
			self.agents[agent.index] = agent
		f.close()

	def create_info_dict(self,info_list):
		info_dict = {}
		for i,key in enumerate(self.parameter_keys):
			info_dict[key] = info_list[i]
		return info_dict

class ReadResource(BaseReadFile):
	def __init__(self, config_obj):
		super().__init__()
		filename = config_obj.glucose_filename
		n = config_obj.grid_size
		self.resource_grid = [[0 for i in range(n)] for j in range(n)]
		if(filename != ''):
			f = open(filename,'r')
			for i in range(n):
				row_i = [int(x) for x in self.get_value(f.readline()).split()]
				self.resource_grid[i] = row_i
			f.close()
