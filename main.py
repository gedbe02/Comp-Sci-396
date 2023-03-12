import os
import matplotlib.pyplot as plt
import random
import time

#os.system("python3 search.py ")

from parallelHillCilmber import PARALLEL_HILL_CLIMBER
evolutions = []
t1 = time.time()
for i in range(1):
    print("Add random seed again")
    #random.seed(i+1) 
    phc = PARALLEL_HILL_CLIMBER(True) # True = Symmetry
    #input("Start ")
    phc.Evolve()
    #Wait for input
    input("Show ")
    phc.Show_Best(False)
    evolutions.append(phc.bestOfGens)
t2 = time.time()


if True:
    delta_t = round(t2-t1)
    hours = delta_t // 360
    minutes = (delta_t - hours*360) // 60
    seconds = (delta_t - hours*360 - minutes*60)


    h = str(hours)
    if len(h) == 1:
        h = "0" + h
    m = str(minutes)
    if len(m) == 1:
        m = "0" + m
    s = str(seconds)
    if len(s) == 1:
        s = "0" + s

print(f'Done. It took {h}:{m}:{s}')

#for e in evolutions:
#    plt.plot(e)
#plt.legend()
#plt.show()


'''
Symmetry vs. Asymmetrical
'''