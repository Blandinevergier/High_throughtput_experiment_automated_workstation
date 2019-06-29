# -*- coding: utf-8 -*-
"""
Created on Mon Jun 24 05:14:05 2019

@author: thurm
"""
import numpy as np
"""
def Factors(): #this function returns a dictionnary containing the factors as keys and the levels.

    buffer=input("Which buffer did you use?")
    dic_factors = {"Buffer":buffer}
    list_factors = []
    fac = input("Please enter the names of the 7 factors of 3 levels separated by a coma:")
    fac2 = input("Please enter the name of the factor of 2 levels separated by a coma:")
    list_factors = fac.split(",")
    list_factors.append(fac2)
    
    for fact in list_factors:
        
       var = input("Please enter the levels of "+fact+" (take care of separating the levels by a coma):")
       levels=var.split(",")
       dic_factors.update({fact:levels})
    
    print(dic_factors)
    
    return(dic_factors)
"""

exp_mat = np.array ([[-1,-1,-1,-1,-1,-1,-1,-1]
                    ,[-1,-1,-1,1,1,0,0,0]
                    ,[-1,0,0,0,1,1,-1,-1]
                    ,[-1,0,1,-1,0,1,0,0]
                    ,[-1,1,1,0,-1,0,1,0]
                    ,[-1,1,0,1,0,-1,1,-1]
                    ,[0,-1,0,0,0,0,0,-1]
                    ,[0,-1,0,-1,-1,1,1,0]
                    ,[0,0,-1,0,1,-1,1,0]
                    ,[0,0,1,1,-1,-1,0,-1]
                    ,[0,1,1,-1,1,0,-1,-1]
                    ,[0,1,-1,1,0,1,-1,0]
                    ,[1,-1,1,1,1,1,1,-1]
                    ,[1,-1,1,0,0,-1,-1,0]
                    ,[1,1,-1,0,-1,1,0,-1]
                    ,[1,1,0,-1,1,-1,0,0]
                    ,[1,0,0,1,-1,0,-1,0]
                    ,[1,0,-1,-1,0,0,1,-1]])
print(exp_mat)
