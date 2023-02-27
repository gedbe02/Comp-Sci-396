import pybullet as p
import pyrosim.pyrosim as pyrosim
from pyrosim.neuralNetwork import NEURAL_NETWORK
import os
from sensor import SENSOR
from motor import MOTOR
import constants as c
import math
import random




class ROBOT:
    def __init__(self, solutionID, test, evolved):
        self.sensors = {}
        self.motors = {}

        #Won't work with assignments <=5
        

        if test:
            if evolved:
                self.nn = NEURAL_NETWORK(f'results/evolved/{solutionID}/brain{solutionID}.nndf')
                self.robotId = p.loadURDF(f'results/evolved/{solutionID}/body{solutionID}.urdf') 
            else:
                self.nn = NEURAL_NETWORK(f'results/random/{solutionID}/brain{solutionID}.nndf')
                self.robotId = p.loadURDF(f'results/random/{solutionID}/body{solutionID}.urdf') 
        else:
            self.nn = NEURAL_NETWORK(f'brain{solutionID}.nndf')
            self.robotId = p.loadURDF(f'body{solutionID}.urdf') 

        if not test:
            os.system(f'rm brain{solutionID}.nndf')
            os.system(f'rm body{solutionID}.urdf')
        self.solutionID = solutionID
        #self.totalHeight = 0
        self.totalStandReward = 0
        self.lastSpot = 0
        #self.moveReward = 0
        self.lastYUp = 0
    
    def Prepare_To_Sense(self):
        for linkName in pyrosim.linkNamesToIndices:
            self.sensors[linkName] = SENSOR(linkName)
    
    def Sense(self, i):
        for linkName in self.sensors:
            self.sensors[linkName].Get_Value(i)
    
    def Prepare_To_Act(self):
        for jointName in pyrosim.jointNamesToIndices:
            self.motors[jointName.decode('utf-8')] = MOTOR(jointName)
    
    def Act(self, i):
        for neuronName in self.nn.Get_Neuron_Names():
            if self.nn.Is_Motor_Neuron(neuronName):
                jointName = self.nn.Get_Motor_Neurons_Joint(neuronName)
                desiredAngle = self.nn.Get_Value_Of(neuronName) * c.motorJointRange
                self.motors[jointName].Set_Value(self.robotId, desiredAngle)
    
    def Think(self):
        self.nn.Update()
        #self.nn.Print()
    
    def Get_Fitness(self):
        ''' 
        basePositionAndOrientation = p.getBasePositionAndOrientation(self.robotId)
        basePosition = basePositionAndOrientation[0]
        xPosition = basePosition[0]
        yPosition = basePosition[1]
        zPosition = basePosition[2]
        
        # Fitness is based on the farthest y position the robot got to before falling and
        # Average reward the robot got for standing
        fitness = 0

        # The last y position the robot stood up straight, given a weight of 50
        yReward = self.lastYUp * 50
        fitness += yReward

        # At each step, self.totalStandReward is incremented by 10 if the robot is standing and decremented by 5 if not
        # Below value is the average standing reward given a weight of .3
        fitness += self.totalStandReward*.3/len(self.sensors) #give reward for time spent standing
        
        #print("fitness", yReward, (self.totalStandReward*.3/len(self.sensors)), self.moveReward*20, fitness)
        '''

        basePositionAndOrientation = p.getBasePositionAndOrientation(self.robotId)
        basePosition = basePositionAndOrientation[0]
        xPosition = basePosition[0]
        yPosition = basePosition[1]
        zPosition = basePosition[2]

        fitness = yPosition * 10
        ###
        #fitness = self.solutionID
        ###

        f = open(f'tmp{self.solutionID}.txt', "w")
        f.write(str(fitness))
        f.close()
        os.system(f'mv tmp{self.solutionID}.txt fitness{self.solutionID}.txt')

  
        






