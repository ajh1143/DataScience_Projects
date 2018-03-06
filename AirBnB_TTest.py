#Import Libraries
import pandas as pd
from scipy.stats import ttest_ind
import numpy as np
import matplotlib.pyplot as plt

#Access File
df = pd.read_csv(filepath)

#Extract Columns, Price and Neighborhood
price =  df.price[:]
neighborhood = df.neighborhood[:]
#satisfaction = df.overall_satisfaction[:]
df2 = pd.DataFrame()
df2['Neighborhood'] = neighborhood
df2['Price'] = price

#Save list of neighborhood names
names = df2['Neighborhood'].unique()

#PIVOT DATAFRAME
df3 = df2.pivot(columns='Neighborhood', values='Price')

#Extract Neighborhood A's Price Data
#whittier = df3[['Whittier Heights', 'Portage Bay', 'North Delridge', 'Interbay', 'Crown Hill']]
high_reviews = pd.concat([df3['Whittier Heights'], df3['Portage Bay'], df3['North Delridge'], df3['Interbay'], df3['Crown     
                         Hill']], axis=0)
                         
#Drop Null observations
high_reviews = high_reviews.dropna(how='any',axis=0)

#Check length of good data
print(len(high_reviews))

#Extract Neighborhood B Price Data
#westlake = df3[['Westlake', 'Pike-Market', 'Sunset Hill', 'Westlake', 'Briarcliff', 'Industrial District']]
low_reviews = pd.concat([df3['Westlake'], df3['Pike-Market'], df3['Sunset Hill'], df3['Westlake'], df3['Briarcliff'],
                        df3['Industrial District']], axis=0)
                        
#Drop Null observations
low_reviews = low_reviews.dropna(how='any',axis=0)

#Check length of good data
print(len(low_reviews))

#T-Test (Independent Groups)
#Unequal populations
#Extract mean of means, find mean difference in price
total_mean_high_total = np.mean(high_reviews)
total_mean_low_total = np.mean(low_reviews)
print(str(total_mean_high_total))
print(str(total_mean_low_total))
#Calculate the difference in means
print("Difference in Means from full dataset = $" + str(abs(total_mean_high_total - total_mean_low_total)))
print(ttest_ind(low_reviews, high_reviews))

Random Sampling Method:


t_list = []
p_list = []
higher_means = []
lower_means = []
for each in range(count):
    sample_high = high_reviews.sample(n=150)
    sample_low = low_reviews.sample(n=150)
    higher_means.append(np.mean(sample_high))
    lower_means.append(np.mean(sample_low))
    t,p= ttest_ind(sample_low, sample_high)
    t_list.append(t)
    p_list.append(p)
t_val = np.mean(t_list)
p_val = np.mean(p_list)
total_mean_high = np.mean(higher_means)
total_mean_low = np.mean(lower_means)

#Extract mean of means, find mean difference in price
print(str(total_mean_high))
print(str(total_mean_low))

#Calculate the difference in means
print("Difference in Means = $" + str(abs(total_mean_high - total_mean_low)))

#Print T and P
print("Average T and P Values over " + str(count) + " runs: ")
print("T-Value: " + str(t_val))
print("P-Value: " + str(p_val))

#Plot Distributions

#DataFrame Creation
df_high = pd.DataFrame(higher_means)
df_lower = pd.DataFrame(lower_means)

#Plot fig, axes 
fig, axes = plt.subplots(nrows=1, ncols=2, figsize=(7, 8))
#Apply global title
fig.suptitle("Price Distributions of Top 5 Highest and Lowest Rated AirBnB Neighborhoods")
#Define first plot
ax = df_high.plot.box(color = "green", ax = axes[0], legend = False)
ax.set_ylabel("Price \n(USD)")
ax.set_xlabel("Higher Rated")
#Define second plot
ax2 = df_lower.plot.box(color = "red", ax = axes[1], legend = False)
ax2.set_xlabel("Lower Rated")
#Set y-axes equal for each plot
ax.set_ylim(100, 215)
ax2.set_ylim(100, 215)
#Apply grids to both plots
plt.grid()
plt.grid()
#Tight and Show
plt.tight_layout()
plt.show()
