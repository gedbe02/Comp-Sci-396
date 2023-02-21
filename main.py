import os
#os.system("python3 search.py ")

from parallelHillCilmber import PARALLEL_HILL_CLIMBER
phc = PARALLEL_HILL_CLIMBER() 
phc.Evolve()
phc.Show_Best()

print("Done")