import json
from operator import itemgetter
import copy
from pathlib import Path
import os

def getSolution(reqs, combs):
    needs = copy.deepcopy(reqs)
    res = []
    res.append([])
    for comb in combs:
        #As long as all items from comb[x] fulfill need
        combNeed = True
        while combNeed:
            #Check if comb[x] provides more than need (fail fast)
            for need in needs:
                if comb[need['Length']] > need['Qty']:
                    combNeed = False
            if not combNeed:
                break

            for need in needs:
                need['Qty'] -= comb[need['Length']]
            
            #Append result
            res[0].append(comb.copy())
    
    #Calculate total price
    for sol in res:
        price = round(sum(x['Price'] for x in sol),2)
    
    res.append([price])

    #Return result
    return res

def getCutLists(inputstr = "", outputstr = ""):
    if inputstr:
        jsonlocation = inputstr
    else:
        jsonlocation = './input/input.json' #default input location
    print(jsonlocation)
    errstr = ""

    #Get input
    try:
        with open(jsonlocation) as f:
            data = json.load(f)
    except:
        errstr += "JSON file not found. "
        return(f"Err: {errstr}")
    
    #Get variables from JSON object
    try:
        reqs = data['Required Lengths']
    except:
        errstr += "'Required Lengths' not found. "
        
    try:
        avail = data['Available base material']
    except:
        errstr += "'Available base material' not found. "
    
    try:
        cutwidth = data['Cut loss']
    except:
        errstr += "'Cut loss' not found. "
        
    if errstr:
        return(f"Err: {errstr}")
    
    #Test for required keys in array
    try:
        test = [x['Length'] for x in reqs]
        if min(test) <= 0:
            errstr += f"Err: Required length ({min(test)}) must be bigger than 0."
    except:
        errstr += "'Length' not found in required lengths. "

    try:
        test = [x['Qty'] for x in reqs]
        if min(test) <= 0:
            errstr += f"Err: Required quantity ({min(test)}) must be bigger than 0."
    except:
        errstr += "'Qty' not found in required lengths. "
        
    try:
        test = [x['Length'] for x in avail]
        if min(test) <= 0:
            errstr += f"Err: Available length ({min(test)}) must be bigger than 0."
    except:
        errstr += "'Length' not found in available base material. "
    
    try:
        test = [x['Price'] for x in avail]
        if min(test) < 0:
            errstr += f"Err: Available price ({min(test)}) can't be negative."
    except:
        errstr += "'Price' not found in available base material. "
        
    if errstr:
        return(f"Err: {errstr}")

    
    #Init other vars
    listreq = [x['Length'] for x in reqs]
    listavail = [x['Length'] for x in avail]
    minreq = min(listreq)
    res=[]

    #Error handling on passed inputs
    if max(listreq) > max(listavail):
        return(f"Err: Unable to process, required length of {max(listreq)} is bigger than longest available base material with length of {max(listavail)}.")
    
    if cutwidth < 0:
        return(f"Err: Cut width can't be negative")

    #Make list of all available cut combinations
    combs = []
    for plank in avail:
        myplank = plank.copy()
        for cut in reqs:
            myplank[cut['Length']] = 0

        #Increase first required plank length
        myplank[reqs[0]['Length']] += 1

        #Set other variables
        myplank['Unitprice'] = myplank['Price'] / myplank['Length']

        filling = True
        while filling:
            #Calculate rest length
            myplank['Rest'] = myplank['Length']
            for i in reqs:
                length = i['Length']
                myplank['Rest'] -= ((myplank[length] * length) + (myplank[length] * cutwidth))
            myplank['Rest'] += cutwidth
            
            #Set rest of variables
            myplank['Baseprice'] = (myplank['Price']) / ((myplank['Length'] - myplank['Rest']))
            myplank['Optimal'] = (myplank['Rest'] <= minreq)
            

            #Check if rest length is positive
            if myplank['Rest'] >= 0:
                combs.append(myplank.copy())
                myplank[reqs[0]['Length']] += 1
            else:
                for i in range(len(reqs)):
                    if myplank[reqs[i]['Length']] > 0:
                        myplank[reqs[i]['Length']] = 0
                        if i < len(reqs)-1:
                            myplank[reqs[i+1]['Length']] += 1
                            break
                        else:
                            filling = False

    #Sort combinations descending by remaining length, get solution
    combs = sorted(combs, key=lambda k: k['Rest'])
    res.append(getSolution(reqs, combs))

    #Sort combinations by getting biggest lengths first (largest to smallest), optimal pieces first, get solution
    listreq = sorted(listreq, reverse=True)
    listreq.insert(0,'Optimal')
    for x in reversed(listreq):
        combs.sort(key=itemgetter(x), reverse=True)
    res.append(getSolution(reqs, combs))

    #Sort combination by least effective price per unit, get solution
    combs = sorted(combs, key=lambda k: k['Baseprice'])
    res.append(getSolution(reqs, combs))

    #Get cheapest option & make readable format
    cheapest = min([x[1] for x in res])
    for x in res:
        if x[1] == cheapest:
            sol = {}
            sol['Required base material'] = {}
            sol['Cut list'] = []
            i = 1
            for plank in x[0]:
                if plank['Length'] not in sol['Required base material']:
                    sol['Required base material'][plank['Length']] = 0
                sol['Required base material'][plank['Length']] += 1
                str = f"Plank {i}: Length {plank['Length']}, "
                for req in reqs:
                    if plank[req['Length']] > 0: str += f"{plank[req['Length']]}x {req['Length']}, "
                str += f"rest: {plank['Rest']}"
                sol['Cut list'].append(str)
                i += 1
            
            sol['Total price'] = cheapest
            break

    #Get output location
    if outputstr:
        outputfile = outputstr
        if outputfile[len(outputfile)-1] != "//":
            outputfile += "//"
        outputfile += "cutlist_result.json"
    else:
        outputfile = "./output/cutlist_result.json"
        
    #Make directories
    Path(os.path.dirname(outputfile)).mkdir(parents=True, exist_ok=True)

    #Output to file
    f = open(outputfile, "w")
    json.dump(sol, f, indent=4)
    f.close

    return("Success")