import pybullet as p
import pyrosim.pyrosim as pyrosim
from sensor import SENSOR
from motor import MOTOR



class ROBOT:
    def __init__(self):
        self.sensors = {}
        self.motors = {}
        self.robotId = p.loadURDF("body.urdf")
    
    def Prepare_To_Sense(self):
        for linkName in pyrosim.linkNamesToIndices:
            self.sensors[linkName] = SENSOR(linkName)
    
    def Sense(self, i):
        for linkName in self.sensors:
            self.sensors[linkName].Get_Value(i)
    
    def Prepare_To_Act(self):
        for jointName in pyrosim.jointNamesToIndices:
            self.motors[jointName] = MOTOR(jointName)
    
    def Act(self, i):
        for jointName in self.motors:
            self.motors[jointName].Set_Value(self.robotId, i)




