import pyrosim.pyrosim as pyrosim
import pybullet as p
import numpy as np
import random
import os
import constants as c
from sensor import SENSOR
from motor import MOTOR
from robot import ROBOT
from pyrosim.neuralNetwork import NEURAL_NETWORK

green = ['Green','    <color rgba="0.0 1.0 0.0 1.0"/>']
blue  = ['Blue','    <color rgba="0.0 0.5 1.0 1.0"/>']

class SNAKE(ROBOT): #Combined Solution and Robot
    def __init__(self, id, num_parts, num_sensors):
        self.myID = id
        self.numParts = num_parts
        self.numSensors = num_sensors
        self.isSensor = np.full((1,num_parts), False)[0]
        self.isSensor[random.sample(range(num_parts), num_sensors)] = True

        self.sensors = {}
        self.motors = {}
        self.weights = np.random.rand(num_sensors,num_parts-1)*2-1

        self.Create_Body()
        self.Create_Brain()

        ROBOT.__init__(self, id, False, False)

    def Create_Body(self):
        pyrosim.Start_URDF(f'body{self.myID}.urdf')
        if self.isSensor[0]:
            color = green
        else:
            color = blue
        pyrosim.Send_Cube(name="Torso", pos=[0,0,0.5] , size=[1,1,1], color=color)
        previous = ["Torso", 0, 1]
        z = 0.5
        for i in range(self.numParts-1):   
            parent = previous[0]
            prevY = previous[1]
            prevWidth = previous[2]
            #Randomize below
            width = i+2
            length = i/2 + 1
            height = 1

            newJointY = prevY + prevWidth/2
            newCubeY = width/2

            if self.isSensor[i]:
                color = green
            else:
                color = blue
                                                                                                    #To Do: Randomize Z Axis
            pyrosim.Send_Joint(name = f'{parent}_Part{i}' , parent= parent , child = f'Part{i}' , type = "revolute", position = [0,newJointY,z], jointAxis = "1 0 0") #Make joint axis random
            pyrosim.Send_Cube(name=f'Part{i}', pos=[0,newCubeY,0] , size=[length,width,height], color=color) #To Do: Randomize if sensor
            z = 0
            previous = [f'Part{i}', newJointY, width]

        pyrosim.End()
    
    def Create_Brain(self):
        pyrosim.Start_NeuralNetwork(f'brain{self.myID}.nndf')

       # for sensor in range(self.numSensors):
       #     for motor in range(self.numParts-1): #should be right
       #         pyrosim.Send_Synapse( sourceNeuronName = sensor, targetNeuronName = motor+self.sensors , weight = self.weights[sensor][motor] )
        pyrosim.End()
    
    def Act(self, i):
        for neuronName in self.nn.Get_Neuron_Names():
            if self.nn.Is_Motor_Neuron(neuronName):
                jointName = self.nn.Get_Motor_Neurons_Joint(neuronName)
                desiredAngle = self.nn.Get_Value_Of(neuronName) * c.motorJointRange
                self.motors[jointName]
                self.motors[jointName].Set_Value(self.robotId, desiredAngle)
    



