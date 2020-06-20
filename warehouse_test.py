#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Mar 31 21:14:11 2020

@author: jingci
"""

from new_small_maze import Maze
from QTables import QLearningTable1
from QTables import QLearningTable2
from QTables import QLearningTable3
from QTables import ReturnQLearningTable1
from QTables import ReturnQLearningTable2
from QTables import ReturnQLearningTable3
import matplotlib.pyplot as plt
import pickle
'''
Add the possible human walking path here 
UP: 0
DOWN: 1
RIGHT: 2
LEFT: 3
WAIT: 4
'''
HUMANWALK1 = [4,4,4,4,4,4,4,4]
UNIT = 20
STATE0 = "RAW"
STATE1 = "MAP"
STATE2 = "PATH"
'''
Define the current state here
Different states relate to different pre-trained q table
'''
CURRENTSTATE = STATE2
'''
True, if using the data of this trial for future training
False, if just testing
'''
RECORDDATA = False

'''
Before running the code, please modify this file path as needed
'''
FILEPATH = "/Users/jingci/Desktop/RL/warehouseTest/WarehouseRobotPathPlanning-master/"


def update():
    totalReward1 = 0
    totalReward2 = 0
    totalReward3 = 0
    rewardList1 = []
    rewardList2 = []
    rewardList3 = []
    totalRewardList = []
    #check whether the agent is available to move
    freeze1 = False
    freeze2 = False
    freeze3 = False
    #check whether facing fixed obstacles
    backup1 = False
    backup2 = False
    backup3 = False
    for episode in range(300):
        # initial observation
        observation1, observation2, observation3 = env.resetRobot()
        #nearbyEnvironment(observation1)
        human1, human2 = env.resetHuman()
        humanWalkHelper = 0
        wait_time1 = 0
        wait_time2 = 0
        wait_time3 = 0
        while True:
            # fresh env
            env.render()
            
            # simulation of human walking
            human1 = humanWalk(humanWalkHelper)
            humanWalkHelper +=1

            # RL choose action based on observation
            if freeze1:
                action1 = 4
            else:
                # Choose action
                if not backup1:
                    action1 = chooseAction(episode, RL1, observation1)   
                    if stateChecking(human1, observation1, action1) == 'no_collision':
                        observation1_, reward1, done1 = env.step1(action1)
                    else:
                        if wait_time1 > 5:
                            chooseActionForRobots(stateChecking(human1, observation1, action1), 
                                         observation1_, reward1, done1, "robot1")
                            backup1 = True
                            wait_time1 = 0
                        else:
                            observation1_, reward1, done1 = env.step1(4)
                            wait_time1 +=1 
                    learn (episode, RL1, action1, reward1, observation1, observation1_)
                else:
                    action1 = chooseAction(episode, backupRL1, observation1)
                    observation1_, reward1, done1 = env.step1(action1, human1)
                    learn (episode, backupRL1, action1, reward1, observation1, observation1_)      
                    
                totalReward1+=reward1
                observation1 = observation1_
            
            if freeze2:
                action2 = 4
            else:
                # Choose action
                if not backup2:
                    action2 = chooseAction(episode, RL2, observation2)   
                    if stateChecking(human1, observation2, action2) == 'no_collision':
                        observation2_, reward2, done2 = env.step2(action2)
                    else:
                        if wait_time2 > 5:
                            chooseActionForRobots(stateChecking(human1, observation2, action2), 
                                          observation2_, reward2, done2, "robot2")
                            backup2 = True
                            wait_time2 = 0
                        else:
                            observation2_, reward2, done2 = env.step2(4)
                            wait_time2 +=1 
                    learn (episode, RL2, action2, reward2, observation2, observation2_)
                else:
                    action2 = chooseAction(episode, backupRL2, observation2)
                    observation2_, reward2, done2 = env.step2(action2, human1)
                    learn (episode, backupRL2, action2, reward2, observation2, observation2_)      
                    
                totalReward2+=reward2

                # swap observation
                observation2 = observation2_
                
            if freeze3:
                action3 = 4
            else:
                # Choose action
                action3 = chooseAction(episode, RL3, observation3) 
                collisionType = ['upward_collision','downward_collision','left_collision','right_collision']
                # RL take action and get next observation and reward         
                if (stateChecking(observation1, observation3, action3) == 'no_collision'
                    and stateChecking(observation2, observation3, action3) == 'no_collision'):
                    observation3_, reward3, done3 = env.step3(action3) 
                    wait_time3 = 0
                elif (stateChecking(observation1, observation3, action3) in collisionType
                    or stateChecking(observation1, observation3, action3) in collisionType):
                    observation3_, reward3, done3 = env.step3(4)
                    wait_time3 += 1
                else:
                    observation3_, reward3, done3 = env.step3(action3)
                    wait_time3 = 0
                    
                totalReward3+=reward3
                # RL learn from this transition
                learn (episode, RL3, action3, reward3, observation3, observation3_)

                # swap observation
                observation3 = observation3_
            
            # break while loop when end of this episode
                
            if (done1 == 'hit' or done1 == 'arrive') and (done2 == 'hit' or done2 == 'arrive') and (done3 == 'hit' or done3 == 'arrive'):
                print (episode, 'trial: ','Robot1: ', totalReward1, '; Robot2: ', totalReward2, '; Robot3: ', totalReward3)
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
    if RECORDDATA:
        f1 = open(FILEPATH + 'Return_qtable1.txt', 'wb');
        pickle.dump(ReturnRL1.q_table,f1)
        f1.close()
        f2 = open(FILEPATH + 'Return_qtable2.txt', 'wb');
        pickle.dump(ReturnRL2.q_table,f2)
        f2.close()
        f3 = open(FILEPATH + 'Return_qtable3.txt', 'wb');
        pickle.dump(ReturnRL3.q_table,f3)
        f3.close()
        f4 = open(FILEPATH + 'path_qtable1.txt', 'wb');
        pickle.dump(RL1.q_table,f4)
        f4.close()
        f5 = open(FILEPATH + 'path_qtable2.txt', 'wb');
        pickle.dump(RL2.q_table,f5)
        f5.close()
        f6 = open(FILEPATH + 'path_qtable3.txt', 'wb');
        pickle.dump(RL3.q_table,f6)
        f6.close()

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

def chooseActionForRobots(state, observation, reward, done, robot):

    if (robot == "robot1"):
        if state == 'upward_collision':
            observation, reward, done = env.step1(1)
        elif state == 'downward_collision':
            observation, reward, done = env.step1(0)
        elif state == 'left_collision':
            observation, reward, done = env.step1(2)
        elif state == 'right_collision':
            observation, reward, done = env.step1(3)  

    if (robot == "robot2"):
        if state == 'upward_collision':
            observation, reward, done = env.step2(1)
        elif state == 'downward_collision':
            observation, reward, done = env.step2(0)
        elif state == 'left_collision':
            observation, reward, done = env.step2(2)
        elif state == 'right_collision':
            observation, reward, done = env.step2(3)  

    if (robot == "robot3"):
        if state == 'upward_collision':
            observation, reward, done = env.step3(1)
        elif state == 'downward_collision':
            observation, reward, done = env.step3(0)
        elif state == 'left_collision':
            observation, reward, done = env.step3(2)
        elif state == 'right_collision':
            observation, reward, done = env.step3(3)  

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
    
def stateChecking(alien_agent, key_agent, action):
    directEnvironment = directNearbyEnvironment(key_agent)

    indirectEnvironment = indirectNearbyEnvironment(key_agent)
    if action == 0 and (alien_agent in [directEnvironment[0], indirectEnvironment[0], indirectEnvironment[1]]):
            return 'upward_collision'
    elif action == 1 and (alien_agent in [directEnvironment[1], indirectEnvironment[2], indirectEnvironment[3]]):
            return 'downward_collision'
    elif action == 2 and (alien_agent in [directEnvironment[3], indirectEnvironment[1], indirectEnvironment[3]]):
            return 'right_collision'
    elif action == 3 and (alien_agent in [directEnvironment[2], indirectEnvironment[0], indirectEnvironment[2]]):
            return 'left_collision'
    else:
        return 'no_collision'

def indirectNearbyEnvironment(coordinate):
    upleft = [coordinate[0]-UNIT, coordinate[1]-UNIT, coordinate[2]-UNIT, coordinate[3]-UNIT]
    upright = [coordinate[0]+UNIT, coordinate[1]-UNIT, coordinate[2]+UNIT, coordinate[3]-UNIT]
    downleft = [coordinate[0]-UNIT, coordinate[1]+UNIT, coordinate[2]-UNIT, coordinate[3]+UNIT]
    downright = [coordinate[0]+UNIT, coordinate[1]+UNIT, coordinate[2]+UNIT, coordinate[3]+UNIT]
    nearby = [upleft, upright, downleft, downright]
    return nearby

def directNearbyEnvironment(coordinate):
    left = [coordinate[0]-UNIT, coordinate[1], coordinate[2]-UNIT, coordinate[3]]
    right = [coordinate[0]+UNIT, coordinate[1], coordinate[2]+UNIT, coordinate[3]]
    up = [coordinate[0], coordinate[1]-UNIT, coordinate[2], coordinate[3]-UNIT]
    down = [coordinate[0], coordinate[1]+UNIT, coordinate[2], coordinate[3]+UNIT]
    nearby = [up, down, left, right]
    return nearby

def humanWalk(humanWalkHelper):
    if humanWalkHelper % 2 == 0:
        if humanWalkHelper/2 < len(HUMANWALK1):
            human = env.humanStep1(HUMANWALK1[int(humanWalkHelper/2)])
        else:
            human = env.humanStep1(4)
    else:
        human = env.humanStep1(4)
    return human
    
if __name__ == "__main__":
    env = Maze()
    RL1 = QLearningTable1(actions=list(range(env.n_actions)),state=CURRENTSTATE)
    RL2 = QLearningTable2(actions=list(range(env.n_actions)),state=CURRENTSTATE)
    RL3 = QLearningTable3(actions=list(range(env.n_actions)),state=CURRENTSTATE)
    backupRL1 = QLearningTable1(actions=list(range(env.n_actions)),state=STATE1)
    backupRL2 = QLearningTable2(actions=list(range(env.n_actions)),state=STATE1)
    backupRL3 = QLearningTable3(actions=list(range(env.n_actions)),state=STATE1)
    ReturnRL1 = ReturnQLearningTable1(actions=list(range(env.n_actions)),state=CURRENTSTATE)
    ReturnRL2 = ReturnQLearningTable2(actions=list(range(env.n_actions)),state=CURRENTSTATE)
    ReturnRL3 = ReturnQLearningTable3(actions=list(range(env.n_actions)),state=CURRENTSTATE)
    env.after(300, update)
    env.mainloop()
