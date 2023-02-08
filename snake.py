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
        self.num_parts = num_parts
        self.num_sensors = num_sensors
        self.sensors = {}
        self.motors = {}
        self.weights = np.random.rand(num_sensors,num_parts-1)*2-1

        self.Create_Body()
        self.Create_Brain()

        ROBOT.__init__(self, id, False, False)

    def Create_Body(self):
        pyrosim.Start_URDF(f'body{self.myID}.urdf')

        pyrosim.Send_Cube(name="Torso", pos=[0,0,0.5] , size=[1,1,1], color=blue)

        pyrosim.End()
    
    def Create_Brain(self):
        pyrosim.Start_NeuralNetwork(f'brain{self.myID}.nndf')

        for sensor in range(self.num_sensors):
            for motor in range(self.num_parts-1): #should be right
                pyrosim.Send_Synapse( sourceNeuronName = sensor, targetNeuronName = motor+self.sensors , weight = self.weights[sensor][motor] )
        pyrosim.End()
    
    def Act(self, i):
        for neuronName in self.nn.Get_Neuron_Names():
            if self.nn.Is_Motor_Neuron(neuronName):
                jointName = self.nn.Get_Motor_Neurons_Joint(neuronName)
                desiredAngle = self.nn.Get_Value_Of(neuronName) * c.motorJointRange
                self.motors[jointName]
                self.motors[jointName].Set_Value(self.robotId, desiredAngle)
    



