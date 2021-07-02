import matplotlib.pyplot as plt
import matplotlib.animation as ani
from PIL import Image
import numpy as np
import Simulate
import ReadFile

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

        if(stats):
            statFile = open(self.config_obj.example_path + '/Statistics.txt', 'a')
            if(world_number == 0):
                statFile.write('\n' + 'Initial Resource Grid' + '\n')
                for row in resource_obj.resource_grid:
                    for x in row:
                        statFile.write(str(x) + ' ')
                    statFile.write('\n')
            statFile.write('\nAll Time Step Stats | World Number - ' + str(world_number + 1))
            statFile.close()

        # Simulation Loop
        for i in range(time_steps):
            sim_obj.onStartTimeStep(i)
            sim_obj.handleTimeStepForAllAgents()
            sim_obj.endTimeStep()

        end_state = sim_obj.endSimulation()
        return end_state

    # Average number time series
    def average(self, tdict, number):
        for k in tdict.keys():
            l = tdict[k]
            for i in range(len(l)):
                tdict[k][i] /= number
        return tdict

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

        tdict = self.average(tdict, self.config_obj.worlds)

        # Statistics
        if(stats):
            statFile = open(self.config_obj.example_path + '/Statistics.txt', 'a')
            statFile.write('\n' + 'Overall Stats' + '\n')
            for x in tdict:
                statFile.write('Type: ' + x + '\n\tCount With Time:' + str(tdict[x]) + '\n')
            statFile.close()

        # Plotting
        for state in tdict:
            plt.plot(tdict[state])
        plt.title('Simulation Plot')
        plt.legend(list(tdict.keys()), loc='upper left', shadow=True)
        plt.ylabel('Number of Microbes in Grid')
        plt.xlabel('Time Steps (in unit steps)')
        plt.grid(b=True, which='major', color='#666666', linestyle='-')
        plt.minorticks_on()
        plt.grid(b=True, which='minor', color='#999999', linestyle='-', alpha=0.2)
        fig1 = plt.gcf()
        fig1.savefig(self.config_obj.example_path + '/results.jpg')
        if(plot):
            plt.show()
        if anim:
            fig = plt.figure()
            def buildmebarchart(i=int):
                plt.clf()
                plt.title('Simulation Plot')
                plt.ylabel('Number of Microbes in Grid')
                plt.xlabel('Time Steps (in unit steps)')
                plt.grid(b=True, which='major', color='#666666', linestyle='-')
                plt.minorticks_on()
                plt.grid(b=True, which='minor', color='#999999', linestyle='-', alpha=0.2)
                for state in tdict.keys():
                    plt.plot(tdict[state][:i], label = state)
                plt.legend(loc='upper left', shadow=True)
            animator = ani.FuncAnimation(fig, buildmebarchart, interval=150)
            animator.save(self.config_obj.example_path + '/results.gif')

        # Spread in Grid
        agent_locations = {}
        for agent in self.agents_obj.agents.values():
            agent_locations[agent.type] = (agent_locations.get(agent.type, [])) + [(agent.x, agent.y)]

        for state in self.model.individual_state_types:
            data = np.zeros((self.config_obj.grid_size, self.config_obj.grid_size, 3), dtype=np.uint8)
            max_for_state = 0
            for loc in agent_locations.get(state, []):
                data[loc[0], loc[1], 0] += 1
                max_for_state = max(max_for_state, data[loc[0], loc[1], 0])
            if max_for_state != 0:
                for i in range(self.config_obj.grid_size):
                    for j in range(self.config_obj.grid_size):
                        data[i, j, 0] *= 255/max_for_state
            img = Image.fromarray(data, 'RGB')
            img = img.resize((1600,1600))
            img.save(self.config_obj.example_path + '/Distribution_of_' + state + '.png')
