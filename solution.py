import pyrosim.pyrosim as pyrosim
import numpy as np
import os
import random
import time
import constants as c
from cube import CUBE
from joint import JOINT

# To Do
# change init
# Change Create_Body
# Change Create_brain
# Change Mutate
    # On mutate, maybe add 0-c.maxNewParts parts and increase num sensors by 0-(# of new parts - 1)
# Change Start_Simulation and Wait_For_Simulation_To_End

green = ['Green','    <color rgba="0.0 1.0 0.0 1.0"/>']
blue  = ['Blue','    <color rgba="0.0 0.5 1.0 1.0"/>']
class SOLUTION:
    def __init__(self, nextAvailableID):  
        self.weights = np.random.rand(c.numSensorNeurons,c.numMotorNeurons)*2-1
        #self.motorJointRange = np.random.rand(c.numSensorNeurons,c.numMotorNeurons)*2-1 - Maybe add?
        self.myID = nextAvailableID

        # Random Generation #
        # All parents shoudl initally start with 2 parts and 1-2 sensors, so it can actually move
        self.numParts = 2
        self.numSensors = random.randint(1,2)
        self.isSensor = np.full((1,self.numParts), False)[0]
        self.isSensor[random.sample(range(self.numParts), self.numSensors)] = True

        self.Initialize_Body()



    def Start_Simulation(self, directOrGUI):
        self.Create_World()
        self.Create_Body()
        self.Create_Brain()
        os.system("python3 simulate.py " + directOrGUI + " "+ str(self.myID) + " not_test e &")
    
    def Wait_For_Simulation_To_End(self):
        while not os.path.exists(f'fitness{self.myID}.txt'):
            time.sleep(0.01)
        f = open(f'fitness{self.myID}.txt', "r")
        self.fitness = float(f.readlines()[0])
        os.system(f'rm fitness{self.myID}.txt')


    def Create_World(self):
        pyrosim.Start_SDF("world.sdf")
        pyrosim.End()
    
    '''
    Information:
    Initialize_Body populates self.parts, but does so randomly every time

    What Needs to Happen:
    In init, Initialize_Body populates self.parts with Part0 and Part1

    Run Create_Body to test solution

    *Mutation*
    A new body part(s) must be added to self.parts
    Mutate_Body should do this
        Needs to also randomly decide if part is a sensor or not

    To Do:
    Split Initialize Body into two functions
    
    '''


    def Create_Body(self):
        #Min Z - To Do
        parts = self.parts.copy()
        parts['Part0'].z -= self.minZ
        if 'Part0_Part1' in parts:
            self.parts['Part0_Part1'].z -= self.minZ

        pyrosim.Start_URDF(f'body{self.myID}.urdf')
        for name in parts:
            part = parts[name]
            if part.isJoint:
                part.Send_Joint()
            else:
                part.Send_Cube()
        #If branch breaks, need to decrease numSensors
        #self.numSensors = newTotalSensors
        pyrosim.End()
    
    def Initialize_Body(self):
        #Part0
        #newTotalSensors = 0
        if self.isSensor[0]:
            color = green
            #newTotalSensors += 1
        else:
            color = blue

        self.minSide = 100 * c.minSide #/100
        self.maxSide = 100 * c.maxSide #/100

        self.parts = {}
        self.cubes = []
        self.joints = []

        length = random.randint(self.minSide,self.maxSide)/100
        width  = random.randint(self.minSide,self.maxSide)/100
        height = random.randint(self.minSide,self.maxSide)/100
        x = 0
        y = 0
        z = 0.5
        cubePos = [x,y,z]

        cube = CUBE("Part0", length, width, height, cubePos, cubePos, color, None)
        self.parts["Part0"] = cube
        self.cubes.append(cube)

        #Trying to get minZ: Lowest z coordinate of body (Lowest edge)
        self.minZ = z - height/2 #Z coord of Center of Part0 - its "radius"

        oldCenter = cubePos
        parent    = self.cubes[0]
        self.Make_Part(oldCenter, parent, 1)

    
    #For Mutation#
    # potential_parents = self.cubes[1:].copy()
    # parent            = random.choice(potential_parents)
    # oldCenter = np.array([0,0,0])
    # oldCenter = oldCenter + (prevDirection*np.array([prevLength, prevWidth, prevHeight])/2)
    # vv Still for Mutation vv
    '''
    # In the very unlikely situation that no branches can be made, stop trying to grow
                if len(potential_parents) == 0:
                    self.numParts = i
                    if self.numParts == 1:
                        self.numSensors = 0
                    stop = True
                    print("Break")
                    break
                #Give new parent
                potential_parents.remove(parent)
    '''
    #^^If Make_Part returns -1, try another parent
    ## In the very unlikely situation that no branches can be made, stop trying to grow
                ############ NEED STOP VARIABLE
    '''
    if stop:
            print("Need to bug test when numParts parts can't be made")
            exit()
            break
    '''

    # Takes in previous center (relative or absolute) and a random parent
    def Make_Part(self, oldCenter, parent, i):
        #If branch cant continue, stop making new links
        #stop = False
        parentName    = parent.name
        oldX          = parent.absolutePos[0]
        oldY          = parent.absolutePos[1]
        oldZ          = parent.absolutePos[2]
        prevWidth     = parent.width
        prevLength    = parent.length
        prevHeight    = parent.height
        prevDirection = parent.direction

        length = random.randint(self.minSide,self.maxSide)/100
        width  = random.randint(self.minSide,self.maxSide)/100
        height = random.randint(self.minSide,self.maxSide)/100

        #Direction Options
        options = [[1,0,0], [0,1,0], [0,0,1], [-1,0,0], [0,-1,0], [0,0,-1]]
        if prevDirection:
            options.remove(list(prevDirection*-1))
        
        # Try to make new cube/joint
        intersecting = True
        while intersecting: 
            intersecting = False
            direction = np.array(random.choice(options))

            #X
            jointX = oldCenter[0] + direction[0]*prevLength/2
            cubeX = length/2
            newX = oldX + ((prevLength+length)/2 * direction[0])

            #Y
            jointY = oldCenter[1] + direction[1]*prevWidth/2
            cubeY = width/2
            newY = oldY + ((prevWidth+width)/2 * direction[1])

            #Z
            jointZ = oldCenter[2] + direction[2]*prevHeight/2
            cubeZ = height/2
            newZ = oldZ + ((prevHeight+height)/2 * direction[2])

            #Check for overlapping cubes
            for cub in self.cubes:
                intersecting |= cub.overlapping([newX, newY, newZ], [length, width, height])
            if intersecting:
                options.remove(list(direction))

            #If branch reaches end point, start a new branch
            if (len(options)) == 0:
                return -1
        
        #Joint and Cube Positions
        jointPos = np.array([jointX, jointY, jointZ])
        relativeCubePos  = np.array([cubeX, cubeY, cubeZ]) * direction
        absoluteCubePos = np.array([newX, newY, newZ])
        
        # If not moving on z, must maintain height
        # DO I NEED THIS? DO CHECK
        if not prevDirection and abs(direction[2]) != 1: #Don't do if moving on z axis
            jointPos[2] = oldZ 

        #minZ Calculation
        self.minZ = min(self.minZ, newZ-height/2)
        
        #Make joint and cube
        if self.isSensor[i]:
            color = green
            #newTotalSensors += 1
        else:
            color = blue
        
        jointAxis = random.choice(["1 0 0", "0 1 0", "0 0 1"])
        joint = JOINT(f'{parentName}_Part{i}', jointPos, parentName, f'Part{i}', jointAxis)
        self.parts[f'{parentName}_Part{i}'] = joint
        self.joints.append(joint)
        
        cube = CUBE(f'Part{i}', length, width, height, relativeCubePos, absoluteCubePos, color, direction) 
        self.parts[f'Part{i}'] = cube
        self.cubes.append(cube)

        return 0

    def Create_Brain(self):
        pyrosim.Start_NeuralNetwork(f'brain{self.myID}.nndf')
        # To Do
        pyrosim.End()
    
    def Mutate(self):
        row = random.randint(0,c.numSensorNeurons-1)
        col = random.randint(0,c.numMotorNeurons-1)
        self.weights[row][col] = random.random() * 2 - 1
    
    def Set_ID(self, id):
        self.myID = id