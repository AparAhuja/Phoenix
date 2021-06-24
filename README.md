# Phoenix : Microbial Growth Simulation Platform
Phoenix is currently being used as a tool for game theoretic ananlysis of microbial growth.<br>

## Dependencies

To install dependencies using pipenv run ```pipenv install```.

## Running Examples
Type the following commands in terminal and hit enter to run the code -

	cd examples
	python ../src/Main.py <Example_Name> -noplot -stats


> **NOTE** <br>
1. The arguments *-noplot* and *-stats* are optional.
2. Add *-noplot* if you don't wish to see the plot after the simulation.
3. The *-stats* argument creates a *statistics.txt* file in the *Example_Name* folder.
4. All plots are stored in the *Example_Name* folder and shown after the simulation. 
5. Images of grid distributions of all mircobes is saved in the *Example_Name* folder.
