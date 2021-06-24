# Phoenix : Microbial Growth Simulation Platform
Phoenix is simulation platform to study microbial growth.<br>

## Dependencies

To install dependencies using pipenv run ```pipenv install```.

## Running Examples
Type the following commands in terminal and hit enter to run the code -

	cd examples
	python ../src/Main.py <Example_Name> -noplot -stats

NOTE: -noplot and -stats are optional arguments. Plots are stored in the *Example_Name* folder and shown after the simulation. Add *-noplot* if you don't wish to see the plot after the simulation. The *-stats* argument creates a *statistics.txt* file in the *Example_Name* folder for analysis. Further, image distributions of all mircobes is saved in the *Example_Name* folder.
