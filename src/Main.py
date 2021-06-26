import sys
import ReadFile
import World
import importlib.util
import os.path as osp

def module_from_file(module_name, file_path):
    spec = importlib.util.spec_from_file_location(module_name, file_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module

def get_example_path():
    return sys.argv[1]

def get_config_path(path):
    if osp.isdir(path):
        config_filepath=osp.join(path,'config.txt')
        return config_filepath
    else:
        print("ERROR: \"" + path + "\" folder not found!")
        exit()

def get_model(example_path):
    UserModel = module_from_file("Generate_model", osp.join(example_path,'UserModel.py'))
    model = UserModel.UserModel()
    return model

if __name__=="__main__":

    example_path = get_example_path()
    config_filename = get_config_path(example_path)

    plot = True
    stats = False

    if osp.isfile(example_path + '/Statistics.txt'):
        statFile = open(example_path + '/Statistics.txt', 'w')
        statFile.close()

    if len(sys.argv) > 2:
        if sys.argv[2] == '-noplot':
            plot = False
        if sys.argv[2] == '-stats':
            stats = True

    if len(sys.argv) > 3:
        if sys.argv[3] == '-noplot':
            plot = False
        if sys.argv[3] == '-stats':
            stats = True

    # Read Config File
    config_obj = ReadFile.ReadConfiguration(config_filename, example_path)

    # User Model
    model = get_model(example_path)

    # Creation of World object
    world_obj = World.World(config_obj, model)
    # Simulate Worlds
    world_obj.simulate_worlds(plot, stats)
