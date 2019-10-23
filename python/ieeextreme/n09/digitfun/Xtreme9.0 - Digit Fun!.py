import sys

def main(argv):

    #input = getInput()

    for line in sys.stdin:
        if "END" in line:
            break
        A = line.replace("\n","")
        #i = findCondition(A, 0)
        i = findCondition(A, 0)
        #print("Result for "+str(A)+" is "+str(i))
        print(i)

# A [str]
# j = i-1

def findCondition(Aj, j):
    if Aj=="1":
        return j+1
    else:
        Ai = len(Aj)
        if Ai==1:
            return j+2
        elif Ai<10:
            return j+3
        else:
            return j+4

    """
def findCondition(A):
    if
    # Ai = len(str(Aj)) # TIMEOUT
    Ai = len(Aj)
    #print(Ai)
    #print(Aj)
    #print(j)
    # Case 1
    if 10<=Ai:
        return j+4
    else:
        Aj_n = int(Aj)
        # Case 2
        if Aj_n==Ai:
            return j+1
        elif Aj_n==0:
            return j+2
        else:
            return j+3
            #findCondition(str(Ai), j+1)
    """
    """
    ---------------------    
    Case 1: 10<=n<=1.000.000
    ------

    A0=0
    A1=|A0|=1
    A2=|A1|=1
    
    A0=1
    A1=|A0|=1

    A0=2,3,4,5,6,7,8,9
    A1=|A0|=1
    A2=|A1|=1

    A0=10,...,
    A1=|A0|=2
    A2=|A1|=1
    A3=|A2|=1
    
    A1=|A0|=1.000.000
    A2=|A1|=7
    A3=|A2|=1
    A4=|A3|=1=A4
    
    A1=|A0|=1000
    A2=|A1|=4
    A3=|A2|=1
    A4=|A3|=1
    
    A1=|A0|=100
    A2=|A1|=3
    A3=|A2|=1
    A4=|A3|=1
    
    A1=|A0|=10
    A2=|A1|=2
    A3=|A2|=1
    A4=|A3|=1
   

    
    
    
    
    """


    """
def findCondition(Aj, j):
    Ai = len(Aj) # TIMEOUT
    if Ai==int(Aj):
        return j+1
    else:
        return findCondition(str(Ai), j+1)
    """

def getInput():
    inputs = []
    for input in sys.stdin:
        inputs.append(input)
    return inputs

if __name__ == "__main__":
    main(sys.argv)
    """
    for i in range(1000000000000000000000000000000000):
        if i == len(str(i)):
            print(i)
    """