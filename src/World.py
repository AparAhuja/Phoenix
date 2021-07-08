from Utility import visual, stat, average
import Simulate
import ReadFile
import os

class World():
    def __init__(self, config_obj, model):
        self.config_obj = config_obj
        self.model      = model
        self.agents_obj = None

    def one_world(self, stats, res, world_number):
        time_steps = self.config_obj.time_steps

        # Initialize agents
        self.agents_obj = ReadFile.ReadAgents(self.config_obj)

        # Intialize resource grid
        resource_obj = ReadFile.ReadResource(self.config_obj)

        sim_obj = Simulate.Simulate(self.config_obj, self.model, self.agents_obj, resource_obj, stats, res, world_number)
        sim_obj.onStartSimulation()

        # Save Statistics
        stat.saveWorld(self.config_obj, resource_obj, world_number, stats)

        # Simulation Loop
        for i in range(time_steps):
            sim_obj.onStartTimeStep(i)
            sim_obj.handleTimeStepForAllAgents()
            sim_obj.endTimeStep()

        end_state = sim_obj.endSimulation()
        return end_state

    # Averages multiple simulations and plots a single plot
    def simulate_worlds(self, plot, stats, anim, res):

        tdict = {}
        for state in self.model.individual_state_types:
            tdict[state] = [0]*(self.config_obj.time_steps+1)

        for i in range(self.config_obj.worlds):
            sdict = self.one_world(stats, res, i)
            for state in self.model.individual_state_types:
                for j in range(len(tdict[state])):
                    tdict[state][j] += sdict[state][j]

        # Average number time series
        tdict = average(tdict, self.config_obj.worlds)

        # Enter example directory
        os.chdir(self.config_obj.example_path)

        # Save Statistics
        stat.saveOverall(tdict, stats)

        # Plotting
        visual.plotResults(tdict, plot)

        # Animation
        visual.animateResults(tdict, anim)

        # Spatial Growth
        visual.spatialPlotResults(self.agents_obj, self.config_obj, self.model)
