from __future__ import division

import os
import pandas
import numpy
import csv

# method can be BinSeg, PELT ou SegNeigh
method="BinSeg"

# Penalty can be BIC, SIC, MBIC, AIC or Hannan-Quinn
penalty="SIC"

# Distribution can be Normal, Gamma, Poisson ou empirical_distribution
test_stat="Normal"

# length of the window
len_window=3


#Function that gives credit to the first true positive found within the window and ignores any other true positives
#within the window. An empty window is a false negative. At the end of this run, the number of points that have not been flagged
#as true positive or false negative are flagged as false positives
def perf_measure(labels, predictions):
    TP = 0
    FP = 0
    TN = 0
    FN = 0
    bla=[]
    for i in range(3,len(labels)-1): 
        if labels[i]==1:
            index=numpy.flatnonzero(predictions[i-len_window:i+len_window])
            if len(index)>0:
                cp=index.flat[numpy.abs(index - len_window).argmin()]
                predictions[i+cp-len_window]=0
                TP+=1
            else:
                FN+=1
    FP=sum(predictions)
    TN= len(labels)-TP-FN-FP
    

    return (TP, FP, TN, FN)


results=[]

#Path to the .csv files containing the results of the tested algorithm

files = os.listdir("/Path../results/"+method+"_"+penalty+"_"+test_stat)

files = [k.replace('result','') for k in files if k.endswith('.csv')]


for i in files:

    #change the directory to the one with the ground truth data
    
    os.chdir("Path../Labeled")

    # load ground truth file
    data = pandas.read_csv(i, sep=';')

    #  ground truth
    try:
        labels= [eval(str(k).strip()) for k in data['cp']]
    except (TypeError, ValueError) as e:
        print e
    nbre_cp=sum(labels)
    tai=len(labels)

    
    # load the change point detection results

    path="/Path../results/"+method+"_"+penalty+"_"+test_stat"+method+"_"+penalty+"_"+test_stat

    os.chdir(path)

    fil="result"+i

    data = pandas.read_csv(fil, sep=';')
    
    predictions = data['cp']

    x=perf_measure(labels, predictions)
    
    TP=x[0]
    FP=x[1]
    TN=x[2]
    FN=x[3]
    
    p=[method+"_"+penalty+"_"+test_stat,TP/nbre_cp,FN/nbre_cp,FP/tai]

    #Write the results of the scoring algorithm in a .csv file in the following directory path

    path="/Path.../globalresults/"

    os.chdir(path)
    with open(i, "a") as output:
        writer = csv.writer(output,delimiter=';', lineterminator='\n')
        writer.writerow(p)    
    results.append(p)

