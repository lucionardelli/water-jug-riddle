import sys

from jug_riddle.command_line import get_inputs, play_water_jug_riddle

if __name__ == "__main__":
    x, y ,z = get_inputs()
    play_water_jug_riddle(x, y, z)
    sys.exit(0)
