import os
import matplotlib.pyplot as plt

#os.system("python3 search.py ")

from parallelHillCilmber import PARALLEL_HILL_CLIMBER
phc = PARALLEL_HILL_CLIMBER() 
input("Start ")
phc.Evolve()
#Wait for input
input("Show ")
phc.Show_Best()

print("Done")
# Change this if we want to save best body

plt.plot(phc.bestOfGens)
plt.legend()
plt.show()