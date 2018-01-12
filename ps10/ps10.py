# Problem Set 10
# Name: Mert Dede

#Code shared across examples
import pylab, random, string, copy, math

class Point(object):
    def __init__(self, name, originalAttrs, normalizedAttrs = None):
        """normalizedAttrs and originalAttrs are both arrays"""
        self.name = name
        self.unNormalized = originalAttrs
        self.attrs = normalizedAttrs
    def dimensionality(self):
        return len(self.attrs)
    def getAttrs(self):
        return self.attrs
    def getOriginalAttrs(self):
        return self.unNormalized
    def distance(self, other):
        #Euclidean distance metric
        difference = self.attrs - other.attrs
        return sum(difference * difference) ** 0.5
    def getName(self):
        return self.name
    def toStr(self):
        return self.name + str(self.attrs)
    def __str__(self):
        return self.name
    
class County(Point):
    ## weights = pylab.array([1.0] * 14)
    
    vector = [1.0] * 14
    vector[3-1] = 0
    vector[2-1] = 0 # HomeValue
    vector[7-1] = 0 # Below18
    vector[10-1] = 0 # PercentCollage
    vector[4-1] = 0 # PopDensity
    vector[9-1] = 0.5 # HSGraduate
    vector[8-1] = 0 # PrcntFemale
    vector[6-1] = 0.25 # Prcnt65+
    
    weights = pylab.array(vector)
    
    # Override Point.distance to use County.weights to decide the
    # significance of each dimension
    def distance(self, other):
        difference = self.getAttrs() - other.getAttrs()
        return sum(County.weights * difference * difference) ** 0.5
    
class Cluster(object):
    def __init__(self, points, pointType):
        self.points = points
        self.pointType = pointType
        self.centroid = self.computeCentroid()
    def getCentroid(self):
        return self.centroid
    def computeCentroid(self):
        dim = self.points[0].dimensionality()
        totVals = pylab.array([0.0]*dim)
        for p in self.points:
            totVals += p.getAttrs()
        meanPoint = self.pointType('mean',
                                   totVals/float(len(self.points)),
                                   totVals/float(len(self.points)))
        return meanPoint
    def update(self, points):
        oldCentroid = self.centroid
        self.points = points
        if len(points) > 0:
            self.centroid = self.computeCentroid()
            return oldCentroid.distance(self.centroid)
        else:
            return 0.0
    def getPoints(self):
        return self.points
    def contains(self, name):
        for p in self.points:
            if p.getName() == name:
                return True
        return False
    def toStr(self):
        result = ''
        for p in self.points:
            result = result + p.toStr() + ', '
        return result[:-2]
    def __str__(self):
        result = ''
        for p in self.points:
            result = result + str(p) + ', '
        return result[:-2]
    
def kmeans(points, k, cutoff, pointType, minIters = 3, maxIters = 100, toPrint = False):
    """ Returns (Cluster list, max dist of any point to its cluster) """
    #Uses random initial centroids
    initialCentroids = random.sample(points,k)
    clusters = []
    for p in initialCentroids:
        clusters.append(Cluster([p], pointType))
    numIters = 0
    biggestChange = cutoff
    while (biggestChange >= cutoff and numIters < maxIters) or numIters < minIters:
        print("Starting iteration " + str(numIters))
        newClusters = []
        for c in clusters:
            newClusters.append([])
        for p in points:
            smallestDistance = p.distance(clusters[0].getCentroid())
            index = 0
            for i in range(len(clusters)):
                distance = p.distance(clusters[i].getCentroid())
                if distance < smallestDistance:
                    smallestDistance = distance
                    index = i
            newClusters[index].append(p)
        biggestChange = 0.0
        for i in range(len(clusters)):
            change = clusters[i].update(newClusters[i])
            #print "Cluster " + str(i) + ": " + str(len(clusters[i].points))
            biggestChange = max(biggestChange, change)
        numIters += 1
        if toPrint:
            print('Iteration count =', numIters)
    maxDist = 0.0
    for c in clusters:
        for p in c.getPoints():
            if p.distance(c.getCentroid()) > maxDist:
                maxDist = p.distance(c.getCentroid())
    print('Total Number of iterations =', numIters, 'Max Diameter =', maxDist)
    print(biggestChange)
    return clusters, maxDist

#US Counties example
def readCountyData(fName, numEntries = 14):
    dataFile = open(fName, 'r')
    dataList = []
    nameList = []
    maxVals = pylab.array([0.0]*numEntries)
    #Build unnormalized feature vector
    for line in dataFile:
        if len(line) == 0 or line[0] == '#':
            continue
        dataLine = string.split(line)
        name = dataLine[0] + dataLine[1]
        features = []
        #Build vector with numEntries features
        for f in dataLine[2:]:
            try:
                f = float(f)
                features.append(f)
                if f > maxVals[len(features)-1]:
                    maxVals[len(features)-1] = f
            except ValueError:
                name = name + f
        if len(features) != numEntries:
            continue
        dataList.append(features)
        nameList.append(name)
    return nameList, dataList, maxVals
    
def buildCountyPoints(fName):
    """
    Given an input filename, reads County values from the file and returns
    them all in a list.
    """
    nameList, featureList, maxVals = readCountyData(fName)
    points = []
    for i in range(len(nameList)):
        originalAttrs = pylab.array(featureList[i])
        normalizedAttrs = originalAttrs/pylab.array(maxVals)
        points.append(County(nameList[i], originalAttrs, normalizedAttrs))
    return points

def randomPartition(l, p):
    """
    Splits the input list into two partitions, where each element of l is
    in the first partition with probability p and the second one with
    probability (1.0 - p).
    
    l: The list to split
    p: The probability that an element of l will be in the first partition
    
    Returns: a tuple of lists, containing the elements of the first and
    second partitions.
    """
    l1 = []
    l2 = []
    for x in l:
        if random.random() < p:
            l1.append(x)
        else:
            l2.append(x)
    return (l1,l2)

def getAveIncome(cluster):
    """
    Given a Cluster object, finds the average income field over the members
    of that cluster.
    
    cluster: the Cluster object to check
    
    Returns: a float representing the computed average income value
    """
    tot = 0.0
    numElems = 0
    for c in cluster.getPoints():
        tot += c.getOriginalAttrs()[1]

    return float(tot) / len(cluster.getPoints())


def test(points, k = 200, cutoff = 0.1):
    """
    A sample function to show you how to do a simple kmeans run and graph
    the results.
    """
    incomes = []
    print('')
    clusters, maxSmallest = kmeans(points, k, cutoff, County)

    for i in range(len(clusters)):
        if len(clusters[i].points) == 0: continue
        incomes.append(getAveIncome(clusters[i]))

    pylab.hist(incomes)
    pylab.xlabel('Ave. Income')
    pylab.ylabel('Number of Clusters')
    pylab.show()

def graphRemovedErr(points, kvals = [25, 50, 75, 100, 125, 150], cutoff = 0.1):
    
    errors = dict() #contains tuples as (holdout error, training error)
    
    for k in kvals:
        holdoutSet, trainingSet = randomPartition(points, 0.2)
        trainingClusters, maxDist = kmeans(trainingSet, k, cutoff, County)

        trainingError = list()
        for c in trainingClusters:
            for p in c.getPoints():
                trainingError.append( p.distance( c.getCentroid() )**2  )

        holdoutError = list()
        for p in holdoutSet:
            minDist = None
            for c in trainingClusters:
                if minDist is None or minDist > p.distance( c.getCentroid() ):
                    minDist = p.distance( c.getCentroid() )
                    
            holdoutError.append( minDist**2 )
        
        errors[k] = sum(holdoutError), sum(trainingError)

    # Plotting #
    pylab.figure( ' Error Analysis ' )
    plotNum = 0
    for k in kvals:
        plotNum += 1
        pylab.subplot(2, 3, plotNum)
        pylab.title( 'k: ' + str(k) )
        pylab.ylabel( ' Error Value ' )
        # pylab.ylim(0, errors[ kvals[0] ][1]+errors[ kvals[0] ][0] )
        
        pylab.hist( errors[k][0], label = ' Holdout Set ' , orientation = 'horizontal')
        pylab.hist( errors[k][1], label = ' Training Set  ', orientation = 'horizontal' )
        pylab.legend( loc = 'best' )

    pylab.figure(' Ratio of Errors ')
    pylab.title( ' Training Set Error / Holdout Set Error ' )
    pylab.xlabel(' k ')
    pylab.ylabel(' Ratio ')
    errorRatio = list()
    for k in kvals: errorRatio.append( float(errors[k][1])/errors[k][0] )
    pylab.plot(kvals, errorRatio)
    
    pylab.show()
    
def get_aveVal(cluster, dimension):
    tot = 0.0
    numElems = 0
    for c in cluster.getPoints():
        tot += c.getOriginalAttrs()[dimension-1]

    return float(tot) / len(cluster.getPoints())

def getPredictionErr(holdoutSet, nearestCluster, trainingClusters, aveVal, dimension):
    """
    holdoutSet: list
    nearestCluster: dict, keys as holdoutSet points
    trainingClusters: list
    aveVal: dict, keys as trainingClusters clusters
    dimension: int
    """
    
    error = list()
   
    return error

def graphPredictionErr(points, dimension, kvals = [25, 50, 75, 100, 125, 150], cutoff = 0.1):
    """
    Given input points and a dimension to predict, should cluster on the
    appropriate values of k and graph the error in the resulting predictions,
    as described in Problem 3.
    """

    for p in points: p.weights[dimension-1] = 0.0
    holdoutSet, trainingSet = randomPartition(points, 0.2)

    plotData = dict() # error as key k
    for k in kvals:
        trainingClusters, maxDist = kmeans(trainingSet, k, cutoff, County)

        # Find nearest clusters
        nearestCluster = dict() # keys are holdoutSet points, values are clusters
        for i in range( len(holdoutSet) ):
            minDist = None
            for j in range( len(trainingClusters) ):
                if minDist is None or minDist > holdoutSet[i].distance( trainingClusters[j].getCentroid() ):
                    minDist = holdoutSet[i].distance( trainingClusters[j].getCentroid() )
                    nearestCluster[ holdoutSet[i] ] = trainingClusters[j]

        # Find average value of clusters
        aveVal = dict() # Cluster as key, float as value
        for i in range( len(trainingClusters) ):
            aveVal[ trainingClusters[i] ] = get_aveVal( trainingClusters[i], dimension )

        # Find prediction error
        errors = list()
        for p in holdoutSet:
            errors.append( ( aveVal[ nearestCluster[p] ] - p.getOriginalAttrs()[dimension-1] )**2 )

        plotData[k] = errors

    # Plotting #
    pylab.figure( ' Prediction Errors ' )
    plotNum = 0
    for k in kvals:
        plotNum += 1
        pylab.subplot(2, 3, plotNum)
        pylab.title( 'k: ' + str(k) )
        pylab.xlabel( ' Error value ' )
        pylab.ylabel( ' # of Counties ' )
        pylab.hist( plotData[k], label = ' Poverty std error ')

    pylab.show()
            

def graphPredictionErr2(points, dimension, kvals = [25, 50, 75, 100, 125, 150], cutoff = 0.1):
    """
    Given input points and a dimension to predict, should cluster on the
    appropriate values of k and graph the error in the resulting predictions,
    as described in Problem 3.
    """

    holdoutSet, trainingSet = randomPartition(points, 0.2)

    plotData = dict() # error as key k
    for k in kvals:
        trainingClusters, maxDist = kmeans(trainingSet, k, cutoff, County)

        # Find nearest clusters
        nearestCluster = dict() # keys are holdoutSet points, values are clusters
        for i in range( len(holdoutSet) ):
            minDist = None
            for j in range( len(trainingClusters) ):
                if minDist is None or minDist > holdoutSet[i].distance( trainingClusters[j].getCentroid() ):
                    minDist = holdoutSet[i].distance( trainingClusters[j].getCentroid() )
                    nearestCluster[ holdoutSet[i] ] = trainingClusters[j]

        # Find average value of clusters
        aveVal = dict() # Cluster as key, float as value
        for i in range( len(trainingClusters) ):
            aveVal[ trainingClusters[i] ] = get_aveVal( trainingClusters[i], dimension )

        # Find prediction error
        errors = list()
        for p in holdoutSet:
            errors.append( ( aveVal[ nearestCluster[p] ] - p.getOriginalAttrs()[dimension-1] )**2 )

        plotData[k] = errors

    # Plotting #
    pylab.figure( ' Prediction Errors ' )
    plotNum = 0
    for k in kvals:
        plotNum += 1
        pylab.subplot(2, 3, plotNum)
        pylab.title( 'k: ' + str(k) )
        pylab.xlabel( ' Error value ' )
        pylab.ylabel( ' # of Counties ' )
        pylab.hist( plotData[k], label = ' Poverty std error ')

    pylab.show()

##if __name__ == '__main__':
##    points = buildCountyPoints('counties.txt')
##    graphPredictionErr2(points, 3)
