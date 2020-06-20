#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Mar 31 21:22:27 2020

@author: jingci
"""

import numpy as np
import pandas as pd
import pickle
from RLBrain import RLBrain

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

