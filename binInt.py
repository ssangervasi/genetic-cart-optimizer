def binToInt(bstr, intrange):
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
