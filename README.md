Our benchmark is composed of: 
1) an R implementation of the algorithms we want to test from the R packages 'changepoint' and 'changepoint.np'; 
2) a python algorithm that computes the results of the test; 
3) 69 manually labeled RTT time series (the ground truths);

This benchmark will take in input an algorithm we want to test and gives in output the scores of the detection compared to labeled data. 


Our corpus of 69 RTT time series data files (536155 points & 1858 changepoints ) is designed to provide data for research on network performances. It is comprised of both real-world and artificial time series data containing labeled change points.
The majority of the data (49 time series) is real-world gathered from RIPE Atlas from a variety of probes in different Autonomous Systems with different behaviors that we have conscientiously selected and labeled.
