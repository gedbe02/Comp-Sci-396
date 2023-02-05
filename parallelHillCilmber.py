from solution import SOLUTION
import constants as c
import copy
import os

class PARALLEL_HILL_CLIMBER:
    def __init__(self):
        os.system("rm brain*.nndf")
        os.system("rm fitness*.txt")
        self.nextAvailableID = 0
        self.parents = {}
        for p in range(c.populationSize):
            self.parents[p] = SOLUTION(self.nextAvailableID)
            self.nextAvailableID += 1
        #exit()

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
        for c in self.children:
            self.children[c].Mutate()

    def Select(self):
        for p in self.parents:
            if self.children[p].fitness > self.parents[p].fitness:
                self.parents[p] = self.children[p]
    
    def Show_Best(self):
        best_fitness = -float('inf')
        best = self.parents[0]
        for p in self.parents:
            if self.parents[p].fitness > best_fitness:
                best = self.parents[p]
                best_fitness = self.parents[p].fitness
        print(best_fitness)
        best.Start_Simulation("GUI")
        os.system(f'cp brain{best.myID}.nndf results/brain{best.myID}.nndf')
    
    def Evaluate(self, solutions):
        for p in range(c.populationSize):
            solutions[p].Start_Simulation("DIRECT")
        for p in range(c.populationSize):
            solutions[p].Wait_For_Simulation_To_End()
    
    def Print(self):
        print()
        for p in self.parents:
            print(self.parents[p].fitness, self.children[p].fitness)
        print()