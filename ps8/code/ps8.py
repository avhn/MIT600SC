# 6.00 Problem Set 8
# Name: Mert Dede

import numpy
import random
import pylab
from ps7 import *

#
# PROBLEM 1
#

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
        e.g. {'guttagonol':False, 'grimpex',False}, means that this virus
        particle is resistant to neither guttagonol nor grimpex.

        mutProb: Mutation probability for this virus particle (a float). This is
        the probability of the offspring acquiring or losing resistance to a drug.        

        """

        self.maxBirthProb = maxBirthProb
        self.clearProb = clearProb
        self.mutProb = mutProb
        self.resistances = resistances

    def isResistantTo(self, drug):

        """
        Get the state of this virus particle's resistance to a drug. This method
        is called by getResistPop() in Patient to determine how many virus
        particles have resistance to a drug.    

        drug: The drug (a string)
        returns: True if this virus instance is resistant to the drug, False
        otherwise.
        """
        return self.resistances.get(drug, False)

    def reproduce(self, popDensity, activeDrugs):

        """
        Stochastically determines whether this virus particle reproduces at a
        time step. Called by the update() method in the Patient class.

        If the virus particle is not resistant to any drug in activeDrugs,
        then it does not reproduce. Otherwise, the virus particle reproduces
        with probability:       
        
        self.maxBirthProb * (1 - popDensity).                       
        
        If this virus particle reproduces, then reproduce() creates and returns
        the instance of the offspring ResistantVirus (which has the same
        maxBirthProb and clearProb values as its parent). 

        For each drug resistance trait of the virus (i.e. each key of
        self.resistances), the offspring has probability 1-mutProb of
        inheriting that resistance trait from the parent, and probability
        mutProb of switching that resistance trait in the offspring.        

        For example, if a virus particle is resistant to guttagonol but not
        grimpex, and `self.mutProb` is 0.1, then there is a 10% chance that
        that the offspring will lose resistance to guttagonol and a 90% 
        chance that the offspring will be resistant to guttagonol.
        There is also a 10% chance that the offspring will gain resistance to
        grimpex and a 90% chance that the offspring will not be resistant to
        grimpex.

        popDensity: the population density (a float), defined as the current
        virus population divided by the maximum population        

        activeDrugs: a list of the drug names acting on this virus particle
        (a list of strings). 
        
        returns: a new instance of the ResistantVirus class representing the
        offspring of this virus particle. The child should have the same
        maxBirthProb and clearProb values as this virus. Raises a
        NoChildException if this virus particle does not reproduce.         
        """
        for drug in activeDrugs:
            if not self.isResistantTo(drug):
                raise NoChildException()

        if random.random() <= self.maxBirthProb * (1 - popDensity):

            # arrange drug resistance probs for offspring
            child_resistances = dict()
            for drug in self.resistances.keys():
                is_resistant = None

                if self.isResistantTo(drug):
                    if random.random() <= self.mutProb:
                        is_resistant = False
                    else:
                        is_resistant = True

                    child_resistances[ drug ] = is_resistant

                else:
                    if random.random() <= self.mutProb:
                        is_resistant = True
                    else:
                        is_resistant = False

                child_resistances[ drug ] = is_resistant

            return ResistantVirus(self.maxBirthProb, self.clearProb, child_resistances, self.mutProb)

        else:
            raise NoChildException()


class Patient(SimplePatient):

    """
    Representation of a patient. The patient is able to take drugs and his/her
    virus population can acquire resistance to the drugs he/she takes.
    """

    def __init__(self, viruses, maxPop):
        """
        Initialization function, saves the viruses and maxPop parameters as
        attributes. Also initializes the list of drugs being administered
        (which should initially include no drugs).               

        viruses: the list representing the virus population (a list of
        SimpleVirus instances)
        
        maxPop: the  maximum virus population for this patient (an integer)
        """

        self.viruses = viruses
        self.maxPop = maxPop
        self.popDensity = len(viruses)/float(maxPop)

        self.Prescriptions = list()

    def addPrescription(self, newDrug):

        """
        Administer a drug to this patient. After a prescription is added, the 
        drug acts on the virus population for all subsequent time steps. If the
        newDrug is already prescribed to this patient, the method has no effect.

        newDrug: The name of the drug to administer to the patient (a string).

        postcondition: list of drugs being administered to a patient is updated
        """
        # should not allow one drug being added to the list multiple times
        newDrug = newDrug.lower()

        if not newDrug in self.getPrescriptions():
            self.Prescriptions.append(newDrug)

    def getPrescriptions(self):

        """
        Returns the drugs that are being administered to this patient.
        returns: The list of drug names (strings) being administered to this
        patient.
        """

        return self.Prescriptions

    def getResistPop(self, drugResist):
        """
        Get the population of virus particles resistant to the drugs listed in 
        drugResist.        

        drugResist: Which drug resistances to include in the population (a list
        of strings - e.g. ['guttagonol'] or ['guttagonol', 'grimpex'])

        returns: the population of viruses (an integer) with resistances to all
        drugs in the drugResist list.
        """
        ResistPop = 0
        drugs = len(drugResist)

        for virus in self.viruses:
            resistant = True
            for drug in drugResist:
                if not virus.isResistantTo(drug):
                    resistant = False
                    break

            ResistPop += resistant

        return ResistPop

    def getTotalPop(self):
        return len(self.viruses)

    def update(self):

        """
        Update the state of the virus population in this patient for a single
        time step. update() should execute these actions in order:
        
        - Determine whether each virus particle survives and update the list of 
          virus particles accordingly          
        - The current population density is calculated. This population density
          value is used until the next call to update().
        - Determine whether each virus particle should reproduce and add
          offspring virus particles to the list of viruses in this patient. 
          The listof drugs being administered should be accounted for in the
          determination of whether each virus particle reproduces. 

        returns: the total virus population at the end of the update (an
        integer)
        """
        newPop = list()
        for virus in self.viruses:
            if not virus.doesClear():
                newPop.append(virus)
        self.viruses = newPop

        self.popDensity = len(self.viruses)/float(self.maxPop)

        offSprings = list()
        for virus in self.viruses:
            try:
                mutation = virus.reproduce(self.popDensity, self.getPrescriptions())
                offSprings.append(mutation)
            except NoChildException:
                continue
        self.viruses += offSprings

        return len(self.viruses)

#
# PROBLEM 2
#

def simulationWithDrug(timesteps = 150, num_trials = 30):

    """

    Runs simulations and plots graphs for problem 4.
    Instantiates a patient, runs a simulation for 150 timesteps, adds
    guttagonol, and runs the simulation for an additional 150 timesteps.
    total virus population vs. time and guttagonol-resistant virus population
    vs. time are plotted
    """
    # Instances
    maxBirthProb, clearProb, resistances, mutProb = 0.1, 0.05, {'guttagonol':False}, 0.005
    num_viruses, maxPop = 100, 1000

    # initial data + timesteps, for average data, mean
    pop, resist_pop = numpy.array( [0 for i in range(1 + 2*timesteps)]), numpy.array( [0 for i in range(1 + timesteps)] )

    # try number of trials and sum data
    for trial in xrange(num_trials):
        viruses = list()
        for i in xrange(num_viruses):
            viruses.append( ResistantVirus( maxBirthProb, clearProb, resistances, mutProb) )

        patient = Patient( viruses, maxPop )

        total_pop = [num_viruses]
        for normal in xrange(timesteps):
            total_pop.append( patient.update() )

        patient.addPrescription('guttagonol')
        resistant_pop = [ patient.getResistPop( ['guttagonol'] ) ]
        for resistancy in xrange(timesteps):
            total_pop.append( patient.update() )
            resistant_pop.append( patient.getResistPop( ['guttagonol'] ))

        pop += numpy.array(total_pop)
        resist_pop += numpy.array(resistant_pop)
    # Compute mean, for numtrials
    pop /= num_trials
    resist_pop /= num_trials

    pylab.figure(1)
    pylab.plot(pop, label = 'Virus population')
    pylab.title( ' Virus population simulation ' )
    pylab.xlabel( ' Time steps ' )
    pylab.ylabel( ' Number of Viruses ' )
    pylab.legend( loc = 'best' )

    pylab.figure(2)
    pylab.plot(range(timesteps, 1 + 2*timesteps), resist_pop, label = 'Resistancy to guttagonol')
    pylab.title( ' Resistant virus population increasement ' )
    pylab.xlabel( ' Time steps ' )
    pylab.ylabel( ' Number of Viruses ' )
    pylab.legend( loc = 'best' )

    pylab.show()

#
# PROBLEM 3
#        

def simulationDelayedTreatment(delays = (0, 75, 150, 300), num_trials = 30):

    """
    Runs simulations and make histograms for problem 5.
    Runs multiple simulations to show the relationship between delayed treatment
    and patient outcome.
    Histograms of final total virus populations are displayed for delays of 300,
    150, 75, 0 timesteps (followed by an additional 150 timesteps of
    simulation).    
    """
    maxBirthProb, clearProb, resistances, mutProb = 0.1, 0.05, {'guttagonol':False}, 0.005
    num_viruses, maxPop = 100, 1000

    data = dict()
    for drugtime in delays:

        pop_data = list()
        for i in xrange(num_trials):

            viruses = list()
            for virus in xrange(num_viruses):
                viruses.append( ResistantVirus(maxBirthProb, clearProb, resistances, mutProb) )

            patient = Patient(viruses, maxPop)

            for time in xrange(drugtime+150):
                if time is drugtime:
                    patient.addPrescription('guttagonol')
                patient.update()

            pop_data.append( patient.getTotalPop() )

        data[drugtime] = pop_data

    # --- Plot ---
    pylab.figure( ' Delay ' )
    pylab.title( ' Delaying treatment simulation ' )

    plotNum = 0
    for time in delays:
        plotNum += 1
        pylab.subplot(2, 2, plotNum)
        pylab.hist(data[time], range = (0,600), bins = 12,  label = 'delay: '+str(time))
        pylab.xlabel( ' Final virus count ' )
        pylab.ylabel( ' Number of trials ' )
        pylab.legend( loc = 'best' )

    #    pylab.title(' Delayed treatment simulation ')
    pylab.show()

#
# PROBLEM 4
#

def simulationTwoDrugsDelayedTreatment(lags = (0, 75, 150), num_trials = 1):

    """
    Runs simulations and make histograms for problem 6.
    Runs multiple simulations to show the relationship between administration
    of multiple drugs and patient outcome.
   
    Histograms of final total virus populations are displayed for lag times of
    150, 75, 0 timesteps between adding drugs (followed by an additional 150
    timesteps of simulation).
    """

    maxBirthProb, clearProb, resistances, mutProb = 0.1, 0.05, {'guttagonol':False, 'grimpex':False}, 0.005
    num_viruses, maxPop = 100, 1000


    data = dict()
    for lag in lags:
        pop_data = list()
        for trial in xrange(num_trials):
            viruses = list()
            for i in xrange(num_viruses):
                viruses.append( ResistantVirus(maxBirthProb, clearProb, resistances, mutProb) )

            patient = Patient(viruses, maxPop)

            for time in xrange(1, 1 + 150 + lag + 150):
                if time is 150:
                    patient.addPrescription('guttagonol')
                elif time is 150+lag:
                    patient.addPrescription('grimpex')

                patient.update()

            pop_data.append( patient.getTotalPop() )

        data[lag] = pop_data

    pylab.figure(' Two Drugs Delayed Treatment ')

    plotNum = 0
    for lag in lags:
        plotNum += 1
        pylab.subplot(1,3, plotNum)
        pylab.hist(data[lag], range=(0,600), bins = 12, label = 'lag: '+str(lag))
        pylab.xlabel(' Final virus counts ')
        pylab.ylabel(' Number of trials ')
        pylab.legend( loc = 'best' )

    pylab.show()

#
# PROBLEM 5
#    

def simulationTwoDrugsVirusPopulations(num_trials = 1, lags = (0, 300)):

    """

    Run simulations and plot graphs examining the relationship between
    administration of multiple drugs and patient outcome.
    Plots of total and drug-resistant viruses vs. time are made for a
    simulation with a 300 time step delay between administering the 2 drugs and
    a simulations for which drugs are administered simultaneously.        

    """

    maxBirthProb, clearProb, resistances, mutProb = 0.1, 0.05, {'guttagonol':False, 'grimpex':False}, 0.005
    num_viruses, maxPop = 100, 1000

    data = dict()
    for lag in lags:
        lagdata = list()
        for trial in xrange(num_trials):

            viruses = list()
            for virus in xrange(num_viruses):
                viruses.append( ResistantVirus(maxBirthProb, clearProb, resistances, mutProb) )

            patient = Patient(viruses, maxPop)

            for time in xrange(150 + lag + 150):
                if time is 150:
                    patient.addPrescription('guttagonol')
                if time is 150+lag:
                    patient.addPrescription('grimpex')

                patient.update()

            lagdata.append( patient.getTotalPop() )

        data[lag] = lagdata

    pylab.figure('Two Drugs Lag Simulation')

    plotNum = 0
    for lag in lags:
        plotNum += 1
        pylab.subplot(1, len(lags), plotNum)
        pylab.hist(data[lag], range=(0,600), bins = 12, label = 'lag: '+str(lag))
        pylab.xlabel(' Final virus counts ')
        pylab.ylabel(' Number of trials ')
        pylab.legend( loc = 'best')

    pylab.show()
