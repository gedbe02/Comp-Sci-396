import pyrosim.pyrosim as pyrosim
import pybullet_data
import constants as c
import pybullet as p
import time
import os
from world import WORLD
from snake import SNAKE

class RANDOM_GENERATION:
    def __init__(self, num_generations):
        self.generations = num_generations
        self.snakes = {}
        self.running = False
        self.Create_World()

        p.connect(p.GUI)
        p.setAdditionalSearchPath(pybullet_data.getDataPath())
        p.setGravity(c.gravity_x,c.gravity_y,c.gravity_z)
        self.world = WORLD()

    
    def Create_World(self):
        pyrosim.Start_SDF("world.sdf")
        pyrosim.End()

    def Generate_And_Run(self):
        #for i in range(self.generations):
        #    self.snakes[i] = SNAKE(i, 1, 0) #for now. make dynamic
            
        for i in range(self.generations):
            while self.running:
                time.sleep(0.01)
            print(i)
            self.snakes[i] = SNAKE(i, 1, 0) #for now. make dynamic
            pyrosim.Prepare_To_Simulate(self.snakes[i].robotId)
            self.snakes[i].Prepare_To_Sense()
            self.snakes[i].Prepare_To_Act()
            self.Run_Snake(self.snakes[i])
            self.running = True
            
        

        os.system("rm body*.urdf")
        os.system("rm brain*.urdf")

    def Run_Snake(self, snake):
        for i in range(c.steps):
            p.stepSimulation()
            snake.Sense(i) 
            snake.Think()
            snake.Act(i)
            #if self.directOrGUI == "GUI":
            time.sleep(c.sleep_time)
        
        self.running = False