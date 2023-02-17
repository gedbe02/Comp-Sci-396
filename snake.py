import pyrosim.pyrosim as pyrosim
import pybullet as p
import numpy as np
import random
import os
import math
import constants as c
from sensor import SENSOR
from motor import MOTOR
from robot import ROBOT
from part import PART
from cube import CUBE
from joint import JOINT
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
        '''
        side = random.randint(50,100)/100
        length = side
        width = side
        height = side
        '''
        minSide = 100 * c.minSide #/100
        maxside = 100 * c.maxSide #/100

        parts = {}

        length = random.randint(minSide,maxside)/100
        width = random.randint(minSide,maxside)/100
        height = random.randint(minSide,maxside)/100
        x = 0
        y = 0
        startingZ = 0.5
        #pyrosim.Send_Cube(name="Part0", pos=[x,y,z] , size=[length, width, height], color=color)
        parts["Part0"] = CUBE("Part0", length, width, height, x, y, startingZ, color)
        '''
            Idea: Random choice on each cube that a leg will grow out of it. Nested for loop
        '''
        #Trying to get minZ: Lowest z coordinate of body (Lowest edge)
        minZ = startingZ - height/2 #Z coord of Center of Part0 - its "radius"

        previous = ["Part0", y, startingZ, width, height]
        for i in range(1, self.numParts):   
            parent = previous[0]
            prevY = previous[1]
            prevZ = previous[2]
            prevWidth = previous[3]
            prevHeight = previous[4]

            length = random.randint(minSide,maxside)/100
            width = random.randint(minSide,maxside)/100
            height = random.randint(minSide,maxside)/100


            jointX = 0
            cubeX = 0
            cubeZ = 0
            
            zOffset = random.randint(0, math.floor((prevHeight*100)/2))/100 * random.choice([-1,1])
   
            if i == 1:
                jointY = prevY + prevWidth/2
                cubeY = width/2
                jointZ = prevZ + zOffset 
                newZ = jointZ
            else:
                jointY = prevWidth
                cubeY = width/2
                jointZ = zOffset 
                newZ = prevZ + jointZ
            
            minZ = min(minZ, newZ-height/2)

            if self.isSensor[i]:
                color = green
            else:
                color = blue

            #pyrosim.Send_Joint(name = f'{parent}_Part{i}' , parent= parent , child = f'Part{i}' , type = "revolute", position = [jointX,jointY,jointZ], jointAxis = jointAxis) #To Do: Make joint axis random
            parts[f'{parent}_Part{i}'] = JOINT(f'{parent}_Part{i}', jointX, jointY, jointZ, parent, f'Part{i}')
            #pyrosim.Send_Cube(name=f'Part{i}', pos=[0,newCubeY,0] , size=[length,width,height], color=color)
            parts[f'Part{i}'] = CUBE(f'Part{i}', length, width, height, cubeX, cubeY, cubeZ, color) 

            previous = [f'Part{i}', jointY, newZ, width, height] #CHANGE


        parts['Part0'].z -= minZ
        if 'Part0_Part1' in parts:
            #First joints in stream need this. Will need to edit this
            parts['Part0_Part1'].z -= minZ
        
        
        for name in parts:
            part = parts[name]
            if part.isJoint:
                part.Send_Joint()
            else:
                part.Send_Cube()
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
    



