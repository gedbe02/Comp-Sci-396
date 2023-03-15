import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches



f = open('data/round 4/savedSymData.txt', 'r')
f2 = open('data/round 4/savedAsymData.txt', 'r')
text = f.readlines()
text2 = f2.readlines()
sym_sets = []
asym_sets = []

i = 0
a = []
b = []
while i < 2505:
    if i % 501 == 0:
        sym_sets.append(a)
        asym_sets.append(b)
        a = []
        b = []
    t = text[i]
    t2 = text2[i]
    a.append(float(t.strip()))
    b.append(float(t2.strip()))
    i+=1
sym_sets.append(a)
asym_sets.append(b)
f.close()

sym_sets = sym_sets[1:]
asym_sets = asym_sets[1:]
print("Sym:")
total = 0
total_changed = 0
for i in sym_sets:
    total += max(i)
    for j in range(len(i)):
        if j != 0 and i[j]>i[j-1]:
            total_changed += 1

print("Max:", total/5)
print("Num Changed:", total_changed)

print()

print("Asym:")
total = 0
total_changed = 0
for i in asym_sets:
    total += max(i)
    for j in range(len(i)):
        if j != 0 and i[j]>i[j-1]:
            total_changed += 1
print("Max:", total/5)
print("Num Changed:", total_changed)



'''for e in sym_sets:
    plt.plot(e, color="green", label="Symmetrical")
for e in asym_sets:
    plt.plot(e, color="blue", label="Asymmetrical")

sym = mpatches.Patch(color='green', label='Symmetrical')
asym = mpatches.Patch(color='blue', label='Asymmetrical')

plt.legend(handles=[sym, asym])
plt.xlabel('Generations')
plt.ylabel('Fitness')
plt.show()'''
