import sys
import ReadFile
import World
import importlib.util
import os
import os.path as osp
import argparse

def module_from_file(module_name, file_path):
    spec = importlib.util.spec_from_file_location(module_name, file_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module

def get_config_path(path):
    if osp.isdir(path):
        config_filepath=osp.join(path,'config.txt')
        return config_filepath
    else:
        print("ERROR: The Folder \"" + path + "\" was not found!")
        exit()

def get_model(example_path):
    UserModel = module_from_file("Generate_model", osp.join(example_path,'UserModel.py'))
    model = UserModel.UserModel()
    return model

if __name__=="__main__":

    arg_parser = argparse.ArgumentParser(prog='Main.py', usage='%(prog)s Example_Name [options]')

    # input argument options
    arg_parser.add_argument("Example_Name")
    arg_parser.add_argument("-np", "--noplot", help="doesn't show plot after simulation", required = False, action = "store_true")
    arg_parser.add_argument("-s" , "--stats" , help="creates statistics.txt file in the example folder", required = False, action = "store_true")
    arg_parser.add_argument("-a", "--animate", help="creates gif animation in the example folder", required=False, action="store_true")
    args = arg_parser.parse_args()

    example_path = args.Example_Name
    config_filename = get_config_path(example_path)

    if osp.isfile(example_path + '/Statistics.txt'):
        os.remove(example_path + '/Statistics.txt')

    stats = args.stats
    plot = not args.noplot
    anim = args.animate

    # Read Config File
    config_obj = ReadFile.ReadConfiguration(config_filename, example_path)

    # User Model
    model = get_model(example_path)

    # Creation of World object
    world_obj = World.World(config_obj, model)
    # Simulate Worlds
    world_obj.simulate_worlds(plot, stats, anim)
