import pandas as pd
import numpy as np
import matplotlib.pyplot as plt 

c = pd.read_csv('Comcast_telecom_complaints_data.csv')
c = pd.DataFrame(c)
c.head(n=1)

num_complaints_daily = c.groupby(by=["Date_month_year"], dropna=False).count()
daily_complaints = num_complaints_daily['Customer Complaint']
daily_complaints

date_list = c['Date_month_year'].str.split('-', n=-1, expand=False)

months = []
for date in date_list:
    months.append(date[1])

c['months'] = months
c = c.reindex(columns=['Ticket #', 'Customer Complaint', 'Date', 'Date_month_year', 'months', 'Time', 'Received Via', 'City', 'State', 'Zip code', 'Status', 'Filing on Behalf of Someone'])
c.head()

num_complaints_monthly = c.groupby(by=["months"], dropna=False).count()
monthly_complaints = num_complaints_monthly['Customer Complaint']
monthly_complaints

pd.set_option('display.max_rows', 15)
fct = pd.DataFrame(c['Customer Complaint'].value_counts().reset_index())
freq_complaint_types = fct.rename(columns={'index':'complaint type', 'Customer Complaint':'count'})
freq_complaint_types

status = []
for index, row in c.iterrows():
    if row['Status'] == 'Open' or row['Status'] == 'Pending':
        status.append('Open')
    elif row['Status'] == 'Closed' or row['Status'] == 'Solved':
       status.append('Closed')

c['Status Value'] = status
c.head()

complaints_by_state = c.groupby(by=["State"], dropna=False).count()
cbs = complaints_by_state.reset_index()

total_num_complaints = []
for index, row in cbs.iterrows():
    total_num_complaints.append(row['Customer Complaint'])

cbs['Total Complaints'] = total_num_complaints
cbs.head()








# Which state has the maximum complaints - Georgia

data = {}
for index, row in cbs.iterrows():
    data[row['State']] = row['Customer Complaint']
  
state = list(data.keys())
count = list(data.values())

fig = plt.figure(figsize = (30, 10))
plt.bar(state, count, color ='maroon',
        width = 0.4)
 
plt.xlabel("State")
plt.xticks(rotation=30)
plt.ylabel("No. of Complaints ")
plt.title("No. of Complaints by State")
plt.show()







# Which state has the highest percentage of unresolved complaints - Kansas
total_complaints = cbs[['State', 'Total Complaints']]
complaints_by_state_status = c.groupby(by=["State", 'Status Value'], dropna=False).count()
cbss = pd.DataFrame(complaints_by_state_status['Customer Complaint'])
cbss.head()
cbss = cbss.reset_index()

cbss = cbss.merge(total_complaints, on='State')

percentage = []
for index, row in cbss.iterrows():
    perc = round((row['Customer Complaint']/row['Total Complaints'])*100, 1)
    percentage.append(perc)

cbss['Percentage'] = percentage
open_complaints = cbss.loc[cbss['Status Value'] == 'Open']

state = list(open_complaints['State'])
perc_closed = list(open_complaints['Percentage'])

fig = plt.figure(figsize = (30, 10))
plt.bar(state, perc_closed, color ='maroon',
        width = 0.4)
 
plt.xlabel("State")
plt.xticks(rotation=30)
plt.ylabel("Percent of Complaints ")
plt.title("Percentage of Open Complaints by State")
plt.show()







perc_resolved = c.groupby(by=["Status Value"], dropna=False).count()
resolved = perc_resolved.drop(columns='Total Complaints')
resolved = resolved['Customer Complaint']
res = pd.DataFrame(resolved).reset_index()
res.columns = ['Status', 'Num Complaints']
total = res['Num Complaints'].sum()
res['Percent Total'] = round(((res['Num Complaints']/total)*100), 1)
res