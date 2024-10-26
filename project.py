import retro
import numpy as np
from sklearn import linear_model
import random
import time

#set the frames per second
FPS = 60
SLEEP_TIME = 1/4

#create map of inputs to position in action array
INPUTS = {
    "A": 8,
    "B": 0,
    "UP": 4,
    "DOWN": 5,
    "LEFT": 6,
    "RIGHT": 7,
    "NULL": 0
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
    0: "NULL"
}

#function is a renderer that uses the FPS to determine speed
def new_render(env):
    time.sleep(1/FPS)
    env.render()

#main driver
def main():
    #create the enviornment
    env = retro.make('KirbysDreamLand-GameBoy', 'begginning.state')
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

        #get the current state and its data
        state = env.em.get_state()
        before = load_data(info)

        #if a model has not been created
        if(model == 0):
            #get the current state and make a random move until it is good
            model, move_size_model = make_random_move(info, model, total_data, moves, state, env, move_size_model, move_sizes, before)
        else:
            #make a good move if the model is created
            model, move_size_model = make_move(info, model, total_data, moves, state, env, move_size_model, move_sizes, before)

#function used to make an action (player input)
def make_action(enter):
    action = [0] * 9
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
def load_data(info):
    screen_data = load_screen_data(info)
    kirby_health = info["kirby_health"]
    kirby_life = info["kirby_life"]
    boss_health = info["boss_health"]
    kirby_x_scrol = info["kirby_x_scrol"]
    kirby_x = info["kirby_x"]

    return [*screen_data, boss_health, kirby_life, kirby_health, kirby_x_scrol, kirby_x]

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
    move_size = random.randrange(30, 75)

    #perform the move for move_size frames
    for i in range(move_size):
        new_render(env)
        ob, rew, done, info = env.step(make_action(action))

    #return info needed from making an action
    return ob, rew, done, info, move_size

#function used to make a predicted move
def make_move(info, model, total_data, moves, state, env, move_size_model, move_sizes, before):

    #predict what move should be made 
    move = model.predict([before])
    move = move[0]

    #try the move
    ob, rew, done, info, move_size = make_movement(INVERSE_INPUTS[move], env, move_size_model)
    time.sleep(SLEEP_TIME)
    print("Predicted: ", INVERSE_INPUTS[move], move_size)

    #load data after the move was made
    after = load_data(info)

    #determine if the move was good, if so, update the model. Otherwise, try a random move until a good move occurs
    if(good_move([before[-1], before[-2], before[-3], before[-4], before[-5]], [after[-1], after[-2], after[-3], after[-4], after[-5]])):
       add_to_data(total_data, after, moves, move, move_sizes, move_size)
       model = update_model(total_data, moves)
       move_size_model = update_move_size_model(moves, move_sizes)
    else:
        return make_random_move(info, model, total_data, moves, state, env, move_size_model, move_sizes, before)

    #return both models to be updated in the driver
    return model, move_size_model

#function used to make a random move
def make_random_move(info, model, total_data, moves, state, env, move_size_model, move_sizes, before):
    #load the previous state
    env.em.set_state(state)

    #make a random move
    move = INVERSE_INPUTS[random.randrange(4, 9) % 9]

    #try the move
    ob, rew, done, info, move_size = make_random_movement(move, env)
    time.sleep(SLEEP_TIME)
    print(move, move_size)

    #load data after the move was made
    after = load_data(info)

    #determine if the move was good, if so, update the model. Otherwise, try again 
    if(good_move([before[-1], before[-2], before[-3], before[-4], before[-5]], [after[-1], after[-2], after[-3], after[-4], after[-5]])):
       add_to_data(total_data, after, moves, INPUTS[move], move_sizes, move_size)
       model = update_model(total_data, moves)
       move_size_model = update_move_size_model(moves, move_sizes)
    else:
        #use recursion to try again
        return make_random_move(info, model, total_data, moves, state, env, move_size_model, move_sizes, before)

    #return both models to be updated in the driver
    return model, move_size_model

#function used to determine if a move was good based on present and future data
def good_move(data_before, data_after):
    #print(data_before[1], data_after[1])
    #print(data_before[0], data_after[0])

    if(data_after[4] == 0):
        cond2 = data_after[1] > 68 and data_before[0] != data_after[0]
    else:
        cond2 = True

    cond1 = data_before[2] == data_after[2] and data_before[3] == data_after[3]

    #data[0] xpos, data[1] xscrol, data[4] boss health
    return cond1 and cond2

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

#run the driver
main()
