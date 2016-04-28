
'''
***EDIT THIS LIST WITH THE COL NAMES FROM ***'''
chosenKeys = ['csvCol1', 'csvCol2']
keys = ['Date','Name'] + chosenKeys
'''
***CSV INPUT FILE PATH***'''
FileName = "C:\Users\James\Documents\Top11\Small Example.csv" 

'''
***JSON OUTPUT FILE PATH***'''    
outPutFile = 'C:\Users\James\Documents\Top11\Small.json'


def getYear(x):
    '''returns year from 'Date' value'''
    return x['Date'][-4:]

def getMonth(x):
   '''returns month from 'Date' value for formatting as two characters'''
   
   firstSlash = x['Date'].index("/")
   
   if len(x['Date'][:firstSlash]) < 2:
       month = '0' + x['Date'][:1]
       return month
   else:
       month = x['Date'][:2]
       return  month

    
def getDay(x):
    '''returns day from 'Date' value as two characters'''  
    firstSlash = x['Date'].index("/")
    if len(x['Date'][firstSlash+1:-5]) == 1:
       return '0' + x['Date'][firstSlash+1:-5]
    else:
       return x['Date'][firstSlash+1:-5]


def get_key_pos(FileName, keys):
    import csv
    '''gets position of the keys in key list and the position of 'Name', in the header document. Returned as a Tuple'''
    reader = csv.reader(open(FileName))    
    count = 0
    for row in reader:
        if count <1:
            keyPosList =[]
            for k in keys:
                keyPosList += [row.index(k)]
            nameIndex = row.index("Name")
                
        count+=1
    return (keyPosList, nameIndex)
  

 

def Pre_Result_List_Creator(FileName, key_Pos, keys):
    import csv
    """takes each row from the csv as a dictionary and puts all the dictionaries in a list of dicts"""
    #rowKeyCount = 0
    preResultDict = {}
    
    reader = csv.reader(open(FileName))
    
    for row in reader:
        itDict = {}
        count = 0
        for key in keys:
            Key_Pos_in_Row = key_Pos[0][count]
            count +=1
            itDict[key] = row[Key_Pos_in_Row]
        itDict.pop("Name")
        Name = row[key_Pos[1]]
        
        if Name <> "Name" and Name not in preResultDict:
            preResultDict[Name] = [itDict]
        elif Name <> "Name" and Name in preResultDict:
            preResultDict[Name] += [itDict]
    return preResultDict
            
        

    

def result_list_date_formatted(preResultDict):
    """returns list of dictionaries with each requested field with dates formatted""" 
    resultDict ={}
    for Name in preResultDict:
       for dicti in preResultDict[Name]:
            Year = getYear(dicti)
            Month = getMonth(dicti)
            Day = getDay(dicti)
            dicti['Date'] = Year + '/' + Month + '/' + Day
            if  Name not in resultDict:
                resultDict[Name] = [dicti]
            elif Name in resultDict:
                resultDict[Name] += [dicti]
            
        
    return resultDict



def Key_Date_Value_Dict_Creator(Name,resultDict):
    '''Returns List of small Lists of [date,value] pairings by key name'''
    dateValueDict = {}
    for dicti in resultDict[Name]:
        #print dicti
        for key in dicti:
              if key <> 'Date' and key in dateValueDict:
                  dateValueDict[key] += [[dicti['Date'], float(dicti[key])]]
              elif key <> 'Date' and key not in dateValueDict:
                  dateValueDict[key] = [[dicti['Date'], float(dicti[key])]]
    for key in dateValueDict:
        dateValueDict[key] = sorted(dateValueDict[key])      
    return dateValueDict
       
       
 
def writeToFile(outPutFile,resultDict, keys):
    '''Writes the contents of resultDict to a Json file'''
    target = open(outPutFile, 'a')
    target.write("[")
    nameCount = 0
    for Name in resultDict:
        dateValueDict = Key_Date_Value_Dict_Creator(Name,resultDict)
        target.write("{")
        target.write('"Name": ' + '"'+Name +'",')
        target.write("\n")
        keyCount = 0
        for key in dateValueDict:
            if keyCount == len(dateValueDict)-1:
                    target.write('"' + key+ '"'  + ':'  + str(dateValueDict[key]).replace("'",'"'))
                    target.write("\n")
            else:
                target.write( '"' + key+ '"'  + ':' + str(dateValueDict[key]).replace("'",'"')+',')
                target.write("\n")
            keyCount += 1
                
        nameCount +=1
        if nameCount == len(resultDict):
                
            target.write("}")
        else:
                
            target.write("},")
    target.write("]") 
    target.close()



import sys
def main():
    """Main entry point for the script."""
    
    key_Pos = get_key_pos(FileName, keys)
    preResultDict =  Pre_Result_List_Creator(FileName, key_Pos, keys)
    resultDict = result_list_date_formatted(preResultDict)
    writeToFile(outPutFile,resultDict, keys)
    print "Completed"




if __name__ == '__main__':
    sys.exit(main())