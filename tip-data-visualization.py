import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import datetime
import csv

File_Name="data.csv"
NonNumerical=['sex','smoker','day','time']

# My Professor wrote this portion for the class:
def CSV_Data_Reader(File_Name, Seprator, NonNumerical):
  with open(File_Name) as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=Seprator)
    line_count=0
    Data=[]
    for row in csv_reader:
      if line_count==0:
        Header=row
      else:
        Data.append(row)
      line_count=line_count+1

  Data_dict={}

  idx=0
  for name in Header:
    Data_dict[name]=[]
    for row in Data:
      if name in NonNumerical:
        Data_dict[name].append(row[idx])
      else:
        if row[idx].replace('.','').isdigit():
          Data_dict[name].append(float(row[idx]))
        else:
          Data_dict[name].append(None)
    idx=idx+1
  return Data_dict
# =============================================================

# My code begins:

# Cut data we aren't using
Data=CSV_Data_Reader(File_Name, ",", NonNumerical)
DataCut={}
for i in Data:
  if i in ['tip','day','size']:
      DataCut[i]=Data[i]

plt.title("Greatest Tip Per Day")
plt.xlabel("day")
plt.ylabel("max tip")
plt.bar(DataCut['day'],DataCut['tip'])
plt.show()

plt.title("test")
plt.xlabel("tip amount")
plt.ylabel("number recorded")
plt.hist(DataCut['tip'])
plt.show()

plt.title("test")
plt.xlabel("tip amount")
plt.ylabel("size of table")
plt.scatter(DataCut['tip'],DataCut['size'])
plt.show()

# Group the data for each day
DataGrouped={'day':['Thur', 'Fri', 'Sat', 'Sun'], 'tip':[[] for i in range(4)], 'size':[[] for i in range (4)]}
for i in range(len(DataCut['day'])):
  if DataCut['day'][i]=='Thur':
    DataGrouped['tip'][0].append(DataCut['tip'][i])
    DataGrouped['size'][0].append(DataCut['size'][i])
  elif DataCut['day'][i]=='Fri':
    DataGrouped['tip'][1].append(DataCut['tip'][i])
    DataGrouped['size'][1].append(DataCut['size'][i])
  elif DataCut['day'][i]=='Sat':
    DataGrouped['tip'][2].append(DataCut['tip'][i])
    DataGrouped['size'][2].append(DataCut['size'][i])
  else:
    DataGrouped['tip'][3].append(DataCut['tip'][i])
    DataGrouped['size'][3].append(DataCut['size'][i])

# Calculate statistics for each day
Stats={'day':['Thur', 'Fri', 'Sat', 'Sun'], 'tip_AVG':[], 'tip_Max':[], 'size_Count':[]}
for i in range(4):
  Stats['tip_AVG'].append(sum(DataGrouped['tip'][i])/len(DataGrouped['tip'][i]))
  Stats['tip_Max'].append(max(DataGrouped['tip'][i]))
  Stats['size_Count'].append(sum(DataGrouped['size'][i]))

plt.plot(Stats['day'],Stats['size_Count'])
plt.scatter(Stats['day'],Stats['size_Count'])
plt.title("Number of customers recorded for each day")
plt.xlabel("Weekday")
plt.ylabel("Count")
plt.show()

plt.scatter(Stats['day'],Stats['tip_AVG'])
plt.plot(Stats['day'],Stats['tip_AVG'])
plt.title("Average Tip% for each day")
plt.xlabel("Weekday")
plt.ylabel("Average Tip%")
plt.show()

plt.scatter(Stats['day'],Stats['tip_Max'])
plt.plot(Stats['day'],Stats['tip_Max'])
plt.title("Maximum Tip% for each day")
plt.xlabel("Weekday")
plt.ylabel("Max Tip%")
plt.show()

# Compare manual calculations to pandas
df=pd.read_csv('data.csv')
df = df.dropna(thresh=3, subset=['day', 'tip', 'size'])
df['day'] = pd.Categorical(df['day'],categories=['Thur','Fri','Sat','Sun'],ordered=True)

plt.scatter(Stats['day'], Stats['size_Count'])
plt.plot(Stats['day'], df.groupby(df.day)['size'].sum(),c='orange')
plt.title("Comparison of Manual calculation and Pandas calculation on number of customers per day")
plt.xlabel("Weekday")
plt.ylabel("Count")
plt.legend(["Manual calculation", "pandas"])
plt.show()

