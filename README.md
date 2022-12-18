AI Snake Game

In this study, there are two different fruits in addition to the food in a classic snake game. One (good fruit) increases the snake's body, while the other (bad fruit) decreases the snake's body. The aim of the game in this project, the snakes, is to avoid the bad fruits and to collect as many pieces of the good fruit as possible without hitting each other against walls and bodies. BFS algorithm is implemented for tree–based AI search algorithm. Reinforcement Learning is used as a machine learning model. As a learning algorithm, a feedforward neural network isimplemented.


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
