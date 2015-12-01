from ps3b_precompiled_27 import *
import numpy
import random
import pylab

def simulationWithDrug(numViruses, maxPop, maxBirthProb, clearProb, resistances,
                       mutProb, numTrials):
    steps = 300
    treatOnStep = 150
    trialResultsTot = [[] for s in range(steps)]
    trialResultsRes = [[] for s in range(steps)]
    for __ in range(numTrials):
        viruses = [ResistantVirus(maxBirthProb, clearProb,
                                  resistances.copy(), mutProb)
                   for v in range(numViruses)]
        patient = TreatedPatient(viruses, maxPop)
        for step in range(steps):
            if step == treatOnStep:
                patient.addPrescription("guttagonol")
            patient.update()
            trialResultsTot[step].append(patient.getTotalPop())
            trialResultsRes[step].append(patient.getResistPop(["guttagonol"]))
    resultsSummaryTot = [sum(l) / float(len(l)) for l in trialResultsTot]
    resultsSummaryRes = [sum(l) / float(len(l)) for l in trialResultsRes]
    pylab.plot(resultsSummaryTot, label="Total Virus Population")
    pylab.plot(resultsSummaryRes, label="Resistant Virus Population")
    pylab.title("ResistantVirus simulation")
    pylab.xlabel("time step")
    pylab.ylabel("# viruses")
    pylab.legend()
    pylab.show()


random.seed(0)
print '\n simulationWithDrug(1, 10, 1.0, 0.0, {}, 1.0, 5) \n'
simulationWithDrug(1, 10, 1.0, 0.0, {}, 1.0, 5)
print '\n simulationWithDrug(1, 20, 1.0, 0.0, {"guttagonol": True}, 1.0, 5) \n'
simulationWithDrug(1, 20, 1.0, 0.0, {"guttagonol": True}, 1.0, 5)
print '\n simulationWithDrug(75, 100, .8, 0.1, {"guttagonol": True}, 0.8, 1) \n'
simulationWithDrug(75, 100, .8, 0.1, {"guttagonol": True}, 0.8, 10)