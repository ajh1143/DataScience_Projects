
#Merging Multiple CSV Files into A Single File

#IMPORT LIBRARIES
import os
import pandas as pd
import matplotlib.pyplot as plt

#IMPORT FILES
#SET DIRECTORY TARGET
dir = input(print("Enter directory"))
#SET FILES ALGORITHM
files = filter(lambda x: x.endswith('.csv'), os.listdir(dir))

#MERGE EACH FILE WITH CONCAT
for file in files:
    raw = pd.read_csv(dir+file)
    df = pd.DataFrame(raw)
    merged = pd.concat([df])

#SAVE OUTPUT FILE
output_path = input(print("Output location"))
merged.to_csv(output_path)

#OPEN AND READ MERGED FILE
df = pd.read_csv(output_path)

#Neighborhood Ratings
#EXTRACT SATISFACTION RATING AND NEIGHBORHOOD
df2 = df[['overall_satisfaction', 'neighborhood']]

#MAKE LIST OF NEIGHBORHOOD NAMES
names = df2['neighborhood'].unique()

#PIVOT DATAFRAME
df3 = df2.pivot(columns='neighborhood', values='overall_satisfaction')

#Creating A New DataFrame

#Create new dataframe with N.Hood, Sample, Average Rating
name_list = []
mean_list = []
count_list = []

#Add Targets to Lists
for each in names:
    name_list.append(each)
    cur_mean = df3[each].mean()
    mean_list.append(cur_mean)
    cur_count = df3[each].count()
    count_list.append(cur_count)

#Create Dict from Lists
raw_data = {'Neighborhood' : name_list,
            'Sample_Size': count_list,
            'Average_Rating': mean_list}

#Create DataFrame from Dict, Specify Columns
df4 = pd.DataFrame(raw_data, columns = ['Neighborhood', 'Sample_Size', 'Average_Rating'])

Plotting The Top 5 Best, and Top 5 Worst Neighborhoods By Average Review


#Sort New DataFrame in Ascending Order
sort_test = df4.sort_values('Average_Rating', ascending=[0])

#Extract Top 5 and Bottom 5 Elements of Sorted DataFrame 
x = sort_test.head(5)
x1 = sort_test.tail(5)

#Set Plot Style
plt.style.use('ggplot')

#Structure Plot, 1 Row and 2 Columns (Creates Side By Side Plot)
fig, axes = plt.subplots(nrows=1, ncols=2, figsize=(7, 8))

#Build Plot

#Figure 1 (Top 5 Best Rated Neighborhoods)
ax = x.plot.bar(color = "green", x= 'Neighborhood', y='Average_Rating', ax = axes[0], legend = False)
ax.set_ylim(top = 5)
ax.set_ylabel("Avg Rating (1-5)")
ax.set_xlabel("")

#Figure 2 (Bottom 5 Worst Rated Neighborhoods)
ax2 = x1.plot.bar(color = "orange", x= 'Neighborhood', y='Average_Rating', ax = axes[1], legend = False)
ax2.set_ylim(top = 5)
ax2.set_ylabel("")
ax2.set_xlabel("")

#Fit Plot and Show Plot
plt.tight_layout()
plt.show()
