import os,sys,time,random,pygame,copy
import torch
import numpy as np
import heapq as hq
from collections import deque

from snake_rander import Snake_Rander
from snake_nn import Snake_NN

class Parameters:
    def __init__(self):
        self.game_size = 10
        self.fruit_number = [np.random.randint(1,4),np.random.randint(1,4)]
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

class State:
    def __init__(self,p):
        self.game_size = p.game_size
        self.snake_position = copy.deepcopy(p.snake_position)
        self.snake_body = [copy.deepcopy(p.snake_position)]
        self.fruit_position_good = []
        self.fruit_position_bad = []
        self.action_list = []
        self.score = 0
        self.direction = copy.deepcopy(p.direction)
        self.update_valid_actions()
        self.over = False
        self.round_count = 0
        self.step_count = 0
        self.pack_board()


    def __eq__(self,other):
        #(self.board == other.board).all()
        return True if self.direction==other.direction and len(self.snake_body)==len(other.snake_body)\
        and self.snake_position == other.snake_position else False

    def pack_board(self):
        self.board = np.zeros((self.game_size,self.game_size))

        for i in range(len(self.fruit_position_good)):
            self.board[self.fruit_position_good[i][0],self.fruit_position_good[i][1]] = 2*self.game_size
        for i in range(len(self.fruit_position_bad)):
            self.board[self.fruit_position_bad[i][0],self.fruit_position_bad[i][1]] = -2*self.game_size

        for i in self.snake_body:
            if not self.out_of_board(i):
                self.board[i[0],i[1]] = 1
        if not self.out_of_board(self.snake_position):
            self.board[self.snake_position[0],self.snake_position[1]] = 2

    def one_hot_encoding(self):
        data = np.zeros((4,self.game_size,self.game_size))
        for i in range(self.game_size):
            for j in range(self.game_size):
                if self.board[i][j] == 1:
                    data[1][i][j] = 1
                elif self.board[i][j] == 2:
                    data[0][i][j] = 1
                elif self.board[i][j] == 2*self.game_size:
                    data[2][i][j] = 1
                elif self.board[i][j] == -2*self.game_size:
                    data[3][i][j] = 1
        return data

    def update_valid_actions(self):
        self.valid_actions = ['UP','DOWN','LEFT','RIGHT']
        if self.direction == 'UP':
            self.valid_actions.remove('DOWN')
        elif self.direction == 'DOWN':
            self.valid_actions.remove('UP')
        elif self.direction == 'RIGHT':
            self.valid_actions.remove('LEFT')
        elif self.direction == 'LEFT':
            self.valid_actions.remove('RIGHT')
        self.action_list.append(self.direction)

    def round_end(self):
        return True if len(self.fruit_position_good) == 0 else False

    def round_fail(self):
        return True if len(self.fruit_position_bad) == 0 else False

    def out_of_board(self,point):
        return True if point[0] < 0 or point[0] > self.game_size-1 or point[1] < 0 or point[1] > self.game_size-1 else False

    def print_state(self):
        print('current state:')
        print(self.board.T.astype(np.int32))
        print('current score: %d'%self.score)
        print('current direction: %s'%self.direction)
        print('valid_actions:')
        print(self.valid_actions)

class Snake_Env:
    def __init__(self,p):
        self.p = p
        self.game_size = p.game_size
        self.fruit_number = p.fruit_number
        self.round = p.round

        self.state = State(p)

        self.generate_fruit(self.state)

    def unpack_board(self,board):
        fruit_position_good = []
        fruit_position_bad = []
        snake_body = []
        snake_position = None
        for i in range(self.game_size):
            for j in range(self.game_size):
                if board[i][j] == 1:
                    snake_body.append([i,j])
                elif board[i][j] == 2:
                    snake_body.append([i,j])
                    snake_position = [i,j]
                elif board[i][j] == 2*self.game_size:
                    fruit_position_good.append([i,j])
                elif board[i][j] == -2*self.game_size:
                    fruit_position_bad.append([i,j])
        return snake_position,snake_body,fruit_position_good,fruit_position_bad

    def out_of_board(self,point):
        return True if point[0] < 0 or point[0] > self.game_size-1 or point[1] < 0 or point[1] > self.game_size-1 else False

    def generate_fruit(self,state):
        if self.p.random:
            state.fruit_position_good = []
            state.fruit_position_bad = []

            for i in range(self.fruit_number[0]):
                tmp = [np.random.randint(1, self.game_size),np.random.randint(1, self.game_size)]
                while tmp in state.fruit_position_good or tmp in state.fruit_position_bad or tmp in state.snake_body:
                    tmp = [np.random.randint(1, self.game_size),np.random.randint(1, self.game_size)]
                state.fruit_position_good.append(tmp)

            for i in range(self.fruit_number[1]):
                tmp = [np.random.randint(1, self.game_size),np.random.randint(1, self.game_size)]
                while tmp in state.fruit_position_good or tmp in state.fruit_position_bad or tmp in state.snake_body:
                    tmp = [np.random.randint(1, self.game_size),np.random.randint(1, self.game_size)]
                state.fruit_position_bad.append(tmp)
        else:
            state.fruit_position_good = copy.deepcopy(self.p.fruit_list[self.state.round_count][0])
            state.fruit_position_bad = copy.deepcopy(self.p.fruit_list[self.state.round_count][1])

        state.pack_board()
        self.state.round_count += 1

    # check game over function
    def check_game_over(self,state):
        over=False

        if self.out_of_board(state.snake_position):
            #print(1)
            over=True

        for block in state.snake_body[1:]:
            if state.snake_position[0] == block[0] and state.snake_position[1] == block[1]:
                #print(2)
                over=True

        if len(state.snake_body)==0:
            #print(3)
            over =True

        if state.round_count == self.round and (len(state.fruit_position_good)==0 or len(state.fruit_position_bad)==0):
            #print(4)
            over=True

        state.over = over

    def move_tf(self,direction):
        changeto_list = ['UP','DOWN','LEFT','RIGHT']
        dx_list = [0,0,-1,1]
        dy_list = [-1,1,0,0]
        for i in range(4):
            if direction == changeto_list[i]:
                return dx_list[i],dy_list[i]

    def keyboard_input(self):
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    return 'UP'
                if event.key == pygame.K_DOWN:
                    return 'DOWN'
                if event.key == pygame.K_LEFT:
                    return 'LEFT'
                if event.key == pygame.K_RIGHT:
                    return 'RIGHT'


    def step(self,state,change_to):

        def snake_control(state,direction):
            change_to = direction if direction!=None else self.keyboard_input()
            if change_to in state.valid_actions:
                state.direction = change_to

            dx,dy = self.move_tf(direction)
            state.snake_position[0] += dx
            state.snake_position[1] += dy

            state.update_valid_actions()

        def get_good_fruit(state):
            yes = False
            remove_list = []
            for i in range(len(state.fruit_position_good)):
                if state.snake_position[0] == state.fruit_position_good[i][0] and state.snake_position[1] == state.fruit_position_good[i][1]:
                    state.score += self.game_size*2
                    remove_list.append(i)
                    yes = True
            for i in range(len(remove_list)):
                state.fruit_position_good.pop(remove_list[i])
            return yes

        def get_bad_fruit(state):
            yes = False
            remove_list = []
            for i in range(len(state.fruit_position_bad)):
                if state.snake_position[0] == state.fruit_position_bad[i][0] and state.snake_position[1] == state.fruit_position_bad[i][1]:
                    state.score -= self.game_size*2
                    remove_list.append(i)
                    state.snake_body.pop()
                    yes = True
            for i in range(len(remove_list)):
                state.fruit_position_bad.pop(remove_list[i])
            return yes

        snake_control(state,change_to)

        state.snake_body.insert(0, list(state.snake_position))

        if not get_good_fruit(state):
            get_bad_fruit(state)
            state.snake_body.pop()

        self.check_game_over(state)

        if not state.over:
            if len(state.fruit_position_good) == 0 or (len(state.fruit_position_bad) == 0 and self.fruit_number[1]!=0):
                self.generate_fruit(state)
            state.score -= 1

        state.pack_board()

        state_copy = copy.deepcopy([state])[0]

        return state_copy

    def heuristic_cost(self,point,state):
        def distance(x,y):
            return abs(x[0]-y[0])+abs(x[1]-y[1])

        cost_list =[]
        for i in range(len(state.fruit_position_good)):
            cost_list.append(distance(point,state.fruit_position_good[i]))
        cost = min(cost_list)
        if point in state.snake_body  or self.out_of_board(point):
            cost += self.game_size*100
        if point in state.fruit_position_bad:
            cost += self.game_size*2
        return cost

    def simple_heuristic(self,state):

        actions_point = []
        for action in state.valid_actions:
            dx,dy = self.move_tf(action)
            x = state.snake_position[0] + dx
            y = state.snake_position[1] + dy
            actions_point.append([x,y])

        actions_cost = []
        for point in actions_point:
            actions_cost.append(self.heuristic_cost(point,state))
        idx = actions_cost.index(min(actions_cost))
        direction = state.valid_actions[idx]

        return direction

    def breadth_first_search(self,state):
        frontier = []
        explored = []
        frontier.append(state)
        node_count = 0
        result = None
        while len(frontier)!=0:
            if len(frontier)>1000:
                break
            #print(len(frontier))
            node = frontier.pop()
            node_count+=1
            node_copy = copy.deepcopy([node])[0]

            if node.round_end():
                result = node
                break
            explored.append(node_copy)

            child_list = []
            for action in node.valid_actions:
                node_copy = copy.deepcopy([node])[0]
                tmp = self.step(node_copy,action)
                if (not tmp.over or (tmp.over and tmp.round_end())) and not tmp.round_fail():
                    child_list.append(tmp)

            for child in child_list:
                if child in explored: continue
                frontier.append(child)

        return result.action_list

    def a_start_search(self,state):
        frontier = []
        explored = []
        frontier.append(state)
        node_count = 0
        result = state
        while len(frontier)!=0:
            if len(frontier)>1000:
                break
            #print(len(frontier))
            node = frontier.pop()
            node_count+=1
            node_copy = copy.deepcopy([node])[0]

            if node.round_end():
                result = node
                break
            explored.append(node_copy)

            child_list = []
            for action in node.valid_actions:
                node_copy = copy.deepcopy([node])[0]
                tmp = self.step(node_copy,action)
                if not tmp.over or (tmp.over and tmp.round_end()):
                    child_list.append(tmp)

            for child in child_list:
                if child in explored: continue
                frontier.append(child)
            frontier.sort(key=lambda x: x.score)

        return result.action_list

    def baseline_ai(self):
        self.state.print_state()

        direction = self.simple_heuristic(self.state)

        print('next action: %s'%direction)

        #input()

        self.state = self.step(self.state,direction)

        return self.state.over

    def human_play(self):
        self.state.print_state()

        print('Please enter you action idx(1,2,3) or 0 to let ai chose')
        idx = input()
        while idx not in ['0','1','2','3']:
            print('Please enter you action idx(1,2,3) or 0 to let ai chose')
            idx = input()

        if idx in ['1','2','3']:
            self.state = self.step(self.state,self.state.valid_actions[int(idx)-1])
        else:
            direction = self.simple_heuristic(self.state)
            print("AI chose %s"%direction)
            input()
            self.state  = self.step(self.state,direction)

        return self.state.over


if __name__ == '__main__':
    #test()
    #play()
    NN_model()
