# Problem Set 6: Simulating robots
# Name: Mert Dede

import math
import random

import ps6_visualize
import pylab

# === Provided classes

class Position(object):
    """
    A Position represents a location in a two-dimensional room.
    """
    def __init__(self, x, y):
        """
        Initializes a position with coordinates (x, y).
        """
        self.x = x
        self.y = y
    def getX(self):
        return self.x
    def getY(self):
        return self.y
    def getNewPosition(self, angle, speed):
        """
        Computes and returns the new Position after a single clock-tick has
        passed, with this object as the current position, and with the
        specified angle and speed.

        Does NOT test whether the returned position fits inside the room.

        angle: float representing angle in degrees, 0 <= angle < 360
        speed: positive float representing speed

        Returns: a Position object representing the new position.
        """
        old_x, old_y = self.getX(), self.getY()
        # Compute the change in position
        delta_y = speed * math.cos(math.radians(angle))
        delta_x = speed * math.sin(math.radians(angle))
        # Add that to the existing position
        new_x = old_x + delta_x
        new_y = old_y + delta_y
        return Position(new_x, new_y)

# === Problems 1

class RectangularRoom(object):
    """
    A RectangularRoom represents a rectangular region containing clean or dirty
    tiles.

    A room has a width and a height and contains (width * height) tiles. At any
    particular time, each of these tiles is either clean or dirty.
    """
    def __init__(self, width, height):
        """
        Initializes a rectangular room with the specified width and height.

        Initially, no tiles in the room have been cleaned.

        width: an integer > 0
        height: an integer > 0
        """
        self.w = width
        self.h = height

        self.cleaned = list()
    def cleanTileAtPosition(self, pos):
        """
        Mark the tile under the position POS as cleaned.

        Assumes that POS represents a valid position inside this room.

        pos: a Position
        """

        even_pos = int(pos.getX()), int(pos.getY())
        if not even_pos in self.cleaned:
            self.cleaned.append(even_pos)
            
    def isTileCleaned(self, m, n):
        """
        Return True if the tile (m, n) has been cleaned.

        Assumes that (m, n) represents a valid tile inside the room.

        m: an integer
        n: an integer
        returns: True if (m, n) is cleaned, False otherwise
        """
        if (m, n) in self.cleaned:
            return True
        return False
    
    def getNumTiles(self):
        """
        Return the total number of tiles in the room.

        returns: an integer
        """
        return self.w * self.h

    def getNumCleanedTiles(self):
        """
        Return the total number of clean tiles in the room.

        returns: an integer
        """
        return len(self.cleaned)

    def getRandomPosition(self):
        """
        Return a random position inside the room.

        returns: a Position object.
        """
        return Position(random.choice( [round(w*.1, 1) for w in range((self.w)*10)] ), random.choice( [round(h*.1,1) for h in range((self.h)*10)] ))

    def isPositionInRoom(self, pos):
        """
        Return True if pos is inside the room.

        pos: a Position object.
        returns: True if pos is in the room, False otherwise.
        """
        return ( 0 < pos.getX() and pos.getX() < self.w ) and (0 < pos.getY() and pos.getY() < self.h )

    def dirtyRoom(self):
        self.cleaned = list()

class Robot(object):
    """
    Represents a robot cleaning a particular room.

    At all times the robot has a particular position and direction in the room.
    The robot also has a fixed speed.

    Subclasses of Robot should provide movement strategies by implementing
    updatePositionAndClean(), which simulates a single time-step.
    """
    def __init__(self, room, speed):
        """
        Initializes a Robot with the given speed in the specified room. The
        robot initially has a random direction and a random position in the
        room. The robot cleans the tile it is on.

        room:  a RectangularRoom object.
        speed: a float (speed > 0)
        """
        self.room = room
        self.speed = speed
        self.direction = random.choice(range(360))
        
        self.pos = self.room.getRandomPosition()
    def getRobotPosition(self):
        """
        Return the position of the robot.

        returns: a Position object giving the robot's position.
        """
        return self.pos
    
    def getRobotDirection(self):
        """
        Return the direction of the robot.

        returns: an integer d giving the direction of the robot as an angle in
        degrees, 0 <= d < 360.
        """
        return self.direction

    def setRobotPosition(self, position):
        """
        Set the position of the robot to POSITION.

        position: a Position object.
        """
        self.pos = position

    def setRobotDirection(self, direction):
        """
        Set the direction of the robot to DIRECTION.

        direction: integer representing an angle in degrees
        """
        self.direction = direction

    def updatePositionAndClean(self):
        """
        Simulate the raise passage of a single time-step.

        Move the robot to a new position and mark the tile it is on as having
        been cleaned.
        """
        self.pos = self.pos.getNewPosition(self.direction, self.speed)
        self.room.cleanTileAtPosition(self.pos)

# === Problem 2
class StandardRobot(Robot):
    """
    A StandardRobot is a Robot with the standard movement strategy.

    At each time-step, a StandardRobot attempts to move in its current direction; when
    it hits a wall, it chooses a new direction randomly.
    """
    def updatePositionAndClean(self):
        """
        Simulate the passage of a single time-step.

        Move the robot to a new position and mark the tile it is on as having
        been cleaned.
        """
        while True:
            new_pos = self.pos.getNewPosition(self.direction, self.speed)
            if self.room.isPositionInRoom(new_pos):
                self.room.cleanTileAtPosition(new_pos)
                self.setRobotPosition(new_pos)
                break
            self.setRobotDirection(random.randrange(360))

# === Problem 3
def check_coverage(room, min_coverage):
    covered = float(room.getNumCleanedTiles()) / float(room.getNumTiles())
    return min_coverage <= covered

def runSimulation(num_robots, speed, width, height, min_coverage, num_trials,
                  robot_type, runAnim = True):
    """
    Runs NUM_TRIALS trials of the simulation and returns the mean number of
    time-steps needed to clean the fraction MIN_COVERAGE of the room.

    The simulation is run with NUM_ROBOTS robots of type ROBOT_TYPE, each with
    speed SPEED, in a room of dimensions WIDTH x HEIGHT.

    num_robots: an int (num_robots > 0)
    speed: a float (speed > 0)
    width: an int (width > 0)
    height: an int (height > 0)
    min_coverage: a float (0 <= min_coverage <= 1.0)
    num_trials: an int (num_trials > 0)
    robot_type: class of robot to be instantiated (e.g. Robot or
                RandomWalkRobot)
    runAnim: a bool
    """
    assert(num_robots > 0)
    #Initilize specified room
    room = RectangularRoom(width, height)
    
    #Initilize robots
    robots = list()
    for i in range(num_robots): robots.append(robot_type(room, speed))

    #Try number of trials, append time info into a list
    trials = list()
    for curr_trial in range(num_trials):
        time = 0
        if runAnim:
            anim = ps6_visualize.RobotVisualization(num_robots, width, height)
            
        while True:
            time += 1
            for robot in robots:
                robot.updatePositionAndClean()
                
            if runAnim:
                anim.update(room, robots)
            
            if check_coverage(room, min_coverage):
                room.dirtyRoom()
                
                if runAnim:
                    anim.done()
                break

        trials.append(time)
    mean = float(sum(trials))/len(trials)
    return mean

# === Problem 4

def showPlot1():
    """
    Produces a plot showing dependence of cleaning time on number of robots.
    """
    #Set initials
    s, w, h, min_coverage, num_trials = 1, 20, 20, .8, 20

    #Calculate datas
    robots = range(1,11)
    trials = list()
    for num_robots in robots:
        trials.append(runSimulation(num_robots, s, w, h, min_coverage, num_trials, StandardRobot))

    #Plot
    pylab.figure(1)
    pylab.title('Time to clean 80% of a 20x20 room with various robot numbers')
    pylab.xlabel('Number of robots')
    pylab.ylabel('Time')

    pylab.plot(robots, trials)
    pylab.legend(['Standard Robot'])
    pylab.show()
    
def showPlot2():
    """
    Produces a plot showing dependence of cleaning time on room shape.
    """
    #Set initials
    num_robots, s, min_coverage, num_trials = 2, 1, .8, 100
    dimensions = ((20,20), (25,16), (40,10), (50,8), (80, 5), (100, 4))

    #Calculate data
    data = list()
    ratio = list()
    for d in dimensions:
        w, h = d
        ratio.append(float(w)/h)
        data.append(runSimulation(num_robots, s, w, h, min_coverage, num_trials, StandardRobot))

    #Plot
    pylab.figure(1)
    pylab.title('Time to clean 80% of various shaped 400-tile rooms with two robots')
    pylab.xlabel('Aspect Ratio')
    pylab.ylabel('Time')
    pylab.plot(ratio, data)
    pylab.show()

# === Problem 5

class RandomWalkRobot(Robot):
    """
    A RandomWalkRobot is a robot with the "random walk" movement strategy: it
    chooses a new direction at random after each time-step.
    """
    def updatePositionAndClean(self):
        while True:
            self.direction = random.randrange(360)
            new_pos = self.getRobotPosition().getNewPosition(self.direction, self.speed)
            if self.room.isPositionInRoom(new_pos):
                self.pos = new_pos
                self.room.cleanTileAtPosition(self.getRobotPosition())
                break


# === Problem 6

# For the parameters tested below (cleaning 80% of a 20x20 square room),
# RandomWalkRobots take approximately twice as long to clean the same room as
# StandardRobots do.
def showPlot3():
    """
    Produces a plot comparing the two robot strategies for a 20x20 room with 80% minimum coverage.
    """

    s, w, h, min_coverage, num_trials = 1, 20, 20, .8, 20

    standard_robots = list()
    random_robots = list()
    num_robots = range(1,11)
    
    for num in num_robots:
        random_robots.append(float(runSimulation(num, s, w, h, min_coverage, num_trials, RandomWalkRobot)))
        standard_robots.append(float(runSimulation(num, s, w, h, min_coverage, num_trials, StandardRobot)))

    #Plot
    pylab.figure(1)
    pylab.title('Time to clean 80% of a 20x20 square room, with various robot numbers')
    pylab.xlabel('Number of robots')
    pylab.ylabel('Time')
    
    pylab.plot(num_robots, random_robots, 'r')
    pylab.plot(num_robots, standard_robots, 'b')
    pylab.legend(('Random Walk Robots', 'Standard Robots'))

    pylab.show()


print(runSimulation(2, 1, 20, 20, 1, 100, StandardRobot))
