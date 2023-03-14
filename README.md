# Comp-Sci-396

<h2>Symmetry vs. Asymmetry</h2>
While watching my robots evolve, I noticed that robots that seemed more symmetrical moved better. Additionally, creatures in the real world are generally symmetric, so I hypothesized that symmetric must be valuable to fitness. Thus, in this experiment, I tested the difference between symmetrical robots and asymmetrical robots. 

The symmetrical robots were bilaterally symmetric on the y axis. Their evolutionary algorithm was altered to assure symmetry. The asymmetrical robots were constructed with normal randomness. To test which type of robot was better, I ran 5 sets of symmetrical robots and 5 sets of asymmetrical robots with 500 generations and a population size of 10. 

To see a video of the experiment and its results, click [here].
Here's a sneak peek: [gif]
 [Explain experiment, AB groups, how to run experiment, how to run tests, inspiration, teaser gif, video]
  
 To run the experiment, simply run main.py (10 sets of 500 generations with population size of 10. Half the sets are symmetrical and the other half are asymmetrical.
 
 Note: The below diagrams show the x and y axis, but the z axis is also included in practice. For symmetrical robots, the z and y axes act the same, and for asymmetrical robots, all axes act the same
 
 To see a specific saved robot in action, go into testing.py, replace the robot ID with your desired robot, and hit run. #MAKE SURE WORKS
 <h3> Genotypes and Phenotypes</h3>
 Each robot's genotype is saved as a list of links and joints. The link data structure saves the name, dimensions, relative position, absolute position, sensorness, and direction. The joint data structure saves the name, relative position, parent link name, child link name, and joint axis. When the robot is mutated, the list of parts is appended to. 
 
 <br></br>
 To create the phenotype, first, the z position of the first link and all joints connected to it are changed so the robot doesn't intersect the ground. Then, the function loops through all links and joints and creates them. Every time a simulation is run, the phenotype is recreated to account for changes in the genotype. 
 
 Genotypes and phenotypes were stored the same way for symmetrical and asymmetrical robots
 <img width="785" alt="Screen Shot 2023-03-14 at 1 09 28 AM" src="https://user-images.githubusercontent.com/82680052/224911298-bfd387f2-2a57-402b-b9e2-aa191c2fd46b.png">
 <br></br>Each joint has a parent (top of arrow) and a child (bottom of arrow)


 
 <h3> Evolution </h3>
 Bodies and synapse weights change throughout evolution, but the brain remains the same (fully connected)
 <h4> Symmetrical Bodies </h4>
 [Explain how bodies are formed, what OG ones look like, how mutation works, give examples of lineages, etc.]
 The symmetrical robots are bilaterally symmetrical on the y axis. This means that if you split the robot down the middle on the y plane, each side will be identical. This was chosen instead of radial symmetry to decrease the amount of links. 
 ...
 <h5> Initalization </h5>
 To create the initial bodies, a link with random dimensions is created and made to be either a sensor (green links) or a nonsenor (blue links). Then, two new links and joints of the same random dimensions are added to the initial link. For example, if the x axis is chosen, the new links will grow out of the left and right faces, if the y axis is chosen, out of the front and back face, and if the z axis is chosen, out of the top and bottom faces. The new links are either both sensors or both nonsensors.
 
 The brain is totally connected, meaning that every motor neuron is connected to every sensor neuron. Synapse weights are then randomly generated.
 

 
 Here's some examples of initial bodies:
<img width="191" alt="Screen Shot 2023-03-14 at 11 33 49 AM" src="https://user-images.githubusercontent.com/82680052/225074292-8d64f105-dcf5-4655-95a5-4810f4a632d6.png">
<img width="210" alt="Screen Shot 2023-03-14 at 11 34 02 AM" src="https://user-images.githubusercontent.com/82680052/225074314-efc6bddc-c1a6-4ce2-8b6c-e49ab28bc3<img width="174" alt="Screen Shot 2023-03-14 at 11 34 09 AM" src="https://user-images.githubusercontent.com/82680052/225074454-8883069f-c14f-4254-ae94-4bd8da82f064.png">
a3.png">

 
 Here's a diagram of how this process is done:
<img width="1067" alt="Screen Shot 2023-03-14 at 11 30 06 AM" src="https://user-images.githubusercontent.com/82680052/225073289-5f6825b8-ebe1-4105-be6d-cf6a06a40d31.png">

 <h5> Mutation </h5>
 Every generation, populationSize children are created with different mutations. There are different types of mutations that can happen: Variations of adding links and mutating synapse weights, with about a 25% adding links and 75% chance of mutating synapse weights.
 <h6> Adding Links </h6>
 Only two links can be added at every mutation. Random dimensions for the new link are made and a random parent and direction is chosen. If creating a link in that direction doesn't overlap with any other link in the body, that direction and parent are chosen. If the link does overlap, a different direction is chosen, but if there are no more directions to choose from, a different parent is chosen. Due to the nature of the robots, this process will eventually allow the creation of a link. 
 
 Once the first link's creation is allowed, a second link with the same exact dimensions is made. If the first link's direction is on the x axis, the second link will be made on the opposite side of the robot in the opposite direction. If the direction is on the y or z axis, the second link will be made on the opposite side of the robot in the same direction. If the second link cannot be made, the first link is recalcaluated.
 
 Either both the links will be sensors or both will be nonsensors. Additionally, their joints will have identical qualities (e.g., same joint axis). 
 Random synapse weights are created for each link. If the links are sensors, additional weights are added to the motor neurons. 
 
 As the brains of these robots are fully connected, these new sensor and motor neurons are connected to every other motor and sensor neurons.
 
 Direction Meaning: Positive z direction = Top face of link, negative z direction = Bottom face of link, etc.
 
 <h6> Mutating Synapse Weights </h6>
 A motor neuron and sensor is randomly selected and their weight is randomly changed. 
 
 Here's some examples of final evolutions:
 <br></br>
 <img width="259" alt="Screen Shot 2023-03-14 at 11 10 02 AM" src="https://user-images.githubusercontent.com/82680052/225068451-b993ff11-6c64-4e77-9c13-90b65cdb48fe.png">
<img width="220" alt="Screen Shot 2023-03-14 at 11 10 48 AM" src="https://user-images.githubusercontent.com/82680052/225068483-2cff5218-b700-4c86-83e9-16a43b8981ce.png">
<img width="439" alt="Screen Shot 2023-03-14 at 11 09 07 AM" src="https://user-images.githubusercontent.com/82680052/225068522-d12f2ab6-cb5c-4a3e-942e-feb0b6cec3e3.png">
 <br></br>

Here's a step-by-step example of evolution, showing the creation of the initial body and every potential mutation type
 
 <img width="709" alt="Screen Shot 2023-03-13 at 7 38 29 PM" src="https://user-images.githubusercontent.com/82680052/224862842-450647a0-b048-4064-869d-7dfcc511767e.png">
<img width="876" alt="Screen Shot 2023-03-13 at 10 09 13 PM" src="https://user-images.githubusercontent.com/82680052/224883150-b0b6ab60-013e-45a3-8b18-907d739278c8.png">


 <h4> Asymmetrical Bodies </h4>
 [Explain how bodies are formed, what OG ones look like, how mutation works, give examples of lineages, etc.]
 The asymmetrical robots are random and asymmetrical. Every new link is randomly added independent of any other link (besides checking for overlapping and relationship to parent)
 ...
 <h5> Initalization </h5>
To create the initial bodies, a link with random dimensions is created and made to be either a sensor (green links) or a nonsenor (blue links). Then, one  link of random dimensions is added to the initial link on any of its faces. This link can either be a sensor or a nonsensor
 
 The brain is totally connected, meaning that every motor neuron is connected to every sensor neuron. Synapse weights are then randomly generated.
 
Here's some examples of initial bodies
 [Examples of Intial Bodies]
 
 Here's a diagram of how this process is done:
<img width="1016" alt="Screen Shot 2023-03-14 at 11 29 51 AM" src="https://user-images.githubusercontent.com/82680052/225073208-464ceb11-b81e-4444-8d26-2053f8522045.png">


 <h5> Mutation </h5>
  Every generation, populationSize children are created with different mutations. There are different types of mutations that can happen: Variations of adding links and mutating synapse weights, with 50% adding links and 50% mutating synapse weights.
  
   <h6> Adding Links </h6>
 1-2 links can be added at every mutation. These links are independent and are randomly shaped. 0-2 are randomly decided to be sensors. Once the dimensions of a link are made, a random parent and direction are chosen. If all directions lead to overlapping another link in the body, a different parent is chosen. By the nature of the robot, eventually a link can be made. Random synapse weights are made for this link, and if the link is a sensor, additional weights are added to the motor neurons. 
 
  As the brains of these robots are fully connected, these new sensor and motor neurons are connected to every other motor and sensor neurons.

 
 <h6> Mutating Synapse Weights </h6>
 A motor neuron and sensor is randomly selected and their weight is randomly changed. 
 
  Here's some examples of final evolutions:
   <br></br>
<img width="172" alt="Screen Shot 2023-03-14 at 11 11 16 AM" src="https://user-images.githubusercontent.com/82680052/225068846-44352adf-8836-4e54-93f3-e9e0b6603aac.png">
<img width="400" alt="Screen Shot 2023-03-14 at 11 11 40 AM" src="https://user-images.githubusercontent.com/82680052/225068874-f6920069-023f-4a78-a233-5da9d08ede68.png">
<img width="377" alt="Screen Shot 2023-03-14 at 11 12 25 AM" src="https://user-images.githubusercontent.com/82680052/225068900-3575bcda-670c-414a-821e-489d121a7a8d.png">
 <br></br>


Here's a step-by-step example of evolution, showing the creation of the initial body and every potential mutation type
  
 <img width="901" alt="Screen Shot 2023-03-13 at 3 41 43 PM" src="https://user-images.githubusercontent.com/82680052/224827536-75eaeee2-e4ed-4114-94d3-a5d332fa27bb.png">
<img width="894" alt="Screen Shot 2023-03-13 at 3 41 59 PM" src="https://user-images.githubusercontent.com/82680052/224827547-79835236-d1f4-4c9c-9b87-1a191e9d927d.png">

 
 <h4> Fitness </h4>
The fitness of a robot is the y position of the robot times 10. Simply, the farther in the positive y direction the robot goes, the more fit it is
  [Add Diagram for Selection]

 <h4> Brain Generation </h4>
 Every motor neuron is connected to every sensor neuron. This never changes.
 [Diagrams]

<h3> Results </h3>
[Graph, diagrams, images, cartoons]
After running the experiment several times, the results were:
<img width="500" src="https://user-images.githubusercontent.com/82680052/224903923-d25a4553-8e79-4cfb-aa76-5896301ce39a.png">
<img width="500" src="https://user-images.githubusercontent.com/82680052/224903939-2570391e-425a-4042-bb73-877006c3a41b.png">
<img width="500" src="https://user-images.githubusercontent.com/82680052/225068977-66abeb4e-2e57-4bd3-82c1-c992471313c7.png">


NEED TO EDIT: As per the graphs, it seems that adding symmetry isn't worse or better than normal asymmetry. The lines are overlapping and no group seems to be significantly better than the next.

DO MORE DATA ANALYSIS


<h3> Conclusions </h3>
[Conclusions, limtations, future researsh]
...
Since the synapse weights were not symmetrical, the symmetry of the body may not have been as helpful. Many symmetrical robots made ended up moving in ways that didn't utilize their symmetry due to their weight differences. 
<h4> Limitations </h4>
While the symmetrical robots have symmetrical bodies, they do not have symmetrical brains. This means that each side of the body will act differently. Thus, it's possible that this issue cause the symmetrical robots to have similar results to the asymmetrical robots. Due to the limitations of the laptop used to run these simulations, robot bodies could only be so big and simulations so long. 

<h4> Future Research </h4>
Future research on symmetrical bodies should try to make symmetrical brains along with them. The synapse weights would be randomly generated, but each symmetrical pair will share them. Additionally, every time a synapse weight is mutated, the same change would occurr for the other pair. 


 
 
Code based on reddit.com/r/ludobots. pyrosim folder taken from [Pyrosim](https://github.com/jbongard/pyrosim.git)
