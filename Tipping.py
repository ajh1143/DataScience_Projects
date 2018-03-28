import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

#Get file, extract dataframe
def getTipFile(fileName):
    raw_data = pd.read_csv(fileName)
    df = pd.DataFrame(raw_data)
    return df
    
#Explore Data
def EDA(dataframe, outputpath):
    head = str(dataframe.head())
    desc = str(dataframe.describe())
    missing = str(dataframe.info())
    lineBreak = "---------------------------------------"
    text_data = (lineBreak, head, lineBreak, desc, lineBreak, missing, lineBreak)
    for each in text_data:
        print(each+'\n')
    print_EDA(outputpath, head, desc, dataframe, lineBreak)

#Print to File
def print_EDA(output, head, desc, df, lb):
    with open(output, "w") as file:
        file.write(lb+"\n")
        file.write(head+"\n"+lb +"\n")
        file.write(desc + "\n"+lb+"\n")
        f = open('dataframe.info()', 'w+')
        df.info(buf=file)
        f.close()
        
#Set Input and Output file name + locations
input_file = "tips.csv"
output_file = "tips_report.txt"

#Extract DataFrame
df1 = getTipFile(input_file)
#EDA
EDA(df1, output_file)

#Pivot Table Creation and Plots
table = pd.pivot_table(df1, values='tip', index=['sex'], aggfunc= [np.mean, min, max])
table.plot(kind='bar', title = "Sex and Tips")
plt.xlabel("Sex \n (Male / Female)")
plt.ylabel("Customer Tips (USD)")
plt.grid(True)
plt.tight_layout()

table = pd.pivot_table(df1, values='tip', index=['sex', 'day'], aggfunc= [np.mean, min, max])
table.plot(kind='bar', title = "Sex and Day")
plt.xlabel("Sex and Day")
plt.ylabel("Customer Tips (USD)")
plt.grid(True)
plt.tight_layout()
plt.show()

table = pd.pivot_table(df1, values='tip', index=['sex', 'smoker'], aggfunc= [np.mean, min, max])
table.plot(kind='bar', title = "Sex, Smokers, and Tips")
plt.xlabel("Sex and Smoker")
plt.ylabel("Customer Tips (USD)")
plt.grid(True)
plt.tight_layout()
plt.show()

table = pd.pivot_table(df1, values='tip', index=['sex', 'day', 'smoker'], aggfunc= [np.mean, min, max])
table.plot(kind='bar', title = "Sex, Tips, Day, and Smokers")
plt.xlabel("Sex and Smoker Categories")
plt.ylabel("Customer Tips (USD)")
plt.grid(True)
plt.tight_layout()
plt.show()

#Box Plot
df1.boxplot(column='tip', by=['sex', 'smoker', 'day'])
plt.xticks(rotation=90)
plt.show()

#Binarize Data
df1['sex'] = pd.Categorical(df1.sex).codes
