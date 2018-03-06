# Importing pandas
import pandas as pd

# Importing matplotlib and setting aesthetics for plotting later.
import matplotlib.pyplot as plt
%matplotlib inline
%config InlineBackend.figure_format = 'svg' 
plt.style.use('fivethirtyeight')

# Reading in current data from coinmarketcap.com
current = pd.read_json("https://api.coinmarketcap.com/v1/ticker/")


#EDA
# Print Column Names
print(current.columns)
# Check Head
print(current.head())
# Check Tail
print(current.tail())

#Build DataFrame and More EDA
# Read the CSV
csv_data = pd.read_csv('datasets/coinsJan2018.csv')
raw_df = pd.DataFrame(csv_data)
# Extract 'id' and 'market_cap_usd' 
market_cap_raw = raw_df[['id','market_cap_usd']]
# Using .info()
print(market_cap_raw.info())
# Summary Statistics
print(market_cap_raw.describe())
# Counting the number of values
market_cap_raw.count()

#Filtering Data
# Filtering out rows without a market capitalization
market_cap_filtered = market_cap_raw.query('market_cap_usd > 0')
# Counting the number of values again
print(market_cap_filtered.info())
print(market_cap_filtered.count())

top_10 = pd.DataFrame(market_cap_filtered[0:10]).set_index('id')
# market_cap_perc top_10 = top_10.assign(market_cap_perc=(top_10.market_cap_usd / market_cap_filtered.market_cap_usd.sum()) * 100)

# Plot- Figure 1
TOP_TEN_TITLE = ''Top 10 Currencies by Market Cap'' TOP_TEN_YLABEL = 'Percent Total (%)'
ax = top_10.plot.bar(y='market_cap_perc', title=TOP_CAP_TITLE)
ax.set_ylabel(TOP_CAP_YLABEL)
plt.show()

#Plot- Figure 2
# Colors for the bar plot
COLORS = ['orange', 'green']
# adding the colors and scaling the y-axis
ax = top_10.plot.bar(title = TOP_CAP_TITLE, color = COLORS)
ax.set_yscale('log')
# Annotating the y axis with 'USD'
ax.set_ylabel('USD')
# Removing useless x-label
ax.set_xlabel('')
plt.show()

#Measuring Volatility
# Selecting the id, percent_change_24h and percent_change_7d columns
volatility = raw_df[['id', 'percent_change_24h', 'percent_change_7d']]
# Setting the index to 'id' and dropping all NaN rows
volatility = volatility.dropna().set_index('id')
# Sorting the DataFrame by percentage_change_24h in ascending order
volatility = volatility.sort_values(by = 'percent_change_24h', ascending = True)
# Checking the first few rows
print(volatility.head())
print(volatility.tail())

#Plotting Volatility
# Defining a function with 2 parameters, the series to plot and the title
def top10_subplot(volatility_series, title):
    # Making the subplot and the figure for two side by side plots
    fig, axes = plt.subplots(nrows=1, ncols=2, figsize=(10, 6))

    # Plotting with pandas the barchart for the top 10 losers
    ax1 = volatility_series[:10].plot.bar(color="red", ax=axes[0])

    # Setting the figure's main title to the text passed as parameter
    fig.suptitle(title)

    # Setting the ylabel to '% change'
    ax1.set_ylabel('% change')
    ax1.set_xlabel('')

    # Same as above, but for the top 10 winners
    ax2 = volatility_series[-10:].plot.bar(color="green", ax=axes[1])
    ax2.set_xlabel('')
    plt.tight_layout()
    plt.show()
    # Returning this for good practice, might use later
    return fig, axes

DTITLE = "24 hours top losers and winners"

# Calling the function above with the 24 hours period series and title DTITLE
fig, ax = top10_subplot(volatility['percent_change_24h'], DTITLE)

# Sorting in ascending order
volatility7d = volatility['percent_change_7d'].sort_values(ascending = True)

WTITLE = "Weekly top losers and winners"

# Calling the top10_subplot function
fig, ax = top10_subplot(volatility7d, WTITLE)

#Classification of CryptoCurrencies
# Function to return cap counts, pass in an argument 'market_cap_usd larger or smaller than value'
def capcount(query_string):
    #return a query for the designated size condition, returns a count of that query
    return cap.query(query_string).count().id

# Labels for the plot
LABELS = ["large", "mid", "small"]
# Using capcount count the 'large' coins
medium = capcount('market_cap_usd > 300000000')
# get the micro counts
micro = capcount('market_cap_usd < 300000000 and market_cap_usd > 50000000')
# and the nano counts
nano =  capcount('market_cap_usd < 50000000')
# Populate a list with the 3 counts
values = [large, micro, nano]

# Plot them out with matplotlib 
plt.bar(range(len(values)), values, tick_label = LABELS)
plt.title("Crypto Size Chart")
plt.ylabel("Observations")
plt.xlabel("Market Cap Size")
plt.tight_layout()
plt.show()
