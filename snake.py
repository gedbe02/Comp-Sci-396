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
        
        side = random.randint(50,100)/100
        length = side
        width = side
        height = side

        pyrosim.Send_Cube(name="Part0", pos=[0,0,0.5] , size=[length, width, height], color=color)

        previous = ["Part0", 0, width]
        for i in range(1, self.numParts):   
            parent = previous[0]
            prevY = previous[1]
            prevWidth = previous[2]
            #Randomize below
            side = random.randint(50,100)/100
            length = side
            width = side
            height = side

            if i == 1:
                newJointY = prevY + prevWidth/2
                newCubeY = width/2
                z = 0.5
            else:
                newJointY = prevWidth
                newCubeY = width/2
                z = 0

            if self.isSensor[i]:
                color = green
            else:
                color = blue
                                                                                                                               
            pyrosim.Send_Joint(name = f'{parent}_Part{i}' , parent= parent , child = f'Part{i}' , type = "revolute", position = [0,newJointY,z], jointAxis = "1 0 0") #To Do: Make joint axis random
            pyrosim.Send_Cube(name=f'Part{i}', pos=[0,newCubeY,0] , size=[length,width,height], color=color) 
            previous = [f'Part{i}', newJointY, width]

        pyrosim.End()
    
    def Create_Brain(self):
        pyrosim.Start_NeuralNetwork(f'brain{self.myID}.nndf')
        i = 0
        j = self.numSensors
        for part in range(self.numParts):
            #Sensor Neurons
            is_sensor = self.isSensor[part]
            if is_sensor:
                pyrosim.Send_Sensor_Neuron(name = i , linkName = f'Part{part}')
                i += 1
                
            #Motor Neurons
            if part != self.numParts-1:
                pyrosim.Send_Motor_Neuron( name = j , jointName = f'Part{part}_Part{part+1}')
                j += 1

        for sensor in range(self.numSensors):
            for motor in range(self.numParts-1): #should be right
                pyrosim.Send_Synapse( sourceNeuronName = sensor, targetNeuronName = motor+self.numSensors , weight = self.weights[sensor][motor] )
        pyrosim.End()
    
    def Act(self, i):
        for neuronName in self.nn.Get_Neuron_Names():
            if self.nn.Is_Motor_Neuron(neuronName):
                jointName = self.nn.Get_Motor_Neurons_Joint(neuronName)
                desiredAngle = self.nn.Get_Value_Of(neuronName) * c.motorJointRange
                self.motors[jointName].Set_Value(self.robotId, desiredAngle)
    



