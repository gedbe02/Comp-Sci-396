import pybullet as p
import pybullet_data
import time
import pyrosim.pyrosim as pyrosim
import numpy
import random

physicsClient = p.connect(p.GUI)
p.setAdditionalSearchPath(pybullet_data.getDataPath())

p.setGravity(0,0,-9.8)
planeId = p.loadURDF("plane.urdf")
robotId = p.loadURDF("body.urdf")

p.loadSDF("world.sdf")

backLegSensorValues = numpy.zeros(10000)
frontLegSensorValues = numpy.zeros(10000)

pyrosim.Prepare_To_Simulate(robotId)
pi = 3.14159

targetAngles = numpy.sin(numpy.array((0., 30., 45., 60., 90.)) * numpy.pi / 180. )
for i in range(10000):
    p.stepSimulation()
    backLegSensorValues[i] = pyrosim.Get_Touch_Sensor_Value_For_Link("BackLeg")
    frontLegSensorValues[i] = pyrosim.Get_Touch_Sensor_Value_For_Link("FrontLeg")

    pyrosim.Set_Motor_For_Joint(
    bodyIndex = robotId,
    jointName = b"Torso_BackLeg",
    controlMode = p.POSITION_CONTROL,
    targetPosition = random.random()%(pi/8.0),
    maxForce = 200)

    """pyrosim.Set_Motor_For_Joint(
    bodyIndex = robotId,
    jointName = b"Torso_FrontLeg",
    controlMode = p.POSITION_CONTROL,
    targetPosition = random.random()%(pi/8.0),
    maxForce = 200)"""

    time.sleep(1/2000)

p.disconnect()
numpy.save('data/backLegSensorValues', backLegSensorValues)
numpy.save('data/frontLegSensorValues', frontLegSensorValues)
