#www.github.com/ssangervasi/genetic-cart-optimizer
#(c) 2014 Sebastian Sangervasi
#
#

import random

def makeCart(numItems = 30):
    items = []
    for i in range(numItems):
        items.append("Item_"+str(i+1))
    return items
    
def makeSellers(cart=None, priceList = None, sellerList = None, pAv = 0.50, pVar = 0.25, pMin = 1.0, satisfiable = True):
    if cart == None:
        cart = makeCart()
        numItems = 30
    else:
        numItems = len(cart)        
    if priceList == None:
        priceList = [pAv]*numItems
    if sellerList == None:
        sellerList = ["Seller_"+str(i+1) for i in range(50)]
        numSellers = 50
    else:
        numSellers = len(sellerList)
    
    sellers = {}
    for seller in sellerList:
        inventSize = random.randint(1, numItems)
        inventDict = {}
        sellers[seller] = []
        added = 0
        for i in range(inventSize):
            item = random.choice(cart)
            sellerPrice = 0.0
            if not item in inventDict:
                inventDict[item] = added
                added += 1
                if satisfiable and sellerPrice < pMin and i== inventSize - 1:
                    price = pMin - sellerPrice
                else:    
                    price  = pAv + 2*(random.random()-0.5)*pVar*pAv
                sellerPrice += price
                sellers[seller].append( (item, price, 1) )
            else:
                tupAsList = list( sellers[seller][inventDict[item]])
                tupAsList[2] += 1   #Increase quantity
                if satisfiable and sellerPrice < pMin and i== inventSize - 1:
                    #price = (pMin - sellerPrice)/tupAsList[2] #Does not satisfy when quantity is ignored.
                    price = pMin - sellerPrice
                    sellerPrice += pMin
                    tupAsList[1] = price
                sellerPrice += tupAsList[1] #Increase total price
                sellers[seller][inventDict[item]] = tuple(tupAsList)
    #For now I'm not worrying about solvability, but it should be encorperated.
    return sellers
    
def dataStore(cart, sellers, fileName):
    path = fileName[0:fileName.find(".")]
    realName = path+".py"
    f = open(realName, 'w')
    f.write("#This is a data file for genetic-cart-optimizer\n\n")
    f.write("Cart = "+str(cart)+"\n")
    f.write("Sellers = "+ str(sellers) + "\n")
    f.close()
    return True
    
def makeData(fileName = None):
    cart = makeCart()
    sellers = makeSellers()
    if fileName == None:
        return cart, sellers
    dataStore(cart, sellers, fileName)
    return cart, sellers
    
    
    
makeData(fileName = "April30.py")




    
    
        
    
    
