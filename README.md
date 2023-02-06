# Comp-Sci-396

<h2>Bipedal Walking:</h2>

 The goal of this robot is to walk in the positive y direction without falling for as long as possible. 
 
 <img width="266" alt="Screen Shot 2023-02-05 at 7 14 46 PM" src="https://user-images.githubusercontent.com/82680052/216859877-b27a3854-4928-4670-9fad-63e66d26de8c.png">
  
  The robot has 2 arms and two legs. For each arm, there's a shoulder joint connected to an upper arm, which is connected to a lower arm by an elbow joint.
  For each leg, there's a hip joint connected to an upper leg, which is connected to lower leg by a knee joint. Additionally, there's a foot connected to
  the lower leg by an ankle joint. All these limbs are connected to the main torso, a rectangular prism. 
  
  The arms, legs, and feet all had their own motor joint range. 

<h2>Fitness Function:</h2>
 
 The Fitness of a robot (shown in Get_Fitness method in robot.py) is based on the farthest y position the robot got to before falling and Average reward 
 the robot got for standing. 

 When a robot's z position drops below 2, it is considered as falling/fallen, and that y value is saved in self.lastSpot. 
 At every step, if the robot's z position is above 2, it gets a reward of 10 added to self.totalStandReward, if not, it gets a punishment of -5.
 
 When calculating fitness, self.lastSpot is multiplied by 50 and self.totalStandReward is divided by the number of steps (Average stand reward) and 
 multiplied by .3. The sum of these values is the robot's fitness. If a child's fitness is greater than its parent, it is selected. 
 
 
