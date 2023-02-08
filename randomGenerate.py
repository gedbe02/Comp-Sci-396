from randomGeneration import RANDOM_GENERATION
import os

os.system("rm body*.urdf")
os.system("rm brain*.urdf")

rG = RANDOM_GENERATION(2)
rG.Generate_And_Run()
