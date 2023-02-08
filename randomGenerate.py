from randomGeneration import RANDOM_GENERATION
import os
import sys

os.system("rm body*.urdf")
os.system("rm brain*.urdf")
id = sys.argv[1] 


rG = RANDOM_GENERATION(id)
rG.Generate_And_Run()
