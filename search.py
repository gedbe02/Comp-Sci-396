import os
from hillclimber import HILLCLIMBER

hc = HILLCLIMBER()
hc.Show_Best()
hc.Evolve()
hc.Show_Best()

#for i in range(5):
#    os.system("python3 generate.py")
#    os.system("python3 simulate.py")


