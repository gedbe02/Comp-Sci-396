# Comp-Sci-396

<h2>Symmetry vs. Asymmetry</h2>
While watching my robots evolve, I noticed that robots that seemed more symmetrical moved better. Additionally, creatures in the real world are generally symmetric, so I hypothesized that symmetric must be valuable to fitness. Thus, in this experiment, I tested the difference between symmetrical robots and asymmetrical robots. 

The symmetrical robots were bilaterally symmetric on the y axis. Their evolutionary algorithm was altered to assure symmetry. The asymmetrical robots were constructed with normal randomness. To test which type of robot was better, I ran 5 sets of symmetrical robots and 5 sets of asymmetrical robots with 500 generations and a population size of 10. 

To see a video of the experiment and its results, click [here].
Here's a sneak peek: [gif]
 [Explain experiment, AB groups, how to run experiment, how to run tests, inspiration, teaser gif, video]
  
 To run the experiment, simply run main.py (10 sets of 500 generations with population size of 10. Half the sets are symmetrical and the other half are asymmetrical.
 
 To see a specific saved robot in action, go into testing.py, replace the robot ID with your desired robot, and hit run. *MAKE SURE WORKS
 
 <h3> Evolution </h3>
 <h4> Symmetrical Bodies </h4>
 [Explain how bodies are formed, what OG ones look like, how mutation works, give examples of lineages, etc.]
 The symmetrical robots are bilaterally symmetrical on the y axis. This means that if you split the robot down the middle on the y plane, each side will be identical. This was chosen instead of radial symmetry to decrease the amount of links. 
 ...
 <h5> Initalization </h5>
 To create the initial bodies, a link with random dimensions is created and made to be either a sensor (green links) or a nonsenor (blue links). Then, two new links and joints of the same random dimensions are added to the initial link. For example, if the x axis is chosen, the new links will grow out of the left and right faces, if the y axis is chosen, out of the front and back face, and if the z axis is chosen, out of the top and bottom faces. The new links are either both sensors or both nonsensors.
 
 The brain is totally connected, meaning that every motor neuron is connected to every sensor neuron. Synapse weights are then randomly generated.
 
 Here's some examples of initial bodies
 [Examples of Intial Bodies]
 <h5> Mutation </h5>
 Every generation, populationSize children are created with different mutations. There are different types of mutations that can happen: Variations of adding links and mutating synapse weights, with about a 25% adding links and 75% chance of mutating synapse weights.
 <h6> Adding Links </h6>
 Only two links can be added at every mutation. Random dimensions for the new link are made and a random parent and direction is chosen. If creating a link in that direction doesn't overlap with any other link in the body, that direction and parent are chosen. If the link does overlap, a different direction is chosen, but if there are no more directions to choose from, a different parent is chosen. Due to the nature of the robots, this process will eventually allow the creation of a link. 
 
 Once the first link's creation is allowed, a second link with the same exact dimensions is made. If the first link's direction is on the x axis, the second link will be made on the opposite side of the robot in the opposite direction. If the direction is on the y or z axis, the second link will be made on the opposite side of the robot in the same direction. If the second link cannot be made, the first link is recalcaluated.
 
 Either both the links will be sensors or both will be nonsensors. Additionally, their joints will have identical qualities (e.g., same joint axis). 
 Random synapse weights are created for each link. If the links are sensors, additional weights are added to the motor neurons. 
 
 Direction Meaning: Positive z direction = Top face of link, negative z direction = Bottom face of link, etc.
 
 [Example of Mutation] ADD IMAGE
 
 <h6> Mutating Synapse Weights </h6>
 A motor neuron and sensor is randomly selected and their weight is randomly changed. 
 
 
 <h5> Diagram </h5>
 <img width="709" alt="Screen Shot 2023-03-13 at 7 38 29 PM" src="https://user-images.githubusercontent.com/82680052/224862842-450647a0-b048-4064-869d-7dfcc511767e.png">
<img width="876" alt="Screen Shot 2023-03-13 at 10 09 13 PM" src="https://user-images.githubusercontent.com/82680052/224883150-b0b6ab60-013e-45a3-8b18-907d739278c8.png">


 <h4> Asymmetrical Bodies </h4>
 [Explain how bodies are formed, what OG ones look like, how mutation works, give examples of lineages, etc.]
 The asymmetrical robots are random and asymmetrical. Every new link is randomly added independent of any other link (besides checking for overlapping and relationship to parent)
 ...
 <h5> Initalization </h5>
To create the initial bodies, a link with random dimensions is created and made to be either a sensor (green links) or a nonsenor (blue links). Then, one  link of random dimensions is added to the initial link on any of its faces. This link can either be a sensor or a nonsensor
 
 The brain is totally connected, meaning that every motor neuron is connected to every sensor neuron. Synapse weights are then randomly generated.
 <h5> Mutation </h5>
  Every generation, populationSize children are created with different mutations. There are different types of mutations that can happen: Variations of adding links and mutating synapse weights, with 50% adding links and 50% mutating synapse weights.
  
   <h6> Adding Links </h6>
 1-2 links can be added at every mutation. These links are independent and are randomly shaped. 0-2 are randomly decided to be sensors. Once the dimensions of a link are made, a random parent and direction are chosen. If all directions lead to overlapping another link in the body, a different parent is chosen. By the nature of the robot, eventually a link can be made. Random synapse weights are made for this link, and if the link is a sensor, additional weights are added to the motor neurons. 
 
 
 [Example of Mutation] ADD IMAGE
 
 <h6> Mutating Synapse Weights </h6>
 A motor neuron and sensor is randomly selected and their weight is randomly changed. 
  

 <h5> Diagram </h5>
 <img width="901" alt="Screen Shot 2023-03-13 at 3 41 43 PM" src="https://user-images.githubusercontent.com/82680052/224827536-75eaeee2-e4ed-4114-94d3-a5d332fa27bb.png">
<img width="894" alt="Screen Shot 2023-03-13 at 3 41 59 PM" src="https://user-images.githubusercontent.com/82680052/224827547-79835236-d1f4-4c9c-9b87-1a191e9d927d.png">

 
 <h4> Fitness </h4>
 [Fitness Function Explanation]
 
 <h4> Brain Generation </h4>
 Every motor neuron is connected to every sensor neuron. 
 [Diagrams]

<h3> Results </h3>
[Graph, diagrams, images, cartoons]
![Figure_1](https://user-images.githubusercontent.com/82680052/224827577-aa34d5d7-b020-457e-8bfc-9b2dea60b22d.png)

<h3> Conclusions </h3>
[Conclusions, limtations, future researsh]

 
 
Code based on reddit.com/r/ludobots. pyrosim folder taken from [Pyrosim](https://github.com/jbongard/pyrosim.git)
