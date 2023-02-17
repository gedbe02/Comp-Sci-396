import pyrosim.pyrosim as pyrosim
from part import PART
class CUBE(PART):
    def __init__(self, name, length, width, height, pos, color):
        self.name = name
        self.length = length
        self.width = width
        self.height = height
        self.x = pos[0]
        self.y = pos[1]
        self.z = pos[2]
        self.color = color
        self.isJoint = False

        PART.__init__(self, name, self.x, self.y, self.z, self.isJoint)

    def Send_Cube(self):
        pyrosim.Send_Cube(name=self.name, pos=[self.x,self.y,self.z] , size=[self.length,self.width,self.height], color=self.color)