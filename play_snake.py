from snake_helper import *
# from snake_minimax import minimax, simple_evaluate
import numpy as np
import random
def get_user_action(state):
    # print(valid_actions(state))
    # actions = list(map(str, valid_actions(state)))
    actions = valid_actions(state)
    player, board, snake1_index, snake2_index = state
    options = ["human","baseline AI","tree-based AI","tree+NN AI"]
    prompt = "Player %d, choose an option(%s): " % (player, ",".join(options))
    while True:
        option = input(prompt)
        if option in options:
            break
        print("Invalid option, try again.")
    if option == "human":
        prompt = "Player %d, choose an action (%s): " % (player, ",".join(actions))
        while True:
            action = input(prompt)
            # result = {}
            # result[action] = actions[action]
            if action in actions.keys(): return actions[action]
            print("Invalid action, try again.")
    if option == "baseline AI":
        actionlen = len(actions)
        choice = random.randint(0,actionlen-1)
        action = list(actions.keys())[choice]
        return actions[action]

if __name__ == "__main__":
    while True:
        board_size = input("please input board size (greater than 8): ")
        board_size = int(board_size)
        if board_size > 8 :
            break
        print("Invalid board size, try again.")
    state = initial_state(board_size)
    while not game_over(state):

        player, board, snake1_index, snake2_index= state
        print(board)
        if player == 0:
            action = get_user_action(state)
            state = perform_action(action, state)
        else:
            print("--- AI's turn --->")
            action = get_user_action(state)
            state = perform_action(action, state)

    player, board, snake1_index, snake2_index = state
    print(board)
    if is_tied(board):
        print("Game over, it is tied.")
    else:
        winner = winner_of(board)
        print("Game over, player %d wins." % winner)

