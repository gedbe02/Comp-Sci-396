import os

os.system("rm body*.urdf")
os.system("rm brain*.urdf")

for i in range(5):
    os.system("python3 randomGenerate.py " + str(i))

os.system("rm body*.urdf")
os.system("rm brain*.urdf")