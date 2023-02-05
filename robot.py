import pybullet as p
import pyrosim.pyrosim as pyrosim
from pyrosim.neuralNetwork import NEURAL_NETWORK
import os
from sensor import SENSOR
from motor import MOTOR
import constants as c
import math




class ROBOT:
    def __init__(self, solutionID):
        self.sensors = {}
        self.motors = {}
        self.robotId = p.loadURDF("body.urdf")
        self.nn = NEURAL_NETWORK(f'brain{solutionID}.nndf')
        #self.motorJointRange = ???
        os.system(f'rm brain{solutionID}.nndf')
        self.solutionID = solutionID
        self.totalHeight = 0
    
    def Prepare_To_Sense(self):
        for linkName in pyrosim.linkNamesToIndices:
            self.sensors[linkName] = SENSOR(linkName)
    
    def Sense(self, i):
        for linkName in self.sensors:
            self.sensors[linkName].Get_Value(i)
            self.sensors[linkName].values[i] = math.sin(10*i)
        #print(linkName)
    
    def Prepare_To_Act(self):
        for jointName in pyrosim.jointNamesToIndices:
            self.motors[jointName.decode('utf-8')] = MOTOR(jointName)
    
    def Act(self, i):
        for neuronName in self.nn.Get_Neuron_Names():
            if self.nn.Is_Motor_Neuron(neuronName):
                jointName = self.nn.Get_Motor_Neurons_Joint(neuronName)
                desiredAngle = self.nn.Get_Value_Of(neuronName) * c.motorJointRange
                #print("da", desiredAngle)
                #print(self.nn.Get_Value_Of(neuronName), c.motorJointRange, desiredAngle)
                self.motors[jointName]
                self.motors[jointName].Set_Value(self.robotId, desiredAngle)
        
        zPosition = p.getBasePositionAndOrientation(self.robotId)[0][2]
        self.totalHeight += zPosition
    
    def Think(self):
        self.nn.Update()
        #self.nn.Print()
    
    def Get_Fitness(self):
        basePositionAndOrientation = p.getBasePositionAndOrientation(self.robotId)
        basePosition = basePositionAndOrientation[0]
        xPosition = basePosition[0]
        yPosition = basePosition[1]
        zPosition = basePosition[2]
        

        f = open(f'tmp{self.solutionID}.txt', "w")
        f.write(str(yPosition+(self.totalHeight*2/len(self.sensors))))
        f.close()
        os.system(f'mv tmp{self.solutionID}.txt fitness{self.solutionID}.txt')

  
        






