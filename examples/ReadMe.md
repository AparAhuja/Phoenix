# Phoenix : Microbial Growth Simulation Platform

## Files Required
1. config.txt<br>
2. UserModel.py<br>
3. agents.txt<br>
4. resource.txt (optional)

### 1. *config.txt*
>Grid Size <*grid_size*><br>
>Number of Worlds <*number_of_worlds*><br>
>Number of Time Steps <*number_of_time_steps*><br>
>Initial Agents Filename <*agents.txt*><br>
>Initial Resource Filename <*resource.txt*><br>
>Initial Enzyme Filename <*enzyme.txt*><br>


### 2. *UserModel.py*
```python
import Model

class UserModel(Model.ScheduledModel):
	def __init__(self):
		super(UserModel, self).__init__()
		self.resource_production_fn = lambda x, y, z : 1 
		# Format - self.insert_state(name, resource_consumption_fn, atp_production_fn, enzyme_production_fn, enzyme_consumption_fn, \
			 # division_age, min_atp_req_to_divide, no_of_div_before_death)
			 # provide the tuple (mean, std_dev) for division_age, min_atp_req_to_divide, no_of_div_before_death.
		# Example -
		self.insert_state( "Cooperator", lambda x, y : 1, lambda x : 2, lambda x : 0, lambda x : 0, (4, 1), (3, 1), (5, 3) )
		self.insert_state(  "Defector" , lambda x, y : 2, lambda x : 2, lambda x : 0, lambda x : 0, (3, 1), (5, 2), (6, 2) )
```

### 3. *agents.txt*
><pre>Time Step : Type       : X : Y</pre>
><pre>    0     : Cooperator : 0 : 1</pre>
><pre>    2     : Defector   : 3 : 4</pre>
><pre>    5     : Defector   : 1 : 3</pre>
><pre>    1     : Cooperator : 2 : 1</pre>


### 4. *resource.txt* (optional)
>2 0 0 0 2<br>
>0 2 0 2 0<br>
>0 0 5 0 0<br>
>0 2 0 2 0<br>
>2 0 0 0 2<br>

