import retro
from sklearn import linear_model
import random
import time
import tkinter as tk

'''
Name: Lucas Hasting
Date: 11/20/2024

Sources:
https://retro.readthedocs.io/en/latest/
https://github.com/openai/retro/releases/tag/f347d7e
https://www.geeksforgeeks.org/python-gui-tkinter/
https://stackoverflow.com/questions/6920302/how-to-pass-arguments-to-a-button-command-in-tkinter
https://stackoverflow.com/questions/110923/how-do-i-close-a-tkinter-window
'''

#set the frames per second
FPS = 60

#set the sleep time - used to ensure all data is read before making checking a good move
SLEEP_TIME = 1/4

#set the min and max allowed frame sizes for making random move sizes
MIN_MOVE_SIZE = 45
MAN_MOVE_SIZE = 90

#the starting game state
STATE_FILE = "begginning.state"

#used to determine how many wrong moves can be made until the
#state changes to the previous state
RESET_COUNT = 20

#create map of inputs to position in action array
INPUTS = {
    "A": 8,
    "B": 0,
    "UP": 4,
    "DOWN": 5,
    "LEFT": 6,
    "RIGHT": 7,
    "NULL": -1,
    "DOWN-LEFT": 1,
    "DOWN-RIGHT": 9,
    "UP-LEFT": 2,
    "UP-RIGHT": 3
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
    1: "DOWN-LEFT",
    9: "DOWN-RIGHT",
    2: "UP-LEFT",
    3: "UP-RIGHT"
}

#create list of states
GAME_STATES = ["UNKOWN",
               "HORIZONTAL-RIGHT",
               "HORIZONTAL-LEFT",
               "VERTICAL-UP",
               "VERTICAL-DOWN",
               "BOSS",
               "DOOR-PRESENT"]

#create map of states to state index
STATE_MAP = {
    "UNKOWN": 0,
    "HORIZONTAL-RIGHT": 1,
    "HORIZONTAL-LEFT": 2,
    "VERTICAL-UP": 3,
    "VERTICAL-DOWN": 4,
    "BOSS": 5,
    "DOOR-PRESENT": 6
}

#The main driver
def main():
    #display the main menu
    m = tk.Tk()
    main_menu(m)

#function used to display a main menu GUI
def main_menu(m):
    button_1 = tk.Button(m, text='AI - Create data (play the first screen)', width=50, command=lambda: three_file_gui(m, 'Play the game!', "Screen One"))
    button_1.pack()
    button_2 = tk.Button(m, text='AI - Create data (play the full game - not finished)', width=50, command=lambda: three_file_gui(m, 'Play the game!', "Full Game"))
    button_2.pack()
    button_3 = tk.Button(m, text='AI - Test Model (first screen only)', width=50, command=lambda: two_file_gui(m, 'Test the model!', "Test Model"))
    button_3.pack()
    button_4 = tk.Button(m, text='AI - Improve Model (first screen only)', width=50, command=lambda: three_file_gui(m, 'Play the game!', "I - Screen One"))
    button_4.pack()
    button_5 = tk.Button(m, text='Playback a recording', width=50, command=lambda: playback_gui(m))
    button_5.pack()
    button_6 = tk.Button(m, text='Quit', width=25, command=m.destroy)
    button_6.pack()
    m.mainloop()

#function used to display a GUI requesting two input files
def two_file_gui(m, message, t):
    incorrect_count = [0]
    m.destroy()
    m = tk.Tk()
    label_1 = tk.Label(m, text="Enter move type file: ")
    label_1.pack()
    text_1 = tk.Text(m, height=1, width=30)
    text_1.pack()
    label_2 = tk.Label(m, text="Enter move size file: ")
    label_2.pack()
    text_2 = tk.Text(m, height=1, width=30)
    text_2.pack()
    button = tk.Button(m, text=message, width=25, command=lambda: two_file_validate_gui(m, text_1, text_2, incorrect_count, t))
    button.pack()
    button_2 = tk.Button(m, text="Go Back", width=25, command=lambda: transition_main_menu(m))
    button_2.pack()
    m.mainloop()

#function used to validate a GUI requesting two input files
def two_file_validate_gui(m, text_1, text_2, incorrect_count, t):
    if((text_1.get("1.0") == "\n" or text_2.get("1.0") == "\n") and incorrect_count[0] == 0):
        label = tk.Label(m, text="Please enter a file name!")
        label.pack()
        incorrect_count[0] += 1
    elif (text_1.get("1.0") != "\n" and text_2.get("1.0") != "\n"):
        game_driver(m, text_1.get("1.0", "end-1c").strip(), text_2.get("1.0", "end-1c").strip(), "", True, True)

#function used to display a GUI requesting three input files
def three_file_gui(m, message, t):
    incorrect_count = [0]
    m.destroy()
    m = tk.Tk()
    label_1 = tk.Label(m, text="Enter move type file: ")
    label_1.pack()
    text_1 = tk.Text(m, height=1, width=30)
    text_1.pack()
    label_2 = tk.Label(m, text="Enter move size file: ")
    label_2.pack()
    text_2 = tk.Text(m, height=1, width=30)
    text_2.pack()
    label_3 = tk.Label(m, text="Enter recording file: ")
    label_3.pack()
    text_3 = tk.Text(m, height=1, width=30)
    text_3.pack()
    button = tk.Button(m, text=message, width=25, command=lambda: three_file_validate_gui(m, text_1, text_2, text_3, incorrect_count, t))
    button.pack()
    button_2 = tk.Button(m, text="Go Back", width=25, command=lambda: transition_main_menu(m))
    button_2.pack()
    m.mainloop()

#function used to validate a GUI requesting three input files
def three_file_validate_gui(m, text_1, text_2, text_3, incorrect_count, t):
    if((text_1.get("1.0") == "\n" or text_2.get("1.0") == "\n" or text_3.get("1.0") == "\n") and incorrect_count[0] == 0):
        label = tk.Label(m, text="Please enter a file name that exists!")
        label.pack()
        incorrect_count[0] += 1
    elif (text_1.get("1.0") != "\n" and text_2.get("1.0") != "\n"):
        if(t=="Full Game"):
            game_driver(m)
        if(t=="Screen One"):
            game_driver(m, text_1.get("1.0", "end-1c").strip(), text_2.get("1.0", "end-1c").strip(), text_3.get("1.0", "end-1c").strip(), True)
        elif(t=="Test Model"):
            game_driver(m, text_1.get("1.0", "end-1c").strip(), text_2.get("1.0", "end-1c").strip(), text_3.get("1.0", "end-1c").strip(), True, True)
        elif(t=="I - Screen One"):
            game_driver(m, text_1.get("1.0", "end-1c").strip(), text_2.get("1.0", "end-1c").strip(), text_3.get("1.0", "end-1c").strip(), True, False, True)

#function used to display a GUI requesting one input file - used to playback a recording
def playback_gui(m):
    incorrect_count = [0]
    m.destroy()
    m = tk.Tk()
    label = tk.Label(m, text="Enter recording file: ")
    label.pack()
    text = tk.Text(m, height=1, width=30)
    text.pack()
    button = tk.Button(m, text='Watch the game!', width=25, command=lambda: playback_gui_validate(m, text, incorrect_count))
    button.pack()
    button_2 = tk.Button(m, text="Go Back", width=25, command=lambda: transition_main_menu(m))
    button_2.pack()
    m.mainloop()

#function used to validate a GUI requesting one input file - used to playback a recording
def playback_gui_validate(m, text, incorrect_count):
    if(text.get("1.0") == "\n" and incorrect_count[0] == 0):
        label = tk.Label(m, text="Please enter a file name!")
        label.pack()
        incorrect_count[0] += 1
    elif (text.get("1.0") != "\n"):
        playback_driver(m, text.get("1.0", "end-1c").strip())

#function used to display a GUI which displays the accuracy of the model
def result_gui(m, incorrect, total):
    m.destroy()
    m = tk.Tk()
    label = tk.Label(m, text=f"{(((total - incorrect) / total) * 100):.2f}% accurate")
    label.pack()
    button = tk.Button(m, text='Return to main menu', width=25, command=lambda: transition_main_menu(m))
    button.pack()
    m.mainloop()

#function used to transistion to the main menu GUI
def transition_main_menu(m):
    m.destroy()
    m = tk.Tk()
    main_menu(m)

#function used to get data from a file
def get_data_from_file(file, total_data=False):
    data = []
    
    for line in file:
        line = line.split(",")

        length = len(line)

        #if total data, adjust the length of the line (account for move itself)
        if(total_data):
            length = len(line) - 1
        
        for j in range(length):
            line[j] = int(line[j])
        data.append(line[:length])

    file.close()

    return data

#function used to write the data to the data files
def write_data_file(file_1, file_2, file_3, data1, data2, data3, improve_model, moves_size, recoring_file_name):
    #write the data to the data files
    all_length = len(data1)
    for i in range(all_length):
        for j in range(len(data1[0])):
            file_1.write(str(data1[i][j]) + ",")

        file_1.write(str(data2[i]) + "\n")
        file_2.write(str(data2[i]) + ",")
        file_2.write(str(data3[i]) + "\n")
        if(not improve_model):
            file_3.write(str(data2[i]) + ",")
            file_3.write(str(int(data3[i])) + "\n")

    #if the model is improved, save only the new moves made to the recording
    if(improve_model):
        moves = data2[moves_size:]
        move_frames = data3[moves_size:]
        for i in range(len(moves)):
            file_3.write(str(moves[i]) + ",")
            file_3.write(str(int(move_frames[i])) + "\n")

    file_1.close()
    file_2.close()
    file_3.close()

    #compress the recording file
    compress_recording_file(recoring_file_name)

#function used to playback a recording (the playback driver)
def playback_driver(m, text):
    m.destroy()

    #read in data from recording
    file = open("./data/recordings/"+text, "r")
    move_data = get_data_from_file(file)
    moves = [x for x in (move[0] for move in move_data)]
    move_frames = [x for x in (move[1] for move in move_data)]
    file.close()

    #start gym retro enviornment
    env = retro.make('KirbysDreamLand-GB', STATE_FILE)
    env.reset()

    #loop for every move
    while(len(move_frames) != 0):
        
        #render the game
        new_render(env)

        #get move size and move type
        move_size = move_frames[0]
        action = INVERSE_INPUTS[moves[0]]

        #perform the move
        for i in range(move_size):
            new_render(env)
            ob, rew, done, info = env.step(make_action(action))

        #remove moves from the pipe
        move_frames.pop(0)
        moves.pop(0)

    #close the gym retro enviornment
    env.render(close=True)
    env.close()

    #go to the main menun
    m = tk.Tk()
    main_menu(m)

#function used for all other drivers
def game_driver(m, text_1 = "", text_2 = "", text_3 = "", screen_one=False, test_model=False, improve_model=False):
    m.destroy()

    #initilize variables
    current_state = GAME_STATES[0]
    data_file = 0
    move_file = 0
    recording_file = 0
    incorrect = [0]
    
    #create the gym retro enviornment
    env = retro.make('KirbysDreamLand-GB', STATE_FILE)
    env.reset()

    #initilize default values
    total_data = []
    moves = []
    move_sizes = []

    model = 0
    move_size_model = 0

    #get data if test_model or improve_mode
    if(test_model or improve_model):
        data_file = open("./data/move_type_models/"+text_1, "r")
        move_file = open("./data/move_size_models/"+text_2, "r")
        total_data = get_data_from_file(data_file, True)
        move_data = get_data_from_file(move_file)
        moves = [x for x in (move[0] for move in move_data)]
        move_sizes = [x for x in (move[1] for move in move_data)]
        model = update_model(total_data, moves)
        move_size_model = update_move_size_model(moves, move_sizes)
        data_file.close()
        move_file.close()

    #if first screen only, open data file for writing
    if((screen_one or improve_model) and not (test_model)):
        data_file = open("./data/move_type_models/"+text_1, "w")
        move_file = open("./data/move_size_models/"+text_2, "w")
        recording_file = open("./data/recordings/"+text_3, "w")

    #get move size (used for improve_model)
    moves_size = len(moves)

    #get the starting state
    state = [env.em.get_state()]
        
    #play the game
    while(True):
        
        #render the game
        new_render(env)

        #have kirby do nothing to get screen info
        ob, rew, done, info = env.step(make_action("NULL"))

        #if a state of 6 is reached, end the game, the first screen has been reached
        if(screen_one and info["game_state"] == 6):
            break

        #get the current state and its data
        before = load_data(info, STATE_MAP[current_state])

        #if a model has not been created
        if(model == 0 or current_state == "UNKOWN"):
            #get the current state and make a random move until it is good
            if(test_model):
                model, move_size_model, current_state = make_move(info, model, total_data, moves, state, env, move_size_model, move_sizes, before, current_state, True, incorrect, True)
            else:
                model, move_size_model, current_state = make_move(info, model, total_data, moves, state, env, move_size_model, move_sizes, before, current_state, True)
        else:
            #make a good move if the model is created
            if(not test_model):
                model, move_size_model, current_state = make_move(info, model, total_data, moves, state, env, move_size_model, move_sizes, before, current_state)  
            else:
                model, move_size_model, current_state = make_move(info, model, total_data, moves, state, env, move_size_model, move_sizes, before, current_state, False, incorrect, True)

    #update data if the model was not being tested
    if(not test_model):
        write_data_file(data_file, move_file, recording_file, total_data, moves, move_sizes, improve_model, moves_size, text_3)

    #close the gym retro enviornment
    env.render(close=True)
    env.close()

    #go to the next GUI
    m = tk.Tk()
    if(test_model):
        result_gui(m, incorrect[0], len(total_data))
    else:
        main_menu(m)

#function used to compress a recording file (combines adjacent frame sizes)
def compress_recording_file(text):
    #get the data from the recording file
    file = open("./data/recordings/"+text, "r")
    move_data = get_data_from_file(file)
    moves = [x for x in (move[0] for move in move_data)]
    move_frames = [x for x in (move[1] for move in move_data)]
    file.close()

    #get size and starting index
    size = len(moves) - 1
    i = 0

    #loop through every frame option, if the adjacent frames are the same, combine frame sizes and adjust pipe arrays
    while (i < size - 1):
        if(moves[i] == moves[i+1]):
            move_frames[i] += move_frames[i + 1]
            move_frames.pop(i + 1)
            moves.pop(i + 1)
            size -= 1
        else:
            i += 1

    #save the results in the recording file
    file = open("./data/recordings/"+text, "w")
    for i in range(len(moves)):
            file.write(str(moves[i]) + ",")
            file.write(str(move_frames[i]) + "\n")
    file.close()
    
#function is a new renderer that uses the FPS to determine speed
def new_render(env):
    time.sleep(1/FPS)
    env.render()

#function used to make an action (player input)
def make_action(enter):
    action = [0] * 9
    if(INPUTS[enter] == 1):
        action[5] = 1
        action[6] = 1
    elif(INPUTS[enter] == 2):
        action[4] = 1
        action[6] = 1
    elif(INPUTS[enter] == 3):
        action[4] = 1
        action[7] = 1
    elif(INPUTS[enter] == 9):
        action[5] = 1
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

#function used perform a move
def make_movement(action, env, move_size_model, state, random_move=False):

    #predict move size, or get random move size
    if(random_move):
        move_size = random.randrange(MIN_MOVE_SIZE, MAN_MOVE_SIZE)
    else:
        move_size = move_size_model.predict([[INPUTS[action]]])
        move_size = round(move_size[0])

    #load the state before moving
    env.em.set_state(state[len(state) - 1])

    #perform the move for move_size frames
    for i in range(move_size):
        new_render(env)
        ob, rew, done, info = env.step(make_action(action))

    #return info needed from making an action
    return ob, rew, done, info, move_size

#function used to make a move
def make_move(info, model, total_data, moves, state, env, move_size_model, move_sizes, before, current_state, random_move = False, incorrect=[0], test_model=False, count=0):
    #if the AI is stuck, revert to previous state
    if(count == RESET_COUNT):
        pop_data(total_data, moves, move_sizes, state, test_model)
        count = 0

        #update the models accordingly
        if(not test_model):
            model = update_model(total_data, moves)
            move_size_model = update_move_size_model(moves, move_sizes)

    #give variables default values that will change later
    ob, rew, done, info, move_size = 0,0,0,0,0

    #decide what move to make (random or predicted)
    if(random_move):
        move = random.randrange(0, 10)
        while(current_state == "HORIZONTAL-RIGHT" and "LEFT" in INVERSE_INPUTS[move]):
            move = random.randrange(0, 10)
    else:
        move = model.predict([before])
        move = move[0]

    #make a move (random or predicted)
    if(random_move):
        ob, rew, done, info, move_size = make_movement(INVERSE_INPUTS[move], env, 0, state, True)
    else:
        ob, rew, done, info, move_size = make_movement(INVERSE_INPUTS[move], env, move_size_model, state)

    #allow time for the data to be gathered (such as being hit)
    time.sleep(SLEEP_TIME)

    #load data after the move was made
    after = load_data(info, STATE_MAP[current_state])

    #check game state and display the current state along with the predicted move
    current_state = determine_game_state([before[-2], before[-3], before[-7], before[-8]], current_state)
    if(random_move):
        print(INVERSE_INPUTS[move], move_size, current_state, count)
    else:
        print("Predicted: ", INVERSE_INPUTS[move], move_size, current_state)

    #determine if the move was good, if so, update the model. Otherwise, try a random move until a good move occurs
    if(good_move([before[-2], before[-1], before[-3], before[-4], before[-5], before[-6]], [after[-2], after[-1], after[-3], after[-4], after[-5], before[-6]], current_state)):
        state.append(env.em.get_state())
        #if a model is not being tested, update the current models
        if(not test_model):
           add_to_data(total_data, after, moves, move, move_sizes, move_size)
           model = update_model(total_data, moves)
           move_size_model = update_move_size_model(moves, move_sizes)
    else:
        #if the move was bad and not random, the prediction was wrong (increase incorrect prediction count)
        if(not random_move):
            incorrect[0] += 1
        #try a random move
        return make_move(info, model, total_data, moves, state, env, move_size_model, move_sizes, before, current_state, True, incorrect, test_model, count + 1)

    #return both models to be updated in the driver, along with the current state
    return model, move_size_model, current_state

#add data to lists to be used in an updated model
def add_to_data(total_data, new_data, moves, move, move_sizes, move_size):
    total_data.append(new_data)
    moves.append(move)
    move_sizes.append(move_size)

#function used to remove data if a game state is stuck
def pop_data(total_data, moves, move_sizes, state, test_model):
    if(not test_model):
        total_data.pop(len(total_data) - 1)
        moves.pop(len(moves) - 1)
        move_sizes.pop(len(move_sizes) - 1)
    state.pop(len(state) - 1)
    
#update the move prediciton model
def update_model(total_data, moves):
    #do not create a model if not enough data exists
    if(len(list(set(moves))) < 2):
        return 0

    #make the move type classification model
    model = linear_model.LogisticRegression(solver='liblinear', C=1)
    model.fit(total_data, moves)

    #return the model
    return model

#update the move size prediciton model
def update_move_size_model(moves, move_sizes):
    #do not create a model if not enough data exists
    if(len(list(set(moves))) < 2):
        return 0

    #make the move size regression model
    move_size_model = linear_model.LinearRegression()
    temp_moves = [[i] for i in moves]
    move_size_model.fit(temp_moves, move_sizes)

    #return the model
    return move_size_model

def determine_game_state(data_after, current_state):
    #put the data into more meaningfull variables
    scroll_x = data_after[0]
    scroll_y = data_after[1]
    boss_health = data_after[2]
    game_state = data_after[3]

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
        elif (current_state == "BOSS" and boss_health == 0):
            current_state = GAME_STATES[STATE_MAP["UNKOWN"]]
        elif (boss_health != 0):
            current_state = GAME_STATES[STATE_MAP["BOSS"]]

        conditions = [False]

    #set door present
    if(current_state != "UNKOWN"):
        if (((scroll_x > 76 or scroll_x < 68) and "HORIZONTAL" in current_state) or
            ((scroll_y > 84, scroll_y < 76) and "VERTICAL" in current_state)):
            current_state = GAME_STATES[STATE_MAP["DOOR-PRESENT"]]
    
    return current_state

#function used to determine if a move was good based on present and future data
def good_move(data_before, data_after, current_state):
    #put the data into more meaningfull variables
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

    #conditions for all states
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
        
    #return true if all conditions for the state are true (it is a good move)
    return all(conditions)

#run the driver
main()
