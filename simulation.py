import pybullet as p
import pybullet_data
import pyrosim.pyrosim as pyrosim
import time


import constants as c
from world import WORLD
from robot import ROBOT

class SIMULATION:
    def __init__(self):
        self.physicsClient = p.connect(p.GUI)
        p.setAdditionalSearchPath(pybullet_data.getDataPath())
        p.setGravity(c.gravity_x,c.gravity_y,c.gravity_z)

        self.world = WORLD()
        self.robot = ROBOT()

        pyrosim.Prepare_To_Simulate(self.robot.robotId)
        self.robot.Prepare_To_Sense()
        self.robot.Prepare_To_Act()
    
    def Run(self):
        for i in range(c.steps):
            p.stepSimulation()
            self.robot.Sense(i)
            self.robot.Think()
            self.robot.Act(i)

            time.sleep(c.sleep_time)

    def __del__(self):
        p.disconnect()  


       

        

