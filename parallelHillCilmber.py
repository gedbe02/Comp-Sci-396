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
    def __init__(self, symmetrical):
        os.system("rm brain*.nndf")
        os.system("rm body*.nndf")
        os.system("rm fitness*.txt")
        self.nextAvailableID = 0
        self.parents = {}
        for p in range(c.populationSize):
            self.parents[p] = SOLUTION(self.nextAvailableID, symmetrical)
            self.nextAvailableID += 1
        self.parents[0].Create_World()
        #exit()
        self.bestOfGens = []
        self.isSymmetrical = symmetrical

    def Evolve(self):
        self.Evaluate(self.parents)
        for currentGeneration in range(c.numberOfGenerations):
            #
            #self.Show_Best(currentGeneration, True)
            #
            self.bestOfGens.append(self.Best_Fitness())
            self.Evolve_For_One_Generation()
        self.bestOfGens.append(self.Best_Fitness())
    
    def Evolve_For_One_Generation(self):
        self.Spawn()
        self.Mutate()
        self.Evaluate(self.children)
        self.Print()
        self.Select()

    
    def Spawn(self):
        self.children = {}
        for p in self.parents:
            self.children[p] = copy.deepcopy(self.parents[p])
            self.children[p].Set_ID(self.nextAvailableID)
            self.nextAvailableID += 1

    def Mutate(self):
        num_mutated = 0
        for child in self.children:
            if self.isSymmetrical:
                new_parts   = random.choice([0,2]) 
                new_sensors = random.randint(0,4)
                if new_sensors != 0:
                    new_sensors = 2
            else:
                new_parts   = random.randint(1,c.maximumAddedParts)
                new_sensors = random.randint(new_parts//2, max(new_parts-1, 0))
            change_weight = False
            if self.children[child].numParts > 11:
                new_parts = 0
                new_sensors = 0
                change_weight = True
            if num_mutated < c.populationSize/2 and not change_weight:
                self.children[child].Mutate(new_parts, new_sensors)
            else:
                self.children[child].Mutate(0, 0)

            num_mutated += 1

    def Select(self):
        for p in self.parents:
            if self.children[p].fitness > self.parents[p].fitness:
                self.parents[p] = self.children[p]
            #print("REVERT SELECT FUNCTION")
            #self.parents[p] = self.children[p]
        #self.bestOfGens.append(self.Best_Fitness())
    
    def Best_Fitness(self):
        best_fitness = -float('inf')
        best = self.parents[0]
        for p in self.parents:
            if self.parents[p].fitness > best_fitness:
                best = self.parents[p]
                best_fitness = self.parents[p].fitness
        
        return best_fitness

    def Show_Best(self, save, sym): 
        best_fitness = -float('inf')
        best = self.parents[0]
        for p in self.parents:
            if self.parents[p].fitness > best_fitness:
                best = self.parents[p]
                best_fitness = self.parents[p].fitness
        #
        if (type(save)==int):
            best.Start_Simulation("NO", save, sym)
        else:    
        #
            print(f'The best fitness was {best_fitness}. Reached {best_fitness/10} y position')
            best.Start_Simulation("GUI", save, sym)
    
    def Evaluate(self, solutions):
        for p in range(c.populationSize):
            solutions[p].Start_Simulation("DIRECT", False, False) 
        for p in range(c.populationSize):
            solutions[p].Wait_For_Simulation_To_End()
    
    def Print(self):
        print()
        for p in self.parents:
            print(self.parents[p].fitness, self.children[p].fitness)
        print()