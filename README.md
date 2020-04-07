## Training an AI to play 2048

We build a game similar to 2048. Tiles have been custom made in Photoshop.
This game can be independently played by the user, without the neural network.
Just execute the Environment.py file.

I designed a Deep Q network to be trained to play the game. As input, the 4x4 game tiles will be fed to it as a flattened array.
Which passes through the fully connected layer of the DQN. We make decisions based on exploitation or exploration.

There are two fully connected layers in the DQN. The DQN class can also be used for other games/environments. To start training, execute Game.py
