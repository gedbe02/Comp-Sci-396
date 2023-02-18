import pyrosim.pyrosim as pyrosim
import pybullet as p
import numpy as np
import random
import os
import math
import constants as c
from sensor import SENSOR
from motor import MOTOR
from robot import ROBOT
from part import PART
from cube import CUBE
from joint import JOINT
from pyrosim.neuralNetwork import NEURAL_NETWORK

green = ['Green','    <color rgba="0.0 1.0 0.0 1.0"/>']
blue  = ['Blue','    <color rgba="0.0 0.5 1.0 1.0"/>']

#tests
red  = ['Red','    <color rgba="1.0 0.0 0.0 1.0"/>']
purple  = ['Purple','    <color rgba="1.0 0.0 1.0 1.0"/>']
teal  = ['Teal','    <color rgba="0.0 1.0 1.0 1.0"/>']

class CREATURE(ROBOT): #Combined Solution and Robot
    def __init__(self, id, num_parts, num_sensors):
        self.myID = id
        self.numParts = num_parts
        self.numSensors = num_sensors
        print(num_parts, num_sensors)
        self.isSensor = np.full((1,num_parts), False)[0]
        self.isSensor[random.sample(range(num_parts), num_sensors)] = True

        self.Create_Body()
        self.weights = np.random.rand(self.numSensors,self.numParts-1)*2-1
        self.Create_Brain()

        ROBOT.__init__(self, id, False, False)

    def Create_Body(self):
        pyrosim.Start_URDF(f'body{self.myID}.urdf')

        #Part0
        newTotalSensors = 0
        if self.isSensor[0]:
            color = green
            newTotalSensors += 1
        else:
            color = blue

        minSide = 100 * c.minSide #/100
        maxSide = 100 * c.maxSide #/100

        self.parts = {}
        self.cubes = []

        length = random.randint(minSide,maxSide)/100
        width  = random.randint(minSide,maxSide)/100
        height = random.randint(minSide,maxSide)/100
        x = 0
        y = 0
        z = 0.5
        cubePos = [x,y,z]
        ###
        #color = blue
        ###
        cube = CUBE("Part0", length, width, height, cubePos, cubePos, color, None)
        self.parts["Part0"] = cube
        self.cubes.append(cube)
        #print(cubePos)

        #Trying to get minZ: Lowest z coordinate of body (Lowest edge)
        minZ = z - height/2 #Z coord of Center of Part0 - its "radius"

        previous = ["Part0", x, y, z, x, y, z, width, length, height, None]
        #If branch cant continue, stop making new links
        stop = False
        for i in range(1, self.numParts):  
            branches = 0
            #Can I clean this up? Like OOP it?
            parent = previous[0]
            prevX = previous[1]
            prevY = previous[2]
            prevZ = previous[3]
            oldX = previous[4]
            oldY = previous[5]
            oldZ = previous[6]
            prevWidth = previous[7]
            prevLength = previous[8]
            prevHeight = previous[9]
            prevDirection = previous[10]

            length = random.randint(minSide,maxSide)/100
            width  = random.randint(minSide,maxSide)/100
            height = random.randint(minSide,maxSide)/100
            
            # Do Later??
            xOffset = 0
            yOffset = 0
            zOffset = 0#random.randint(0, math.floor((prevHeight*100)/2))/100 * random.choice([-1,1])
            #

            #Direction Options
            options = [[1,0,0], [0,1,0], [0,0,1], [-1,0,0], [0,-1,0], [0,0,-1]]
            if i != 1:
                options.remove(list(prevDirection*-1))
            
            #Make new cube. If intersecting another, make again
            #What if out of directions?
            ###
            #x = 1
            setOptions = [[0,1,0], [0,1,0], [1,0,0], [0,-1,0], [0,0,-1], [0,-1,0], [0,0,-1]]
            ###
            
            intersecting = True
            while intersecting: #change to while new cube intersecting
                intersecting = False
                #x = 0
                # Direction
                direction = np.array(random.choice(options))
                ###
                #direction = np.array(setOptions[i])
                ###

                # Calculate Position
                if i == 1:
                    oldCenter = [oldX, oldY, oldZ]
                else:
                    oldCenter = np.array([0,0,0])
                    oldCenter = oldCenter + (prevDirection*np.array([prevLength, prevWidth, prevHeight])/2)
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
                #newZ = oldZ + (prevHeight/2 * direction[2])
                newZ = oldZ + ((prevHeight+height)/2 * direction[2])

                #Check for overlapping cubes
                for cub in self.cubes:
                    intersecting |= cub.overlapping([newX, newY, newZ], [length, width, height])
                if intersecting:
                    options.remove(list(direction))

                #If branch reaches end point, start a new branch
                if (len(options)) == 0:
                    branches += 1
                    # In very unlikely situation that no branches can be made, stop trying to gorw
                    if branches == len(self.cubes):
                        self.numParts = i
                        stop = True
                        print("Break")
                        break
                    #previous = [f'Part{i}', jointPos[0], jointPos[1], jointPos[2], newX, newY, newZ, width, length, height, direction] 
                    #Make new parent
                    print("New Branch", i)
                    new_parent    = random.choice(self.cubes[1:])
                    name          = new_parent.name
                    #prevX = previous[1]
                    #prevY = previous[2]
                    #prevZ = previous[3]
                    oldX          = new_parent.absolutePos[0]
                    oldY          = new_parent.absolutePos[1]
                    oldZ          = new_parent.absolutePos[2]
                    prevWidth     = new_parent.width
                    prevLength    = new_parent.length
                    prevHeight    = new_parent.height
                    prevDirection = new_parent.direction
                    options = [[1,0,0], [0,1,0], [0,0,1], [-1,0,0], [0,-1,0], [0,0,-1]]
                    options.remove(list(prevDirection*-1))

                    #Old Cut Off
                    #self.numParts = i
                    #stop = True
                    #print("Break")
                    #Maybe choose random part to offshoot off of
                    #break
                #WHAT DO IF NO MORE OPTIONS?
                ###
                #setOptions[i] = [0,0,1]
                ###
            
           
            #Joint and Cube Positions
            if stop:
                break
            jointPos = np.array([jointX, jointY, jointZ])
            relativeCubePos  = np.array([cubeX, cubeY, cubeZ]) * direction
            absoluteCubePos = np.array([newX, newY, newZ])
            
            # If not moving on z, must maintain height
            if i == 1 and abs(direction[2]) != 1: #Don't do if moving on z axis
                jointPos[2] = oldZ #prevZ
    
            #print(absoluteCubePos)


            #minZ Calculation
            # Need extra distance to calculate minZ
            #if direction[2] == -1:
            #    newZ -= height/2
            minZ = min(minZ, newZ-height/2)
            
            # Make joint and cube
            if self.isSensor[i]:
                color = green
                newTotalSensors += 1
            else:
                color = blue
            
            ###
            #colors = [blue,green,red,purple,teal]
            #j = i % 5
            #color = colors[j]

            ###

            jointAxis = random.choice(["1 0 0", "0 1 0", "0 0 1"])

            self.parts[f'{parent}_Part{i}'] = JOINT(f'{parent}_Part{i}', jointPos, parent, f'Part{i}', jointAxis)

            cube = CUBE(f'Part{i}', length, width, height, relativeCubePos, absoluteCubePos, color, direction) 
            self.parts[f'Part{i}'] = cube
            self.cubes.append(cube)

            previous = [f'Part{i}', jointPos[0], jointPos[1], jointPos[2], newX, newY, newZ, width, length, height, direction] 

        print("Double check min z calc after done with before")
        oldTorsoZ = self.parts['Part0'].z
        self.parts['Part0'].z -= minZ
        if 'Part0_Part1' in self.parts:
            #First joints in stream need this. Will need to edit this
            self.parts['Part0_Part1'].z -= minZ
        newTorsoZ = self.parts['Part0'].z
        print(f'minZ: {minZ}, old torso z: {oldTorsoZ}, new torso z: {newTorsoZ}')
        
        
        for name in self.parts:
            part = self.parts[name]
            if part.isJoint:
                part.Send_Joint()
            else:
                part.Send_Cube()
        #If branch breaks, need to decrease numSensors
        self.numSensors = newTotalSensors
        pyrosim.End()
    
   

    def Create_Brain(self):
        pyrosim.Start_NeuralNetwork(f'brain{self.myID}.nndf')
        print(self.numParts, self.numSensors)
        i = 0
        j = self.numSensors
        for part in range(self.numParts):
            #Sensor Neurons
            is_sensor = self.isSensor[part]
            if is_sensor:
                pyrosim.Send_Sensor_Neuron(name = i , linkName = f'Part{part}')
                i += 1
                
            #Motor Neurons
            if part != self.numParts-1:
                pyrosim.Send_Motor_Neuron( name = j , jointName = f'Part{part}_Part{part+1}')
                j += 1
       
        for sensor in range(self.numSensors):
            for motor in range(self.numParts-1): #should be right
                pyrosim.Send_Synapse( sourceNeuronName = sensor, targetNeuronName = motor+self.numSensors , weight = self.weights[sensor][motor] )
        pyrosim.End()
    
    def Act(self, i):
        for neuronName in self.nn.Get_Neuron_Names():
            if self.nn.Is_Motor_Neuron(neuronName):
                jointName = self.nn.Get_Motor_Neurons_Joint(neuronName)
                desiredAngle = self.nn.Get_Value_Of(neuronName) * c.motorJointRange
                self.motors[jointName].Set_Value(self.robotId, desiredAngle)
    



