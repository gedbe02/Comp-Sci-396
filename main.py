import os
import matplotlib.pyplot as plt
import random

#os.system("python3 search.py ")

from parallelHillCilmber import PARALLEL_HILL_CLIMBER
evolutions = []
for i in range(1):
    random.seed(i+1)
    phc = PARALLEL_HILL_CLIMBER() 
    #input("Start ")
    phc.Evolve()
    #Wait for input
    input("Show ")
    phc.Show_Best()
    evolutions.append(phc.bestOfGens)



print("Done")

for e in evolutions:
    plt.plot(e)
#plt.legend()
#plt.show()