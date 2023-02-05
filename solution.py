import pyrosim.pyrosim as pyrosim
import numpy as np
import os
import random
import time
import constants as c

class SOLUTION:
    def __init__(self, nextAvailableID):
        self.weights = np.random.rand(c.numSensorNeurons,c.numMotorNeurons)*2-1
        self.motorJointRange = np.random.rand(c.numSensorNeurons,c.numMotorNeurons)*2-1
        self.myID = nextAvailableID

    def Start_Simulation(self, directOrGUI):
        self.Create_World()
        self.Create_Body()
        self.Create_Brain()
        os.system("python3 simulate.py " + directOrGUI + " "+ str(self.myID) + " &")
    
    def Wait_For_Simulation_To_End(self):
        while not os.path.exists(f'fitness{self.myID}.txt'):
            time.sleep(0.01)
        f = open(f'fitness{self.myID}.txt', "r")
        self.fitness = float(f.readlines()[0])
        os.system(f'rm fitness{self.myID}.txt')


    def Create_World(self):
        length = 1
        width = 1
        height = 1

        x = -2
        y = 2
        z = 0.5

        pyrosim.Start_SDF("world.sdf")
        #pyrosim.Send_Cube(name="Box", pos=[x,y,z] , size=[length,width,height])
        pyrosim.End()
    
    def Create_Body(self):
        pyrosim.Start_URDF("body.urdf")

        pyrosim.Send_Cube(name="Torso", pos=[0,0,2] , size=[0.75,0.5,1], color=['Green','    <color rgba="0.0 1.0 0.0 1.0"/>'])

        #Right Leg - Test Joint Axis
        pyrosim.Send_Joint( name = "Torso_UpperRightLeg" , parent= "Torso" , child = "UpperRightLeg" , type = "revolute", position = [0.375,0,1.75], jointAxis = "1 0 0")
        pyrosim.Send_Cube(name="UpperRightLeg", pos=[0.125,0,-0.5] , size=[0.25,0.25,1], color=['Blue','    <color rgba="0.0 0.25 1.0 1.0"/>'])

        pyrosim.Send_Joint( name = "UpperRightLeg_LowerRightLeg" , parent= "UpperRightLeg" , child = "LowerRightLeg" , type = "revolute", position = [0.125,0,-1], jointAxis = "1 0 0")
        pyrosim.Send_Cube(name="LowerRightLeg", pos=[0,0,-0.35] , size=[0.25,0.25,0.70], color=['Light Blue','    <color rgba="0.0 0.5 1.0 1.0"/>'])

        

        #Left Leg - Test Joint Axis
        pyrosim.Send_Joint( name = "Torso_UpperLeftLeg" , parent= "Torso" , child = "UpperLeftLeg" , type = "revolute", position = [-0.375,0,1.75], jointAxis = "1 0 0")
        pyrosim.Send_Cube(name="UpperLeftLeg", pos=[-0.125,0,-0.5] , size=[0.25,0.25,1], color=['Red','    <color rgba="1.0 0.25 0 1.0"/>'])

        pyrosim.Send_Joint( name = "UpperLeftLeg_LowerLeftLeg" , parent= "UpperLeftLeg" , child = "LowerLeftLeg" , type = "revolute", position = [-0.125,0,-1], jointAxis = "1 0 0")
        pyrosim.Send_Cube(name="LowerLeftLeg", pos=[0,0,-0.35] , size=[0.25,0.25,0.70], color=['Orange','    <color rgba="1.0 0.5 0.0 1.0"/>'])

        
        
        #Feet 
        pyrosim.Send_Joint( name = "LowerRightLeg_RightFoot" , parent= "LowerRightLeg" , child = "RightFoot" , type = "revolute", position = [0,0,-0.70], jointAxis = "1 0 0")
        pyrosim.Send_Cube(name="RightFoot", pos=[0,0,-0.025] , size=[0.25,0.5,0.05], color=['Black','    <color rgba="0 0 0 1"/>'])

        pyrosim.Send_Joint( name = "LowerLeftLeg_LeftFoot" , parent= "LowerLeftLeg" , child = "LeftFoot" , type = "revolute", position = [0,0,-0.70], jointAxis = "1 0 0")
        pyrosim.Send_Cube(name="LeftFoot", pos=[0,0,-0.025] , size=[0.25,0.5,0.05], color=['Black','    <color rgba="0 0 0 1"/>'])


        pyrosim.End()
    

    def Create_Brain(self):
        pyrosim.Start_NeuralNetwork(f'brain{self.myID}.nndf')

        pyrosim.Send_Sensor_Neuron(name = 0 , linkName = "RightFoot")
        pyrosim.Send_Sensor_Neuron(name = 1 , linkName = "LeftFoot")

        pyrosim.Send_Motor_Neuron( name = 2 , jointName = "Torso_UpperRightLeg")
        pyrosim.Send_Motor_Neuron( name = 3 , jointName = "UpperRightLeg_LowerRightLeg")
        pyrosim.Send_Motor_Neuron( name = 4 , jointName = "LowerRightLeg_RightFoot")
        pyrosim.Send_Motor_Neuron( name = 5 , jointName = "Torso_UpperLeftLeg")
        pyrosim.Send_Motor_Neuron( name = 6 , jointName = "UpperLeftLeg_LowerLeftLeg")
        pyrosim.Send_Motor_Neuron( name = 7 , jointName = "LowerLeftLeg_LeftFoot")

        for currentRow in range(c.numSensorNeurons):
            for currentColumn in range(c.numMotorNeurons):
                pyrosim.Send_Synapse( sourceNeuronName = currentRow, targetNeuronName = currentColumn+c.numSensorNeurons , weight = self.weights[currentRow][currentColumn] )

        pyrosim.End()
    
    def Mutate(self):
        row = random.randint(0,c.numSensorNeurons-1)
        col = random.randint(0,c.numMotorNeurons-1)
        self.weights[row][col] = random.random() * 2 - 1
    
    def Set_ID(self, id):
        self.myID = id
    



    def Create_Quad_Body(self):
        pyrosim.Start_URDF("body.urdf")

        pyrosim.Send_Cube(name="Torso", pos=[0,0,1] , size=[1,1,1])

        pyrosim.Send_Joint( name = "Torso_BackLeg" , parent= "Torso" , child = "BackLeg" , type = "revolute", position = [0,-0.5,1], jointAxis = "1 0 0")
        pyrosim.Send_Cube(name="BackLeg", pos=[0,-0.5,0] , size=[0.2,1,0.2])

        pyrosim.Send_Joint( name = "Torso_FrontLeg" , parent= "Torso" , child = "FrontLeg" , type = "revolute", position = [0,0.5,1], jointAxis = "1 0 0")
        pyrosim.Send_Cube(name="FrontLeg", pos=[0,0.5,0] , size=[0.2,1,0.2])

        pyrosim.Send_Joint( name = "Torso_LeftLeg" , parent= "Torso" , child = "LeftLeg" , type = "revolute", position = [-0.5,0,1], jointAxis = "0 1 0")
        pyrosim.Send_Cube(name="LeftLeg", pos=[-0.5,0,0] , size=[1,0.2,0.2])

        pyrosim.Send_Joint( name = "Torso_RightLeg" , parent= "Torso" , child = "RightLeg" , type = "revolute", position = [0.5,0,1], jointAxis = "0 1 0")
        pyrosim.Send_Cube(name="RightLeg", pos=[0.5,0,0] , size=[1,0.2,0.2], color = ['Red','    <color rgba="1.0 0.0 0.0 1.0"/>'])

        pyrosim.Send_Joint( name = "BackLeg_BackLowerLeg" , parent= "BackLeg" , child = "BackLowerLeg" , type = "revolute", position = [0,-1,0], jointAxis = "1 0 0")
        pyrosim.Send_Cube(name="BackLowerLeg", pos=[0,0,-0.5] , size=[0.2,0.2,1])

        pyrosim.Send_Joint( name = "FrontLeg_FrontLowerLeg" , parent= "FrontLeg" , child = "FrontLowerLeg" , type = "revolute", position = [0,1,0], jointAxis = "1 0 0")
        pyrosim.Send_Cube(name="FrontLowerLeg", pos=[0,0,-0.5] , size=[0.2,0.2,1])

        pyrosim.Send_Joint( name = "LeftLeg_LeftLowerLeg" , parent= "LeftLeg" , child = "LeftLowerLeg" , type = "revolute", position = [-1,0,0], jointAxis = "0 1 0")
        pyrosim.Send_Cube(name="LeftLowerLeg", pos=[0,0,-0.5] , size=[0.2,0.2,1])

        pyrosim.Send_Joint( name = "RightLeg_RightLowerLeg" , parent= "RightLeg" , child = "RightLowerLeg" , type = "revolute", position = [1,0,0], jointAxis = "0 1 0")
        pyrosim.Send_Cube(name="RightLowerLeg", pos=[0,0,-0.5] , size=[0.2,0.2,1], color = ['Red','    <color rgba="1.0 0.0 0.0 1.0"/>'])

        pyrosim.End()

    def Create_Quad_Brain(self):
        pyrosim.Start_NeuralNetwork(f'brain{self.myID}.nndf')

        '''pyrosim.Send_Sensor_Neuron(name = 0 , linkName = "Torso")
        pyrosim.Send_Sensor_Neuron(name = 1 , linkName = "BackLeg")
        pyrosim.Send_Sensor_Neuron(name = 2 , linkName = "FrontLeg")
        pyrosim.Send_Sensor_Neuron(name = 3 , linkName = "LeftLeg")
        pyrosim.Send_Sensor_Neuron(name = 4 , linkName = "RightLeg")
        pyrosim.Send_Sensor_Neuron(name = 5 , linkName = "BackLowerLeg")
        pyrosim.Send_Sensor_Neuron(name = 6 , linkName = "FrontLowerLeg")
        pyrosim.Send_Sensor_Neuron(name = 7 , linkName = "LeftLowerLeg")
        pyrosim.Send_Sensor_Neuron(name = 8 , linkName = "RightLowerLeg")

        pyrosim.Send_Motor_Neuron( name = 9 , jointName = "Torso_BackLeg")
        pyrosim.Send_Motor_Neuron( name = 10 , jointName = "Torso_FrontLeg")
        pyrosim.Send_Motor_Neuron( name = 11 , jointName = "Torso_LeftLeg")
        pyrosim.Send_Motor_Neuron( name = 12 , jointName = "Torso_RightLeg")
        pyrosim.Send_Motor_Neuron( name = 13 , jointName = "BackLeg_BackLowerLeg")
        pyrosim.Send_Motor_Neuron( name = 14 , jointName = "FrontLeg_FrontLowerLeg")
        pyrosim.Send_Motor_Neuron( name = 15 , jointName = "LeftLeg_LeftLowerLeg")
        pyrosim.Send_Motor_Neuron( name = 16 , jointName = "RightLeg_RightLowerLeg")'''

        pyrosim.Send_Sensor_Neuron(name = 0 , linkName = "BackLowerLeg")
        pyrosim.Send_Sensor_Neuron(name = 1 , linkName = "FrontLowerLeg")
        pyrosim.Send_Sensor_Neuron(name = 2 , linkName = "LeftLowerLeg")
        pyrosim.Send_Sensor_Neuron(name = 3 , linkName = "RightLowerLeg")

        pyrosim.Send_Motor_Neuron( name = 4 , jointName = "Torso_BackLeg")
        pyrosim.Send_Motor_Neuron( name = 5 , jointName = "Torso_FrontLeg")
        pyrosim.Send_Motor_Neuron( name = 6 , jointName = "Torso_LeftLeg")
        pyrosim.Send_Motor_Neuron( name = 7 , jointName = "Torso_RightLeg")
        pyrosim.Send_Motor_Neuron( name = 8 , jointName = "BackLeg_BackLowerLeg")
        pyrosim.Send_Motor_Neuron( name = 9 , jointName = "FrontLeg_FrontLowerLeg")
        pyrosim.Send_Motor_Neuron( name = 10 , jointName = "LeftLeg_LeftLowerLeg")
        pyrosim.Send_Motor_Neuron( name = 11 , jointName = "RightLeg_RightLowerLeg")

        for currentRow in range(c.numSensorNeurons):
            for currentColumn in range(c.numMotorNeurons):
                pyrosim.Send_Synapse( sourceNeuronName = currentRow, targetNeuronName = currentColumn+c.numSensorNeurons , weight = self.weights[currentRow][currentColumn] )

        pyrosim.End()