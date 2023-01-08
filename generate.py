import pyrosim.pyrosim as pyrosim

length = 1
width = 1
height = 1

x = 0
y = 0
z = 0.5

pyrosim.Start_SDF("boxes.sdf")

for row in range(5):
    for col in range(5):
        for i in range(10):
            pyrosim.Send_Cube(name="Box"+str(i)+"_"+str("row")+"_"+str(col), pos=[x,y,z] , size=[length,width,height])
            z += 1
            length *= .9
            width *= .9
            height *= .9
        y+=1
        z=0.5
        length,width,height = 1,1,1
    x+=1
    y=0
    z=0.5

pyrosim.End()


