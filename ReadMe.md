# Phoenix : Microbial Growth Simulation Platform
Phoenix is a general purpose microbial growth simulation platform and is built to handle a wide variety of biological phenomena. It’s main aim is to assist research in microbiology. But it can be developed into an educational tool as well. This might be useful in times when labs are inaccessible. Further, current research simulators use partial differentials for modelling which provides very limited scope for experimentation. Agent based simulators like Phoenix can provide a lot more flexibility and can handle almost any input.<br>

## Dependencies

To install dependencies run ```pip install -r requirements.txt```.

## Running Examples
Type the following commands in terminal and hit enter to run the code -

	cd examples
	python ../src/Main.py <Example_Name> -np -s -a -r

> **NOTE** <br>
>1. The arguments -np [*--noplot*], -s [*--stats*], -r [*--resource_stats*] and -a [*--animation*] are optional.
>2. Add *--noplot* if you don't wish to display the plot after the simulation. 
>3. The *--stats* argument creates a *statistics.txt* file in the *Example_Name* folder.
>4. The *--animation* argument creates a *results.gif* file in the *Example_Name* folder.
>5. The *--resource_stats* argument creates a *ResourceStats.txt* file in the *Example_Name* folder.
>6. Images of grid distributions of all mircobes is saved in the *Example_Name* folder.
