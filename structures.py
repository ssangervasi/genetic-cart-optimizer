#www.github.com/ssangervasi/genetic-cart-optimizer
#(c) 2014 Sebastian Sangervasi
#
#

import random
import math

class Market:

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
        self.r=priceQuant = {}
        self.unSellers = []
        self.unProducts = []
        
        self.assembleProducts(sellers)
        
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
                if pMax < priceMin:
                    self.unSellers.append(s)    
        
        def makeName(p):
            i = p.find('#')
            return p[:i]

       
        
class Species:

    def __init__(self, market):
        self.market = market
        self.bitString = self.uniformString()
        return
        
    def uniformString(self):
        bits = ""
        for p in market.products:
            numSel = len(market.products[p])
            bitLen = math.log(numSel),2
            bitLen = int(bitLen) + 1*( (bitLen - int(bitLen)) > 0)
            for i in range():
                bits += str(randomBit())
        return ""


def binToInt(bstr, intrange):
    '''
    Converts bstr, a string of zeroes and ones, into an integer
        scaled by maximum string of that length to be within [0,intrange].
    '''
    pf = '0b'
    maxstr = float(eval(pf+ len(bstr)*'1'))
    flstr = float(eval(pf + bstr))
    fl = (flstr/maxstr)*float(intrange)
    i = int(round(fl))
    return i
        
    
def randomBit():
    return int(random.random() < 0.5)
    
'''    
def test():
    ir = 10
    for i in range(16):
        bs = bin(16+i)[3:]
        #print bs
        print binToInt(bs, ir)
        
test()    
''' 
    
    
    
    
    
