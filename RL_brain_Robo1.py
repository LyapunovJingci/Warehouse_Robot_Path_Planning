#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Mar 30 19:57:20 2020

@author: jingci
"""

import numpy as np
import pandas as pd
import pickle
from RLBrain import RLBrain

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
