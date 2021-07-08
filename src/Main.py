import ReadFile
import World
import argparse
from Utility import *

if __name__=="__main__":

    arg_parser = argparse.ArgumentParser(prog='Main.py', usage='%(prog)s Example_Name [options]')

    # input argument options
    arg_parser.add_argument("Example_Name")
    arg_parser.add_argument("-np", "--noplot", help="doesn't show plot after simulation", required = False, action = "store_true")
    arg_parser.add_argument("-s" , "--stats" , help="creates Statistics.txt file in the example folder", required = False, action = "store_true")
    arg_parser.add_argument("-r", "--resource_stats", help="creates ResourceStats.txt file in the example folder", required=False, action="store_true")
    arg_parser.add_argument("-a", "--animate", help="creates gif animation in the example folder", required=False, action="store_true")
    args = arg_parser.parse_args()

    example_path = args.Example_Name
    config_filename = get_config_path(example_path)

    visual.eraseOldResults(example_path)

    stats = args.stats
    plot  = not args.noplot
    anim  = args.animate
    res   = args.resource_stats

    # Read Config File
    config_obj = ReadFile.ReadConfiguration(config_filename, example_path)

    # User Model
    model = get_model(example_path)

    # Creation of World object
    world_obj = World.World(config_obj, model)
    # Simulate Worlds
    world_obj.simulate_worlds(plot, stats, anim, res)
