import json

class TalysInput:

    def __init__(self):        
        self.Input ={}
        self.InputString = ""

    def fromJson(self, json):
        self.Input = json
        return 1
    
    def fromString(self, string):
        #create TalysInput object from string
        pass

    def toString(self):
        string=""
        for key, var in self.Input.items():
            string += key + " " + var +"\n"

        return string    

class TalysJson:
    
    def __init__(self):
        #List for TalysInput-objects
        self.TalysInputList=[]
        #List for Talys-Stdin strings
        self.StdInList=[]

    def readJsonInput(self, jsonFile):
        #read a Jsonfile and store input parameters in TalysJson class attributes
        
        #store total content of jsonFile in jsonData
        jsonData = json.load(open(jsonFile))        
        #dummy for TalysInput
        dummy = TalysInput()
        
        #for each input in json-File store input in dummy and push it to InputList
        for part in jsonData:
            dummy.fromJson(part)
            self.TalysInputList.append(dummy)
            self.StdInList.append(dummy.toString())
    
    def JsonToTalysInputList(self, jsonFile):
        self.readJsonInput(jsonFile)
