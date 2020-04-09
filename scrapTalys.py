#!/bin/python
from argparse import ArgumentParser
import numpy as np

def getUserInput(file):
    start = 'USER INPUT FILE'
    end = 'USER INPUT FILE + DEFAULTS'
    ListOfLines = []
    file_handler = open(file)
    started = False
    for line in file_handler:
        if start in line:
            started = True
        if end in line:
            #print("Ended")
            started = False       
        if started and len(line)>1:
            ListOfLines.append(line.strip())

    del ListOfLines[0]

    file_handler.close()
    return ListOfLines

def getIncidentEnergies(file):
    start = 'incident energies (LAB):'
    end = ' Q-values for binary reactions:'
    ListOfLines = []
    file_handler = open(file)
    started = False
    for line in file_handler:
        if start in line:
            started = True
        if end in line:
            #print("Ended")
            started = False       
        if started and len(line)>1:
            ListOfLines.append(line.strip())

    del ListOfLines[0]

    file_handler.close()
    return ListOfLines

def getBinaryCrossSection_Channel(file, channel):
    pass

def getResultsForEnergy(file,energy):
    start=""
    end=""
    started = False
    ListOfLines = []
    file_handler = open(file)


    if float(energy) > 10:
        start = '########## RESULTS FOR E=  '+energy
    else:
        start = '########## RESULTS FOR E=   '+energy
    
    if float(energy) > 10:
        end = '########## REACTION SUMMARY FOR E=  '+energy
    else:
        end = '########## REACTION SUMMARY FOR E=   '+energy
    
    for line in file_handler:
        if start in line:
            started = True
        if end in line:
            print("Ended")
            started = False       
        if started and len(line)>1:
            ListOfLines.append(line.strip())            

    #del ListOfLines[0]

    file_handler.close()
    return ListOfLines

def getReactionSummaryForEnergy(file,eStart, step, eEnd):
    start=""
    end=""
    started = False
    ListOfLines = []
    file_handler = open(file)

    if float(eStart) >= 10:
        start = '########## REACTION SUMMARY FOR E=  '+eStart
    else:
        start = '########## REACTION SUMMARY FOR E=   '+eStart


    if float(eStart)+step >= 10:
        end = '########## RESULTS FOR E=  '+str(float(eStart)+step)
    else:
        end = '########## RESULTS FOR E=   '+str(float(eStart)+step)

    if float(eStart) == float(eEnd):
        end = '########## EXCITATION FUNCTIONS ###########'
    
    for line in file_handler:
        if start in line:
            started = True
        if end in line:
            #print("Ended")
            started = False       
        if started and len(line)>1:
            ListOfLines.append(line.strip())            

    #del ListOfLines[0]

    file_handler.close()
    return ListOfLines

def ReactionSummary(file):
    ReactionSummary = []
    IncidentEnergies=getIncidentEnergies(file)
    eEnd = IncidentEnergies[-1].replace(' ', '')
    eStep = float(IncidentEnergies[1].replace(' ', ''))-float(IncidentEnergies[0].replace(' ', ''))
    #print(eStep)
    for i in range(len(IncidentEnergies)):                            
            ReactionSummary.append(getReactionSummaryForEnergy(args.TalysOutputFile, IncidentEnergies[i].replace(' ', ''), eStep, eEnd)) 
    return ReactionSummary

def ResultsForEnergies(file):
    ResultsForEnergies = []
    IncidentEnergies=getIncidentEnergies(file)        
    for i in range(len(IncidentEnergies)):                    
        ResultsForEnergies.append(getResultsForEnergy(args.TalysOutputFile, IncidentEnergies[i].replace(' ', '')))
    
    return ResultsForEnergies 

def xsPerMass(SummaryLines):
    start = 'b. Per mass'
    end = 'Total residual production'
    ListOfLines = []
    started = False
    for line in SummaryLines:
        if start in line:
            started = True
        if end in line:
            #print("Ended")
            started = False       
        if started and len(line)>1:
            ListOfLines.append(line.strip())

    del ListOfLines[0]
    return ListOfLines

def xsPerIsotope(SummaryLines):
    start = 'a. Per isotope'
    end = 'b. Per mass'
    ListOfLines = []
    started = False
    for line in SummaryLines:
        if start in line:
            started = True
        if end in line:
            #print("Ended")
            started = False       
        if started and len(line)>1:
            ListOfLines.append(line.strip())

    del ListOfLines[0]
    del ListOfLines[1]
    return ListOfLines

def scrapPopulationGamma(file):
    start="after binary gamma"
    end1 ="after binary neutron"
    end2 ="after binary proton"
    end3 ="after binary alpha"
    ListOfLines = []
    file_handler = open(file)
    started = False
    for line in file_handler:
        if start in line:
            started = True
        if end1 in line or end2 in line or end3 in line:
            started = False
        if started and len(line)>1:
            ListOfLines.append(line.strip())
    
    emission=ListOfLines[0][-11:].strip()
    excitationEnergy=ListOfLines[1][26:34].strip()
    discreteLevels=ListOfLines[1][51:54].strip()

    del ListOfLines[0]
    del ListOfLines[0]
    del ListOfLines[0]

    file_handler.close()
    return emission, excitationEnergy, discreteLevels, ListOfLines 


if __name__ == '__main__':
    #print("\nscrapTalys.py - auTalys toolkit - (c)2019 Philipp Scholz")
    #print("**************************************************************\n") 
    parser=ArgumentParser()
    parser.add_argument("TalysOutputFile",type=str,help="TalysOutputFile")
    parser.add_argument("-ui", "--UserInput", action="store_true", help="Get USER INPUT for calculation")
    parser.add_argument("-e", "--IncidentEnergies", action="store_true", help="Get INCIDENT ENERGIES for calculation")
    parser.add_argument("-rfe", "--ResultsForEnergies", action="store_true", help="Get RESULTS FOR ENERGIES for calculation")
    parser.add_argument("-rse", "--ReactionSummary", action="store_true", help="Get REACTION SUMMARY FOR ENERGIES for calculation")
    parser.add_argument("-bcs", "--binaryXS", action="store_true", help="Get BINARY CROSSSECTIONS FOR ENERGIES for calculation [Doesnt work yet]")
    parser.add_argument("-popG", "--populationGamma", action="store_true", help="Get Population after primary gamma")
    parser.add_argument("-CF", "--compoundFormation", action="store_true", help="Get compound formation cross section after primary gamma [Doesnt work yet]")
    
    args=parser.parse_args()
    
    if args.UserInput:
        userInput=getUserInput(args.TalysOutputFile)
        #print('USER INPUT FILE')
        for line in userInput[:]:
            print(line)    

        print("")

    if args.IncidentEnergies:
        IncidentEnergies=getIncidentEnergies(args.TalysOutputFile)
        for line in IncidentEnergies[:]:
            print(line)
        print("")
    
    if args.ResultsForEnergies:
        ResultsForEnergies = ResultsForEnergies(args.TalysOutputFile)

        for result in ResultsForEnergies:
            for line in result:
                print(line)
            print("\n\n")
    
    if args.ReactionSummary:
        ReactionSummary=ReactionSummary(args.TalysOutputFile)

        for summary in ReactionSummary:
            for line in summary:
                print(line)
            print("")

    if args.binaryXS:
        
        pass

    if args.populationGamma:
        em, exE, dL, popG=scrapPopulationGamma(args.TalysOutputFile)
        print("#Emission: "+em)
        print("#Excitation Energy: "+exE)
        print("#Discrete Levels: "+dL)
        print("#E_g\tE_L\tpopXS\tIntensity")

        data=np.loadtxt(popG[:int(dL)+1])

        for line in data:
            print("%2.3f\t%2.3f\t%2.2e\t%02.2e" % (float(exE)-line[1],line[1],line[2],line[2]/float(em)))