# -*- coding: utf-8 -*-
"""
Created on Mon Jul 27 15:28:21 2020

@author: dataphile-jeff
"""
import matplotlib.pyplot as plt
from datetime import datetime,date
import numpy as np
import random


'''////////////////////////////////////////////////////////////////////Functions'''
'''////////////////////////////////////////////////////////////////////Functions'''

'''define functions'''
def days_between(d1, d2):
    d1 = datetime.strptime(d1, "%Y-%m-%d")
    d2 = datetime.strptime(d2, "%Y-%m-%d")
    return abs((d2 - d1).days)

def FV(rate, periods, payment, present_value, beginning): 
	return float(present_value*(1 + rate)**periods + payment*(1 + rate*beginning)*((1 + rate)**periods - 1) / rate)

def bootstrap(mean, cov, cumWealth, yearsTillRetirement,payment):
    '''New fictional growths and inflations through retirement with appropriate covariance'''
    growths, inflations, unemploys = np.random.multivariate_normal(mean, cov, size=int(yearsTillRetirement)).T
    
    #set baseline variables
    cumGrowth=1
    
    j=0
    for growth in growths:
        thisPayment=(payment/12)
        thisGrowth=(growth-inflations[j])/12
        cumGrowth=cumGrowth*(1+(growth-inflations[j]))
        cumWealth=FV(thisGrowth,12,thisPayment,cumWealth,1)
        j=j+1
    
    return cumWealth,cumGrowth

def bootstrap_unemploy(mean, cov, cumWealth, yearsTillRetirement,payment):
    '''New fictional growths and inflations through retirement with appropriate covariance'''
    growths, inflations, unemploys = np.random.multivariate_normal(mean, cov, size=int(yearsTillRetirement)).T
    
    #set baseline variables
    unemployedTime=0
    countUnemploys=0
    cumGrowth=1
    
    j=0
    for growth in growths:
        thisPayment=(payment/12)
        thisGrowth=(growth-inflations[j])/12
        cumGrowth=cumGrowth*(1+(growth-inflations[j]))
        employChance=random.random()
        if((employChance<=(unemploys[j])/2) and (unemployedTime==0)):
            unemployedTime=random.randint(1, 2)
            countUnemploys=countUnemploys+1
        if(unemployedTime>0):
            cumWealth=FV(thisGrowth,12,thisPayment*.25,cumWealth,1)
            unemployedTime=unemployedTime-1
        else:
            cumWealth=FV(thisGrowth,12,thisPayment,cumWealth,1)
        j=j+1
    
    return cumWealth,countUnemploys,cumGrowth

def diff_month(d1, d2):
    return (d1.year - d2.year) * 12 + d1.month - d2.month

def CAGR(last,first,N):
    return (last/first)**(1/N)-1

'''//////////////////////////////////////////////////Starting Assumptions'''
'''//////////////////////////////////////////////////Starting Assumptions'''
#now
today = date.today()
#current age
age=38
#retirement age
retire=55
#retirement year
retireYear=str((retire-age)+int(today.strftime("%Y")))
#years till retirement
yearsTillRetirement=days_between(today.strftime("%Y-%m-%d"), retireYear+'-01-01')/365.25
#market capital today
startCapital=250000 
#normal payment
normalPayment=25000 
#projected expectation from FV
expectedFV=FV(.04,yearsTillRetirement,normalPayment,startCapital,1)
#CAGRs for expected NW projections
CAGRFV=CAGR(expectedFV,startCapital,yearsTillRetirement)
CAGRFVNC=.04
#iterations to run
iterations=10000
#downward adjustment to the percentage of real growth rates
downward=.04

'''//////////////////////////////////////////////////Basic Scenario'''
'''//////////////////////////////////////////////////Basic Scenario'''

#array of real annualized growth rates, inflation rates, and unemployment rates
x = np.array([[0.0401,0.0584,0.049],[0.1431,0.043,0.059],[0.1898,0.0327,0.056],[-0.1466,0.0616,0.049],[-0.2647,0.1103,0.056],[0.372,0.092,0.085],
              [0.2384,0.0575,0.077],[-0.0718,0.065,0.071],[0.0656,0.0762,0.061],[0.1844,0.1122,0.058],[0.325,0.1358,0.071],[-0.0492,0.1035,0.076],
              [0.2155,0.0616,0.097],[0.2256,0.0322,0.096],[0.0627,0.043,0.075],[0.3173,0.0355,0.072],[0.1867,0.0191,0.07],[0.0525,0.0366,0.062],
              [0.1661,0.0408,0.055],[0.3169,0.0483,0.053],[-0.031,0.0539,0.056],[0.3047,0.0425,0.068],[0.0762,0.0303,0.075],[0.1008,0.0296,0.069],
              [0.0132,0.0261,0.061],[0.3758,0.0281,0.056],[0.2296,0.0293,0.054],[0.3336,0.0234,0.049],[0.2858,0.0155,0.045],[0.2104,0.0219,0.042],
              [-0.091,0.0338,0.04],[-0.1189,0.0283,0.047],[-0.221,0.0159,0.058],[0.2868,0.0227,0.06],[0.1088,0.0268,0.055],[0.0491,0.0339,0.051],
              [0.1579,0.0324,0.046],[0.0549,0.0285,0.046],[-0.37,0.0385,0.058],[0.2646,-0.0034,0.093],[0.1506,0.0164,0.096],[0.0211,0.0316,0.089],
              [0.16,0.0207,0.081],[0.3239,0.0147,0.074],[0.1369,0.0162,0.062],[0.0138,0.0012,0.053],[0.1196,0.0126,0.049],[0.2183,0.0213,0.044],
              [-0.0438,0.0244,0.039],[0.3149,0.0181,0.037]]).T

'''//////////////////////////////////////////////////Track runtime of script'''
begin_time = datetime.now()

#empty array to hold results
results=[]
results_growths=[]
#calculate the means from the real values above
mean = (np.mean(x[0]),np.mean(x[1]),np.mean(x[2]))
#calculate the covariance matrix from the real covariances between growth, inflation, and unemployment
cov = np.cov(x)

for i in range(iterations):
    this_result,this_growth=bootstrap(mean,cov,startCapital,yearsTillRetirement,normalPayment)
    results.append(this_result)
    results_growths.append(this_growth)


'''//////////////////////////////////////////////////Unemployment Scenario'''
'''//////////////////////////////////////////////////Unemployment Scenario'''
#empty array to hold results
results_unemploy=[]
results_unemploy_counts=[]
results_unemploy_growths=[]

for i in range(iterations):
   this_result_unemploy,this_unemploy_count,this_unemploy_growth=bootstrap_unemploy(mean, cov, startCapital, yearsTillRetirement,normalPayment)
   results_unemploy.append(this_result_unemploy)
   results_unemploy_counts.append(this_unemploy_count)
   results_unemploy_growths.append(this_unemploy_growth)

'''//////////////////////////////////////////////////Reduced Growth Scenario'''
'''//////////////////////////////////////////////////Reduced Growth Scenario'''
#array of downward-adjusted annualized growth rates, real inflation rates, and real unemployment rates
x[0]=np.subtract(x[0],downward)

#empty array to hold results
results_downward=[]
results_downward_growths=[]

#calculate the means from the real values above
mean = (np.mean(x[0]),np.mean(x[1]),np.mean(x[2]))
#calculate the covariance matrix from the real covariances between growth, inflation, and unemployment
cov = np.cov(x)

for i in range(iterations):
    this_result,this_growth=bootstrap(mean,cov,startCapital,yearsTillRetirement,normalPayment)
    results_downward.append(this_result)
    results_downward_growths.append(this_growth)


'''//////////////////////////////////////////////////Review Results'''
'''//////////////////////////////////////////////////Review Results'''

#normal scenario average, median, median growth CAGR, and median total CAGR
print(f'Average Retiring NW: {np.average(results):,.0f}')
print(f'Median Retiring NW: {np.percentile(results,50):,.0f}')
print(f'Median Growth CAGR: {CAGR(float(np.percentile(results_growths,50)),1,yearsTillRetirement):,.4f}')
print(f'Median Total CAGR: {CAGR(float(np.percentile(results,50)),startCapital,yearsTillRetirement):,.4f}')

#unemployement scenario average, median, median growth CAGR, median total CAGR, and unemployment frequency
print(f'Average Retiring NW: {np.average(results_unemploy):,.0f}')
print(f'Median Retiring NW: {np.percentile(results_unemploy,50):,.0f}')
print(f'Median Growth CAGR: {CAGR(float(np.percentile(results_unemploy_growths,50)),1,yearsTillRetirement):,.4f}')
print(f'Median Total CAGR: {CAGR(float(np.percentile(results_unemploy,50)),startCapital,yearsTillRetirement):,.4f}')
npUnemployCounts=np.array(results_unemploy_counts)
print(f'Unemployment Frequency: {len(npUnemployCounts[np.where(npUnemployCounts > 0)])/len(results_unemploy):,.4f}')

#downward growth scenario average, median, median growth CAGR, and median total CAGR
print(f'Average Retiring NW: {np.average(results_downward):,.0f}')
print(f'Median Retiring NW: {np.percentile(results_downward,50):,.0f}')
print(f'Median Growth CAGR: {CAGR(float(np.percentile(results_downward_growths,50)),1,yearsTillRetirement):,.4f}')
print(f'Median Total CAGR: {CAGR(float(np.percentile(results_downward,50)),startCapital,yearsTillRetirement):,.4f}')


'''//////////////////////////////////////////////////Track runtime of script'''
print(f'Runtime: {(datetime.now() - begin_time):}')





'''////////////////////////////////////////////////////////////////////Charts'''
'''////////////////////////////////////////////////////////////////////Charts'''
'''////////////////////////////////////////////////////////////////////Charts'''
'''////////////////////////////////////////////////////////////////////Charts'''





'''//////////////////////////////////////////////////Histogram Charts'''
'''//////////////////////////////////////////////////Histogram Charts'''
#divide to get results in millions and remove those with absurdly low probabilites/high values
graphResults=list(filter(lambda x: x <= 20, np.divide(results,1000000)))
graphResults_Unemploy=list(filter(lambda x: x <= 20, np.divide(results_unemploy,1000000)))
graphResults_Downward=list(filter(lambda x: x <= 20, np.divide(results_downward,1000000)))

#scenarios
fig, ax = plt.subplots(figsize=(10,5))
plt.hist(graphResults, bins=40, color='blue',label='Normal')
plt.hist(graphResults_Unemploy, bins=40, color='purple',alpha=.66,label='Unemployment')
plt.hist(graphResults_Downward, bins=40, color='green',alpha=.66,label='Downward Growth')
plt.xlabel("Retirement NW (in MM)")
plt.ylabel("frequency")
plt.xticks(np.arange(round(min(graphResults+graphResults_Unemploy+graphResults_Downward)), 20, 2.0))
plt.legend(loc='upper right')
ax.set_axisbelow(True)
plt.xticks(rotation=90)
plt.axvline(x=expectedFV/1000000,dashes=[6, 2],color='red',alpha=.66,label='Projected NW (FV)')
plt.grid()
plt.show()   



'''//////////////////////////////////////////////////Percentile Charts'''
'''//////////////////////////////////////////////////Percentile Charts''' 
percentiles=[
    round(np.percentile(graphResults,10),2),
    round(np.percentile(graphResults,20),2),
    round(np.percentile(graphResults,30),2),
    round(np.percentile(graphResults,40),2),
    round(np.percentile(graphResults,50),2),
    round(np.percentile(graphResults,60),2),
    round(np.percentile(graphResults,70),2),
    round(np.percentile(graphResults,80),2),
    round(np.percentile(graphResults,90),2)
]

percentiles_unemploy=[
    round(np.percentile(graphResults_Unemploy,10),2),
    round(np.percentile(graphResults_Unemploy,20),2),
    round(np.percentile(graphResults_Unemploy,30),2),
    round(np.percentile(graphResults_Unemploy,40),2),
    round(np.percentile(graphResults_Unemploy,50),2),
    round(np.percentile(graphResults_Unemploy,60),2),
    round(np.percentile(graphResults_Unemploy,70),2),
    round(np.percentile(graphResults_Unemploy,80),2),
    round(np.percentile(graphResults_Unemploy,90),2)
]

percentiles_downward=[
    round(np.percentile(graphResults_Downward,10),2),
    round(np.percentile(graphResults_Downward,20),2),
    round(np.percentile(graphResults_Downward,30),2),
    round(np.percentile(graphResults_Downward,40),2),
    round(np.percentile(graphResults_Downward,50),2),
    round(np.percentile(graphResults_Downward,60),2),
    round(np.percentile(graphResults_Downward,70),2),
    round(np.percentile(graphResults_Downward,80),2),
    round(np.percentile(graphResults_Downward,90),2)
]

width = .25 
pos = list(range(len(percentiles))) 
titles=[]
for i in range(10,100,10):
    titles.append(str(i)+"th")


fig, ax = plt.subplots(figsize=(10,5))
ax.set_axisbelow(True)
plt.grid()
plt.bar(pos,percentiles,width,color='blue',label='Normal')
plt.bar([p + width for p in pos],percentiles_unemploy,width,color='orange',label='Unemployment')
plt.bar([p + width*2 for p in pos],percentiles_downward,width,color='green',label='Downward Growth')
plt.hlines(expectedFV/1000000,0-width,9,linestyles='dotted',color='red',label='Projected NW (FV)')
ax.set_ylabel('Retirement NW (in MM)')
ax.set_title('Projected Retirement NW by Scenario')
ax.set_xticklabels(titles)
ax.set_xticks([p + 1.5 * width for p in pos])
plt.legend(loc='upper left')

plt.show()   

print(f'{np.percentile(results,10):,}')
print(f'{np.percentile(results,20):,}')
print(f'{np.percentile(results,30):,}')
print(f'{np.percentile(results,40):,}')
print(f'{np.percentile(results,50):,}')
print(f'{np.percentile(results,60):,}')
print(f'{np.percentile(results,70):,}')
print(f'{np.percentile(results,80):,}')
print(f'{np.percentile(results,90):,}')

'''//////////////////////////////////////////////////GROWTH CAGR Charts'''
'''//////////////////////////////////////////////////GROWTH CAGR Charts''' 
#exponent for CAGR calculation
powerVar=(1/yearsTillRetirement)

#normal scenario
resultsCAGR=np.divide(results_growths,1)
resultsCAGR=np.power(resultsCAGR,powerVar)
resultsCAGR=np.subtract(resultsCAGR,1)

#unemployment scenario
results_unemployCAGR=np.divide(results_unemploy_growths,1)
results_unemployCAGR=np.power(results_unemployCAGR,powerVar)
results_unemployCAGR=np.subtract(results_unemployCAGR,1)

#downward growth scenario
results_downwardCAGR=np.divide(results_downward_growths,1)
results_downwardCAGR=np.power(results_downwardCAGR,powerVar)
results_downwardCAGR=np.subtract(results_downwardCAGR,1)

percentiles_CAGR=[
    round(np.percentile(resultsCAGR,10),2),
    round(np.percentile(resultsCAGR,20),2),
    round(np.percentile(resultsCAGR,30),2),
    round(np.percentile(resultsCAGR,40),2),
    round(np.percentile(resultsCAGR,50),2),
    round(np.percentile(resultsCAGR,60),2),
    round(np.percentile(resultsCAGR,70),2),
    round(np.percentile(resultsCAGR,80),2),
    round(np.percentile(resultsCAGR,90),2)
]

percentiles_unemploy_CAGR=[
    round(np.percentile(results_unemployCAGR,10),2),
    round(np.percentile(results_unemployCAGR,20),2),
    round(np.percentile(results_unemployCAGR,30),2),
    round(np.percentile(results_unemployCAGR,40),2),
    round(np.percentile(results_unemployCAGR,50),2),
    round(np.percentile(results_unemployCAGR,60),2),
    round(np.percentile(results_unemployCAGR,70),2),
    round(np.percentile(results_unemployCAGR,80),2),
    round(np.percentile(results_unemployCAGR,90),2)
]

percentiles_downward_CAGR=[
    round(np.percentile(results_downwardCAGR,10),2),
    round(np.percentile(results_downwardCAGR,20),2),
    round(np.percentile(results_downwardCAGR,30),2),
    round(np.percentile(results_downwardCAGR,40),2),
    round(np.percentile(results_downwardCAGR,50),2),
    round(np.percentile(results_downwardCAGR,60),2),
    round(np.percentile(results_downwardCAGR,70),2),
    round(np.percentile(results_downwardCAGR,80),2),
    round(np.percentile(results_downwardCAGR,90),2)
]

fig, ax = plt.subplots(figsize=(10,5))
ax.set_axisbelow(True)
plt.grid()
plt.bar(pos,percentiles_CAGR,width,color='blue',label='Normal')
plt.bar([p + width for p in pos],percentiles_unemploy_CAGR,width,color='orange',label='Unemployment')
plt.bar([p + width*2 for p in pos],percentiles_downward_CAGR,width,color='green',label='Downward Growth')
plt.hlines(CAGRFVNC,0-width,9,linestyles='dotted',color='red',label='Projected NW (FV)')
ax.set_ylabel('CAGR')
ax.set_title('Market Growth CAGR by Scenario')
ax.set_xticklabels(titles)
ax.set_xticks([p + 1.5 * width for p in pos])
plt.legend(loc='upper left')

plt.show()  


'''//////////////////////////////////////////////////TOTAL CAGR Charts'''
'''//////////////////////////////////////////////////TOTAL CAGR Charts''' 
#exponent for CAGR calculation
powerVar=(1/yearsTillRetirement)

#normal scenario
resultsCAGR=np.divide(results,startCapital)
resultsCAGR=np.power(resultsCAGR,powerVar)
resultsCAGR=np.subtract(resultsCAGR,1)

#unemployment scenario
results_unemployCAGR=np.divide(results_unemploy,startCapital)
results_unemployCAGR=np.power(results_unemployCAGR,powerVar)
results_unemployCAGR=np.subtract(results_unemployCAGR,1)

#downward growth scenario
results_downwardCAGR=np.divide(results_downward,startCapital)
results_downwardCAGR=np.power(results_downwardCAGR,powerVar)
results_downwardCAGR=np.subtract(results_downwardCAGR,1)

percentiles_CAGR=[
    round(np.percentile(resultsCAGR,10),2),
    round(np.percentile(resultsCAGR,20),2),
    round(np.percentile(resultsCAGR,30),2),
    round(np.percentile(resultsCAGR,40),2),
    round(np.percentile(resultsCAGR,50),2),
    round(np.percentile(resultsCAGR,60),2),
    round(np.percentile(resultsCAGR,70),2),
    round(np.percentile(resultsCAGR,80),2),
    round(np.percentile(resultsCAGR,90),2)
]

percentiles_unemploy_CAGR=[
    round(np.percentile(results_unemployCAGR,10),2),
    round(np.percentile(results_unemployCAGR,20),2),
    round(np.percentile(results_unemployCAGR,30),2),
    round(np.percentile(results_unemployCAGR,40),2),
    round(np.percentile(results_unemployCAGR,50),2),
    round(np.percentile(results_unemployCAGR,60),2),
    round(np.percentile(results_unemployCAGR,70),2),
    round(np.percentile(results_unemployCAGR,80),2),
    round(np.percentile(results_unemployCAGR,90),2)
]

percentiles_downward_CAGR=[
    round(np.percentile(results_downwardCAGR,10),2),
    round(np.percentile(results_downwardCAGR,20),2),
    round(np.percentile(results_downwardCAGR,30),2),
    round(np.percentile(results_downwardCAGR,40),2),
    round(np.percentile(results_downwardCAGR,50),2),
    round(np.percentile(results_downwardCAGR,60),2),
    round(np.percentile(results_downwardCAGR,70),2),
    round(np.percentile(results_downwardCAGR,80),2),
    round(np.percentile(results_downwardCAGR,90),2)
]

fig, ax = plt.subplots(figsize=(10,5))
ax.set_axisbelow(True)
plt.grid()
plt.bar(pos,percentiles_CAGR,width,color='blue',label='Normal')
plt.bar([p + width for p in pos],percentiles_unemploy_CAGR,width,color='orange',label='Unemployment')
plt.bar([p + width*2 for p in pos],percentiles_downward_CAGR,width,color='green',label='Downward Growth')
plt.hlines(CAGRFV,0-width,9,linestyles='dotted',color='red',label='Projected NW (FV)')
ax.set_ylabel('CAGR')
ax.set_title('Total Growth (market + contributions) CAGR by Scenario')
ax.set_xticklabels(titles)
ax.set_xticks([p + 1.5 * width for p in pos])
plt.legend(loc='upper left')

plt.show()  
