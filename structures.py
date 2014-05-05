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
            sellers:    A dictionary of seller names mapping to a list of (product name, price, quantity) tuples indicating the seller's inventory.
            priceMin:   Universal minimum price. Implementation may allow this to become seller-dependent.
            
            Output:     None, this is an initilizer.

            Note: Items are currently assumed to be unique, i.e. the quantity element of each seller is ignored. An implementation that generalizes for non-unique quantities may come later.
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
        #print "STR: ", self.bitString
        self.cart = self.mappingFromBits()
        self.totalPrice, self.totalSatisfaction = self.priceAndSat()
        self.fitness = -1
        return

    def sortKey(self):
        #Function for sorting. Seemed to be best done by fitness, might use satisfaction instead.
        return self.fitness
        
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
        '''
            Price is total price of items based on chosen sellers.
            Satisfaction is the fraction of sellers used that met minimum price requirement.
        '''
        sellerTotals = {}
        totalPrice = 0
        totalNumSellers = 0
        for product in self.cart:
            seller = self.cart[product]
            value = self.market.priceQuant[(seller,product)][0]
            totalPrice += value
            if seller not in sellerTotals:
                sellerTotals[seller] = 0
                totalNumSellers += 1
            sellerTotals[seller] += value
        totalSat = 0
        for seller in sellerTotals:
            totalSat += (sellerTotals[seller] >= self.market.priceMin)
        return totalPrice, (float(totalSat)/totalNumSellers)
    
    def calculateFitness(self, satCoef, priceCoef, lowestPrice):
        '''
            This is the hard function. The trick is that satisfying a seller should be high
                fitness factor, becaus you need all satisfied to purchase, but beyond this
                you need to reward minimizing the price.
            This will probably have to be tuned depending on problem.
            Maybe these coefficients should be an input?
            
            Update April 29: yes, the coefficients are now an input passed into this function
        '''           
        fitness = (satCoef*self.totalSatisfaction) + priceCoef*(lowestPrice/self.totalPrice)
        self.fitness = fitness
        return
    
    def reproduce(self, partner, cross = False):
        if len(self.bitString) != len(partner.bitString):
            return None, None
        numCuts = len(self.bitString) - 1
        cut = random.randint(0,numCuts)
        child1 = ""
        child2 = ""
        for i in range(len(self.bitString)):
            if i <= numCuts or (not cross):
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
            return str(int(not(int(bit))))     #Check out that logic mmhmm
        return bit
   
   
class Population:
    def __init__(self, popSize):
        self.species = []
        self.lowestPrice = float('inf')
        self.popSize = popSize
        self.satCoef = 10.0
        self.priceCoef = 1.0
        self.crossProb = 0.3
        return

    
    def initializeRandom(self, market):
        for i in range(self.popSize):
            self.species.append(Species(market, ''))
            specPrice = self.species[-1].totalPrice
            if specPrice < self.lowestPrice:
                self.lowestPrice = specPrice
        return

    def addSpecies(self, species):
        self.species.append(species)
        specPrice = self.species[-1].totalPrice
        if specPrice < self.lowestPrice:
            self.lowestPrice = specPrice
        return
            
    def populationFeatures(self, echo = False):
        totalPrice = 0
        totalSat = 0
        totalFit = 0
        if echo:
            print("Species\tPrice\tSatisfaction\tFitness")
        avPrice = 0
        avSat = 0
        r = 2
        for s in range(len(self.species)):
            totalPrice += round(self.species[s].totalPrice,r)
            totalSat += round(self.species[s].totalSatisfaction,r)
            totalFit += round(self.species[s].fitness,r)
            if echo:
                print(str(s)+"\t$"+str(round(self.species[s].totalPrice,r))+"\t"+str(round(self.species[s].totalSatisfaction,r))+"\t"+str(round(self.species[s].fitness,r)))
        avPrice = round(float(totalPrice)/len(self.species),r)
        avSat = round(float(totalSat)/len(self.species),r)
        avFit = round(float(totalFit)/len(self.species), r)
        if echo:
            print("\nAverage\t" + str(avPrice) + "\t" + str(avSat) + "\t" + str(avFit))
        return avPrice, avSat, avFit

    
    def newGeneration(self):
        '''
            Used to produce a new population object from the currrent population.
            Calls several helper functions to generate the probability of each species reproducing,
            then generates a dictionary of upper bounds for choosing a species from a random number
            that is uniform in [0,1].
            Note that, from the Species class, each reproduction produces two offspring, so to
            get a new generation of equal size there must be popSize/2 reproductions.
        
        '''
        reproProb = self.probFromFitness() #Map of fitness probabilities to list of species with that prob
        probMap = self.probBounds(reproProb)
        newGen = Population(self.popSize)
        
        #print probMap
        for romanticEncounter in range(int(self.popSize/2)+(self.popSize%2)):
            romeo = self.itemFromProb(probMap)
            juliette = self.itemFromProb(probMap)
            crossGenes = random.random()<self.crossProb
            kidA, kidB = romeo.reproduce(juliette, cross = crossGenes)
            newGen.addSpecies(kidA)
            newGen.addSpecies(kidB)
        return newGen
                
    def itemFromProb(self,boundMap):
        chance = random.random()
        toIter = list(boundMap.keys()) #need to ensure this works in python 2 and 3 equally well
        toIter.sort()
        item = None
        for edge in toIter:
            if chance <= edge:
                item = boundMap[edge]
                break
        return item

        
    def probFromFitness(self):
        fitnessMap = {}
#        fitnessOrder = []
        totalFitness = 0
        for s in self.species:
            s.calculateFitness(self.satCoef, self.priceCoef, self.lowestPrice)
            if not s.fitness in fitnessMap:
                fitnessMap[s.fitness] = []
                #fitnessOrder.append(s.fitness)
            fitnessMap[s.fitness].append(s)
            totalFitness += s.fitness
#        fitnessOrder.sort(reverse=True)
        normFitnessMap = {}
        for f in fitnessMap:
            normFitnessMap[float(f)/totalFitness] = fitnessMap[f]
        return normFitnessMap

    def probBounds(self, reproProb):
        '''
            Takes a dictionary of {probability:[species1, ...]} and returns a dictionary of
            cummulative probability marks mapping to single species, {probabilityBound:species}
        '''
        bounds = {}
        runningSum = 0
        for prob in reproProb:
            for species in reproProb[prob]:
                runningSum += prob
                bounds[runningSum] = species
        #if int(runningSum) != 1:
        #    print "Probability error" #putting this in as a test for now
        #    print "\t", runningSum, int(runningSum)
        #That test turned out to be bad because of roundoff errors breaking equality
        return bounds

    def sortByFitness(self):
        self.species = sorted(self.species, key = Species.sortKey, reverse = True)
        return

    def writeToFile(self, fileName):
        f = open(fileName+".txt", 'w')
        f.write("#Population Output File\n")
        f.write("Price\tSatisfaction\tFitness\tBitString\tSellers\n")
        self.newGeneration()
        self.sortByFitness()
        for spec in self.species:
            f.write(str(spec.totalPrice)+"\t"+str(spec.totalSatisfaction)+"\t"+str(spec.fitness)+"\t"+str(spec.bitString)+"\t"+str(spec.cart)+"\n")
        f.close()
        return fileName+".txt"
