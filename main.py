import os
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

import random
import time

#os.system("python3 search.py ")

from parallelHillCilmber import PARALLEL_HILL_CLIMBER
sym_evolutions = []
asym_evolutions = []
t1 = time.time()
num_runs = 10
for i in range(num_runs):
    ''' print("Add random seed again")
    #random.seed(i+1) 
    #random.seed(3)
    phc = PARALLEL_HILL_CLIMBER(True) # True = Symmetry
    phc.Evolve()
    #Wait for input
    #input("Show ")
    phc.Show_Best(True, True)
    sym_evolutions.append(phc.bestOfGens)'''
    random.seed(i+1) 
    if i < num_runs / 2:
        phc = PARALLEL_HILL_CLIMBER(True) # True = Symmetry
        phc.Evolve()
        #Wait for input
        #input("Show ")
        phc.Show_Best(True, True)
        sym_evolutions.append(phc.bestOfGens)
    else:
        phc = PARALLEL_HILL_CLIMBER(False) # True = Symmetry
        phc.Evolve()
        asym_evolutions.append(phc.bestOfGens)
        phc.Show_Best(True, False)


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

for e in sym_evolutions:
    plt.plot(e, color="green", label="Symmetrical")
for e in asym_evolutions:
    plt.plot(e, color="blue", label="Asymmetrical")

sym = mpatches.Patch(color='green', label='Symmetrical')
asym = mpatches.Patch(color='blue', label='Asymmetrical')

plt.legend(handles=[sym, asym])
plt.xlabel('Generations')
plt.ylabel('Fitness')
plt.show()


f = open('savedSymData.txt', 'w')
for s in sym_evolutions:
    for i in s:
        f.write(str(i) + "\n")
f.close()
f = open('savedAsymData.txt', 'w')
for a in asym_evolutions:
    for i in a:
        f.write(str(i) + "\n")
f.close()



'''
Symmetry vs. Asymmetrical
'''