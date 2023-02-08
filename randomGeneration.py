import pyrosim.pyrosim as pyrosim
import pybullet_data
import constants as c
import pybullet as p
import time
import os
from world import WORLD
from snake import SNAKE
from snakeSimulation import SNAKE_SIMILATION

class RANDOM_GENERATION:
    def __init__(self, num_generations):
        self.generations = num_generations
        self.snakes = {}
        self.running = False
        '''self.Create_World()

        p.connect(p.GUI)
        p.setAdditionalSearchPath(pybullet_data.getDataPath())
        p.setGravity(c.gravity_x,c.gravity_y,c.gravity_z)
        self.world = WORLD()'''


    def Generate_And_Run(self):
        #Need to generate world and robot before running each time
        for i in range(self.generations):
            print(i)
            sim = SNAKE_SIMILATION(i) #Generate
            sim.Run()                 #Run/Simulate
            
        os.system("rm body*.urdf")
        os.system("rm brain*.urdf")
        

        