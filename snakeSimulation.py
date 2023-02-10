import pybullet as p
import pybullet_data

from simulation import SIMULATION
from snake import SNAKE
import pyrosim.pyrosim as pyrosim
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

        self.robot = SNAKE(id, 4, 2)# for now. make random later
        self.directOrGUI = "GUI"

        pyrosim.Prepare_To_Simulate(self.robot.robotId)
        self.robot.Prepare_To_Sense()
        self.robot.Prepare_To_Act()
    
    def Create_World(self):
        pyrosim.Start_SDF("world.sdf")
        pyrosim.End()