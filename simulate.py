from simulation import SIMULATION
import constants as c
import sys 

directOrGUI = sys.argv[1] 
solutionID = sys.argv[2]
test = sys.argv[3] == "test"
testABot = sys.argv[4] == "testABot"

simulation = SIMULATION(directOrGUI, solutionID, test, testABot) 
simulation.Run()
simulation.Get_Fitness()