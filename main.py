import os,sys,time,random,pygame,copy
import torch
import numpy as np
import heapq as hq
from collections import deque

from snake_env import Snake_Env,State
from snake_rander import Snake_Rander
from snake_nn import Snake_NN

class Parameters:
    def __init__(self):
        self.game_size = 10
        self.fruit_size = int(self.game_size*self.game_size/4)
        self.fruit_number = [np.random.randint(1,self.fruit_size),np.random.randint(1,self.fruit_size)]
        #self.fruit_number = [4,2]
        self.round = 1

        self.snake_position = [np.random.randint(self.game_size), np.random.randint(self.game_size)]
        self.direction = 'RIGHT'
        self.random = False

        self.generate_fruit()

    def generate_fruit(self):
        self.fruit_list = []
        for i in range(self.round):
            self.fruit_position_good = []
            self.fruit_position_bad = []

            for i in range(self.fruit_number[0]):
                tmp = [np.random.randint(1, self.game_size),np.random.randint(1, self.game_size)]
                while tmp in self.fruit_position_good or tmp in self.fruit_position_bad or tmp == self.snake_position:
                    tmp = [np.random.randint(1, self.game_size),np.random.randint(1, self.game_size)]
                self.fruit_position_good.append(tmp)

            for i in range(self.fruit_number[1]):
                tmp = [np.random.randint(1, self.game_size),np.random.randint(1, self.game_size)]
                while tmp in self.fruit_position_good or tmp in self.fruit_position_bad or tmp == self.snake_position:
                    tmp = [np.random.randint(1, self.game_size),np.random.randint(1, self.game_size)]
                self.fruit_position_bad.append(tmp)
            self.fruit_list.append([self.fruit_position_good,self.fruit_position_bad])
        #self.fruit_list=[[[[1, 1]], []]]


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
    snake_nn.load('checkpoint_79')

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
        data = data[None,]

        pre = snake_nn(data)
        pre = pre[0]
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
    action_list,node_count = snake_ai.a_start_search(snake_ai.state)
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
    action_list,node_count = snake_ai.breadth_first_search(snake_ai.state)
    print('done')
    print(action_list)
    input()
    for action in action_list[1:]:
        snake_ai.state = snake_ai.step(snake_ai.state,action)
        snake_rander.game_render(snake_ai.state)

    wait_for_end()

def baseline_ai_vs_a_star_experment():
    baseline_ai_score = []
    a_star_score = []
    a_star_node = []
    for i in range(100):
        print(i)
        p = Parameters()
        baseline_ai = Snake_Env(p)
        a_star_ai = Snake_Env(p)
        action_list,node_count = a_star_ai.a_start_search(a_star_ai.state)
        a_star_node.append(node_count)

        step = 0

        while(not baseline_ai.state.over):
            step+=1
            direction = baseline_ai.simple_heuristic(baseline_ai.state)
            baseline_ai.state = baseline_ai.step(baseline_ai.state,direction)
            if step>1000:
                break
        baseline_ai_score.append(baseline_ai.state.score)

        for action in action_list[1:]:
            a_star_ai.state = a_star_ai.step(a_star_ai.state,action)
        a_star_score.append(a_star_ai.state.score)
    print('baseline_ai_score')
    print(baseline_ai_score)
    print('a_star_score')
    print(a_star_score)
    print('a_star_node')
    print(a_star_node)



if __name__ == '__main__':
    play_with_baseline_ai()
    #play_bfs_ai()
    #play_a_star_ai()
    #NN_play()
    #baseline_ai_vs_a_star_experment()
