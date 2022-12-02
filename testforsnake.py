import random
import numpy as np

board_size = 10
snake1_index = [[3,3],[3,4],[3,5]]
temp = board_size - 3
snake2_index = [[temp,temp],[temp,temp-1],[temp,temp-2]]
board = np.zeros((board_size,board_size))
for i in snake1_index:
    board[i[0],i[1]] = 1


board[snake1_index[0][0],snake1_index[0][1]] = 2

for i in snake2_index:
    board[i[0],i[1]] = -1
board[snake2_index[0][0],snake2_index[0][1]] = -2

fruit_number = 7
good_fruits=[]

for i in range(fruit_number):

   generateddata=[random.randint(0,9),random.randint(0,9)]

   if not generateddata in good_fruits:
       good_fruits.append(generateddata)

for i in range(len(good_fruits)):

    if (good_fruits[i] not in snake1_index) and (good_fruits[i] not in snake2_index):
        board[good_fruits[i][0],good_fruits[i][1]] = 5

bad_fruits=[]
for i in range(fruit_number):

   generateddata=[random.randint(0,9),random.randint(0,9)]

   if not generateddata in bad_fruits:
       bad_fruits.append(generateddata)

for i in range(len(bad_fruits)):
    if (bad_fruits[i] not in snake1_index) and (bad_fruits[i] not in snake2_index):
        board[bad_fruits[i][0],bad_fruits[i][1]] = -5


print(board)
