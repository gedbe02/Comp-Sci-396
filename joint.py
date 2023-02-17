import pyrosim.pyrosim as pyrosim
from part import PART
import random

class JOINT(PART):
    def __init__(self, name, pos, parent, child, jointAxis):
        self.name = name
        self.x = pos[0]
        self.y = pos[1]
        self.z = pos[2]
        self.parent = parent
        self.child = child
        self.isJoint = True
        self.jointAxis = jointAxis

        PART.__init__(self, name, self.x, self.y, self.z, self.isJoint)

    def Send_Joint(self):
         pyrosim.Send_Joint(name = self.name, parent= self.parent , child = self.child , type = "revolute", position = [self.x,self.y,self.z], jointAxis = self.jointAxis) 