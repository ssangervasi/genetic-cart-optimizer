#www.github.com/ssangervasi/genetic-cart-optimizer
#(c) 2014 Sebastian Sangervasi
#
#

from structures import *
from generateData import *
import sys
#This imports the data file. Need a smoother way of doing this input.
import May3 as DataSet

        
def testLargeData(numGens = 10000):
    cart = DataSet.Cart
    sellers = DataSet.Sellers
    pmin = 1.0
    mark = Market(cart,sellers,pmin)
    print ("Satisfiable? ", mark.satisfiable)
    firstGen = Population(64)
    firstGen.initializeRandom(mark)
    prevGen = firstGen.newGeneration()
    prevAvFit = firstGen.populationFeatures()[-1]
    newAvFit = prevAvFit
    
    onePercent = numGens/100
    fivePercent = numGens/20
    twentyPercent = numGens/5
    fiftyPercent = numGens/2
    print ( "Evolving\n" + "[" + " "*100 + "]")
    outString = ""
    for i in range( numGens):
        newGen = prevGen.newGeneration()
        
        if i == 0:
            sys.stdout.write('[')
            outString += '['
        elif i %fiftyPercent == 0:
            sys.stdout.write("||")
            outString += '||'
        elif i %twentyPercent == 0:
            sys.stdout.write("=")
            outString += '='
        elif i%(fivePercent) == 0:
            sys.stdout.write("~")
            outString += '~'
            newAvFit = prevGen.populationFeatures()[-1]
            perChangeFit = round(100.0*(newAvFit-prevAvFit)/float(prevAvFit),4)
            prevAvFit = newAvFit
            if perChangeFit >= 5:
                sys.stdout.write("\nSignificant Fitness Increase: " +str(perChangeFit)+"%  At Gen: " + str(i)+"\n"+outString)
        elif i%(onePercent) == 0:
            sys.stdout.write("-")
            outString += '-'
        sys.stdout.flush()
        prevGen = newGen
    sys.stdout.write("]\n")
    print("First Gen")
    firstGen.sortByFitness()
    firstGen.populationFeatures(echo = True)    
    print("Last Gen")
    newGen.newGeneration() #Fitenss only updated on redproduction
    newGen.sortByFitness()
    newGen.populationFeatures(echo = True)
    newGen.writeToFile("testOutput")
    return    
    
#testLargeData()
testLargeData(numGens = 500)   
    
    
