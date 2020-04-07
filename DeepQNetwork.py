#!usr/bin/env python3
from tensorflow import keras
import numpy as np
import os

class ReplayBuffer:
    def __init__(self,max_size,input_shape,n_actions):
        self.mem_size = max_size
        self.state_memory = np.zeros((self.mem_size,input_shape))
        self.new_state_memory = np.zeros((self.mem_size,input_shape))
        self.action_memory = np.zeros((self.mem_size,n_actions))
        self.reward_memory = np.zeros(self.mem_size)
        self.terminal_memory = np.zeros(self.mem_size,dtype=np.float32)
        self.mem_counter = 0

    def store_transition(self, state, new_state,action, reward, done):
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
        states = self.state_memory[batch]
        n_states = self.new_state_memory[batch]
        rewards = self.reward_memory[batch]
        terminals = self.terminal_memory[batch]
        actions = self.action_memory[batch]

        return states, n_states, actions, rewards, terminals

class DQNAgent:
    def __init__(self, alpha, gamma, epsillon, batch_size,
                 input_dims, n_actions, epsillon_dec=0.99, epsillon_end=0.01,
                 fc_1=256, fc_2=256, mem_size=1000000,fname='DQN_model.h5'):
        self.action_space = [i for i in range(n_actions)]
        self.gamma = gamma
        self.epsillon = epsillon
        self.epsillon_dec = epsillon_dec
        self.epsillon_end = epsillon_end
        self.batch_size = batch_size
        self.model_file = fname
        self.model = load_model() if os.path.exists(fname) else self.create_model(alpha,fc_1,fc_2,input_dims,n_actions)
        self.memory = ReplayBuffer(mem_size,input_dims,n_actions)


    def create_model(self,alpha,fc_1,fc_2,input_dims,n_actions):
        model = keras.Sequential([
                        keras.layers.Dense(fc_1,input_shape=(input_dims,)),
                        keras.layers.Activation('relu'),
                        keras.layers.Dense(fc_2),
                        keras.layers.Activation('relu'),
                        keras.layers.Dense(n_actions)
        ])

        #(input_dims,) expects batch size here. As (input_dims, x)
        model.compile(optimizer=keras.optimizers.Adam(lr=alpha),loss='mse')
        return model

    def remember(self,state,new_state,action,reward,done):
        self.memory.store_transition(state,new_state,action,reward,done)

    def choose_action(self,state):
        state = state[np.newaxis, :] #Adds a new axis to the vector
        if np.random.random() < self.epsillon:
            actions = np.random.choice(self.action_space) #random actions
            action = [0 if i!=actions else 1 for i in range(len(self.action_space))]
        else:
            actions = self.model.predict(state)
            action = [0 if i!=np.argmax(actions) else 1 for i in range(len(self.action_space))]

        return action

    def learn(self):
        if self.memory.mem_counter < self.batch_size:
            return
        states, new_states, actions, rewards, done = \
                                self.memory.get_batch_sample(self.batch_size)

        action_values = np.array(self.action_space,dtype=np.int8)
        action_indices = np.dot(actions,action_values)

        q_eval = self.model.predict(states)
        q_next = self.model.predict(new_states)

        q_target = q_eval.copy()

        batch_index = np.arange(self.batch_size,dtype=np.int32)

        q_target[batch_index,action_indices] = rewards + self.gamma*np.max(q_next,axis=1)*done

        _ = self.model.fit(states, q_target, verbose=0)

        self.epsillon = self.epsillon*self.epsillon_dec if \
                        self.epsillon > self.epsillon_end else self.epsillon_end

    def save_model(self):
        self.model.save(self.model_file)

    def load_model(self):
        self.model = keras.models.load_model(self.model_file)
