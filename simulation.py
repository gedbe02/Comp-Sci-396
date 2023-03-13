import pybullet as p
import pybullet_data
import pyrosim.pyrosim as pyrosim
import time


import constants as c
from world import WORLD
from robot import ROBOT

class SIMULATION:
    def __init__(self, directOrGUI, solutionID, test, evolved):
        self.directOrGUI = directOrGUI
        self.test = test
        self.evolved = evolved
        if directOrGUI == "DIRECT":
            self.physicsClient = p.connect(p.DIRECT)
        else:
            p.connect(p.GUI)
        p.configureDebugVisualizer(p.COV_ENABLE_GUI,0)
        p.setAdditionalSearchPath(pybullet_data.getDataPath())
        p.setGravity(c.gravity_x,c.gravity_y,c.gravity_z)
        self.world = WORLD()

        self.robot = ROBOT(solutionID, test, evolved) 

        pyrosim.Prepare_To_Simulate(self.robot.robotId) 
        self.robot.Prepare_To_Sense()
        self.robot.Prepare_To_Act()
    
    def Run(self):
        for i in range(c.steps): 
            p.stepSimulation()
            self.robot.Sense(i) 
            self.robot.Think()
            self.robot.Act(i)
            if self.directOrGUI == "GUI":
                time.sleep(c.sleep_time)
    
    def Get_Fitness(self):
        self.robot.Get_Fitness()
        
    def __del__(self): 
        p.disconnect()  


       

        

