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
red  = ['Red','    <color rgba="1.0 0.5 0.0 1.0"/>']
class SOLUTION:
    def __init__(self, nextAvailableID): 
        #self.weights = np.random.rand(c.numSensorNeurons,c.numMotorNeurons)*2-1 
        #self.motorJointRange = np.random.rand(c.numSensorNeurons,c.numMotorNeurons)*2-1 - Maybe add?
        self.myID = nextAvailableID

        # Random Generation #
        # All parents shoudl initally start with 2 parts and 1-2 sensors, so it can actually move
        self.numParts = 2
        self.numSensors = random.randint(1,2)
        self.isSensor = np.full((1,self.numParts), False)[0]
        self.isSensor[random.sample(range(self.numParts), self.numSensors)] = True
        self.isSensor = list(self.isSensor)

        self.weights = np.random.rand(self.numSensors, self.numParts-1)*2-1

        self.Initialize_Body()



    def Start_Simulation(self, directOrGUI, save):
        self.Create_Body()
        self.Create_Brain()
        if save:
            os.system(f'cp brain{self.myID}.nndf results/brain{self.myID}.nndf')
            os.system(f'cp body{self.myID}.urdf results/body{self.myID}.urdf')
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
        # Temporarily alter absolute z's by Min Z
        self.parts['Part0'].z -= self.minZ
        for p in self.parts:
            part = self.parts[p]
            if part.isJoint and part.doAbsolute:
                part.z -= self.minZ
        #if 'Part0_Part1' in self.parts:
        #    self.parts['Part0_Part1'].z -= self.minZ

        pyrosim.Start_URDF(f'body{self.myID}.urdf')
        for name in self.parts:
            part = self.parts[name]
            if part.isJoint:
                part.Send_Joint()
            else:
                part.Send_Cube()

        pyrosim.End()

        # Revert z's Back
        self.parts['Part0'].z += self.minZ
        for p in self.parts:
            part = self.parts[p]
            if part.isJoint and part.doAbsolute:
                part.z += self.minZ
        #if 'Part0_Part1' in self.parts:
        #    self.parts['Part0_Part1'].z += self.minZ
    
    def Initialize_Body(self):
        #Part0
        #newTotalSensors = 0
        if self.isSensor[0]:
            color = green
            #newTotalSensors += 1
        else:
            color = blue
        #color = red

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

        cube = CUBE("Part0", length, width, height, cubePos, cubePos, color, None, True)
        cube.isPair = True #Part0 can't be paired with other links
        self.parts["Part0"] = cube
        self.cubes.append(cube)

        #Trying to get minZ: Lowest z coordinate of body (Lowest edge)
        self.minZ = z - height/2 #Z coord of Center of Part0 - its "radius"

        #oldCenter = cubePos
        
        parent = self.cubes[0]
        self.Make_Part(parent, 1)

    # Takes in previous center (relative or absolute) and a random parent
    def Make_Part(self, parent, i):
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
        doAbsolute    = parent.isOriginal

        if doAbsolute:
            oldCenter = parent.absolutePos
        else:
            oldCenter = (parent.direction*np.array([parent.length, parent.width, parent.height])/2)

        length = random.randint(self.minSide,self.maxSide)/100
        width  = random.randint(self.minSide,self.maxSide)/100
        height = random.randint(self.minSide,self.maxSide)/100

        #Direction Options
        options = [[1,0,0], [0,1,0], [0,0,1], [-1,0,0], [0,-1,0], [0,0,-1]]
        if not doAbsolute:
            options.remove(list(prevDirection*-1))
            ####
            self.test_dims = [length, width, height]
            self.test_options = options.copy()
            self.tests = []
            ####

        
        # Try to make new cube/joint
        intersecting = True
        pairing = True
        while intersecting: 
            intersecting = False
            #if not parent.isPair and list(prevDirection) in options: #Trying to bias longer limbs
            #    direction = prevDirection
                #print(f'{parentName} to Part{i}')
                #parent.isPair = True
           # else:
            direction = np.array(random.choice(options))
             #   pairing = False

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

            ####
            if not doAbsolute:
                self.tests.append([newX, newY, newZ, direction])
            ####
            #Check for overlapping cubes
            for cub in self.cubes:
                intersecting |= cub.overlapping([newX, newY, newZ], [length, width, height])
            if intersecting:
                options.remove(list(direction))

            #If branch reaches end point, start a new branch
            if (len(options)) == 0:
                return 0
        
        #Joint and Cube Positions
        jointPos = np.array([jointX, jointY, jointZ])
        relativeCubePos  = np.array([cubeX, cubeY, cubeZ]) * direction
        absoluteCubePos = np.array([newX, newY, newZ])
        
        # If not moving on z, must maintain height
        # Need this because x and y start at 0, but z doesn't. Honestly, to get rid of this, make xyz=000
        if doAbsolute and abs(direction[2]) != 1: #Don't do if moving on z axis
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
        joint = JOINT(f'{parentName}_Part{i}', jointPos, parentName, f'Part{i}', jointAxis, doAbsolute)
        self.parts[f'{parentName}_Part{i}'] = joint
        self.joints.append(joint)
        
        cube = CUBE(f'Part{i}', length, width, height, relativeCubePos, absoluteCubePos, color, direction, False) 
        #if pairing:
            # If parent and child share a direction, they are pairs
         #   parent.isPair = True
            #cube.isPair = True
            #SET CHILD AND PARENT ISPAIR TRUE
        self.parts[f'Part{i}'] = cube
        self.cubes.append(cube)

        return 1

    # Add newParts body parts OR mutate a weight
    # IMPORTANT: Make sure new weight is added for new parts
    def Mutate(self, newParts, newSensors): 
        # If no parts are being added, mutate a weight instead
        if newParts == 0:
            row = random.randint(0,self.numSensors-1)
            col = random.randint(0,self.numParts-2)
            self.weights[row][col] = random.random() * 2 - 1
            return

        # Decide Sensors
        is_sensor = np.full((1,newParts), False)[0]
        is_sensor[random.sample(range(newParts), newSensors)] = True
        # Mutating Body
        for j in range(newParts):
            i = self.numParts + j
            self.isSensor.append(is_sensor[j])

            potential_parents = self.cubes.copy()
            parents_remaining = len(potential_parents)
            while len(potential_parents) != 0:
                #if is_sensor[j]: 
                #    self.numSensors += 1
                parent    = random.choice(potential_parents)
                #oldCenter= np.array([0,0,0])
                
                potential_parents.remove(parent)
                if self.Make_Part(parent, i):
                    #Can we see an example of a robot that cant keep building?
                    break
                parents_remaining -= 1
            
            #Debug this if need
            if parents_remaining == 0:
                print("\nNeed to debug situations when body cannot be expanded", i, len(self.cubes), self.numParts)
                print(self.test_options)
                print(self.test_dims)
                print(self.tests)
                for cube in self.cubes:
                    cube.print()
                exit()
                #If bug occurs here, will likely need to subtract from self.numParts
                '''
                # In the very unlikely situation that no branches can be made, stop trying to grow
                            if len(potential_parents) == 0:
                                self.numParts = i
                                if self.numParts == 1:
                                    self.numSensors = 0
                                stop = True
                                print("Break")
                                break
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

        # Update weights
        # Adding new motor neurons to weights
        for i in range(newParts): 
            newCol = np.random.rand(1, self.numSensors)*2*-1
            newCol = np.array([[x] for x in newCol[0]])
            self.weights = np.append(self.weights, newCol, axis=1)

        # Adding new sensor neurons to weights
        for i in range(newSensors):
            newRow = np.random.rand(1, self.numParts+newParts-1)*2*-1
            self.weights = np.append(self.weights, newRow, axis=0)
        
        self.numParts   += newParts
        self.numSensors += newSensors

    def Create_Brain(self):
        pyrosim.Start_NeuralNetwork(f'brain{self.myID}.nndf')
        #Sensor Neurons
        i = 0
        a = []
        for cube in range(len(self.cubes)):
            is_sensor = self.isSensor[cube]
            if is_sensor:
                pyrosim.Send_Sensor_Neuron(name = i , linkName = self.cubes[cube].name)
                a.append(i)
                i += 1
        #Motor Neurons
        j = self.numSensors
        b = []
        for joint in self.joints:
            pyrosim.Send_Motor_Neuron( name = j , jointName = joint.name)
            b.append(j)
            j += 1
        #print("\n",self.cubes, self.joints, "\nThis should be sequential: ", a+b, "Also: ", self.numParts, self.numSensors)

        for sensor in range(self.numSensors):
            for motor in range(self.numParts-1):
                pyrosim.Send_Synapse( sourceNeuronName = sensor, targetNeuronName = motor+self.numSensors , weight = self.weights[sensor][motor] )
        pyrosim.End()
    def Set_ID(self, id):
        self.myID = id