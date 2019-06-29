# Autor: Blandine Vergier
# Version: 29-06-2019

#------------------------ LIBRARIES --------------------------------------
import numpy as np
import pandas as pd
import datetime

#------------------------ FUNCTIONS --------------------------------------

def Factors(): #this function returns a dictionnary containing the factors as keys and the levels.

    buffer=input("Which buffer did you used?")
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
       
       
    dic_factors.update({"list_fact":list_factors})
    
    return(dic_factors)
    
def Columns_index(FactorDictionnary): #this function allows to add the columns of the plate corresponding to the tested buffer and the blank as new keys in the dictionnary   
    
    buffer_columns=input("In which columns of the plate did you put the buffer to test? (take care of separating the columns by a coma)")
    buf_columns = buffer_columns.split(",")

    buf_columns = list(map(int,buf_columns))
    
    blank_columns = input("In which column of the plate did you put the blank corresponding to this buffer?")
    blk_columns = blank_columns.split(",")
    blk_columns = list(map(int,blk_columns))
    
    FactorDictionnary.update({"Columns_blank":blk_columns, "Columns_buffer":buf_columns})
    
    return(FactorDictionnary)
    
def Get_data(FileName, DicFactors): #This function returns a dictionary containing all the raw data (keys: "Measured_P", "Measured_S", "Blank_S", "Blank_P")

    with open(FileName) as f:
        lines = f.readlines()[15:30]
        lines = [l.replace (",", ".") for l in lines]
        lines = [li.split('\t') for li in lines]
          
    
    S_values = []
    P_values = []
    Blk_S_values = []
    Blk_P_values = []
    
    for col in DicFactors['Columns_buffer']:
    
        for i in range(0,6):
            S_values.append(float(lines[i*2][int(col)+1]))
            P_values.append(float(lines[i*2+1][int(col)+1]))
            Blk_S_values.append(float(lines[i*2][int(DicFactors['Columns_blank'][0])+1]))
            Blk_P_values.append(float(lines[i*2+1][int(DicFactors['Columns_blank'][0])+1]))
    
    
    
    Raw_data = {"Measured_S":np.array(S_values), "Measured_P":np.array(P_values), "Blank_S":np.array(Blk_S_values), "Blank_P":np.array(Blk_P_values)}

    return(Raw_data)    

def Data_correction(RAW_Data, FactDictionnary, Mod_mat): #this function returns the dictionary containing the data with in addition the corrected data (keys: "Corrected_S", "Corrected_P")

    if "tween" in FactDictionnary["list_fact"]:
        Tween_index = FactDictionnary["list_fact"].index("tween")
    else:
        Tween_index = -2
        
    Cor_S = []
    Cor_P = [] 
    
    for ind in range(0,18):
        if Tween_index > -1:
            if Mod_mat[ind][Tween_index+1]<0:
                Cor_S.append(RAW_Data["Measured_S"][ind]-RAW_Data["Blank_S"][0])
                Cor_P.append(RAW_Data["Measured_P"][ind]-RAW_Data["Blank_P"][0])
                
            else:
                Cor_S.append(RAW_Data["Measured_S"][ind]-RAW_Data["Blank_S"][2])
                Cor_P.append(RAW_Data["Measured_P"][ind]-RAW_Data["Blank_P"][2])
        else:
            Cor_S.append(RAW_Data["Measured_S"][ind]-RAW_Data["Blank_S"][0])
            Cor_P.append(RAW_Data["Measured_P"][ind]-RAW_Data["Blank_P"][0])  
    
    RAW_Data.update({"Corrected_S":np.array(Cor_S), "Corrected_P":np.array(Cor_P)})
    
    return(RAW_Data)
    
    
def Parameter_res(Yexp, X): #this function solves the equation of type Yexp = X.b, with Yexp, X and b the results matrix, the model matrix and the parameters matrix respectively. Yexp_t and X are numpy arrays and their dimensions are (1, n) and (n, m) respectively. 
    
    Yexp = np.asmatrix(Yexp)
    X = np.asmatrix(X)
    X_t = X.transpose()
    
    Parameters = np.linalg.inv(X_t*X)*X_t*Yexp
    
    Parameters = Parameters.tolist()

    parameters = [str(fa[0]) for fa in Parameters]
    
    return(parameters) 
    
def Write_equation(D_factors, Para): #this function returns the equation with all the parameters

    listFactors = D_factors["list_fact"]
    fac2 = [fa+"^2" for fa in listFactors]
    del fac2[7]
    listFactors = listFactors + fac2
    
    equation = "Y = "+ Para[0]+" + "+Para[1]+"*"+listFactors[0]+" + "+Para[2]+"*"+listFactors[1]+" + "+Para[3]+"*"+listFactors[2]+" + "+Para[4]+"*"+listFactors[3]+" + "+Para[5]+"*"+listFactors[4]+" + "+Para[6]+"*"+listFactors[5]+" + "+Para[7]+"*"+listFactors[6]+" + "+Para[8]+"*"+listFactors[7]+" + "+Para[9]+"*"+listFactors[8]+" + "+Para[10]+"*"+listFactors[9]+" + "+Para[11]+"*"+listFactors[10]+" + "+Para[12]+"*"+listFactors[11]+" + "+Para[13]+"*"+listFactors[12]+" + "+Para[14]+"*"+listFactors[13]+" + "+Para[15]+"*"+listFactors[14]
    
    return(equation)    
    
    

def Dict_result(D_factors, Para): #this function returns the equation with all the parameters

    listFactors = D_factors["list_fact"]
    fac2 = [fa+"^2" for fa in listFactors]
    del fac2[7]
    listFactors = listFactors + fac2
    equation = "Y = "+ Para[0]+" + "+Para[1]+"*"+listFactors[0]+" + "+Para[2]+"*"+listFactors[1]+" + "+Para[3]+"*"+listFactors[2]+" + "+Para[4]+"*"+listFactors[3]+" + "+Para[5]+"*"+listFactors[4]+" + "+Para[6]+"*"+listFactors[5]+" + "+Para[7]+"*"+listFactors[6]+" + "+Para[8]+"*"+listFactors[7]+" + "+Para[9]+"*"+listFactors[8]+" + "+Para[10]+"*"+listFactors[9]+" + "+Para[11]+"*"+listFactors[10]+" + "+Para[12]+"*"+listFactors[11]+" + "+Para[13]+"*"+listFactors[12]+" + "+Para[14]+"*"+listFactors[13]+" + "+Para[15]+"*"+listFactors[14]
    
    Add_list_factors = ["", equation]
    nothing = [""]
    listFactors = nothing + listFactors + Add_list_factors
    Para = Para + nothing + nothing
    
    D_result = {"Buffer": ["", D_factors["Buffer"],"","","","","","","","","","","","","","","",""], " ":["", "","","","","","","","","","","","","","","","",""], "Factors":listFactors, "Parameters":Para}
    
    return(D_result) 
    

    
    
#-------------------------------------------------------------------------
current_time = datetime.datetime.now() 



# 0. Creation of the dictionnary containing all the factors
    
Dictionnay_factors = Columns_index(Factors())


# 1. creation of the model matrix

Matrix_model = np.array([[1, -1, -1, -1, -1, -1, -1, -1, -1, 1, 1, 1, 1, 1, 1, 1],
                         [1, -1, -1, -1, 1, 1, 0, 0, 0, 1, 1, 1, 1, 1, 0, 0],
                         [1, -1, 0, 0, 0, 1, 1, -1, -1, 1, 0, 0, 0, 1, 1, 1],
                         [1, -1, 0, 1, -1, 0, 1, 0, 0, 1, 0, 1, 1, 0, 1, 0],
                         [1, -1, 1, 1, 0, -1, 0, 1, 0, 1, 1, 1, 0, 1, 0, 1],
                         [1, -1, 1, 0, 1, 0, -1, 1, -1, 1, 1, 0, 1, 0, 1, 1],
                         [1, 0, -1, 0, 0, 0, 0, 0, -1, 0, 1, 0, 0, 0, 0, 0],
                         [1, 0, -1, 0, -1, -1, 1, 1, 0, 0, 1, 0, 1, 1, 1, 1],
                         [1, 0, 0, -1, 0, 1, -1, 1, 0, 0, 0, 1, 0, 1, 1, 1],
                         [1, 0, 0, 1, 1, -1, -1, 0, -1, 0, 0, 1, 1, 1, 1, 0],
                         [1, 0, 1, 1, -1, 1, 0, -1, -1, 0, 1, 1, 1, 1, 0, 1],
                         [1, 0, 1, -1, 1, 0, 1, -1, 0, 0, 1, 1, 1, 0, 1, 1],
                         [1, 1, -1, 1, 1, 1, 1, 1, -1, 1, 1, 1, 1, 1, 1, 1],
                         [1, 1, -1, 1, 0, 0, -1, -1, 0, 1, 1, 1, 0, 0, 1, 1],
                         [1, 1, 1, -1, 0, -1, 1, 0, -1,  1, 1, 1, 0, 1, 1, 0],
                         [1, 1, 1, 0, -1, 1, -1, 0, 0, 1, 1, 0, 1, 1, 1, 0],
                         [1, 1, 0, 0, 1, -1, 0, -1, 0, 1, 0, 0, 1, 1, 0, 1],
                         [1, 1, 0, -1, -1, 0, 0, 1, -1, 1, 0, 1, 1, 0, 0, 1]])
                       

# 2. Get the data

Raw_Data = Get_data('21062019_group2_HEPES_sodium.txt', Dictionnay_factors)

# 3. Correction of the data and calculation of mP values
    
Corr_Data =  Data_correction(Raw_Data, Dictionnay_factors, Matrix_model)

mp_values = 1000*(Corr_Data["Corrected_P"]-Corr_Data["Corrected_S"])/(Corr_Data["Corrected_P"]+Corr_Data["Corrected_S"])
mp_values = np.array([mp_values])
mp_values = mp_values.transpose()


# 4. Solve the matrix equation
    
Parameter_values = Parameter_res(mp_values,Matrix_model)

# 5. create excel file containing the results

D_Results = Dict_result(Dictionnay_factors, Parameter_values)
Df_Results = pd.DataFrame.from_dict(D_Results)

# Create a Pandas Excel writer using XlsxWriter as the engine.
writer = pd.ExcelWriter(str(current_time.day) + "-" + str(current_time.month) +"-"+str(current_time.year) + "_HD-project_" + Dictionnay_factors["Buffer"]+'-buffer_Results.xlsx', engine='xlsxwriter')

# Convert the dataframe to an XlsxWriter Excel object.
Df_Results.to_excel(writer, sheet_name='Sheet1')

# Close the Pandas Excel writer and output the Excel file.
writer.save()

print("----------- END ------------")
