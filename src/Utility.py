import importlib.util
import os.path as osp
import os
from PIL import Image
import numpy as np
import matplotlib.animation as ani
import matplotlib.pyplot as plt

class visual:
    def plotResults(tdict, plot):
        for state in tdict:
            plt.plot(tdict[state])
        plt.title('Simulation Plot')
        plt.legend(list(tdict.keys()), loc='upper left', shadow=True)
        plt.ylabel('Population')
        plt.xlabel('Time Steps (in unit steps)')
        plt.grid(b=True, which='major', color='#666666', linestyle='-')
        plt.minorticks_on()
        plt.grid(b=True, which='minor', color='#999999', linestyle='-', alpha=0.2)
        fig = plt.gcf()
        if plot:
            plt.show()
        fig.savefig('results.jpg')


    def animateResults(tdict, anim):
        if not anim:
            return
        fig = plt.figure()
        def buildmebarchart(i=int):
            plt.clf()
            plt.title('Simulation Plot')
            plt.ylabel('Population')
            plt.xlabel('Time Steps (in unit steps)')
            plt.grid(b=True, which='major', color='#666666', linestyle='-')
            plt.minorticks_on()
            plt.grid(b=True, which='minor', color='#999999', linestyle='-', alpha=0.2)
            for state in tdict.keys():
                plt.plot(tdict[state][:i], label=state)
            plt.legend(loc='upper left', shadow=True)
        animator = ani.FuncAnimation(fig, buildmebarchart, interval=150)
        animator.save('results.gif')


    def spatialPlotResults(agents_obj, config_obj, model):
        agent_locations = {}
        for agent in agents_obj.agents.values():
            agent_locations[agent.type] = (agent_locations.get(agent.type, [])) + [(agent.x, agent.y)]

        for state in model.individual_state_types:
            data = np.zeros((config_obj.grid_size, config_obj.grid_size, 3), dtype=np.uint8)
            max_for_state = 0
            for loc in agent_locations.get(state, []):
                data[loc[0], loc[1], 0] += 1
                max_for_state = max(max_for_state, data[loc[0], loc[1], 0])
            if max_for_state != 0:
                for i in range(config_obj.grid_size):
                    for j in range(config_obj.grid_size):
                        data[i, j, 0] *= 255/max_for_state
            img = Image.fromarray(data, 'RGB')
            img = img.resize((1600, 1600))
            img.save('Distribution_of_' + state + '.png')

    def eraseOldResults(example_path):
        mydir = osp.join(os.getcwd(), example_path)
        filelist = [f for f in os.listdir(mydir) if f.endswith((".gif", ".png"))]
        for file in filelist:
            os.remove(osp.join(example_path, file))
        if osp.isfile(example_path + '/Statistics.txt'):
            os.remove(example_path + '/Statistics.txt')
        if osp.isfile(example_path + '/ResourceStats.txt'):
            os.remove(example_path + '/ResourceStats.txt')

class stat:
    def saveWorld(config_obj, resource_obj, world_number, stats):
        if(stats):
            statFile = open(config_obj.example_path + '/Statistics.txt', 'a')
            if(world_number == 0):
                statFile.write('\n' + 'Initial Resource Grid' + '\n')
                for row in resource_obj.resource_grid:
                    for x in row:
                        statFile.write(str(x) + ' ')
                    statFile.write('\n')
            statFile.write(
                '\nAll Time Step Stats | World Number - ' + str(world_number + 1))
            statFile.close()

    def saveTimeStep(config_obj, world_number, current_time_step, state_list, stats, start = False):
        if not stats:
            return
        statFile = open(config_obj.example_path + '/Statistics.txt', 'a')
        if start:
            if world_number == 0:
                statFile.write('\nInitial Microbe Distribution\n')
                for state in state_list:
                    statFile.write('\t' + state + ': ' + str(state_list[state]) + '\n')
        else:
            statFile.write('\nTime Step: ' + str(current_time_step + 1) + '\n')
            for state in state_list:
                statFile.write('\t' + state + ': ' + str(state_list[state]) + '\n')
        statFile.close()

    def saveGrid(config_obj, resource_obj, current_time_step, res):
        if not res:
            return
        resFile = open(config_obj.example_path + '/ResourceStats.txt', 'a')
        resFile.write('Time Step: ' + str(current_time_step + 1) + '\n')
        for row in resource_obj.resource_grid:
            resFile.write(str(row) + '\n')
        resFile.write('\n\n')
        resFile.close()

    def saveOverall(tdict, stats):
        if(stats):
            statFile = open('Statistics.txt', 'a')
            statFile.write('\n' + 'Overall Stats' + '\n')
            for x in tdict:
                statFile.write(
                    'Type: ' + x + '\n\tCount With Time:' + str(tdict[x]) + '\n')
            statFile.close()

def module_from_file(module_name, file_path):
    spec = importlib.util.spec_from_file_location(module_name, file_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module

def get_config_path(path):
    if osp.isdir(path):
        config_filepath = osp.join(path, 'config.txt')
        return config_filepath
    else:
        print("ERROR: The Folder \"" + path + "\" was not found!")
        exit()

def get_model(example_path):
    UserModel = module_from_file("Generate_model", osp.join(example_path, 'UserModel.py'))
    model = UserModel.UserModel()
    return model

def average(tdict, number):
    for k in tdict.keys():
        l = tdict[k]
        for i in range(len(l)):
            tdict[k][i] /= number
    return tdict
