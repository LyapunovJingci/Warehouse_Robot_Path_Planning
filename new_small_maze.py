#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Mar 31 20:00:07 2020

@author: jingci
"""

import numpy as np
import time
import sys

if sys.version_info.major == 2:
    import Tkinter as tk
else:
    import tkinter as tk

UNIT = 20   # pixels
MAZE_H = 21  # grid height
MAZE_W = 21 # grid width

#shelf coordinates
X_Block_pic = [1,2,3,4,6,7,8,9,11,12,13,14,16,17,18,19]
X_Block = [element * UNIT for element in X_Block_pic]
Y_Block_pic = [5,6,8,9,11,12,14,15,17,18]
Y_Block = [element * UNIT for element in Y_Block_pic]

origin1 = np.array([50, 50])
origin2 = np.array([210,50])
origin3 = np.array([350,50])

class Maze(tk.Tk, object):
    def __init__(self):
        super(Maze, self).__init__()
        self.action_space = ['u', 'd', 'l', 'r','w']
        self.n_actions = len(self.action_space)
        self.title('Warehouse')
        self.geometry('{0}x{1}'.format(MAZE_H * UNIT, MAZE_H * UNIT))
        self._build_maze()

   
    def _build_maze(self):
        self.canvas = tk.Canvas(self, bg='white',
                           height=MAZE_H * UNIT,
                           width=MAZE_W * UNIT)

        # create grids
        for c in range(0, MAZE_W * UNIT, UNIT):
            x0, y0, x1, y1 = c, 0, c, MAZE_H * UNIT
            self.canvas.create_line(x0, y0, x1, y1)
        for r in range(0, MAZE_H * UNIT, UNIT):
            x0, y0, x1, y1 = 0, r, MAZE_W * UNIT, r
            self.canvas.create_line(x0, y0, x1, y1)
        # create operation desk 
        for i in range (1,16,7):
            self.canvas.create_rectangle(i*UNIT, 0, (i+5)*UNIT, 2*UNIT, fill = 'orange')
        
        # create shelf
        for k in range (1,17,5):
            for i in range (5,18,3):
                self.canvas.create_rectangle(k*UNIT, i*UNIT, (k+4)*UNIT,(i+2)*UNIT,fill='gray')

        # create target
        
        self.target1 = self.canvas.create_rectangle(
            4*UNIT,10*UNIT,5*UNIT,11*UNIT,
            fill='yellow')
        self.target2 = self.canvas.create_rectangle(
            7*UNIT,13*UNIT,8*UNIT,14*UNIT,
            fill='turquoise')
        self.target3 = self.canvas.create_rectangle(
            12*UNIT,10*UNIT,13*UNIT,11*UNIT,
            fill='tan')
          

        #create robot1
        self.rect1 = self.canvas.create_rectangle(
            origin1[0] - 10, origin1[1] - 10,
            origin1[0] + 10, origin1[1] + 10,
            fill='red')
        #create robot2
        self.rect2 = self.canvas.create_rectangle(
            origin2[0] - 10, origin2[1] - 10,
            origin2[0] + 10, origin2[1] + 10,
            fill='salmon')
        #create robot3
        self.rect3 = self.canvas.create_rectangle(
            origin3[0] - 10, origin3[1] - 10,
            origin3[0] + 10, origin3[1] + 10,
            fill='tomato' )
        # pack all
        self.canvas.pack()

    def resetRobot(self):
        self.update()
        time.sleep(0.01)
        self.canvas.delete(self.rect1)
        self.canvas.delete(self.rect2)
        self.canvas.delete(self.rect3)
        self.rect1 = self.canvas.create_rectangle(
            origin1[0] - 10, origin1[1] - 10,
            origin1[0] + 10, origin1[1] + 10,
            fill='red')
        self.rect2 = self.canvas.create_rectangle(
            origin2[0] - 10, origin2[1] - 10,
            origin2[0] + 10, origin2[1] + 10,
            fill='salmon')   
        self.rect3 = self.canvas.create_rectangle(
            origin3[0] - 10, origin3[1] - 10,
            origin3[0] + 10, origin3[1] + 10,
            fill='tomato' )
        return self.canvas.coords(self.rect1), self.canvas.coords(self.rect2), self.canvas.coords(self.rect3)
        

    def step1(self, action):
        s = self.canvas.coords(self.rect1)
        base_action = np.array([0, 0])
        if action == 0:   # up
            if s[1] > UNIT:
                base_action[1] -= UNIT
        elif action == 1:   # down
            if s[1] < (MAZE_H - 1) * UNIT:
                base_action[1] += UNIT
        elif action == 2:   # right
            if s[0] < (MAZE_W - 1) * UNIT:
                base_action[0] += UNIT
        elif action == 3:   # left
            if s[0] > UNIT:
                base_action[0] -= UNIT
        elif action == 4:   # wait
            base_action = np.array([0, 0])
        self.canvas.move(self.rect1, base_action[0], base_action[1])  # move agent
        s_ = self.canvas.coords(self.rect1)  # next state
      
        # reward function 
        
        if s_ == self.canvas.coords(self.target1):
            reward = 50
            done = 'arrive'
            s_ = 'terminal'   
        elif s_[0] == 0 or s_[1] < 40 or s_[2] >= MAZE_H * UNIT or s_[3] >= MAZE_W * UNIT:
            reward = -50
            done = 'hit'
            s_ = 'terminal'
        elif int(s_[0]) in X_Block and int(s_[1]) in Y_Block:
            reward = -50
            done = 'hit'
            s_ = 'terminal'
        else:
            reward = 0
            done = 'nothing'
              
        return s_, reward, done
    
    def step2(self, action):
        s = self.canvas.coords(self.rect2)
        base_action = np.array([0, 0])
        if action == 0:   # up
            if s[1] > UNIT:
                base_action[1] -= UNIT
        elif action == 1:   # down
            if s[1] < (MAZE_H - 1) * UNIT:
                base_action[1] += UNIT
        elif action == 2:   # right
            if s[0] < (MAZE_W - 1) * UNIT:
                base_action[0] += UNIT
        elif action == 3:   # left
            if s[0] > UNIT:
                base_action[0] -= UNIT
        elif action == 4:   # wait
            base_action = np.array([0, 0])
        self.canvas.move(self.rect2, base_action[0], base_action[1])  # move agent
        s_ = self.canvas.coords(self.rect2)  # next state
      
        # reward function      

        if s_ == self.canvas.coords(self.target2):
            reward = 50
            done = 'arrive'
            s_ = 'terminal'
        elif s_[0] == 0 or s_[1] < 40 or s_[2] >= MAZE_H * UNIT or s_[3] >= MAZE_W * UNIT:
            reward = -50
            done = 'hit'
            s_ = 'terminal'
        elif int(s_[0]) in X_Block and int(s_[1]) in Y_Block:
            reward = -50
            done = 'hit'
            s_ = 'terminal'
        else:
            reward = 0
            done = 'nothing'
     
        return s_, reward, done      

    def step3(self, action):
        s = self.canvas.coords(self.rect3)
        base_action = np.array([0, 0])
        if action == 0:   # up
            if s[1] > UNIT:
                base_action[1] -= UNIT
        elif action == 1:   # down
            if s[1] < (MAZE_H - 1) * UNIT:
                base_action[1] += UNIT
        elif action == 2:   # right
            if s[0] < (MAZE_W - 1) * UNIT:
                base_action[0] += UNIT
        elif action == 3:   # left
            if s[0] > UNIT:
                base_action[0] -= UNIT
        elif action == 4:   # wait
            base_action = np.array([0, 0])
        self.canvas.move(self.rect3, base_action[0], base_action[1])  # move agent
        s_ = self.canvas.coords(self.rect3)  # next state
      
        # reward function

        if s_ == self.canvas.coords(self.target3):
            reward = 50
            done = 'arrive'
            s_ = 'terminal'
        elif s_[0] == 0 or s_[1] < 40 or s_[2] >= MAZE_H * UNIT or s_[3] >= MAZE_W * UNIT:
            reward = -50
            done = 'hit'
            s_ = 'terminal'
        elif int(s_[0]) in X_Block and int(s_[1]) in Y_Block:
            reward = -50
            done = 'hit'
            s_ = 'terminal'
        else:
            reward = 0
            done = 'nothing'
          
        return s_, reward, done

    def render(self):
        time.sleep(0.01)
        self.update()

def update():
    for t in range(10):
        s1, s2 = env.resetRobot()
        while True:
            env.render()
                      
            s1,r1, done1 = env.step1(2)
            s2,r2,done2 = env.step2(1)
            
            if done1 == 'hit' and done2 == 'hit':
                break
            elif done1 == 'hit' and done2 == 'nothing':
                break
            elif done1 == 'arrive' and done2 == 'arrive':
                break
            elif s1 == s2:
                break

if __name__ == '__main__':
    env = Maze()
    env.after(2000, update)
    env.mainloop()