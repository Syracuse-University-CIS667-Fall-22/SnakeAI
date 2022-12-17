import os,sys,time,random,pygame,copy
import numpy as np
import heapq as hq
from collections import deque

from snake_rander import Snake_Rander
from queue_search import*

class Parameters:
    def __init__(self):
        self.game_size = 10
        self.fruit_number = [25,10]
        self.round = 1

        self.snake_position = [2, 2]
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

class Snake_Env:
    def __init__(self,p):
        self.p = p
        self.game_size = p.game_size
        self.fruit_number = p.fruit_number
        self.round = p.round
        self.board = np.zeros((self.game_size,self.game_size))

        self.direction = copy.deepcopy(p.direction)
        self.round_count = 0
        self.over = False
        self.step_count = 0

        self.state = self.init_state()

        self.state = self.generate_fruit(self.state)
        self.board,self.score = self.pack_board(self.state)

    def init_state(self):
        snake_position = copy.deepcopy(self.p.snake_position)
        snake_body = [copy.deepcopy(self.p.snake_position)]
        fruit_position_good = []
        fruit_position_bad = []
        score = 0
        return (snake_position,snake_body,fruit_position_good,fruit_position_bad,score)

    def get_state(self):
        return {'state':self.state,'count':self.round_count,'board':self.board,'over':self.over}

    def round_end(self,board):
        snake_position,snake_body,fruit_position_good,fruit_position_bad = self.unpack_board(board)
        return True if len(fruit_position_good) == 0 else False

    def print_state(self):
        print('current state:')
        print(self.board.T.astype(np.int32))
        print('current score: %d'%self.state[4])
        print('current direction: %s'%self.direction)
        print('valid_actions:')
        print(self.valid_actions())
        #print(self.snake_body)

    def pack_board(self,state):
        snake_position,snake_body,fruit_position_good,fruit_position_bad,score = state
        board = np.zeros((self.game_size,self.game_size))

        for i in range(len(fruit_position_good)):
            board[fruit_position_good[i][0],fruit_position_good[i][1]] = 2*self.game_size
        for i in range(len(fruit_position_bad)):
            board[fruit_position_bad[i][0],fruit_position_bad[i][1]] = -2*self.game_size

        for i in snake_body:
            if not self.out_of_board(i):
                board[i[0],i[1]] = 1
        if not self.out_of_board(snake_position):
            board[snake_position[0],snake_position[1]] = 2

        return board,score

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

    def valid_actions(self):
        actions = ['UP','DOWN','LEFT','RIGHT']
        if self.direction == 'UP':
            actions.remove('DOWN')
        elif self.direction == 'DOWN':
            actions.remove('UP')
        elif self.direction == 'RIGHT':
            actions.remove('LEFT')
        elif self.direction == 'LEFT':
            actions.remove('RIGHT')
        return actions

    def out_of_board(self,point):
        return True if point[0] < 0 or point[0] > self.game_size-1 or point[1] < 0 or point[1] > self.game_size-1 else False

    def generate_fruit(self,state):
        snake_position,snake_body,fruit_position_good,fruit_position_bad,score = state
        if self.p.random:
            fruit_position_good = []
            fruit_position_bad = []

            for i in range(self.fruit_number[0]):
                tmp = [np.random.randint(1, self.game_size),np.random.randint(1, self.game_size)]
                while tmp in fruit_position_good or tmp in fruit_position_bad or tmp in snake_body:
                    tmp = [np.random.randint(1, self.game_size),np.random.randint(1, self.game_size)]
                fruit_position_good.append(tmp)

            for i in range(self.fruit_number[1]):
                tmp = [np.random.randint(1, self.game_size),np.random.randint(1, self.game_size)]
                while tmp in fruit_position_good or tmp in fruit_position_bad or tmp in snake_body:
                    tmp = [np.random.randint(1, self.game_size),np.random.randint(1, self.game_size)]
                fruit_position_bad.append(tmp)
        else:
            fruit_position_good = copy.deepcopy(self.p.fruit_list[self.round_count][0])
            fruit_position_bad = copy.deepcopy(self.p.fruit_list[self.round_count][1])

        self.round_count += 1
        state = (snake_position,snake_body,fruit_position_good,fruit_position_bad,score)
        return state

    # check game over function
    def check_game_over(self,state):
        snake_position,snake_body,fruit_position_good,fruit_position_bad,score = state
        over=False

        if self.out_of_board(snake_position):
            #print(1)
            over=True

        for block in snake_body[1:]:
            if snake_position[0] == block[0] and snake_position[1] == block[1]:
                #print(2)
                over=True

        if len(snake_body)==0:
            #print(3)
            over =True

        if self.round_count == self.round and len(fruit_position_good)==0:
            #print(4)
            over=True

        return over

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


    def step(self,state,direction):

        def snake_control():
            actions = self.valid_actions()
            change_to = direction if direction!=None else self.keyboard_input()
            if change_to in actions:
                self.direction = change_to

            dx,dy = self.move_tf(self.direction)
            snake_position[0] += dx
            snake_position[1] += dy


        def get_good_fruit(score):
            yes = False
            remove_list = []
            for i in range(len(fruit_position_good)):
                if snake_position[0] == fruit_position_good[i][0] and snake_position[1] == fruit_position_good[i][1]:
                    score += self.game_size*2
                    remove_list.append(i)
                    yes = True
            for i in range(len(remove_list)):
                fruit_position_good.pop(remove_list[i])
            return yes,score

        def get_bad_fruit(score):
            yes = False
            remove_list = []
            for i in range(len(fruit_position_bad)):
                if snake_position[0] == fruit_position_bad[i][0] and snake_position[1] == fruit_position_bad[i][1]:
                    score -= self.game_size*2
                    remove_list.append(i)
                    snake_body.pop()
                    yes = True
            for i in range(len(remove_list)):
                fruit_position_bad.pop(remove_list[i])
            return yes,score

        snake_position,snake_body,fruit_position_good,fruit_position_bad,score = state
        snake_control()

        snake_body.insert(0, list(snake_position))

        check,score = get_good_fruit(score)

        if not check:
            _,score = get_bad_fruit(score)
            snake_body.pop()

        state = (snake_position,snake_body,fruit_position_good,fruit_position_bad,score)

        over = self.check_game_over(state)
        board,_ = self.pack_board(state)

        if not over:
            if len(fruit_position_good) == 0 or (len(fruit_position_bad) == 0 and self.fruit_number[1]!=0):
                state = self.generate_fruit(state)
            score -= 1
            state = (snake_position,snake_body,fruit_position_good,fruit_position_bad,score)

        return over,state,board

    def heuristic_cost(self,point,state):
        def distance(x,y):
            return abs(x[0]-y[0])+abs(x[1]-y[1])
        snake_position,snake_body,fruit_position_good,fruit_position_bad,score = state
        cost_list =[]
        for i in range(len(fruit_position_good)):
            cost_list.append(distance(point,fruit_position_good[i]))
        cost = min(cost_list)
        if point in snake_body  or self.out_of_board(point):
            cost += self.game_size*100
        if point in fruit_position_bad:
            cost += self.game_size*2
        return cost

    def simple_heuristic(self,state):
        snake_position,snake_body,fruit_position_good,fruit_position_bad,score = state
        actions = self.valid_actions()

        actions_point = []
        for action in actions:
            dx,dy = self.move_tf(action)
            x = snake_position[0] + dx
            y = snake_position[1] + dy
            actions_point.append([x,y])

        actions_cost = []
        for point in actions_point:
            actions_cost.append(self.heuristic_cost(point,state))
        idx = actions_cost.index(min(actions_cost))
        direction = actions[idx]

        return direction

    def breadth_first_search(self):
        frontier = []
        explored = set()
        root = [self.snake_position,self.direction]
        frontier.append(root)
        node_count = 0
        while len(frontier)!=0:
            node = frontier.pop() # need to count how many times this happens
            node_count+=1
            if node.is_goal(): break
            explored.add(node.state)
            for child in node.children():
                if child.state in explored: continue
                frontier.push(child)
        plan = node.path() if node.is_goal() else []

        # Second return value should be node count, not 0
        return plan, node_count

    def baseline_ai(self):
        self.print_state()

        direction = self.simple_heuristic(self.state)

        print('next action: %s'%direction)

        self.over,self.state,self.board  = self.step(self.state,direction)

        return self.over

    def human_play(self):
        self.print_state()

        actions = self.valid_actions()

        print('Please enter you action idx(1,2,3) or 0 to let ai chose')
        idx = input()
        while idx not in ['0','1','2','3']:
            print('Please enter you action idx(1,2,3) or 0 to let ai chose')
            idx = input()

        if idx in ['1','2','3']:
            self.over,self.state,self.board  = self.step(self.state,actions[int(idx)-1])
        else:
            direction = self.simple_heuristic()
            print("AI chose %s"%direction)
            input()
            self.over,self.state,self.board  = self.step(self.state,direction)

        return self.over

def mode_1():
    p = Parameters()
    snake_rander = Snake_Rander(p)
    snake_ai = Snake_Env(p)
    snake_human = Snake_Env(p)
    snake_rander.game_render(snake_ai.get_state(),snake_human.get_state())
    input()
    over_1 = False
    over_2 = False
    while True:
        if not over_1:
            over_1 = snake_ai.baseline_ai()
            snake_rander.game_render(snake_ai.get_state(),snake_human.get_state())
        if not over_2:
            over_2 = snake_human.human_play()
            snake_rander.game_render(snake_ai.get_state(),snake_human.get_state())
        if over_1 and over_2:
            break

def mode_2():
    p = Parameters()
    snake_rander = Snake_Rander(p,2)
    snake_ai = Snake_Env(p)
    snake_rander.game_render(snake_ai.get_state())
    input()
    over_1 = False
    while True:
        if not over_1:
            over_1 = snake_ai.baseline_ai()
            snake_rander.game_render(snake_ai.get_state())
        if over_1:
            break

if __name__ == '__main__':
    mode_1()
    print('Press x to exit')
    key = input()
    while key !='x':
        print('Press x to exit')
        key = input()
