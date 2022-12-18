import os,sys,time,random,pygame,copy
import torch
import numpy as np
import heapq as hq
from collections import deque

from snake_env import Parameters,Snake_Env,State
from snake_rander import Snake_Rander
from snake_nn import Snake_NN


# For the NN training_data
def generate_training_data():
    data_list = []
    for i in range(1000):
        print(i)
        p = Parameters()
        snake_ai = Snake_Env(p)
        snake_ai.state.print_state()
        action_list = snake_ai.a_start_search(snake_ai.state)
        if len(action_list)==1:
            continue
        print('done')
        for action in action_list[1:]:
            data = snake_ai.state.one_hot_encoding()
            data_list.append([data,action])
            snake_ai.state = snake_ai.step(snake_ai.state,action)
    np.save('training_data.npy',np.array(data_list,dtype=object))

def NN_play():
    snake_nn = Snake_NN()
    snake_nn.load()

    p = Parameters()
    snake_rander = Snake_Rander(p,2)
    snake_ai = Snake_Env(p)
    snake_rander.game_render(snake_ai.state)
    input()
    over = False
    action = ['UP','DOWN','LEFT','RIGHT']
    while True:
        snake_ai.state.print_state()

        data = torch.from_numpy(snake_ai.state.one_hot_encoding())
        data = data.to(torch.float32)

        pre = snake_nn(data)
        index = pre.argmax(0)
        direction = action[index]

        print('next action: %s'%direction)

        #input()

        snake_ai.state = snake_ai.step(snake_ai.state,direction)
        snake_rander.game_render(snake_ai.state)

        if snake_ai.state.over:
            break

def wait_for_end():
    print('Press x to exit')
    key = input()
    while key !='x':
        print('Press x to exit')
        key = input()

def play_with_baseline_ai():
    p = Parameters()
    snake_rander = Snake_Rander(p)
    snake_ai = Snake_Env(p)
    snake_human = Snake_Env(p)
    snake_rander.game_render(snake_ai.state,snake_human.state)
    input()
    over_1 = False
    over_2 = False
    while True:
        if not over_1:
            over_1 = snake_ai.baseline_ai()
            snake_rander.game_render(snake_ai.state,snake_human.state)
        if not over_2:
            over_2 = snake_human.human_play()
            snake_rander.game_render(snake_ai.state,snake_human.state)
        if over_1 and over_2:
            break
    wait_for_end()

def play_a_star_ai():
    p = Parameters()
    snake_rander = Snake_Rander(p,2)
    snake_ai = Snake_Env(p)
    snake_rander.game_render(snake_ai.state)
    snake_ai.state.print_state()
    action_list = snake_ai.a_start_search(snake_ai.state)
    print('done')
    print(action_list)
    input()
    for action in action_list[1:]:
        snake_ai.state = snake_ai.step(snake_ai.state,action)
        snake_rander.game_render(snake_ai.state)

    wait_for_end()

def play_bfs_ai():
    p = Parameters()
    snake_rander = Snake_Rander(p,2)
    snake_ai = Snake_Env(p)
    snake_rander.game_render(snake_ai.state)
    snake_ai.state.print_state()
    action_list = snake_ai.breadth_first_search(snake_ai.state)
    print('done')
    print(action_list)
    input()
    for action in action_list[1:]:
        snake_ai.state = snake_ai.step(snake_ai.state,action)
        snake_rander.game_render(snake_ai.state)

    wait_for_end()

if __name__ == '__main__':
    #play_with_baseline_ai()
    play_a_star_ai()
    #play_bfs_ai()
