import pyrosim.pyrosim as pyrosim
import numpy as np
import os
import random
import time
import constants as c
from cube import CUBE
from joint import JOINT

green = ['Green','    <color rgba="0.0 1.0 0.0 1.0"/>']
blue  = ['Blue','    <color rgba="0.0 0.5 1.0 1.0"/>']
red  = ['Red','    <color rgba="1.0 0.5 0.0 1.0"/>']
class SOLUTION:
    def __init__(self, nextAvailableID, symmetrical): 
        #self.motorJointRange = np.random.rand(c.numSensorNeurons,c.numMotorNeurons)*2-1 - Maybe add?
        self.myID = nextAvailableID
        self.isSymmetrical = symmetrical
        self.dir_dict ={"pos_x" : [1,0,0],
                        "neg_x" : [-1,0,0],
                        "pos_y" : [0,1,0],
                        "neg_y" : [0,-1,0],
                        "pos_z" : [0,0,1],
                        "neg_z" : [0,0,-1]}
        self.reverse_dir_dict ={"pos_x" : "neg_x",
                                "neg_x" : "pos_x",
                                "pos_y" : "neg_y",
                                "neg_y" : "pos_y",
                                "pos_z" : "neg_z",
                                "neg_z" : "pos_z"}

        self.Initialize_Body() 
        self.weights = np.random.rand(self.numSensors, self.numParts-1)*2-1

        
        



    def Start_Simulation(self, directOrGUI, save, sym):
        self.Create_Body()
        self.Create_Brain()

        if sym:
            folder = "sym"
        else:
            folder = "asym"
        if save:
            os.mkdir(f'results/{folder}/{self.myID}')
            os.system(f'cp brain{self.myID}.nndf results/{folder}/{self.myID}/brain{self.myID}.nndf')
            os.system(f'cp body{self.myID}.urdf results/{folder}/{self.myID}/body{self.myID}.urdf')
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
    
    def Create_Body(self):
        # Temporarily alter absolute z's by Min Z
        self.parts['Part0'].z -= self.minZ
        for p in self.parts:
            part = self.parts[p]
            if part.isJoint and part.doAbsolute:
                part.z -= self.minZ

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
    
    def Initialize_Body(self):
        self.numParts = 1 #Part0
        if self.isSymmetrical:
            partsToAdd = 2 #Change?
            numParts = partsToAdd + 1

            self.numSensors = random.randint(1,3) #Either 1 sensor (Part0), 2 sensors (Part1,2), or 3 sensors (Part1,2,3)
            if self.numSensors == 2:
                self.isSensor = [False]
            else:
                self.isSensor = [True]
        else:
            partsToAdd = random.randint(c.maxInitialParts//2, c.maxInitialParts)
            numParts = partsToAdd + 1

            self.numSensors = random.randint(numParts//2, numParts-1)
            self.isSensor = [random.choice([True, False])]
        

        


        # Part0
        if self.isSensor[0]:
            color = green
            sensorsToAdd = self.numSensors - 1
        else:
            color = blue
            sensorsToAdd = self.numSensors

        self.minSide = 100 * c.minSide #/100
        self.maxSide = 100 * c.maxSide #/100

        self.parts = {}
        self.cubes = {}
        self.joints = {}

        length = random.randint(self.minSide,self.maxSide)/100
        width  = random.randint(self.minSide,self.maxSide)/100
        height = random.randint(self.minSide,self.maxSide)/100
        x = 0
        y = 0
        z = 0.5
        cubePos = [x,y,z]

        cube = CUBE("Part0", length, width, height, cubePos, cubePos, color, None, True, 0, True)
        cube.isPair = True #Part0 can't be paired with other links
        self.parts["Part0"] = cube
        self.cubes["Part0"] = cube

        #Trying to get minZ: Lowest z coordinate of body (Lowest edge)
        self.minZ = z - height/2 #Z coord of Center of Part0 - its "radius"
        
        # Add other parts
        output = self.Add_Parts(partsToAdd, sensorsToAdd) ###
        addedParts = output[0]
        addedSensors = output[1]
        self.numParts += addedParts
        ##
        if addedParts == 0:
            if self.numSensors == 3:
                self.numSensors = 1
            elif self.numSensors == 2:
                self.numSensors = 0
        ##
        #self.weights = np.random.rand(self.numSensors, self.numParts-1)*2-1


    
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
        if parent.direction in self.dir_dict:
            prevDirection = self.dir_dict[parent.direction]
        else:
            prevDirection = None
        doAbsolute    = parent.isOriginal

        if doAbsolute:
            oldCenter = parent.absolutePos
        else:
            oldCenter = (prevDirection*np.array([parent.length, parent.width, parent.height])/2)

        length = random.randint(self.minSide,self.maxSide)/100
        width  = random.randint(self.minSide,self.maxSide)/100
        height = random.randint(self.minSide,self.maxSide)/100

        #Direction Options
        options = ["pos_x", "neg_x", "pos_y", "neg_y", "pos_z", "neg_z"]
        if not doAbsolute:
            #options.remove(list(prevDirection*-1))
            options.remove(self.reverse_dir_dict[parent.direction])
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
            dir = random.choice(options)
            direction = self.dir_dict[dir]
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
            for cub_key in self.cubes:
                cub = self.cubes[cub_key]
                intersecting |= cub.overlapping([newX, newY, newZ], [length, width, height])
            if intersecting:
                options.remove(dir)

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
        self.joints[f'{parentName}_Part{i}'] = joint
        
        cube = CUBE(f'Part{i}', length, width, height, relativeCubePos, absoluteCubePos, color, dir, False, -1, -1) 
        #if pairing:
            # If parent and child share a direction, they are pairs
         #   parent.isPair = True
            #cube.isPair = True
            #SET CHILD AND PARENT ISPAIR TRUE
        self.parts[f'Part{i}'] = cube
        self.cubes[f'Part{i}'] = cube

        return 1

        # Takes in previous center (relative or absolute) and a random parent
    
    
    def Make_Sym_Parts(self, parent, i):
        length = random.randint(self.minSide,self.maxSide)/100
        width  = random.randint(self.minSide,self.maxSide)/100
        height = random.randint(self.minSide,self.maxSide)/100
        jointAxis = random.choice(["1 0 0", "0 1 0", "0 0 1"])
        #Direction Options
        options = ["pos_x", "neg_x", "pos_y", "neg_y", "pos_z", "neg_z"]
        if not parent.isCenter: #CHANGE TO ISCENTER
            options.remove(self.reverse_dir_dict[parent.direction])
            options.remove(parent.direction)
        #else:
        #    options = ["pos_x", "neg_x"]

        while len(options) != 0:
            for k in range(2):
                parentName    = parent.name
                oldX          = parent.absolutePos[0]
                oldY          = parent.absolutePos[1]
                oldZ          = parent.absolutePos[2]
                prevWidth     = parent.width
                prevLength    = parent.length
                prevHeight    = parent.height
                if parent.direction in self.dir_dict:
                    prevDirection = self.dir_dict[parent.direction]
                else:
                    prevDirection = None
                doAbsolute    = parent.isOriginal

                if doAbsolute:
                    oldCenter = parent.absolutePos
                else:
                    oldCenter = (prevDirection*np.array([parent.length, parent.width, parent.height])/2)

                
                
                # Try to make new cube/joint
                intersecting = True
                while intersecting: 
                    intersecting = False

                    if k == 0:
                        dir = random.choice(options)
                    direction = self.dir_dict[dir]

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
                    #print("INTERSECT CHECK")
                    #print("OG:", [newX, newY, newZ])
                    for cub_key in self.cubes:
                        cub = self.cubes[cub_key]
                        #print(cub_key, cub.absolutePos)
                        #print([length, width, height], [cub.length, cub.width, cub.height])
                        #print(cub_key)
                        #if cub_key == "Part2":
                        #    print(cub.absolutePos, [cub.length, cub.width, cub.height])
                         #   print([newX, newY, newZ], [length, width, height])

                        #rint("TEST ZONE:")
                        intersecting |= cub.overlapping([newX, newY, newZ], [length, width, height])

                        #print(intersecting)
                    if intersecting:
                        if k == 1:
                            options = []
                        else:
                            options.remove(dir)

                    #If branch reaches end point, start a new branch
                    if (len(options)) == 0:
                        if k == 1:
                            del self.parts[firstCube]
                            del self.cubes[firstCube]
                            
                            del self.parts[firstJoint]
                            del self.joints[firstJoint]
                        return 0 #Parent doesn't work
                
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
                else:
                    color = blue
            
                
                joint = JOINT(f'{parentName}_Part{i}', jointPos, parentName, f'Part{i}', jointAxis, doAbsolute)
                self.parts[f'{parentName}_Part{i}'] = joint
                self.joints[f'{parentName}_Part{i}'] = joint
                
                # Assure pairing numbering works
                if k == 0:
                    pair = i + 1
                else: #k == 1
                    pair = i - 1
                
                if parent.isCenter and dir not in ["pos_x", "neg_x"] and (dir == parent.direction or parent.direction == None):
                    is_center = True
                else:
                    is_center = False
                cube = CUBE(f'Part{i}', length, width, height, relativeCubePos, absoluteCubePos, color, dir, False, pair, is_center) 

                self.parts[f'Part{i}'] = cube
                self.cubes[f'Part{i}'] = cube

                #If Need to Delete first part
                firstJoint = f'{parentName}_Part{i}'
                firstCube = f'Part{i}'
                #
                if parent.isCenter and not is_center:
                    parent = parent
                else:
                    parent = self.parts[f'Part{parent.symPair}']
                # Next Direction
                if dir in ["pos_x", "neg_x"] or is_center:
                    dir = self.reverse_dir_dict[dir]
                #else: Stay the same
                i += 1 #Assure that this works right

                
            return 1 #is this correct indent?
        
        return 0 #If this is reached, the parent doesn't work


       

    # Adds #newParts parts with #newSensors of them being sensors
    def Add_Parts(self, newParts, newSensors):
        # Decide Sensors
        is_sensor = np.full((1,newParts), False)[0]
        is_sensor[random.sample(range(newParts), newSensors)] = True
        #
        successful_parts = 0
        successful_sensors = 0
        #
        if self.isSymmetrical:
            j = 0
            while j < newParts:
                i = self.numParts + j
                self.isSensor.append(is_sensor[j])
                self.isSensor.append(is_sensor[j+1])

                potential_parents = list(self.cubes.keys())
                parents_remaining = len(potential_parents)
                success = False
                while len(potential_parents) != 0:
                    parent = self.cubes[random.choice(potential_parents)]
                    
                    potential_parents.remove(parent.name)
                    if self.Make_Sym_Parts(parent, i):
                        successful_parts += 2
                        if is_sensor[j]:
                            successful_sensors += 2
                        success = True
                        break
                    parents_remaining -= 1
                if not success:
                    self.isSensor.pop()
                    self.isSensor.pop()
                    newParts -= 2
                else:
                    j += 2


        else: # Asymmetry
            j = 0
            while j < newParts:
                i = self.numParts + j
                self.isSensor.append(is_sensor[j])

                potential_parents = list(self.cubes.keys())
                parents_remaining = len(potential_parents)
                success = False
                while len(potential_parents) != 0:
                    parent = self.cubes[random.choice(potential_parents)]
                    
                    potential_parents.remove(parent.name)
                    if self.Make_Part(parent, i):
                        #Can we see an example of a robot that cant keep building?
                        successful_parts += 1
                        if is_sensor[j]:
                            successful_sensors += 1
                        success = True
                        break
                    parents_remaining -= 1
                if not success:
                    self.isSensor.pop()
                    newParts -= 1
                else:
                    j += 1
        
        return [successful_parts, successful_sensors]
        #
        
   # TO DO 
    # Add newParts body parts OR mutate a weight
    def Mutate(self, newParts, newSensors): 
        # If no parts are being added, mutate a weight instead
        if newParts == 0:
            row = random.randint(0,self.numSensors-1)
            col = random.randint(0,self.numParts-2)
            self.weights[row][col] = random.random() * 2 - 1
            return

        # Mutating Body
        output = self.Add_Parts(newParts, newSensors)
        addedParts = output[0]
        addedSensors = output[1]
                
        # Update weights
        # Adding new motor neurons to weights
        for i in range(addedParts): 
            newCol = np.random.rand(1, self.numSensors)*2*-1
            newCol = np.array([[x] for x in newCol[0]])
            self.weights = np.append(self.weights, newCol, axis=1)

        # Adding new sensor neurons to weights
        for i in range(addedSensors):
            newRow = np.random.rand(1, self.numParts+newParts-1)*2*-1
            self.weights = np.append(self.weights, newRow, axis=0)
        
        self.numParts   += addedParts
        self.numSensors += addedSensors

    def Create_Brain(self):
        pyrosim.Start_NeuralNetwork(f'brain{self.myID}.nndf')
        #Sensor Neurons
        i = 0
        a = []
        for c in range(len(self.cubes)):
            is_sensor = self.isSensor[c]
            cube = self.cubes[f'Part{c}']
            if is_sensor:
                pyrosim.Send_Sensor_Neuron(name = i , linkName = cube.name)
                a.append(i)
                i += 1
        #Motor Neurons
        j = self.numSensors
        b = []
        for joint_key in self.joints:
            joint = self.joints[joint_key]
            pyrosim.Send_Motor_Neuron( name = j , jointName = joint.name)
            b.append(j)
            j += 1

        for sensor in range(self.numSensors):
            for motor in range(self.numParts-1):
                pyrosim.Send_Synapse( sourceNeuronName = sensor, targetNeuronName = motor+self.numSensors , weight = self.weights[sensor][motor] )
        pyrosim.End()
   
    def Set_ID(self, id):
        self.myID = id