#www.github.com/ssangervasi/genetic-cart-optimizer
#(c) 2014 Sebastian Sangervasi
#
#

import random
import math

class Market:
    '''
        There should be a single market instance for each optimization problem.
        This class is used to keep track of the products in the 'cart' and their availability from sellers.
        It also does some work to determine a baseline for whether the problem can be solved at all.
    
    '''


    def __init__(self, cart, sellers, priceMin):
        '''Class initializer.
        Input:
            cart:   A list of products, as strings of names. 
                        The format "p#x" can be used to represent the x'th copy of product 'name'.
                        Produt names should never inlcude the symbol "#".
            sellers:    A dictionary of seller names mapping to a list of (product name, price, quantity) tuples indicating the seller's inventory.
            priceMin:   Universal minimum price. Implementation may allow this to become seller-dependent.
            
            Output:     None, this is an initilizer.
        '''
        self.priceMin = priceMin
        self.products = {}
        self.priceQuant = {}
        self.unSellers = []
        self.unProducts = []
        
        self.assembleProducts(sellers)
        self.satisfiable = len(self.unSellers)<1
        return
        
    def assembleProducts(self, sellers):
        for s in sellers:
            pMax = 0.0
            for n,p,q in sellers[s]:
                pMax += p*q
                if n not in self.products:
                    self.products[n] = []
                self.products[n].append(s)
                self.priceQuant[(s, n)] = (p, q)
            if pMax < self.priceMin:
                self.unSellers.append(s)    
    
    def makeName(p):
        i = p.find('#')
        return p[:i]

       
        
class Species:
    '''
        Each species instance is a potential choice of a product-->seller mapping 
            that will be evaluated and engage in reproduction with some probability.    
        Note that bit strings are stored without the python '0b' prefix that is used
            to represent base-2 numbers.
    '''
    def __init__(self, market, bstr):
        self.mutationProb = 0.001
        self.market = market
        if bstr == "":
            self.bitString = self.uniformString()
        else:
            self.bitString = bstr
        print "STR: ", self.bitString
        self.cart = self.mappingFromBits()
        self.totalPrice, self.totalSatisfaction = self.priceAndSat()
        self.fitness = self.calculateFitness()
        return
        
    def uniformString(self):
        bits = ""
        for p in self.market.products:
            #This determines what length of bit string is necessary to represent each potential seller
            numSel = len(self.market.products[p])
            bitLen = math.log(numSel,2)
            bitLen = max(1, int(bitLen) + 1*( (bitLen - int(bitLen)) > 0) )
            #We then randomly choose each bit
            for i in range(bitLen):
                bits += str(self.randomBit())
        return bits

    def randomBit(self):
        return int(random.random() < 0.5)

    def binToInt(self,bstr, intrange):
        '''
        Converts bstr, a string of zeroes and ones, into an integer
            scaled by maximum so that it is within [0,intrange].
        '''
        pf = "0b"
        allOnes =  (pf+(len(bstr)*"1")) 
        maxstr = float(eval(allOnes))
        flstr = float(eval(pf + bstr))
        fl = (flstr/maxstr)*float(intrange)
        i = int(round(fl))
        return i

    def mappingFromBits(self):
        start = 0
        mapping = {}
        for p in self.market.products:
            numSel = len(self.market.products[p])
            bitLen = math.log(numSel,2)
            bitLen = max(1, int(bitLen) + 1*( (bitLen - int(bitLen)) > 0))
            selBits = self.bitString[start:start+bitLen]
            selInt = self.binToInt(selBits, numSel)
            mapping[p] = self.market.products[p][selInt-1]
            start += bitLen
        return mapping
        
    def priceAndSat(self):
        sellerTotals = {}
        totalPrice = 0
        for product in self.cart:
            seller = self.cart[product]
            value = self.market.priceQuant[(seller,product)][0]
            totalPrice += value
            if seller not in sellerTotals:
                sellerTotals[seller] = 0
            sellerTotals[seller] += value
        totalSat = 0
        for seller in sellerTotals:
            totalSat += (sellerTotals[seller] >= self.market.priceMin)
        return totalPrice, totalSat
    
    def calculateFitness(self):
        '''
            This is the hard function. The trick is that satisfying a seller should be high
                fitness factor, becaus you need all satisfied to purchase, but beyond this
                you need to reward minimizing the price.
            This will probably have to be tuned depending on problem.
            Maybe these coefficients should be an input?
        '''           
        satCoef = 10.0
        priceCoef = 1.0
        fitness = (satCoef*self.totalSatisfaction) + (priceCoef/self.totalPrice)
        return fitness
    
    def reproduce(self, partner):
        if len(self.bitString) != len(partner.bitString):
            return None, None
        numCuts = len(self.bitString) - 1
        cut = random.randint(0,numCuts)
        child1 = ""
        child2 = ""
        for i in range(len(self.bitString)):
            if i <= numCuts:
                child1 += self.mutate(self.bitString[i])
                child2 += partner.mutate(partner.bitString[i])
            else:
                child1 += partner.mutate(partner.bitString[i])
                child2 += self.mutate(self.bitString[i])
        newSpecies1 = Species(self.market, child1)
        newSpecies2 = Species(self.market, child2)
        return newSpecies1, newSpecies2       
                
    def mutate(self, bit):
        if random.random() < self.mutationProb:
            return str(not(int(bit)))
        return bit
   
def test():
    cart = ["apples","oranges", "bananas"]
    sellers = {"alpha":[("apples", 1.1, 1),("oranges",1.5,1)], "beta":[("bananas", 2.0, 2),("oranges",1.1,1)]}
    pmin = 1.0
    mark = Market(cart,sellers,pmin)
    print " MmHmm"
    sa = Species(mark, "")
    print " Quite "
    sb = Species(mark, "")
    print " Yep "
    ca, cb = sa.reproduce(sb)
    print ca.bitString, ca.fitness
    print cb.bitString, cb.fitness
        
test()    
    
    
    
    
    
