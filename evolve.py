#www.github.com/ssangervasi/genetic-cart-optimizer
#(c) 2014 Sebastian Sangervasi
#
#

from structures import *

   
def test():
    cart = ["apples","oranges", "bananas"]
    sellers = {"alpha":[("apples", 1.1, 1),("oranges",3.5,1)], "beta":[("bananas", 1.0, 2),("oranges",3.1,1)], "gamma":[("bananas", 3.0, 2),("oranges",1.1,1)]}
    pmin = 1.0
    mark = Market(cart,sellers,pmin)
    print " MmHmm"
    
    firstGen = Population(10)
    firstGen.initializeRandom(mark)
    newGen = firstGen.newGeneration()
    for i in range(50):
        newGen = newGen.newGeneration()
    print("First Gen")
    firstGen.displayPriceSat()    
    print("Last Gen")
    newGen.displayPriceSat()
        
test()    
    
    
    
    
    
