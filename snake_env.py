import os,sys,time,random,pygame,threading,copy
from multiprocessing import Process
import numpy as np

class Parameters:
    def __init__(self):
        self.game_size = 10
        self.fruit_number = [1,1]
        self.round = 2

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
                while tmp in self.fruit_position_good or tmp in self.fruit_position_bad:
                    tmp = [np.random.randint(1, self.game_size),np.random.randint(1, self.game_size)]
                self.fruit_position_good.append(tmp)

            for i in range(self.fruit_number[1]):
                tmp = [np.random.randint(1, self.game_size),np.random.randint(1, self.game_size)]
                while tmp in self.fruit_position_good or tmp in self.fruit_position_bad:
                    tmp = [np.random.randint(1, self.game_size),np.random.randint(1, self.game_size)]
                self.fruit_position_bad.append(tmp)
            self.fruit_list.append([self.fruit_position_good,self.fruit_position_bad])

class Snake_Rander:
    def __init__(self,p,mode=1,name='Snake Game'):
        self.game_size = p.game_size
        self.mode = mode

        self.black = pygame.Color(0, 0, 0)
        self.white = pygame.Color(255, 255, 255)
        self.red = pygame.Color(255, 0, 0)
        self.green = pygame.Color(0, 255, 0)
        self.blue = pygame.Color(0, 0, 255)

        self.snake_speed = 10
        self.window_size = 600
        self.block_size = self.window_size/self.game_size

        # Window size
        self.window_x = self.window_size
        self.window_y = self.window_size

        # Initialising pygame
        pygame.init()
        pygame.display.set_caption('%s'%name)
        if mode == 1:
            self.game_window = pygame.display.set_mode((self.window_x*2+50, self.window_y))
        else:
            self.game_window = pygame.display.set_mode((self.window_x, self.window_y))

        # FPS (frames per second) controller
        self.fps = pygame.time.Clock()


    def game_render(self,game_1,game_2=None):
        # displaying Score function
        def show_score(score,count,direction=None):
            score_font = pygame.font.SysFont('times new roman', 20)
            if self.mode==1:
                if direction==None:
                    score_surface = score_font.render('Score : ' + str(score)+'  Round : '+str(count)+'                           AI', True, self.white)
                else:
                    score_surface = score_font.render('Score : ' + str(score)+'  Round : '+str(count)+'                           Human', True, self.white)
            else:
                score_surface = score_font.render('Score : ' + str(score)+'  Round : '+str(count), True, self.white)
            score_rect = score_surface.get_rect()
            if direction==None:
                score_rect.topleft = (0,0)
                self.game_window.blit(score_surface, score_rect)
            else:
                score_rect.topleft = (self.window_size+50,0)
                self.game_window.blit(score_surface, score_rect)

        def show_over(score,direction=None):
            my_font = pygame.font.SysFont('times new roman', 50)
            game_over_surface = my_font.render('Your Score is : ' + str(score), True, self.red)
            game_over_rect = game_over_surface.get_rect()
            if direction ==None:
                game_over_rect.midtop = (self.window_x/2, self.window_y/4)
            else:
                if direction=='l':
                    game_over_rect.midtop = (self.window_size/2, self.window_y/4)
                else:
                    game_over_rect.midtop = (self.window_size/2+self.window_size+50, self.window_y/4)
            self.game_window.blit(game_over_surface, game_over_rect)
            pygame.display.flip()
            #pygame.quit()
            #quit()

        def show_object(board,offset=0):
            for i in range(self.game_size):
                for j in range(self.game_size):
                    if board[i][j] == 1:
                        pygame.draw.rect(self.game_window, self.green,pygame.Rect(i*S+offset, j*S, S, S))
                    elif board[i][j] == 2:
                        pygame.draw.rect(self.game_window, self.blue, pygame.Rect(i*S+offset, j*S, S, S))
                    elif board[i][j] == 2*self.game_size:
                        pygame.draw.rect(self.game_window, self.white, pygame.Rect(i*S+offset, j*S, S, S))
                    elif board[i][j] == -2*self.game_size:
                        pygame.draw.rect(self.game_window, self.red, pygame.Rect(i*S+offset, j*S, S, S))

        self.game_window.fill(self.black)

        S = self.block_size

        if game_1['over']:
            if self.mode==1:
                show_over(game_1['score'],'l')
            else:
                show_over(game_1['score'])
        else:
            show_object(game_1['board'])

        show_score(game_1['score'],game_1['count'])
        if self.mode==1:
            if game_2['over']:
                show_over(game_2['score'],'r')
            else:
                show_object(game_2['board'],self.window_size+50)
            show_score(game_2['score'],game_2['count'],'r')

            pygame.draw.line(self.game_window,self.white, (self.window_size+25, 0), (self.window_size+25, self.window_y))

        pygame.display.update()
        self.fps.tick(self.snake_speed)

class Snake_Env:
    def __init__(self,p):
        self.p = p
        self.game_size = p.game_size
        self.fruit_number = p.fruit_number
        self.round = p.round
        self.board = np.zeros((self.game_size,self.game_size))

        self.snake_position = copy.deepcopy(p.snake_position)
        self.snake_body = [self.snake_position]
        self.direction = copy.deepcopy(p.direction)
        self.round_count = 0
        self.score = 0
        self.over = False

        self.generate_fruit()

        self.update_board()

    def get_state(self):
        return {'score':self.score,'count':self.round_count,'board':self.board,'over':self.over}

    def update_board(self):
        self.board = np.zeros((self.game_size,self.game_size))
        for i in self.snake_body:
            self.board[i[0],i[1]] = 1
        self.board[self.snake_position[0],self.snake_position[1]] = 2

        for i in range(len(self.fruit_position_good)):
            self.board[self.fruit_position_good[i][0],self.fruit_position_good[i][1]] = 2*self.game_size
        for i in range(len(self.fruit_position_bad)):
            self.board[self.fruit_position_bad[i][0],self.fruit_position_bad[i][1]] = -2*self.game_size

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

    def generate_fruit(self):
        if self.p.random:
            self.fruit_position_good = []
            self.fruit_position_bad = []

            for i in range(self.fruit_number[0]):
                tmp = [np.random.randint(1, self.game_size),np.random.randint(1, self.game_size)]
                while tmp in self.fruit_position_good or tmp in self.fruit_position_bad or tmp in self.snake_body:
                    tmp = [np.random.randint(1, self.game_size),np.random.randint(1, self.game_size)]
                self.fruit_position_good.append(tmp)

            for i in range(self.fruit_number[1]):
                tmp = [np.random.randint(1, self.game_size),np.random.randint(1, self.game_size)]
                while tmp in self.fruit_position_good or tmp in self.fruit_position_bad or tmp in self.snake_body:
                    tmp = [np.random.randint(1, self.game_size),np.random.randint(1, self.game_size)]
                self.fruit_position_bad.append(tmp)
        else:
            self.fruit_position_good = copy.deepcopy(self.p.fruit_list[self.round_count][0])
            self.fruit_position_bad = copy.deepcopy(self.p.fruit_list[self.round_count][1])

        self.round_count += 1

    # check game over function
    def check_game_over(self):
        over=False

        if self.out_of_board(self.snake_position):
            over=True

        for block in self.snake_body[1:]:
            if self.snake_position[0] == block[0] and self.snake_position[1] == block[1]:
                over=True

        if len(self.snake_body)==0:
            over =True

        if self.round_count == self.round and len(self.fruit_position_good)==0:
            over=True

        return over

    def move_tf(self,direction):
        changeto_list = ['UP','DOWN','LEFT','RIGHT']
        dx_list = [0,0,-1,1]
        dy_list = [-1,1,0,0]
        for i in range(4):
            if direction == changeto_list[i]:
                return dx_list[i],dy_list[i]

    def snake_control(self,direction=None):
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

        actions = self.valid_actions()
        change_to = direction if direction!=None else keyboard_input()
        if change_to in actions:
            self.direction = change_to

        dx,dy = self.move_tf(self.direction)
        self.snake_position[0] += dx
        self.snake_position[1] += dy

    def game_update(self):
        def get_good_fruit():
            yes = False
            remove_list = []
            for i in range(len(self.fruit_position_good)):
                if self.snake_position[0] == self.fruit_position_good[i][0] and self.snake_position[1] == self.fruit_position_good[i][1]:
                    self.score += self.game_size*2
                    remove_list.append(i)
                    yes = True
            for i in range(len(remove_list)):
                self.fruit_position_good.pop(remove_list[i])
            return yes

        def get_bad_fruit():
            yes = False
            remove_list = []
            for i in range(len(self.fruit_position_bad)):
                if self.snake_position[0] == self.fruit_position_bad[i][0] and self.snake_position[1] == self.fruit_position_bad[i][1]:
                    self.score -= self.game_size*2
                    remove_list.append(i)
                    self.snake_body.pop()
                    yes = True
            for i in range(len(remove_list)):
                self.fruit_position_bad.pop(remove_list[i])
            return yes

        # Snake body growing mechanism
        # if fruits and snakes collide then scores
        # will be incremented by 10
        self.snake_body.insert(0, list(self.snake_position))
        if not get_good_fruit():
            get_bad_fruit()
            self.snake_body.pop()

        over = self.check_game_over()

        if not over:
            if len(self.fruit_position_good) == 0 or (len(self.fruit_position_bad) == 0 and self.fruit_number[1]!=0):
                self.generate_fruit()
            self.score -= 1
            self.update_board()
        self.over = over
        return over

    def simple_heuristic(self):
        def distance(x,y):
            return abs(x[0]-y[0])+abs(x[1]-y[1])

        actions = self.valid_actions()

        actions_point = []
        for action in actions:
            dx,dy = self.move_tf(action)
            x = self.snake_position[0] + dx
            y = self.snake_position[1] + dy
            actions_point.append([x,y])

        actions_cost = []
        for point in actions_point:
            cost = distance(point,self.fruit_position_good[0])
            if point in self.snake_body  or self.out_of_board(point):
                cost += self.game_size*10
            if point in self.fruit_position_bad:
                cost += self.game_size*2
            actions_cost.append(cost)
        idx = actions_cost.index(min(actions_cost))
        direction = actions[idx]

        return direction

    def print_state(self):
        print('current state:')
        print(self.board.T.astype(np.int32))
        print('current score: %d'%self.score)
        print('current direction: %s'%self.direction)
        print('valid_actions:')
        print(self.valid_actions())

    def baseline_ai(self):
        self.print_state()

        direction = self.simple_heuristic()

        print('next action: %s'%direction)
        input()

        self.snake_control(direction)
        over = self.game_update()

        return over

    def human_play(self):
        self.print_state()

        actions = self.valid_actions()

        print('Please enter you action idx(1,2,3) or 0 to let ai chose')
        idx = input()
        while idx not in ['0','1','2','3']:
            print('Please enter you action idx(1,2,3) or 0 to let ai chose')
            idx = input()

        if idx in ['1','2','3']:
            self.snake_control(actions[int(idx)-1])
        else:
            direction = self.simple_heuristic()
            print("AI chose %s"%direction)
            input()
            self.snake_control(direction)


        over = self.game_update()

        return over

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
