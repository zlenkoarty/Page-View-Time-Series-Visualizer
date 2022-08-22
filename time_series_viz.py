import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns


# Import data from csv and parse dates 
df = pd.read_csv("fcc-forum-pageviews.csv", parse_dates=['date'], index_col='date')

# Clean data by quantile (upper and lower)
df = df.loc[(df['value'] >= df['value'].quantile(0.025)) & 
            (df['value'] <= df['value'].quantile(0.975))]

fig, ax = plt.subplots(figsize=(32, 10), dpi=100)
ax.set_title("Daily freeCodeCamp Forum Page Views 5/2016-12/2019")
ax.set_xlabel("Date")
ax.set_ylabel("Page Views")
sns.lineplot(data=df, legend=False)
fig.savefig('line_plot.png')

#Groupping data by Year and Month for bar plot
df['Month']=pd.DatetimeIndex(df.index).month_name()
df['Year']=pd.DatetimeIndex(df.index).year
df_bar = df.groupby(['Year', 'Month'], sort=False).agg(value=('value', 'mean'))['value'].round().astype(int).reset_index()
df_bar = df_bar.rename(columns={"value": "Average Page Views"})

#Cause data have not full 2016 year we are adding missing data
missing_months = {
        "Year": [2016, 2016, 2016, 2016],
        "Month": ['January', 'February', 'March', 'April'],
        "Average Page Views": [0, 0, 0, 0]
    }

df_bar = pd.concat([pd.DataFrame(missing_months), df_bar])

fig, ax = plt.subplots(figsize=(18, 10), dpi=100)
ax.set_title("Daily freeCodeCamp Forum Average Page Views per Month")

chart = sns.barplot(data=df_bar, x="Year", y="Average Page Views", hue="Month", palette="tab10")
chart.set_xticklabels(chart.get_xticklabels(), rotation=90, horizontalalignment='center')
fig.savefig('bar_plot.png')

#Copy dataframe for box plot
df_box = df

# Draw box plots (using Seaborn)
fig, axes = plt.subplots(1, 2, figsize=(32, 10), dpi=100)

# Yearly boxplot
sns.boxplot(data=df_box, x="Year", y="value", ax=axes[0])
axes[0].set_title("Year-wise Box Plot (Trend)")
axes[0].set_xlabel("Year")
axes[0].set_ylabel("Page Views")

# Monthly boxplot
month_order = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
sns.boxplot(data=df_box, x="Month", y="value",ax=axes[1])
axes[1].set_title("Month-wise Box Plot (Seasonality)")
axes[1].set_xlabel("Month")
axes[1].set_ylabel("Page Views")

# Save image and return fig (don't change this part)
fig.savefig('box_plot.png')

