AI Snake Game

The snake can move in four directions (up, down, right, and left) as in a classic snake game. The aim of the snake game is to control the snake by the player to collect the food on the game board and make the snake as big as possible. The game is over when the snake dies. The snake dies in one of two situations: when it hits its head against the wall or against its own body. 

In the snake game developed in this project, instead of a snake controlled by a single player, there are two snakes controlled by two players that one of both is human and the other is AI. There are two types of food in the game. One (good fruit) increases the snake's size by 1, while the other (bad fruit) decreases the snake's size by 1. There are always these fruits in pair on the game board and as soon as the snake eats one of the related fruits, a new pair of fruits again are produced. The final score of the game depends on the total number of fruits eaten by the snake. Each time when the snake eats the fruit that longens it, the score increases by 1, and when it eats the fruit that shortens it, the score decreases by 1. AI and human will compete at every step for food that will grow their own snake. 

In summary, the aim of the game in this project, the snakes to avoid the bad fruits and to collect as many pieces of the good fruits as possible without hitting each other against walls and bodies. AI will try to advance in the game through algorithms and training and get high scores.


A* search [1]

The A* algorithm depends on the heuristic distance from the head of the snake to the good fruit and cost of the path.

f(n)=g(n)+h(n)

where n is the good fruit on the board, g(n) is the cost of the path from the head of the snake to goof fruit, and h(n) represents the heuristic distance. 

The algorithm checks the path information until the head of snake reaches good fruit and stops working when the target is reached. Thus, when the fruit on the game board is updated, it again calculates a minimum cost for the distance between the head of the snake and the new location of the good fruit.


Deep Reinforcement Learning with PyTorch and Pygame [2]


References

[1] Shubham Sharma, Saurabh Mishra, Nachiket Deodhar, Akshay Katageri, and Parth Sagar. Solving the classic snake game using ai. In2019 IEEE Pune Section International Conference (PuneCon), pages 1–4. IEEE,2019.

[2] https://www.youtube.com/playlist?list=PLqnslRFeH2UrDh7vUmJ60YrmWd64mTTKV

States:
Food is above the snake
Food is on the right of the snake
Food is below the snake
Food is on the left of the snake
Obstacle(wall&tail) directly above the snake
Obstacle directly on the right
Obstacle directly below the snake
Obstacle directly on the left
Snake direction == up
Snake direction == right
Snake direction == down
Snake direction == left
Two types of fruits: 
One fruit makes the snake get longer && increase the score of the player who eats the food
Another fruit makes it get shorter (removes the last piece of the tail) && decreases the score of the player who eats the food
