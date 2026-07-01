import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import squarify

df = pd.read_csv("clean_jobs.csv")

st.title("Job Market Intelligence Dashboard")

st.subheader("Overview")

col1,col2,col3=st.columns(3)

with col1:
    st.metric("Total Jobs",len(df))

with col2:
    st.metric("Comapanies",df["company_name"].nunique())

with col3:
    st.metric("Locations",df["location"].nunique())

st.subheader("Top Job Titles")

top_jobs=(df["title"].value_counts().head(10))

fig,ax=plt.subplots(figsize=(8,6))

ax.barh(top_jobs.index,top_jobs.values)
ax.set_title("Top 10 Jobs")
ax.set_xlabel("Count")
st.pyplot(fig)

#Top Hiring Locations

st.subheader("Top Hiring Locations")

top_locations=(df["location"].value_counts().head(10))

fig,ax=plt.subplots(figsize=(10,6))

ax.bar(top_locations.index,top_locations.values)
ax.set_title("Top Hiring Locations")
ax.set_ylabel("Number of Jobs")
plt.xticks(rotation=45)
st.pyplot(fig)

#Work Type Distribution
st.subheader("Work Type Distribution")

work=(df["formatted_work_type"].value_counts())

fig,ax=plt.subplots(figsize=(12,6))
squarify.plot(sizes=work.values,label=work.index,alpha=0.8)
st.pyplot(fig)

#Salary Distribution
st.subheader("Salary Distribution (>10K)")
salary_df=(df.dropna(subset=["med_salary"]))

upper=(salary_df["med_salary"].quantile(0.95))
filtered=(salary_df[salary_df["med_salary"]<=upper])

fig,ax=plt.subplots(figsize=(10,6))
ax.hist(
    filtered[
        filtered["med_salary"] > 10000
    ]["med_salary"],
    bins=25
)
ax.set_title("Median Salary Distribution")
ax.set_xlabel("Salary")
ax.set_ylabel("Jobs")
st.pyplot(fig)

#View vs Applications
st.subheader("Views vs Applications")
sample=(df[["views","applies"]].sample(3000))

fig,ax=plt.subplots(figsize=(10,6))
ax.scatter(sample["views"],sample["applies"],alpha=0.4,)
ax.set_title("Views vs Applications")
ax.set_xlabel("Views")
ax.set_ylabel("Applications")
st.pyplot(fig)

#SIDEBAR
st.sidebar.title("Filters")

selected_work=(st.sidebar.selectbox("Work Type",["All"]+list(df["formatted_work_type"].dropna().unique())))

if selected_work !="All":
    df=(df[df["formatted_work_type"]==selected_work])

#SEAECH BOX
search=(st.sidebar.text_input("Search Job Title"))

if search:
    df=(df[df["title"].str.contains(search,case=False,na=False)])

st.subheader(
    "Dataset Preview"
)

st.dataframe(
    df.head(20)
)

st.markdown("---")
st.caption("Built using Python • Pandas • Streamlit")