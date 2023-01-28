import pyrosim.pyrosim as pyrosim
import numpy as np
import os
import random


class SOLUTION:
    def __init__(self):
        self.weights = np.random.rand(3,2)*2-1

    def Evaluate(self, directOrGUI):
        self.Create_World()
        self.Create_Body()
        self.Create_Brain()

        os.system("python3 simulate.py " + directOrGUI)

        f = open("fitness.txt", "r")
        self.fitness = float(f.readlines()[0])


    def Create_World(self):
        length = 1
        width = 1
        height = 1

        x = -2
        y = 2
        z = 0.5

        pyrosim.Start_SDF("world.sdf")
        pyrosim.Send_Cube(name="Box", pos=[x,y,z] , size=[length,width,height])
        pyrosim.End()

        
    def Create_Body(self):
        length = 1
        width = 1
        height = 1

        x = 0
        y = 0
        z = 0.5
        pyrosim.Start_URDF("body.urdf")

        pyrosim.Send_Cube(name="Torso", pos=[0,0,1.5] , size=[length,width,height])

        pyrosim.Send_Joint( name = "Torso_BackLeg" , parent= "Torso" , child = "BackLeg" , type = "revolute", position = [0.5,0,1])
        pyrosim.Send_Cube(name="BackLeg", pos=[0.5,0,-0.5] , size=[length,width,height])

        pyrosim.Send_Joint( name = "Torso_FrontLeg" , parent= "Torso" , child = "FrontLeg" , type = "revolute", position = [-0.5,0,1])
        pyrosim.Send_Cube(name="FrontLeg", pos=[-0.5,0,-0.5] , size=[length,width,height])


        pyrosim.End()

    def Create_Brain(self):
        pyrosim.Start_NeuralNetwork("brain.nndf")

        pyrosim.Send_Sensor_Neuron(name = 0 , linkName = "Torso")
        pyrosim.Send_Sensor_Neuron(name = 1 , linkName = "BackLeg")
        pyrosim.Send_Sensor_Neuron(name = 2 , linkName = "FrontLeg")

        pyrosim.Send_Motor_Neuron( name = 3 , jointName = "Torso_BackLeg")
        pyrosim.Send_Motor_Neuron( name = 4 , jointName = "Torso_FrontLeg")

        for currentRow in [0,1,2]:
            for currentColumn in [0,1]:
                pyrosim.Send_Synapse( sourceNeuronName = currentRow, targetNeuronName = currentColumn+3 , weight = self.weights[currentRow][currentColumn] )

        pyrosim.End()
    
    def Mutate(self):
        row = random.randint(0,2)
        col = random.randint(0,1)
        self.weights[row][col] = random.random() * 2 - 1