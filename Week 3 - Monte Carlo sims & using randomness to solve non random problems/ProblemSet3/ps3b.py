# Problem Set 3: Simulating the Spread of Disease and Virus Population Dynamics 

import numpy
import random
import pylab

# #
# # '''
# # Begin helper code
# # '''
#
class NoChildException(Exception):
    """
    NoChildException is raised by the reproduce() method in the SimpleVirus
    and ResistantVirus classes to indicate that a virus particle does not
    reproduce. You can use NoChildException as is, you do not need to
    modify/add any code.
    """

'''
End helper code
'''

#
# # PROBLEM 2
#
class SimpleVirus(object):

    """
    Representation of a simple virus (does not model drug effects/resistance).
    """
    def __init__(self, maxBirthProb, clearProb):
        """
        Initialize a SimpleVirus instance, saves all parameters as attributes
        of the instance.
        maxBirthProb: Maximum reproduction probability (a float between 0-1)
        clearProb: Maximum clearance probability (a float between 0-1).
        """
        self.maxBirthProb = maxBirthProb
        self.clearProb = clearProb

    def getMaxBirthProb(self):
        """
        Returns the max birth probability.
        """
        return self.maxBirthProb

    def getClearProb(self):
        """
        Returns the clear probability.
        """
        return self.clearProb

    def doesClear(self):
        """ Stochastically determines whether this virus particle is cleared from the
        patient's body at a time step.
        returns: True with probability self.getClearProb and otherwise returns
        False.
        """
        if random.random() <= self.getClearProb():
            return True
        else:
            return False


    def reproduce(self, popDensity):
        """
        Stochastically determines whether this virus particle reproduces at a
        time step. Called by the update() method in the Patient and
        TreatedPatient classes. The virus particle reproduces with probability
        self.maxBirthProb * (1 - popDensity).

        If this virus particle reproduces, then reproduce() creates and returns
        the instance of the offspring SimpleVirus (which has the same
        maxBirthProb and clearProb values as its parent).

        popDensity: the population density (a float), defined as the current
        virus population divided by the maximum population.

        returns: a new instance of the SimpleVirus class representing the
        offspring of this virus particle. The child should have the same
        maxBirthProb and clearProb values as this virus. Raises a
        NoChildException if this virus particle does not reproduce.
        """
        if random.random() <= self.maxBirthProb * (1 - popDensity):
            return SimpleVirus(self.maxBirthProb, self.clearProb)
        else:
            raise NoChildException





class Patient(object):
    """
    Representation of a simplified patient. The patient does not take any drugs
    and his/her virus populations have no drug resistance.
    """

    def __init__(self, viruses, maxPop):
        """
        Initialization function, saves the viruses and maxPop parameters as
        attributes.

        viruses: the list representing the virus population (a list of
        SimpleVirus instances)

        maxPop: the maximum virus population for this patient (an integer)
        """
        self.viruses = viruses
        self.maxPop = maxPop

    def getViruses(self):
        """
        Returns the viruses in this Patient.
        """
        return self.viruses

    def getMaxPop(self):
        """
        Returns the max population.
        """
        return self.maxPop

    def getTotalPop(self):
        """
        Gets the size of the current total virus population.
        returns: The total virus population (an integer)
        """
        return len(self.viruses)

    def update(self):
        """
        Update the state of the virus population in this patient for a single
        time step. update() should execute the following steps in this order:

        - Determine whether each virus particle survives and updates the list
        of virus particles accordingly.

        - The current population density is calculated. This population density
          value is used until the next call to update()

        - Based on this value of population density, determine whether each
          virus particle should reproduce and add offspring virus particles to
          the list of viruses in this patient.

        returns: The total virus population at the end of the update (an
        integer)
        """
        viruses_copy = self.viruses[:]
        for v in viruses_copy:
            if v.doesClear():
                self.viruses.remove(v)
                # print "virus cleared", v

        try:
            totalPop = self.getTotalPop()
            self.popDensity = totalPop / float(self.maxPop)
        except ZeroDivisionError:
            self.popDensity = 0.0
            # print "Zero division error raised when calculating the pop density"
        # print "total population: ", totalPop
        # print "Population density = ", self.popDensity

        viruses_copy = self.viruses[:]
        newViruses = []
        if self.popDensity < 1:
            for v in range(len(viruses_copy)):
                try:
                    newViruses.append(self.viruses[v].reproduce(self.popDensity))
                    # print "new virus added"
                except NoChildException:
                    # print "NoChildException raised - new virus NOT added"
                    continue
            self.viruses = self.viruses + newViruses
        return self.getTotalPop()

# from ps3b_precompiled_27 import *

#
# PROBLEM 3
#
def simulationWithoutDrug(numViruses, maxPop, maxBirthProb, clearProb,
                          numTrials):
    """
    Run the simulation and plot the graph for problem 3 (no drugs are used,
    viruses do not have any drug resistance).
    For each of numTrials trial, instantiates a patient, runs a simulation
    for 300 timesteps, and plots the average virus population size as a
    function of time.

    numViruses: number of SimpleVirus to create for patient (an integer)
    maxPop: maximum virus population for patient (an integer)
    maxBirthProb: Maximum reproduction probability (a float between 0-1)
    clearProb: Maximum clearance probability (a float between 0-1)
    numTrials: number of simulation runs to execute (an integer)
    """
    trialTimeSteps = 300
    trialResults = [[] for step in range(trialTimeSteps)]   # Create new nested empty list to store results
    avgTimeList = []
    for trial in range(numTrials):
        # Create a list of required viruses
        viruses = [SimpleVirus(maxBirthProb, clearProb) for v in range(numViruses)]
        # Create a new instance of Patient
        simPatient = Patient(viruses, maxPop)
        for timeStep in range(trialTimeSteps):      # update trial results for each time step
            trialResults[timeStep].append(simPatient.update())
    for t in range(trialTimeSteps):     # Append the average trail time step value to the average time list
        avgTimeList.append(float(sum(trialResults[t])) / float(numTrials))
    # print avgTimeList
    # Create plot for results
    pylab.plot(avgTimeList, label = 'Virus Population')
    pylab.title('SimpleVirus simulation')
    pylab.xlabel('Time Steps')
    pylab.ylabel('Average Virus Population')
    pylab.legend()
    pylab.show()


#
# PROBLEM 4

class ResistantVirus(SimpleVirus):
    """
    Representation of a virus which can have drug resistance.
    """

    def __init__(self, maxBirthProb, clearProb, resistances, mutProb):
        """
        Initialize a ResistantVirus instance, saves all parameters as attributes
        of the instance.

        maxBirthProb: Maximum reproduction probability (a float between 0-1)

        clearProb: Maximum clearance probability (a float between 0-1).

        resistances: A dictionary of drug names (strings) mapping to the state
        of this virus particle's resistance (either True or False) to each drug.
        e.g. {'guttagonol':False, 'srinol':False}, means that this virus
        particle is resistant to neither guttagonol nor srinol.

        mutProb: Mutation probability for this virus particle (a float). This is
        the probability of the offspring acquiring or losing resistance to a drug.
        """
        SimpleVirus.__init__(self, maxBirthProb, clearProb)
        self.maxBirthProb = maxBirthProb
        self.clearProb = clearProb
        self.resistances = resistances
        self.mutProb = mutProb
        # TODO


    def getResistances(self):
        """
        Returns the resistances for this virus.
        """
        # TODO
        return self.resistances

    def getMutProb(self):
        """
        Returns the mutation probability for this virus.
        """
        # TODO
        return self.mutProb

    def isResistantTo(self, drug):
        """
        Get the state of this virus particle's resistance to a drug. This method
        is called by getResistPop() in TreatedPatient to determine how many virus
        particles have resistance to a drug.

        drug: The drug (a string)

        returns: True if this virus instance is resistant to the drug, False
        otherwise.
        """
        if drug in self.resistances and self.resistances[drug] == True:
            return True
        else:
            return False
        # TODO


    def reproduce(self, popDensity, activeDrugs):
        """
        Stochastically determines whether this virus particle reproduces at a
        time step. Called by the update() method in the TreatedPatient class.

        A virus particle will only reproduce if it is resistant to ALL the drugs
        in the activeDrugs list. For example, if there are 2 drugs in the
        activeDrugs list, and the virus particle is resistant to 1 or no drugs,
        then it will NOT reproduce.

        Hence, if the virus is resistant to all drugs
        in activeDrugs, then the virus reproduces with probability:

        self.maxBirthProb * (1 - popDensity).

        If this virus particle reproduces, then reproduce() creates and returns
        the instance of the offspring ResistantVirus (which has the same
        maxBirthProb and clearProb values as its parent). The offspring virus
        will have the same maxBirthProb, clearProb, and mutProb as the parent.

        For each drug resistance trait of the virus (i.e. each key of
        self.resistances), the offspring has probability 1-mutProb of
        inheriting that resistance trait from the parent, and probability
        mutProb of switching that resistance trait in the offspring.

        For example, if a virus particle is resistant to guttagonol but not
        srinol, and self.mutProb is 0.1, then there is a 10% chance that
        that the offspring will lose resistance to guttagonol and a 90%
        chance that the offspring will be resistant to guttagonol.
        There is also a 10% chance that the offspring will gain resistance to
        srinol and a 90% chance that the offspring will not be resistant to
        srinol.

        popDensity: the population density (a float), defined as the current
        virus population divided by the maximum population

        activeDrugs: a list of the drug names acting on this virus particle
        (a list of strings).

        returns: a new instance of the ResistantVirus class representing the
        offspring of this virus particle. The child should have the same
        maxBirthProb and clearProb values as this virus. Raises a
        NoChildException if this virus particle does not reproduce.
        """
        reproduce = True
        for drug in activeDrugs:   # Check to see if virus can reproduce
            if not self.isResistantTo(drug):
                reproduce = False
        if reproduce == True and random.random() <= (self.maxBirthProb * (1 - popDensity)):
            offspringResist = {}
            for drug in self.resistances.keys():
                if random.random() <= (1 - self.mutProb):  # the offspring has probability 1-mutProb of inheriting that resistance trait from the parent
                    offspringResist[drug] = self.resistances[drug]
                else:
                    offspringResist[drug] = not self.resistances[drug]
            return ResistantVirus(self.maxBirthProb, self.clearProb,offspringResist, self.getMutProb())
        else:
            raise NoChildException



class TreatedPatient(Patient):
    """
    Representation of a patient. The patient is able to take drugs and his/her
    virus population can acquire resistance to the drugs he/she takes.
    """

    def __init__(self, viruses, maxPop):
        """
        Initialization function, saves the viruses and maxPop parameters as
        attributes. Also initializes the list of drugs being administered
        (which should initially include no drugs).

        viruses: The list representing the virus population (a list of
        virus instances)

        maxPop: The  maximum virus population for this patient (an integer)
        """
        Patient.__init__(self, viruses, maxPop)
        self.viruses = viruses
        self.maxPop = maxPop
        self.activeDrugs = []

        # TODO


    def addPrescription(self, newDrug):
        """
        Administer a drug to this patient. After a prescription is added, the
        drug acts on the virus population for all subsequent time steps. If the
        newDrug is already prescribed to this patient, the method has no effect.

        newDrug: The name of the drug to administer to the patient (a string).

        postcondition: The list of drugs being administered to a patient is updated
        """
        if newDrug not in self.activeDrugs:
            self.activeDrugs.append(newDrug)

        # TODO


    def getPrescriptions(self):
        """
        Returns the drugs that are being administered to this patient.

        returns: The list of drug names (strings) being administered to this
        patient.
        """
        return self.activeDrugs
        # TODO


    def getResistPop(self, drugResist):
        """
        Get the population of virus particles resistant to the drugs listed in
        drugResist.

        drugResist: Which drug resistances to include in the population (a list
        of strings - e.g. ['guttagonol'] or ['guttagonol', 'srinol'])

        returns: The population of viruses (an integer) with resistances to all
        drugs in the drugResist list.
        """
        virusPop = 0
        for virus in self.viruses:
            foundResistance = True
            for drug in drugResist:
                isResistant =  virus.isResistantTo(drug)
                foundResistance *= isResistant
            if foundResistance:
                virusPop += 1
        return virusPop

        # TODO


    def update(self):
        """
        Update the state of the virus population in this patient for a single
        time step. update() should execute these actions in order:

        - Determine whether each virus particle survives and update the list of
          virus particles accordingly

        - The current population density is calculated. This population density
          value is used until the next call to update().

        - Based on this value of population density, determine whether each
          virus particle should reproduce and add offspring virus particles to
          the list of viruses in this patient.
          The list of drugs being administered should be accounted for in the
          determination of whether each virus particle reproduces.

        returns: The total virus population at the end of the update (an
        integer)
        """
        viruses_copy = self.viruses[:]
        virusResistances = []
        for v in viruses_copy:
            if v.doesClear():
                self.viruses.remove(v)
                # print "virus cleared", v
            else:
                virusResistances += v.getResistances().keys()
        try:
            resistPop = self.getResistPop(virusResistances)
            popDensity = resistPop / float(self.getMaxPop())
        except ZeroDivisionError:
            popDensity = 0.0
            # print "Zero division error raised when calculating the pop density"
        # print "resist population: ", resistPop
        # print "Population density = ", popDensity

        viruses_copy = self.viruses[:]
        newViruses = []
        if popDensity < 1:
            for v in range(len(viruses_copy)):
                try:
                    newViruses.append(self.viruses[v].reproduce(popDensity, self.activeDrugs))
                    # print "new virus added"
                except NoChildException:
                    # print "NoChildException raised - new virus NOT added"
                    continue
            self.viruses += newViruses
        return self.getTotalPop()




# from ps3b_precompiled_27 import *

#
# PROBLEM 5
#
# def simulationWithDrug(numViruses, maxPop, maxBirthProb, clearProb, resistances,
#                        mutProb, numTrials):
#     """
#     Runs simulations and plots graphs for problem 5.
#
#     For each of numTrials trials, instantiates a patient, runs a simulation for
#     150 timesteps, adds guttagonol, and runs the simulation for an additional
#     150 timesteps.  At the end plots the average virus population size
#     (for both the total virus population and the guttagonol-resistant virus
#     population) as a function of time.
#
#     numViruses: number of ResistantVirus to create for patient (an integer)
#     maxPop: maximum virus population for patient (an integer)
#     maxBirthProb: Maximum reproduction probability (a float between 0-1)
#     clearProb: maximum clearance probability (a float between 0-1)
#     resistances: a dictionary of drugs that each ResistantVirus is resistant to
#                  (e.g., {'guttagonol': False})
#     mutProb: mutation probability for each ResistantVirus particle
#              (a float between 0-1).
#     numTrials: number of simulation runs to execute (an integer)
#
#     """
#     trialTimeSteps = 300
#     trialResultsTot = [[] for step in range(trialTimeSteps)]   # Create new nested empty list to store results
#     # simResultsTot = [[] for step in range(trialTimeSteps)]
#     simResultsTot = []
#     trialResultsRes = [[] for step in range(trialTimeSteps)]    # Create new nested empty list to store the resistant population
#     # simResultsRes = [[] for step in range(trialTimeSteps)]
#     simResultsRes = []
#     drugResistances = {"guttagonol": False}
#     # if resistances != {}:
#     #     for drug in resistances.keys():
#     #          virusResistances[drug] = resistances[drug]
#     # else:
#     #     resistances = drugResistances
#     for trial in range(numTrials):
#         # Create a list of required viruses
#         viruses = [ResistantVirus(maxBirthProb, clearProb, drugResistances.copy(), mutProb) for v in range(numViruses)]
#         # print 'resistances', resistances.copy()
#         # Create a new instance of Patient
#         simPatient = TreatedPatient(viruses, maxPop)
#         for timeStep in range(trialTimeSteps):      # update trial results for each time step
#             if timeStep == 150:
#                 simPatient.addPrescription("guttagonol")
#             simPatient.update()
#             if resistances != {}:
#                 trialResultsRes[timeStep].append(simPatient.getResistPop(resistances.keys()))
#             trialResultsTot[timeStep].append(simPatient.getTotalPop())
#
#
#             # trialResultsRes[timeStep].append(simPatient.getResistPop(simPatient.getPrescriptions()))
#             #trialResultsRes[timeStep].append(simPatient.getResistPop(['guttagonol']))
#             # print 'get prescriptions trial#',trial , 'Timestep #',timeStep , simPatient.getPrescriptions()
#             # print 'total ', trialResultsTot[timeStep]
#             # print 'resistant ', trialResultsRes[timeStep], '\n'
#     # print trialResultsTot
#     # print trialResultsRes
#     for t in range(trialTimeSteps):     # Append the average trail time step value to the average time list
#         # try:
#         #     simResultsTot.append(float(sum(trialResultsTot[t])) / float(numTrials))
#         # except:
#         #     return simResultsTot[t].append(0)
#         simResultsTot.append(float(sum(trialResultsTot[t])) / float(numTrials))
#         try:
#             simResultsRes.append(float(sum(trialResultsRes[t])) / float(numTrials))
#         except ZeroDivisionError:
#             return simResultsRes[t].append([0])
#
#
#
#     # simResultsTot = [sum(i) / float(len(i)) for i in trialResultsTot]
#     # simResultsRes = [sum(i) / float(len(i)) for i in trialResultsRes]
#     # Create plot for results
#     print simResultsTot , '\n'
#     print simResultsRes, '\n'
#     pylab.plot(simResultsTot, label = 'Total Virus Population')
#     pylab.plot(simResultsRes, label = 'guttagonol-resistant virus particles')
#     pylab.title('ResistantVirus simulation')
#     pylab.xlabel('time step')
#     pylab.ylabel('# viruses')
#     pylab.legend()
#     pylab.show()


# def simulationWithDrug(numViruses, maxPop, maxBirthProb, clearProb, resistances,
#                        mutProb, numTrials):
#     """
#     Runs simulations and plots graphs for problem 5.
#
#     For each of numTrials trials, instantiates a patient, runs a simulation for
#     150 timesteps, adds guttagonol, and runs the simulation for an additional
#     150 timesteps.  At the end plots the average virus population size
#     (for both the total virus population and the guttagonol-resistant virus
#     population) as a function of time.
#
#     numViruses: number of ResistantVirus to create for patient (an integer)
#     maxPop: maximum virus population for patient (an integer)
#     maxBirthProb: Maximum reproduction probability (a float between 0-1)
#     clearProb: maximum clearance probability (a float between 0-1)
#     resistances: a dictionary of drugs that each ResistantVirus is resistant to
#                  (e.g., {'guttagonol': False})
#     mutProb: mutation probability for each ResistantVirus particle
#              (a float between 0-1).
#     numTrials: number of simulation runs to execute (an integer)
#
#     """
#     trialTimeSteps = 300
#     trialResultsTot = [0.0 for step in range(trialTimeSteps)]   # Create new nested empty list to store results
#     simResultsTot = []
#     trialResultsRes = [0.0 for step in range(trialTimeSteps)]    # Create new nested empty list to store the resistant population
#     simResultsRes = []
#     drugResistances = {"guttagonol": False}
#     # random.seed(0)
#     for trial in range(numTrials):
#         # Create a list of required viruses
#         viruses = [ResistantVirus(maxBirthProb, clearProb, drugResistances.copy(), mutProb) for v in range(numViruses)]
#         # Create a new instance of Patient
#         simPatient = TreatedPatient(viruses, maxPop)
#         for timeStep in range(trialTimeSteps):      # update trial results for each time step
#             # trialResultsTot[timeStep].append(simPatient.update())
#             if timeStep == 150:
#                 simPatient.addPrescription('guttagonol')
#             # simPatient.update()
#             # trialResultsTot[timeStep].append(simPatient.getTotalPop())
#             # trialResultsTot[timeStep] += simPatient.getTotalPop()
#             trialResultsTot[timeStep] += simPatient.update()
#             if resistances != {}:
#                 # trialResultsRes[timeStep].append(simPatient.getResistPop(['guttagonol']))
#                 trialResultsRes[timeStep] += simPatient.getResistPop(['guttagonol'])
#                 # trialResultsRes[timeStep].append(simPatient.getResistPop(simPatient.getPrescriptions()))
#     # for t in range(trialTimeSteps):     # Append the average trail time step value to the average time list
#     for t in range(len(trialResultsTot)):
#         # simResultsTot.append(sum(trialResultsTot[t]) / float(numTrials))
#         trialResultsTot[t] /= float(numTrials)
#         try:
#             # simResultsRes.append(float(sum(trialResultsRes[t])) / float(numTrials))
#             trialResultsRes[t] /= float(numTrials)
#         except ZeroDivisionError:
#             # return simResultsRes[t].append([0])
#             trialResultsRes[t] += 0.0
#             return trialResultsRes[t]
#     # print simResultsTot, '\n'
#     # print simResultsRes, '\n'
#     # print trialResultsTot, '\n'
#     # print trialResultsRes, '\n'
#     # pylab.plot(simResultsTot, label = 'Total Virus Population')
#     # pylab.plot(simResultsRes, label = 'guttagonol-resistant virus particles')
#     pylab.plot(trialResultsTot, label = 'Total Virus Population')
#     pylab.plot(trialResultsRes, label = 'guttagonol-resistant virus particles')
#     pylab.title('ResistantVirus simulation')
#     pylab.xlabel('time step')
#     pylab.ylabel('# viruses')
#     pylab.legend()
#     pylab.show()
#
#     # ===========================================================================================================
#
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
#
#
#     # ===========================================================================================================
#     # pylab.title('SimpleVirus simulation')
#     # pylab.xlabel('Time Steps')
#     # pylab.ylabel('Average Virus Population')
#     # pylab.legend()
#     # pylab.show()
# linestyle = 'dashed'

# numViruses = 100
# maxPop = 1000
# maxBirthProb = 0.1
# clearProb = 0.05
# numTrials = 100
# resistances = {'guttagonol': False}
# mutProb = 0.005
# simulationWithDrug(numViruses, maxPop, maxBirthProb, clearProb, resistances, mutProb, numTrials)

random.seed(0)
# simulationWithDrug(100, 1000, 0.1, 0.05, {'guttagonol': False}, 0.005, 100)
print '\n simulationWithDrug(1, 10, 1.0, 0.0, {}, 1.0, 5) \n'
simulationWithDrug(1, 10, 1.0, 0.0, {}, 1.0, 5)
print '\n simulationWithDrug(1, 20, 1.0, 0.0, {"guttagonol": True}, 1.0, 5) \n'
simulationWithDrug(1, 20, 1.0, 0.0, {"guttagonol": True}, 1.0, 5)
print '\n simulationWithDrug(75, 100, .8, 0.1, {"guttagonol": True}, 0.8, 1) \n'
simulationWithDrug(75, 100, .8, 0.1, {"guttagonol": True}, 0.8, 1)


# Testcase 3
plotTotal = [79.0, 91.0, 92.0, 97.0, 99.0, 102.0, 99.0, 92.0, 97.0, 98.0, 97.0, 94.0, 97.0, 99.0, 101.0, 98.0, 97.0, 93.0, 89.0, 88.0, 87.0, 90.0, 98.0, 93.0, 93.0, 89.0, 96.0, 97.0, 93.0, 91.0, 99.0, 99.0, 93.0, 99.0, 100.0, 98.0, 95.0, 95.0, 101.0, 98.0, 91.0, 97.0, 93.0, 88.0, 92.0, 100.0, 100.0, 96.0, 93.0, 97.0, 94.0, 98.0, 101.0, 95.0, 97.0, 95.0, 93.0, 95.0, 100.0, 102.0, 97.0, 99.0, 98.0, 95.0, 95.0, 96.0, 94.0, 90.0, 95.0, 95.0, 100.0, 96.0, 96.0, 93.0, 92.0, 91.0, 97.0, 96.0, 97.0, 100.0, 98.0, 95.0, 102.0, 99.0, 93.0, 94.0, 100.0, 97.0, 98.0, 93.0, 98.0, 98.0, 92.0, 98.0, 95.0, 95.0, 99.0, 97.0, 99.0, 96.0, 100.0, 101.0, 100.0, 97.0, 96.0, 93.0, 89.0, 94.0, 93.0, 96.0, 97.0, 94.0, 94.0, 98.0, 100.0, 99.0, 97.0, 99.0, 98.0, 98.0, 92.0, 92.0, 96.0, 96.0, 99.0, 104.0, 98.0, 99.0, 96.0, 94.0, 100.0, 93.0, 92.0, 92.0, 90.0, 101.0, 100.0, 95.0, 90.0, 93.0, 96.0, 96.0, 96.0, 95.0, 93.0, 95.0, 95.0, 91.0, 91.0, 94.0, 90.0, 81.0, 76.0, 77.0, 82.0, 81.0, 75.0, 75.0, 72.0, 75.0, 75.0, 77.0, 81.0, 84.0, 75.0, 76.0, 77.0, 71.0, 79.0, 78.0, 76.0, 73.0, 73.0, 69.0, 62.0, 62.0, 60.0, 55.0, 45.0, 45.0, 51.0, 54.0, 56.0, 55.0, 55.0, 54.0, 51.0, 55.0, 45.0, 43.0, 38.0, 36.0, 35.0, 34.0, 36.0, 40.0, 40.0, 37.0, 41.0, 40.0, 44.0, 43.0, 46.0, 48.0, 51.0, 54.0, 54.0, 52.0, 48.0, 48.0, 47.0, 50.0, 48.0, 52.0, 53.0, 56.0, 53.0, 52.0, 48.0, 48.0, 48.0, 44.0, 41.0, 42.0, 44.0, 46.0, 47.0, 48.0, 48.0, 44.0, 43.0, 41.0, 39.0, 38.0, 37.0, 29.0, 27.0, 28.0, 22.0, 23.0, 22.0, 20.0, 20.0, 20.0, 20.0, 19.0, 19.0, 24.0, 26.0, 29.0, 30.0, 33.0, 31.0, 25.0, 25.0, 25.0, 22.0, 20.0, 20.0, 21.0, 20.0, 23.0, 22.0, 21.0, 21.0, 24.0, 22.0, 23.0, 24.0, 27.0, 23.0, 21.0, 21.0, 20.0, 19.0, 17.0, 16.0, 15.0, 15.0, 12.0, 10.0, 9.0, 8.0, 8.0, 8.0, 8.0, 7.0, 7.0, 6.0, 5.0, 4.0, 3.0, 3.0, 3.0, 2.0, 2.0, 2.0, 2.0, 2.0, 2.0]
plotRes = [65.0, 67.0, 62.0, 63.0, 61.0, 62.0, 58.0, 53.0, 51.0, 50.0, 52.0, 49.0, 49.0, 51.0, 51.0, 47.0, 47.0, 41.0, 42.0, 40.0, 37.0, 42.0, 48.0, 46.0, 46.0, 44.0, 47.0, 47.0, 41.0, 40.0, 45.0, 45.0, 42.0, 48.0, 49.0, 48.0, 49.0, 46.0, 50.0, 49.0, 47.0, 54.0, 53.0, 49.0, 50.0, 52.0, 51.0, 50.0, 49.0, 48.0, 46.0, 49.0, 49.0, 44.0, 43.0, 43.0, 42.0, 42.0, 43.0, 46.0, 46.0, 47.0, 50.0, 51.0, 47.0, 45.0, 48.0, 46.0, 49.0, 49.0, 50.0, 48.0, 50.0, 48.0, 49.0, 48.0, 50.0, 48.0, 50.0, 51.0, 51.0, 49.0, 52.0, 49.0, 48.0, 49.0, 45.0, 45.0, 47.0, 48.0, 47.0, 46.0, 43.0, 51.0, 51.0, 50.0, 53.0, 51.0, 51.0, 52.0, 53.0, 52.0, 51.0, 49.0, 48.0, 45.0, 39.0, 43.0, 44.0, 46.0, 48.0, 45.0, 45.0, 49.0, 52.0, 51.0, 49.0, 49.0, 48.0, 49.0, 43.0, 45.0, 50.0, 48.0, 50.0, 51.0, 48.0, 46.0, 42.0, 42.0, 42.0, 43.0, 43.0, 44.0, 38.0, 43.0, 39.0, 37.0, 38.0, 41.0, 42.0, 42.0, 42.0, 43.0, 41.0, 45.0, 47.0, 44.0, 45.0, 48.0, 44.0, 37.0, 32.0, 33.0, 33.0, 32.0, 29.0, 29.0, 27.0, 29.0, 27.0, 29.0, 29.0, 32.0, 26.0, 24.0, 24.0, 22.0, 24.0, 21.0, 19.0, 17.0, 15.0, 15.0, 14.0, 16.0, 17.0, 13.0, 10.0, 12.0, 13.0, 15.0, 14.0, 13.0, 12.0, 11.0, 9.0, 9.0, 8.0, 8.0, 7.0, 5.0, 6.0, 7.0, 7.0, 9.0, 11.0, 11.0, 11.0, 11.0, 11.0, 10.0, 11.0, 14.0, 14.0, 13.0, 14.0, 12.0, 9.0, 11.0, 11.0, 14.0, 14.0, 15.0, 13.0, 14.0, 12.0, 11.0, 11.0, 12.0, 12.0, 10.0, 10.0, 11.0, 12.0, 11.0, 10.0, 11.0, 8.0, 7.0, 6.0, 5.0, 6.0, 6.0, 6.0, 3.0, 3.0, 3.0, 2.0, 2.0, 2.0, 2.0, 2.0, 2.0, 3.0, 5.0, 5.0, 5.0, 6.0, 7.0, 7.0, 7.0, 4.0, 4.0, 5.0, 4.0, 5.0, 4.0, 3.0, 4.0, 4.0, 5.0, 5.0, 4.0, 3.0, 3.0, 3.0, 4.0, 4.0, 5.0, 3.0, 3.0, 2.0, 2.0, 1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
pylab.figure(2)
pylab.plot(plotTotal, label = 'Total Virus Population')
pylab.plot(plotRes, label = 'guttagonol-resistant virus particles')
pylab.title('ResistantVirus simulation test case 3')
pylab.xlabel('time step')
pylab.ylabel('# viruses')
pylab.legend()
pylab.show()

simulationWithDrug(75, 100, .8, 0.1, {"guttagonol": True}, 0.8, 1000)

# print " \n" 'test sime test case simulationWithDrug(75, 100, .8, 0.1, {"guttagonol": True}, 0.8, 1) \n'
# simulationWithDrug(100, 1000, .1, 0.05, {"guttagonol": True}, 0.005, 100)
# "==================================TEST AREA======================================="

# Test SimpleVirus & patient

# random.seed(0)
# virus1 = SimpleVirus(0.5, 0.3)
# virus2 = SimpleVirus(0.9, 0.6)
# virus3 = SimpleVirus(0.8, 0.7)
# virus4 = SimpleVirus(0.1, 0.1)
# virus5 = SimpleVirus(0.9, 0.6)
# virus6 = SimpleVirus(random.random(), random.random())
# virus7 = SimpleVirus(random.random(), random.random())
#
# viruses = [virus1, virus2, virus3, virus4, virus5, virus6, virus7]
# patient = Patient(viruses, 10)
#
# print "get viruses: ", patient.getViruses()
# print "get total pop: ", patient.getTotalPop()
# print "get max pop: ", patient.getMaxPop()
# print "patient update: ", "\n", patient.update()
# print patient.getViruses()
# "==================================Problem 3======================================
#
# numViruses = 100
# maxPop = 1000
# maxBirthProb = 0.1
# clearProb = 0.05
# numTrials = 100
# "==================================Problem 4======================================

# random.seed(0)
# maxBirthProb = 0.1
# clearProb = 0.2
# resistances = {'drugA': False, 'drugB':True}
# mutProb = 0.5
#
# resistantVirus = ResistantVirus(maxBirthProb, clearProb, resistances, mutProb)
# print resistantVirus
# print "getResistances", resistantVirus.getResistances()
# print 'getMutProb', resistantVirus.getMutProb()
# print 'isResistantTo - drugA', resistantVirus.isResistantTo('drugA')
# print 'maxBirthProb', resistantVirus.getMaxBirthProb()
# print 'getClearProb', resistantVirus.getClearProb()
# print 'reproduce', resistantVirus.reproduce(0.2, ['drugB'])
# # resistances = {'drugA': True, 'drugB':True, 'drugC':True}
# # resistantVirus = ResistantVirus(maxBirthProb, clearProb, resistances, mutProb)
# # print 'reproduce', resistantVirus.reproduce(0.2, ['drugB', 'drugC'])

# ==============================Problem 5==========================================

# Test SimpleVirus & patient

# random.seed(0)

# resistances = {'drugA': True, 'drugB':True, 'drugC':True}
# viruses = [ResistantVirus(random.random(), random.random(), resistances, random.random()) for v in range(10)]
# print viruses
# patient = TreatedPatient(viruses, 10)
#
# print "get viruses: ", patient.getViruses()
# print "get total pop: ", patient.getTotalPop()
# print "get max pop: ", patient.getMaxPop()
# print "patient update: ", "\n", patient.update()
# print patient.getViruses()

