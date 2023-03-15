# Comp-Sci-396

<h1>Symmetry vs. Asymmetry</h1>
While watching my robots evolve, I noticed that robots that seemed more symmetrical moved better. Additionally, creatures in the real world are generally symmetric, so I hypothesized that symmetry must be valuable to fitness. Thus, in this experiment, I tested the difference between symmetrical robots and asymmetrical robots. 

The symmetrical robots were bilaterally symmetric on the y axis. Their evolutionary algorithm was altered to assure symmetry. The asymmetrical robots were constructed with normal randomness. To test which type of robot was better, I ran 5 sets of symmetrical robots and 5 sets of asymmetrical robots with 500 generations and a population size of 10. 

To see a video of the experiment and its results, click <a href="https://youtu.be/-9nzSqWoJsk">here</a>.

Here's a sneak peek showing the symmetrical robots: 
<br></br>
![Teaser Gif](https://user-images.githubusercontent.com/82680052/225194220-cf7bee9e-1bca-4a4f-afcf-4784840ee833.gif)
  
 To run the experiment, simply run main.py (10 sets of 500 generations with population size of 10. Half the sets are symmetrical and the other half are asymmetrical.
 
 Note: The below diagrams show the x and y axis, but the z axis is also included in practice. For symmetrical robots, the z and y axes act the same, and for asymmetrical robots, all axes act the same
 
 To see a specific saved robot in action, go into runABot.py, replace the robot ID with your desired robot ID (IDs are under results/to_run), and hit run. 
 
 <h3> Genotypes and Phenotypes</h3>
 Each robot's genotype is saved as a list of links and joints. The link data structure saves the name, dimensions, relative position, absolute position, sensorness, and direction. The joint data structure saves the name, relative position, parent link name, child link name, and joint axis. When the robot is mutated, the list of parts is appended to. 
 
 <br></br>
 To create the phenotype, first, the z position of the first link and all joints connected to it are changed so the robot doesn't intersect the ground. Then, the function loops through all links and joints and creates them. Every time a simulation is run, the phenotype is recreated to account for changes in the genotype. 
 
 Genotypes and phenotypes were stored the same way for symmetrical and asymmetrical robots
 <img width="785" alt="Screen Shot 2023-03-14 at 1 09 28 AM" src="https://user-images.githubusercontent.com/82680052/224911298-bfd387f2-2a57-402b-b9e2-aa191c2fd46b.png">
 <br></br>Each joint has a parent (top of arrow) and a child (bottom of arrow)


 
 <h2> Evolution </h2>
 Bodies and synapse weights change throughout evolution, but the brain remains the same (fully connected)
 
 <h3> Symmetrical Bodies </h3>
 The symmetrical robots are bilaterally symmetrical on the y axis. This means that if you split the robot down the middle on the y plane, each side will be identical. This was chosen instead of radial symmetry to decrease the amount of links. 

 <h4> Initalization </h4>
 To create the initial bodies, a link with random dimensions is created and made to be either a sensor (green links) or a nonsenor (blue links). Then, two new links and joints of the same random dimensions are added to the initial link. For example, if the x axis is chosen, the new links will grow out of the left and right faces, if the y axis is chosen, out of the front and back face, and if the z axis is chosen, out of the top and bottom faces. The new links are either both sensors or both nonsensors.
 
 The brain is totally connected, meaning that every motor neuron is connected to every sensor neuron. Synapse weights are then randomly generated.
 

 
 Here's some examples of initial bodies:
 <br></br>
<img width="191" alt="Screen Shot 2023-03-14 at 11 33 49 AM" src="https://user-images.githubusercontent.com/82680052/225074292-8d64f105-dcf5-4655-95a5-4810f4a632d6.png">
<img width="210" alt="Screen Shot 2023-03-14 at 11 34 02 AM" src="https://user-images.githubusercontent.com/82680052/225074314-efc6bddc-c1a6-4ce2-8b6c-e49ab28bc3a3.png">
<img width="174" alt="Screen Shot 2023-03-14 at 11 34 09 AM" src="https://user-images.githubusercontent.com/82680052/225074649-89b301f3-f671-4474-94ad-bc52ab284d32.png">

 
 Here's a diagram of how this process is done:
<img width="1067" alt="Screen Shot 2023-03-14 at 11 30 06 AM" src="https://user-images.githubusercontent.com/82680052/225073289-5f6825b8-ebe1-4105-be6d-cf6a06a40d31.png">

 <h4> Mutation </h4>
 Every generation, populationSize children are created with different mutations. There are different types of mutations that can happen: Variations of adding links and mutating synapse weights, with about a 50% adding links and 50% chance of mutating synapse weights.
 
 <h5> Adding Links: </h5>
 Only two links can be added at every mutation. Random dimensions for the new link are made and a random parent and direction is chosen. If creating a link in that direction doesn't overlap with any other link in the body, that direction and parent are chosen. If the link does overlap, a different direction is chosen, but if there are no more directions to choose from, a different parent is chosen. Due to the nature of the robots, this process will eventually allow the creation of a link. 
 
 Once the first link's creation is allowed, a second link with the same exact dimensions is made. If the first link's direction is on the x axis, the second link will be made on the opposite side of the robot in the opposite direction. If the direction is on the y or z axis, the second link will be made on the opposite side of the robot in the same direction. If the second link cannot be made, the first link is recalcaluated.
 
 Either both the links will be sensors or both will be nonsensors. Additionally, their joints will have identical qualities (e.g., same joint axis). 
 Random synapse weights are created for each link. If the links are sensors, additional weights are added to the motor neurons. 
 
 As the brains of these robots are fully connected, these new sensor and motor neurons are connected to every other motor and sensor neurons.
 
 Direction Meaning: Positive z direction = Top face of link, negative z direction = Bottom face of link, etc.
 
 <h5> Mutating Synapse Weights: </h5>
 A motor neuron and sensor is randomly selected and their weight is randomly changed. 
 <br></br>
 
 Here's some examples of final evolutions:
 <br></br>
 <img width="259" alt="Screen Shot 2023-03-14 at 11 10 02 AM" src="https://user-images.githubusercontent.com/82680052/225068451-b993ff11-6c64-4e77-9c13-90b65cdb48fe.png">
<img width="220" alt="Screen Shot 2023-03-14 at 11 10 48 AM" src="https://user-images.githubusercontent.com/82680052/225068483-2cff5218-b700-4c86-83e9-16a43b8981ce.png">
<img width="439" alt="Screen Shot 2023-03-14 at 11 09 07 AM" src="https://user-images.githubusercontent.com/82680052/225068522-d12f2ab6-cb5c-4a3e-942e-feb0b6cec3e3.png">
 <br></br>

Here's a step-by-step example of evolution, showing the creation of the initial body and every potential mutation type
 
 <img width="876" alt="Screen Shot 2023-03-13 at 7 38 29 PM" src="https://user-images.githubusercontent.com/82680052/224862842-450647a0-b048-4064-869d-7dfcc511767e.png">
<img width="876" alt="Screen Shot 2023-03-13 at 10 09 13 PM" src="https://user-images.githubusercontent.com/82680052/224883150-b0b6ab60-013e-45a3-8b18-907d739278c8.png">

Lineage Example:
<br></br>

<img width="816" alt="Screen Shot 2023-03-14 at 3 48 45 PM" src="https://user-images.githubusercontent.com/82680052/225132832-c46e6f63-fab8-432b-bb61-cda33d04d543.png">


 <h3> Asymmetrical Bodies </h3>
 The asymmetrical robots are random and asymmetrical. Every new link is randomly added independent of any other link (besides checking for overlapping and relationship to parent)
 
 <h4> Initalization </h4>
To create the initial bodies, a link with random dimensions is created and made to be either a sensor (green links) or a nonsenor (blue links). Then, one  link of random dimensions is added to the initial link on any of its faces. This link can either be a sensor or a nonsensor. If another link is chosen to be made, its dimensions will be random and its parent can be the initial link or the second link
 
 The brain is totally connected, meaning that every motor neuron is connected to every sensor neuron. Synapse weights are then randomly generated.
 
Here's some examples of initial bodies:
<br></br>
<img width="216" alt="Screen Shot 2023-03-14 at 11 36 03 AM" src="https://user-images.githubusercontent.com/82680052/225075581-fd0f037d-6d52-4841-a999-0ea320ed34a2.png">
<img width="151" alt="Screen Shot 2023-03-14 at 11 36 12 AM" src="https://user-images.githubusercontent.com/82680052/225075601-90497818-a085-48dc-a4c7-d33efc56fa0b.png">
<img width="203" alt="Screen Shot 2023-03-14 at 11 39 10 AM" src="https://user-images.githubusercontent.com/82680052/225075629-e7393581-e67a-47fc-bbc1-d1ee0941a7fc.png">

 
 Here's a diagram of how this process is done:
<img width="1016" alt="Screen Shot 2023-03-14 at 11 29 51 AM" src="https://user-images.githubusercontent.com/82680052/225073208-464ceb11-b81e-4444-8d26-2053f8522045.png">

Lineage Example:
<br></br>
<img width="915" alt="Screen Shot 2023-03-14 at 4 01 07 PM" src="https://user-images.githubusercontent.com/82680052/225135239-1b9b4be9-1222-4c3f-8e90-e4de4659317c.png">


 <h4> Mutation </h4>
  Every generation, populationSize children are created with different mutations. There are different types of mutations that can happen: Variations of adding links and mutating synapse weights, with 50% adding links and 50% mutating synapse weights.
  
   <h5> Adding Links: </h5>
 1-2 links can be added at every mutation. These links are independent and are randomly shaped. 0-2 are randomly decided to be sensors. Once the dimensions of a link are made, a random parent and direction are chosen. If all directions lead to overlapping another link in the body, a different parent is chosen. By the nature of the robot, eventually a link can be made. Random synapse weights are made for this link, and if the link is a sensor, additional weights are added to the motor neurons. 
 
  As the brains of these robots are fully connected, these new sensor and motor neurons are connected to every other motor and sensor neurons.

 
 <h5> Mutating Synapse Weights: </h5>
 A motor neuron and sensor is randomly selected and their weight is randomly changed. 
 <br></br>
 
  Here's some examples of final evolutions:
   <br></br>
<img width="172" alt="Screen Shot 2023-03-14 at 11 11 16 AM" src="https://user-images.githubusercontent.com/82680052/225068846-44352adf-8836-4e54-93f3-e9e0b6603aac.png">
<img width="400" alt="Screen Shot 2023-03-14 at 11 11 40 AM" src="https://user-images.githubusercontent.com/82680052/225068874-f6920069-023f-4a78-a233-5da9d08ede68.png">
<img width="377" alt="Screen Shot 2023-03-14 at 11 12 25 AM" src="https://user-images.githubusercontent.com/82680052/225068900-3575bcda-670c-414a-821e-489d121a7a8d.png">
 <br></br>


Here's a step-by-step example of evolution, showing the creation of the initial body and every potential mutation type
  
 <img width="901" alt="Screen Shot 2023-03-13 at 3 41 43 PM" src="https://user-images.githubusercontent.com/82680052/224827536-75eaeee2-e4ed-4114-94d3-a5d332fa27bb.png">
<img width="894" alt="Screen Shot 2023-03-13 at 3 41 59 PM" src="https://user-images.githubusercontent.com/82680052/224827547-79835236-d1f4-4c9c-9b87-1a191e9d927d.png">

 <h3> Brain Generation and Evolution </h3>
 Every motor neuron is connected to every sensor neuron. When a new link is added, its associated motor neuron is added to the brain and conncted to all other sensor neurons. If the new link is a sensor, its associated sensor neuron is connected to all other motor neurons (including its own).
 
 This logic is the same for both symmetrical and asymmetrical robots
<img width="765" alt="Screen Shot 2023-03-14 at 4 29 15 PM" src="https://user-images.githubusercontent.com/82680052/225141273-311b08f4-8b37-4e05-b79d-24cdc042f415.png">

 
 <h3> Fitness </h3>
The fitness of a robot is the y position of the robot times 10. Simply, the farther in the positive y direction the robot goes, the more fit it is

<h4> Parallel Hill Climber </h4>
To choose which robots are chosen for the next generation, a parallel hill climber (PHC) is used. When the PHC is created, populationSize (10 in this experiment) random bodies are created, the parents. Then, the children are created by copying the parents and then mutating them (e.g., Add one link, add two links, mutate synapse weight, etc.). The fitness of each parent and child pair are compared, and the better robot becomes a parent for the next generation. This loop occurs numberOfGeneration times (500 in this experiment) and once it ends, the best parent out of the last generation is chosen as the final evolution.
<br></br>
While body creation is different for symmetrical and asymmetrical robots, the PHC operates the same way.
<img width="543" alt="Screen Shot 2023-03-14 at 12 14 59 PM" src="https://user-images.githubusercontent.com/82680052/225085360-95746d09-895f-40cc-aa42-303d3f3c27f5.png">




<h2> Results </h2>

<h3> Data </h3>
After running the experiment two times, the results were:
<br></br>
Run 1:
<br></br>
<img width="500" src="https://user-images.githubusercontent.com/82680052/224903939-2570391e-425a-4042-bb73-877006c3a41b.png">
<br></br>
Average Final Symmetrical Fitness: 69.76, 
Number of Improvements: 77, 

Average Final Asymmetrical Fitness: 70.60, 
Number of Improvements: 80

Run 2:
<br></br>
<img width="500" src="https://user-images.githubusercontent.com/82680052/225068977-66abeb4e-2e57-4bd3-82c1-c992471313c7.png">
<br></br>
Average Final Symmetrical Fitness: 65.93, 
Number of Improvements: 111

Average Final Asymmetrical Fitness: 69.35, 
Number of Improvements: 83

<h3> Examples of Final Robots </h3>
<h4> Symmetrical Robots </h4>
<img width="272" alt="Screen Shot 2023-03-14 at 6 41 34 PM" src="https://user-images.githubusercontent.com/82680052/225166220-0b1d5de0-9764-43a4-98ca-2354d984ef72.png">
<img width="312" alt="Screen Shot 2023-03-14 at 6 41 55 PM" src="https://user-images.githubusercontent.com/82680052/225166236-345fe75d-2dac-461e-83dd-3f33b5bc507d.png">
<img width="194" alt="Screen Shot 2023-03-14 at 7 38 39 PM" src="https://user-images.githubusercontent.com/82680052/225173898-36b3a010-9f37-43fe-a486-ef37b309cd9f.png">


<h4> Asymmetrical Robots </h4>
<img width="445" alt="Screen Shot 2023-03-14 at 6 42 26 PM" src="https://user-images.githubusercontent.com/82680052/225166244-df406c2e-cc22-4579-9bd4-f2c6e68f3158.png">
<img width="344" alt="Screen Shot 2023-03-14 at 6 42 13 PM" src="https://user-images.githubusercontent.com/82680052/225166251-4d255d9d-f739-4d5d-9f7d-234db7c43146.png">


As per the graphs, it seems that adding symmetry isn't worse or better than normal asymmetry. The lines are overlapping and no group seems to be significantly better than the next. Additionally, both groups ended up with about the same average fitness. Symmetrical and asymmetrical robots evolved a similar amount of times in Run 1, but Symmetrical robots had more changes in Run 2. However, this aspect seems to not be important to being more fit than the other group. 

Symmetrical robots also ended up being smaller usually than asymmetrical robots


<h3> Conclusion </h3>
The results of the experiment demonstrate that adding bilateral symmetry doesn't necessarily improve fitness. Symmetrical and Asymmetrical robots usually ended up with relatively equal fitnesses on average and neither seemed to be better in that regard. However, the symmetrical robots were smaller, meaning they had to rely more on moving fast rather than the slower strides of the larger asymmetrical robots. Nevertheless, symmetry, in the way it was utilized in this experiment, did not lead to better results.  

<h4> Limitations </h4>
While the symmetrical robots have symmetrical bodies, they do not have symmetrical synapse weights. This means that each side of the body will act differently. Thus, it's possible that this issue caused the symmetrical robots to have similar results to the asymmetrical robots. Due to the limitations of the laptop used to run these simulations, robot bodies could only be so big and simulations so long. 

Since the synapse weights were not symmetrical, the symmetry of the body may not have been as helpful. Many symmetrical robots made ended up moving in ways that didn't utilize their symmetry due to their weight differences. 

<h4> Future Research </h4>
Future research on symmetrical bodies should try to make symmetrical brains along with them. The synapse weights would be randomly generated, but each symmetrical pair will share them. Additionally, every time a synapse weight is mutated, the same change would occurr for the other pair. 


 <br></br>
 
Code based on reddit.com/r/ludobots. pyrosim folder taken from [Pyrosim](https://github.com/jbongard/pyrosim.git)
