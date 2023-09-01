from jug_riddle import Jug, JugAction, JugRiddle


def main(x: int, y: int, z: int) -> bool:

    riddle = JugRiddle(x, y, z)
    while not riddle.done:
        user_action = input("Fill, Empty, Transfer, Quit: ")
        user_action = user_action.upper()
        if user_action == "Q":
            print("You went kabooom!")
            return False
        action = None
        if user_action == "F":
            action = JugAction.FILL
        elif user_action == "E":
            action = JugAction.EMPTY
        elif user_action == "T":
            action = JugAction.TRANSFER
        else:
            print(f"Invalid user action '{user_action}'!")
        if action is not None:
            user_jug = input("Jug 1 or Jug 2? ")
            jug = None
            if user_jug == "1":
                jug = Jug.JUG_1
            elif user_jug == "2":
                jug = Jug.JUG_2
            else:
                print(f"Invalid jug '{user_jug}'")
            if jug is not None:
                riddle.take_action(jug, action)
            if riddle.almost_done:
                print("YOU ARE ALMOST THERE CHAMP!")
            print(riddle)
    print(f"YOU DID IT! (and it only took you {len(riddle)} actions)")
    print(riddle.view_solution())
    return True


def get_inputs():
    x = input("Jug1 size: ")
    y = input("Jug2 size: ")
    g = input("Goal: ")
    return int(x), int(y), int(g)


if __name__ == "__main__":
    import sys
    x, y, g = get_inputs()
    ret = main(x, y, g)
    sys.exit(0)
