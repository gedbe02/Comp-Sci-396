import pyrosim.pyrosim as pyrosim
import pybullet as p
import numpy as np
import random
import constants as c
from robot import ROBOT
from cube import CUBE
from joint import JOINT

green = ['Green','    <color rgba="0.0 1.0 0.0 1.0"/>']
blue  = ['Blue','    <color rgba="0.0 0.5 1.0 1.0"/>']

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
        self.joints = []

        length = random.randint(minSide,maxSide)/100
        width  = random.randint(minSide,maxSide)/100
        height = random.randint(minSide,maxSide)/100
        x = 0
        y = 0
        z = 0.5
        cubePos = [x,y,z]

        cube = CUBE("Part0", length, width, height, cubePos, cubePos, color, None)
        self.parts["Part0"] = cube
        self.cubes.append(cube)

        #Trying to get minZ: Lowest z coordinate of body (Lowest edge)
        minZ = z - height/2 #Z coord of Center of Part0 - its "radius"

        #If branch cant continue, stop making new links
        stop = False
        for i in range(1, self.numParts):  
            branches = 0
            if i == 1:
                parent    = self.cubes[0]
            else:
                parent    = random.choice(self.cubes[1:])
            parentName    = parent.name
            oldX          = parent.absolutePos[0]
            oldY          = parent.absolutePos[1]
            oldZ          = parent.absolutePos[2]
            prevWidth     = parent.width
            prevLength    = parent.length
            prevHeight    = parent.height
            prevDirection = parent.direction

            length = random.randint(minSide,maxSide)/100
            width  = random.randint(minSide,maxSide)/100
            height = random.randint(minSide,maxSide)/100

            #Direction Options
            options = [[1,0,0], [0,1,0], [0,0,1], [-1,0,0], [0,-1,0], [0,0,-1]]
            if i != 1:
                options.remove(list(prevDirection*-1))
            
            # Try to make new cube/joint
            intersecting = True
            while intersecting: 
                intersecting = False
                direction = np.array(random.choice(options))

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
                newZ = oldZ + ((prevHeight+height)/2 * direction[2])

                #Check for overlapping cubes
                for cub in self.cubes:
                    intersecting |= cub.overlapping([newX, newY, newZ], [length, width, height])
                if intersecting:
                    options.remove(list(direction))

                #If branch reaches end point, start a new branch
                if (len(options)) == 0:
                    branches += 1
                    # In the very unlikely situation that no branches can be made, stop trying to grow
                    if branches == len(self.cubes):
                        self.numParts = i
                        if self.numParts == 1:
                            self.numSensors = 0
                        stop = True
                        print("Break")
                        break
                    #Make new parent
                    print("New Branch", i)
                    new_parent    = random.choice(self.cubes[1:])
                    parentName    = new_parent.name
                    oldX          = new_parent.absolutePos[0]
                    oldY          = new_parent.absolutePos[1]
                    oldZ          = new_parent.absolutePos[2]
                    prevWidth     = new_parent.width
                    prevLength    = new_parent.length
                    prevHeight    = new_parent.height
                    prevDirection = new_parent.direction
                    options = [[1,0,0], [0,1,0], [0,0,1], [-1,0,0], [0,-1,0], [0,0,-1]]
                    options.remove(list(prevDirection*-1))
            
           
            #Joint and Cube Positions
            if stop:
                break
            jointPos = np.array([jointX, jointY, jointZ])
            relativeCubePos  = np.array([cubeX, cubeY, cubeZ]) * direction
            absoluteCubePos = np.array([newX, newY, newZ])
            
            # If not moving on z, must maintain height
            if i == 1 and abs(direction[2]) != 1: #Don't do if moving on z axis
                jointPos[2] = oldZ 
    


            #minZ Calculation
            minZ = min(minZ, newZ-height/2)
            
            #Make joint and cube
            if self.isSensor[i]:
                color = green
                newTotalSensors += 1
            else:
                color = blue
            
            jointAxis = random.choice(["1 0 0", "0 1 0", "0 0 1"])
            joint = JOINT(f'{parentName}_Part{i}', jointPos, parentName, f'Part{i}', jointAxis)
            self.parts[f'{parentName}_Part{i}'] = joint
            self.joints.append(joint)
            
            cube = CUBE(f'Part{i}', length, width, height, relativeCubePos, absoluteCubePos, color, direction) 
            self.parts[f'Part{i}'] = cube
            self.cubes.append(cube)


        self.parts['Part0'].z -= minZ
        if 'Part0_Part1' in self.parts:
            self.parts['Part0_Part1'].z -= minZ
        
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
        #Sensor Neurons
        i = 0
        for part in range(self.numParts):
            is_sensor = self.isSensor[part]
            if is_sensor:
                pyrosim.Send_Sensor_Neuron(name = i , linkName = f'Part{part}')
                i += 1
        #Motor Neurons
        j = self.numSensors
        for joint in self.joints:
            pyrosim.Send_Motor_Neuron( name = j , jointName = joint.name)
            j += 1

        for sensor in range(self.numSensors):
            for motor in range(self.numParts-1):
                pyrosim.Send_Synapse( sourceNeuronName = sensor, targetNeuronName = motor+self.numSensors , weight = self.weights[sensor][motor] )
        pyrosim.End()
    
    def Act(self, i):
        for neuronName in self.nn.Get_Neuron_Names():
            if self.nn.Is_Motor_Neuron(neuronName):
                jointName = self.nn.Get_Motor_Neurons_Joint(neuronName)
                desiredAngle = self.nn.Get_Value_Of(neuronName) * c.motorJointRange
                self.motors[jointName].Set_Value(self.robotId, desiredAngle)
    



