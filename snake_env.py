import os,sys,time,random,pygame
import numpy as np

class Snake_Env:
    def __init__(self,rander=False):
        self.game_size = 10
        self.board = np.zeros((self.game_size,self.game_size))
        self.generate_fruit()

        self.snake_position = [2, 2]
        self.snake_body = [self.snake_position]

        if rander:
            self.game_setup()

        self.score = 0

    def update_board(self):
        self.board = np.zeros((self.game_size,self.game_size))
        for i in self.snake_body:
            self.board[i[0],i[1]] = 1
        self.board[self.snake_position[0],self.snake_position[1]] = 2

        self.board[self.fruit_position_good[0],self.fruit_position_good[1]] = 10
        self.board[self.fruit_position_bad[0],self.fruit_position_bad[1]] = -10

    def get_state(self):
        pass

    def game_setup(self):
        # defining colors
        self.black = pygame.Color(0, 0, 0)
        self.white = pygame.Color(255, 255, 255)
        self.red = pygame.Color(255, 0, 0)
        self.green = pygame.Color(0, 255, 0)
        self.blue = pygame.Color(0, 0, 255)

        self.fruit_spawn = True
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
        self.change_to = self.direction

    def generate_fruit(self,good_p=None,bad_p=None):
        # fruit position
        self.fruit_position_good = [np.random.randint(1, self.game_size),np.random.randint(1, self.game_size)] if good_p==None else good_p
        self.fruit_position_bad = [np.random.randint(1, self.game_size),np.random.randint(1, self.game_size)] if bad_p==None else bad_p

        self.fruit_spawn = False


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
        if self.snake_position[0] < 0 or self.snake_position[0] > self.game_size-1\
        or self.snake_position[1] < 0 or self.snake_position[1] > self.game_size-1:
            over=True

        # Touching the snake body
        for block in self.snake_body[1:]:
            if self.snake_position[0] == block[0] and self.snake_position[1] == block[1]:
                over=True

        if len(self.snake_body)==0:
            over =True

        return over


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

        self.change_to = direction if direction!=None else keyboard_input()

        # If two keys pressed simultaneously
        # we don't want snake to move into two
        # directions simultaneously
        changeto_list = ['UP','DOWN','LEFT','RIGHT']
        direction_list = ['DOWN','UP','RIGHT','LEFT']
        for i in range(4):
            if self.change_to == changeto_list[i] and self.direction != direction_list[i]:
                self.direction = changeto_list[i]

        # Moving the snake
        dx_list = [0,0,-1,1]
        dy_list = [-1,1,0,0]
        for i in range(4):
            if self.direction == changeto_list[i]:
                self.snake_position[0]+=dx_list[i]
                self.snake_position[1]+=dy_list[i]

    def game_update(self):
        # Snake body growing mechanism
        # if fruits and snakes collide then scores
        # will be incremented by 10
        self.snake_body.insert(0, list(self.snake_position))
        if self.snake_position[0] == self.fruit_position_good[0] and self.snake_position[1] == self.fruit_position_good[1]:
            self.score += 10
            self.fruit_spawn = True
        else:
            if self.snake_position[0] == self.fruit_position_bad[0] and self.snake_position[1] == self.fruit_position_bad[1]:
                self.score -= 10
                self.fruit_spawn = True
                self.snake_body.pop()
            self.snake_body.pop()


        if self.fruit_spawn:
            self.generate_fruit()

        over = self.check_game_over()

        if not over:
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
        pygame.draw.rect(self.game_window, self.white, pygame.Rect(self.fruit_position_good[0]*S, self.fruit_position_good[1]*S, S, S))
        pygame.draw.rect(self.game_window, self.red, pygame.Rect(self.fruit_position_bad[0]*S, self.fruit_position_bad[1]*S, S, S))
        self.show_score()
        pygame.display.update()
        self.fps.tick(self.snake_speed)

    def step(self,direction):
        self.snake_control(direction)
        self.game_update()
        over = self.check_game_over()
        return over,self.board

    def baseline_ai(self):

        return 'RIGHT' # 'UP','LEFT','DOWN','RIGHT'

    def test(self):
        directions=['UP','LEFT','DOWN','RIGHT']
        i=0
        while True:

            self.snake_control(directions[i])
            #self.snake_control()
            i=i+1
            i= 0 if i>3 else i

            self.game_update()
            print('snake')
            print(self.snake_position)
            print('snake body')
            print(self.snake_body)
            print('fruit')
            print(self.fruit_position_good)
            print(self.board.T)

            over = self.check_game_over()

            self.game_render(over)


    def main(self):
        while True:

            direction = self.baseline_ai()

            self.snake_control(direction)

            over = self.game_update()
            print('snake')
            print(self.snake_position)
            print('snake body')
            print(self.snake_body)
            print('fruit')
            print(self.fruit_position_good)
            print(self.board.T)

            self.game_render(over)

            input()

    def human_play(self):
        while True:

            self.snake_control()

            over = self.game_update()
            print('snake')
            print(self.snake_position)
            print('snake body')
            print(self.snake_body)
            print('fruit')
            print(self.fruit_position_good)
            print(self.board.T)

            self.game_render(over)



if __name__ == '__main__':
    snake = Snake_Env(True)
    snake.main()
    #snake.test()
    #snake.human_play()
