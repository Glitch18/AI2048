from DeepQNetwork import DQNAgent
from Environment import GameState
from utils import plotLearning
import numpy as np

if(__name__=="__main__"):
    env = GameState()
    n_games = 20
    agent = DQNAgent(alpha=0.005,gamma=0.99,epsillon=1.0,batch_size=64,input_dims=16,n_actions=4)

    scores = []
    epi_history = []

    for i in range(n_games):
        observation = env.reset()
        score=0
        done = False

        while not done:
            action = agent.choose_action(observation)
            observation_,reward,done = env.frame_step(action)
            score += reward
            agent.remember(observation,observation_,action,reward,done)
            observation = observation_
            agent.learn()

        epi_history.append(agent.epsillon)
        scores.append(score)

        avg_score = np.mean(scores[max(0,i-20):(i+1)])

        print('episode ',i,'score %.2f'%score,' average score %.2f'%avg_score)

        if i%10==0:
            agent.save_model()

    filename = 'DQN_LearningPlot.png'
    x = [i+1 for i in range(n_games)]
    plotLearning(x,scores,epi_history,filename)
    print("DONE")
