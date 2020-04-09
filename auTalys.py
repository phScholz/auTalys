from subprocess import Popen, PIPE, STDOUT
from argparse import ArgumentParser
import numpy as np
import os
import sys
from multiprocessing import Process
import progressbar

import jsonTalysInput
#import createTalysJson
#import plotRPFiles

class auTalys():

    def __init__(self, tDir="/data/pscholz/programs/talys1.9/talys/talys",working="./.temp",output="./output"):
        self.max_procs=30
        self.talys=tDir
        self.oDir=output
        self.wDir=working
        self.RPFiles=[]

    def deltree(self,target):
        for d in os.listdir(target):
            try:
                self.deltree(target + '/' + d)
            except OSError:
                os.remove(target + '/' + d)

        os.rmdir(target)

    def copyRPFiles(self,workingDir, outputDir, name):
        f = []
        cwd=os.getcwd()
        os.chdir(outputDir)
        rpDir="rp"+name

        if os.path.isdir(rpDir):
            deltree(rpDir)
            os.mkdir(rpDir)
            os.chdir(rpDir)
        else:
            os.mkdir(rpDir)
            os.chdir(rpDir)

        rpDir=os.getcwd()
        os.chdir(cwd)    

        for dirpath, dirnames, filenames in os.walk(workingDir):
            for file in filenames:
                if "rp" in file:                
                    f.append(file)

        for file in f:
            rp = open(os.path.join(workingDir,file), "r")
            data=rp.read()
            rp.close()
            rp = open(os.path.join(rpDir,file+"."+name),"w")
            rp.write(data)
            rp.close()
    
    def copyRateFiles(self,workingDir, outputDir, name):
        f = []
        cwd=os.getcwd()
        os.chdir(outputDir)
        rpDir="astro"+name

        if os.path.isdir(rpDir):
            deltree(rpDir)
            os.mkdir(rpDir)
            os.chdir(rpDir)
        else:
            os.mkdir(rpDir)
            os.chdir(rpDir)

        rpDir=os.getcwd()
        os.chdir(cwd)    

        for dirpath, dirnames, filenames in os.walk(workingDir):
            for file in filenames:
                if "astro" in file:                
                    f.append(file)

        for file in f:
            rp = open(os.path.join(workingDir,file), "r")
            data=rp.read()
            rp.close()
            rp = open(os.path.join(rpDir,file+"."+name),"w")
            rp.write(data)
            rp.close()

    def writeOutputFiles(self,name,outputdir,cwd, stdout):
        os.chdir(outputdir)    
        f = open(name + ".out", "w")
        f.write(stdout)
        f.close()
        os.chdir(cwd)

    def prepareOutputDir(self,outputDir,cwd):
        if os.path.isdir(outputDir):
            self.deltree(outputDir)
            os.mkdir(outputDir)
        else:
            os.mkdir(outputDir)

    def prepareWorkingDir(self,workingDir,cwd):
        if os.path.isdir(workingDir):
            self.deltree(workingDir)
            os.mkdir(workingDir)
        else:
            os.mkdir(workingDir)

    def callTalys(self, StdIn, TalysInput, name):
        #print(StdIn)
        workingDir=self.wDir+name
        outputDir=self.oDir
        talysPath=self.talys
        

        #store current-working-directory path
        cwd = os.getcwd()

        self.prepareWorkingDir(workingDir,cwd)

        os.chdir(workingDir)

        #open talys subprocess with Stdin
        #STDOUT is stored in stdout_data
        dummyProcess = Popen([talysPath], stdout=PIPE, stdin=PIPE, stderr=PIPE)
        dummyOut = dummyProcess.communicate(input=StdIn)[0]

        while dummyProcess.poll() == None:
            dummyProcess.wait()

        #change directory to former working directory
        os.chdir(cwd)  

        self.copyRPFiles(workingDir,outputDir,name)
        self.copyRateFiles(workingDir,outputDir,name)

        self.writeOutputFiles(name,outputDir,cwd,dummyOut)

        #change directory to former working directory
        os.chdir(cwd)

        #remove temporary directories
        self.deltree(workingDir)

        #return STDOUT of talys
        return 1

    def handleInput(self,input):
        print("Reading input file: "+ input + "\n")
        data = jsonTalysInput.TalysJson()
        data.JsonToTalysInputList(input)        
        return data.StdInList, data.TalysInputList

    def start(self,jsonFile, max_procs=30):
        stdInList, TalysInputList=self.handleInput(jsonFile)

        if "astro y" in str(stdInList):
            print("Calculation of reaction rates detected.")

        stdOutList = []
        procs = []

        if len(stdInList) < max_procs:
            max_procs = len(stdInList)
    
        print("Preparing output directory!\n")
        self.prepareOutputDir(self.oDir,os.getcwd())

        print("\nStarting " + str(len(stdInList))+" TALYS calculations using " + str(max_procs) + " processes at once.\n")
        finished=0
        active = 0
        with progressbar.ProgressBar(max_value=len(stdInList)) as bar:
            bar.update(finished)
            for i in range(len(stdInList)):
                if active == max_procs:
                    for proc in procs:
                        proc.join()
                    finished=finished+max_procs
                    bar.update(finished)
                    active=active-max_procs                

                if active < max_procs:
                    #print(str(i).zfill(6),stdInList[i])
                    proc = Process(target=self.callTalys, args=(stdInList[i],TalysInputList[i],str(i).zfill(6)))
                    procs.append(proc)
                    proc.start()
                    active=active+1          
    
if __name__ == '__main__':
    print("\nauTalys.py - auTalys toolkit - (c)2019-2020 Philipp Scholz")
    print("**************************************************************") 
    parser=ArgumentParser()
    parser.add_argument("jsonFile",type=str,help="JSON Talys input file")
    parser.add_argument("-o","--outputDir",type=str, nargs='?',help="path to output directory", default="./output")
    parser.add_argument("-t","--talys",type=str, nargs="?", help="path to talys", default="/data/pscholz/programs/talys1.9/talys/talys")
    #parser.add_argument("-r", "--reactionRate", action="store_true", help="Additionally calculates reaction rates")
    #parser.add_argument("-rp", "--copyRPfiles", action="store_true", help="Stores reaction product files in output directory")
    args=parser.parse_args()
    #if args.reactionRate:
    #    print("Additional reaction rate calculation turned on!")
    #if args.copyRPfiles:
    #    print("Copying of RP-Files turned on!")
    a=auTalys(output=args.outputDir)
    a.start(args.jsonFile)

