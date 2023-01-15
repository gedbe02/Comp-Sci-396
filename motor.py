import pyrosim.pyrosim as pyrosim
import pybullet as p
import numpy as np
import constants as c

class MOTOR:
    def __init__(self, jointName):
        self.jointName = jointName
        
        self.Prepare_To_Act()
    
    def Prepare_To_Act(self):
        print(self.jointName)
        if self.jointName == b'Torso_BackLeg':
            self.amplitude = c.amplitude
            self.frequency = c.frequency
            self.phaseOffset = c.phaseOffset
        else:
            self.amplitude = c.amplitude
            self.frequency = c.frequency/2
            self.phaseOffset = c.phaseOffset

        self.motorAngles = np.array(list(map(lambda x: self.amplitude * np.sin(self.frequency * x + self.phaseOffset), 
                                 np.linspace(0, 2*np.pi, c.steps))))
    
    def Set_Value(self, robotId, desiredAngle):
        pyrosim.Set_Motor_For_Joint(
            bodyIndex = robotId,
            jointName = self.jointName,
            controlMode = p.POSITION_CONTROL,
            targetPosition = desiredAngle,
            maxForce = c.max_force)
    
    def Save_Values(self):
        np.save(f'data/{self.jointName}MotorValues', self.motorAngles)