import pyrosim.pyrosim as pyrosim
from part import PART
class CUBE(PART):
    def __init__(self, name, length, width, height, x, y, z, color):
        self.name = name
        self.length = length
        self.width = width
        self.height = height
        self.x = x
        self.y = y
        self.z = z
        self.color = color
        self.isJoint = False

        PART.__init__(self, name, x, y, z, self.isJoint)

    def Send_Cube(self):
        pyrosim.Send_Cube(name=self.name, pos=[self.x,self.y,self.z] , size=[self.length,self.width,self.height], color=self.color)