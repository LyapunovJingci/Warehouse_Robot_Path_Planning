#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jun 19 22:55:35 2020

@author: jingci
"""


import numpy as np
import pandas as pd
import pickle
from RLBrain import RLBrain

'''
Q-learning models for learning the position of target
'''
class QLearningTable1(RLBrain):
    def __init__(self, actions, state):
        self.actions = actions  # a list
        
        if state == "RAW": 
            #The q_table without previous knowledge
            self.q_table = pd.DataFrame(columns=self.actions, dtype=np.float64)
        elif state == "MAP":
            #The q_table after map training
            f = open(RLBrain.FILEPATH + 'q_table1.txt', 'rb')
            self.q_table = pickle.load(f)
            f.close()
        elif state == "PATH":
            #The q_table after path training
            f = open(RLBrain.FILEPATH + 'path_qtable1.txt', 'rb')
            self.q_table = pickle.load(f)
            f.close()

class QLearningTable2(RLBrain):
    def __init__(self, actions, state):
        self.actions = actions  # a list

        if state == "RAW": 
            #The q_table without previous knowledge
            self.q_table = pd.DataFrame(columns=self.actions, dtype=np.float64)
        elif state == "MAP":
            #The q_table after map training
            f = open(RLBrain.FILEPATH + 'q_table2.txt', 'rb')
            self.q_table = pickle.load(f)
            f.close()
        elif state == "PATH":
            #The q_table after path training
            f = open(RLBrain.FILEPATH + 'path_qtable2.txt', 'rb')
            self.q_table = pickle.load(f)
            f.close()

class QLearningTable3(RLBrain):
    def __init__(self, actions, state):
        self.actions = actions  # a list

        if state == "RAW": 
            #The q_table without previous knowledge
            self.q_table = pd.DataFrame(columns=self.actions, dtype=np.float64)
        elif state == "MAP":
            #The q_table after map training
            f = open(RLBrain.FILEPATH + 'q_table3.txt', 'rb')
            self.q_table = pickle.load(f)
            f.close()
        elif state == "PATH":
            #The q_table after path training
            f = open(RLBrain.FILEPATH + 'path_qtable3.txt', 'rb')
            self.q_table = pickle.load(f)
            f.close()
            
'''
Q-learning models for learning the position of starting point
'''            
class ReturnQLearningTable1(RLBrain):
    def __init__(self, actions, state):
        self.actions = actions  # a list
        if state == "RAW": 
            #The q_table without previous knowledge
            self.q_table = pd.DataFrame(columns=self.actions, dtype=np.float64)
        elif state == "MAP":
            #The q_table after map training
            f = open(RLBrain.FILEPATH + 'Return_q_table1.txt', 'rb')
            self.q_table = pickle.load(f)
            f.close()
        elif state == "PATH":
            #The q_table after path training
            f = open(RLBrain.FILEPATH + 'Return_q_table1.txt', 'rb')
            self.q_table = pickle.load(f)
            f.close()

class ReturnQLearningTable2(RLBrain):
    def __init__(self, actions, state):
        self.actions = actions  # a list
        if state == "RAW": 
            #The q_table without previous knowledge
            self.q_table = pd.DataFrame(columns=self.actions, dtype=np.float64)
        elif state == "MAP":
            #The q_table after map training
            f = open(RLBrain.FILEPATH + 'Return_table2.txt', 'rb')
            self.q_table = pickle.load(f)
            f.close()
        elif state == "PATH":
            #The q_table after path training
            f = open(RLBrain.FILEPATH + 'Return_qtable2.txt', 'rb')
            self.q_table = pickle.load(f)
            f.close()

class ReturnQLearningTable3(RLBrain):
    def __init__(self, actions, state):
        self.actions = actions  # a list
        if state == "RAW": 
            #The q_table without previous knowledge
            self.q_table = pd.DataFrame(columns=self.actions, dtype=np.float64)
        elif state == "MAP":
            #The q_table after map training
            f = open(RLBrain.FILEPATH + 'Return_table3.txt', 'rb')
            self.q_table = pickle.load(f)
            f.close()
        elif state == "PATH":
            f = open(RLBrain.FILEPATH + 'Return_qtable3.txt', 'rb')
            self.q_table = pickle.load(f)
            f.close()
