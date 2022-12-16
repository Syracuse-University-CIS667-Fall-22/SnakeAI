import os,sys,time,random,pygame
import numpy as np

class Snake_Env:
    def __init__(self,rander=False):
        self.game_size = 10
        self.fruit_number = [3,3]
        self.board = np.zeros((self.game_size,self.game_size))

        self.snake_position = [2, 2]
        self.snake_body = [self.snake_position]

        self

        self.generate_fruit()

        if rander:
            self.game_setup()

        self.score = 0

    def update_board(self):
        self.board = np.zeros((self.game_size,self.game_size))
        for i in self.snake_body:
            self.board[i[0],i[1]] = 1
        self.board[self.snake_position[0],self.snake_position[1]] = 2

        for i in range(len(self.fruit_position_good)):
            self.board[self.fruit_position_good[i][0],self.fruit_position_good[i][1]] = 10
        for i in range(len(self.fruit_position_bad)):
            self.board[self.fruit_position_bad[i][0],self.fruit_position_bad[i][1]] = -10

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

    def get_state(self):
        pass

    def game_setup(self):
        # defining colors
        self.black = pygame.Color(0, 0, 0)
        self.white = pygame.Color(255, 255, 255)
        self.red = pygame.Color(255, 0, 0)
        self.green = pygame.Color(0, 255, 0)
        self.blue = pygame.Color(0, 0, 255)

        self.snake_speed = 5
        self.window_size = 720
        self.block_size = self.window_size/self.game_size

        # Window size
        self.window_x = self.window_size
        self.window_y = self.window_size

        # Initialising pygame
        pygame.init()
        pygame.display.set_caption('Snake Game')
        self.game_window = pygame.display.set_mode((self.window_x, self.window_y))

        # FPS (frames per second) controller
        self.fps = pygame.time.Clock()

        # defining first 1 block of snake body
        self.snake_body = [[]]

        self.direction = 'RIGHT'

    def generate_fruit(self,good_p=None,bad_p=None):
        # fruit position
        self.fruit_position_good = []
        self.fruit_position_bad = []

        for i in range(self.fruit_number[0]):
            tmp = [np.random.randint(1, self.game_size),np.random.randint(1, self.game_size)]
            while tmp in self.fruit_position_good or tmp in self.fruit_position_bad or tmp in self.snake_body:
                tmp = [np.random.randint(1, self.game_size),np.random.randint(1, self.game_size)]
            self.fruit_position_good.append( tmp if good_p==None else good_p[i])

        for i in range(self.fruit_number[1]):
            tmp = [np.random.randint(1, self.game_size),np.random.randint(1, self.game_size)]
            while tmp in self.fruit_position_good or tmp in self.fruit_position_bad or tmp in self.snake_body:
                tmp = [np.random.randint(1, self.game_size),np.random.randint(1, self.game_size)]
            self.fruit_position_bad.append(tmp if bad_p==None else bad_p[i])


    # displaying Score function
    def show_score(self):
        score_font = pygame.font.SysFont('times new roman', 20)
        score_surface = score_font.render('Score : ' + str(self.score), True, self.white)
        score_rect = score_surface.get_rect()
        self.game_window.blit(score_surface, score_rect)

    # check game over function
    def check_game_over(self):
        over=False
        # Game Over conditions
        if self.out_of_board(self.snake_position):
            over=True

        # Touching the snake body
        for block in self.snake_body[1:]:
            if self.snake_position[0] == block[0] and self.snake_position[1] == block[1]:
                over=True

        if len(self.snake_body)==0:
            over =True

        return over

    def move_tf(self,direction):
        changeto_list = ['UP','DOWN','LEFT','RIGHT']
        dx_list = [0,0,-1,1]
        dy_list = [-1,1,0,0]
        for i in range(4):
            if direction == changeto_list[i]:
                return dx_list[i],dy_list[i]


    def snake_control(self,direction=None):
        def keyboard_input():
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

        if len(self.fruit_position_good) == 0 or len(self.fruit_position_bad) == 0:
            self.generate_fruit()

        over = self.check_game_over()

        if not over:
            self.score -= 1
            self.update_board()
        return over

    def game_render(self,over):
        if over:
            my_font = pygame.font.SysFont('times new roman', 50)
            game_over_surface = my_font.render('Your Score is : ' + str(self.score), True, self.red)
            game_over_rect = game_over_surface.get_rect()
            game_over_rect.midtop = (self.window_x/2, self.window_y/4)
            self.game_window.blit(game_over_surface, game_over_rect)
            pygame.display.flip()
            time.sleep(2)
            pygame.quit()
            quit()

        self.game_window.fill(self.black)

        S = self.block_size

        for pos in self.snake_body:
            pygame.draw.rect(self.game_window, self.green,pygame.Rect(pos[0]*S, pos[1]*S, S, S))
        for i in range(len(self.fruit_position_good)):
            pygame.draw.rect(self.game_window, self.white, pygame.Rect(self.fruit_position_good[i][0]*S, self.fruit_position_good[i][1]*S, S, S))
        for i in range(len(self.fruit_position_bad)):
            pygame.draw.rect(self.game_window, self.red, pygame.Rect(self.fruit_position_bad[i][0]*S, self.fruit_position_bad[i][1]*S, S, S))
        self.show_score()
        pygame.display.update()
        self.fps.tick(self.snake_speed)

    def step(self,direction):
        self.snake_control(direction)
        self.game_update()
        over = self.check_game_over()
        return over,self.board

    def simple_heuristic(self):
        def distance(position):
            return abs(position[0]-self.fruit_position_good[0][0])+abs(position[1]-self.fruit_position_good[0][1])
        actions = self.valid_actions()

        actions_point = []
        for action in actions:
            dx,dy = self.move_tf(action)
            x = self.snake_position[0] + dx
            y = self.snake_position[1] + dy
            actions_point.append([x,y])

        actions_cost = []
        for point in actions_point:
            cost = distance(point)
            if point in self.snake_body  or self.out_of_board(point):
                cost += self.game_size*10
            if point in self.fruit_position_bad:
                cost += self.game_size*2
            actions_cost.append(cost)
        idx = actions_cost.index(min(actions_cost))
        direction = actions[idx]

        return direction

    def baseline_ai(self):
        while True:

            direction = self.simple_heuristic()

            self.snake_control(direction)

            over = self.game_update()

            self.game_render(over)

            #input()

    def human_play(self):
        while True:
            self.snake_control()
            over = self.game_update()
            self.game_render(over)



if __name__ == '__main__':
    snake = Snake_Env(True)
    snake.baseline_ai()
    #snake.human_play()
