import pybullet as p
import pybullet_data
import time
import pyrosim.pyrosim as pyrosim
import numpy as np
import random

physicsClient = p.connect(p.GUI)
p.setAdditionalSearchPath(pybullet_data.getDataPath())

p.setGravity(0,0,-9.8)
planeId = p.loadURDF("plane.urdf")
robotId = p.loadURDF("body.urdf")

p.loadSDF("world.sdf")

backLegSensorValues = np.zeros(10000)
frontLegSensorValues = np.zeros(10000)

pyrosim.Prepare_To_Simulate(robotId)
pi = 3.14159

#targetAngles = abs(np.sin(np.linspace(-np.pi, np.pi, 201))*2*np.pi)
bl_amplitude = np.pi/8
bl_frequency = 5
bl_phaseOffset = 0

bl_targetAngles = np.array(list(map(lambda x: bl_amplitude * np.sin(bl_frequency * x + bl_phaseOffset), 
                                 np.linspace(0, 2*np.pi, 1000))))

fl_amplitude = np.pi/4
fl_frequency = 10
fl_phaseOffset = np.pi/4

fl_targetAngles = np.array(list(map(lambda x: fl_amplitude * np.sin(fl_frequency * x + fl_phaseOffset), 
                                 np.linspace(0, 2*np.pi, 1000))))
#p.save('data/fl_targetAngles', fl_targetAngles)
#np.save('data/bl_targetAngles', bl_targetAngles)

for i in range(1000):
    p.stepSimulation()
    backLegSensorValues[i] = pyrosim.Get_Touch_Sensor_Value_For_Link("BackLeg")
    frontLegSensorValues[i] = pyrosim.Get_Touch_Sensor_Value_For_Link("FrontLeg")

    pyrosim.Set_Motor_For_Joint(
    bodyIndex = robotId,
    jointName = b"Torso_BackLeg",
    controlMode = p.POSITION_CONTROL,
    targetPosition = bl_targetAngles[i],
    maxForce = 200)

    pyrosim.Set_Motor_For_Joint(
    bodyIndex = robotId,
    jointName = b"Torso_FrontLeg",
    controlMode = p.POSITION_CONTROL,
    targetPosition = fl_targetAngles[i],
    maxForce = 200)

    time.sleep(1/2000)

p.disconnect()
np.save('data/backLegSensorValues', backLegSensorValues)
np.save('data/frontLegSensorValues', frontLegSensorValues)
