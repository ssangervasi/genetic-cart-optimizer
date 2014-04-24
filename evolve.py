#www.github.com/ssangervasi/genetic-cart-optimizer
#(c) 2014 Sebastian Sangervasi
#
#

from structures import *

   
def test():
    cart = ["apples","oranges", "bananas"]
    sellers = {"alpha":[("apples", 1.1, 1),("oranges",1.5,1)], "beta":[("bananas", 2.0, 2),("oranges",1.1,1)]}
    pmin = 1.0
    mark = Market(cart,sellers,pmin)
    print " MmHmm"
    
    firstGen = Population(4)
    firstGen.initializeRandom(mark)
    
    secondGen = firstGen.newGeneration()
        
test()    
    
    
    
    
    
