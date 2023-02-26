from solution import SOLUTION
import constants as c
import copy
import os
import random
import numpy as np

# To Do
# Change init
# Change mutate

class PARALLEL_HILL_CLIMBER:
    def __init__(self):
        os.system("rm brain*.nndf")
        os.system("rm body*.nndf")
        os.system("rm fitness*.txt")
        self.nextAvailableID = 0
        self.parents = {}
        for p in range(c.populationSize):
            self.parents[p] = SOLUTION(self.nextAvailableID)
            self.nextAvailableID += 1
        self.parents[0].Create_World()
        #exit()
        self.bestOfGens = []

    def Evolve(self):
        self.Evaluate(self.parents)
        for currentGeneration in range(c.numberOfGenerations):
            self.Evolve_For_One_Generation()
    
    def Evolve_For_One_Generation(self):
        #exit()
        self.Spawn()
        self.Mutate()
        self.Evaluate(self.children)
        self.Print()
        self.Select()
        #exit()

    
    def Spawn(self):
        self.children = {}
        for p in self.parents:
            self.children[p] = copy.deepcopy(self.parents[p])
            self.children[p].Set_ID(self.nextAvailableID)
            self.nextAvailableID += 1


    def Mutate(self):
        num_mutated = 0
        for child in self.children:
            new_parts   = random.randint(1,c.maximumAddedParts)
            new_sensors = random.randint(new_parts//2, max(new_parts-1, 0))
            if num_mutated < c.populationSize/2:
                self.children[child].Mutate(new_parts, new_sensors)
            else:
                self.children[child].Mutate(0, 0)
            #Randomly add new sensors?

            num_mutated += 1

    def Select(self):
        for p in self.parents:
            if self.children[p].fitness > self.parents[p].fitness:
                self.parents[p] = self.children[p]
        self.bestOfGens.append(self.Best_Fitness())
    
    def Best_Fitness(self):
        best_fitness = -float('inf')
        best = self.parents[0]
        for p in self.parents:
            if self.parents[p].fitness > best_fitness:
                best = self.parents[p]
                best_fitness = self.parents[p].fitness
        return best_fitness

    def Show_Best(self):
        best_fitness = -float('inf')
        best = self.parents[0]
        for p in self.parents:
            if self.parents[p].fitness > best_fitness:
                best = self.parents[p]
                best_fitness = self.parents[p].fitness
        print(f'The best fitness was {best_fitness}. Reached {best_fitness/10} y position')
        best.Start_Simulation("GUI", True)
    
    
    def Evaluate(self, solutions):
        for p in range(c.populationSize):
            solutions[p].Start_Simulation("DIRECT", False) 
        for p in range(c.populationSize):
            solutions[p].Wait_For_Simulation_To_End()
    
    def Print(self):
        print()
        for p in self.parents:
            print(self.parents[p].fitness, self.children[p].fitness)
        print()