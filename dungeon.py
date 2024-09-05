import curses
import map

'''
import os
# Clear screen
def clear():
    os.system('cls' if os.name == 'nt' else 'clear')
'''

# Current floor
floor = 0

# List to add char lists converted into strings to print graphics
view_strings = []

# where player is facing
direction = "north"

# what tile the player is currently in [x,y]
position = [0,0]

# is there a wall in front of player
is_there_wall = False

# are there stairs (0: none / 1: up / 2: down)
stairs = 0

# Update the view graphics based on the current position on the map
def update_view():

    global is_there_wall
    global stairs
    stairs = 0
    message = ""
    
    # Graphics view
    view_template = [
    "##############################",
    "#                            #",
    "#                            #",
    "#                            #",
    "#   +                    +   #",
    "#                            #     Press up to move forward",
    "#                            #     Press left/right to look left/right",
    "#                            #     Press down to look back",
    "#                            #     Press Q to quit",
    "#                            #     Press D to go down stairs",
    "#                            #     Press U to go up stairs",
    "#                            #     Press P to check the party",
    "#                            #",
    "#                            #",
    "#   +                    +   #",
    "#                            #",
    "#                            #",
    "#                            #",
    "##############################"]
    
    # Current floor layout
    layout = map.floors[floor]
    
    # char coordinates in the layout map [x,y]
    coordinate = [4*position[0]+2, 18-(2*position[1]+1)]
    
    # Convert view to lists to allow char editing
    view = []
    for line in view_template:
        string_list = list(line)
        view.append(string_list)
    
    # if there are stairs going up in current tile
    if layout[coordinate[1]][coordinate[0]] == "u":
        view[1][6] = "\\"
        view[1][23] = "/"
        for x in range(7,23):
            view[1][x] = "_"
        message = "You see stairs going up."
        stairs = 1

    # if there are stairs going down in current tile
    if layout[coordinate[1]][coordinate[0]] == "d":
        view[17][6] = "/"
        view[17][23] = "\\"
        for x in range(7,23):
            view[16][x] = "_"
        message = "You see stairs going down."
        stairs = 2

    # if there is text on the current tile
    #if layout[coordinate[1]][coordinate[0]] == "i":
    #    message = floor_text

    # NORTH ^
    if direction == "north":

    #### LEFT SIDE ####

        # if there's a wall on the LEFT
        if layout[coordinate[1]][coordinate[0]-2] == "|" or layout[coordinate[1]][coordinate[0]-2] == "=" or layout[coordinate[1]][coordinate[0]-2] == "#":
            view[1][1] = "\\"
            view[2][2] = "\\"
            view[3][3] = "\\"
            view[15][3] = "/"
            view[16][2] = "/"
            view[17][1] = "/"
            
            # if there's a door on the LEFT wall
            if layout[coordinate[1]][coordinate[0]-2] == "=":
                view[7][1] = "_"
                for y in range(8,16):
                    view[y][2] = "!"
                
        # if there's no wall on the LEFT but there's wall ahead
        elif layout[coordinate[1]-1][coordinate[0]-3] == "-":
            view[4][1] = "="
            view[4][2] = "="
            view[4][3] = "="
            view[14][1] = "="
            view[14][2] = "="
            view[14][3] = "="
            
        # if there's intersection between walls on the LEFT
        if layout[coordinate[1]-1][coordinate[0]-2] == "+":
            for y in range(5,14):
                view[y][4] = "|"
            
    #### RIGHT SIDE ####
            
        # if there's a wall on the RIGHT
        if layout[coordinate[1]][coordinate[0]+2] == "|" or layout[coordinate[1]][coordinate[0]+2] == "=" or layout[coordinate[1]][coordinate[0]+2] == "#":
            view[1][28] = "/"
            view[2][27] = "/"
            view[3][26] = "/"
            view[15][26] = "\\"
            view[16][27] = "\\"
            view[17][28] = "\\"
            
            # if there's a door on the RIGHT wall
            if layout[coordinate[1]][coordinate[0]+2] == "=":
                view[7][28] = "_"
                for y in range(8,16):
                    view[y][27] = "!"
            
        # if there's no wall on the RIGHT but there's wall ahead
        elif layout[coordinate[1]-1][coordinate[0]+3] == "-":
            view[4][26] = "="
            view[4][27] = "="
            view[4][28] = "="
            view[14][26] = "="
            view[14][27] = "="
            view[14][28] = "="
            
        # if there's intersection between walls on the RIGHT
        if layout[coordinate[1]-1][coordinate[0]+2] == "+":
            for y in range(5,14):
                view[y][25] = "|"
            
    #### FRONT SIDE ####
        
        # if there's a wall in FRONT
        if layout[coordinate[1]-1][coordinate[0]-1] == "-":
            for x in range(5, 25):
                view[4][x] = "="
                view[14][x] = "="
            is_there_wall = True
            
            # if there's a door in FRONT wall
            if layout[coordinate[1]-1][coordinate[0]] == "=":
                for y in range(8,15):
                    view[y][10] = "!"
                    view[y][19] = "!"
                for x in range(11,19):
                    view[8][x] = "¨"
                    view[14][x] = "-"
                is_there_wall = False
            
            # if there's a secret door
            if layout[coordinate[1]-1][coordinate[0]] == "#":
                is_there_wall = False
            
        # if there's no wall in FRONT
        else:
            
            is_there_wall = False
            
            # if there are stairs going up in the tile ahead
            if layout[coordinate[1]-2][coordinate[0]] == "u":
                for x in range(10,20):
                    view[5][x] = "_"
                for x in range(11,19):
                    view[6][x] = "_"
                view[6][10] = "\\"
                view[6][19] = "/"
            
            # if there are stairs going down in the tile ahead
            if layout[coordinate[1]-2][coordinate[0]] == "d":
                for x in range(11,19):
                    view[11][x] = "_"
                    view[12][x] = "_"
                view[12][10] = "/"
                view[12][19] = "\\"
                
    #### FRONT LEFT ####
            
            # if there's a wall in FRONT LEFT
            if layout[coordinate[1]-2][coordinate[0]-2] == "|" or layout[coordinate[1]-2][coordinate[0]-2] == "=" or layout[coordinate[1]-2][coordinate[0]-2] == "#":
                view[5][5] = "\\"
                view[6][6] = "\\"
                view[7][7] = "\\"
                view[11][7] = "/"
                view[12][6] = "/"
                view[13][5] = "/"
                
                # if there's a door in FRONT LEFT wall
                if layout[coordinate[1]-2][coordinate[0]-2] == "=":
                    view[9][6] = "!"
                    view[9][7] = "!"
                    view[10][6] = "!"
                    view[10][7] = "!"
                    view[11][6] = "!"
                
            # if there's no wall in FRONT LEFT but there's wall ahead
            elif layout[coordinate[1]-3][coordinate[0]-3] == "-":
                view[8][5] = "="
                view[8][6] = "="
                view[8][7] = "="
                view[10][5] = "="
                view[10][6] = "="
                view[10][7] = "="
            
            # if there's intersection in FRONT LEFT
            if layout[coordinate[1]-3][coordinate[0]-2] == "+":
                view[8][8] = "+"
                view[9][8] = "|"
                view[10][8] = "+"
            
    #### FRONT RIGHT ####
            
            # if there's a wall in FRONT RIGHT
            if layout[coordinate[1]-2][coordinate[0]+2] == "|" or layout[coordinate[1]-2][coordinate[0]+2] == "=" or layout[coordinate[1]-2][coordinate[0]+2] == "#":
                view[5][24] = "/"
                view[6][23] = "/"
                view[7][22] = "/"
                view[11][22] = "\\"
                view[12][23] = "\\"
                view[13][24] = "\\"

                # if there's a door in FRONT RIGHT wall
                if layout[coordinate[1]-2][coordinate[0]+2] == "=":
                    view[9][22] = "!"
                    view[9][23] = "!"
                    view[10][22] = "!"
                    view[10][23] = "!"
                    view[11][23] = "!"
                
            # if there's no wall in FRONT RIGHT but there's wall ahead
            elif layout[coordinate[1]-3][coordinate[0]+3] == "-":
                view[8][22] = "="
                view[8][23] = "="
                view[8][24] = "="
                view[10][22] = "="
                view[10][23] = "="
                view[10][24] = "="
            
            # if there's intersection in FRONT RIGHT
            if layout[coordinate[1]-3][coordinate[0]+2] == "+":
                view[8][21] = "+"
                view[9][21] = "|"
                view[10][21] = "+"
            
    #### FRONT FRONT ####

            # if there's a wall in FRONT of next tile
            if layout[coordinate[1]-3][coordinate[0]-1] == "-":
                for x in range(9,21):
                    view[8][x] = "="
                    view[10][x] = "="
                
                # if there's a door in the wall ahead of next tile
                if layout[coordinate[1]-3][coordinate[0]] == "=":
                    view[9][13] = "!"
                    view[9][14] = "¨"
                    view[9][15] = "¨"
                    view[9][16] = "!"
                    view[10][13] = "'"
                    view[10][16] = "'"


    # SOUTH v
    if direction == "south":

    #### LEFT SIDE ####

        # if there's a wall on the LEFT
        if layout[coordinate[1]][coordinate[0]+2] == "|" or layout[coordinate[1]][coordinate[0]+2] == "=" or layout[coordinate[1]][coordinate[0]+2] == "#":
            view[1][1] = "\\"
            view[2][2] = "\\"
            view[3][3] = "\\"
            view[15][3] = "/"
            view[16][2] = "/"
            view[17][1] = "/"
            
            # if there's a door on the LEFT wall
            if layout[coordinate[1]][coordinate[0]+2] == "=":
                view[7][1] = "_"
                for y in range(8,16):
                    view[y][2] = "!"
                
        # if there's no wall on the LEFT but there's wall ahead
        elif layout[coordinate[1]+1][coordinate[0]+3] == "-":
            view[4][1] = "="
            view[4][2] = "="
            view[4][3] = "="
            view[14][1] = "="
            view[14][2] = "="
            view[14][3] = "="
            
        # if there's intersection between walls on the LEFT
        if layout[coordinate[1]+1][coordinate[0]+2] == "+":
            for y in range(5,14):
                view[y][4] = "|"
            
    #### RIGHT SIDE ####
            
        # if there's a wall on the RIGHT
        if layout[coordinate[1]][coordinate[0]-2] == "|" or layout[coordinate[1]][coordinate[0]-2] == "=" or layout[coordinate[1]][coordinate[0]-2] == "#":
            view[1][28] = "/"
            view[2][27] = "/"
            view[3][26] = "/"
            view[15][26] = "\\"
            view[16][27] = "\\"
            view[17][28] = "\\"
            
            # if there's a door on the RIGHT wall
            if layout[coordinate[1]][coordinate[0]-2] == "=":
                view[7][28] = "_"
                for y in range(8,16):
                    view[y][27] = "!"
            
        # if there's no wall on the RIGHT but there's wall ahead
        elif layout[coordinate[1]+1][coordinate[0]-3] == "-":
            view[4][26] = "="
            view[4][27] = "="
            view[4][28] = "="
            view[14][26] = "="
            view[14][27] = "="
            view[14][28] = "="
            
        # if there's intersection between walls on the RIGHT
        if layout[coordinate[1]+1][coordinate[0]-2] == "+":
            for y in range(5,14):
                view[y][25] = "|"
            
    #### FRONT SIDE ####
            
        # if there's a wall in FRONT
        if layout[coordinate[1]+1][coordinate[0]+1] == "-":
            for x in range(5, 25):
                view[4][x] = "="
                view[14][x] = "="
            is_there_wall = True
            
            # if there's a door in FRONT wall
            if layout[coordinate[1]+1][coordinate[0]] == "=":
                for y in range(8,15):
                    view[y][10] = "!"
                    view[y][19] = "!"
                for x in range(11,19):
                    view[8][x] = "¨"
                    view[14][x] = "-"
                is_there_wall = False
            
            # if there's a secret door
            if layout[coordinate[1]+1][coordinate[0]] == "#":
                is_there_wall = False
            
        # if there's no wall in FRONT
        else:
        
            is_there_wall = False
            
            # if there are stairs going up in the tile ahead
            if layout[coordinate[1]+2][coordinate[0]] == "u":
                for x in range(10,20):
                    view[5][x] = "_"
                for x in range(11,19):
                    view[6][x] = "_"
                view[6][10] = "\\"
                view[6][19] = "/"
            
            # if there are stairs going down in the tile ahead
            if layout[coordinate[1]+2][coordinate[0]] == "d":
                for x in range(11,19):
                    view[11][x] = "_"
                    view[12][x] = "_"
                view[12][10] = "/"
                view[12][19] = "\\"
                
    #### FRONT LEFT ####
            
            # if there's a wall in FRONT LEFT
            if layout[coordinate[1]+2][coordinate[0]+2] == "|" or layout[coordinate[1]+2][coordinate[0]+2] == "=" or layout[coordinate[1]+2][coordinate[0]+2] == "#":
                view[5][5] = "\\"
                view[6][6] = "\\"
                view[7][7] = "\\"
                view[11][7] = "/"
                view[12][6] = "/"
                view[13][5] = "/"
                
                # if there's a door in FRONT LEFT wall
                if layout[coordinate[1]+2][coordinate[0]+2] == "=":
                    view[9][6] = "!"
                    view[9][7] = "!"
                    view[10][6] = "!"
                    view[10][7] = "!"
                    view[11][6] = "!"
                
            # if there's no wall in FRONT LEFT but there's wall ahead
            elif layout[coordinate[1]+3][coordinate[0]+3] == "-":
                view[8][5] = "="
                view[8][6] = "="
                view[8][7] = "="
                view[10][5] = "="
                view[10][6] = "="
                view[10][7] = "="
            
            # if there's intersection in FRONT LEFT
            if layout[coordinate[1]+3][coordinate[0]+2] == "+":
                view[8][8] = "+"
                view[9][8] = "|"
                view[10][8] = "+"
            
    #### FRONT RIGHT ####
            
            # if there's a wall in FRONT RIGHT
            if layout[coordinate[1]+2][coordinate[0]-2] == "|" or layout[coordinate[1]+2][coordinate[0]-2] == "=" or layout[coordinate[1]+2][coordinate[0]-2] == "#":
                view[5][24] = "/"
                view[6][23] = "/"
                view[7][22] = "/"
                view[11][22] = "\\"
                view[12][23] = "\\"
                view[13][24] = "\\"

                # if there's a door in FRONT RIGHT wall
                if layout[coordinate[1]+2][coordinate[0]-2] == "=":
                    view[9][22] = "!"
                    view[9][23] = "!"
                    view[10][22] = "!"
                    view[10][23] = "!"
                    view[11][23] = "!"
                
            # if there's no wall in FRONT RIGHT but there's wall ahead
            elif layout[coordinate[1]+3][coordinate[0]-3] == "-":
                view[8][22] = "="
                view[8][23] = "="
                view[8][24] = "="
                view[10][22] = "="
                view[10][23] = "="
                view[10][24] = "="
            
            # if there's intersection in FRONT RIGHT
            if layout[coordinate[1]+3][coordinate[0]-2] == "+":
                view[8][21] = "+"
                view[9][21] = "|"
                view[10][21] = "+"
            
    #### FRONT FRONT ####

            # if there's a wall in FRONT of next tile
            if layout[coordinate[1]+3][coordinate[0]+1] == "-":
                for x in range(9,21):
                    view[8][x] = "="
                    view[10][x] = "="
                
                # if there's a door in the wall ahead of next tile
                if layout[coordinate[1]+3][coordinate[0]] == "=":
                    view[9][13] = "!"
                    view[9][14] = "¨"
                    view[9][15] = "¨"
                    view[9][16] = "!"
                    view[10][13] = "'"
                    view[10][16] = "'"


    # EAST >
    if direction == "east":

    #### LEFT SIDE ####

        # if there's a wall on the LEFT
        if layout[coordinate[1]-1][coordinate[0]+1] == "-":
            view[1][1] = "\\"
            view[2][2] = "\\"
            view[3][3] = "\\"
            view[15][3] = "/"
            view[16][2] = "/"
            view[17][1] = "/"
            
            # if there's a door on the LEFT wall
            if layout[coordinate[1]-1][coordinate[0]] == "=":
                view[7][1] = "_"
                for y in range(8,16):
                    view[y][2] = "!"
                
        # if there's no wall on the LEFT but there's wall ahead
        elif layout[coordinate[1]-2][coordinate[0]+2] == "|" or layout[coordinate[1]-2][coordinate[0]+2] == "=" or layout[coordinate[1]-2][coordinate[0]+2] == "#":
            view[4][1] = "="
            view[4][2] = "="
            view[4][3] = "="
            view[14][1] = "="
            view[14][2] = "="
            view[14][3] = "="
            
        # if there's intersection between walls on the LEFT
        if layout[coordinate[1]-1][coordinate[0]+2] == "+":
            for y in range(5,14):
                view[y][4] = "|"
            
    #### RIGHT SIDE ####
            
        # if there's a wall on the RIGHT
        if layout[coordinate[1]+1][coordinate[0]+1] == "-":
            view[1][28] = "/"
            view[2][27] = "/"
            view[3][26] = "/"
            view[15][26] = "\\"
            view[16][27] = "\\"
            view[17][28] = "\\"
            
            # if there's a door on the RIGHT wall
            if layout[coordinate[1]+1][coordinate[0]] == "=":
                view[7][28] = "_"
                for y in range(8,16):
                    view[y][27] = "!"
            
        # if there's no wall on the RIGHT but there's wall ahead
        elif layout[coordinate[1]+2][coordinate[0]+2] == "|" or layout[coordinate[1]+2][coordinate[0]+2] == "=" or layout[coordinate[1]+2][coordinate[0]+2] == "#":
            view[4][26] = "="
            view[4][27] = "="
            view[4][28] = "="
            view[14][26] = "="
            view[14][27] = "="
            view[14][28] = "="
            
        # if there's intersection between walls on the RIGHT
        if layout[coordinate[1]+1][coordinate[0]+2] == "+":
            for y in range(5,14):
                view[y][25] = "|"
            
    #### FRONT SIDE ####
            
        # if there's a wall in FRONT
        if layout[coordinate[1]][coordinate[0]+2] == "|" or layout[coordinate[1]][coordinate[0]+2] == "=" or layout[coordinate[1]][coordinate[0]+2] == "#":
            for x in range(5, 25):
                view[4][x] = "="
                view[14][x] = "="
            is_there_wall = True
            
            # if there's a door in FRONT wall
            if layout[coordinate[1]][coordinate[0]+2] == "=":
                for y in range(8,15):
                    view[y][10] = "!"
                    view[y][19] = "!"
                for x in range(11,19):
                    view[8][x] = "¨"
                    view[14][x] = "-"
                is_there_wall = False
            
            # if there's a secret door
            if layout[coordinate[1]][coordinate[0]+2] == "#":
                is_there_wall = False
                
        # if there's no wall in FRONT
        else:
        
            is_there_wall = False
        
            # if there are stairs going up in the tile ahead
            if layout[coordinate[1]][coordinate[0]+4] == "u":
                for x in range(10,20):
                    view[5][x] = "_"
                for x in range(11,19):
                    view[6][x] = "_"
                view[6][10] = "\\"
                view[6][19] = "/"
            
            # if there are stairs going down in the tile ahead
            if layout[coordinate[1]][coordinate[0]+4] == "d":
                for x in range(11,19):
                    view[11][x] = "_"
                    view[12][x] = "_"
                view[12][10] = "/"
                view[12][19] = "\\"
                
    #### FRONT LEFT ####
            
            # if there's a wall in FRONT LEFT
            if layout[coordinate[1]-1][coordinate[0]+3] == "-":
                view[5][5] = "\\"
                view[6][6] = "\\"
                view[7][7] = "\\"
                view[11][7] = "/"
                view[12][6] = "/"
                view[13][5] = "/"
                
                # if there's a door in FRONT LEFT wall
                if layout[coordinate[1]-1][coordinate[0]+4] == "=":
                    view[9][6] = "!"
                    view[9][7] = "!"
                    view[10][6] = "!"
                    view[10][7] = "!"
                    view[11][6] = "!"
                
            # if there's no wall in FRONT LEFT but there's wall ahead
            elif layout[coordinate[1]-2][coordinate[0]+6] == "|" or layout[coordinate[1]-2][coordinate[0]+6] == "=" or layout[coordinate[1]-2][coordinate[0]+6] == "#":
                view[8][5] = "="
                view[8][6] = "="
                view[8][7] = "="
                view[10][5] = "="
                view[10][6] = "="
                view[10][7] = "="
            
            # if there's intersection in FRONT LEFT
            if layout[coordinate[1]-1][coordinate[0]+6] == "+":
                view[8][8] = "+"
                view[9][8] = "|"
                view[10][8] = "+"
            
    #### FRONT RIGHT ####
            
            # if there's a wall in FRONT RIGHT
            if layout[coordinate[1]+1][coordinate[0]+3] == "-":
                view[5][24] = "/"
                view[6][23] = "/"
                view[7][22] = "/"
                view[11][22] = "\\"
                view[12][23] = "\\"
                view[13][24] = "\\"

                # if there's a door in FRONT RIGHT wall
                if layout[coordinate[1]+1][coordinate[0]+4] == "=":
                    view[9][22] = "!"
                    view[9][23] = "!"
                    view[10][22] = "!"
                    view[10][23] = "!"
                    view[11][23] = "!"
                
            # if there's no wall in FRONT RIGHT but there's wall ahead
            elif layout[coordinate[1]+2][coordinate[0]+6] == "|" or layout[coordinate[1]+2][coordinate[0]+6] == "=" or layout[coordinate[1]+2][coordinate[0]+6] == "#":
                view[8][22] = "="
                view[8][23] = "="
                view[8][24] = "="
                view[10][22] = "="
                view[10][23] = "="
                view[10][24] = "="
            
            # if there's intersection in FRONT RIGHT
            if layout[coordinate[1]+1][coordinate[0]+6] == "+":
                view[8][21] = "+"
                view[9][21] = "|"
                view[10][21] = "+"
            
    #### FRONT FRONT ####

            # if there's a wall in FRONT of next tile
            if layout[coordinate[1]][coordinate[0]+6] == "|" or layout[coordinate[1]][coordinate[0]+6] == "=" or layout[coordinate[1]][coordinate[0]+6] == "#":
                for x in range(9,21):
                    view[8][x] = "="
                    view[10][x] = "="
                
                # if there's a door in the wall ahead of next tile
                if layout[coordinate[1]][coordinate[0]+6] == "=":
                    view[9][13] = "!"
                    view[9][14] = "¨"
                    view[9][15] = "¨"
                    view[9][16] = "!"
                    view[10][13] = "'"
                    view[10][16] = "'"


    # WEST <
    if direction == "west":

    #### LEFT SIDE ####

        # if there's a wall on the LEFT
        if layout[coordinate[1]+1][coordinate[0]-1] == "-":
            view[1][1] = "\\"
            view[2][2] = "\\"
            view[3][3] = "\\"
            view[15][3] = "/"
            view[16][2] = "/"
            view[17][1] = "/"
            
            # if there's a door on the LEFT wall
            if layout[coordinate[1]+1][coordinate[0]] == "=":
                view[7][1] = "_"
                for y in range(8,16):
                    view[y][2] = "!"
                
        # if there's no wall on the LEFT but there's wall ahead
        elif layout[coordinate[1]+2][coordinate[0]-2] == "|" or layout[coordinate[1]+2][coordinate[0]-2] == "=" or layout[coordinate[1]+2][coordinate[0]-2] == "#":
            view[4][1] = "="
            view[4][2] = "="
            view[4][3] = "="
            view[14][1] = "="
            view[14][2] = "="
            view[14][3] = "="
            
        # if there's intersection between walls on the LEFT
        if layout[coordinate[1]+1][coordinate[0]-2] == "+":
            for y in range(5,14):
                view[y][4] = "|"
            
    #### RIGHT SIDE ####
            
        # if there's a wall on the RIGHT
        if layout[coordinate[1]-1][coordinate[0]-1] == "-":
            view[1][28] = "/"
            view[2][27] = "/"
            view[3][26] = "/"
            view[15][26] = "\\"
            view[16][27] = "\\"
            view[17][28] = "\\"
            
            # if there's a door on the RIGHT wall
            if layout[coordinate[1]-1][coordinate[0]] == "=":
                view[7][28] = "_"
                for y in range(8,16):
                    view[y][27] = "!"
            
        # if there's no wall on the RIGHT but there's wall ahead
        elif layout[coordinate[1]-2][coordinate[0]-2] == "|" or layout[coordinate[1]-2][coordinate[0]-2] == "=" or layout[coordinate[1]-2][coordinate[0]-2] == "#":
            view[4][26] = "="
            view[4][27] = "="
            view[4][28] = "="
            view[14][26] = "="
            view[14][27] = "="
            view[14][28] = "="
            
        # if there's intersection between walls on the RIGHT
        if layout[coordinate[1]-1][coordinate[0]-2] == "+":
            for y in range(5,14):
                view[y][25] = "|"
            
    #### FRONT SIDE ####
            
        # if there's a wall in FRONT
        if layout[coordinate[1]][coordinate[0]-2] == "|" or layout[coordinate[1]][coordinate[0]-2] == "=" or layout[coordinate[1]][coordinate[0]-2] == "#":
            for x in range(5, 25):
                view[4][x] = "="
                view[14][x] = "="
            is_there_wall = True
            
            # if there's a door in FRONT wall
            if layout[coordinate[1]][coordinate[0]-2] == "=":
                for y in range(8,15):
                    view[y][10] = "!"
                    view[y][19] = "!"
                for x in range(11,19):
                    view[8][x] = "¨"
                    view[14][x] = "-"
                is_there_wall = False
            
            # if there's a secret door
            if layout[coordinate[1]][coordinate[0]-2] == "#":
                is_there_wall = False
                
        # if there's no wall in FRONT
        else:
        
            is_there_wall = False
        
            # if there are stairs going up in the tile ahead
            if layout[coordinate[1]][coordinate[0]-4] == "u":
                for x in range(10,20):
                    view[5][x] = "_"
                for x in range(11,19):
                    view[6][x] = "_"
                view[6][10] = "\\"
                view[6][19] = "/"
            
            # if there are stairs going down in the tile ahead
            if layout[coordinate[1]][coordinate[0]-4] == "d":
                for x in range(11,19):
                    view[11][x] = "_"
                    view[12][x] = "_"
                view[12][10] = "/"
                view[12][19] = "\\"
                
    #### FRONT LEFT ####
            
            # if there's a wall in FRONT LEFT
            if layout[coordinate[1]+1][coordinate[0]-3] == "-":
                view[5][5] = "\\"
                view[6][6] = "\\"
                view[7][7] = "\\"
                view[11][7] = "/"
                view[12][6] = "/"
                view[13][5] = "/"
                
                # if there's a door in FRONT LEFT wall
                if layout[coordinate[1]+1][coordinate[0]-4] == "=":
                    view[9][6] = "!"
                    view[9][7] = "!"
                    view[10][6] = "!"
                    view[10][7] = "!"
                    view[11][6] = "!"
                
            # if there's no wall in FRONT LEFT but there's wall ahead
            elif layout[coordinate[1]+2][coordinate[0]-6] == "|" or layout[coordinate[1]+2][coordinate[0]-6] == "=" or layout[coordinate[1]+2][coordinate[0]-6] == "#":
                view[8][5] = "="
                view[8][6] = "="
                view[8][7] = "="
                view[10][5] = "="
                view[10][6] = "="
                view[10][7] = "="
            
            # if there's intersection in FRONT LEFT
            if layout[coordinate[1]+1][coordinate[0]-6] == "+":
                view[8][8] = "+"
                view[9][8] = "|"
                view[10][8] = "+"
            
    #### FRONT RIGHT ####
            
            # if there's a wall in FRONT RIGHT
            if layout[coordinate[1]-1][coordinate[0]-3] == "-":
                view[5][24] = "/"
                view[6][23] = "/"
                view[7][22] = "/"
                view[11][22] = "\\"
                view[12][23] = "\\"
                view[13][24] = "\\"

                # if there's a door in FRONT RIGHT wall
                if layout[coordinate[1]-1][coordinate[0]-4] == "=":
                    view[9][22] = "!"
                    view[9][23] = "!"
                    view[10][22] = "!"
                    view[10][23] = "!"
                    view[11][23] = "!"
                
            # if there's no wall in FRONT RIGHT but there's wall ahead
            elif layout[coordinate[1]-2][coordinate[0]-6] == "|" or layout[coordinate[1]-2][coordinate[0]-6] == "=" or layout[coordinate[1]-2][coordinate[0]-6] == "#":
                view[8][22] = "="
                view[8][23] = "="
                view[8][24] = "="
                view[10][22] = "="
                view[10][23] = "="
                view[10][24] = "="
            
            # if there's intersection in FRONT RIGHT
            if layout[coordinate[1]-1][coordinate[0]-6] == "+":
                view[8][21] = "+"
                view[9][21] = "|"
                view[10][21] = "+"
            
    #### FRONT FRONT ####

            # if there's a wall in FRONT of next tile
            if layout[coordinate[1]][coordinate[0]-6] == "|" or layout[coordinate[1]][coordinate[0]-6] == "=" or layout[coordinate[1]][coordinate[0]-6] == "#":
                for x in range(9,21):
                    view[8][x] = "="
                    view[10][x] = "="
                
                # if there's a door in the wall ahead of next tile
                if layout[coordinate[1]][coordinate[0]-6] == "=":
                    view[9][13] = "!"
                    view[9][14] = "¨"
                    view[9][15] = "¨"
                    view[9][16] = "!"
                    view[10][13] = "'"
                    view[10][16] = "'"
    
    view_strings.clear()
    for line in view:
        new_string = "".join(line)
        view_strings.append(new_string)

    view_strings.append(message)


# Call function at the start to draw the graphics
update_view()


### Print graphics

def update_text(window, text_lines, prev_text_lines):
    for i, line in enumerate(text_lines):
        if i >= len(prev_text_lines) or line != prev_text_lines[i]:
            window.addstr(i, 0, line.ljust(curses.COLS - 1))  # Clear the line
    window.refresh()  # Refresh to update the display

def main(stdscr):

    # Initialize curses
    curses.curs_set(0)  # Hide the cursor
    stdscr.nodelay(1)   # Don't block waiting for user input
    stdscr.timeout(100) # Wait 100ms for user input

    # Initial text
    current_text = view_strings
    previous_text = []

    # Key mappings
    key_up = curses.KEY_UP
    key_down = curses.KEY_DOWN
    key_left = curses.KEY_LEFT
    key_right = curses.KEY_RIGHT
    
    global direction
    global floor
    toggle_menu = False
    
    while True:
    
        key = stdscr.getch()
        
        # Move forward
        if key == key_up and is_there_wall == False:
            if direction == "north":
                position[1] = position[1]+1
            elif direction == "south":
                position[1] = position[1]-1
            elif direction == "east":
                position[0] = position[0]+1
            elif direction == "west":
                position[0] = position[0]-1
            update_view()
            current_text = view_strings
            
        # Look back
        elif key == key_down:
            if direction == "north":
                new_direction = "south"
            elif direction == "south":
                new_direction = "north"
            elif direction == "east":
                new_direction = "west"
            elif direction == "west":
                new_direction = "east"
            direction = new_direction
            update_view()
            current_text = view_strings
            
        # Turn left
        elif key == key_left:
            if direction == "north":
                new_direction = "west"
            elif direction == "south":
                new_direction = "east"
            elif direction == "east":
                new_direction = "north"
            elif direction == "west":
                new_direction = "south"
            direction = new_direction
            update_view()
            current_text = view_strings
            
        # Turn right
        elif key == key_right:
            if direction == "north":
                new_direction = "east"
            elif direction == "south":
                new_direction = "west"
            elif direction == "east":
                new_direction = "south"
            elif direction == "west":
                new_direction = "north"
            direction = new_direction
            update_view()
            current_text = view_strings
        
        # Go up stairs
        elif key == ord('u'):
            if stairs == 1:
                if floor == 0:
                    break;
                else:
                    floor = floor-1
                    update_view()
                    current_text = view_strings
                    
        # Go down stairs
        elif key == ord('d'):
            if stairs == 2:
                floor = floor+1
                update_view()
                current_text = view_strings
        
        # Check party
        elif key == ord('p'):
            if toggle_menu:
                current_text = view_strings
                toggle_menu = False
            else:
                current_text = ["##########################################",
                                "# Party                                  #",
                                "# Hero 1 | Warrior | 22/22 HP | Healthy  #",
                                "# Hero 2 | Cleric  | 18/18 HP | Healthy  #",
                                "# Hero 3 | Thief   | 15/15 HP | Poisoned #",
                                "# Hero 4 | Mage    | 10/10 HP | Healthy  #",
                                "#                                        #",
                                "##########################################"]
                toggle_menu = True
        
        elif key == ord('q'):  # Press 'q' to quit
            break

        # Update only the lines that changed compared to the previous state
        update_text(stdscr, current_text, previous_text)
        previous_text = current_text.copy()
        
        # Run the main function wrapped with curses.wrapper to initialize and cleanup
curses.wrapper(main)

# TODO:
# display floor messages

