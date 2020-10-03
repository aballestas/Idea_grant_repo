# -*- coding: utf-8 -*-
"""
Created on Mon Aug 17 12:42:07 2020

@author: antob
"""

# -*- coding: utf-8 -*-
"""
Created on Mon Aug  3 18:10:46 2020

@author: antob
"""

# -*- coding: utf-8 -*-
"""
Created on Sun Jul 12 19:57:03 2020

@author: antob
"""

import pandas as pd 
import matplotlib.pyplot as plt
from collections import defaultdict

#loads the Google Movement data

movement_df = pd.read_csv("Global_Mobility_Report.csv")


GroceryMovement_filtered = movement_df.loc[movement_df["sub_region_1"] ==  "Florida",["date","grocery", "sub_region_2"]]

GroceryMovement_df = pd.DataFrame(GroceryMovement_filtered)




#deletes the empty counties 
GroceryMovement_df.dropna(
    axis=0,
    how='any',
    thresh=None,
    subset=None,
    inplace=True
)


GroceryMovement_df = pd.DataFrame(GroceryMovement_filtered)




#deletes the empty counties 
GroceryMovement_df.dropna(
    axis=0,
    how='any',
    thresh=None,
    subset=None,
    inplace=True
)


#fills in empty grocery values
GroceryMovement_df.fillna(value = 0 )

'''
                                    Data Stripping Secion
-------------------------------------------------------------------------------------------
'''

#this strips the date, a KEY, and it's date and delta_change it's VALUE
dates_per_county = {}

for index,row in GroceryMovement_df.iterrows():
    date = row["date"]
    county_date_change = (row["grocery"])
    county_name =row["sub_region_2"]
    if date in dates_per_county:
        dates_per_county[date].append(county_date_change)
    else: 
        dates_per_county[date] = [county_date_change]



county_value_dict = {}
list_of_counties = []

for index,row in GroceryMovement_df.iterrows():
    county_date_change = (row["grocery"])
    county_name =row["sub_region_2"]
    if county_name in county_value_dict:
        county_value_dict[county_name].append(county_date_change)
    else: 
        county_value_dict[county_name] = [county_date_change]


for index,row in GroceryMovement_df.iterrows():
    county_name =row["sub_region_2"]
    if county_name not in list_of_counties:
        list_of_counties.append(county_name)

'''
                           Evaluating Lengths for the Loops 
--------------------------------------------------------------------------------------------
'''

#This is the number of counties
# first_dates = dates_per_county[next(iter(dates_per_county))]
number_of_Counties = max(len(item) for item in dates_per_county.values())

#This is the number of dates
number_of_dates = max(len(item) for item in county_value_dict.values())

# print ("Checking if this number matches above: " + str(number_of_Counties))

'''
                                Data Fixing Section  
-------------------------------------------------------------------------------------------
'''
#This ensures that all dates have the same number of obs which is the number of counties 
for date in dates_per_county.keys(): 
    length_of_values = len(dates_per_county[date]) 
    if length_of_values < number_of_Counties:
        missing_ammount = number_of_Counties - length_of_values
        for i in range(missing_ammount):
            dates_per_county[date].append(0)



for county in county_value_dict.keys(): 
    number_of_val = len(county_value_dict[county]) 
    if number_of_val < number_of_dates:
        missing_ammount = number_of_dates - number_of_val
        for w in range(missing_ammount):
            county_value_dict[county].append(-100)




'''
                        Data Evaluation/Dataset Generator 
----------------------------------------------------------------------------------------
'''
#Dict for date and value
num_big_deltas_per_date = {}

#Dict for county and value
infected_counties_per_timestep = {}
infected_counties_per_timestep = defaultdict(list)

# for key in dates_per_county.keys():
#     num_big_deltas_per_date[key] = 0
# #print (num_big_deltas_per_date)

# #This tally's the number of counties that are 'infected' or panic buying 
# #aka over 5% movement     
# for i in range(number_of_Counties):
#     for date in dates_per_county.keys():
#         delta = dates_per_county[date][i]
#         if i < 48: 
#             if delta >= 5.0:
#                 num_big_deltas_per_date[date] += 1
#         else: 
#             if delta >= -10.0:  
#                 num_big_deltas_per_date[date] += 1


#This makes each date a key before the next loop


#This shows the infected counties per date  
   
for x in range(number_of_dates):
    for county in county_value_dict.keys():
        omega = county_value_dict[county][x]
        if x < 48:
            if omega >= 10.0:
                infected_counties_per_timestep[x].append(county)
        else: 
            if omega >= 0:  
                infected_counties_per_timestep[x].append(county)
        
print (len(infected_counties_per_timestep[0]))


for key in infected_counties_per_timestep.keys():
    num_big_deltas_per_date[key] = len(infected_counties_per_timestep[key])
            
        
        
        
        
        
        
'''
                            Ploting and Saving Data Section
-----------------------------------------------------------------------------------------
'''

#Saves the dataset
delta_df = df = pd.DataFrame.from_dict(num_big_deltas_per_date, orient="index")
delta_df.to_csv (path_or_buf ='_4_Florida_grocery_movement.csv',index = True)


#Time Series Plot
delta_df.plot( title = "Florida Panic Buying Timeline", color = "#333333")

#Stay at home marker 
plt.axvline(x = 48, color='#D63931', linestyle=("--")) 


#annotation/arrow
plt.annotate("State wide stay at home order", xy = (48, 60),
              xytext = (49, 60)) 

plt.legend().remove()
plt.margins(0)
plt.ylabel("Number of Panic Buying Counties", fontsize=10)
plt.xlabel("Dates", fontsize=10)
plt.savefig("RESULTS_FloridaInfectedDataPlot.png", dpi=1200)
plt.show()