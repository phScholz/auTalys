import json
import sys
import os
from argparse import ArgumentParser

class createTalysJson():
    def single(self, mass, element, projectile):
        InputList = []
        dic={
                "energy":       "2 12.0 0.5",
                "projectile":   projectile,
                "transeps":     "1e-30",
                "xseps ":       "1e-30",
                "popeps":       "1e-30",
                "element":      element,
                "mass":         mass,
                "outbasic":     "y",                
        }
        ID=0
        for alphaomp in [2,3,4,5,6]:
            for strength in [1,2,6,8]:
                for ldmodel in [1,4,5,6]:
                    for jlmomp in ["n","y"]:
                        if jlmomp == "y":
                            for jlmmode in [0,1,2]:
                                dummyDic = dic.copy()
                                dummyDic["#InputID"]=str(ID).zfill(6)                                
                                dummyDic["mass"] = str(mass)
                                dummyDic["element"] = str(element)
                                dummyDic["alphaomp"] = str(alphaomp)
                                dummyDic["strength"] = str(strength)
                                dummyDic["ldmodel"] = str(ldmodel)
                                dummyDic["jlmomp"] = jlmomp;
                                dummyDic["jlmmode"] = str(jlmmode)
                                InputList.append(dummyDic)
                                ID=ID+1
                        else:
                                dummyDic = dic.copy()
                                dummyDic["#InputID"]=str(ID).zfill(6)
                                dummyDic["mass"] = str(mass)
                                dummyDic["element"] = str(element)
                                dummyDic["alphaomp"] = str(alphaomp)
                                dummyDic["strength"] = str(strength)
                                dummyDic["ldmodel"] = str(ldmodel)                                                               
                                InputList.append(dummyDic)
                                ID=ID+1
                            

        f = open(mass+element+"_"+projectile+".json", "w")
        f.write(json.dumps(InputList, indent=4))
        f.close()
        print("\nInput has been written to '"+mass+element+"_"+projectile+".json"+"'")

if __name__ == '__main__':
    print("\ncreateTalysJson.py - auTalys toolkit - (c)2019 Philipp Scholz")
    print("**************************************************************")
    parser=ArgumentParser()
    parser.add_argument("mass",type=str,help="Mass of the target")
    parser.add_argument("element",type=str,help="Z of the target")
    parser.add_argument("projectile",type=str,help="projectile = a,p,d,n,g,t")
    args=parser.parse_args()
    x=createTalysJson()
    x.single(args.mass, args.element, args.projectile)
    
