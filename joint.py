import pyrosim.pyrosim as pyrosim
from part import PART
import random

class JOINT(PART):
    def __init__(self, name, x, y, z, parent, child):
        self.name = name
        self.x = x
        self.y = y
        self.z = z
        self.parent = parent
        self.child = child
        self.isJoint = True
        self.jointAxis = jointAxis = random.choice(["1 0 0", "0 0 1"])

        PART.__init__(self, name, x, y, z, self.isJoint)

    def Send_Joint(self):
         pyrosim.Send_Joint(name = self.name, parent= self.parent , child = self.child , type = "revolute", position = [self.x,self.y,self.z], jointAxis = self.jointAxis) 