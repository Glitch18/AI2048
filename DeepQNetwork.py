from Game import GameState
from tensorflow import keras
import tensorflow as tf

class DQNAgent:
    def __init__(self):
        self.model = create_model()
        self.target_model = create_model()

    def create_model():
        model = keras.Sequential()

        model.add(keras.layers.Dense(16,input_shape=(4,4),activation="relu"))
        
