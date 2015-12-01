# 6.00.2x Problem Set 4

import numpy
import random
import pylab
from ps3b import *

#
# PROBLEM 1
#        
def simulationDelayedTreatment(numTrials):
    """
    Runs simulations and make histograms for problem 1.

    Runs numTrials simulations to show the relationship between delayed
    treatment and patient outcome using a histogram.

    Histograms of final total virus populations are displayed for delays of 300,
    150, 75, 0 timesteps (followed by an additional 150 timesteps of
    simulation).

    numTrials: number of simulation runs to execute (an integer)
    """
    
    # TODO




def simulationWithDrug(numViruses, maxPop, maxBirthProb, clearProb, resistances,
                       mutProb, numTrials):
    """
    Runs simulations and plots graphs for problem 5.

    For each of numTrials trials, instantiates a patient, runs a simulation for
    150 timesteps, adds guttagonol, and runs the simulation for an additional
    150 timesteps.  At the end plots the average virus population size
    (for both the total virus population and the guttagonol-resistant virus
    population) as a function of time.

    numViruses: number of ResistantVirus to create for patient (an integer)
    maxPop: maximum virus population for patient (an integer)
    maxBirthProb: Maximum reproduction probability (a float between 0-1)
    clearProb: maximum clearance probability (a float between 0-1)
    resistances: a dictionary of drugs that each ResistantVirus is resistant to
                 (e.g., {'guttagonol': False})
    mutProb: mutation probability for each ResistantVirus particle
             (a float between 0-1).
    numTrials: number of simulation runs to execute (an integer)

    """
    # popList = list of 300 zeros - for the total population after each step
    popList = [0.0]*300
    # resList = list of 300 zeros - for the resistant population
    resList = [0.0]*300

    # trials loop (numTrials times)
    for trial in range(numTrials):
    #     instantiate a new list of viruses of length numViruses
        viruses = [ResistantVirus(maxBirthProb, clearProb, resistances, mutProb) for v in range(numViruses)]
    #     instantiate a new Patient
        patient = TreatedPatient(viruses, maxPop)
    #     timesteps loop - first 150 steps
        for step in range(150):
    #         call to update the Patient and get the new total population. Increment popList[i].
            patient.update()
            popList[step] += patient.getTotalPop()
    #         call to get new resistant population. Increment resList [i]
            resList[step] += patient.getResistPop(['guttagonol'])
        # prescription call to add new drug
        patient.addPrescription('guttagonol')
        # timesteps loop - next 150 steps
        for step in range(150, 300):
        #     call to update the Patient and get the new total population. Increment popList[i]..
            patient.update()
            popList[step] += patient.getTotalPop()
        #   call to get new resistant population. Increment resList[i]..
            resList[step] += patient.getResistPop(['guttagonol'])

    # divide popList and resList by numTrials to find average populations at each step.
    for i in range(len(popList)):
        popList[i] /= float(numTrials)
        resList[i] /= float(numTrials)
    pylab.plot(popList, label = 'Total Virus Population')
    pylab.plot(resList, label = 'guttagonol-resistant virus particles')
    pylab.title('ResistantVirus simulation')
    pylab.xlabel('time step')
    pylab.ylabel('# viruses')
    pylab.legend()
    pylab.show()

#
# PROBLEM 2
#
def simulationTwoDrugsDelayedTreatment(numTrials):
    """
    Runs simulations and make histograms for problem 2.

    Runs numTrials simulations to show the relationship between administration
    of multiple drugs and patient outcome.

    Histograms of final total virus populations are displayed for lag times of
    300, 150, 75, 0 timesteps between adding drugs (followed by an additional
    150 timesteps of simulation).

    numTrials: number of simulation runs to execute (an integer)
    """
    # TODO
