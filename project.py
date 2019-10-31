import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
sns.set(style="whitegrid")
import streamlit as st

'''
# Big City Data Analysis

## Group Member:
> Jie Ni
>  
>  

'''
@st.cache
def filter_and_load_data():
    data = pd.read_csv("./dataset/BCHI-dataset_2019-03-04.csv")
    data['Value'].fillna(0,inplace=True)
    exclude_place = ["U.S. Total, U.S. Total"]
    include_sex = "Both"
    include_race = "All"
    filtered_data = data[~(data['Place'].isin(exclude_place) ) & (data['Race/Ethnicity'] == include_race) & (data['Sex'] == include_sex)]

    return filtered_data


data = filter_and_load_data()
st.dataframe(data)
# exclude_place = 'U.S. Total, U.S. Total'
population_data = data[(data['Indicator'] == 'Total Population (People)') & (data['Place'] != exclude_place)]
suicide_data = data[(data['Indicator'] == "Suicide Rate (Age-Adjusted; Per 100,000 people)") & (data['Place'] != exclude_place)]

least_populous_data = pd.merge(population_data,suicide_data, on=['Year','Sex','Race/Ethnicity','Place'], suffixes=("_pop","_suicide")).sort_values(by=['Year','Value_pop'],ascending=[True,True]).groupby("Year").head(3)
most_populous_data = pd.merge(population_data,suicide_data, on=['Year','Sex','Race/Ethnicity','Place'], suffixes=("_pop","_suicide")).sort_values(by=['Year','Value_pop'],ascending=[True,False]).groupby("Year").head(3)

fig, axes = plt.subplots(5,figsize=(10,10))
plt.tight_layout()
j = 0
for year in least_populous_data['Year'].unique():
    sns.barplot(x='Place',y='Value_suicide',data=least_populous_data[least_populous_data['Year']==year],ax=axes[j])
    j += 1

j=0
if st.checkbox("Least Populous Cities Suicide Rate"):
    st.pyplot()

for year in most_populous_data['Year'].unique():
    sns.barplot(x='Place',y='Value_suicide',data=most_populous_data[most_populous_data['Year']==year],ax=axes[j])
    j += 1

if st.checkbox("Most Populous Cities Suicide Rate"):
    st.pyplot()
#print(data.head(10))