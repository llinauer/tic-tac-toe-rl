# tic-tac-toe-rl

This project was heavily (not to say, solely) influenced by this blog entry: https://towardsdatascience.com/reinforcement-learning-implement-tictactoe-189582bea542
of Jeremy Zhang. The original code can be found here: https://github.com/MJeremy2017/reinforcement-learning-implementation/tree/master/TicTacToe
So please give credit to him.

What I wanted to achieve with this project is:

1) Re-create it and learn
2) Add my own touch to it
3) Create a tutorial in german, for all my german-speaking fellows (the german version is currently in development).

So there you have it. Now, let's get started.

# Pre-requisites

This project uses python 3 and the following modules:
* tkinter
* pickle
* numpy
* game

Please make sure that you have installed all the pre-requisites before running.

# Tic Tac Toe with Reinformcement Learning

Before you can start, let me give you a quick introduction in Reinforcement Learning. The emphasis is on quick. This shall serve merely as a high-level overview and will not go into mathematical detail.
If you are interested in the (very awesome) topic of Reinforcement Learning, I suggest you look into this book Reinforcement Learning: An Introduction by Richard Sutton and Andrew Barto
At the time of writing, the book is available for free at: http://incompleteideas.net/book/the-book.html

Tic Tac Toe is a very easy game. Very very easy. That's why it is well suited for an implementation with Reinforcement Learning.
Reinforcement Learning is a subfield of Machine Learning, where an agent learns to take actions in an environment by interacting with it and 
receiving rewards. So far for the definition.

How can we picture this in the case of Tic Tac Toe?
The agent (player) can take actions (draw Xs and Os) in the environment (the board). It receives a reward for winning the game and gets a penalty (= negative reward) for loosing. A draw will result in a small yet non-zero reward, since the agent did some things right and at least not loose.
The agent wants to maximize its reward and will therefore take actions that will lead it to a win or if not possible, at least a draw.
Now, how can this be achieved in practice? 

The agent has a set of possible actions it can take at every turn. Consider the board state below:

![X_turn](https://user-images.githubusercontent.com/85884720/123281669-2a3d9400-d50a-11eb-8b42-4552311ec2ea.png "Player Xs turn")

It's Xs turn and he has five possible fields where to put his sign. However, if he does not put the X in the top left corner, player O has won.
So there are better and worse turns, but how does the agent know the utility of a turn? A way to do this is by keeping a table with a value for
each possible game configuration. If the agent has such a table, than it simply chooses the action that leads to the state with the highest value.
We can construct this lookup table by making use of Reinforcement Learning.

Before the learning process, we fill up the table with zeros. This represents the total lack of knowledge of the individual configurations utilities.
Start of the first game. Player X starts and puts his X somewhere on the board. The agents turn. It has eight possible actions to take corresponding to the eight remaining fields. However, since every action leads to a configuration with value 0 (remember, all board configurations in the lookup table are assigned a zero as of yet), so the best it can do is choose an action randomly. The agent thus puts its sign in one of the remaining eight fields at random, but it remembers where. The same situation will appear at the agents next turn. As the game progresses, the random acting agent won't stand much chance against an even minimally talented Tic Tac Toe player and so it looses and receives a negative reward. 

Now comes the crucial part. The agent can learn from this frustrating experience of losing, by decreasing the value of those configurations, that lead to the loss. It remembered all actions it took during the course of the game and all board configurations that resulted from those actions. The agent goes through all the configurations in reverse order and updates their values according to the formula:

![update_value](https://user-images.githubusercontent.com/85884720/123281558-12fea680-d50a-11eb-806a-25b0ecc51923.png "Formula for updating the values of board configurations")


The formula may look complicated, but it's actually quite simple. You can think of it this way.
The new value of a board configuration is equal to the old value plus the difference of the value of the next configuration and the current configuration times a constant alpha. To make it even clearer, let's look at what happens after the game described above.

![update_after_loss](https://user-images.githubusercontent.com/85884720/123281736-37f31980-d50a-11eb-8913-b67c36597d1b.png "The agent updates the values for the board states it experienced during the game")

The agent has lost the game and receives a negative reward. It fetches the last board configuration from the list and calculates the new value according to the formula. The only thing here is, there is no following configuration to the last configuration. So instead, it uses the reward as the value V(next config). Then, it takes the second to last board configuration and calculates its new value. Here V(next config) is the updated value of the last board configuration.
And so on and so forth. All the board configurations the agent saw in during that game, will now have updated values. And since the game was lost, the values have decreased. In following games, actions that will lead to these configurations will less likely be chosen, since the values are now actually less than zero.

The exact same would happen if the agent wins a game. The only difference is that the reward is now positive and the values of board configurations that lead to the win will be increased. In the case of a draw, the reward is positive yet small, so the values will only change slightly.

A word on the parameter alpha. Alpha is called the learning rate of the agent and determines in a way how "fast" the agent learns. You may say that faster learning is better, because if you learn faster than know things sooner. However, in Reinforcement Learning this is not the case. When alpha is too high, the agent over- or underestimates the values of certain board configurations. This will cause the agent to avoid those configurations in the future. However, it may be the case that the configurations are actually better than the agent thought they would be. By keeping the learning rate lower, the values will only be in- or decreased slightly, making the agent less volatile.

Now, we have all the knowledge needed.

There is actually much more to it and you can look into the code itself to see how the mathematics works.
Feel free to tweak the parameters and see if you can improve the learning.

# Training the agent

You can train the Tic Tac Toe agent by running:

`python tic_tac_toe.py --train --n <number>`


The agent will play `<number>` games against itself, updating the values of board configurations as explained above and save the results in two files called policy_X and policy_O. These are the lookup tables for players X and O stored (pickled) as binary files.

Depending on the hardware you are running the program on and the number of games the agent should play against itself, the training may take some time.
Be sure to test the training with a lower `<number>` (e.g. 100) before really pushing the agent.

# Playing against the agent

You can now test the intelligence of the agent by actually playing against it.
Run: 

`python tic_tac_toe.py --play`

You are the X player and you will go first. Depending on the number of games you let the agent train, it may surprise you how good it actually can play. However,  don't expect too much from it. Just experiment with it a little and let it win sometimes, so it won't get discouraged (JK).

Have fun!

# German version in the making


