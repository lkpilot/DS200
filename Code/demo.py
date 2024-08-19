import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np
from datetime import datetime
import time

data_1 = pd.DataFrame({
    'Aspect': ['Character - Outlook',
               'Character - Outlook',
               'Character - Outlook',
               'Character - Voice',
               'Character - Voice',
               'Character - Voice',
               'Character - Overall',
               'Character - Overall',
               'Character - Overall'],
    'Count': [0, 0, 0, 0, 0, 0, 0, 0, 0],
    'Sentiment': ['Negative', 'Positive','Neutral', 'Negative', 'Positive', 'Neutral', 'Negative',  'Positive',  'Neutral']
})

data_2 = pd.DataFrame({
    'Aspect': ['Character - Outlook',
               'Character - Outlook',
               'Character - Outlook',
               'Character - Voice',
               'Character - Voice',
               'Character - Voice',
               'Character - Overall',
               'Character - Overall',
               'Character - Overall'],
    'Count': [0, 0, 0, 0, 0, 0, 0, 0, 0],
    'Sentiment': ['Negative', 'Positive','Neutral', 'Negative', 'Positive', 'Neutral', 'Negative',  'Positive',  'Neutral']
})

ac_map = {
    'Character - Outlook': 0,
    'Character - Voice': 1,
    'Character - Overall': 2
}

sp_map = {
    'negative': 0,
    'positive': 1,
    'neutral': 2
}

data = {
    'data_1': data_1,
    'data_2': data_2
}

Candidate_name = [['tuimi', 'Tuimi', 'tumi', ''],
                  ['Rich', 'Richchoi', 'rich', 'richchoi']]
                  #if there are more candidates, add their names here

df = pd.DataFrame(columns=['Comments', 'Aspect Category', 'Aspect Term', 'Sentiment Polarity', 'Opinion Term'])

st.title("Rap Viet and King of Rap Aspects and Sentiment Visualization")

st.markdown("<h2 style='text-align: center; color: black;'>Candidate Statistics </h2>", unsafe_allow_html=True)

now = datetime.now()
dt_string = now.strftime("%d %B %Y %H:%M:%S")
st.write(f"Last update: {dt_string}")

if not "sleep_time" in st.session_state:
    st.session_state.sleep_time = 5

if not "auto_refresh" in st.session_state:
    st.session_state.auto_refresh = True

mapping = {
    "1 hour": {"period": "60", "granularity": "minute", "raw": 60},
    "30 minutes": {"period": "30", "granularity": "minute", "raw": 30},
    "10 minutes": {"period": "10", "granularity": "minute", "raw": 10},
    "5 minutes": {"period": "5", "granularity": "minute", "raw": 5}
}

with st.expander("Configure Dashboard", expanded=True):
    left, right = st.columns(2)

    with left:
        auto_refresh = st.checkbox('Auto Refresh?', st.session_state.auto_refresh)

        if auto_refresh:
            number = st.number_input('Refresh rate in seconds', value=st.session_state.sleep_time)
            st.session_state.sleep_time = number

    with right:
            time_ago = st.radio("Time period to cover", mapping.keys(), horizontal=True, key="time_ago")
            

st.header("Live Kafka Statistics" ) 

a = pd.read_csv(r'C:\Users\nguye\Downloads\data_result.csv')
st.write(a)

for i in range(len(a)):
    if a['Aspect Term'][i] in Candidate_name[0]:
        ac = ac_map[a['Aspect Category'][i]]
        sp = sp_map[a['Sentiment Polarity'][i]]
        data_1.loc[3 * ac + sp, 'Count'] = data_1.loc[3 * ac + sp, 'Count'] + 1
    
    elif a['Aspect Term'][i] in Candidate_name[1]:
        ac = ac_map[a['Aspect Category'][i]]
        sp = sp_map[a['Sentiment Polarity'][i]]
        data_2.loc[3 * ac + sp, 'Count'] = data_2.loc[3 * ac + sp, 'Count'] + 1
    
fig, ax = plt.subplots(1, 2, figsize=(10, 4))

cols = ['data_1', 'data_2']
name_candidate = ['Tuimi', 'Rich Choi']
for i, res in enumerate(cols):
  ax = plt.subplot(1, 2, i+1)
  #ax = data[res].plot(y=['Negative', 'Positive', 'Neutral'],use_index=True, kind="bar", color=my_colors)
  ax = sns.barplot(data[res], x='Aspect', y='Count', hue='Sentiment', palette='YlGn')
  ax.set_title(name_candidate[i])
plt.subplots_adjust(wspace=.3, hspace=.3)

st.pyplot(fig)

minute = mapping[time_ago]["period"]
print(str(minute))

if auto_refresh:
    time.sleep(number)
    st.experimental_rerun()