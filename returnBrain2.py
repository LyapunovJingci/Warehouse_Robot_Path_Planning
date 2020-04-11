#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Apr 10 14:30:40 2020

@author: jingci
"""

import numpy as np
import pandas as pd
import pickle

class ReturnQLearningTable2:
    def __init__(self, actions, learning_rate=0.2, reward_decay=0.9, e_greedy=0.8):
        self.actions = actions  # a list
        self.lr = learning_rate
        self.gamma = reward_decay
        self.epsilon = e_greedy
        #f = open('/Users/jingci/Desktop/RL/warehouseTest/WarehouseRobotPathPlanning-master/Return_table2.txt', 'rb')
        #self.q_table = pd.DataFrame(columns=self.actions, dtype=np.float64)
        f = open('/Users/jingci/Desktop/RL/warehouseTest/WarehouseRobotPathPlanning-master/Return_qtable2.txt', 'rb')
        self.q_table = pickle.load(f)
        f.close()

    def choose_action(self, observation, epsilon):
        self.check_state_exist(observation)
        # action selection
        if np.random.uniform() < epsilon:
            # choose best action
            state_action = self.q_table.loc[observation, :]
            # some actions may have the same value, randomly choose on in these actions
            action = np.random.choice(state_action[state_action == np.max(state_action)].index)
        else:
            # choose random action
            action = np.random.choice(self.actions)
        return action

    def learn(self, s, a, r, s_, alpha, gamma):
        self.check_state_exist(s_)
        q_predict = self.q_table.loc[s, a]
        if s_ != 'terminal':
            q_target = r + gamma * self.q_table.loc[s_, :].max()  # next state is not terminal
        else:
            q_target = r  # next state is terminal
        self.q_table.loc[s, a] += alpha * (q_target - q_predict)  # update
        #print (self.q_table)

    def check_state_exist(self, state):
        if state not in self.q_table.index:
            # append new state to q table
            self.q_table = self.q_table.append(
                pd.Series(
                    [0]*len(self.actions),
                    index=self.q_table.columns,
                    name=state,
                )
            )

