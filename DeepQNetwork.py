from Game import GameState
from tensorflow import keras
import tensorflow as tf
import numpy as np

class ReplayBuffer:
    def __init__(self,max_size,input_shape,n_actions):
        self.mem_size = max_size
        self.state_memory = np.zeros((self.mem_size,input_shape))
        self.new_state_memory = np.zeros((self.mem_size,input_shape))
        self.action_memory = np.zeros((self.mem_size,n_actions))
        self.reward_memory = np.zeros(self.mem_size)
        self.terminal_memory = np.zeros(np.mem_size,dtype=np.float32)
        self.mem_counter = 0

    def store_transition(self, state, action, reward, new_state, done):
        index = self.mem_counter % self.mem_size
        self.state_memory[index] = state
        self.new_state_memory[index] = new_state
        self.action_memory[index] = list(action)
        self.reward_memory[index] = reward
        self.terminal_memory[index] = 1 - int(done)

        self.mem_counter += 1

    def get_batch_sample(self, batch_size):
        size = min(self.mem_counter,self.mem_size)
        batch = np.random.choice(size,batch_size)
        sates = self.state_memory[batch]
        n_states = self.new_state_memory[batch]
        rewards = self.reward_memory[batch]
        terminals = self.terminal_memory[batch]
        actions = self.action_memory[batch]

        return states, n_states, actions, rewards, terminals



class DQNAgent:
    def __init__(self):
        self.model = create_model()
        self.target_model = create_model()

    def create_model():
        model = keras.Sequential()

        model.add(keras.layers.Dense(16,input_shape=(4,4),activation="relu"))
