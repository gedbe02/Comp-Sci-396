from randomGeneration import RANDOM_GENERATION
import os
import sys

id = sys.argv[1] 

rG = RANDOM_GENERATION(id)
rG.Generate_And_Run()
