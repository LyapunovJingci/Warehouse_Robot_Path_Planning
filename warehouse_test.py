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
from returnBrain1 import ReturnQLearningTable1
from returnBrain2 import ReturnQLearningTable2
from returnBrain3 import ReturnQLearningTable3
import matplotlib.pyplot as plt
import pickle
HUMANWALK1 = [1,1,1,1,3,3,1,1,1,2,2,2,2,2,1,1,1,2,2,2,2,2,1,1,1,1,1,1,2,2,2,2,2]
UNIT = 20

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
    for episode in range(300):
        # initial observation
        observation1, observation2, observation3 = env.resetRobot()
        nearbyEnvironment(observation1)
        #human1, human2 = env.resetHuman()
        #humanWalkHelper = 0
        while True:
            # fresh env
            env.render()
            '''
            if humanWalkHelper % 2 == 0:
                if humanWalkHelper/2 < len(HUMANWALK1):
                    env.humanStep1(HUMANWALK1[int(humanWalkHelper/2)])
                else:
                    env.humanStep1(4)
            else:
                env.humanStep1(4)
            humanWalkHelper +=1
            '''
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
                if done1 == 'arrive' and done2 == 'arrive' and done3 == 'arrive':
                    for i in range(50):
                        if startReturnTable (episode, observation1, ReturnRL1,1) == 'arrive':
                            break
                    for i in range(50): 
                        if startReturnTable (episode, observation2, ReturnRL2,2) == 'arrive':
                            break
                    for i in range(50): 
                        if startReturnTable (episode, observation3, ReturnRL3,3) == 'arrive': 
                            break

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
       
        # Train the map and dump into pickle
        '''
        if episode == 2500:     
            f1 = open('/Users/jingci/Desktop/RL/warehouseTest/WarehouseRobotPathPlanning-master/Return_q_table1.txt', 'wb')
            pickle.dump(RL1.q_table,f1)
            f1.close()
            f2 = open('/Users/jingci/Desktop/RL/warehouseTest/WarehouseRobotPathPlanning-master/Return_table2.txt', 'wb')
            pickle.dump(RL2.q_table,f2)
            f2.close()
            f3 = open('/Users/jingci/Desktop/RL/warehouseTest/WarehouseRobotPathPlanning-master/Return_table3.txt', 'wb')
            pickle.dump(RL3.q_table,f3)
            f3.close()
        '''
    '''
    f1 = open('/Users/jingci/Desktop/RL/warehouseTest/WarehouseRobotPathPlanning-master/Return_qtable1.txt', 'wb')
    pickle.dump(ReturnRL1.q_table,f1)
    f1.close()
    f2 = open('/Users/jingci/Desktop/RL/warehouseTest/WarehouseRobotPathPlanning-master/Return_qtable2.txt', 'wb')
    pickle.dump(ReturnRL2.q_table,f2)
    f2.close()
    f3 = open('/Users/jingci/Desktop/RL/warehouseTest/WarehouseRobotPathPlanning-master/Return_qtable3.txt', 'wb')
    pickle.dump(ReturnRL3.q_table,f3)
    f3.close()
    f4 = open('/Users/jingci/Desktop/RL/warehouseTest/WarehouseRobotPathPlanning-master/path_qtable1.txt', 'wb')
    pickle.dump(RL1.q_table,f4)
    f4.close()
    f5 = open('/Users/jingci/Desktop/RL/warehouseTest/WarehouseRobotPathPlanning-master/path_qtable2.txt', 'wb')
    pickle.dump(RL2.q_table,f5)
    f5.close()
    f6 = open('/Users/jingci/Desktop/RL/warehouseTest/WarehouseRobotPathPlanning-master/path_qtable3.txt', 'wb')
    pickle.dump(RL3.q_table,f6)
    f6.close()
    '''
    plot(rewardList1)
    plot(rewardList2)
    plot(rewardList3)   
    plot(totalRewardList)                    
    # end of game         
    print('game over')
    env.destroy()
    #print(rewardList)
    
def startReturnTable (episode, observation, RL, robotNumber):
    #observation1, observation2, observation3 = env.resetRobot()
    while True:
        env.render()
        action = chooseNoRandomAction(RL, observation)
        if robotNumber == 1:
            observation_, reward, done = env.returnStep1(action)
        elif robotNumber == 2:
            observation_, reward, done = env.returnStep2(action)
        elif robotNumber == 3:
            observation_, reward, done = env.returnStep3(action)
        learn (episode, RL, action, reward, observation, observation_)
        observation = observation_
        #print (done)
        if done == 'arrive' or done == 'hit':
            break
    return done

def chooseNoRandomAction(RL, observation):
    return RL.choose_action(str(observation),1)
      
def chooseAction (episode, RL, observation):
    if episode < -1:
        return RL.choose_action(str(observation), 0.9 + episode * 0.001)
    else:
        return RL.choose_action(str(observation),1)

def learn (episode, RL, action, reward, observation, observation_):
     if episode < 500:
         RL.learn(str(observation), action, reward, str(observation_), 0.03, 0.9)
     elif episode < 1500 and episode >= 500:
         RL.learn(str(observation), action, reward, str(observation_), 0.3-0.0002*(episode-500), 0.9)
     else:
         RL.learn(str(observation), action, reward, str(observation_), 0.001, 0.9)
 
def plot(reward):
    plt.style.use('seaborn-deep')
    plt.plot(reward,linewidth= 0.3)
    plt.title('Q Learning Total Reward')
    plt.xlabel('Trial')
    plt.ylabel('Reward')
    plt.show() 

def nearbyEnvironment(coordinate):
    left = [coordinate[0]-UNIT, coordinate[1], coordinate[2]-UNIT, coordinate[3]]
    right = [coordinate[0]+UNIT, coordinate[1], coordinate[2]+UNIT, coordinate[3]]
    up = [coordinate[0], coordinate[1]-UNIT, coordinate[2], coordinate[3]-UNIT]
    down = [coordinate[0], coordinate[1]+UNIT, coordinate[2], coordinate[3]+UNIT]
    upleft = [coordinate[0]-UNIT, coordinate[1]-UNIT, coordinate[2]-UNIT, coordinate[3]-UNIT]
    upright = [coordinate[0]+UNIT, coordinate[1]-UNIT, coordinate[2]+UNIT, coordinate[3]-UNIT]
    downleft = [coordinate[0]-UNIT, coordinate[1]+UNIT, coordinate[2]-UNIT, coordinate[3]+UNIT]
    downright = [coordinate[0]+UNIT, coordinate[1]+UNIT, coordinate[2]+UNIT, coordinate[3]+UNIT]
    nearby = [upleft, up, upright, left, right, downleft, down, downright]
    return nearby
    
if __name__ == "__main__":
    env = Maze()
    RL1 = QLearningTable1(actions=list(range(env.n_actions)))
    RL2 = QLearningTable2(actions=list(range(env.n_actions)))
    RL3 = QLearningTable3(actions=list(range(env.n_actions)))
    ReturnRL1 = ReturnQLearningTable1(actions=list(range(env.n_actions)))
    ReturnRL2 = ReturnQLearningTable2(actions=list(range(env.n_actions)))
    ReturnRL3 = ReturnQLearningTable3(actions=list(range(env.n_actions)))
    env.after(3000, update)
    env.mainloop()
