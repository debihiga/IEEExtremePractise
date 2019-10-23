
DEBUG = True

match_table = []

rock = "Rock"
paper = "Paper"
scissors = "Scissors"
lizard = "Lizard"
spock = "Spock"

shapes = {  "Rock":         0,
            "Paper":        1,
            "Lizard":       2,
            "Spock":        3,
            "Scissors":     4}

rules = {   0:  (rock,      (shapes[scissors], shapes[lizard]),     (shapes[paper], shapes[spock])),
            1:  (paper,     (shapes[rock], shapes[spock]),          (shapes[scissors], shapes[lizard])),
            2:  (lizard,    (shapes[paper], shapes[spock]),         (shapes[scissors], shapes[rock])),
            3:  (spock,     (shapes[scissors], shapes[rock]),       (shapes[paper], shapes[lizard])),
            4:  (scissors,  (shapes[paper], shapes[lizard]),        (shapes[rock], shapes[spock]))}

alice_rules = {
            0: shapes[paper],
            1: shapes[scissors],
            2: shapes[rock],
            3: shapes[lizard],
            4: shapes[spock]
}
"""
rules = {   "Rock":         (scissors, lizard),
            "Paper":        (rock, spock),
            "Scissors":     (paper, lizard),
            "Lizard":       (paper, spock),
            "Spock":        (scissors, rock)}
"""
def getShapeName(shape):
    return rules[shape][0]
def getShapesOK(shape):
    return rules[shape][1]
def getShapesKO(shape):
    return rules[shape][2]
def shape1OKshape2(shape_1, shape_2):
    shapes_beaten = getShapesOK(shape_1)
    if shape_2 in shapes_beaten:
        return True
    else:
        return False

TIE = -1

class Player:

    def __init__(self, id, name):
        self.id = id
        self.name = name
        self.win_games = 0
        self.shape = rock
    def addWinGame(self):
        self.win_games += 1
    def resetWinGame(self):
        self.win_games = 0
    def setShape(self, shape):
        self.shape = shapes[shape]
    def getShape(self):
        return getShapeName(self.shape)

class Alice(Player):

    def __init__(self):
        super().__init__(0, "Alice")

    def setShapeAfterWon(self):
        """
        1) If she wins a game, she keeps the same shape.
        """
        pass
    def setShapeAfterTied(self):
        """
        2) If she ties, she chooses a shape from one of the two that would beat her current shape.
        Of these two, she chooses the one that beats the other.
        For example, if she has tied when choosing Rock,
        her options are Paper and Spock.
        Since Paper beats Spock, she chooses Paper.
        """
        # self.shape = self.getBestShape(self.shape)
        self.shape = alice_rules[self.shape]
    def setShapeAfterLost(self, opponent_shape):
        """
        3) If she loses, she chooses a shape from one of the two that would
        beat her opponent's current shape.
        Of these two, she chooses the one that beats the other.
        For example, let's say she has lost by choosing Rock,
        when her opponent chose Paper.
        She will then choose from Scissors or Lizard.
        Since Scissors beats Lizard, she chooses Scissors.
        """
        #self.shape = self.getBestShape(oponent_shape)
        self.shape = alice_rules[opponent_shape]

class Bob(Player):

    def __init__(self):
        super().__init__(1, "Bob")

    def setShapeAfterWon(self):
        """
        2) If he won the previous turn when playing Spock, he chooses Rock.
        """
        if self.shape == shapes[spock]:
            self.setShape(rock)
        else:
            self.setShape(spock)
    def setShapeAfterTied(self):
        """
        3) If he tied the previous turn when playing Spock, he chooses Lizard.
        """
        if self.shape == shapes[spock]:
            self.setShape(lizard)
        else:
            self.setShape(spock)
    def setShapeAfterLost(self):
        """
        4) If he lost the previous turn when playing Spock, he chooses Paper.
        """
        if self.shape == shapes[spock]:
            self.setShape(paper)
        else:
            self.setShape(spock)

alice = Alice()
bob = Bob()

"""
        Bob

Alice     (alice, bob)
"""
def generateMatchTable():
    # for alice_shape in shapes.values(): <- no devuelve ordenado.
    for alice_shape in range(5):
        row = []
        for bob_shape in range(5):
            alice.shape = alice_shape
            bob.shape = bob_shape
            winner = -1
            if alice.shape == bob.shape:
                alice.setShapeAfterTied()
                bob.setShapeAfterTied()
            elif shape1OKshape2(alice.shape, bob.shape):
                winner = alice.id
                alice.setShapeAfterWon()
                bob.setShapeAfterLost()
            else:
                winner = bob.id
                alice.setShapeAfterLost(bob.shape)
                bob.setShapeAfterWon()
            row.append((alice.shape, bob.shape, winner))
        match_table.append(row)
    print(match_table)

def checkIfCyclic():
    for alice_shape_i in range(5):
        for bob_shape_i in range(5):  # Bob never uses scissors.
            (alice_shape_f, bob_shape_f, winner) = match_table[alice_shape_i][bob_shape_i]
            i = 0
            print(str(alice_shape_i)+" "+str(bob_shape_i))
            while alice_shape_i!=alice_shape_f and bob_shape_i!=bob_shape_f:
                alice_shape_i = alice_shape_f
                bob_shape_i = bob_shape_f
                (alice_shape_f, bob_shape_f, winner) = match_table[alice_shape_i][bob_shape_i]
                i += 1
            print(i)
            print("Cyclic!")

cycles = []
def generateCyclesMatch(alice_shape_i, bob_shape_i):
    alice_shape_f = None
    bob_shape_f = None
    i = 0
    cycle = []
    while not (alice_shape_i==alice_shape_f and bob_shape_i==bob_shape_f):
        if alice_shape_f is None and bob_shape_f is None:
            alice_shape_f = alice_shape_i
            bob_shape_f = bob_shape_i
        (alice_shape_f, bob_shape_f, winner) = match_table[alice_shape_f][bob_shape_f]
        cycle.append((alice_shape_f, bob_shape_f, winner))
        i += 1
        if 1000<i:
            if (4, 3, -1) in cycle and (2, 0, 1) in cycle and (1,3,1) in cycle and (1,1,0) in cycle:
                return True
            return None
    print(i)
    return cycle

if __name__ == "__main__":
    generateMatchTable()
    #checkIfCyclic()
    for row in range(5):
        cycle = []
        for col in range(5):
            result = generateCyclesMatch(row, col)
            cycle.append(result)
        cycles.append(cycle)
    print(cycles)
