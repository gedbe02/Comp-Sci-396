import numpy as np
import matplotlib.pyplot as plt

#x = np.linspace(-np.pi, np.pi, 201)
#plt.plot(x, abs(np.sin(x)*2*np.pi))
#plt.plot(x, [2*np.pi]*201,)
#plt.plot(x, [0]*201,)
"""x = np.load("data/sinVector.npy")
plt.plot(np.linspace(0,1000, 1000), x)
plt.xlabel('steps')
plt.ylabel('sin(x)')
plt.axis('tight')
plt.show()"""



backLegTargetValues = np.load("data/bl_targetAngles.npy")
frontLegTargetValues = np.load("data/fl_targetAngles.npy")
plt.plot(backLegTargetValues, label='back', linewidth=5)
plt.plot(frontLegTargetValues, label='front')
plt.legend()
plt.show()

