import pybullet as p
import pyrosim.pyrosim as pyrosim
from pyrosim.neuralNetwork import NEURAL_NETWORK
from sensor import SENSOR
from motor import MOTOR



class ROBOT:
    def __init__(self):
        self.sensors = {}
        self.motors = {}
        self.robotId = p.loadURDF("body.urdf")
        self.nn = NEURAL_NETWORK("brain.nndf")

    
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
                desiredAngle = self.nn.Get_Value_Of(neuronName)
                #print("DA", desiredAngle)
                #exit()
                self.motors[jointName].Set_Value(self.robotId, desiredAngle)
    
    def Think(self):
        self.nn.Update()
        self.nn.Print()
        






