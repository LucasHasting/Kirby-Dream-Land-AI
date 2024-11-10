import retro
import numpy as np
from sklearn import linear_model
import random
import time
import tkinter as tk

'''
https://www.geeksforgeeks.org/how-to-clear-out-a-frame-in-the-tkinter/
https://www.geeksforgeeks.org/python-gui-tkinter/
https://stackoverflow.com/questions/6920302/how-to-pass-arguments-to-a-button-command-in-tkinter
https://stackoverflow.com/questions/110923/how-do-i-close-a-tkinter-window
'''

#set the frames per second
FPS = 60
SLEEP_TIME = 1/4
MIN_MOVE_SIZE = 30
MAN_MOVE_SIZE = 60

#pit.state
#begginning.state
#door.state
#boss.state
STATE_FILE = "begginning.state"

#create map of inputs to position in action array
INPUTS = {
    "A": 8,
    "B": 0, 
    "UP": 4,
    "DOWN": 5,
    "LEFT": 6,
    "RIGHT": 7,
    "NULL": -1, 
    "UP-LEFT": 2,
    "UP-RIGHT": 3
    #unknown: 1, 2, 3
}

#create map of positions in action array to input
INVERSE_INPUTS = {
    8: "A",
    0: "B",
    4: "UP",
    5: "DOWN",
    6: "LEFT",
    7: "RIGHT",
    -1: "NULL",
    2: "UP-LEFT",
    3: "UP-RIGHT"
}

GAME_STATES = ["UNKOWN",
               "HORIZONTAL-RIGHT",
               "HORIZONTAL-LEFT",
               "VERTICAL-UP",
               "VERTICAL-DOWN",
               "BOSS",
               "DOOR-PRESENT"]

STATE_MAP = {
    "UNKOWN": 0,
    "HORIZONTAL-RIGHT": 1,
    "HORIZONTAL-LEFT": 2,
    "VERTICAL-UP": 3,
    "VERTICAL-DOWN": 4,
    "BOSS": 5,
    "DOOR-PRESENT": 6
}

def main():
    m = tk.Tk()
    main_menu(m)

def main_menu(m):
    button_1 = tk.Button(m, text='AI - Create data (play the first screen)', width=50, command=lambda: screen_one_play_file_gui(m))
    button_1.pack()
    button_2 = tk.Button(m, text='AI - Create data (play the full game - not finished)', width=50, command=lambda: game_driver(m))
    button_2.pack()
    button_3 = tk.Button(m, text='AI - Test Model (first screen only)', width=50, command=m.destroy)
    button_3.pack()
    button_4 = tk.Button(m, text='Record Gameplay - Human (first screen only)', width=50, command=m.destroy)
    button_4.pack()
    button_5 = tk.Button(m, text='Playback a recording', width=50, command=lambda: playback_gui(m))
    button_5.pack()
    button_6 = tk.Button(m, text='Quit', width=25, command=m.destroy)
    button_6.pack()
    m.mainloop()

def screen_one_play_file_gui(m):
    incorrect_count = [0]
    m.destroy()
    m = tk.Tk()
    label_1 = tk.Label(m, text="Enter data file: ")
    label_1.pack()
    text_1 = tk.Text(m, height=1, width=30)
    text_1.pack()
    label_2 = tk.Label(m, text="Enter move file: ")
    label_2.pack()
    text_2 = tk.Text(m, height=1, width=30)
    text_2.pack()
    button = tk.Button(m, text='Play the game!', width=25, command=lambda: screen_one_play_file_gui_validate(m, text_1, text_2, incorrect_count))
    button.pack()
    m.mainloop()

def screen_one_play_file_gui_validate(m, text_1, text_2, incorrect_count):
    if((text_1.get("1.0") == "\n" or text_2.get("1.0") == "\n") and incorrect_count[0] == 0):
        label = tk.Label(m, text="Please enter a file name!")
        label.pack()
        incorrect_count[0] += 1
    elif (text_1.get("1.0") != "\n" and text_2.get("1.0") != "\n"):
        game_driver(m, text_1.get("1.0", "end-1c").strip(), text_2.get("1.0", "end-1c").strip(), True)

def playback_gui(m):
    incorrect_count = [0]
    m.destroy()
    m = tk.Tk()
    label = tk.Label(m, text="Enter move file: ")
    label.pack()
    text = tk.Text(m, height=1, width=30)
    text.pack()
    button = tk.Button(m, text='Watch the game!', width=25, command=lambda: playback_gui_validate(m, text, incorrect_count))
    button.pack()
    m.mainloop()

def playback_gui_validate(m, text, incorrect_count):
    if(text.get("1.0") == "\n" and incorrect_count[0] == 0):
        label = tk.Label(m, text="Please enter a file name!")
        label.pack()
        incorrect_count[0] += 1
    elif (text.get("1.0") != "\n"):
        playback_driver(m, text.get("1.0", "end-1c").strip())

def get_data_from_file(file):
    data = []

    for line in file:
        line = line.split(",")
        line[0] = int(line[0])
        line[1] = int(line[1])
        data.append(line)

    return data
    
def playback_driver(m, text):
    m.destroy()
    move_data = get_data_from_file(open(text, "r"))
    moves = [x for x in (move[0] for move in move_data)]
    move_frames = [move[1] for move in move_data]

    env = retro.make('KirbysDreamLand-GB', STATE_FILE)
    env.reset()
    
    while(len(move_frames) != 0):
        
        #render the game
        new_render(env)

        move_size = move_frames[0]
        action = INVERSE_INPUTS[moves[0]]

        for i in range(move_size):
            new_render(env)
            ob, rew, done, info = env.step(make_action(action))

        move_frames.pop(0)
        moves.pop(0)

    env.render(close=True)
    env.close()
    
    m = tk.Tk()
    main_menu(m)

def game_driver(m, text_1 = "", text_2 = "", screen_one=False):
    m.destroy()
    current_state = GAME_STATES[0]
    data_file = 0
    move_file = 0

    #if first screen only, open data file for writing
    if(screen_one):
        data_file = open(text_1, "w")
        move_file = open(text_2, "w")
    
    #create the enviornment
    env = retro.make('KirbysDreamLand-GB', STATE_FILE)
    env.reset()

    #initilize default values
    total_data = []
    moves = []
    move_sizes = []

    model = 0
    move_size_model = 0
    
    #play the game
    while(True):
        
        #render the game
        new_render(env)

        #have kirby do nothing to get screen info
        ob, rew, done, info = env.step(make_action("NULL"))

        if(screen_one and info["game_state"] == 6):
            break

        #get the current state and its data
        state = env.em.get_state()
        before = load_data(info, STATE_MAP[current_state])

        #if a model has not been created
        if(model == 0 or current_state == "UNKOWN"):
            #get the current state and make a random move until it is good
            model, move_size_model, current_state = make_random_move(info, model, total_data, moves, state, env, move_size_model, move_sizes, before, current_state)
        else:
            #make a good move if the model is created
            model, move_size_model, current_state = make_move(info, model, total_data, moves, state, env, move_size_model, move_sizes, before, current_state)

    write_data_file(data_file, move_file, total_data, moves, move_sizes)

    env.render(close=True)
    env.close()

    m = tk.Tk()
    main_menu(m)

def write_data_file(file_1, file_2, data1, data2, data3):
    all_length = len(data1)
    for i in range(all_length):
        for j in range(len(data1[0])):
            file_1.write(str(data1[i][j]) + ",")

        file_1.write(str(data2[i]) + "\n")
        file_2.write(str(data2[i]) + ",")
        file_2.write(str(data3[i] * 2) + "\n")

    file_1.close()
    file_2.close()

def clear_all_inside_frame_tk(frame):
    # Iterate through every widget inside the frame
    for widget in frame.winfo_children():
        widget.destroy()  # deleting widget

#function is a renderer that uses the FPS to determine speed
def new_render(env):
    time.sleep(1/FPS)
    env.render()

#function used to make an action (player input)
def make_action(enter):
    action = [0] * 9
    if(INPUTS[enter] == 2):
        action[4] = 1
        action[6] = 1
    elif(INPUTS[enter] == 3):
        action[4] = 1
        action[7] = 1
    elif(INPUTS[enter] == -1):
        pass
    else:
        action[INPUTS[enter]] = 1
    return action

#get all the screen data (there is alot)
def load_screen_data(info):
    data = []
    for i in range(40):
        for j in range(4):
            data.append(info[f"screen{i+1}_{j}"])
    return data

#load in all the data
def load_data(info, current_state):
    screen_data = load_screen_data(info)
    kirby_health = info["kirby_health"]
    kirby_life = info["kirby_life"]
    boss_health = info["boss_health"]
    kirby_x_scrol = info["kirby_x_scrol"]
    kirby_x = info["kirby_x"]
    kirby_y_scrol = info["kirby_y_scrol"]
    kirby_y = info["kirby_y"]
    game_state = info["game_state"]

    return [*screen_data, current_state, game_state, boss_health, kirby_life, kirby_health, kirby_y, kirby_y_scrol, kirby_x_scrol, kirby_x]

#make a movement based on move predicited, predicts how long a move should be held
def make_movement(action, env, move_size_model):
    #predict move size
    move_size = move_size_model.predict([[INPUTS[action]]])
    move_size = round(move_size[0])

    #perform the move for move_size frames
    for i in range(move_size):
        new_render(env)
        ob, rew, done, info = env.step(make_action(action))

    #return info needed from making an action
    return ob, rew, done, info, move_size

#make a movement based on move predicited, has a random move size
def make_random_movement(action, env):
    #get random move size
    move_size = random.randrange(MIN_MOVE_SIZE, MAN_MOVE_SIZE)

    #perform the move for move_size frames
    for i in range(move_size):
        new_render(env)
        ob, rew, done, info = env.step(make_action(action))

    #return info needed from making an action
    return ob, rew, done, info, move_size

#function used to make a predicted move
def make_move(info, model, total_data, moves, state, env, move_size_model, move_sizes, before, current_state):

    #predict what move should be made 
    move = model.predict([before])
    move = move[0]

    #try two moves - account for pits
    make_movement(INVERSE_INPUTS[move], env, move_size_model)
    ob, rew, done, info, move_size = make_movement(INVERSE_INPUTS[move], env, move_size_model)
    time.sleep(SLEEP_TIME)

    #load data after the move was made
    after = load_data(info, STATE_MAP[current_state])

    #check game state
    current_state = determine_game_state([before[-2], before[-3], before[-7], before[-8]], current_state)
    print("Predicted: ", INVERSE_INPUTS[move], move_size, current_state)

    #determine if the move was good, if so, update the model. Otherwise, try a random move until a good move occurs
    if(good_move([before[-2], before[-1], before[-3], before[-4], before[-5], before[-6]], [after[-2], after[-1], after[-3], after[-4], after[-5], before[-6]], current_state)):
       add_to_data(total_data, after, moves, move, move_sizes, move_size)
       model = update_model(total_data, moves)
       move_size_model = update_move_size_model(moves, move_sizes)
    else:
        return make_random_move(info, model, total_data, moves, state, env, move_size_model, move_sizes, before, current_state)

    #return both models to be updated in the driver
    return model, move_size_model, current_state

#function used to make a random move
def make_random_move(info, model, total_data, moves, state, env, move_size_model, move_sizes, before, current_state):
    #load the previous state
    env.em.set_state(state)

    #make a random move
    move = INVERSE_INPUTS[random.randrange(2, 10) % 9]

    #try two moves - account for pits
    make_random_movement(move, env)
    ob, rew, done, info, move_size = make_random_movement(move, env)
    time.sleep(SLEEP_TIME)

    #load data after the move was made
    after = load_data(info, STATE_MAP[current_state])

    #check game state
    current_state = determine_game_state([after[-2], after[-3], after[-7], after[-8]], current_state)
    print(move, move_size, current_state)

    #determine if the move was good, if so, update the model. Otherwise, try again 
    if(good_move([before[-2], before[-1], before[-3], before[-4], before[-5], before[-6]], [after[-2], after[-1], after[-3], after[-4], after[-5], before[-6]], current_state)):
       add_to_data(total_data, after, moves, INPUTS[move], move_sizes, move_size)
       model = update_model(total_data, moves)
       move_size_model = update_move_size_model(moves, move_sizes)
    else:
        #use recursion to try again
        return make_random_move(info, model, total_data, moves, state, env, move_size_model, move_sizes, before, current_state)

    #return both models to be updated in the driver
    return model, move_size_model, current_state

#add data to lists to be used in an updated model
def add_to_data(total_data, new_data, moves, move, move_sizes, move_size):
    total_data.append(new_data)
    moves.append(move)
    move_sizes.append(move_size)
    
#update the move prediciton model
def update_model(total_data, moves):
    #if there are not enough moves to make the model, return 0
    if(len(list(set(moves))) < 2):
        return 0

    #make the move classification model
    model = linear_model.LogisticRegression(solver='liblinear', C=1)
    model.fit(total_data, moves)

    #return the model
    return model

#update the move size prediciton model
def update_move_size_model(moves, move_sizes):
    #update the move size prediciton model
    if(len(list(set(moves))) < 2):
        return 0

    #make the move classification model
    move_size_model = linear_model.LinearRegression()
    temp_moves = [[i] for i in moves]
    move_size_model.fit(temp_moves, move_sizes)

    #return the model
    return move_size_model

def determine_game_state(data_after, current_state):
    scroll_x = data_after[0]
    scroll_y = data_after[1]
    boss_health = data_after[2]
    game_state = data_after[3]
    #print(f"scroll_x: {scroll_x}, scroll_y: {scroll_y}, boss_health: {boss_health}, game_state: {game_state}")

    #set the game state
    if(current_state == "UNKOWN"):    
        if (scroll_x == 76):
            current_state = GAME_STATES[STATE_MAP["HORIZONTAL-RIGHT"]]
        elif (scroll_x == 68):
            current_state = GAME_STATES[STATE_MAP["HORIZONTAL-LEFT"]]
        elif (scroll_y == 76):
            current_state = GAME_STATES[STATE_MAP["VERTICAL-UP"]]
        elif (scroll_y == 84):
            current_state = GAME_STATES[STATE_MAP["VERTICAL-DOWN"]]
        elif (boss_health != 0):
            current_state = GAME_STATES[STATE_MAP["BOSS"]]

    #check to break the current game state
    else:
        if(game_state == 6):
            GAME_STATES[STATE_MAP["UNKOWN"]]

        conditions = [False]

        #if(current_state == "HORIZONTAL-RIGHT"):
        #    conditions.append(scroll_x > 76)
        #elif(current_state == "HORIZONTAL-LEFT"):
        #    conditions.append(scroll_x < 68)
        #elif(current_state == "VERTICAL-UP"):
        #    conditions.append(scroll_y < 76)
        #elif(current_state == "VERTICAL-DOWN"):
        #    conditions.append(scroll_y > 84)
        #elif(current_state == "BOSS"):
        #    conditions.append(boss_health == 0)
        
        #if(any(conditions)):
        #    current_state = GAME_STATES[STATE_MAP["DOOR-PRESENT"]]

    #set door present
    if(current_state != "UNKOWN"):
        if (((scroll_x > 76 or scroll_x < 68) and "HORIZONTAL" in current_state) or
            ((scroll_y > 84, scroll_y < 76) and "VERTICAL" in current_state)):
            current_state = GAME_STATES[STATE_MAP["DOOR-PRESENT"]]
    
    return current_state

#function used to determine if a move was good based on present and future data
def good_move(data_before, data_after, current_state):
    scroll_x_before = data_before[0]
    x_before = data_before[1]
    scroll_y_before = data_before[2]
    y_before = data_before[3]
    health_before = data_before[4]
    kirby_lives_before = data_before[5]

    scroll_x_after = data_after[0]
    x_after = data_after[1]
    scroll_y_after = data_after[2]
    y_after = data_after[3]
    health_after = data_after[4]
    kirby_lives_after = data_after[5]

    conditions = [health_after == health_before, kirby_lives_after == kirby_lives_before,
                  scroll_x_after > 10, scroll_x_after < 152]

    if(current_state == "HORIZONTAL-RIGHT"):
        #going in the right direction is a good move, and standing in place is not a good move
        conditions.append(scroll_x_after > 68 and x_before != x_after)

    elif(current_state == "HORIZONTAL-LEFT"):
        #going in the left direction is a good move, and standing in place is not a good move
        conditions.append(scroll_x_after < 76 and x_before != x_after)
        
    elif(current_state == "VERTICAL-UP"):
        #going in the up direction is a good move, and standing in place is not a good move
        conditions.append(scroll_y_after < 84 and x_before != x_after) #y_before != y_after)
        
    elif(current_state == "VERTICAL-DOWN"):
        #going in the down direction is a good move, and standing in place is not a good move
        conditions.append(scroll_y_after > 76 and x_before != x_after) #y_before != y_after)
        
    elif(current_state == "BOSS"):
        #standing in place is a bad move
        conditions.append(x_before != x_after) #y_before != y_after)

    elif(current_state == "DOOR-PRESENT"):
        #standing in place is a bad move
        conditions.append(x_before != x_after)
        conditions.append(scroll_x_after > 68)
        

    return all(conditions)

#run the driver
main()
