import pyrosim.pyrosim as pyrosim
from part import PART
class CUBE(PART):
    def __init__(self, name, length, width, height, relative_pos, absolute_pos, color):
        self.name = name
        self.length = length
        self.width = width
        self.height = height
        self.x = relative_pos[0]
        self.y = relative_pos[1]
        self.z = relative_pos[2]
        self.absolutePos = absolute_pos
        self.color = color
        self.isJoint = False

        PART.__init__(self, name, self.x, self.y, self.z, self.isJoint)

    def Send_Cube(self):
        pyrosim.Send_Cube(name=self.name, pos=[self.x,self.y,self.z] , size=[self.length,self.width,self.height], color=self.color)
    
    def overlapping(self, newPos, dim):
        #Calculating Cube 1
        x1 = self.absolutePos[0]
        y1 = self.absolutePos[1]
        z1 = self.absolutePos[2]
        l1 = self.length/2
        w1 = self.width/2
        h1 = self.height/2

        maxX1 = x1+l1
        minX1 = x1-l1

        maxY1 = y1+w1
        minY1 = y1-w1

        maxZ1 = z1+h1
        minZ1 = z1-h1

        #Calculating Cube 2
        x2 = newPos[0]
        y2 = newPos[1]
        z2 = newPos[2]
        l2 = dim[0]/2
        w2 = dim[1]/2
        h2 = dim[2]/2

        maxX2 = x2+l2
        minX2 = x2-l2

        maxY2 = y2+w2
        minY2 = y2-w2

        maxZ2 = z2+h2
        minZ2 = z2-h2

        
        overlapping  = maxX1 > minX2 and minX1 < maxX2
        overlapping &= maxY1 > minY2 and minY1 < maxY2
        overlapping &= maxZ1 > minZ2 and minZ1 < maxZ2

        return overlapping


