#!/usr/bin/env python
# coding: utf-8

# In[11]:


import streamlit as st
import pandas as pd
import plotly.express as px

# Set Page Config (Professional Branding)
st.set_page_config(page_title="Beauty Campaign Optimizer", layout="wide")

st.title("💄 Nano-Influencer Campaign ROI Dashboard")
st.markdown("### Strategic Insights for Customer Success Managers")

# Load our processed data
@st.cache_data # This keeps the app fast
def load_data():
    return pd.read_csv("data/processed/final_campaign_analysis.csv")

df = load_data()


# In[12]:


st.sidebar.header("Filter Campaign Data")

selected_market = st.sidebar.multiselect(
    "Select Market:", options=df['market'].unique(), default=df['market'].unique()
)

selected_category = st.sidebar.multiselect(
    "Select Category:", options=df['category'].unique(), default=df['category'].unique()
)

# Filter the dataframe based on selection
mask = (df['market'].isin(selected_market)) & (df['category'].isin(selected_category))
filtered_df = df[mask]


# In[13]:


col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Total Engagement", f"{filtered_df['total_engagement'].sum():,}")
with col2:
    st.metric("Avg Engagement Rate", f"{filtered_df['er'].mean():.2f}%")
with col3:
    st.metric("Avg CPE (Cost per Engagement)", f"${filtered_df['cpe'].mean():.2f}")

st.divider()


# In[14]:


st.subheader("Which Rewards Drive the Best ROI?")

# Logic: Group by reward type to see which is most efficient
reward_analysis = filtered_df.groupby('reward_type')['cpe'].mean().reset_index()

fig = px.bar(
    reward_analysis, 
    x='reward_type', 
    y='cpe', 
    title="Average Cost per Engagement by Reward",
    labels={'cpe': 'Cost Per Engagement ($)', 'reward_type': 'Reward Tier'},
    color_discrete_sequence=['#ff4b4b']
)
st.plotly_chart(fig, use_container_width=True)


# In[15]:


st.subheader("Tactical Recommendations")

# Identify the most efficient creator in the filtered view
top_creator = filtered_df.sort_values(by='cpe').iloc[0]

st.info(f"""
**Optimization Tips for this Selection:**
- **Scale Up:** Creator **{top_creator['name']}** is your most efficient partner with a CPE of ${top_creator['cpe']:.2f}.
- **Budget Shift:** If CPE is high, consider moving from 'Exclusive Kits' to 'Full Size Sets' to lower the cost-per-interaction.
- **Content Strategy:** Markets like {filtered_df.groupby('market')['er'].mean().idxmax()} are showing peak engagement; prioritize these for the next product launch.
""")


# In[ ]:




