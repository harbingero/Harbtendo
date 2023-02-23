# TO DO:
# create a list of all map location numbers
# create battle decision function
# flesh out battle values function
# determine if I need to go back and heal after battle (Poison, low HP, etc.)
# figure out if after a level up, if a Pokémon is learning a new move
import struct
import colorama
from colorama import Fore
import random
from pyboy import PyBoy
from pyboy import botsupport
from pyboy import WindowEvent
from pyboy import openai_gym
import pyboy.plugins

appended = ""
started = False
named = False
pathed_to_starters = False
map_number_name = ["Pallet Town",
                   "Viridian City",
                   "",
                   "",
                   "",
                   "",
                   "",
                   "",
                   "",
                   "",
                   "",
                   "",
                   "Route 1",
                   "",
                   "",
                   "",
                   "",
                   "",
                   "",
                   "",
                   "",
                   "",
                   "",
                   "",
                   "",
                   "",
                   "",
                   "",
                   "",
                   "",
                   "",
                   "",
                   "",
                   "",
                   "",
                   "",
                   "",
                   "Mom's Room",
                   "Bedroom",
                   "Gary's House",
                   "Oak's Lab",
                   "Viridian City Pokecenter",
                   "Viridian City Pokemart",
                   "Viridian City South House",
                   "Viridian City North House",
                   "",
                   "",
                   "",
                   "",
                   "",
                   "",
                   "",
                   "",
                   "",
                   "",
                   "",
                   "",
                   "",
                   "",
                   "",
                   "",
                   "",
                   "",
                   "",
                   "",
                   ""]
starters = ["Charmander", "Squirtle", "Bulbasaur"]
play_time = 50000
regain_control = False
overwrite = True
controlled_ticks = 0
letter_axis = {"a": "00",
               "b": "10",
               "c": "20",
               "d": "30",
               "e": "40",
               "f": "50",
               "g": "60",
               "h": "70",
               "i": "80",
               "j": "01",
               "k": "11",
               "l": "21",
               "m": "31",
               "n": "41",
               "o": "51",
               "p": "61",
               "q": "71",
               "r": "81",
               "s": "02",
               "t": "12",
               "u": "22",
               "v": "32",
               "w": "42",
               "x": "52",
               "y": "62",
               "z": "72",
               " ": "82",
               "*": "03",
               "(": "13",
               ")": "23",
               ":": "33",
               ";": "43",
               "[": "53",
               "]": "63",
               "#": "73",  # pk
               "$": "83",  # mn
               "-": "04",
               "?": "14",
               "!": "24",
               "^": "34",  # ♂
               "%": "44",  # ♀
               "/": "54",
               ".": "64",
               ",": "74",
               "&": "84"}  # (*)=x,  (#)=pk, ($)=mn, (^)=♂, (%)=♀, (&)=End
player_name = ["Jesse", "Josh", "Sam", "Dakota", "Ash", "Smant"]
rival_name = ["Blue", "Gio", "Trash", "Oak", "Gary", "Logan"]
pokemon_name = ["Good Boy", "Puppy", "Slave", "Legend"]
map_no_paths = {"Bedroom": ["00", "05", "06", "33", "34", "65", "66"],
                "Mom's Room": ["00", "01", "30", "33", "34", "43", "44", "53"]}
map_destinations = {"Bedroom": ["70"],
                    "Mom's Room": ["27", "37", "70"]}
#  0 Pallet Town
#  1 Viridian City
#  12 Route 1
#  33 Left of Viridian City
#  37 Downstairs home
#  38 Bedroom
#  39 Gary's house
#  40 Oak's lab
#  41 Viridian City Pokemon Center
#  42 Viridian City Pokemart
#  43 Viridian City House
#  44 Viridian City House

if overwrite:
    with open("debug.txt", "w") as f1:
        f1.write("")


def tick_pass(number):
    printer_number = number
    if number <= 0:
        return None
    while number > 0:
        save_values(9999999)
        pyboy.tick()
        number -= 1
    print("----------------------------", printer_number)
#  A future potential improvement on the code would be to append button presses to show what inputs it's getting.
#  I'm sure I would have to modify each of these functions to tick elsewhere.  This would allow multiple inputs at once.


def hold_up(x):
    pyboy.send_input(WindowEvent.PRESS_ARROW_UP)
    tick_pass(x)
    pyboy.send_input(WindowEvent.RELEASE_ARROW_UP)
    print("Up--------------------------", x)


def hold_down(x):
    pyboy.send_input(WindowEvent.PRESS_ARROW_DOWN)
    tick_pass(x)
    pyboy.send_input(WindowEvent.RELEASE_ARROW_DOWN)
    print("--Down----------------------", x)


def hold_left(x):
    pyboy.send_input(WindowEvent.PRESS_ARROW_LEFT)
    tick_pass(x)
    pyboy.send_input(WindowEvent.RELEASE_ARROW_LEFT)
    print("------Left------------------", x)


def hold_right(x):
    pyboy.send_input(WindowEvent.PRESS_ARROW_RIGHT)
    tick_pass(x)
    pyboy.send_input(WindowEvent.RELEASE_ARROW_RIGHT)
    print("----------Right-------------", x)


def hold_a(x):
    pyboy.send_input(WindowEvent.PRESS_BUTTON_A)
    tick_pass(x)
    pyboy.send_input(WindowEvent.RELEASE_BUTTON_A)
    print("---------------A------------", x)


def hold_b(x):
    pyboy.send_input(WindowEvent.PRESS_BUTTON_B)
    tick_pass(x)
    pyboy.send_input(WindowEvent.RELEASE_BUTTON_B)
    print("----------------B-----------", x)


def hold_start(x):
    pyboy.send_input(WindowEvent.PRESS_BUTTON_START)
    tick_pass(x)
    pyboy.send_input(WindowEvent.RELEASE_BUTTON_START)
    print("-----------------Start------", x)


def hold_select(x):
    pyboy.send_input(WindowEvent.PRESS_BUTTON_SELECT)
    tick_pass(x)
    pyboy.send_input(WindowEvent.RELEASE_BUTTON_SELECT)
    print("----------------------Select", x)


def press_up():
    pyboy.send_input(WindowEvent.PRESS_ARROW_UP)
    pyboy.tick()
    pyboy.send_input(WindowEvent.RELEASE_ARROW_UP)
    print("Up--------------------------")


def press_down():
    pyboy.send_input(WindowEvent.PRESS_ARROW_DOWN)
    pyboy.tick()
    pyboy.send_input(WindowEvent.RELEASE_ARROW_DOWN)
    print("--Down----------------------")


def press_left():
    pyboy.send_input(WindowEvent.PRESS_ARROW_LEFT)
    pyboy.tick()
    pyboy.send_input(WindowEvent.RELEASE_ARROW_LEFT)
    print("------Left------------------")


def press_right():
    pyboy.send_input(WindowEvent.PRESS_ARROW_RIGHT)
    pyboy.tick()
    pyboy.send_input(WindowEvent.RELEASE_ARROW_RIGHT)
    print("----------Right-------------")


def press_a():
    pyboy.send_input(WindowEvent.PRESS_BUTTON_A)
    pyboy.tick()
    pyboy.send_input(WindowEvent.RELEASE_BUTTON_A)
    print("---------------A------------")


def press_b():
    pyboy.send_input(WindowEvent.PRESS_BUTTON_B)
    pyboy.tick()
    pyboy.send_input(WindowEvent.RELEASE_BUTTON_B)
    print("----------------B-----------")


def press_start():
    pyboy.send_input(WindowEvent.PRESS_BUTTON_START)
    pyboy.tick()
    pyboy.send_input(WindowEvent.RELEASE_BUTTON_START)
    print("-----------------Start------")


def press_select():
    pyboy.send_input(WindowEvent.PRESS_BUTTON_SELECT)
    pyboy.tick()
    pyboy.send_input(WindowEvent.RELEASE_BUTTON_SELECT)
    print("----------------------Select")

# An attempt to refactor the naming function can be as easy as creating a dictionary with each potential character
# and a value of x and y coordinates.  Then figure out the delta x, and delta y.  Move accordingly


def spell_name(name):
    xi = 55
    for i in range(1):
        press_b()
        tick_pass(xi)
    x = 0
    y = 0
    caps = True
    for letter in name:
        x_true = False
        y_true = False
        while x_true is False and y_true is False:
            destination = letter_axis[letter.lower()]
            delta_x = int(destination[0]) - x
            delta_y = int(destination[1]) - y
            if delta_x == 0:
                x_true = True
            if delta_y == 0:
                y_true = True
            if delta_x > 0:
                for i in range(delta_x):
                    press_right()
                    tick_pass(xi)
                    x = x + 1
            if delta_x < 0:
                delta_x = delta_x * (-1)
                for i in range(delta_x):
                    press_left()
                    tick_pass(xi)
                    x = x - 1
            if delta_y > 0:
                for i in range(delta_y):
                    press_down()
                    tick_pass(xi)
                    y = y + 1
            if delta_y < 0:
                delta_y = delta_y * (-1)
                for i in range(delta_y):
                    press_up()
                    tick_pass(xi)
                    y = y - 1
        press_a()
        tick_pass(xi)
        print(caps)
        if caps:
            press_select()
            tick_pass(xi)
            caps = False
        if letter == " ":
            press_select()
            tick_pass(xi)
            caps = True
    press_start()
    tick_pass(xi)


def naming(fun_named):
    xi = 120
    xj = 60
    for h in range(25):  # 25
        press_b()
        tick_pass(xj)
    press_a()
    tick_pass(xi)
    spell_name(player_name[random.randint(0, len(player_name) - 1)])
    for k in range(11):  # 11
        press_b()
        tick_pass(xj)
    tick_pass(xi)
    press_a()
    tick_pass(xi)
    spell_name(rival_name[random.randint(0, len(rival_name) - 1)])
    for c in range(12):  # 12
        press_b()
        tick_pass(xj)
    fun_named = True
    return fun_named


# def overworld_move(map_number, x, y):
#     print(map_number)
#     map_name = map_number_name[map_number]
#     no_paths = map_no_paths[map_name]
#     if len(map_destinations[map_name]) < 2:
#         random_destination = random.randint(0, len(map_destinations[map_name]) - 1)
#     else:
#         random_destination = 0
#     destination = map_destinations[map_name][random_destination]
#     print(destination)
#     print(no_paths)
#     while x != int(destination[0]) and y != int(destination[1]):
#         try_left = True
#         try_right = True
#         try_up = True
#         try_down = True
#         print(destination[0], destination[1])
#         delta_x = int(destination[0]) - x
#         delta_y = int(destination[1]) - y
#         if delta_x > 0:  # Try right
#             trying = str(int(x+1)) + y
#             for position in no_paths:
#                 if trying in position:
#                     try_right = False
#         if delta_x < 0:  # Try left
#             trying = str(int(x-1)) + y
#             for position in no_paths:
#                 if trying in position:
#                     try_left = False
#         if delta_y > 0:  # Try down
#             trying = x + str(int(y+1))
#             for position in no_paths:
#                 if trying in position:
#                     try_down = False
#         if delta_y < 0:  # Try up
#             trying = x + str(int(y-1))
#             for position in no_paths:
#                 if trying in position:
#                     try_up = False
#         print("UP: ", try_up, "\nDOWN: ", try_down, "\nLEFT: ", try_left, "\nRIGHT: ", try_right)
#         vert_or_hori = random.randint(0, 1)   #  0=vertical 1=horizontal
#         if vert_or_hori == 0
#         riup_or_ledo = random.randint(0, 4)  # 0,1,2=towards direction 3=opposite direction
#               #  To continue I need to go left/right and determine if I can go into the next square
#     return x, y  #  Once this function is done, I need to delete the while loop under where this is being implimented in to_starters and impliment this in Mom's room as well.xi = 55



def to_starters(name):
    walk_speed = 21
    transition = 40
    oak_walk = 500
    random_starter = random.randint(0, 2)
    x = 3
    y = 5
    tick_pass(250)
    # x, y = overworld_move(pyboy.get_memory_value(54110), x, y)
    while pyboy.get_memory_value(54110) == 38:
        hold_right(walk_speed * 1)
        hold_up(walk_speed * 1)
    tick_pass(transition)  # Out of room
    hold_down(walk_speed * 5)
    hold_left(walk_speed * 4)
    hold_down(walk_speed)
    tick_pass(transition)  # Out of house
    hold_right(walk_speed * 5)
    hold_up(walk_speed * 5)
    for i in range(1250):  # In grass
        press_b()
        pyboy.tick()
    # tick_pass(oak_walk)
    hold_down(walk_speed - 5)
    hold_right((walk_speed - 3) * (1 + random_starter))
    hold_up(walk_speed)
    press_a()
    for i in range(350):  # Starter selected
        press_a()
        pyboy.tick()
    for i in range(20):
        press_b()
        pyboy.tick()
    spell_name(name)
    for i in range(280):
        press_a()
        pyboy.tick()


def to_rival_battle1():
    pass  # Finish the path from starter to challenge the rival


def save_values(tick_number):
    with open("debug.txt", "a") as f:
        other_battle_type = pyboy.get_memory_value(53335)
        battle_type = pyboy.get_memory_value(53338)
        direction = pyboy.get_memory_value(49417)
        grass = pyboy.get_memory_value(49671)
        badges = pyboy.get_memory_value(54102)
        map_number = pyboy.get_memory_value(54110)
        sprite_walk = pyboy.get_memory_value(49664)
        sprite_x_pos = pyboy.get_memory_value(49669)
        sprite_x_pos_delta = pyboy.get_memory_value(49667)
        sprite_y_pos = pyboy.get_memory_value(49668)
        sprite_y_pos_delta = pyboy.get_memory_value(49666)
        sprite_move_check = pyboy.get_memory_value(49672)
        move_status = pyboy.get_memory_value(49409)
        image_index = pyboy.get_memory_value(49410)
        animation_frame_counter = pyboy.get_memory_value(49416)
        undocumented = []
        for i in range(49418, 49423):
            undocumented.append(i)
        undocumented_appended = []
        for i in undocumented:
            undocumented_appended.append(pyboy.get_memory_value(i))

        player_input = []
        if len(pyboy.get_input()) > 0:
            for i in range(len(pyboy.get_input())):
                player_input.append(str(pyboy.get_input()[i]))
        print("Grass: ", grass, "128 while in, 0 while not")
        print(Fore.BLUE + "Move status: ", move_status)
        print("Image index: ", image_index)
        print("Animation Frame Counter: ", animation_frame_counter)
        print("Undocumented values: ", undocumented_appended)
        print(Fore.GREEN + "Map number:  ", str(map_number) + Fore.RESET)
        print("_________________________"
              "Number of ticks in over world in control " + str(tick_number) +
              "_________________________")
        f.write("Direction: " + str(direction) + "\t\t| 0: down, 4: up, 8: left, 12: right\nPlayer input: " +
                str(player_input))
        f.write("\nReady to move:  " + str(sprite_move_check) + "\t| 0=ready to move")
        f.write("\nMovement:  " + str(sprite_walk) + "\t\t| Countdown")
        f.write("\nPossition X:  " + str(sprite_x_pos) + "\nDelta X:  " + str(sprite_x_pos_delta) +
                "\nPossition Y:  " + str(sprite_y_pos) + "\nDelta Y:  " + str(sprite_y_pos_delta))
        f.write("\nPlayer in grass: " + str(grass) + "\t| 128 while in, 0 while not\n")
        f.write("Badges:  " + str(badges) + "\t\t| Binary values\n")
        # f.write("Battle Type:  " + str(other_battle_type) + "\t\t| 0 not in battle, 1 wild PKMN, 2 Trainer\n")
        f.write("\n_________________________"
                "^Number of ticks in over world in control " + str(tick_number) +
                "^_________________________\n\n")


#     49408: picture ID (fixed, loaded at map init)
#     49409: movement status (0: uninitialized, 1: ready, 2: delayed, 3: moving)
#     49410: sprite image index (changed on update, $ff if off screen, includes facing direction,
#           progress in walking animation and a sprite-specific offset)
#     49411: Y screen position delta (-1,0 or 1; added to 49412 on each walking animation update)
#     49412: Y screen position (in pixels, always 4 pixels above grid which makes sprites
#           appear to be in the center of a tile)
#     49413: X screen position delta (-1,0 or 1; added to 49414 on each walking animation update)
#     49414: X screen position (in pixels, snaps to grid if not currently walking)
#     49415: intra-animation-frame counter (counting upwards to 4 until 49416 is incremented)
#     49416: animation frame counter (increased every 4 updates, hold four states (totalling to 16 walking frames)
#     49417: facing direction (0: down, 4: up, 8: left, $c: right)
#     49418 to 49423 are unudocumented (if used)


def battle_values():
    with open("debug.txt", "a") as f0:
        other_battle_type = pyboy.get_memory_value(53335)
        battle_type = pyboy.get_memory_value(53338)
        battle_turn = pyboy.get_memory_value(52437)
        party_quantity = pyboy.get_memory_value(53603)
        party1 = pyboy.get_memory_value(53603)
        party2 = pyboy.get_memory_value(53603)
        party3 = pyboy.get_memory_value(53603)
        party4 = pyboy.get_memory_value(53603)
        party5 = pyboy.get_memory_value(53603)
        party6 = pyboy.get_memory_value(53603)
        player_input = []
        print("Battle type: ",  other_battle_type)
        if len(pyboy.get_input()) > 0:
            for i in range(len(pyboy.get_input())):
                player_input.append(str(pyboy.get_input()[i]))
        f0.write("Battle turn #:  " + str(battle_turn))
        f0.write("\nParty quantity:  " + str(party_quantity))
        f0.write("\nLead Pokemon:  " + str(party1))
        f0.write("\nParty 2:  " + str(party2))
        f0.write("\nParty 3:  " + str(party3))
        f0.write("\nParty 4:  " + str(party4))
        f0.write("\nParty 5:  " + str(party5))
        f0.write("\nParty 6:  " + str(party6))
        f0.write("\n_________________________^Number of turns in battle under your control " + str(battle_turn) +
                 "^_________________________\n\n")


# I can create a function that checks the map number value compared to the previous map number value you leave from
# and determine delta x and delta y between entrance x and y to destination x and y.
# Other finessing potential is checking if there is a direction you can go vs cannot


pyboy = PyBoy('Roms/Pokemon Red.gb')
increment = 0
for i in range(play_time):
    in_battle = pyboy.get_memory_value(53335)
    manager = pyboy.botsupport_manager()
    sprite0 = manager.sprite(0)
    if manager.sprite(0).on_screen and started is False:
        while started is False and sprite0.on_screen:
            sprite0 = manager.sprite(0)
            press_start()
            tick_pass(110)
        started = True
    if named is False and started:
        named = naming(named)
    if named and started and pathed_to_starters is False:
        starter_name = pokemon_name[random.randint(0, len(pokemon_name)-1)]
        to_starters(starter_name)
        pathed_to_starters = True
    if named and started and pathed_to_starters:
        regain_control = True
    if regain_control and in_battle == 0:
        save_values(controlled_ticks)
    if regain_control and in_battle != 0:
        battle_values()
    pyboy.tick()
    check = appended
    appended = ""
    if regain_control:
        controlled_ticks += 1
    # for j in range(42392, 42402):
    #     appended += str(pyboy.get_memory_value(j)) + ": "
    # if check != appended:
    #     print(check, "\n" + Fore.GREEN + appended + Fore.RESET)
    # else:
    #     print("Same")
    # appended = str(pyboy.get_memory_value(42392))  This section was used to find different
    # memory values at the beginning of the game.
    # for j in range(16384, 17000):
    #     appended += str(pyboy.get_memory_value(j)) + ": "
    # if i % 50 == 0:
    #     increment += 1
    #     pil_image = pyboy.screen_image()
    #     pil_image.save('screenshot' + str(increment) + '.png')
    # print(str(i) + "\n", manager.tilemap_window())
    # print(manager.tilemap_background())
    # for j in range(24):
    #     print(manager.sprite(j), "\n", manager.sprite(j).tiles)
else:
    pyboy.stop(save=False)
    # pyboy.send_input(WindowEvent.PRESS_BUTTON_START)
    # pyboy.tick()
    # pyboy.send_input(WindowEvent.RELEASE_BUTTON_START)
# while not pyboy.tick():
#     pass
# pyboy.stop(save=False)
#
#