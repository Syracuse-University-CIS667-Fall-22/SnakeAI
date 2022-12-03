import pygame
import time
import random

# defining colors
black = pygame.Color(0, 0, 0)
white = pygame.Color(255, 255, 255)
red = pygame.Color(255, 0, 0)
green = pygame.Color(0, 255, 0)
blue = pygame.Color(0, 0, 255)

class Snake_Env:
    def __init__(self):
        self.snake_speed = 1
        self.block_size = 100

        # Window size
        self.window_x = 720
        self.window_y = 480

        # Initialising pygame
        pygame.init()
        pygame.display.set_caption('GeeksforGeeks Snakes')
        self.game_window = pygame.display.set_mode((self.window_x, self.window_y))

        # FPS (frames per second) controller
        self.fps = pygame.time.Clock()

        # defining snake default position
        self.snake_position = [2*self.block_size, 2*self.block_size]

        # defining first 1 block of snake body
        self.snake_body = [[]]

        self.generate_fruit()

        self.fruit_spawn = True

        # setting default snake direction towards
        # right
        self.direction = 'RIGHT'
        self.change_to = self.direction

        # initial score
        self.score = 0

    def generate_fruit(self):
        # fruit position
        self.fruit_position = [random.randrange(1, (self.window_x//self.block_size)) * self.block_size,
                               random.randrange(1, (self.window_y//self.block_size)) * self.block_size]


    # displaying Score function
    def show_score(self):
        score_font = pygame.font.SysFont('times new roman', 20)
        score_surface = score_font.render('Score : ' + str(self.score), True, white)
        score_rect = score_surface.get_rect()
        self.game_window.blit(score_surface, score_rect)

    # check game over function
    def check_game_over(self):
        over=False
        # Game Over conditions
        if self.snake_position[0] < 0 or self.snake_position[0] > self.window_x-self.block_size\
        or self.snake_position[1] < 0 or self.snake_position[1] > self.window_y-self.block_size:
            over=True

        # Touching the snake body
        for block in self.snake_body[1:]:
            if self.snake_position[0] == block[0] and self.snake_position[1] == block[1]:
                over=True

        return over


    def snake_control(self):
        # handling key events
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    self.change_to = 'UP'
                if event.key == pygame.K_DOWN:
                    self.change_to = 'DOWN'
                if event.key == pygame.K_LEFT:
                    self.change_to = 'LEFT'
                if event.key == pygame.K_RIGHT:
                    self.change_to = 'RIGHT'

        # If two keys pressed simultaneously
        # we don't want snake to move into two
        # directions simultaneously
        changeto_list = ['UP','DOWN','LEFT','RIGHT']
        direction_list = ['DOWN','UP','RIGHT','LEFT']
        for i in range(4):
            if self.change_to == changeto_list[i] and self.direction != direction_list[i]:
                self.direction = changeto_list[i]

        # Moving the snake
        dx_list = [0,0,-self.block_size,self.block_size]
        dy_list = [-self.block_size,self.block_size,0,0]
        for i in range(4):
            if self.direction == changeto_list[i]:
                self.snake_position[0]+=dx_list[i]
                self.snake_position[1]+=dy_list[i]

    def game_update(self):
        # Snake body growing mechanism
        # if fruits and snakes collide then scores
        # will be incremented by 10
        self.snake_body.insert(0, list(self.snake_position))
        if self.snake_position[0] == self.fruit_position[0] and self.snake_position[1] == self.fruit_position[1]:
            self.score += 10
            self.fruit_spawn = False
        else:
            self.snake_body.pop()

        if not self.fruit_spawn:
            self.generate_fruit()

        self.fruit_spawn = True

    def game_render(self,over):
        self.game_window.fill(black)

        for pos in self.snake_body:
            pygame.draw.rect(self.game_window, green,pygame.Rect(pos[0], pos[1], self.block_size, self.block_size))
        pygame.draw.rect(self.game_window, white, pygame.Rect(self.fruit_position[0], self.fruit_position[1], self.block_size, self.block_size))
        self.show_score()
        pygame.display.update()
        self.fps.tick(self.snake_speed)

        if over:
            my_font = pygame.font.SysFont('times new roman', 50)
            game_over_surface = my_font.render('Your Score is : ' + str(self.score), True, red)
            game_over_rect = game_over_surface.get_rect()
            game_over_rect.midtop = (self.window_x/2, self.window_y/4)
            self.game_window.blit(game_over_surface, game_over_rect)
            pygame.display.flip()
            time.sleep(2)
            pygame.quit()
            quit()


    def main(self):
        while True:

            self.snake_control()

            self.game_update()

            over = self.check_game_over()

            self.game_render(over)


if __name__ == '__main__':
    snake = Snake_Env()
    snake.main()
