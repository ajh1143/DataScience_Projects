#IMPORT LIBRARIES
import pandas as pd
import matplotlib.pyplot as plt 

#READ DATA
df = pd.read_csv("datasets/cookie_cats.csv")

#EDA
# Check Head
print(df.head())
# Integrity Check
df.info()
# Describe
df.describe()
# Check levels
df.version.unique()

#Sample Size
# Counting the number of players in each AB group.
A = df.version.groupby(df.version == "gate_30").count()
B = df.version.groupby(df.version == "gate_40").count()
print(A)
print(B)

#Total Rounds Played - Population Level
# Counting the number of players for each number of gamerounds 
plot_df = df.groupby("sum_gamerounds").count()
# Plotting the distribution of players that played 0 to 100 game rounds
ax = plot_df[:100].plot()
ax.set_xlabel("Total Game Rounds")
ax.set_ylabel("userid")

#Total Rounds Played - By Groups
# Counting the number of players for each number of gamerounds 
Group_A = df[df.version == 'gate_30']
print(Group_A.head())
print(Group_B.head())
Group_B = df[df.version == 'gate_40']
bins = [0,1,10,20,30,40,50,60,70,80,90,100,200,500]
plt.style.use('ggplot')
plot_GA = pd.DataFrame(Group_A.groupby(pd.cut(Group_A["sum_gamerounds"], bins=bins)).count())
plot_GB = pd.DataFrame(Group_B.groupby(pd.cut(Group_B["sum_gamerounds"], bins=bins)).count())
# Plotting the distribution of players that played 0 to 100 game rounds
ax = plot_GA[:50].plot(kind = 'bar', y="userid", color = "black", alpha = 1, 
                       title = 'Total Usage By Groups')
plot_GB[:50].plot(kind = 'bar', y="userid", ax=ax, color = "red", alpha = 0.7 )
ax.set_xlabel("Total Game Rounds")
ax.set_ylabel("Players")
#plt.axvline(30, linestyle='dashed', linewidth=2)
#plt.axvline(40, linestyle='dashed', linewidth=2)
plt.legend(["Group A", "Group B"])
plt.tight_layout()
plt.grid(True)

#Single Day Retention - Population Level
# Calculate percent of returning users - next day
oneday = df.retention_1.sum()/df.retention_1.count()
print(str(oneday*100)+"%")

#Single Day Retention - By Groups 
#Calculating 1-day retention for each AB-group
oneday = df.retention_1.groupby(df.version).sum()/df.retention_1.groupby(df.version).count()
print(oneday)

#Bootstrapping Statistics
# Creating an list with bootstrapped means for each AB-group
boot_1d = []
for i in range(500):
    boot_mean = df.retention_1.sample(frac=1, replace=True).groupby(df.version).mean()
    boot_1d.append(boot_mean)
    
# Transform boot_1d to a Pandas DataFrame
boot_1d = pd.DataFrame(boot_1d)
print(boot_1d)
   
# Create Kernel Density Estimate visual from our bootstrap distributions
boot_1d.plot.kde()

#Calculating AB Group Percent Differences For A New Column, and Plotting
# Populate a new % Difference Column
boot_1d['difference'] = (boot_1d['gate_30'] - boot_1d['gate_40']) /  boot_1d['gate_40'] * 100
# Plot the new Column
ax = boot_1d['difference'].plot.kde()

#Calculating the probability that 1-day retention is greater when the gate is at level 30
prob = (boot_1d['diff'] > 0).sum() / len(boot_1d['diff'])
print(str(prob*100)+"%")

#7-day retention for both AB-groups
sevenday = df.retention_7.sum()/df.retention_7.count()
print(sevenday)

#Generate boot_7d as list containing bootstrapped means for each AB-group
boot_7d = []
for i in range(500):
    boot_mean = df.retention_7.sample(frac=1, replace=True).groupby(df.version).mean()
    boot_7d.append(boot_mean)
    
# boot_7d to Pandas DataFrame
boot_7d = pd.DataFrame(boot_7d)

# Generating % difference column between the two AB-groups
boot_7d['diff'] = (boot_7d['gate_30'] - boot_7d['gate_40']) /  boot_7d['gate_40'] * 100

# Bootstrap % difference kde plot
ax = boot_7d['diff'].plot.kde()
ax.set_xlabel("% difference in means")

# Calculating the probability that 7-day retention is greater when the gate is at level 30
prob = (boot_7d['diff'] > 0).sum() / len(boot_7d['diff'])

# Probability
print(prob)
