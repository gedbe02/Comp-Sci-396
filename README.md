# Comp-Sci-396

<h2>Random Creatures:</h2>

 The goal of this program is to create robots with randomly sized and positioned links in 3 Dimenions. Each creature has a random number of parts (Between 7 and 15, as per constants.py) and a random number of sensors (Between 1 and NumParts-1). Sensor links are green, normal links are blue. Each link's length, width, and height are randomly selected (Between 0.25 and 1, as per constants.py). Each link is connected by a joint that either moves on the x, y, or z joint axis. 
  
 To see it in action, click <a href="https://www.youtube.com/watch?v=Gg0BlUyQODs">here</a>. It has 6 random generations with the last one shown moving
  
 To run the experiment, simply run main.py
 
 <h3> Code Explanation </h3>
 <h4> Body Generation </h4>
 The body of the creature is created in the Create_Body method in creature.py. The number of parts and sensors are passed into the initializer and
 saved to the object (CREATURE intialized in randomGeneration.py). The minimum and maximum size of each side is defined in constants.py. 
 
 To make the body, the initial body is made before of the loop. The position and dimensions of this part is decided and then saved in self.cubes as
 a CUBE class. Then, within the loop, each additional body part and joint is made. When the second part is being made, the joint between Part0 and Part1
 must be absolute, so the creation behavior is slightly different (joint position is based on Part0's position). 
 
 For every new cube, a random parent cube is chosen and a random side of that parent to build off of (For simplicity sake, besides for Part1, each new part's parent must have a joint upstream). After creating the part's relative position, its absolute position is calculated. Then, a check is done to make sure the new part doesn't overlap any previous parts. If the cube does overlap with another, a different side is chosen to build off of. If all sides lead to overlaps, a different parent is chosen. If all potential parents cannot be built off of, the body creation is cut short and the number of parts and sensors is updated. Every joint has a random chance of moving in the x, y, or z axis. 
 
 
 
 <h4> Brain Generation </h4>
 Every motor neuron is connected to every sensor neuron. 

<h3> Examples of Creatures </h3>
  <img width="539" alt="Screen Shot 2023-02-20 at 3 34 44 PM" src="https://user-images.githubusercontent.com/82680052/220201686-716abbe3-824c-4bee-be23-489bd1b1e7e9.png">

<img width="664" alt="Screen Shot 2023-02-20 at 3 32 22 PM" src="https://user-images.githubusercontent.com/82680052/220201706-092bfa7a-fc6c-4d5f-a646-210534b60970.png">

  <img width="379" alt="Screen Shot 2023-02-20 at 3 34 56 PM" src="https://user-images.githubusercontent.com/82680052/220201715-6fcca301-7b34-41e6-8cd9-5969471e8680.png">

 
 
Code based on reddit.com/r/ludobots. pyrosim folder taken from [Pyrosim](https://github.com/jbongard/pyrosim.git)
