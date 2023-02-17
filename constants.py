import numpy as np
# Gravity
gravity_x = 0
gravity_y = 0
gravity_z = -9.8

# Steps/In Loop
steps = 500
max_force = 100
sleep_time = 1/100

# Default Values
amplitude = np.pi/8
frequency = 5
phaseOffset = 0

# Backleg Values
bl_amplitude = np.pi/8
bl_frequency = 5
bl_phaseOffset = 0

# Frontleg Values
fl_amplitude = np.pi/4
fl_frequency = 10
fl_phaseOffset = np.pi/4

# Hill Climber
numberOfGenerations = 10
populationSize = 10
numSensorNeurons = 6
numMotorNeurons = 10
motorJointRange = 0.5


# Random Generation
minSide = 0.25
maxSide = 1