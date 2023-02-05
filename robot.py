import pybullet as p
import pyrosim.pyrosim as pyrosim
from pyrosim.neuralNetwork import NEURAL_NETWORK
import os
from sensor import SENSOR
from motor import MOTOR
import constants as c
import math




class ROBOT:
    def __init__(self, solutionID, test):
        self.sensors = {}
        self.motors = {}
        self.robotId = p.loadURDF("body.urdf")
        self.nn = NEURAL_NETWORK(f'brain{solutionID}.nndf')
        #self.motorJointRange = ???
        if not test:
            os.system(f'rm brain{solutionID}.nndf')
        self.solutionID = solutionID
        self.totalHeight = 0
        self.totalGoodBoy = 0
        self.lastSpot = 0
        self.moveReward = 0
        self.lastYUp = 0
    
    def Prepare_To_Sense(self):
        for linkName in pyrosim.linkNamesToIndices:
            self.sensors[linkName] = SENSOR(linkName)
    
    def Sense(self, i):
        for linkName in self.sensors:
            self.sensors[linkName].Get_Value(i)
            #if linkName in ["UpperRightLeg", "UpperLeftLeg"]:
            #self.sensors[linkName].values[i] = math.sin(10*i)
        #print(linkName)
    
    def Prepare_To_Act(self):
        for jointName in pyrosim.jointNamesToIndices:
            self.motors[jointName.decode('utf-8')] = MOTOR(jointName)
    
    def Act(self, i):
        for neuronName in self.nn.Get_Neuron_Names():
            if self.nn.Is_Motor_Neuron(neuronName):# and neuronName in ["6", "7", "8","9", "10", "11"]:
                jointName = self.nn.Get_Motor_Neurons_Joint(neuronName)
                if jointName in ["Torso_UpperRightLeg", "Torso_UpperLeftLeg"]:
                    desiredAngle = self.nn.Get_Value_Of(neuronName) * 1
                elif jointName in ["UpperRightLeg_LowerRightLeg", "UpperLeftLeg_LowerLeftLeg"]:
                    desiredAngle = self.nn.Get_Value_Of(neuronName) * 0.5
                elif jointName in ["LowerRightLeg_RightFoot", "LowerLeftLeg_LeftFoot"]:
                    desiredAngle = self.nn.Get_Value_Of(neuronName) * 0.2
                else:
                    desiredAngle = self.nn.Get_Value_Of(neuronName) * 0.4
                #print(self.nn.Get_Value_Of(neuronName), c.motorJointRange, desiredAngle)
                self.motors[jointName]
                self.motors[jointName].Set_Value(self.robotId, desiredAngle)
        
        
        xPosition = p.getBasePositionAndOrientation(self.robotId)[0][0]
        yPosition = p.getBasePositionAndOrientation(self.robotId)[0][1]
        zPosition = p.getBasePositionAndOrientation(self.robotId)[0][2]

        #NOTE TO FUTURE BEN: IF ROBOT DOESN'T MOVE, PUNISH ITS FITNESS

        if i % 100 == 0:
            deltaY = yPosition - self.lastSpot
            if deltaY > 0.1:
                self.moveReward += 1
            #print(deltaY)
            self.lastSpot = yPosition
            #print(xPosition, yPosition)

        self.totalHeight += zPosition
        if zPosition >= 2:
            self.totalGoodBoy += 10
            self.lastYUp = yPosition
        else:
            self.totalGoodBoy -= 5
        #print(zPosition)
    
    def Think(self):
        self.nn.Update()
        #self.nn.Print()
    
    def Get_Fitness(self):
        basePositionAndOrientation = p.getBasePositionAndOrientation(self.robotId)
        basePosition = basePositionAndOrientation[0]
        xPosition = basePosition[0]
        yPosition = basePosition[1]
        zPosition = basePosition[2]
        
        fitness = 0

        yReward = 0
        #if zPosition >= 2:                                #if still standing at end, give a big reward
        #    yReward = (yPosition * 50)
        #    fitness += (yPosition * 50)
        yReward = self.lastYUp * 50
        fitness += yReward

        fitness += self.totalGoodBoy*.3/len(self.sensors) #give reward for time spent standing
        #fitness += self.moveReward*20                     #give reward for time spent moving
        print("fitness", yReward, (self.totalGoodBoy*.3/len(self.sensors)), self.moveReward*20, fitness)

        f = open(f'tmp{self.solutionID}.txt', "w")
        f.write(str(fitness))#+(self.totalHeight*2/len(self.sensors))))
        f.close()
        os.system(f'mv tmp{self.solutionID}.txt fitness{self.solutionID}.txt')

  
        






