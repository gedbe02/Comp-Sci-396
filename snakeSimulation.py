import pybullet as p
import pybullet_data
import pyrosim.pyrosim as pyrosim
import random

from simulation import SIMULATION
from snake import SNAKE
from world import WORLD
import constants as c



class SNAKE_SIMILATION(SIMULATION):
    def __init__(self, id):
        self.Create_World()
        #SIMULATION.__init__(self, "GUI", id, False, False)
        p.connect(p.GUI)
        p.setAdditionalSearchPath(pybullet_data.getDataPath())
        p.setGravity(c.gravity_x,c.gravity_y,c.gravity_z)
        self.world = WORLD()

        num_parts = random.randint(2,7)
        num_sensors = random.randint(1, max(num_parts-1,1))
        self.robot = SNAKE(id, num_parts, num_sensors)
        self.directOrGUI = "GUI"

        pyrosim.Prepare_To_Simulate(self.robot.robotId)
        self.robot.Prepare_To_Sense()
        self.robot.Prepare_To_Act()

        #print(f'Num Parts: {self.robot.numParts}')
        #print(self.robot.sensors)
        #print(self.robot.motors)
    
    def Create_World(self):
        pyrosim.Start_SDF("world.sdf")
        pyrosim.End()