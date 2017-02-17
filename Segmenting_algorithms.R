library(changepoint)
library(changepoint.np)
library(data.table)

penalty="Hannan-Quinn"
method="PELT"
test.stat="empirical_distribution"

# Path to the directory where you want to store the results of the segmenting algorithms
path="/Path../results/"


#penalty Choice of "None", "SIC", "BIC", "MBIC", AIC", "Hannan-Quinn", "Manual" and "CROPS" penalties. If Manual is specified, the manual penalty is contained in the 
#pen.value parameter. If CROPS is specified, the penalty range is contained in the pen.value parameter; note this is a vector of length 2 which contains the minimum and 
#maximum penalty value. Note CROPS can only be used if the method is "PELT". The predefined penalties listed DO count the changepoint as a parameter, postfix a 0 e.g."SIC0" 
#to NOT count the changepoint as a parameter.

#pen.value The value of the penalty when using the Manual penalty option. A vector of length 2 (min,max) if using the CROPS penalty.

#Create a repository with method, penalty, stat in name
re = paste(method,penalty, test.stat, sep = "_")
repos=paste(path,re, sep = "")
dir.create(repos)


#change the working directory to the one with the ground truth files 
setwd("Path../Labeled/")
l=list.files(pattern = "\\.csv$")
print(l)

#we iterate over all our files

for ( i in l) { 
  
setwd("Path../Labeled/")
  
  
  #read data  
data <- data.table(read.csv2(i, sep=';', dec='.', stringsAsFactors = F))
  
  #collect rtt from .csv file
rtt = data[["rtt"]]
epoch=data[["epoch"]]


#change point detection algorithm 

#Package changepoint.np, for the non-parametric algorithm
out<-cpt.np(rtt, penalty = penalty,method=method, test.stat=test.stat,
       class=TRUE,minseglen=2, nquantiles =4*log(length(data)))

#Package changepoint for the parametric algorithms

# out<-cpt.meanvar(rtt,penalty=penalty,method=method,test.stat=test.stat, Q=400, class=TRUE,minseglen=2)

#Create a vector of length size(rtt) with 1 for a changepoint, 0 else
n<-length(rtt)
cp <- rep(0, n)
cp[cpts(out)]<- 1

#Create a dataframe and save it to .csv
data<-data.frame(epoch,rtt,cp)

#We save into the directory we created at the beginning
setwd(repos)

s3="result"
file = paste(s3,i, sep = "")

write.csv2(data,file=file)
}



