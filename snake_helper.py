# ********

# TODO: implement pad(num)
# Return a string representation of num that is always two characters wide.
# If num does not already have two digits, a leading " " is inserted in front.
# This is called "padding".  For example, pad(12) is "12", and pad(1) is " 1".
# You can assume num is either one or two digits long.
import random
import numpy as np

def pad(num: int) -> str:
    if num < 10:
        return " " + str(num)
    else:
        return str(num)

# TODO: implement pad_all(nums)
# Return a new list whose elements are padded versions of the elements in nums.
# For example, pad_all([12, 1]) should return ["12", " 1"].
# Your code should create a new list, and not modify the original list.
# You can assume each element of nums is an int with one or two digits.
def pad_all(nums: list) -> list:
    padded_nums = [pad(i) for i in nums]
    return padded_nums # replace with your implementation

# TODO: implement initial_state()
# Return a (player, board) tuple representing the initial game state
# The initial player is player 0.
# board is matrix representing the initial snake game board at the start of the game.
# The number at index p should be the 1 if p is snake 1's body, 2 if p is snake 1's head
# The number at index p should be the -1 if p is snake -1's body, -2 if p is snake 1's head
# The number at index p should be the 1 if p is good fruit, 2 if p is bad fruit

def initial_state() -> tuple:
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

    state = (0, board,snake1_index,snake2_index)
    return state  # replace with your implementation

# TODO: implement game_over(state)
# Return True if the game is over, and False otherwise.
# The game is over once all pits are empty.
# Your code should not modify the board list.
# The built-in functions "any" and "all" may be useful:
#   https://docs.python.org/3/library/functions.html#all
def game_over(state: tuple) -> bool:
    result = True
    player, board, snake1_index,snake2_index = state
    board_size = 10
    for i in range(0, board_size):
        for j in range(0, board_size):

            if board[i][j] == 5 or board[i][j] == -5:
                result = False

    return result

# TODO: implement valid_actions(state)
# state is a (player, board) tuple
# Return a list of all positions on the board where the current player can pick up gems.
# A position is a valid move if it is one of the player's pits and has 1 or more gems in it.
# For example, if all of player's pits are empty, you should return [].
# The positions in the returned list should be ordered from lowest to highest.
# Your code should not modify the board list.
def valid_actions(state: tuple) -> list:
    player, board ,snake1_index,snake2_index= state
    board_size = 10
    if player == 0:
        head = snake1_index[0]
        possible_positions = [[head[0]+1,head[1]],[head[0]-1,head[1]],[head[0],head[1]+1],[head[0],head[1]-1]]
        actions = []
        for i in possible_positions:
            if (i[0] >=0 and i[0]< board_size and i[1] >=0 and i[1]< board_size and board[i[0],i[1]] != 1 and board[i[0],i[1]] != -1 and board[i[0],i[1]] != 2 and board[i[0],i[1]] != -2 ):
                actions.append(i)
    if player == 1:
        head = snake2_index[0]
        possible_positions = [[head[0]+1,head[1]],[head[0]-1,head[1]],[head[0],head[1]+1],[head[0],head[1]-1]]
        actions = []
        for i in possible_positions:
            if (i[0] >=0 and i[0]< board_size and i[1] >=0 and i[1]< board_size and board[i[0],i[1]] != 1 and board[i[0],i[1]] != -1 and board[i[0],i[1]] != 2 and board[i[0],i[1]] != -2 ):
                actions.append(i)



    return actions  # replace with your implementation

# # TODO: implement length_of(player)
# # Return the length of the given player's snake body.
# # You can assume player is either 0 or 1.
# def length_of(player: int) -> int:
#
#     if player == 0:
#         snake_len = len()
#     else:
#         mancala = 13
#     return mancala  # replace with your implementation

# TODO: implement pits_of(player)
# Return a list of numeric positions corresponding to the given player's pits.
# The positions in the list should be ordered from lowest to highest.
# Player 0's pits are on the bottom and player 1's pits are on the top.
# You can assume player is either 0 or 1.

# def pits_of(player: int) -> list:
#     if player == 0:
#         pits = [i for i in range(6)]
#     else:
#         pits = [i for i in range(7,13)]
#
#     return pits  # replace with your implementation

# TODO: implement player_who_can_do(move)
# Return the player (either 0 or 1) who is allowed to perform the given move.
# The move is allowed if it is the position of one of the player's pits.
# For example, position 2 is one of player 0's pits.
# So player_who_can_do(2) should return 0.
# You can assume that move is a valid position for one of the players.
# def player_who_can_do(move: int) -> int:
#
#     if move in range(6):
#         return 0
#     else:
#         return 1
#      # replace with your implementation

# TODO: implement opposite_from(position)
# Return the position of the pit that is opposite from the given position.
# Check the pdf instructions for the definition of "opposite".
def opposite_from(position: int) -> int:
    return 12-position  # replace with your implementation

# TODO: implement play_turn(move, board)
# Return the new game state after the given move is performed on the given board.
# The return value should be a tuple (new_player, new_board).
#   new_player should be the player (0 or 1) whose turn it is after the move.
#   new_board should be a list representing the new board state after the move.
#
# Parameters:
#   board is a list representing the current state of the game board before the turn is taken.
#   move is an int representing the position where the current player picks up gems.
# You can assume that move is a valid move for the current player who is taking their turn.
# Check the pdf instructions for the detailed rules of taking a turn.
#
# It may be helpful to use several of the functions you implemented above.
# You will also need control flow such as loops and if-statements.
# Lastly, the % (modulo) operator may be useful:
#  (x % y) returns the remainder of x / y
#  from: https://docs.python.org/3/library/stdtypes.html#numeric-types-int-float-complex
def play_turn(player,snake1_index,snake2_index, move: list, board: list) -> tuple:

    # Make a copy of the board before anything else
    # This is important for minimax, so that different nodes do not share the same mutable data
    # Your code should NOT modify the original input board or else bugs may show up elsewhere
    board = np.array(board, copy=True)
    snake1_index = list(snake1_index)
    snake2_index = list(snake2_index)

    if player == 0:

        if(board[move[0],move[1]] == 0):
            head = snake1_index[0]
            snake1_index.insert(0,move)
            tail = snake1_index.pop()
            board[move[0],move[1]] = 2
            board[head[0],head[1]] = 1
            board[tail[0],tail[1]] = 0
        elif(board[move[0],move[1]] == 5):
            head = snake1_index[0]
            snake1_index.insert(0,move)
            board[move[0],move[1]] = 2
            board[head[0],head[1]] = 1
        elif(board[move[0],move[1]] == -5):
            head = snake1_index[0]
            if(len(snake1_index) == 2):
                snake1_index.insert(0,move)
                snake1_index.pop()
                snake1_index.pop()
                board[move[0],move[1]] = 2
                board[head[0],head[1]] = 0
            elif(len(snake1_index) == 1):
                snake1_index.pop()
                board[move[0],move[1]] = 0
                board[head[0],head[1]] = 0
            else:
                snake1_index.insert(0,move)
                tail1 = snake1_index.pop()
                tail2 = snake1_index.pop()
                board[move[0],move[1]] = 2
                board[head[0],head[1]] = 1
                board[tail1[0],tail1[1]] = 0
                board[tail2[0],tail2[1]] = 0



    if player == 1:

        if(board[move[0],move[1]] == 0):
            head = snake2_index[0]
            snake2_index.insert(0,move)
            tail = snake2_index.pop()
            board[move[0],move[1]] = 2
            board[head[0],head[1]] = 1
            board[tail[0],tail[1]] = 0
        elif(board[move[0],move[1]] == 5):
            head = snake2_index[0]
            snake2_index.insert(0,move)
            board[move[0],move[1]] = 2
            board[head[0],head[1]] = 1
        elif(board[move[0],move[1]] == -5):
            head = snake2_index[0]
            if(len(snake2_index) == 2):
                snake2_index.insert(0,move)
                snake2_index.pop()
                snake2_index.pop()
                board[move[0],move[1]] = 2
                board[head[0],head[1]] = 0
            elif(len(snake2_index) == 1):
                snake2_index.pop()
                board[move[0],move[1]] = 0
                board[head[0],head[1]] = 0
            else:
                snake2_index.insert(0,move)
                tail1 = snake2_index.pop()
                tail2 = snake2_index.pop()
                board[move[0],move[1]] = 2
                board[head[0],head[1]] = 1
                board[tail1[0],tail1[1]] = 0
                board[tail2[0],tail2[1]] = 0
    new_player = 1 - player

    new_state = (new_player, board,snake1_index,snake2_index)
    return new_state


# This one is done for you.
# Plays a turn and clears pits if needed.
def perform_action(action, state):
    player, board , snake1_index, snake2_index= state
    new_player, new_board , snake1_index, snake2_index = play_turn(player, snake1_index,snake2_index, action , board)
    return new_player, new_board

# TODO: implement score_in(state)
# state is a (player, board) tuple
# Return the score in the given state.
# The score is the number of gems in player 0's mancala, minus the number of gems in player 1's mancala.
def score_in(state: tuple) -> int:
    player, board , snake1_index, snake2_index= state
    score = len(snake1_index)
    return score # replace with your implementation

# TODO: implement is_tied(board)
# Return True if the game is tied in the given board state, False otherwise.
# A game is tied if both players have the same number of gems in their mancalas.
# You can assume all pits have already been cleared on the given board.
def is_tied(state) -> bool:
    player, board , snake1_index, snake2_index= state

    tied = ( len(snake1_index) == len(snake2_index) )
    return tied # replace with your implementation

# TODO: implement winner_of(board)
# Return the winning player (either 0 or 1) in the given board state.
# The winner is the player with more gems in their mancala.
# You can assume it is not a tied game, and all pits have already been cleared.
def winner_of(state) -> int:
    player, board , snake1_index, snake2_index= state

    if (len(snake1_index) > len(snake2_index)):
        return 0
    return 1 # replace with your implementation

# TODO: implement string_of(board)
# Return a string representation of the given board state for text-based game play.
# The string should have three indented lines of text.
# The first line shows the number of gems in player 1's pits,
# The second line shows the number of gems in each player's mancala,
# And the third line shows the number of gems in player 0's pits.
# The gem numbers should be padded and evenly spaced.
# For example, the string representation of the initial game state is:
#
#             5  5  5  5  5  5
#          0                    0
#             5  5  5  5  5  5
#
# Another example for a different game state with more gems is:
#
#            12 12 12 12 12 12
#          0                    0
#             5  5  5  5  5  5
#
# Excluding the leading comment symbols "# " above, all blank space should match exactly:
#   There are exactly 8 blank spaces before the left (padded) mancala number.
#   There is exactly 1 blank space between each (padded) pit number.
#   The returned string should start and end with new-line characters ("\n")

