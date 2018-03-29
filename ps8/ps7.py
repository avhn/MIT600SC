# Problem Set 7: Simulating the Spread of Disease and Virus Population Dynamics 
# Name: Mert Dede

import random
import pylab

''' 
Begin helper code
'''

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
# PROBLEM 1
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

    def doesClear(self):

        """ Stochastically determines whether this virus particle is cleared from the
        patient's body at a time step. 
        returns: True with probability self.clearProb and otherwise returns
        False.
        """

        return random.random() <= self.clearProb


    def reproduce(self, popDensity):

        """
        Stochastically determines whether this virus particle reproduces at a
        time step. Called by the update() method in the SimplePatient and
        Patient classes. The virus particle reproduces with probability
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
            raise NoChildException()


class SimplePatient(object):

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

        maxPop: the  maximum virus population for this patient (an integer)
        """

        self.viruses = viruses
        self.currPop = len(self.viruses)

        self.maxPop = maxPop
        self.popDensity = self.currPop/float(maxPop)

    def getTotalPop(self):

        """
        Gets the current total virus population. 
        returns: The total virus population (an integer)
        """
        return self.currPop

    def update(self):

        """
        Update the state of the virus population in this patient for a single
        time step. update() should execute the following steps in this order:
        
        - Determine whether each virus particle survives and updates the list
        of virus particles accordingly.   
        - The current population density is calculated. This population density
          value is used until the next call to update() 
        - Determine whether each virus particle should reproduce and add
          offspring virus particles to the list of viruses in this patient.                    

        returns: The total virus population at the end of the update (an
        integer)
        """

        # Determine surviving viruses
        new_list = list()
        for virus in self.viruses:
            if not virus.doesClear():
                new_list.append(virus)

        # Update instances
        self.viruses = new_list
        self.popDensity = len(self.viruses)/float(self.maxPop)

        # Compute and add mutated viruses
        new_list = list()
        for virus in self.viruses:
            try:
                mutation = virus.reproduce(self.popDensity)
                new_list.append(mutation)
            except NoChildException:
                continue

        self.viruses += new_list
        self.currPop = len(self.viruses)

        return self.getTotalPop()

#
# PROBLEM 2
#

def runSim(time_steps, num_viruses, maxPop, maxBirthProb, clearProb):
    """
    Runs simulation once
    returns: list of pop data in time steps
    """
    viruses = list()
    for i in xrange(num_viruses):
        viruses.append( SimpleVirus(maxBirthProb, clearProb) )

    patient = SimplePatient(viruses, maxPop)

    data = [ len(viruses) ]
    for s in xrange(time_steps):
        data.append( patient.update() )
    return data


def simulationWithoutDrug(num_trials = 1, time_steps = 300, num_viruses = 100, maxPop = 1000, maxBirthProb = 0.1, clearProb = 0.05):

    """
    Run the simulation and plot the graph for problem 2 (no drugs are used,
    viruses do not have any drug resistance).    
    Instantiates a patient, runs a simulation for 300 timesteps, and plots the
    total virus population as a function of time.    
    """
    plot_data = list()
    for i in xrange(num_trials):
        trial = runSim(time_steps, num_viruses, maxPop, maxBirthProb, clearProb)
        if len(plot_data) is 0:
            plot_data = trial
            continue

        for j in xrange(len(trial)):
            plot_data[j] += trial[j]

    for i in xrange(len(plot_data)):
        plot_data[i] /= float(num_trials)


    pylab.plot( plot_data, label = 'SimpleVirus' )
    pylab.title(' SimpleVirus Simulation ')
    pylab.xlabel(' Time lapse ')
    pylab.ylabel(' Virus Population ')
    pylab.legend(loc = 'best')
