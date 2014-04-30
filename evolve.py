#www.github.com/ssangervasi/genetic-cart-optimizer
#(c) 2014 Sebastian Sangervasi
#
#

from structures import *
from generateData import *
import sys 
import April30

def test():
    cart = ["apples","oranges", "bananas"]
    sellers = {"alpha":[("apples", 1.1, 1),("oranges",3.5,1)], "beta":[("bananas", 1.0, 2),("oranges",3.1,1)], "gamma":[("bananas", 3.0, 2),("oranges",1.1,1)]}
    pmin = 2.0
    mark = Market(cart,sellers,pmin)
    
    firstGen = Population(10)
    firstGen.initializeRandom(mark)
    newGen = firstGen.newGeneration()
    for i in range(50):
        newGen = newGen.newGeneration()
    print("First Gen")
    firstGen.displayPriceSat()    
    print("Last Gen")
    newGen.displayPriceSat()
    return
    
        
def testLargeData(data = None):
    cart = April30.Cart
    sellers = April30.Sellers
    pmin = 1.0
    mark = Market(cart,sellers,pmin)
    print "Satisfiable? ", mark.satisfiable
    firstGen = Population(64)
    firstGen.initializeRandom(mark)
    newGen = firstGen.newGeneration()
    
    numGens = 100000
    onePercent = numGens/100
    fivePercent = numGens/20
    twentyPercent = numGens/5
    fiftyPercent = numGens/2
    print ( "Evolving\n" + "[" + " "*100 + "]")
    for i in range( numGens):
        newGen = newGen.newGeneration()
        if i == 0:
            sys.stdout.write('[')
        elif i %fiftyPercent == 0:
            sys.stdout.write("||")
        elif i %twentyPercent == 0:
            sys.stdout.write("=")
        elif i%(fivePercent) == 0:
            sys.stdout.write("~")
        elif i%(onePercent) == 0:
            sys.stdout.write("-")
        sys.stdout.flush()
    sys.stdout.write("]\n")
    print("First Gen")
    firstGen.displayPriceSat()    
    print("Last Gen")
    newGen.displayPriceSat()
    return    
    
testLargeData()
    
    
    
