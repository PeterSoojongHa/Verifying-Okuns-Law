#Verifying Okun's law (A country's change in real GDP over time and its change in unemployment over time are linearly related)
#Hypothesis test to determine whether there is a linear relationship between US % Unemployment growth and Real GDP growth.
#H0: There is no linear relationship between US % Unemployment growth and Real GDP growth
#Ha: There is a linear relationship between US % Unemployment growth and Real GDP growth
#The alpha-level (.05) is used to accept/reject H0
alpha_level = .05

print("This program verifies Okun's law using recent US unemployment and real GDP data.")
print("It will conduct a hypothesis test to determine whether there is a linear relationship between US % Unemployment growth and Real GDP growth.")
print(" ")
print("H0: There is no linear relationship between US % Unemployment growth and Real GDP growth.")
print("Ha: There is a linear relationship between US % Unemployment growth and Real GDP growth.")
print("an alpha level of %s will be used to accept or reject H0" % alpha_level)



#DATA EXTRACTION
#Data was sourced from https://www.kaggle.com/datasets/pavankrishnanarne/us-real-gdp-quarterly-data-1947-present and https://data.bls.gov/timeseries/LNS14000000. (converted from .xlxs to .csv)
print(" ")
print("Extracting and organizing data...")

import pandas as pd
import numpy as np
from scipy.stats import pearsonr
import matplotlib.pyplot as plt

#Imports the last 40 quarters (10 years) of US real GDP data, and calculates their % growth.
rgdp_data = pd.read_csv('RGDP.csv')
rgdp_data["Prev RGDP"] = rgdp_data.value.shift(1)
rgdp_data["% growth (RGDP)"] = (rgdp_data["value"] / rgdp_data["Prev RGDP"] - 1)
rgdp_data = rgdp_data.drop(rgdp_data.index[:266])
rgdp_data = rgdp_data.reset_index(drop=True)
rgdp_data.drop(columns=["value", "Prev RGDP"], inplace = True)

#Imports/derives the last 10 quarters (10 years) of US unemployment data (converts monthly -> quarterly).
unemp_data = pd.read_csv('Unemployment.csv')
unemp_data = unemp_data.drop(unemp_data.index[:10])
unemp_data.columns = unemp_data.iloc[0]
unemp_data = unemp_data.rename_axis("Index", axis=0)
unemp_data = unemp_data.drop(unemp_data.index[0])
unemp_data = unemp_data.reset_index(drop=True)
unemp_data.drop(columns=['Feb','Mar', 'May', 'Jun', 'Aug', 'Sep', 'Nov', 'Dec'], inplace=True)

#Organize US unemployment data in the same format as US real gdp data and calculates their % growth
tp_unemp_data = unemp_data.transpose()
tp_unemp_data.columns = tp_unemp_data.iloc[0]
form_unemp_data = pd.concat([tp_unemp_data, tp_unemp_data.T.stack().reset_index(name='percent_unemployed')['percent_unemployed']], axis=1)
form_unemp_data.drop(columns=['2013','2014', '2015', '2016', '2017', '2018', '2019', '2020', '2021', '2022', '2023'], inplace=True)
form_unemp_data = form_unemp_data.drop(form_unemp_data.index[:7])
form_unemp_data = form_unemp_data.drop(form_unemp_data.index[3:70:5])
form_unemp_data = form_unemp_data.reset_index(drop=True)
form_unemp_data["Prev unemp"] = form_unemp_data.percent_unemployed.shift(1)
form_unemp_data = form_unemp_data.drop(form_unemp_data.index[0])
form_unemp_data['Prev unemp'] = form_unemp_data['Prev unemp'].astype(float)
form_unemp_data['percent_unemployed'] = form_unemp_data['percent_unemployed'].astype(float)
form_unemp_data["% growth (Unemployment)"] = (form_unemp_data["percent_unemployed"] / form_unemp_data["Prev unemp"] - 1)
form_unemp_data.drop(columns=["percent_unemployed", "Prev unemp"], inplace = True)
form_unemp_data = form_unemp_data.reset_index(drop=True)

#Combine US RGDP and unemployment data onto one dataframe
df = rgdp_data.join(form_unemp_data)
df.set_index('date')
df.drop(columns=["date"], inplace = True)
print("Data organization complete.")

while True:
    prompt1=input('Would you like to view the data as a table? (y/n)').lower()

    if prompt1 == 'y':
       print(df)
       break
    elif prompt1 == 'n':
       break
    else:
       print('please input y (yes) or n (no)')
while True:
    prompt2=input('Would you like to view the data as a scatterplot? (y/n)').lower()

    if prompt2 == 'y':
       df.plot.scatter(x = '% growth (Unemployment)', y = '% growth (RGDP)')
       plt.show()
       break
    elif prompt2 == 'n':
       break
    else:
       print('please input y (yes) or n (no)')



#DATA ANALYSIS
print(" ")
print("Proceeding to data analysis...")

#finding the correlation coefficient (r) and the p_value
correlation_coeff = pearsonr(df['% growth (RGDP)'], df['% growth (Unemployment)'])[0]
p_val = pearsonr(df['% growth (RGDP)'], df['% growth (Unemployment)'])[1]
print("The value of r (the correlation coefficient) is %s." % correlation_coeff)
print("The p-value (the probability of the data set existing assuming that H0 is true) is %s" % p_val)



#Conclusions
print(" ")
print("The conclusions are as follows:")
if correlation_coeff < -.75:
    print("As the correlation coefficient is near -1, it indicates a strong, negative, linear relationship between the change in RGDP and Unemployment over time.")
elif correlation_coeff >.75:
    print("As the correlation coefficient is near +1, it indicates a strong, positive, linear relationship between the change in RGDP and Unemployment over time.")
else:
    print("As the correlation coefficient is not significantly near -1 or +1, it does not indicate a clear linear relationship between the change in RGDP and Unemployment over time.")
if p_val <= alpha_level:
    print("As the p_value (%s) is less than or equal to the alpha level (%s), we succeed in rejecting H0." % (p_val, alpha_level))
    print("There is enough evidence to suggest a linear relationship between % Unemployment growth and Real GDP Growth in the US, which successfully verifies Okun's law")
else:
    print("As the p_value (%s) is greater than the alpha level(%s), we fail to reject H0." % (p_val, alpha_level))
    print("There is not enough evidence to suggest a linear relationship between % Unemployment growth and Real GDP Growth in the US, which fails to verify Okun's law")
	
