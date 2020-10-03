# -*- coding: utf-8 -*-
"""
Created on Sat Jul 11 17:11:21 2020

@author: antob
"""

import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
from scipy.integrate import odeint
import numpy as np 
import pandas as pd


#read in Flu dataset
infected_data = pd.read_csv ("_NOT_CORECT_Florida_grocery_movement.csv")
infected_data = np.array(infected_data)
t = np.linspace(0,140,140)


#total population 
N = 65
#Initial number of infected: 
I0 = infected_data[0,1]
print("Initial infected is " + str(I0))
#Number of initial recovered: 
R0 = 0
#The number of susceptible: 
S0 = N - I0 - R0


Y0 = S0, I0, R0

days = t 
actual_infected = infected_data[:,1]
# sample_actual_infected = infected_data[0:40,1]
actual_susceptable = N - actual_infected


def SIR (y, t, N, beta, gamma, alpha):
    S, I, R = y
    dSdt = (-beta * S * I)/N + (alpha*R)
    dIdt = (beta * S * I)/N - gamma * I 
    dRdt = (gamma*I) - (alpha*R)
    return dSdt, dIdt, dRdt
    
def fit_ode(x, beta, gamma, alpha):
    return odeint(SIR, Y0, t, args = (N, beta, gamma, alpha))[:,1]

popt, pcov = curve_fit(fit_ode, days, actual_infected, bounds=([0,1]))
fitted = fit_ode(days, *popt)
beta = popt[0]
gamma = popt[1] 
alpha = popt[2]

#The fitted function gives me fitted perameters for any number of perameters I ask, in this case its 2. 
#Look at the fit_ode fn. x is given by days and popt is giving two values (beta and gamma). The star before it is just to grab all the values
#of popt
print ("Beta is: " + str(beta))
print ("Gamma is: " + str(gamma))
print ("Alpha is: " + str(alpha))

#Initial condition vector: 
Y0 = S0, I0, R0

sol = odeint(SIR, Y0, t, args = (N, beta, gamma, alpha))
S, I, R = sol.T


for i in range (10):
    susceptible_list = [S0]
    infected_list = [I0]
    recovered_list = [R0]

    current_susceptable = S0
    current_infected = I0
    current_recovered = R0    

      
    for k in range(139):

        #The rate of people getting sick depend on the number of susceptable and devid by n to get a proportion
        #The reason that the num of current infected is there is to scale up the probability of getting sick 
        #the more sick there are the higher chance of getting sick
        sus_to_inf = np.random.binomial(n = current_susceptable, p = (beta *current_infected)/N)
        #The recovery is independent (does not depend on the number of susceptable)
        inf_to_rec = np.random.binomial(n = current_infected, p = gamma)
        rec_to_sus = np.random.binomial(n = current_recovered, p = alpha)
        
        current_susceptable = current_susceptable - sus_to_inf + rec_to_sus
        current_infected = current_infected - inf_to_rec + sus_to_inf
        current_recovered = current_recovered - rec_to_sus + inf_to_rec
        
        susceptible_list.append(current_susceptable)
        infected_list.append(current_infected)
        recovered_list.append(current_recovered)

    # print("infected list is: ")
    # print((infected_list))
    # print("susceptable list is: ")
    # print((susceptible_list))
    # print("recovered list is:")
    # print(recovered_list)
    # print (len(infected_list))
    # print("the current sus is: " + str(current_susceptable))
        
        
    #coin flip number of infected  
    plt.plot(t, infected_list, c = '#edcc6f', label = "_nolegend_" if i else "Stochastic Estimation")


  # #Graphs the eqation
# plt.plot (t, S, label= "SIR Estimated Susceptable")
plt.plot (t, I, c="#D63931", label = "SIR Estimated Infected")
# plt.plot (t, R, c="g",label = "SIR Estimated Recovered")


#Graphs the real numbers acording to the dataset
plt.plot (t, actual_infected,c = "#333333" ,label = "Actual Infected")
# plt.plot (t, actual_susceptable , c= 'c' ,label = "Actual Susceptable")
plt.margins(0)
plt.title("Model Estimations")
plt.ylabel("Number of Panic Buying Counties", fontsize=10) 
plt.xlabel ('Days', fontsize=10)

plt.legend(fontsize = 'small')
plt.savefig("presentation_Estimated_infected_WRONG.png", dpi = 1200)