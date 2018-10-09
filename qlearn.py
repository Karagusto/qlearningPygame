"""
Created on Tue Oct  8 14:57:44 2018

@author: Ricardo Fragoso
"""

import os
from PyGameLearningEnvironment.ple.games import Catcher
from PyGameLearningEnvironment.ple import PLE
from myCatcherAgent import AgentCatcher

#inicializa o jogo
gameON = True

if not gameON:
    os.putenv('SDL_VIDEODRIVER', 'fbcon')
    os.environ["SDL_VIDEODRIVER"] = "dummy"


py_game = Catcher()
c = PLE(py_game, fps=30, display_screen=gameON, force_fps=not gameON)
c.init()
theAgent = AgentCatcher(c.getActionSet(), loadFile=True, name='qtable')

frames = 10000
initial_reward = 0
initial_score = 0
reward = 0.0
k = 1
score = 0
total = 0

try: 
    for i in range(30000):
        k += 1
        total = 0
        for i in range(frames):
            if c.game_over():
                c.reset_game()
                
            current_state = py_game.getGameState()
            this_action = theAgent.get_action(current_state)
            reward = c.act(this_action)
            score = py_game.getScore()
            
            initial_score = score
            initial_reward = reward
            
            next_s = py_game.getGameState()
            #primeiro update da tabela 
            theAgent.update_table(current_state,this_action,reward,next_s)
    theAgent.saveTable('qtable')
    
    theAgent = AgentCatcher(c.getActionSet(), loadFile=True, name='qtable', gamma = 0.85, learning=0)
    total = 0
    for f in range(frames):
        if c.game_over():
            c.reset_game()
            
            current_state = py_game.getGameState()
            this_action = theAgent.get_action(current_state)
            reward = c.act(this_action)
            total += reward
            score = py_game.getScore()
            initial_score = score
            initial_reward = reward
            next_s = py_game.getGameState
            # segundo update pegando a soma de recursos
            theAgent.update_table(current_state, this_action, reward, next_s)
            print('Reward = '+total)
finally:
    theAgent.saveTable('qtable')
    
    
   





































