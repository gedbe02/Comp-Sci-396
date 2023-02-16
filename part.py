import random
import pyrosim.pyrosim as pyrosim
class PART():
    def __init__(self, name, length, width, height, x, y, z, color, is_joint, parent, child):
        self.name = name
        self.length = length
        self.width = width
        self.height = height
        self.x = x
        self.y = y
        self.z = z
        self.color = color
        self.isJoint = is_joint
        self.parent = parent
        self.child = child

        if is_joint:
            self.jointAxis = jointAxis = random.choice(["1 0 0", "0 0 1"])
    
    def Send_Cube(self):
        pyrosim.Send_Cube(name=self.name, pos=[self.x,self.y,self.z] , size=[self.length,self.width,self.height], color=self.color)

    def Send_Joint(self):
         pyrosim.Send_Joint(name = self.name, parent= self.parent , child = self.child , type = "revolute", position = [self.x,self.y,self.z], jointAxis = self.jointAxis) 