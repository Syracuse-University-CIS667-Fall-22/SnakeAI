import os,sys,time,random,pygame,copy
import numpy as np

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
                    if board[i][j] == 1 or board[i][j] == 3:
                        pygame.draw.rect(self.game_window, self.green,pygame.Rect(i*S+offset, j*S, S, S))
                    elif board[i][j] == 2:
                        pygame.draw.rect(self.game_window, self.blue, pygame.Rect(i*S+offset, j*S, S, S))
                    elif board[i][j] == 2*self.game_size:
                        pygame.draw.rect(self.game_window, self.white, pygame.Rect(i*S+offset, j*S, S, S))
                    elif board[i][j] == -2*self.game_size:
                        pygame.draw.rect(self.game_window, self.red, pygame.Rect(i*S+offset, j*S, S, S))

        self.game_window.fill(self.black)

        S = self.block_size

        if game_1.over:
            if self.mode==1:
                show_over(game_1.score,'l')
            else:
                show_over(game_1.score)
        else:
            show_object(game_1.board)

        show_score(game_1.score,game_1.round_count)
        if self.mode==1:
            if game_2.over:
                show_over(game_2.score,'r')
            else:
                show_object(game_2.board,self.window_size+50)
            show_score(game_2.score,game_2.round_count,'r')

            pygame.draw.line(self.game_window,self.white, (self.window_size+25, 0), (self.window_size+25, self.window_y))

        pygame.display.update()
        self.fps.tick(self.snake_speed)
