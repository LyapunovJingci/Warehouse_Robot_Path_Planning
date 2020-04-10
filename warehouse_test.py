#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Mar 31 21:14:11 2020

@author: jingci
"""

from new_small_maze import Maze
from RL_brain_Robo1 import QLearningTable1
from RL_brain_Robo2 import QLearningTable2
from RL_brain_Robo3 import QLearningTable3
import matplotlib.pyplot as plt
import pickle

def update():
    totalReward1 = 0
    totalReward2 = 0
    totalReward3 = 0
    rewardList1 = []
    rewardList2 = []
    rewardList3 = []
    totalRewardList = []

    freeze1 = False
    freeze2 = False
    freeze3 = False
    for episode in range(3000):
        # initial observation
        observation1, observation2, observation3 = env.resetRobot()
        
        while True:
            # fresh env
            env.render()
            
            # RL choose action based on observation
            if freeze1:
                action1 = 4
            else:
                # Choose action
                action1 = chooseAction(episode, RL1, observation1)   
                # RL take action and get next observation and reward                
                observation1_, reward1, done1 = env.step1(action1)
                totalReward1+=reward1
                # RL learn from this transition
                learn (episode, RL1, action1, reward1, observation1, observation1_)

                # swap observation
                observation1 = observation1_
            
            if freeze2:
                action2 = 4
            else:                
                # Choose action
                action2 = chooseAction(episode, RL2, observation2)        
                # RL take action and get next observation and reward                
                observation2_, reward2, done2 = env.step2(action2)
                totalReward2+=reward2
                # RL learn from this transition
                learn (episode, RL2, action2, reward2, observation2, observation2_)

                # swap observation
                observation2 = observation2_
            
            if freeze3:
                action3 = 4
            else:
                # Choose action
                action3 = chooseAction(episode, RL3, observation3) 
                # RL take action and get next observation and reward         
                observation3_, reward3, done3 = env.step3(action3)
                totalReward3+=reward3
                # RL learn from this transition
                learn (episode, RL3, action3, reward3, observation3, observation3_)

                # swap observation
                observation3 = observation3_
            
            # break while loop when end of this episode
                
            if (done1 == 'hit' or done1 == 'arrive') and (done2 == 'hit' or done2 == 'arrive') and (done3 == 'hit' or done3 == 'arrive'):
                print (episode, 'trial: ','Robot1: ', totalReward1, '; Robot2: ', totalReward2, '; Robot3: ', totalReward3)
                #print (freeze1, freeze2, freeze3)
                rewardList1.append(totalReward1)
                rewardList2.append(totalReward2)
                rewardList3.append(totalReward3)
                totalRewardList.append(totalReward1+totalReward2+totalReward3)
                totalReward1 = 0
                totalReward2 = 0
                totalReward3 = 0
                freeze1 = False
                freeze2 = False
                freeze3 = False
                break
            if done1 == 'hit' or done1 == 'arrive':
                freeze1 = True
            if done2 == 'hit' or done2 == 'arrive':
                freeze2 = True
            if done3 == 'hit' or done3 == 'arrive':
                freeze3 = True
        
        if episode == 2500:     
            f1 = open('/Users/jingci/Desktop/RL/warehouseTest/WarehouseRobotPathPlanning-master/q_table1.txt', 'wb')
            pickle.dump(RL1.q_table,f1)
            f1.close()
            f2 = open('/Users/jingci/Desktop/RL/warehouseTest/WarehouseRobotPathPlanning-master/q_table2.txt', 'wb')
            pickle.dump(RL2.q_table,f2)
            f2.close()
            f3 = open('/Users/jingci/Desktop/RL/warehouseTest/WarehouseRobotPathPlanning-master/q_table3.txt', 'wb')
            pickle.dump(RL3.q_table,f3)
            f3.close()
        
            '''
            with open('/Users/jingci/Desktop/RL/warehouseTest/WarehouseRobotPathPlanning-master/q_table1.csv', 'wt') as f1:
                print (RL1.q_table, file=f1)    
            with open('/Users/jingci/Desktop/RL/warehouseTest/WarehouseRobotPathPlanning-master/q_table2.csv', 'wt') as f2:
                print (RL2.q_table, file=f2)  
            with open('/Users/jingci/Desktop/RL/warehouseTest/WarehouseRobotPathPlanning-master/q_table3.csv', 'wt') as f3:
                print (RL3.q_table, file=f3)
            '''
    plot(rewardList1)
    plot(rewardList2)
    plot(rewardList3)   
    plot(totalRewardList)                    
    # end of game         
    print('game over')
    env.destroy()
    #print(rewardList)
    
 
    
def chooseAction (episode, RL, observation):
    if episode < 200:
        return RL.choose_action(str(observation), 0.8+episode*0.01)
    else:
        return RL.choose_action(str(observation),1)
    '''
    if episode < 1000:
        return RL.choose_action(str(observation),0.0009*episode)
    elif episode < 2500 and episode >= 1000:
        return RL.choose_action(str(observation),0.9+(episode-1000)*0.00006)
    else:
        return RL.choose_action(str(observation),1)
    '''
def learn (episode, RL, action, reward, observation, observation_):
     if episode < 500:
         RL.learn(str(observation), action, reward, str(observation_), 0.3, 0.9)
     elif episode < 1500 and episode >= 500:
         RL.learn(str(observation), action, reward, str(observation_), 0.3-0.0002*(episode-500), 0.9)
     else:
         RL.learn(str(observation), action, reward, str(observation_), 0.001, 0.9)
    
def plot (reward):
    plt.style.use('seaborn-deep')
    plt.plot(reward,linewidth= 0.3)
    plt.title('Q Learning Total Reward')
    plt.xlabel('Trial')
    plt.ylabel('Reward')
    plt.show() 
    
if __name__ == "__main__":
    env = Maze()
    RL1 = QLearningTable1(actions=list(range(env.n_actions)))
    RL2 = QLearningTable2(actions=list(range(env.n_actions)))
    RL3 = QLearningTable3(actions=list(range(env.n_actions)))
    env.after(3000, update)
    env.mainloop()
