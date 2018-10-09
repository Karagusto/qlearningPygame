
"""
Created on Tue Oct  7 9:46:41 2018

@author: Ricardo Fragoso
"""

from random import random, randint
import numpy as np

#Classe para o estado
class StateCatcher:

    def __init__(self, state):
        self.vertical = int(state['fruit_y']) + 28
        self.horizontal = int(state['fruit_x']) - int(state['player_x']) + 64

    def __eq__(self, next_s):
        return self.vertical == next_s.vertical and self.horizontal == next_s.horizontal
    
    
#Classe para o agente    
class AgentCatcher:
    
    def __init__(self, set_of_actions, learning = 0.01, gamma = 0.5, loadFile = 0, name = ''):
        self.set_of_actions = set_of_actions
        self.learning = learning
        self.gamma = gamma
        
        if loadFile != 0:
            self.qtable = np.load(name + '.npy')
        else:
            self.qtable = np.zeros((3, 94, 128))
    
    #retorn a próxima ação escolhida do estado
    def get_action(self, state):
        state_now = StateCatcher(state)
        
        best_a = self.bestActionForState(state_now)
        
        if random() < self.learning:
            best_a = self.set_of_actions[randint(0, len(self.set_of_actions)-1)]
            
        return best_a    
    #Escolher a melhor ação dado um estado        
    def bestActionForState(self, state):
        best_s = None;
        best_a = None;
        best_re = None;
        
        for i in range(0, len(self.set_of_actions)):
            re = self.qtable[i, state.vertical, state.horizontal]
            
            if best_s is None or re>best_re:
                best_s = state
                best_a = self.set_of_actions[i]
                best_re = re
                
        return best_a
    
    
    #retorn o indice da ação dada
    def actionIndex(self, action):
        for i in range(0, len(self.set_of_actions)):
            if action == self.set_of_actions[i]:
                return i
        return None
    
    
    
    #atualiza os valores na tabela do qlearning básico
    def update_table(self, state, action, reward, next_state):
        state_now = StateCatcher(state)
        next_s = StateCatcher(next_state)
        
        action_i = self.actionIndex(action)
        next_a_i = self.actionIndex(self.bestActionForState(next_s))
        
        if action_i is None or next_a_i is None:
            raise Exception('Not valid action')
            
        now_qtable = self.qtable[action_i,state_now.vertical,state_now.horizontal]
        next_qtable = self.qtable[next_a_i,next_s.vertical, next_s.horizontal]
        expected_reward = reward + self.gamma*next_qtable
        self.qtable[action_i,state_now.vertical, state_now.horizontal] =  now_qtable + self.learning*(expected_reward - now_qtable)

    # salvar num numpy a tabela
    def saveTable(self, file):
        np.save(file + 'Catcher', self.qtable)









            
            
            
            
            
            
            
            
            
            
            
            