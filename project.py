import retro
import numpy as np
from sklearn import linear_model
import random
import time

'''
next:

1. create regression model that predicts move size
2. combat pits
3. combat bosses
4. shootem up levels
5. going in doors

'''

FPS = 60

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

INVERSE_INPUTS = {
    8: "A",
    0: "B",
    4: "UP",
    5: "DOWN",
    6: "LEFT",
    7: "RIGHT",
    0: "NULL"
}

def new_render(env):
    time.sleep(1/FPS)
    env.render()

def main():
    env = retro.make('KirbysDreamLand-GameBoy', 'begginning.state')
    env.reset()
    new_render(env)

    total_data = []
    moves = []

    model = 0
    
    #play the game
    while(True):
        time.sleep(1/FPS)
        env.render()
        ob, rew, done, info = make_movement("NULL", env)
        if(model == 0):
            state = env.em.get_state()
            model = make_random_move(info, model, total_data, moves, state, env)
        else:
            make_move(info, model, total_data, moves, env)

def make_action(enter):
    action = [0] * 9
    action[INPUTS[enter]] = 1
    return action

def load_screen_data(info):
    data = []
    for i in range(40):
        for j in range(4):
            data.append(info[f"screen{i+1}_{j}"])
    return data

def load_data(info):
    screen_data = load_screen_data(info)
    kirby_health = info["kirby_health"]
    kirby_life = info["kirby_life"]
    boss_health = info["boss_health"]
    kirby_x_scrol = info["kirby_x_scrol"]
    kirby_x = info["kirby_x"]

    return [*screen_data, boss_health, kirby_life, kirby_health, kirby_x_scrol, kirby_x]
    
def make_movement(action, env):
    for i in range(random.randrange(30, 75)):
        new_render(env)
        ob, rew, done, info = env.step(make_action(action))
    return ob, rew, done, info

def make_move(info, model, total_data, moves, env):
    state = env.em.get_state()
    before = load_data(info)
    move = model.predict([before])
    move = move[0]
    print("Predicted: ", INVERSE_INPUTS[move])
    make_movement(INVERSE_INPUTS[move], env)
    ob, rew, done, info = make_movement(INVERSE_INPUTS[move], env)
    time.sleep(1/15)
    after = load_data(info)

    if(good_move([before[-1], before[-2], before[-3], before[-4], before[-5]], [after[-1], after[-2], after[-3], after[-4], after[-5]])):
       add_to_data(total_data, after, moves, move)
       model = update_model(total_data, moves)
    else:
        make_random_move(info, model, total_data, moves, state, env)
    return model

def make_random_move(info, model, total_data, moves, state, env):
    env.em.set_state(state)
    before = load_data(info)
    move = INVERSE_INPUTS[random.randrange(4, 9) % 9]
    print(move)
    ob, rew, done, info = make_movement(move, env)
    time.sleep(1/15)
    after = load_data(info)

    if(good_move([before[-1], before[-2], before[-3], before[-4], before[-5]], [after[-1], after[-2], after[-3], after[-4], after[-5]])):
       add_to_data(total_data, after, moves, INPUTS[move])
       model = update_model(total_data, moves)
    else:
        return make_random_move(info, model, total_data, moves, state, env)
    return model
    
def good_move(data_before, data_after):
    print(data_before[1], data_after[1])
    print(data_before[0], data_after[0])

    if(data_after[4] == 0):
        cond2 = data_after[1] > 68 and data_before[0] != data_after[0]
    else:
        cond2 = True

    cond1 = data_before[2] == data_after[2] and data_before[3] == data_after[3]

    #data[0] xpos, data[1] xscrol, data[4] boss health
    return cond1 and cond2
    
def add_to_data(total_data, new_data, moves, move):
    total_data.append(new_data)
    moves.append(move)

def update_model(total_data, moves):
    if(len(list(set(moves))) < 2):
        return 0
    model = linear_model.LogisticRegression(solver='liblinear', C=1)
    model.fit(total_data, moves)
    return model

main()
