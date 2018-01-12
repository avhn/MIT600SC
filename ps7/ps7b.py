import random, pylab

class simpleDice(object):
    def __init__(self):
        self.sides = 6
        
    def roll(self):
        return random.choice(range(1, 7))

class diceBag(object):
    def __init__(self, num_dices = 5):
        self.dices = list()
        for i in xrange(num_dices):
            self.dices.append( simpleDice() )
    
    def is_yahtzee(self, seq):
        """
        seq: list of values
        returns: True if all values equal
        """
        
        checker = seq[0]
        for i in seq:
            if checker != i:
                return False
        return True
            
    def roll(self):
        """
        Rolls the bag and checks sequence
        returns: True if yathzee
        """
        
        seq = list()
        for dice in self.dices:
            seq.append( dice.roll() )
            
        return self.is_yahtzee(seq)
    

def simYahtzee(num_trials = 1000, num_dice = 5):
    bag = diceBag(num_dice)

    success = 0
    for i in xrange(num_trials):
        success += bag.roll()

    pylab.title('Rolling for yahtzee, %d simple dices' % num_dice )
    pylab.pie([success, num_trials-success], labels = ['Yathzee', 'Non'], colors = ['g','r'], autopct = '%0.5f')
