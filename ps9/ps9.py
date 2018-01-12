# 6.00 Problem Set 9
#
# Intelligent Course Advisor
#
# Name: Mert Dede

SUBJECT_FILENAME = "subjects.txt"
SHORT_SUBJECT_FILENAME = "shortened_subjects.txt"
VALUE, WORK = 0, 1

#
# Problem 1: Building A Subject Dictionary
#
def loadSubjects(filename):
    """
    Returns a dictionary mapping subject name to (value, work), where the name
    is a string and the value and work are integers. The subject information is
    read from the file named by the string filename. Each line of the file
    contains a string of the form "name,value,work".

    returns: dictionary mapping subject name to (value, work)
    """
    subjects = dict()
    
    # The following sample code reads lines from the specified file and prints
    # each one.
    inputFile = open(filename)
    for line in inputFile:
        subject, val, work = tuple( line.strip('\n\r').split(',') )
        subjects[ subject ] = int(val), int(work)

    # TODO: Instead of printing each line, modify the above to parse the name,
    # value, and work of each subject and create a dictionary mapping the name
    # to the (value, work).

    return subjects

def printSubjects(subjects):
    """
    Prints a string containing name, value, and work of each subject in
    the dictionary of subjects and total value and work of all subjects
    """
    totalVal, totalWork = 0,0
    if len(subjects) == 0:
        return 'Empty SubjectList'
    res = 'Course\tValue\tWork\n======\t====\t=====\n'
    subNames = subjects.keys()
    subNames.sort()
    for s in subNames:
        val = subjects[s][VALUE]
        work = subjects[s][WORK]
        res = res + s + '\t' + str(val) + '\t' + str(work) + '\n'
        totalVal += val
        totalWork += work
    res = res + '\nTotal Value:\t' + str(totalVal) +'\n'
    res = res + 'Total Work:\t' + str(totalWork) + '\n'
    print res


#
# Problem 2: Subject Selection By Greedy Optimization
#

def cmpValue(subInfo1, subInfo2):
    """
    Returns True if value in (value, work) tuple subInfo1 is GREATER than
    value in (value, work) tuple in subInfo2
    """
    # TODO...
    return subInfo1[0] > subInfo2[0]

def cmpWork(subInfo1, subInfo2):
    """
    Returns True if work in (value, work) tuple subInfo1 is LESS than than work
    in (value, work) tuple in subInfo2
    """
    # TODO...
    return subInfo1[1] < subInfo2[1]

def cmpRatio(subInfo1, subInfo2):
    """
    Returns True if value/work in (value, work) tuple subInfo1 is 
    GREATER than value/work in (value, work) tuple in subInfo2
    """
    # TODO...

    return ( float(subInfo1[0])/subInfo1[1] ) > ( float(subInfo2[0]) / subInfo2[1] )

def greedyAdvisor(subjects, maxWork, comparator):
    """
    Returns a dictionary mapping subject name to (value, work) which includes
    subjects selected by the algorithm, such that the total work of subjects in
    the dictionary is not greater than maxWork.  The subjects are chosen using
    a greedy algorithm.  The subjects dictionary should not be mutated.

    subjects: dictionary mapping subject name to (value, work)
    maxWork: int >= 0
    comparator: function taking two tuples and returning a bool
    returns: dictionary mapping subject name to (value, work)
    """
    # TODO...
    assert maxWork > 0
    
    advice = dict()
    work = 0 
    keys = subjects.keys()
    
    satisfied = False
    while not satisfied:
        best = None
        for key in keys:
            comp = subjects[key]
            if advice.get(key, 0) is 0 and work+comp[1] <= maxWork and (best is None or comparator(best[1], comp) is False):
                best = key, comp
                
        if best is None:
            satisfied = True
            continue

        advice[best[0]] = best[1]
        work += best[1][1]

    return advice   

#
# Problem 3: Subject Selection By Brute Force
#
def bruteForceAdvisor(subjects, maxWork):
    """
    Returns a dictionary mapping subject name to (value, work), which
    represents the globally optimal selection of subjects using a brute force
    algorithm.

    subjects: dictionary mapping subject name to (value, work)
    maxWork: int >= 0
    returns: dictionary mapping subject name to (value, work)
    """
    # list, work comp. func
    def verify(dictionary):
        work = 0
        for item in dictionary:
            work += dictionary[item][1]

        return maxWork >= work
    
    # list, allAdvices
    allAdvices = list()
    prev_loop = list()
    for sub in subjects:
        if maxWork >= subjects[sub][1]:
            prev_loop.append( {sub: subjects[sub]} )
    allAdvices += prev_loop
        
    while len(prev_loop) != 0:   
        new_loop = list()

        for item in prev_loop:
            for sub in subjects:
                if sub in item:
                    continue
                
                new_item = item.copy()
                new_item.update( {sub: subjects[sub]} )
                
                if verify(new_item):
                    new_loop.append( new_item )

        prev_loop = new_loop
        allAdvices += prev_loop
        
    # Selector comp. func
    def better(dictA, dictB):
        valueA = 0
        for sub in dictA:
            valueA += dictA[sub][0]

        valueB = 0
        for sub in dictB:
            valueB += dictB[sub][0]

        return valueA >= valueB

    # Selector
    import random
    best = random.choice( allAdvices )
    
    for advice in allAdvices:
        if not better(best, advice):
            best = advice

    return best
            

subjects = loadSubjects(SUBJECT_FILENAME)
print( bruteForceAdvisor(subjects, 6) )





        
