import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from api.mongo_connection import get_all_data, get_one_data
from bson import json_util
import json

st.set_page_config(
        page_title="Dashboard",
        page_icon="📊",
)

st.image("assets/mini3.jpg", use_column_width=True)

st.title('View general statistics and insights for your store')

st.divider()
database_name = 'json'
collection_name = 'json_live_video'
documents = get_all_data(database_name, collection_name)

documents = json.loads(documents)
st.json(documents)

document_ids = [str(doc['_id']) for doc in documents]

selected_id = st.selectbox('Select Document ID', document_ids)

if selected_id:
    query = {"_id": selected_id}
    selected_document = get_one_data(query, database_name, collection_name)
    selected_document = json.loads(selected_document)
    st.write(selected_document)


st.divider()

json_file_path = 'assets/data.json' 
with open(json_file_path, 'r') as file:
    data = json.load(file)

records = []
for entry in data:
    frame = entry['frame']
    for prediction in entry['predictions']:
        record = {
            'frame': frame,
            'x': prediction['x'],
            'y': prediction['y'],
            'width': prediction['width'],
            'height': prediction['height'],
            'confidence': prediction['confidence'],
            'class': prediction['class'],
            'level': prediction['level']
        }
        records.append(record)

df = pd.DataFrame(records)

# Create a new column for 5-frame intervals
df['frame_interval'] = (df['frame'] // 5) * 5

# Group by frame_interval and class, then count occurrences
class_counts = df.groupby(['frame_interval', 'class']).size().unstack(fill_value=0)

# Determine the predominant class for each interval
predominant_class = class_counts.idxmax(axis=1)
predominant_class_counts = class_counts.max(axis=1)

# Create a DataFrame for plotting
plot_data = pd.DataFrame({
    'frame_interval': predominant_class.index,
    'predominant_class': predominant_class.values,
    'count': predominant_class_counts.values
})

# Plot: Scatter Plot of Normal, Dangerous, Suspicious over Frames
fig, ax = plt.subplots()
colors = {'normal': 'blue', 'dangerous': 'red', 'suspicious': 'orange'}

for class_name in ['normal', 'dangerous', 'suspicious']:
    class_data = df[df['level'] == class_name]
    ax.scatter(class_data['frame'], class_data['confidence'], label=class_name, color=colors[class_name], alpha=0.5)

ax.set_title('Scatter Plot of Normal, Dangerous, Suspicious over Frames')
ax.set_xlabel('Frame')
ax.set_ylabel('Confidence')
ax.legend(title='Level')
st.pyplot(fig)

# Plot: Histogram of Level Field for Dangerous, Suspicious, and Normal
fig2, ax2 = plt.subplots()
levels = ['normal', 'dangerous', 'suspicious']
colors = {'normal': 'blue', 'dangerous': 'red', 'suspicious': 'orange'}

for level in levels:
    level_data = df[df['level'] == level]
    ax2.hist(level_data['level'], bins=10, alpha=0.5, label=level, color=colors[level])

ax2.set_title('Histogram of Level Field for Dangerous, Suspicious, and Normal')
ax2.set_xlabel('Level')
ax2.set_ylabel('Frequency')
ax2.legend(title='Level')
st.pyplot(fig2)

# Plot: Timeline of Confidence Values
fig3, ax3 = plt.subplots()
for class_name in ['normal', 'dangerous', 'suspicious']:
    if class_name in df['level'].unique():
        class_data = df[df['level'] == class_name]
        ax3.plot(class_data['frame'], class_data['confidence'], label=class_name, color=colors[class_name], alpha=0.5)

ax3.set_title('Timeline of Confidence Values')
ax3.set_xlabel('Frame')
ax3.set_ylabel('Confidence')
ax3.set_ylim(0, 1)
ax3.legend(title='Level')
st.pyplot(fig3)